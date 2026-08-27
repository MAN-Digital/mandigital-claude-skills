#!/usr/bin/env python3
"""
cues.py — cue resolution and dual-timecode emission for graphics placement.

Bundled resource for the graphics-placement skill. Everything here is Tier 1
(text-verifiable). Emits BOTH the master cue and the motion-graphics rebase.

Usage:
    python3 cues.py resolve  TRANSCRIPT.csv CUES.txt [--lead FRAMES]
    python3 cues.py unique   TRANSCRIPT.csv CUES.txt
    python3 cues.py window   TRANSCRIPT.csv --in TC --out TC
    python3 cues.py texture  PLACEMENTS.txt

CUES.txt format, one per line:   asset | step | probe phrase
The first line of each asset block defines that asset's IN point (MG base).

PLACEMENTS.txt format, one per line:   asset | archetype | format | tc
One line per cue event, in order; an asset's first tc is its IN, last is its OUT.
format is one of: full / 23 / 13 / overlay.
"""
import argparse, csv, re, sys
csv.field_size_limit(sys.maxsize)


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        head = fh.read(8192); fh.seek(0)
        d = ";" if head.count(";") > head.count(",") else ","
        rows = list(csv.DictReader(fh, delimiter=d))
    k = {c.lower().strip(): c for c in rows[0]}
    return [{"start": r[k["start time"]], "end": r[k["end time"]],
             "text": (r[k["text"]] or "").strip()} for r in rows]


def detect_fps(rows):
    mx = 0
    for r in rows:
        for t in (r["start"], r["end"]):
            try: mx = max(mx, int(t.split(":")[3]))
            except (IndexError, ValueError): pass
    for f in (24, 25, 30, 50, 60):
        if mx < f: return f
    return 25


def to_frames(t, fps):
    h, m, s, f = (int(x) for x in t.split(":"))
    return ((h * 3600 + m * 60 + s) * fps) + f


def to_tc(fr, fps):
    fr = max(0, fr)
    h, fr = divmod(fr, 3600 * fps); m, fr = divmod(fr, 60 * fps); s, fr = divmod(fr, fps)
    return f"{h:02d}:{m:02d}:{s:02d}:{fr:02d}"


def to_mg(fr, fps):
    """Rebased cue for the motion designer: M:SS:FF from the asset's own IN."""
    sign = "-" if fr < 0 else ""; fr = abs(fr)
    s, f = divmod(fr, fps); m, s = divmod(s, 60)
    return f"{sign}{m}:{s:02d}:{f:02d}"


def occurrences(rows, probe):
    """Every row where `probe` completes. Unanchored (Rule 5.1) and finds ALL
    occurrences, not just the first — a cumulative accumulator silently reports
    only the earliest, which mis-resolves any phrase the speaker repeats."""
    p = re.sub(r"\s+", " ", probe).lower()
    norm = ""; ends = []
    for r in rows:
        norm += re.sub(r"\s+", " ", " " + r["text"])
        ends.append((len(norm), r["start"]))
    low = norm.lower(); out = []
    for m in re.finditer(re.escape(p), low):
        pos = m.end()
        out.append(next(st for end, st in ends if pos <= end))
    return out


def resolve_in_order(rows, cues):
    """Pick the occurrence that keeps each asset's steps in sequence (Rule 4.1),
    while still reporting total occurrence count for the ambiguity warning."""
    out = []; last = {}
    for asset, step, probe in cues:
        hits = occurrences(rows, probe)
        prev = last.get(asset)
        pick = next((h for h in hits if prev is None or h > prev), hits[0] if hits else None)
        if pick: last[asset] = pick
        out.append((asset, step, probe, pick, len(hits)))
    return out


def read_cues(path):
    cues = []
    for ln in open(path, encoding="utf-8"):
        ln = ln.strip()
        if not ln or ln.startswith("#"): continue
        parts = [x.strip() for x in ln.split("|")]
        if len(parts) < 3: sys.exit(f"malformed cue line: {ln}")
        cues.append(tuple(parts[:3]))
    return cues


def cmd_resolve(a):
    rows = load(a.transcript); fps = detect_fps(rows)
    cues = read_cues(a.cues)
    print(f"transcript: {a.transcript}  |  fps {fps} (detected)  |  lead {a.lead} frames\n")
    print(f"{'ASSET':10} {'STEP':22} {'MASTER CUE':>13} {'MG CUE':>9} {'HOLD':>7}  LOCATE STRING")
    print("-" * 118)
    resolved = resolve_in_order(rows, cues); base = {}
    for asset, step, probe, tc, n in resolved:
        if tc and asset not in base: base[asset] = tc
    for i, (asset, step, probe, tc, n) in enumerate(resolved):
        if tc is None:
            print(f"{asset:10} {step:22} {'** MISS **':>13}                    {probe[:40]}"); continue
        nxt = next((r[3] for r in resolved[i+1:] if r[3] and r[0] == asset), None)
        hold = f"{(to_frames(nxt,fps)-to_frames(tc,fps))/fps:.1f}s" if nxt else ""
        cue_f = to_frames(tc, fps) - a.lead
        mg = to_mg(to_frames(tc, fps) - to_frames(base[asset], fps), fps)
        warn = "" if n == 1 else f"  <{n}x AMBIGUOUS>"
        print(f"{asset:10} {step:22} {to_tc(cue_f,fps):>13} {mg:>9} {hold:>7}  {probe[:44]}{warn}")
    print("\nMASTER CUE = place in the sequence.  MG CUE = build the animation to (Rule 7.1).")


def cmd_unique(a):
    """Rule 5.2. A probe with >1 occurrence is not a reliable anchor."""
    rows = load(a.transcript)
    amb = 0
    for asset, step, probe in read_cues(a.cues):
        hits = occurrences(rows, probe)
        if len(hits) != 1: amb += 1
        print(f"  {asset:10} {step:22} {len(hits)}x  {hits if len(hits)!=1 else hits[0]}")
    print(f"\nambiguous probes: {amb}  (0 means ordering claims are safe)")


def cmd_window(a):
    """Rule 4.1. Print exactly what is spoken inside an asset's window."""
    rows = load(a.transcript); fps = detect_fps(rows)
    inw = [r for r in rows if a.tc_in <= r["start"] <= a.tc_out]
    dur = (to_frames(a.tc_out, fps) - to_frames(a.tc_in, fps)) / fps
    print(f"window {a.tc_in} -> {a.tc_out}  ({dur:.0f}s, {len(inw)} rows)\n")
    for r in inw: print(f"  {r['start']} | {r['text']}")


def read_placements(path):
    """PLACEMENTS.txt: asset | archetype | format | tc — grouped by asset, order kept."""
    assets = {}
    for ln in open(path, encoding="utf-8"):
        ln = ln.strip()
        if not ln or ln.startswith("#"): continue
        parts = [x.strip() for x in ln.split("|")]
        if len(parts) < 4: sys.exit(f"malformed placement line: {ln}")
        name, arch, fmt, tc = parts[:4]
        assets.setdefault(name, {"arch": arch, "fmt": fmt, "tcs": []})["tcs"].append(tc)
    return assets


def cmd_texture(a):
    """The texture pass — four signals over the merged plan. All flags are [C]:
    working thresholds from one engagement, expected to be falsified or firmed."""
    assets = read_placements(a.placements)
    fps = detect_fps([{"start": t, "end": t} for d in assets.values() for t in d["tcs"]])
    sec = lambda t: to_frames(t, fps) / fps
    fm = lambda s: f"{int(s // 60)}:{s % 60:04.1f}"
    size = lambda d: "S" if d < 45 else ("M" if d <= 180 else "L")
    merged = sorted(((min(map(sec, d["tcs"])), max(map(sec, d["tcs"])), n, d)
                     for n, d in assets.items()))

    print(f"placements: {a.placements}  |  fps {fps} (detected)  |  flags are [C] working thresholds\n")
    print(f"{'ASSET':26} {'ARCHETYPE':16} {'FMT':>7} {'IN':>8} {'DUR':>7} {'GAP':>7}  SZ")
    print("-" * 84)
    prev_out = 0.0
    for tin, tout, name, d in merged:
        gap = tin - prev_out; prev_out = max(prev_out, tout)
        print(f"{name:26} {d['arch']:16} {d['fmt']:>7} {fm(tin):>8} {fm(tout-tin):>7} {fm(max(gap,0)):>7}  {size(tout-tin)}")

    print("\nSTATIC INTERVALS — worst stretch inside each asset with no cue firing (flag > 40s):")
    for tin, tout, name, d in merged:
        ts = sorted(map(sec, d["tcs"]))
        gaps = [b - x for x, b in zip(ts, ts[1:])]
        if not gaps: continue
        worst = max(gaps)
        note = "  <-- FLAG" + (" (full frame: nothing moves)" if d["fmt"] == "full" else "") if worst > 40 else ""
        print(f"  {name:26} cues {len(ts):2}  mean {fm(sum(gaps)/len(gaps)):>6}  worst {fm(worst):>6}{note}")

    print("\nARCHETYPE RUNS (flag 3+ consecutive same treatment):")
    i, seq = 0, [(n, d["arch"]) for _, _, n, d in merged]
    while i < len(seq):
        j = i
        while j + 1 < len(seq) and seq[j + 1][1] == seq[i][1]: j += 1
        if j - i + 1 >= 3:
            print(f"  <-- FLAG  {j-i+1}x '{seq[i][1]}': {', '.join(n for n, _ in seq[i:j+1])}")
        i = j + 1

    print("\nSIZE RUNS (flag 2+ consecutive over 3min):")
    i, longs = 0, [(n, tout - tin) for tin, tout, n, _ in merged]
    while i < len(longs):
        j = i
        while j + 1 < len(longs) and size(longs[j + 1][1]) == "L" == size(longs[i][1]): j += 1
        if j - i + 1 >= 2 and size(longs[i][1]) == "L":
            print(f"  <-- FLAG  {j-i+1}x L back to back: {', '.join(n for n, _ in longs[i:j+1])}")
        i = j + 1

    ov = [(tin, n) for tin, _, n, d in merged if d["fmt"] == "overlay"]
    print("\nOVERLAY SPREAD (flag: all inventory inside one band):")
    if len(ov) >= 2:
        span_lo, span_hi = ov[0][0], ov[-1][0]
        video_hi = max(t for _, t, _, _ in merged)
        print(f"  {len(ov)} overlays, band {fm(span_lo)} -> {fm(span_hi)}"
              f"  |  bare before: {fm(span_lo)}  bare after: {fm(video_hi - span_hi)}")
        if span_hi - span_lo < 0.5 * video_hi:
            print("  <-- FLAG  overlay texture concentrated; candidates for relocation (remedy 2)")
    else:
        print(f"  {len(ov)} overlay(s) — nothing to spread")
    print("\nRemedies cheapest-first: re-cue / relocate / speaker / reprise / [texture]-marked card.")
    print("Emitting this map is the deliverable; acting on it is Tier 2.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("resolve"); c.add_argument("transcript"); c.add_argument("cues")
    c.add_argument("--lead", type=int, default=0, help="frames of pre-roll on every cue")
    c.set_defaults(fn=cmd_resolve)
    c = sub.add_parser("unique"); c.add_argument("transcript"); c.add_argument("cues"); c.set_defaults(fn=cmd_unique)
    c = sub.add_parser("window"); c.add_argument("transcript")
    c.add_argument("--in", dest="tc_in", required=True); c.add_argument("--out", dest="tc_out", required=True)
    c.set_defaults(fn=cmd_window)
    c = sub.add_parser("texture"); c.add_argument("placements"); c.set_defaults(fn=cmd_texture)
    a = p.parse_args(); a.fn(a)


if __name__ == "__main__":
    main()
