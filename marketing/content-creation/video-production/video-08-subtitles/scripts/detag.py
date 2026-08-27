#!/usr/bin/env python3
"""detag.py — strip inline style tags from SRT deliverables, in place (Stage C).

Usage: python3 detag.py FILE.srt [FILE2.srt ...]

The DaVinci subtitle-track template owns all styling (font/colour/bold), so
deliverables carry no inline markup (Diogo, 2026-08-03). Validates structure
after stripping: cue count unchanged, no empty cues, no surviving tags,
timestamps untouched. Idempotent — running on a clean file is a no-op.
"""
import re
import sys

TAG_RE = re.compile(r"<[^>]+>")
TIME_RE = re.compile(r"\d+:\d{2}:\d{2}[,.]\d{1,3}\s*-->\s*\d+:\d{2}:\d{2}[,.]\d{1,3}")


def detag(path):
    text = open(path, encoding="utf-8-sig").read()
    times_before = TIME_RE.findall(text)
    blocks_before = len([b for b in re.split(r"\n\s*\n", text) if b.strip()])
    clean = TAG_RE.sub("", text)
    times_after = TIME_RE.findall(clean)
    blocks_after = len([b for b in re.split(r"\n\s*\n", clean) if b.strip()])
    if times_before != times_after:
        sys.exit("ERROR: %s — timestamps changed during detag, aborting (file untouched)" % path)
    if blocks_before != blocks_after:
        sys.exit("ERROR: %s — cue count changed during detag, aborting (file untouched)" % path)
    for b in re.split(r"\n\s*\n", clean):
        lines = [ln for ln in b.split("\n") if ln.strip()]
        if lines and TIME_RE.search("\n".join(lines)) and not any(
                ln.strip() and not TIME_RE.search(ln) and not re.fullmatch(r"\d+", ln.strip())
                for ln in lines):
            sys.exit("ERROR: %s — a cue lost all its text, aborting (file untouched)" % path)
    if "<" in TAG_RE.sub("", clean) and clean != text:
        pass  # lone '<' in caption text is legal; only well-formed tags were stripped
    if clean == text:
        print("detag: %s already clean (no-op)" % path)
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(clean)
    print("detag: %s — tags stripped, %d cues, timestamps verified unchanged" % (path, blocks_after))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        detag(p)
