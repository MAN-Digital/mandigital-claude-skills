from __future__ import annotations

import subprocess
from pathlib import Path


def git(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


class GitFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.remote = root / "remote.git"
        self.seed = root / "seed"
        self.managed = root / "managed"
        self.state = root / "state"

        git(["init", "--bare", str(self.remote)])
        git(["init", "-b", "main", str(self.seed)])
        git(["config", "user.name", "Test User"], self.seed)
        git(["config", "user.email", "test@example.com"], self.seed)
        self._write_valid_skill(self.seed / "marketing" / "example-skill")
        (self.seed / "README.md").write_text("# Fixture\n", encoding="utf-8")
        git(["add", "."], self.seed)
        git(["commit", "-m", "initial"], self.seed)
        git(["remote", "add", "origin", str(self.remote)], self.seed)
        git(["push", "-u", "origin", "main"], self.seed)
        git(["symbolic-ref", "HEAD", "refs/heads/main"], self.remote)
        git(["clone", str(self.remote), str(self.managed)])
        git(["config", "user.name", "Managed User"], self.managed)
        git(["config", "user.email", "managed@example.com"], self.managed)
        self.managed_head = self.head(self.managed)

    @staticmethod
    def _write_valid_skill(skill: Path) -> None:
        skill.mkdir(parents=True, exist_ok=True)
        (skill / "SKILL.md").write_text(
            "---\nname: example-skill\ndescription: Validate fixture repositories.\n---\n\n# Example\n",
            encoding="utf-8",
        )

    def head(self, repo: Path) -> str:
        return git(["rev-parse", "HEAD"], repo)

    def push_valid_change(self) -> str:
        (self.seed / "CHANGE.md").write_text("valid update\n", encoding="utf-8")
        git(["add", "CHANGE.md"], self.seed)
        git(["commit", "-m", "valid update"], self.seed)
        git(["push"], self.seed)
        return self.head(self.seed)

    def push_invalid_skill(self) -> str:
        broken = self.seed / "marketing" / "broken-skill"
        broken.mkdir(parents=True)
        (broken / "SKILL.md").write_text(
            "---\nname: broken-skill\nversion: 1\n---\n",
            encoding="utf-8",
        )
        git(["add", "."], self.seed)
        git(["commit", "-m", "invalid update"], self.seed)
        git(["push"], self.seed)
        return self.head(self.seed)


def create_dirty_git_repo(root: Path) -> Path:
    repo = root / "publisher"
    git(["init", "-b", "main", str(repo)])
    git(["config", "user.name", "Publisher Test"], repo)
    git(["config", "user.email", "publisher@example.com"], repo)
    skill = repo / "marketing" / "example-skill"
    GitFixture._write_valid_skill(skill)
    git(["add", "."], repo)
    git(["commit", "-m", "initial"], repo)
    (repo / "CHANGE.md").write_text("local change\n", encoding="utf-8")
    return repo


class RecordingRunner:
    def __init__(self, pr_url: str) -> None:
        self.pr_url = pr_url
        self.calls: list[list[str]] = []

    def __call__(
        self,
        args: list[str],
        cwd: Path | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        arguments = [str(value) for value in args]
        self.calls.append(arguments)
        stdout = ""
        if arguments[:3] == ["git", "branch", "--show-current"]:
            stdout = "main\n"
        elif arguments[:3] == ["git", "status", "--short"]:
            stdout = "?? CHANGE.md\n"
        elif arguments[:3] == ["gh", "pr", "create"]:
            stdout = f"{self.pr_url}\n"
        return subprocess.CompletedProcess(arguments, 0, stdout=stdout, stderr="")
