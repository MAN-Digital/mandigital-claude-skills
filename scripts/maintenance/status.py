from __future__ import annotations

import json
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from .common import load_manifest, run_command


def _git(repo: Path, *arguments: str, check: bool = True) -> str:
    result = run_command(["git", *arguments], cwd=repo, check=check)
    return result.stdout.strip()


def collect_status(
    repo: Path,
    state_dir: Path,
    install_roots: Sequence[Path],
) -> dict[str, object]:
    repo = repo.resolve()
    branch = _git(repo, "branch", "--show-current")
    commit = _git(repo, "rev-parse", "HEAD")
    dirty = bool(_git(repo, "status", "--porcelain"))
    remote_commit = _git(repo, "rev-parse", "origin/main", check=False)
    ahead = 0
    behind = 0
    if remote_commit:
        counts = _git(repo, "rev-list", "--left-right", "--count", "HEAD...origin/main", check=False)
        if counts:
            ahead, behind = (int(value) for value in counts.split())

    links: dict[str, dict[str, object]] = {}
    for root in install_roots:
        for skill in load_manifest(repo):
            destination = root / skill.install_name
            expected = (repo / skill.repo_path).resolve()
            actual = destination.resolve() if destination.exists() or destination.is_symlink() else None
            links[f"{root}:{skill.install_name}"] = {
                "exists": destination.exists(),
                "is_symlink": destination.is_symlink(),
                "correct": destination.is_symlink() and actual == expected,
                "target": str(actual) if actual else None,
            }

    previous: dict[str, object] | None = None
    status_file = state_dir / "status.json"
    if status_file.is_file():
        try:
            previous = json.loads(status_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            previous = None

    return {
        "machine": platform.node(),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "repo": str(repo),
        "branch": branch,
        "commit": commit,
        "remote_commit": remote_commit or None,
        "dirty": dirty,
        "ahead": ahead,
        "behind": behind,
        "links": links,
        "last_run": previous,
    }
