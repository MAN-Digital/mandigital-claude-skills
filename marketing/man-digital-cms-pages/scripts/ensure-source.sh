#!/usr/bin/env bash
set -euo pipefail

skill_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
source_dir=${MAN_DIGITAL_CMS_SOURCE:-"$skill_dir/references/source"}
repo_url=https://github.com/MAN-Digital/man-digital-cms-pages.git

if [[ ! -e "$source_dir" ]]; then
  mkdir -p "$(dirname "$source_dir")"
  git clone "$repo_url" "$source_dir" >&2
elif ! git -C "$source_dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf 'FAIL: %s exists but is not a Git worktree.\n' "$source_dir" >&2
  exit 1
fi

git -C "$source_dir" fetch --prune origin >&2

if [[ -z "$(git -C "$source_dir" status --porcelain)" ]] &&
   git -C "$source_dir" rev-parse --abbrev-ref '@{upstream}' >/dev/null 2>&1; then
  git -C "$source_dir" merge --ff-only '@{upstream}' >&2
else
  printf 'INFO: preserving the current CMS checkout without fast-forwarding because it is dirty or has no upstream.\n' >&2
fi

cd "$source_dir"
pwd
