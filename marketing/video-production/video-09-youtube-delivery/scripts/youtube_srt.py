#!/usr/bin/env python3
"""youtube_srt.py — deterministic SRT operations for video-09-youtube-delivery.

Subcommands:
  strip-tags IN.srt OUT.srt
      Remove inline markup tags (<b>, <font ...>, </...>). Drops cues left empty.
  sentences  IN.srt OUT.srt
      Merge cues into sentence-level cues. REQUIRES punctuated input — a sentence
      ends at . ! ? followed by whitespace/end-of-cue. Timing: sentence spans from
      the start of its first contributing slice to the end of its last; boundaries
      inside a cue are placed character-proportionally.
  wrap       IN.srt OUT.srt [--max-line 42] [--max-lines 2]
      Re-wrap each cue to <= max-lines lines of <= max-line chars (words never
      broken). Overflow becomes extra cues, time split character-proportionally.
  check      FILE.srt [--words-from SRC.srt] [--max-line N] [--min-dur 0.1]
      Structural validation. --words-from verifies word content is identical to
      SRC ignoring punctuation and case (the EN-fidelity guarantee).

All outputs renumbered from 1, UTF-8, blank-line separated. Exit 0 = pass.
"""
import re
import sys
import argparse

TIME_RE = re.compile(
    r"(\d+):(\d{2}):(\d{2})[,.](\d{1,3})\s*-->\s*(\d+):(\d{2}):(\d{2})[,.](\d{1,3})")
TAG_RE = re.compile(r"<[^>]+>")
# sentence-final . ! ? (plus closing quotes/brackets) followed by whitespace or end
BOUNDARY_RE = re.compile(r"[.!?][\"'’”)\]]*(?=\s|$)")


def die(msg):
    sys.stderr.write("ERROR: %s\n" % msg)
    sys.exit(1)


def parse_time_line(line):
    m = TIME_RE.search(line)
    if not m:
        return None
    g = [int(x) for x in m.groups()]
    start = g[0] * 3600000 + g[1] * 60000 + g[2] * 1000 + g[3]
    end = g[4] * 3600000 + g[5] * 60000 + g[6] * 1000 + g[7]
    return start, end


def fmt_time(ms):
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def parse_srt(path):
    """Return list of dicts: {start, end, lines}. Tolerates BOM, CRLF, missing indices."""
    text = open(path, encoding="utf-8-sig").read().replace("\r\n", "\n").replace("\r", "\n")
    cues = []
    for block in re.split(r"\n\s*\n", text):
        lines = [ln for ln in block.split("\n")]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        if not lines:
            continue
        # optional index line
        if re.fullmatch(r"\d+", lines[0].strip()) and len(lines) > 1 and TIME_RE.search(lines[1]):
            lines.pop(0)
        if not lines:
            continue
        t = parse_time_line(lines[0])
        if t is None:
            die("unparseable cue block starting: %r" % lines[0][:60])
        cues.append({"start": t[0], "end": t[1], "lines": lines[1:]})
    return cues


def write_srt(path, cues):
    out = []
    for i, c in enumerate(cues, 1):
        out.append(str(i))
        out.append("%s --> %s" % (fmt_time(c["start"]), fmt_time(c["end"])))
        out.extend(c["lines"])
        out.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def cue_text(c):
    return " ".join(" ".join(c["lines"]).split())


def cmd_strip_tags(args):
    cues = parse_srt(args.infile)
    out = []
    for c in cues:
        lines = [" ".join(TAG_RE.sub("", ln).split()) for ln in c["lines"]]
        lines = [ln for ln in lines if ln]
        if lines:
            out.append({"start": c["start"], "end": c["end"], "lines": lines})
    write_srt(args.outfile, out)
    print("strip-tags: %d cues in, %d cues out -> %s" % (len(cues), len(out), args.outfile))


def cue_slices(c):
    """Split one cue's text at sentence boundaries. Yield (text, start, end, terminal)."""
    text = cue_text(c)
    if not text:
        return
    bounds = [m.end() for m in BOUNDARY_RE.finditer(text)]
    if not bounds or bounds[-1] != len(text):
        bounds.append(len(text))
    span = c["end"] - c["start"]
    prev = 0
    for b in bounds:
        piece = text[prev:b].strip()
        if piece:
            s = c["start"] + int(round(span * prev / len(text)))
            e = c["start"] + int(round(span * b / len(text)))
            yield piece, s, e, bool(BOUNDARY_RE.search(piece[-3:] if len(piece) >= 3 else piece))
        prev = b


def cmd_sentences(args):
    cues = parse_srt(args.infile)
    out, buf, buf_start, buf_end = [], [], None, None
    for c in cues:
        for piece, s, e, terminal in cue_slices(c):
            if buf_start is None:
                buf_start = s
            buf.append(piece)
            buf_end = e
            if terminal:
                out.append({"start": buf_start, "end": buf_end, "lines": [" ".join(buf)]})
                buf, buf_start, buf_end = [], None, None
    if buf:
        sys.stderr.write("WARNING: trailing unterminated sentence kept: %r\n" % " ".join(buf)[:80])
        out.append({"start": buf_start, "end": buf_end, "lines": [" ".join(buf)]})
    write_srt(args.outfile, out)
    print("sentences: %d cues in, %d sentence cues out -> %s" % (len(cues), len(out), args.outfile))


def wrap_lines(text, width):
    lines, cur = [], ""
    for w in text.split():
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= width:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def wrap_balanced(text, width):
    """Same line count as greedy, but the narrowest width that still fits it —
    avoids tiny trailing pieces like a lone 'Right?' becoming its own cue."""
    n = len(wrap_lines(text, width))
    lo, hi = max(len(w) for w in text.split()), width
    best = wrap_lines(text, width)
    while lo <= hi:
        mid = (lo + hi) // 2
        cand = wrap_lines(text, mid)
        if len(cand) <= n:
            best, hi = cand, mid - 1
        else:
            lo = mid + 1
    return best


def cmd_wrap(args):
    cues = parse_srt(args.infile)
    out = []
    for c in cues:
        lines = (wrap_balanced if args.balance else wrap_lines)(cue_text(c), args.max_line)
        chunks = [lines[i:i + args.max_lines] for i in range(0, len(lines), args.max_lines)]
        total = sum(len(" ".join(ch)) for ch in chunks) or 1
        span, t = c["end"] - c["start"], c["start"]
        for i, ch in enumerate(chunks):
            e = c["end"] if i == len(chunks) - 1 else t + int(round(span * len(" ".join(ch)) / total))
            out.append({"start": t, "end": e, "lines": ch})
            t = e
    write_srt(args.outfile, out)
    print("wrap: %d cues in, %d cues out (max %dx%d) -> %s"
          % (len(cues), len(out), args.max_lines, args.max_line, args.outfile))


def cmd_fix_short(args):
    """Give every cue at least --min-dur on screen, so YouTube cannot skip it.
    Cheapest remedy first: (1) extend into a following gap, (2) merge text with a
    neighbour when the result still fits --max-line, (3) borrow start-time from the
    next cue while it keeps its own minimum. Never changes word order or content."""
    cues = parse_srt(args.infile)
    need = int(args.min_dur * 1000)
    stats = {"gap": 0, "merge": 0, "borrow": 0, "left": 0}
    i = 0
    while i < len(cues):
        c = cues[i]
        if c["end"] - c["start"] >= need:
            i += 1
            continue
        nxt = cues[i + 1] if i + 1 < len(cues) else None
        prev = cues[i - 1] if i > 0 else None
        if nxt is None or nxt["start"] - c["start"] >= need:      # (1) free gap
            c["end"] = c["start"] + need if nxt else max(c["end"], c["start"] + need)
            stats["gap"] += 1
            i += 1
            continue
        merged = None
        if nxt and len(cue_text(c)) + 1 + len(cue_text(nxt)) <= args.max_line:
            merged = ("next", nxt)
        elif prev and len(cue_text(prev)) + 1 + len(cue_text(c)) <= args.max_line:
            merged = ("prev", prev)
        if merged:                                                # (2) text merge
            if merged[0] == "next":
                nxt["lines"] = [cue_text(c) + " " + cue_text(nxt)]
                nxt["start"] = c["start"]
            else:
                prev["lines"] = [cue_text(prev) + " " + cue_text(c)]
                prev["end"] = c["end"]
            cues.pop(i)
            stats["merge"] += 1
            continue
        if nxt:                                                   # (3) borrow time
            spare = (nxt["end"] - nxt["start"]) - need
            take = min(need - (c["end"] - c["start"]), max(0, spare))
            if take > 0:
                c["end"] += take
                nxt["start"] += take
                stats["borrow"] += 1
                i += 1
                continue
        stats["left"] += 1
        i += 1
    write_srt(args.outfile, cues)
    print("fix-short: %d cues out — extended %d, merged %d, borrowed %d, unfixable %d (min %.2fs)"
          % (len(cues), stats["gap"], stats["merge"], stats["borrow"], stats["left"], args.min_dur))


def norm_words(cues):
    text = " ".join(cue_text(c) for c in cues).lower()
    text = TAG_RE.sub(" ", text).replace("’", "'")
    text = re.sub(r"[.,!?;:\"“”…()\[\]]", " ", text)
    return text.split()


def cmd_check(args):
    cues = parse_srt(args.file)
    problems, warnings = [], []
    if not cues:
        problems.append("no cues parsed")
    for i, c in enumerate(cues, 1):
        if c["start"] >= c["end"]:
            problems.append("cue %d: start >= end" % i)
        if i > 1 and c["start"] < cues[i - 2]["end"]:
            problems.append("cue %d: overlaps previous (starts %s, prev ends %s)"
                            % (i, fmt_time(c["start"]), fmt_time(cues[i - 2]["end"])))
        txt = cue_text(c)
        if not txt:
            problems.append("cue %d: empty" % i)
        if "<" in txt:
            problems.append("cue %d: markup tag survives: %r" % (i, txt[:50]))
        if (c["end"] - c["start"]) / 1000.0 < args.min_dur:
            warnings.append("cue %d: duration %.3fs < %.2fs" % (i, (c["end"] - c["start"]) / 1000.0, args.min_dur))
        if args.max_line:
            for ln in c["lines"]:
                if len(ln) > args.max_line:
                    problems.append("cue %d: line %d chars > %d: %r" % (i, len(ln), args.max_line, ln))
    if args.words_from:
        a, b = norm_words(cues), norm_words(parse_srt(args.words_from))
        if a != b:
            k = next((j for j in range(min(len(a), len(b))) if a[j] != b[j]), min(len(a), len(b)))
            problems.append("word mismatch vs %s at word %d: %r vs %r (context: ...%s / ...%s)"
                            % (args.words_from, k, a[k:k + 1], b[k:k + 1],
                               " ".join(a[max(0, k - 4):k + 3]), " ".join(b[max(0, k - 4):k + 3])))
        else:
            print("words-match: OK (%d words identical to %s)" % (len(a), args.words_from))
    for w in warnings[:20]:
        print("warn: " + w)
    if len(warnings) > 20:
        print("warn: ... %d more duration warnings" % (len(warnings) - 20))
    if problems:
        for p in problems[:40]:
            print("FAIL: " + p)
        sys.exit(1)
    print("check: %d cues OK (%s -> %s)" % (len(cues), fmt_time(cues[0]["start"]), fmt_time(cues[-1]["end"])))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("strip-tags"); s.add_argument("infile"); s.add_argument("outfile"); s.set_defaults(fn=cmd_strip_tags)
    s = sub.add_parser("sentences"); s.add_argument("infile"); s.add_argument("outfile"); s.set_defaults(fn=cmd_sentences)
    s = sub.add_parser("wrap"); s.add_argument("infile"); s.add_argument("outfile")
    s.add_argument("--max-line", type=int, default=42); s.add_argument("--max-lines", type=int, default=2)
    s.add_argument("--balance", action="store_true")
    s.set_defaults(fn=cmd_wrap)
    s = sub.add_parser("fix-short"); s.add_argument("infile"); s.add_argument("outfile")
    s.add_argument("--min-dur", type=float, default=0.8); s.add_argument("--max-line", type=int, default=32)
    s.set_defaults(fn=cmd_fix_short)
    s = sub.add_parser("check"); s.add_argument("file"); s.add_argument("--words-from")
    s.add_argument("--max-line", type=int, default=0); s.add_argument("--min-dur", type=float, default=0.1)
    s.set_defaults(fn=cmd_check)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
