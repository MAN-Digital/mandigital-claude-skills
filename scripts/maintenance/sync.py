from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence

from .common import load_manifest, run_command, write_status
from .doctor import validate_repository


class SyncError(RuntimeError):
    pass


@dataclass(frozen=True)
class SyncResult:
    changed: bool
    commit: str
    message: str


def _git(repo: Path, *arguments: str, check: bool = True) -> str:
    result = run_command(["git", *arguments], cwd=repo, check=check)
    if check or result.returncode == 0:
        return result.stdout.strip()
    return ""


def _verify_links(repo: Path, install_roots: Sequence[Path]) -> None:
    for root in install_roots:
        for skill in load_manifest(repo):
            destination = root / skill.install_name
            expected = (repo / skill.repo_path).resolve()
            if not destination.is_symlink():
                raise SyncError(f"managed install is not a symlink: {destination}")
            if destination.resolve() != expected:
                raise SyncError(f"managed install points to the wrong target: {destination}")


def sync_checkout(
    repo: Path,
    state_dir: Path,
    install_roots: Sequence[Path],
    *,
    remote: str = "origin",
    branch: str = "main",
) -> SyncResult:
    repo = repo.resolve()
    state_dir = state_dir.resolve()
    state_dir.mkdir(parents=True, exist_ok=True)
    lock = state_dir / "sync.lock"
    try:
        lock.mkdir()
    except FileExistsError as error:
        raise SyncError(f"skill synchronization is already running: {lock}") from error

    candidate_root: Path | None = None
    candidate_checkout: Path | None = None
    worktree_added = False
    try:
        active_branch = _git(repo, "branch", "--show-current")
        if active_branch != branch:
            raise SyncError(f"checkout must be on {branch}; active branch is {active_branch or 'detached'}")
        if _git(repo, "status", "--porcelain"):
            raise SyncError("checkout is dirty; local changes were preserved")

        _git(repo, "fetch", remote, branch)
        current = _git(repo, "rev-parse", "HEAD")
        candidate = _git(repo, "rev-parse", f"{remote}/{branch}")
        if current == candidate:
            report = validate_repository(repo)
            if not report.ok:
                raise SyncError(f"current checkout validation failed:\n{report.render()}")
            _verify_links(repo, install_roots)
            result = SyncResult(False, current, "already up to date")
        else:
            ancestor = run_command(
                ["git", "merge-base", "--is-ancestor", current, candidate],
                cwd=repo,
                check=False,
            )
            if ancestor.returncode != 0:
                raise SyncError("origin/main cannot be fast-forwarded from the installed commit")

            candidate_root = Path(tempfile.mkdtemp(prefix="candidate.", dir=state_dir))
            candidate_checkout = candidate_root / "checkout"
            _git(repo, "worktree", "add", "--detach", str(candidate_checkout), candidate)
            worktree_added = True
            report = validate_repository(candidate_checkout)
            if not report.ok:
                raise SyncError(f"remote candidate validation failed:\n{report.render()}")
            _git(repo, "worktree", "remove", str(candidate_checkout))
            worktree_added = False
            _git(repo, "merge", "--ff-only", f"{remote}/{branch}")

            updated_report = validate_repository(repo)
            if not updated_report.ok:
                raise SyncError(f"updated checkout validation failed:\n{updated_report.render()}")
            _verify_links(repo, install_roots)
            result = SyncResult(True, candidate, "updated and validated")

        write_status(
            state_dir,
            {
                "ok": True,
                "changed": result.changed,
                "commit": result.commit,
                "message": result.message,
                "finished_at": datetime.now(UTC).isoformat(),
            },
        )
        return result
    except Exception as error:
        write_status(
            state_dir,
            {
                "ok": False,
                "error": str(error),
                "finished_at": datetime.now(UTC).isoformat(),
            },
        )
        if isinstance(error, SyncError):
            raise
        raise SyncError(str(error)) from error
    finally:
        if worktree_added and candidate_checkout is not None:
            run_command(["git", "worktree", "remove", "--force", str(candidate_checkout)], cwd=repo, check=False)
        if candidate_root is not None:
            shutil.rmtree(candidate_root, ignore_errors=True)
        lock.rmdir()
