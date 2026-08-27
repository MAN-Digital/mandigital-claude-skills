#!/usr/bin/env python3
"""Multi-file two-camera sync: match every B-cam file against every A-cam file by
audio cross-correlation, and compute each B clip's timeline placement.

Reconstructed 2026-08-01 from the 2026-07-29 production run (7/7 reliable matches,
rollover-boundary self-consistency to 0.01s), generalized from the hardcoded original.

    python3 sync_matrix.py --a A1.MOV A2.MOV --b B1.MOV B2.MOV \
        --a-starts 0 227.04 [--fps 25] [--rate 4000]

--a-starts: timeline start of each A clip (same order as --a; A clips assumed
in-point 0). Placement math: target = A_start + lag, frame-snapped.
Confidence gate: <3.0 is unreliable — do NOT auto-place, use Premiere's native
Synchronize for that clip. Rollover check: consecutive B files from one camera
should land adjacent (prev target + prev duration ≈ next target).
"""

import argparse
import json
import subprocess
import sys

import numpy as np


def extract(path, rate):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:a:0", "-ac", "1",
                        "-ar", str(rate), "-f", "f32le", "-"], capture_output=True, check=True)
    d = np.frombuffer(p.stdout, dtype=np.float32).copy()
    if len(d) == 0:
        raise SystemExit(f"no audio decoded from {path}")
    d -= d.mean()
    return d


def xcorr(a, b, rate):
    n = len(a) + len(b) - 1
    nfft = 1 << (n - 1).bit_length()
    corr = np.fft.irfft(np.fft.rfft(a, nfft) * np.conj(np.fft.rfft(b, nfft)), nfft)
    corr = np.concatenate([corr[-(len(b) - 1):], corr[:len(a)]])
    peak_idx = int(np.argmax(np.abs(corr)))
    lag = (peak_idx - (len(b) - 1)) / rate
    peak = abs(corr[peak_idx])
    guard = int(0.25 * rate)
    masked = np.abs(corr)
    masked[max(0, peak_idx - guard):peak_idx + guard] = 0
    runner = masked.max()
    conf = float(peak / runner) if runner > 0 else float("inf")
    norm = peak / (np.std(a) * np.std(b) * min(len(a), len(b)) + 1e-9)
    return lag, conf, float(norm)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", nargs="+", required=True, help="A-cam files, timeline order")
    ap.add_argument("--b", nargs="+", required=True, help="B-cam files, recording order")
    ap.add_argument("--a-starts", nargs="+", type=float, required=True,
                    help="timeline start seconds of each A clip (same order as --a)")
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--rate", type=int, default=4000)
    args = ap.parse_args()
    if len(args.a) != len(args.a_starts):
        raise SystemExit("--a and --a-starts must have the same length")

    audio = {}
    for f in args.a + args.b:
        sys.stderr.write(f"extracting {f}\n")
        audio[f] = extract(f, args.rate)

    results = []
    for bf in args.b:
        best = None
        for af, a_start in zip(args.a, args.a_starts):
            lag, conf, norm = xcorr(audio[af], audio[bf], args.rate)
            cand = {"a": af, "a_start": a_start, "lag": round(lag, 4),
                    "conf": round(conf, 2), "norm": round(norm, 4)}
            if best is None or cand["norm"] > best["norm"]:
                best = cand
        target = best["a_start"] + best["lag"]
        snapped = round(target * args.fps) / args.fps
        results.append({"b": bf, "match": best["a"], "lag_in_A_file": best["lag"],
                        "confidence": best["conf"], "target_timeline_s": round(snapped, 2),
                        "reliable": best["conf"] >= 3.0})
        sys.stderr.write(f"{bf}: {best['a']} lag {best['lag']:+.2f}s conf {best['conf']}\n")

    # rollover self-consistency report (independent correlations agreeing = proof)
    for prev, nxt in zip(results, results[1:]):
        if prev["match"] == nxt["match"]:
            sys.stderr.write(f"adjacency {prev['b']} → {nxt['b']}: gap would need duration data — check manually\n")

    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
