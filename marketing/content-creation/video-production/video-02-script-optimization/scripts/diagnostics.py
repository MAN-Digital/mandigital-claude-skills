#!/usr/bin/env python3
"""
diagnostics.py — mechanical checks for post-recording script optimization.

Bundled resource for the script-optimization skill. Everything here is Tier 1
(text-verifiable, no audio required). Nothing here makes a judgment call.

Usage:
    python3 diagnostics.py classify   CURRENT.csv [--source SOURCE.csv]
    python3 diagnostics.py repeats    CURRENT.csv [--threshold 0.72] [--window 14]
    python3 diagnostics.py seams      CURRENT.csv --source SOURCE.csv
    python3 diagnostics.py diff       PREVIOUS.csv CURRENT.csv
    python3 diagnostics.py suspect    CURRENT.csv [--glossary glossary.json]
    python3 diagnostics.py verify     CURRENT.csv --strings strings.txt

Assumes Premiere Pro transcript export: Speaker Name, Start Time, End Time, Text
with HH:MM:SS:FF timecodes. Delimiter and frame rate are both auto-detected.
"""

import argparse
import csv
import json
import re
import sys
from difflib import SequenceMatcher

csv.field_size_limit(sys.maxsize)


# ---------------------------------------------------------------- loading

def load(path):
    """Parse a transcript CSV. Auto-detects delimiter. Never trust wc -l on
    these files: transcript fields contain newlines and inflate line counts."""
    with open(path, encoding="utf-8-sig", newline="") as fh:
        head = fh.read(8192)
        fh.seek(0)
        delim = ";" if head.count(";") > head.count(",") else ","
        rows = list(csv.DictReader(fh, delimiter=delim))
    if not rows:
        sys.exit(f"empty or unparseable: {path}")
    key = {k.lower().strip(): k for k in rows[0]}
    for need in ("start time", "end time", "text"):
        if need not in key:
            sys.exit(f"missing column {need!r} in {path}; found {list(rows[0])}")
    return [
        {"start": r[key["start time"]], "end": r[key["end time"]], "text": (r[key["text"]] or "").strip()}
        for r in rows
    ]


def detect_fps(rows):
    """Derive frame rate from the data rather than assuming. Never hardcode 25."""
    mx = 0
    for r in rows:
        for t in (r["start"], r["end"]):
            try:
                mx = max(mx, int(t.split(":")[3]))
            except (IndexError, ValueError):
                pass
    for fps in (24, 25, 30, 50, 60):
        if mx < fps:
            return fps
    return 25


def tc(t, fps):
    h, m, s, f = (int(x) for x in t.split(":"))
    return h * 3600 + m * 60 + s + f / fps


def fmt(sec):
    sec = int(round(sec))
    sign = "-" if sec < 0 else ""
    sec = abs(sec)
    return f"{sign}{sec // 60}:{sec % 60:02d}"


def words(text):
    return re.findall(r"[a-z0-9€£$']+", text.lower())


# ------------------------------------------------------- 1. classify export

def cmd_classify(args):
    """Rules 2.1-2.5. Which of the four export states is this?"""
    rows = load(args.current)
    fps = detect_fps(rows)
    dur = tc(rows[-1]["end"], fps)

    gaps = sum(
        1 for i in range(len(rows) - 1)
        if abs(tc(rows[i]["end"], fps) - tc(rows[i + 1]["start"], fps)) > 0.2
    )
    absorbed = [
        (tc(r["end"], fps) - tc(r["start"], fps), r)
        for r in rows
        if r["text"] and (tc(r["end"], fps) - tc(r["start"], fps)) > 3.0
        and (tc(r["end"], fps) - tc(r["start"], fps)) / max(1, len(r["text"].split())) > 1.5
    ]

    print(f"file        : {args.current}")
    print(f"rows        : {len(rows)}")
    print(f"fps         : {fps} (detected)")
    print(f"runtime     : {fmt(dur)}")
    print(f"gaps >0.2s  : {gaps}")

    state = "B rippled cut (or original source)"
    if args.source:
        src = load(args.source)
        sdur = tc(src[-1]["end"], detect_fps(src))
        delta = sdur - dur
        print(f"source      : {fmt(sdur)}  ({len(src)} rows)")
        print(f"removed     : {fmt(delta)}  ({100 * dur / sdur:.0f}% retained)")
        if delta < 2 and len(rows) < len(src) * 0.95:
            state = "A marked-up transcript (rows deleted, MEDIA NOT CUT)"
        elif len(rows) > len(src) * 0.95 and delta > 2:
            state = "C re-transcribed cut (row count high vs duration)"

    if absorbed:
        state = "A marked-up transcript (rows deleted, MEDIA NOT CUT)"
        print(f"\nABSORBED SPANS ({len(absorbed)}) — removed time folded into neighbours:")
        for d, r in sorted(absorbed, reverse=True)[:12]:
            print(f"  {d:6.1f}s | {len(r['text'].split()):3d}w | {r['start']} | {r['text'][:60]}")

    print(f"\nSTATE       : {state}")
    print("IMPLICATION :", {
        "A": "nothing cut yet; all source timecodes valid; cannot audition by playback",
        "B": "previously issued timecodes are VOID; re-conform any timing document",
        "C": "row indices from earlier passes are void; text may differ from earlier exports",
    }[state[0]])
    print("NOTE        : if word-level diff vs source shows improving substitutions,")
    print("              this is also state D (hand-corrected) -> re-verify all locate strings.")


# --------------------------------------------------- 2. repetition scanning

def cmd_repeats(args):
    """Rule 6.5. Sliding-window similarity across the whole file."""
    rows = load(args.current)
    idx = []
    for i, r in enumerate(rows):
        for w in words(r["text"]):
            idx.append((i, w))

    W, STEP = args.window, 4
    wins = [
        (idx[s][0], idx[s + W - 1][0], " ".join(w for _, w in idx[s:s + W]))
        for s in range(0, max(0, len(idx) - W), STEP)
    ]
    hits = []
    for a in range(len(wins)):
        for b in range(a + 1, min(a + 140, len(wins))):
            if wins[b][0] - wins[a][1] < 2:
                continue
            ratio = SequenceMatcher(None, wins[a][2], wins[b][2]).ratio()
            if ratio > args.threshold:
                hits.append((round(ratio, 2), wins[a][0], wins[a][1], wins[b][0], wins[b][1]))

    seen, out = set(), []
    for h in sorted(hits, key=lambda x: -x[0]):
        k = (h[1] // 5, h[3] // 5)
        if k in seen:
            continue
        seen.add(k)
        out.append(h)

    print(f"repetition candidates: {len(out)}  (threshold {args.threshold}, window {args.window})")
    if not out:
        print("CLEAN — zero surviving repetition. One of the lock conditions is met.")
    for ratio, a1, a2, b1, b2 in sorted(out, key=lambda x: x[1]):
        print(f"\n  {ratio} | {rows[a1]['start']}  <=>  {rows[b1]['start']}")
        print(f"     A: {' '.join(rows[i]['text'] for i in range(a1, a2 + 1))[:150]}")
        print(f"     B: {' '.join(rows[i]['text'] for i in range(b1, b2 + 1))[:150]}")


# ---------------------------------------------------- 3. seam extraction

def cmd_seams(args):
    """Part 5. Every removal vs source, with surviving text on both sides."""
    src, cur = load(args.source), load(args.current)
    fps = detect_fps(src)
    a = [" ".join(words(r["text"])) for r in src]
    b = [" ".join(words(r["text"])) for r in cur]
    n = 0
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag in ("delete", "replace") and i2 > i1:
            n += 1
            dur = tc(src[i2 - 1]["end"], fps) - tc(src[i1]["start"], fps)
            before = src[i1 - 1]["text"] if i1 else "(FILE START)"
            after = src[i2]["text"] if i2 < len(src) else "(FILE END)"
            print(f"\n--- SEAM {n} | src {src[i1]['start']} -> {src[i2 - 1]['end']} ({fmt(dur)}) rows [{i1}-{i2 - 1}]")
            print(f"    OUT-point : ...{before[-80:]}")
            print(f"    REMOVED   : {' '.join(src[k]['text'] for k in range(i1, i2))[:260]}")
            print(f"    IN-point  : {after[:80]}...")
            if tag == "replace":
                print(f"    REPLACED BY: {' '.join(cur[k]['text'] for k in range(j1, j2))[:140]}")
    print(f"\ntotal seams: {n}")
    print("NEXT: classify each CLEAN / TRIM / BREAK using Test A (boundary),")
    print("      Test B (referential dependency), Test C (structural load).")


# ------------------------------------------------------ 4. diff two exports

def cmd_diff(args):
    """Rule 6.3. Word-level change list between consecutive exports.
    The 'new since last export' bucket is the regression report."""
    prev, cur = load(args.previous), load(args.current)
    wp = [w for r in prev for w in words(r["text"])]
    wc = [w for r in cur for w in words(r["text"])]
    big, small = [], []
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, wp, wc, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        ctx = " ".join(wp[max(0, i1 - 7):i1])
        rec = (ctx, " ".join(wp[i1:i2]), " ".join(wc[j1:j2]))
        (big if (i2 - i1) >= 3 else small).append(rec)

    print(f"REMOVALS / REPLACEMENTS >=3 words  ({len(big)})")
    for ctx, out, new in big:
        print(f"  ...{ctx[-45:]:>45} || -[{out[:95]}]")
        if new:
            print(f"  {'':>48} +[{new[:80]}]")
    print(f"\nMICRO EDITS 1-2 words  ({len(small)})  <- corrections AND accidental clips")
    for ctx, out, new in small:
        print(f"  ...{ctx[-45:]:>45} || -[{out}] +[{new}]")
    print("\nCLASSIFY each: applied / applied-differently / not-applied / NEW.")
    print("Report the NEW bucket under 'what got worse'. Improving substitutions")
    print("in the micro list mean state D (hand-corrected) -> re-verify locate strings.")


# ------------------------------------------- 5. transcription suspicion scan

ORDINALS = r"(first|second|third|fourth|forth|fifth|sixth|seventh|eighth|ninth|tenth|next|last|final)"
TERMINAL_RISK = {"is", "the", "a", "an", "and", "or", "to", "for", "of", "in", "on", "by", "that", "was", "be"}


def cmd_suspect(args):
    """Rules 3.1-3.3. Flag likely TRANSCRIPTION failures, never content defects.
    Output is a listen-check batch for the human, who has the audio."""
    rows = load(args.current)
    glossary = {}
    if args.glossary:
        glossary = json.load(open(args.glossary))

    flags = []
    for i, r in enumerate(rows):
        t = r["text"]
        if not t:
            continue
        low = t.lower()

        # class 1: ordinal scaffolding. Only fires when the ordinal sits in
        # list-announcing position (first three words of a short row), which is
        # where ASR fuses it into the following noun ("Fourth thing" -> "for").
        if len(t.split()) <= 6 and re.match(rf"^\W*(the\s+)?{ORDINALS}\b", low):
            flags.append((r["start"], "ordinal/list-scaffolding", t))

        # class 2: brand, product and domain terms (glossary-driven)
        for correct, corruptions in glossary.items():
            for bad in corruptions:
                if bad.lower() in low:
                    flags.append((r["start"], f"domain term -> likely '{correct}'", t))

        # class 3: clause-terminal word dropped.
        # Premiere splits rows mid-sentence, so a row ending on a function word
        # is normally just a row break. It is only suspicious when the NEXT row
        # starts a new sentence, which means this one was left unfinished.
        w = words(t)
        nxt = rows[i + 1]["text"].strip() if i + 1 < len(rows) else ""
        starts_new = bool(nxt) and (nxt[0].isupper() or nxt[0].isdigit())
        if w and w[-1] in TERMINAL_RISK and not t.rstrip().endswith((".", "?", "!")) and starts_new:
            flags.append((r["start"], "clause-terminal word likely clipped", t))

        # class 4: numeral or unit with a missing bound
        if re.search(r"(between|from)\s*$|\band\s*[€£$]?[\d,]+\.?$|[\d,]+\s+(a|per)\s*$", low):
            flags.append((r["start"], "numeral/unit bound likely dropped", t))

    seen, out = set(), []
    for f in flags:
        if f[0] in seen:
            continue
        seen.add(f[0])
        out.append(f)

    print(f"LISTEN-CHECK BATCH ({len(out)}) — Tier 3, route to the human\n")
    print("These are TRANSCRIPTION hypotheses. Do NOT classify any of them as")
    print("content defects and do NOT write predicted readings into the cut.\n")
    for start, why, text in out:
        print(f"  {start} | {why}")
        print(f"             transcript reads: {text[:110]}")


# ------------------------------------------------ 6. verify locate strings

def cmd_verify(args):
    """Rule 10.2. Every quoted string must exist verbatim in the export it
    is keyed to. Catches ellipses and paraphrase creeping into search strings."""
    rows = load(args.current)
    blob = re.sub(r"\s+", " ", " ".join(r["text"] for r in rows if r["text"]))
    bad = []
    with open(args.strings, encoding="utf-8") as fh:
        targets = [ln.rstrip("\n") for ln in fh if ln.strip()]
    for s in targets:
        if re.sub(r"\s+", " ", s).strip() not in blob:
            bad.append(s)
    print(f"checked {len(targets)} locate strings against {args.current}")
    print(f"NOT VERBATIM: {len(bad)}")
    for s in bad:
        print(f"  X {s}")
    if bad:
        sys.exit(1)


# --------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("classify"); c.add_argument("current"); c.add_argument("--source"); c.set_defaults(fn=cmd_classify)
    c = sub.add_parser("repeats"); c.add_argument("current")
    c.add_argument("--threshold", type=float, default=0.72); c.add_argument("--window", type=int, default=14)
    c.set_defaults(fn=cmd_repeats)
    c = sub.add_parser("seams"); c.add_argument("current"); c.add_argument("--source", required=True); c.set_defaults(fn=cmd_seams)
    c = sub.add_parser("diff"); c.add_argument("previous"); c.add_argument("current"); c.set_defaults(fn=cmd_diff)
    c = sub.add_parser("suspect"); c.add_argument("current"); c.add_argument("--glossary"); c.set_defaults(fn=cmd_suspect)
    c = sub.add_parser("verify"); c.add_argument("current"); c.add_argument("--strings", required=True); c.set_defaults(fn=cmd_verify)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
