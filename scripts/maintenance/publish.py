from __future__ import annotations

import re
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable, Sequence

from .common import run_command
from .doctor import validate_repository


class PublishError(RuntimeError):
    pass


Runner = Callable[[Sequence[str], Path | None, bool], subprocess.CompletedProcess[str]]


def build_branch_name(machine: str, timestamp: datetime) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", machine.lower()).strip("-") or "unknown-machine"
    return f"machine/{normalized}/{timestamp.astimezone(UTC).strftime('%Y%m%d-%H%M%S')}"


def _run(
    runner: Callable[..., subprocess.CompletedProcess[str]],
    args: list[str],
    repo: Path,
    *,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return runner(args, cwd=repo, check=check)


def publish_changes(
    repo: Path,
    machine: str,
    *,
    assume_yes: bool,
    runner: Callable[..., subprocess.CompletedProcess[str]] = run_command,
) -> str:
    repo = repo.resolve()
    status = _run(runner, ["git", "status", "--short"], repo).stdout.strip()
    if not status:
        raise PublishError("there are no local changes to publish")

    unstaged = _run(runner, ["git", "diff", "--"], repo).stdout.strip()
    staged = _run(runner, ["git", "diff", "--cached", "--"], repo).stdout.strip()
    print("Changes to publish:")
    print(status)
    if unstaged:
        print(unstaged)
    if staged:
        print(staged)

    report = validate_repository(repo)
    if not report.ok:
        raise PublishError(f"repository validation failed:\n{report.render()}")
    if not assume_yes:
        confirmation = input("Create a branch, commit these changes, and open a draft PR? [y/N] ")
        if confirmation.strip().lower() not in {"y", "yes"}:
            raise PublishError("publishing cancelled")

    branch = _run(runner, ["git", "branch", "--show-current"], repo).stdout.strip()
    if branch == "main":
        branch = build_branch_name(machine, datetime.now(UTC))
        _run(runner, ["git", "switch", "-c", branch], repo)
    elif not branch:
        raise PublishError("cannot publish from a detached checkout")

    _run(runner, ["git", "add", "-A"], repo)
    _run(runner, ["git", "commit", "-m", f"chore: publish skill updates from {machine}"], repo)
    _run(runner, ["git", "push", "-u", "origin", branch], repo)

    body = (
        f"## Machine update\n\n"
        f"Published from `{machine}` using the repository maintenance workflow.\n\n"
        f"## Validation\n\n```\n{report.render()}\n```\n"
    )
    body_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
            handle.write(body)
            body_path = Path(handle.name)
        title = f"chore: publish skill updates from {machine}"
        command = [
            "gh",
            "pr",
            "create",
            "--draft",
            "--base",
            "main",
            "--head",
            branch,
            "--title",
            title,
            "--body-file",
            str(body_path),
        ]
        try:
            result = _run(runner, command, repo)
        except subprocess.CalledProcessError as error:
            retry = " ".join(command)
            raise PublishError(
                f"branch and commit were pushed, but draft PR creation failed; retry with: {retry}"
            ) from error
        url = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ""
        if not url:
            raise PublishError("GitHub did not return a pull request URL")
        return url
    finally:
        if body_path is not None and body_path.exists():
            body_path.unlink()
