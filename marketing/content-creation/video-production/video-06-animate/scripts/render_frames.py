#!/usr/bin/env python3
"""
Deterministic frame-by-frame capture of an HTML animation.

Steps a page through virtual time and screenshots each frame. Because time is an input
rather than something that elapses, the output is identical no matter how slowly the
capture runs -- which is what makes 4K feasible.

The page must expose a render contract (see references/render-contract.md):
  Mode A: CSS/WAAPI animations, driven via document.getAnimations()
  Mode B: window.__renderAt(t)  -- t in seconds
Both may be present; both are applied, A then B.

If window.__segments is set (see assets/harness.js Timeline), a manifest is written
alongside the frames with in/out frames and timecode for every slot -- so you aren't
scrubbing in After Effects hunting for where each animation starts.

Usage:
  python render_frames.py --file design.html    --check-fit    # run this FIRST
  python render_frames.py --file animation.html --verify
  python render_frames.py --file animation.html --check-holds
  python render_frames.py --file animation.html --fps 25 --out frames/
  python render_frames.py --file dash.html --layers --alpha --out layers/

Requires: pip install playwright && playwright install chromium
"""

import argparse
import hashlib
import json
import pathlib
import shutil
import sys
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright not installed.\n  pip install playwright\n  playwright install chromium")


# Injected before any page script runs. Removes every source of wall-clock
# non-determinism so two renders of the same timeline are byte-identical.
DETERMINISM_SHIM = """
(() => {
  let seed = 0x9E3779B9;
  Math.random = function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const FIXED = 1700000000000;
  const RealDate = Date;
  Date.now = () => FIXED;
  window.Date = class extends RealDate {
    constructor(...args) { super(...(args.length ? args : [FIXED])); }
    static now() { return FIXED; }
  };
  if (window.performance) performance.now = () => 0;
})();
"""

# Applied per frame. Scrubs every WAAPI/CSS animation to the given time, then calls
# __renderAt if present. Re-scans each frame so late-mounting elements are caught.
SCRUB = """
(t) => {
  for (const a of document.getAnimations()) {
    try { a.pause(); a.currentTime = t * 1000; } catch (e) { /* unresolved */ }
  }
  if (typeof window.__renderAt === 'function') window.__renderAt(t);
}
"""


# Measures the fitted design against the frame. Geometry only -- no judgment, no
# screenshots to squint at. Answers: does anything leave the frame, is anything below
# the legibility floor, and how much of the frame is the content actually using.
FIT_CHECK = r"""
(cfg) => {
  const W = cfg.w, H = cfg.h, S = cfg.safe;
  const out = {
    doc: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
    cropped: [], outside: [], smallType: [], thinStroke: [], counted: 0, bbox: null,
  };
  const MEDIA = new Set(['IMG', 'SVG', 'CANVAS', 'VIDEO', 'PICTURE']);
  const R = (r) => [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)];

  const label = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    else if (el.classList && el.classList.length) s += '.' + [...el.classList].slice(0, 2).join('.');
    const t = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 44);
    return t ? s + ' "' + t + '"' : s;
  };

  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;

  for (const el of document.querySelectorAll('*')) {
    const tag = el.tagName.toUpperCase();
    if (tag === 'HTML' || tag === 'BODY' || tag === 'SCRIPT' || tag === 'STYLE') continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;

    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    const isMedia = MEDIA.has(tag);
    const inSvg = !!el.ownerSVGElement;
    const svgInk = inSvg && ((cs.fill && cs.fill !== 'none') || (cs.stroke && cs.stroke !== 'none'));
    const isContent = hasText || isMedia || svgInk;
    const painted = isContent ||
      (cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)') ||
      cs.backgroundImage !== 'none' ||
      parseFloat(cs.borderTopWidth) > 0 || parseFloat(cs.borderLeftWidth) > 0;
    if (!painted) continue;
    out.counted++;

    // Content extent, not background extent -- a full-bleed background would otherwise
    // report 100% coverage on a design that is actually pillarboxed.
    if (isContent) {
      x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top);
      x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom);
    }

    if (r.left < -0.5 || r.top < -0.5 || r.right > W + 0.5 || r.bottom > H + 0.5) {
      out.cropped.push({ el: label(el), text: hasText, media: isMedia, rect: R(r) });
    } else if (isContent &&
               (r.left < S[3] - 0.5 || r.top < S[0] - 0.5 ||
                r.right > W - S[1] + 0.5 || r.bottom > H - S[2] + 0.5)) {
      out.outside.push({ el: label(el), rect: R(r) });
    }

    if (hasText) {
      const fs = parseFloat(cs.fontSize);
      if (fs < cfg.typeFloor - 0.01) out.smallType.push({ el: label(el), px: Math.round(fs * 10) / 10 });
    }
    const widths = [cs.borderTopWidth, cs.borderRightWidth, cs.borderBottomWidth, cs.borderLeftWidth];
    if (inSvg && cs.stroke && cs.stroke !== 'none') widths.push(cs.strokeWidth);
    for (const w of widths) {
      const bw = parseFloat(w);
      if (bw > 0.01 && bw < cfg.strokeFloor - 0.01) {
        out.thinStroke.push({ el: label(el), px: Math.round(bw * 100) / 100 });
        break;
      }
    }
  }

  if (x1 > x0) out.bbox = [Math.round(x0), Math.round(y0), Math.round(x1), Math.round(y1)];
  return out;
}
"""


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def tc(frame, fps):
    """Timecode, non-drop. Exact at 25 and 50."""
    f = int(round(frame))
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(
        f // (3600 * fps), (f // (60 * fps)) % 60, (f // fps) % 60, f % fps
    )


def shoot(page, capture, path, alpha):
    capture.screenshot(path=str(path), omit_background=alpha)


def write_manifest(segments, fps, out, compact=False):
    """segments.json / .csv / .md next to the frames, for the edit."""
    rows = []
    for s in segments:
        target = s.get("targetFrame", s["startFrame"])
        rows.append({
            "name": s["name"],
            "render_in_frame": s["startFrame"],
            "render_out_frame": s["endFrame"],
            "render_in_tc": tc(s["startFrame"], fps),
            "render_out_tc": tc(s["endFrame"], fps),
            "place_at_tc": tc(target, fps),
            "place_at_frame": target,
            "anim_frames": s["endFrame"] - s["startFrame"],
            "hold_frames": s["holdEndFrame"] - s["endFrame"],
        })

    (out / "segments.json").write_text(
        json.dumps({"fps": fps, "compact": compact, "segments": rows}, indent=2))

    cols = ["name", "render_in_tc", "render_out_tc", "place_at_tc",
            "render_in_frame", "render_out_frame", "place_at_frame",
            "anim_frames", "hold_frames"]
    csv = [",".join(cols)]
    csv += [",".join(str(r[c]) for c in cols) for r in rows]
    (out / "segments.csv").write_text("\n".join(csv) + "\n")

    md = [f"# Segments ({fps} fps{', compact' if compact else ''})", ""]
    if compact:
        md += ["Rendered compactly: holds are collapsed. **Place at** is where each segment",
               "belongs in the finished video; **renders at** is where it sits in this file.",
               "Time-remap from one to the other.", ""]
    md += ["| Slot | Renders at | Out | Place at | Anim | Hold |", "|---|---|---|---|---|---|"]
    md += [f"| {r['name']} | {r['render_in_tc']} | {r['render_out_tc']} | {r['place_at_tc']} "
           f"| {r['anim_frames']}f | {r['hold_frames']}f |" for r in rows]
    (out / "segments.md").write_text("\n".join(md) + "\n")

    print(f"manifest: {len(rows)} slots -> segments.json / .csv / .md")
    for r in rows:
        arrow = f" -> place at {r['place_at_tc']}" if compact else ""
        print(f"  {r['name']:<14} {r['render_in_tc']}  {r['anim_frames']:>4}f anim"
              f"  {r['hold_frames']:>4}f hold{arrow}")


def report_fit(rep, w, h, safe, type_floor, stroke_floor, still):
    """Print the fit report. Returns True if the design is ready to animate."""
    cw, ch = w - safe[1] - safe[3], h - safe[0] - safe[2]
    print(f"fit check {w}x{h}  safe box {cw}x{ch} "
          f"(margins t{safe[0]:g} r{safe[1]:g} b{safe[2]:g} l{safe[3]:g})")
    print(f"  floors:   type {type_floor:g}px   stroke {stroke_floor:g}px")
    print(f"  document: {rep['doc'][0]}x{rep['doc'][1]}   elements measured: {rep['counted']}")

    fails, warns = [], []

    if rep["bbox"]:
        x0, y0, x1, y1 = rep["bbox"]
        bw, bh = x1 - x0, y1 - y0
        print(f"  content:  x {x0}..{x1}  y {y0}..{y1}  -> {bw}x{bh} "
              f"({bw / w:.0%} of frame width, {bh / h:.0%} of height)")
        if bw / w < 0.75:
            warns.append(f"content uses only {bw / w:.0%} of the frame width -- {w - bw}px "
                         f"of horizontal slack unused.\n"
                         "      Uniform scaling is leaving the frame empty and holding type "
                         "smaller than it needs to be.\n"
                         "      Relayout across the width instead of scaling to fit.")
        elif bh / h < 0.55:
            warns.append(f"content uses only {bh / h:.0%} of the frame height -- "
                         f"{h - bh}px of vertical slack unused.")

    text_cropped = [c for c in rep["cropped"] if c["text"] or c["media"]]
    if text_cropped:
        fails.append((f"{len(text_cropped)} content element(s) cross the frame edge -- "
                      "this is the failure that cuts titles",
                      [f"{c['el']}  rect {c['rect']}" for c in text_cropped]))
    bg_cropped = [c for c in rep["cropped"] if not (c["text"] or c["media"])]
    if bg_cropped:
        warns.append(f"{len(bg_cropped)} container/background element(s) extend past the frame "
                     "(fine if the bleed is deliberate)")

    if rep["smallType"]:
        fails.append((f"{len(rep['smallType'])} text element(s) below the {type_floor:g}px "
                      "legibility floor",
                      [f"{s['el']}  {s['px']:g}px" for s in rep["smallType"]]))

    if rep["outside"]:
        warns.append(f"{len(rep['outside'])} content element(s) inside the frame but outside the "
                     f"safe box:\n" +
                     "\n".join(f"      {o['el']}  rect {o['rect']}" for o in rep["outside"][:8]))
    if rep["thinStroke"]:
        warns.append(f"{len(rep['thinStroke'])} stroke(s) below {stroke_floor:g}px -- these "
                     "shimmer or vanish on motion:\n" +
                     "\n".join(f"      {t['el']}  {t['px']:g}px" for t in rep["thinStroke"][:8]))

    for msg, items in fails:
        print(f"\nFAIL  {msg}:")
        for i in items[:12]:
            print(f"      {i}")
        if len(items) > 12:
            print(f"      ... and {len(items) - 12} more")
    for msg in warns:
        print(f"\nWARN  {msg}")

    print()
    if still:
        print(f"still: {still}  -- show this to the user before animating")
    if fails:
        print("NOT READY TO ANIMATE. Reflow the design; never crop to fit. "
              "See references/canvas-fit.md.")
        return False
    print("PASS - the design fits the frame. Animate now.")
    return True


def main():
    p = argparse.ArgumentParser(description="Frame-step an HTML animation to a PNG sequence.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="local HTML file")
    src.add_argument("--url", help="URL to load")

    p.add_argument("--fps", type=int, default=25, help="frames per second (default 25)")
    p.add_argument("--duration", type=float, default=None,
                   help="seconds; defaults to window.__duration")
    p.add_argument("--start", type=float, default=0.0, help="start time in seconds")
    p.add_argument("--width", type=int, default=1920,
                   help="design canvas width in CSS px (default 1920)")
    p.add_argument("--height", type=int, default=1080,
                   help="design canvas height in CSS px (default 1080)")
    p.add_argument("--scale", type=float, default=2.0,
                   help="device scale factor. Output = width*scale x height*scale. "
                        "The default 1920x1080 @2x outputs 3840x2160. Only pass this "
                        "if the design is authored in a different CSS coordinate space: "
                        "a 4K-native design needs --width 3840 --height 2160 --scale 1 "
                        "(same output). Do not combine a 4K canvas with --scale 2")
    p.add_argument("--out", default="frames", help="output directory")
    p.add_argument("--alpha", action="store_true", help="transparent background")
    p.add_argument("--selector", default=None, help="capture only this element")
    p.add_argument("--layers", action="store_true",
                   help="render each selector in window.__layers to its own subdirectory")
    p.add_argument("--headed", action="store_true", help="run headed (font differences)")
    p.add_argument("--check-fit", action="store_true",
                   help="measure the design against the frame before animating: what leaves "
                        "the frame, what is below the type floor, how much of the frame is "
                        "used. Needs no render contract. Also writes fit-check.png")
    p.add_argument("--type-floor", type=float, default=None,
                   help="minimum legible font size in CSS px (default 2.5%% of frame height "
                        "= 27px on the default 1920x1080 canvas, 54px on a 4K-native one). "
                        "Use 48 for 9:16 panels placed at 56.25%% (96 if 4K-native)")
    p.add_argument("--safe", default=None,
                   help="safe-box margins as T,R,B,L in CSS px "
                        "(default 5%%,5%%,15%%,5%% of the frame -- the bottom band is subtitles)")
    p.add_argument("--verify", action="store_true",
                   help="render one frame twice and compare -- run once per new animation")
    p.add_argument("--check-holds", action="store_true",
                   help="confirm every hold region is static; run before a long render")
    p.add_argument("--clean", action="store_true", help="wipe the output directory first")
    p.add_argument("--allow-oversize", action="store_true",
                   help="permit an output larger than 3840x2160; only for a deliberate "
                        "over-render, and expect 4x the disk and render time")
    args = p.parse_args()

    # Output size is width*scale, not width. Combining a 4K canvas with the default
    # 2x scale silently produces 7680x4320 -- 4x the pixels, 4x the disk, 4x the time.
    out_w, out_h = int(args.width * args.scale), int(args.height * args.scale)
    if (out_w > 3840 or out_h > 2160) and not args.allow_oversize:
        sys.exit(
            f"output would be {out_w}x{out_h}, larger than 3840x2160.\n"
            f"  --width/--height are CSS pixels (the design's own coordinate space);\n"
            f"  --scale multiplies them into real pixels. You asked for "
            f"{args.width}x{args.height} @{args.scale:g}x.\n"
            f"  For a design authored at {args.width}x{args.height}, use --scale "
            f"{min(3840 / args.width, 2160 / args.height):g}.\n"
            f"  Pass --allow-oversize if you really want it."
        )

    if args.file:
        f = pathlib.Path(args.file).resolve()
        if not f.exists():
            sys.exit(f"not found: {f}")
        target = f.as_uri()
    else:
        target = args.url

    out = pathlib.Path(args.out)
    if args.clean and out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.headed)
        ctx = browser.new_context(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
        )
        ctx.add_init_script(DETERMINISM_SHIM)
        page = ctx.new_page()
        page.goto(target, wait_until="networkidle")

        # Fonts must be ready before frame 0 or the first frames use a fallback face.
        page.evaluate("() => document.fonts.ready")
        page.wait_for_timeout(200)

        # ---- fit the design to the frame (runs before any animation exists) -----
        if args.check_fit:
            type_floor = args.type_floor if args.type_floor else args.height * 0.025
            stroke_floor = max(1.0, args.height / 1080.0)
            if args.safe:
                safe = [float(v) for v in args.safe.split(",")]
                if len(safe) != 4:
                    sys.exit("--safe takes four values: T,R,B,L")
            else:
                safe = [args.height * 0.05, args.width * 0.05,
                        args.height * 0.15, args.width * 0.05]

            # If motion is already wired up, measure the settled end state -- mid-flight
            # elements are legitimately off-frame and would report as cropped.
            d = args.duration or page.evaluate("() => window.__duration || null")
            if d and (page.evaluate("() => typeof window.__renderAt === 'function'")
                      or page.evaluate("() => document.getAnimations().length") > 0):
                page.evaluate(SCRUB, max(0.0, float(d) - 1.0 / args.fps))
                print(f"(measuring the settled state at t={float(d) - 1.0 / args.fps:.2f}s)")

            rep = page.evaluate(FIT_CHECK, {
                "w": args.width, "h": args.height, "safe": safe,
                "typeFloor": type_floor, "strokeFloor": stroke_floor,
            })
            still = out / "fit-check.png"
            page.screenshot(path=str(still), omit_background=args.alpha)
            browser.close()
            ok = report_fit(rep, args.width, args.height, safe, type_floor, stroke_floor, still)
            sys.exit(0 if ok else 1)

        duration = args.duration
        if duration is None:
            duration = page.evaluate("() => window.__duration || null")
            if duration is None:
                sys.exit("no --duration given and window.__duration is not set")
        duration = float(duration)

        has_renderat = page.evaluate("() => typeof window.__renderAt === 'function'")
        n_anims = page.evaluate("() => document.getAnimations().length")
        if not has_renderat and n_anims == 0:
            sys.exit("no render contract: define window.__renderAt(t) or use CSS animations")

        segments = page.evaluate("() => window.__segments || null")
        compact = bool(page.evaluate("() => window.__compact || false"))
        mode = ([f"WAAPI ({n_anims})"] if n_anims else []) + (["__renderAt"] if has_renderat else [])
        px = int(args.width * args.scale), int(args.height * args.scale)
        print(f"contract: {' + '.join(mode)}")
        print(f"canvas:   {args.width}x{args.height} CSS px @{args.scale:g}x "
              f"-> output {px[0]}x{px[1]}{' + alpha' if args.alpha else ''}")

        capture = page.locator(args.selector) if args.selector else page

        # ---- verify determinism -------------------------------------------------
        if args.verify:
            a, b = out / "_va.png", out / "_vb.png"
            for path in (a, b):
                page.evaluate(SCRUB, args.start)
                shoot(page, capture, path, args.alpha)
            same = sha(a) == sha(b)
            a.unlink(); b.unlink()
            browser.close()
            print("PASS - frame is deterministic" if same else
                  "FAIL - two renders of the same frame differ.\n"
                  "  Look for Date.now/performance.now reads, unseeded randomness,\n"
                  "  timers driving visual state, or accumulated state in __renderAt.")
            sys.exit(0 if same else 1)

        # ---- verify holds are static -------------------------------------------
        if args.check_holds:
            if not segments:
                browser.close()
                sys.exit("--check-holds needs window.__segments (use the Timeline helper)")
            bad = []
            tmp = out / "_hold.png"
            tmp2 = out / "_hold2.png"
            for s in segments:
                lo, hi = s["endFrame"], s["holdEndFrame"] - 1
                if hi <= lo:
                    continue
                page.evaluate(SCRUB, lo / args.fps)
                shoot(page, capture, tmp, args.alpha)
                page.evaluate(SCRUB, hi / args.fps)
                shoot(page, capture, tmp2, args.alpha)
                if sha(tmp) != sha(tmp2):
                    bad.append(f"{s['name']} (frames {lo}-{hi})")
            for t_ in (tmp, tmp2):
                if t_.exists():
                    t_.unlink()
            browser.close()
            if bad:
                print("FAIL - these hold regions are not static:")
                for b_ in bad:
                    print(f"  {b_}")
                print("\nTime remapping cannot freeze cleanly on a moving hold. Check for\n"
                      "looping/idle animation, or easing that hasn't settled before the hold.")
                sys.exit(1)
            print(f"PASS - all {len(segments)} hold regions are static")
            sys.exit(0)

        # ---- layer mode ---------------------------------------------------------
        if args.layers:
            layers = page.evaluate("() => window.__layers || null")
            if not layers:
                browser.close()
                sys.exit("--layers needs window.__layers = ['#sel', ...]")
            seg_by_name = {s["name"]: s for s in (segments or [])}
            print(f"layers:   {len(layers)}")
            t0 = time.time()
            for spec in layers:
                sel = spec if isinstance(spec, str) else spec["selector"]
                name = (spec.get("segment") if isinstance(spec, dict) else None) or \
                       sel.lstrip("#.").replace(" ", "-")
                seg = seg_by_name.get(name)
                lo = seg["startFrame"] if seg else 0
                hi = seg["holdEndFrame"] if seg else int(round(duration * args.fps))
                d = out / name
                d.mkdir(parents=True, exist_ok=True)
                loc = page.locator(sel)
                for i, fr in enumerate(range(lo, hi)):
                    page.evaluate(SCRUB, fr / args.fps)
                    shoot(page, loc, d / f"f-{i:06d}.png", args.alpha)
                print(f"  {name}: {hi - lo} frames -> {d}/")
            if segments:
                write_manifest(segments, args.fps, out, compact)
            browser.close()
            print(f"done in {(time.time() - t0) / 60:.1f} min")
            print("encode each with: encode.py --frames <dir>/ --profile edit-alpha --out <name>.mov")
            return

        # ---- full sequence ------------------------------------------------------
        total = int(round(duration * args.fps))
        est_gb = total * (px[0] * px[1]) * 4e-9 * 0.35  # rough PNG estimate
        print(f"rendering {total} frames @ {args.fps}fps ({duration:.2f}s), ~{est_gb:.1f} GB")

        t0 = time.time()
        for i in range(total):
            page.evaluate(SCRUB, args.start + i / args.fps)
            shoot(page, capture, out / f"f-{i:06d}.png", args.alpha)
            if i and i % 25 == 0:
                per = (time.time() - t0) / i
                print(f"  {i}/{total}  ({per:.2f}s/frame, ~{per * (total - i) / 60:.1f} min left)")

        if segments:
            write_manifest(segments, args.fps, out, compact)
        browser.close()

    print(f"done: {total} frames in {(time.time() - t0) / 60:.1f} min -> {out}/")
    print(f"next: python encode.py --frames {out}/ --fps {args.fps} --profile edit --out out.mov")


if __name__ == "__main__":
    main()
