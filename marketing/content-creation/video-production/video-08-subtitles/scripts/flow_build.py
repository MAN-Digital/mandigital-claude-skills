#!/usr/bin/env python3
"""Build the FLOW delivery variant of a corrected SRT: sentence-clean cuts,
punctuation stripped, inter-caption gaps closed. Word content is guaranteed
identical to the input (verified before writing).

Usage:
    python3 flow_build.py CORRECTED.srt TRANSCRIPT.json OUT.srt
        [--min-piece 0.24] [--keep-gaps-over 0.5] [--max-line N] [--strip-questions]

Rules:
 1. Any block containing a sentence boundary (. ? !) mid-text is split there.
    Cut time comes from the Premiere JSON word timestamps when the word streams
    align; character-proportional fallback otherwise. Pieces >= --min-piece;
    blocks under 2x min-piece split at midpoint; blocks under 4/3 min-piece are
    left unsplit and reported.
 2. Prose commas and sentence-final dots are removed. Kept: question marks
    (unless --strip-questions), exclamation marks, thousands separators
    (2,750), apostrophes, hyphens, and dots inside URL-like tokens (a/b, x.y).
 3. Gaps: mid-sentence junction gaps are always closed (previous caption
    extends to the next one's start). Sentence-boundary gaps close only when
    shorter than --keep-gaps-over; longer ones are deliberate breathing pauses
    and stay caption-free (each kept pause is listed). The gap histogram is
    printed first — read it before trusting the defaults.
 4. --max-line defaults to the input file's own measured maximum width.
"""
import argparse, difflib, html, json, re, sys


def sec(ts):
    h, mn, rest = ts.split(":")
    s, ms = re.split("[,.]", rest)
    return int(h) * 3600 + int(mn) * 60 + int(s) + int(ms) / 1000


def fmt(t):
    ms = round(t * 1000)
    h, r = divmod(ms, 3600000); mn, r = divmod(r, 60000); s, ms = divmod(r, 1000)
    return f"{h:02d}:{mn:02d}:{s:02d},{ms:03d}"


def wrapper_of(body):
    m = re.match(r"^((?:<[^>]+>)*)(.*?)((?:</[^>]+>)*)$", body, re.S)
    return m.group(1), m.group(2), m.group(3)


def norm(t):
    return re.sub(r"[^\w'&%$€£+-]", "", t.lower())


def clean_token(t, strip_q):
    if "/" in t or re.search(r"\w\.\w", t):          # URL-ish: keep inner dots
        return re.sub(r"[.,]+$", "", t)
    t = re.sub(r",(?!\d)", "", t)                     # prose commas
    t = re.sub(r"(?<!\d),", "", t)
    t = re.sub(r"\.+$", "", t)                        # sentence-final dots
    if strip_q:
        t = t.replace("?", "")
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("srt_in"); ap.add_argument("json_path"); ap.add_argument("srt_out")
    ap.add_argument("--min-piece", type=float, default=0.24)
    ap.add_argument("--keep-gaps-over", type=float, default=0.5)
    ap.add_argument("--max-line", type=int, default=0, help="0 = measure from input")
    ap.add_argument("--strip-questions", action="store_true")
    a = ap.parse_args()

    raw = open(a.srt_in, encoding="utf-8-sig").read()
    blocks = []
    for m in re.finditer(r"(\d+)\s*\n([\d:,.]+) --> ([\d:,.]+)\s*\n(.*?)(?=\n\s*\n|\Z)", raw, re.S):
        pre, inner, suf = wrapper_of(m.group(4).rstrip("\n"))
        blocks.append({"t0": sec(m.group(2)), "t1": sec(m.group(3)), "text": inner,
                       "pre": pre, "suf": suf})
    if not blocks:
        sys.exit("no SRT blocks parsed")
    pre0, suf0 = blocks[0]["pre"], blocks[0]["suf"]
    max_line = a.max_line or max(len(b["text"]) for b in blocks)
    print(f"loaded {len(blocks)} blocks | line width limit: {max_line}")

    # ---- gap histogram (before any change) ----
    def sent_end(txt):
        return bool(re.search(r"[.?!]$", txt.strip()))
    gm, gs = [], []
    for x, y in zip(blocks, blocks[1:]):
        g = y["t0"] - x["t1"]
        if g > 0.001:
            (gs if sent_end(x["text"]) else gm).append(g)
    print(f"gap histogram — mid-sentence: n={len(gm)} max={max(gm, default=0):.2f}s | "
          f"sentence-boundary: n={len(gs)} max={max(gs, default=0):.2f}s | "
          f"boundary gaps >= {a.keep_gaps_over}s (will be KEPT): {sum(1 for g in gs if g >= a.keep_gaps_over)}")

    # ---- align to JSON for split timing ----
    data = json.load(open(a.json_path))
    jwords = [{"start": w["start"], "end": w["start"] + w["duration"], "text": w["text"]}
              for s in data["segments"] for w in s["words"] if w.get("type") == "word"]
    sw = []
    for bi, b in enumerate(blocks):
        for wi, tok in enumerate(b["text"].split()):
            sw.append((bi, wi, tok))
    sm = difflib.SequenceMatcher(a=[norm(w["text"]) for w in jwords],
                                 b=[norm(t) for _, _, t in sw], autojunk=False)
    s2j = {}
    for tag, i0, i1, j0, j1 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i1 - i0):
                s2j[j0 + k] = i0 + k
    pos = {(bi, wi): gi for gi, (bi, wi, _) in enumerate(sw)}
    print(f"aligned {len(s2j)}/{len(sw)} SRT words to JSON times")

    # ---- 1. split at sentence boundaries ----
    MP = a.min_piece
    split_n = json_n = mid_n = 0
    unsplit = []
    nb = []
    for bi, b in enumerate(blocks):
        toks = b["text"].split()
        cut = next((k for k, t in enumerate(toks[:-1])
                    if re.search(r"[.?!]$", t) and "/" not in t and not re.search(r"\w\.\w", t)), None)
        if cut is None:
            nb.append(dict(b)); continue
        t0, t1 = b["t0"], b["t1"]; dur = t1 - t0
        if dur < MP * 4 / 3:
            unsplit.append((t0, b["text"])); nb.append(dict(b)); continue
        split_n += 1
        if dur < 2 * MP:
            st = (t0 + t1) / 2; mid_n += 1
        else:
            st = None
            ja, jb = s2j.get(pos[(bi, cut)]), s2j.get(pos[(bi, cut + 1)])
            if ja is not None and jb is not None and jb == ja + 1:
                m = (jwords[ja]["end"] + jwords[jb]["start"]) / 2
                if t0 + MP <= m <= t1 - MP:
                    st = m; json_n += 1
            if st is None:
                ca = len(" ".join(toks[:cut + 1])); cb = len(" ".join(toks[cut + 1:]))
                st = min(max(t0 + dur * ca / (ca + cb), t0 + MP), t1 - MP)
        nb.append({**b, "t1": st, "text": " ".join(toks[:cut + 1])})
        nb.append({**b, "t0": st, "text": " ".join(toks[cut + 1:])})
    print(f"splits: {split_n} (JSON-timed {json_n}, midpoint {mid_n}, proportional {split_n - json_n - mid_n})")
    for t0, tx in unsplit:
        print(f"  ! unsplit short block @{fmt(t0)}: {tx!r} — sentence collision, review by eye")

    # junction type must be judged on PRE-clean text
    sent_after = [sent_end(b["text"]) for b in nb]

    # ---- 2. strip punctuation ----
    for b in nb:
        b["text"] = " ".join(filter(None, (clean_token(t, a.strip_questions) for t in b["text"].split())))
        if not b["text"]:
            sys.exit("a block emptied by cleaning — aborting")

    # ---- 3. close gaps ----
    closed = kept = 0
    for i, (x, y) in enumerate(zip(nb, nb[1:])):
        g = y["t0"] - x["t1"]
        if g <= 0.001:
            continue
        if sent_after[i] and g >= a.keep_gaps_over:
            kept += 1
            print(f"  kept breathing pause: {g:.2f}s after {fmt(x['t1'])} ({x['text']!r})")
            continue
        x["t1"] = y["t0"]; closed += 1
    print(f"gaps closed: {closed} | breathing pauses kept: {kept}")

    # ---- write ----
    out = [f"{n}\n{fmt(b['t0'])} --> {fmt(b['t1'])}\n{pre0}{b['text']}{suf0}\n"
           for n, b in enumerate(nb, 1)]
    open(a.srt_out, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print(f"written: {a.srt_out} ({len(nb)} blocks)")

    # ---- validation ----
    problems = 0
    strip_all = lambda s: [re.sub(r"[.,?!]", "", t) for t in s.split()]
    if [w for b in blocks for w in strip_all(b["text"])] != [w for b in nb for w in strip_all(b["text"])]:
        print("!! WORD CONTENT CHANGED"); problems += 1
    joined = " ".join(b["text"] for b in nb)
    if re.search(r",(?!\d)|(?<!\d),", joined):
        print("!! residual comma"); problems += 1
    for t in joined.split():
        if "/" not in t and not re.search(r"\w\.\w", t) and t.endswith("."):
            print(f"!! residual final dot: {t!r}"); problems += 1
    prev = 0; mind = 9e9
    for i, b in enumerate(nb):
        if b["t1"] <= b["t0"]: print(f"!! bad duration at {i+1}"); problems += 1
        if b["t0"] < prev - 1e-6: print(f"!! overlap at {i+1}"); problems += 1
        prev = b["t1"]; mind = min(mind, b["t1"] - b["t0"])
        if len(b["text"]) > max_line:
            print(f"!! line too long ({len(b['text'])}): {b['text']!r}"); problems += 1
    print(f"min block duration: {mind:.3f}s | question marks: {sum(b['text'].count('?') for b in nb)}")
    print("validation:", "OK" if problems == 0 else f"{problems} PROBLEMS")
    sys.exit(0 if problems == 0 else 1)


if __name__ == "__main__":
    main()
