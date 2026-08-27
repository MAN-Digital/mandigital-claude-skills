#!/usr/bin/env python3
"""Apply a reviewed edit spec to an SRT, producing the CORRECTED version.

Usage:
    python3 apply_edits.py SOURCE.srt EDITS.json OUT.srt

EDITS.json (block numbers are the SOURCE file's indices, as strings):
{
  "edits":   {"904": ["Europe or in US.", "or in the US."]},
  "retime":  {"904": "00:14:24,291 --> 00:14:25,279"},
  "inserts": {"1367": [["00:22:11,600 --> 00:22:12,707", "So you utilize"],
                        ["00:22:12,707 --> 00:22:13,640", "those skills."]]},
  "forbid":  ["HOPSPOT", "XQL", "SQA", "Mando"]
}

- "edits" values are [old inner-text substring (must occur exactly once), new].
- "inserts" blocks are added AFTER the given source block, wrapped in the file's
  own style tags. All blocks are renumbered sequentially.
- "forbid" strings must not appear anywhere in the output (residue check).

Validations (exit non-zero on failure): unique edit matches, style wrapper
integrity, positive durations, monotonic non-overlapping times, line width
within the source file's own measured maximum, forbid-residue.
"""
import html, json, re, sys


def sec(ts):
    h, mn, rest = ts.split(":")
    s, ms = re.split("[,.]", rest)
    return int(h) * 3600 + int(mn) * 60 + int(s) + int(ms) / 1000


def wrapper_of(body):
    m = re.match(r"^((?:<[^>]+>)*)(.*?)((?:</[^>]+>)*)$", body, re.S)
    return m.group(1), m.group(2), m.group(3)


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    src, spec_path, dst = sys.argv[1:4]
    spec = json.load(open(spec_path))
    edits = {int(k): v for k, v in spec.get("edits", {}).items()}
    retime = {int(k): v for k, v in spec.get("retime", {}).items()}
    inserts = {int(k): v for k, v in spec.get("inserts", {}).items()}
    forbid = spec.get("forbid", [])

    raw = open(src, encoding="utf-8-sig").read()
    blocks = []
    for m in re.finditer(r"(\d+)\s*\n([\d:,.]+ --> [\d:,.]+)\s*\n(.*?)(?=\n\s*\n|\Z)", raw, re.S):
        blocks.append([int(m.group(1)), m.group(2), m.group(3).rstrip("\n")])
    if not blocks:
        sys.exit("no SRT blocks parsed")

    pre0, _, suf0 = wrapper_of(blocks[0][2])
    max_len_src = max(len(wrapper_of(b[2])[1]) for b in blocks)

    problems = 0
    known = set(edits) | set(retime) | set(inserts)
    missing = known - {b[0] for b in blocks}
    if missing:
        sys.exit(f"spec references unknown block(s): {sorted(missing)}")

    applied = 0
    for b in blocks:
        idx = b[0]
        if idx in edits:
            old, new = edits[idx]
            pre, inner, suf = wrapper_of(b[2])
            if inner.count(old) != 1:
                print(f"!! block {idx}: {old!r} found {inner.count(old)}x (need exactly 1) in {inner!r}")
                problems += 1
            else:
                b[2] = pre + inner.replace(old, new) + suf
                applied += 1
        if idx in retime:
            b[1] = retime[idx]

    out_blocks = []
    for b in blocks:
        out_blocks.append(b)
        for t, text in inserts.get(b[0], []):
            out_blocks.append([None, t, f"{pre0}{text}{suf0}"])

    if problems:
        sys.exit(f"aborted: {problems} edit problem(s), nothing written")

    lines = [f"{n}\n{b[1]}\n{b[2]}\n" for n, b in enumerate(out_blocks, 1)]
    open(dst, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(f"edits applied: {applied}/{len(edits)} | retimed: {len(retime)} | "
          f"inserted: {sum(len(v) for v in inserts.values())} | blocks: {len(blocks)} -> {len(out_blocks)}")
    print(f"written: {dst}")

    # ---- validation ----
    prev_end = 0.0
    for n, b in enumerate(out_blocks, 1):
        t0, t1 = b[1].split(" --> ")
        if not sec(t1) > sec(t0):
            print(f"!! non-positive duration at block {n}"); problems += 1
        if sec(t0) < prev_end - 0.001:
            print(f"!! overlap at block {n} ({t0} starts before previous end)"); problems += 1
        prev_end = sec(t1)
        pre, inner, suf = wrapper_of(b[2])
        if (pre, suf) != (pre0, suf0):
            print(f"!! style wrapper differs at block {n}"); problems += 1
        if len(inner) > max_len_src:
            print(f"!! line longer than source max ({len(inner)} > {max_len_src}) at block {n}: {inner!r}")
            problems += 1
    joined = "\n".join(b[2] for b in out_blocks)
    for bad in forbid:
        if bad in joined:
            print(f"!! forbidden residue present: {bad!r}"); problems += 1
    print(f"source max line width: {max_len_src} chars (enforced)")
    print("validation:", "OK" if problems == 0 else f"{problems} PROBLEMS")
    sys.exit(0 if problems == 0 else 1)


if __name__ == "__main__":
    main()
