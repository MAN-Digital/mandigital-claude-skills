#!/usr/bin/env bash
set -euo pipefail

skill_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
source_dir=${1:-${MAN_DIGITAL_CMS_SOURCE:-"$skill_dir/references/source"}}

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

[[ -d "$source_dir" ]] || fail "CMS source checkout is missing. Run scripts/ensure-source.sh first."
source_dir=$(cd "$source_dir" && pwd)
git -C "$source_dir" rev-parse --is-inside-work-tree >/dev/null 2>&1 || fail "CMS source checkout is not a Git worktree."
[[ -f "$source_dir/README.md" ]] || fail "Missing README.md."
[[ -f "$source_dir/theme/theme.json" ]] || fail "Missing theme/theme.json."
[[ -d "$source_dir/theme/templates" ]] || fail "Missing theme/templates/."
[[ -d "$source_dir/theme/modules" ]] || fail "Missing theme/modules/."
[[ -f "$source_dir/pages/revops-service/BUILD-NOTES.md" ]] || fail "Missing RevOps Service build notes."
[[ -f "$source_dir/pages/revops-service/base.html" ]] || fail "Missing RevOps Service base template."

if rg -n --glob '!docs/psi-*.txt' '^(<<<<<<< [^=]+|=======[[:space:]]*$|>>>>>>> [^=]+)$' "$source_dir" >/dev/null; then
  fail "Unresolved merge conflict markers found."
fi

json_count=$(find "$source_dir" -type f -name '*.json' -print0 | python3 -c '
import json, sys
paths = sys.stdin.buffer.read().split(b"\0")
count = 0
for raw in paths:
    if not raw:
        continue
    path = raw.decode()
    with open(path, encoding="utf-8") as handle:
        json.load(handle)
    count += 1
print(count)
')

[[ "$json_count" -gt 0 ]] || fail "No JSON configuration files found."
git_head=$(git -C "$source_dir" rev-parse --short HEAD)
printf 'PASS: MAN Digital CMS source validated (%s; %s JSON files).\n' "$git_head" "$json_count"
