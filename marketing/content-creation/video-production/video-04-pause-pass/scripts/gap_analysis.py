#!/usr/bin/env python3
"""Pause analysis for a Premiere word-level transcript JSON.

    python3 gap_analysis.py TRANSCRIPT.json [--threshold 1.0] [--eos-residual 0.7]
                            [--mid-residual 0.4] [--fps 25] [--list-all]

Finds inter-word silence gaps >= threshold and emits frame-snapped trim rows
(descending, CUT ORDER-ready). The residual is split around the gap middle so
word decay and breath attack both survive. Prints seam words for human veto.
"""

import argparse
import json


def tc(seconds, fps):
    fr = round(seconds * fps)
    s, ff = divmod(fr, fps)
    m, ss = divmod(s, 60)
    h, mm = divmod(m, 60)
    return f"{h:02d}:{mm:02d}:{ss:02d}:{ff:02d}"


def snap(seconds, fps):
    return round(seconds * fps) / fps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("--threshold", type=float, default=1.0)
    ap.add_argument("--eos-residual", type=float, default=0.7)
    ap.add_argument("--mid-residual", type=float, default=0.4)
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--list-all", action="store_true", help="also list gaps below threshold")
    args = ap.parse_args()

    d = json.load(open(args.json_path))
    words = sorted(
        (w for s in d["segments"] for w in s["words"] if w.get("text")),
        key=lambda w: w["start"],
    )

    trims = []
    for a, b in zip(words, words[1:]):
        gap_start = a["start"] + a["duration"]
        gap_len = b["start"] - gap_start
        if gap_len < (0.3 if args.list_all else args.threshold):
            continue
        eos = bool(a.get("eos"))
        residual = args.eos_residual if eos else args.mid_residual
        if gap_len < args.threshold:
            trims.append({"skip": True, "at": gap_start, "len": gap_len, "a": a["text"], "b": b["text"], "eos": eos})
            continue
        f = snap(gap_start + residual / 2, args.fps)
        t = snap(b["start"] - residual / 2, args.fps)
        if t - f < 1 / args.fps:
            continue
        trims.append({"skip": False, "at": gap_start, "len": gap_len, "from": f, "to": t,
                      "cut": t - f, "a": a["text"], "b": b["text"], "eos": eos})

    active = [x for x in trims if not x["skip"]]
    total = sum(x["cut"] for x in active)
    print(f"gaps >= {args.threshold}s: {len(active)} | reclaimable: {total:.2f}s")
    print(f"policy: residual {args.eos_residual}s sentence-end / {args.mid_residual}s mid-sentence, fps {args.fps}\n")
    print("| # | delete from (TC) | delete to (TC) | from_s | to_s | length_s | seam |")
    print("|---|---|---|---|---|---|---|")
    for i, x in enumerate(sorted(active, key=lambda x: -x["from"]), 1):
        kind = "sentence-end" if x["eos"] else "MID-SENTENCE"
        print(f"| {i} | {tc(x['from'], args.fps)} | {tc(x['to'], args.fps)} | {x['from']:.2f} | {x['to']:.2f} | "
              f"{x['cut']:.2f} | `{x['a']}` → `{x['b']}` ({kind}, gap {x['len']:.2f}s) |")
    if args.list_all:
        print("\nBelow threshold (untouched):")
        for x in trims:
            if x["skip"]:
                print(f"  {x['len']:.2f}s at {tc(x['at'], args.fps)}  `{x['a']}` → `{x['b']}`")


if __name__ == "__main__":
    main()
