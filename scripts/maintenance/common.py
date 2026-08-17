from __future__ import annotations

import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


@dataclass(frozen=True)
class ManagedSkill:
    repo_path: str
    install_name: str


def run_command(
    args: Sequence[str],
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(argument) for argument in args],
        cwd=str(cwd) if cwd else None,
        check=check,
        text=True,
        capture_output=True,
    )


def load_manifest(repo: Path, manifest: Path | None = None) -> list[ManagedSkill]:
    manifest_path = manifest or repo / "automation" / "managed-skills.txt"
    if not manifest_path.is_file():
        return []

    skills: list[ManagedSkill] = []
    for line_number, raw_line in enumerate(
        manifest_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("|", maxsplit=1)]
        if len(parts) != 2 or not all(parts):
            raise ValueError(f"{manifest_path}:{line_number}: expected repo-path|install-name")
        repo_path, install_name = parts
        if Path(repo_path).is_absolute() or ".." in Path(repo_path).parts:
            raise ValueError(f"{manifest_path}:{line_number}: repository path must be relative")
        skills.append(ManagedSkill(repo_path=repo_path, install_name=install_name))
    return skills


def write_status(state_dir: Path, payload: Mapping[str, object]) -> Path:
    state_dir.mkdir(parents=True, exist_ok=True)
    destination = state_dir / "status.json"
    descriptor, temporary_name = tempfile.mkstemp(prefix="status.", suffix=".json", dir=state_dir)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary_name, destination)
    finally:
        temporary_path = Path(temporary_name)
        if temporary_path.exists():
            temporary_path.unlink()
    return destination
