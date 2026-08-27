#!/usr/bin/env python3
"""Convert a Premiere Pro word-level transcript JSON export into the row-level
CSV that diagnostics.py consumes ("Speaker Name","Start Time","End Time","Text").

    python3 json_to_rows.py TRANSCRIPT.json [--fps 25] [-o OUT.csv]

Row start = first word onset (segments may carry leading silence);
row end   = segment start + duration (matches Premiere's own CSV export).
"""

import argparse
import csv
import json
import sys


def tc(seconds, fps):
    frames = round(seconds * fps)
    s, ff = divmod(frames, fps)
    m, ss = divmod(s, 60)
    hh, mm = divmod(m, 60)
    return f"{hh:02d}:{mm:02d}:{ss:02d}:{ff:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("-o", "--out", default=None)
    args = ap.parse_args()

    with open(args.json_path) as fh:
        data = json.load(fh)

    speakers = {s["id"]: s.get("name") or "Unknown" for s in data.get("speakers", [])}

    out = open(args.out, "w", newline="") if args.out else sys.stdout
    w = csv.writer(out, quoting=csv.QUOTE_ALL)
    w.writerow(["Speaker Name", "Start Time", "End Time", "Text"])

    for seg in data["segments"]:
        words = [x for x in seg.get("words", []) if x.get("text")]
        if not words:
            continue
        start = words[0]["start"]
        end = seg["start"] + seg["duration"]
        text = " ".join(x["text"] for x in words)
        w.writerow([speakers.get(seg.get("speaker"), "Unknown"), tc(start, args.fps), tc(end, args.fps), text])

    if args.out:
        out.close()


if __name__ == "__main__":
    main()
