#!/usr/bin/env bash
# Build the versioned deploy ZIP from a validated theme dir.
# Usage: package-zip.sh <theme-dir> <out-dir> [--date YYYYMMDD]
set -euo pipefail

command -v zip >/dev/null 2>&1 || { echo "FAIL: 'zip' command not found" >&2; exit 1; }
[[ $# -ge 2 ]] || { echo "usage: package-zip.sh <theme-dir> <out-dir> [--date YYYYMMDD]" >&2; exit 2; }
theme_dir=$(cd "$1" && pwd)
mkdir -p "$2" 2>/dev/null; out_dir=$(cd "$2" && pwd)
stamp=""; if [[ "${3:-}" == "--date" ]]; then stamp="${4:-}"; else stamp=$(date -u +%Y%m%d); fi
[[ "$stamp" =~ ^[0-9]{8}$ ]] || { echo "FAIL: bad date stamp: $stamp" >&2; exit 1; }

evidence="$theme_dir/QA-EVIDENCE.json"
[[ -f "$evidence" ]] || { echo "FAIL: missing QA-EVIDENCE.json — run validate-theme.sh first" >&2; exit 1; }
meta=$(python3 - "$evidence" <<'PYEOF' 2>&1
import json, re, sys
ev = json.load(open(sys.argv[1], encoding="utf-8"))
gates = ev.get("gates", {})
if [gates.get(g) for g in ("g1", "g2", "g3", "g4")] != ["pass"] * 4:
    sys.exit("gates not all pass")
commit = re.sub(r"[^a-z0-9]", "", ev.get("commit", "n/a").lower())[:7] or "nosha"
print(f"{ev['theme']}|{commit}")
PYEOF
) || { echo "FAIL: QA-EVIDENCE invalid: $meta" >&2; exit 1; }
label="${meta%%|*}"; short="${meta##*|}"
label=$(printf '%s' "$label" | tr -cs 'A-Za-z0-9._-' '_')
[[ -n "$label" ]] || { echo "FAIL: empty theme label" >&2; exit 1; }
zip_name="$label-$stamp-$short.zip"
tmp_zip="$out_dir/.$zip_name.part"; (cd "$(dirname "$theme_dir")" && zip -qr "$tmp_zip" "$(basename "$theme_dir")") && mv "$tmp_zip" "$out_dir/$zip_name"
echo "PACKAGED: $out_dir/$zip_name"
