#!/usr/bin/env python3
"""Exact word-level span timing for shorts mining.

Consumes Premiere's Transcript panel word-level JSON export
({language, segments[], speakers[]}, each segment carrying words[] with
start/duration). Matching is case- and punctuation-insensitive over the
flattened, time-ordered word stream, so quoted transcript text locates
even when the ASR text carries punctuation or capitalization.

Subcommands:
  find  --json T.json --phrase "some spoken words" [--fps 25]
        All occurrences: start of first word, end (start+duration) of last.
  span  --json T.json --from "opening words" --to "closing words" [--fps 25]
        Span from the FIRST match of --from to the first --to match that
        ends after it. Also reports the silence gap outside each boundary
        (prev word end -> span start, span end -> next word start) because
        cuts belong in those gaps, not on word onsets.

All times are keyed to the export they came from — a recut voids them.
"""
import argparse
import json
import re
import sys


def norm(w):
    return re.sub(r"[^a-z0-9']+", "", w.lower())


def load_words(path):
    with open(path) as f:
        data = json.load(f)
    words = []
    for seg in data.get("segments", []):
        for w in seg.get("words", []):
            if w.get("type") != "word":
                continue
            words.append(
                {"text": w["text"], "norm": norm(w["text"]),
                 "start": w["start"], "end": w["start"] + w["duration"]}
            )
    words.sort(key=lambda w: w["start"])
    return words


def tc(seconds, fps):
    frames = int(round(seconds * fps))
    f = frames % fps
    s = (frames // fps) % 60
    m = (frames // fps) // 60 % 60
    h = (frames // fps) // 3600
    return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"


def find_phrase(words, phrase):
    target = [norm(t) for t in phrase.split() if norm(t)]
    if not target:
        sys.exit("empty phrase after normalization")
    hits = []
    n = len(target)
    for i in range(len(words) - n + 1):
        if all(words[i + j]["norm"] == target[j] for j in range(n)):
            hits.append((i, i + n - 1))
    return hits


def report_hit(words, i, j, fps, label=""):
    start, end = words[i]["start"], words[j]["end"]
    gap_before = start - words[i - 1]["end"] if i > 0 else start
    gap_after = (words[j + 1]["start"] - end) if j + 1 < len(words) else float("inf")
    print(f"{label}first_word={words[i]['text']!r} last_word={words[j]['text']!r}")
    print(f"{label}start={start:.3f}s ({tc(start, fps)})  end={end:.3f}s ({tc(end, fps)})  length={end - start:.3f}s")
    print(f"{label}gap_before={gap_before:.3f}s  gap_after={gap_after:.3f}s")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("find", "span"):
        p = sub.add_parser(name)
        p.add_argument("--json", required=True)
        p.add_argument("--fps", type=int, default=25)
        if name == "find":
            p.add_argument("--phrase", required=True)
        else:
            p.add_argument("--from", dest="frm", required=True)
            p.add_argument("--to", dest="to", required=True)
    args = ap.parse_args()
    words = load_words(args.json)

    if args.cmd == "find":
        hits = find_phrase(words, args.phrase)
        if not hits:
            sys.exit(f"NOT FOUND: {args.phrase!r}")
        print(f"{len(hits)} match(es)")
        for k, (i, j) in enumerate(hits):
            report_hit(words, i, j, args.fps, label=f"[{k}] ")
    else:
        a = find_phrase(words, args.frm)
        if not a:
            sys.exit(f"NOT FOUND (--from): {args.frm!r}")
        i = a[0][0]
        b = [h for h in find_phrase(words, args.to) if words[h[1]]["end"] > words[i]["start"]]
        if not b:
            sys.exit(f"NOT FOUND after --from (--to): {args.to!r}")
        j = b[0][1]
        start, end = words[i]["start"], words[j]["end"]
        gap_before = start - words[i - 1]["end"] if i > 0 else start
        gap_after = (words[j + 1]["start"] - end) if j + 1 < len(words) else float("inf")
        print(f"span_start={start:.3f}s ({tc(start, args.fps)})  span_end={end:.3f}s ({tc(end, args.fps)})")
        print(f"length={end - start:.3f}s")
        print(f"gap_before={gap_before:.3f}s  gap_after={gap_after:.3f}s")
        if len(a) > 1 or len(b) > 1:
            print(f"WARNING: --from matched {len(a)}x, --to matched {len(b)}x — verify the right occurrence")


if __name__ == "__main__":
    main()
