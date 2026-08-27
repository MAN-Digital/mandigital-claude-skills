#!/usr/bin/env python3
"""Cross-reference a DaVinci Resolve SRT caption export against a Premiere Pro
transcript JSON (word-level confidence) and print every disagreement with
timestamps, confidences and context — the review input for subtitle QA.

Usage:
    python3 align_report.py TRANSCRIPT.json CAPTIONS.srt [--low-conf 0.70]

Output (stdout): header stats, one section per diff (### REPLACE/INSERT/DELETE),
then the low-confidence matched-words list. INSERT = word only in the SRT,
DELETE = word only in the Premiere JSON.
"""
import argparse, difflib, html, json, re, sys


def ts2sec(ts):
    h, m, rest = ts.split(":")
    s, ms = re.split("[,.]", rest)
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def fmt_time(sec):
    h = int(sec // 3600); m = int(sec % 3600 // 60); s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def norm(t):
    return re.sub(r"[^\w'&%$€£+-]", "", t.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("srt_path")
    ap.add_argument("--low-conf", type=float, default=0.70,
                    help="matched words below this Premiere confidence get listed")
    a = ap.parse_args()

    data = json.load(open(a.json_path))
    jwords = [{"start": w["start"], "dur": w["duration"],
               "conf": w.get("confidence"), "text": w["text"]}
              for seg in data["segments"] for w in seg["words"]
              if w.get("type") == "word"]

    raw = open(a.srt_path, encoding="utf-8-sig").read()
    swords, last_end = [], 0.0
    for m in re.finditer(
            r"(\d+)\s*\n(\d\d:\d\d:\d\d[,.]\d\d\d)\s*-->\s*(\d\d:\d\d:\d\d[,.]\d\d\d)\s*\n(.*?)(?=\n\s*\n|\Z)",
            raw, re.S):
        idx, t0, t1, body = int(m.group(1)), m.group(2), m.group(3), m.group(4)
        last_end = max(last_end, ts2sec(t1))
        for tok in strip_tags(body).replace("\n", " ").split():
            swords.append({"blk": idx, "t0": t0, "text": tok})

    jn = [norm(w["text"]) for w in jwords]
    sn = [norm(w["text"]) for w in swords]
    sm = difflib.SequenceMatcher(a=jn, b=sn, autojunk=False)
    ops = sm.get_opcodes()

    jtail = jwords[-1]["start"] + jwords[-1]["dur"] if jwords else 0
    print(f"JSON words: {len(jwords)}   SRT words: {len(swords)}   "
          f"SRT ends {fmt_time(last_end)} / JSON ends {fmt_time(jtail)}"
          + ("   <- JSON tail past SRT end is normally outro junk: disregard"
             if jtail > last_end + 5 else ""))
    print(f"matched words: {sum(i1-i0 for t, i0, i1, j0, j1 in ops if t == 'equal')}")
    print("=" * 100)

    def jctx(i0, i1, pad=6):
        lo, hi = max(0, i0 - pad), min(len(jwords), i1 + pad)
        parts = []
        for k in range(lo, hi):
            w = jwords[k]
            cs = f"[{w['conf']:.2f}]" if (w["conf"] is not None and w["conf"] < 1) else ""
            mk, emk = ("«", "»") if i0 <= k < i1 else ("", "")
            parts.append(f"{mk}{w['text']}{cs}{emk}")
        return " ".join(parts)

    def sctx(j0, j1, pad=6):
        lo, hi = max(0, j0 - pad), min(len(swords), j1 + pad)
        return " ".join(("«" + w["text"] + "»") if j0 <= k < j1 else w["text"]
                        for k, w in enumerate(swords[lo:hi], lo))

    for tag, i0, i1, j0, j1 in ops:
        if tag == "equal":
            continue
        t = jwords[min(i0, len(jwords) - 1)]["start"]
        srt_ref = swords[min(j0, len(swords) - 1)]
        jtxt = " ".join(w["text"] for w in jwords[i0:i1]) or "∅"
        stxt = " ".join(w["text"] for w in swords[j0:j1]) or "∅"
        confs = [w["conf"] for w in jwords[i0:i1] if w["conf"] is not None]
        conf_s = ",".join(f"{c:.2f}" for c in confs) if confs else "-"
        print(f"\n### {tag.upper()} @ json {fmt_time(t)} / srt block {srt_ref['blk']} ({srt_ref['t0']})")
        print(f"  PREMIERE: {jtxt}   (conf: {conf_s})")
        print(f"  DAVINCI : {stxt}")
        print(f"  ctxJ: {jctx(i0, i1)}")
        print(f"  ctxS: {sctx(j0, j1)}")

    print("\n" + "=" * 100)
    print(f"LOW-CONFIDENCE MATCHED WORDS (< {a.low_conf:.2f} — engines agree; ear-check only if context reads oddly)")
    n = 0
    for tag, i0, i1, j0, j1 in ops:
        if tag != "equal":
            continue
        for k in range(i1 - i0):
            w = jwords[i0 + k]
            if w["conf"] is not None and w["conf"] < a.low_conf:
                print(f"  {fmt_time(w['start'])}  conf={w['conf']:.2f}  {w['text']!r}  (srt blk {swords[j0+k]['blk']})")
                n += 1
    print(f"total: {n}")


if __name__ == "__main__":
    main()
