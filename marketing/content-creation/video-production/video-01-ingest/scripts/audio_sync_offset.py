#!/usr/bin/env python3
"""Two-camera waveform sync: compute the timeline offset between two recordings
of the same event by audio cross-correlation.

    python3 audio_sync_offset.py A_CAM_FILE B_CAM_FILE [--fps 25] [--window 180] [--rate 8000]

Output (stdout): placement_offset_seconds — where to START the B clip relative to
the A clip's start on the timeline (positive = B begins later; negative = earlier),
frame-snapped value at --fps, and a confidence ratio (peak vs. runner-up; >=3 is
reliable, <2 means do NOT auto-place). Also reports drift when both files are long
enough to correlate a second, later window.
"""

import argparse
import json
import subprocess
import sys
import tempfile

import numpy as np


def extract(path, start, dur, rate):
    """Decode a mono window of the file's audio as float32 samples."""
    with tempfile.NamedTemporaryFile(suffix=".f32", delete=False) as tmp:
        out = tmp.name
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start), "-t", str(dur), "-i", path,
           "-map", "0:a:0", "-ac", "1", "-ar", str(rate), "-f", "f32le", "-y", out]
    subprocess.run(cmd, check=True)
    data = np.fromfile(out, dtype=np.float32)
    if len(data) == 0:
        raise SystemExit(f"no audio decoded from {path}")
    return data - data.mean()


def duration_of(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "json", path], capture_output=True, text=True, check=True)
    return float(json.loads(p.stdout)["format"]["duration"])


def xcorr_offset(a, b, rate):
    """Return (lag_seconds, confidence). lag>0: b's content begins lag s into a."""
    n = len(a) + len(b) - 1
    nfft = 1 << (n - 1).bit_length()
    fa = np.fft.rfft(a, nfft)
    fb = np.fft.rfft(b, nfft)
    corr = np.fft.irfft(fa * np.conj(fb), nfft)
    corr = np.concatenate([corr[-(len(b) - 1):], corr[:len(a)]])  # lags -(len(b)-1) .. len(a)-1
    peak_idx = int(np.argmax(np.abs(corr)))
    lag = (peak_idx - (len(b) - 1)) / rate
    peak = abs(corr[peak_idx])
    # runner-up outside +-250ms of the peak
    guard = int(0.25 * rate)
    masked = np.abs(corr).copy()
    masked[max(0, peak_idx - guard):peak_idx + guard] = 0
    runner = masked.max()
    confidence = float(peak / runner) if runner > 0 else float("inf")
    return lag, confidence


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file_a")
    ap.add_argument("file_b")
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--window", type=float, default=180.0)
    ap.add_argument("--rate", type=int, default=8000)
    args = ap.parse_args()

    dur_a, dur_b = duration_of(args.file_a), duration_of(args.file_b)
    w = min(args.window, dur_a, dur_b)
    a = extract(args.file_a, 0, w, args.rate)
    b = extract(args.file_b, 0, w, args.rate)
    lag, conf = xcorr_offset(a, b, args.rate)
    snapped = round(lag * args.fps) / args.fps

    result = {
        "placement_offset_seconds": round(lag, 4),
        "frame_snapped": round(snapped, 4),
        "frames_at_fps": round(lag * args.fps),
        "confidence": round(conf, 2),
        "reliable": conf >= 3.0,
        "meaning": ("start B clip %.2fs AFTER A's start" % snapped) if snapped >= 0
                   else ("start B clip %.2fs BEFORE A's start" % -snapped),
    }

    # drift check: correlate a second window late in the shared overlap
    overlap_end = min(dur_a, dur_b + max(lag, 0)) if lag >= 0 else min(dur_a - lag, dur_b)
    late_start = overlap_end - w - 30
    if late_start > w + 60:
        a2 = extract(args.file_a, late_start, w, args.rate)
        b2 = extract(args.file_b, max(0.0, late_start - lag), w, args.rate)
        lag2, conf2 = xcorr_offset(a2, b2, args.rate)
        residual = lag2 - (lag - (lag if late_start - lag >= 0 else 0))  # b window pre-shifted by lag
        if conf2 >= 3.0:
            drift_s = lag2 if abs(lag2) < 1 else None  # residual after pre-shift
            if drift_s is not None:
                span_min = (late_start) / 60
                result["drift_seconds_over_span"] = round(drift_s, 4)
                result["drift_span_minutes"] = round(span_min, 1)
                result["drift_frames_per_10min"] = round(drift_s * args.fps / (span_min / 10), 2) if span_min else None

    print(json.dumps(result, indent=1))
    if not result["reliable"]:
        print("WARNING: low confidence — do NOT auto-place; use Premiere's native "
              "Synchronize (select both clips > Synchronize > Audio) instead.", file=sys.stderr)


if __name__ == "__main__":
    main()
