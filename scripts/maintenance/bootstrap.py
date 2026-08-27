from __future__ import annotations

import os
import plistlib
import shutil
import sys
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from .common import load_manifest, run_command
from .doctor import validate_repository


LAUNCH_AGENT_LABEL = "com.man-digital.skills-sync"


@dataclass(frozen=True)
class BootstrapResult:
    symlinks: tuple[Path, ...]
    backups: tuple[Path, ...]
    plist_path: Path


def build_launch_agent(
    repo: Path,
    state_dir: Path,
    install_roots: Sequence[Path],
) -> dict[str, object]:
    repo = repo.resolve()
    state_dir = state_dir.resolve()
    arguments = [
        sys.executable,
        str(repo / "scripts/skills-sync"),
        "--repo",
        str(repo),
        "--state-dir",
        str(state_dir),
    ]
    for root in install_roots:
        arguments.extend(["--install-root", str(root.resolve())])
    return {
        "Label": LAUNCH_AGENT_LABEL,
        "ProgramArguments": arguments,
        "WorkingDirectory": str(repo),
        "RunAtLoad": True,
        "ProcessType": "Background",
        "StartCalendarInterval": [
            {"Hour": 9, "Minute": 0},
            {"Hour": 17, "Minute": 0},
        ],
        "StandardOutPath": str(state_dir / "logs/sync.out.log"),
        "StandardErrorPath": str(state_dir / "logs/sync.err.log"),
        "EnvironmentVariables": {"PYTHONUNBUFFERED": "1"},
    }


def _write_plist(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            plistlib.dump(payload, handle, sort_keys=True)
        os.replace(temporary_name, path)
    finally:
        temporary_path = Path(temporary_name)
        if temporary_path.exists():
            temporary_path.unlink()


def _load_launch_agent(plist_path: Path) -> None:
    if sys.platform != "darwin":
        raise RuntimeError("LaunchAgent installation requires macOS")
    domain = f"gui/{os.getuid()}"
    loaded = run_command(
        ["launchctl", "print", f"{domain}/{LAUNCH_AGENT_LABEL}"],
        check=False,
    )
    if loaded.returncode == 0:
        run_command(["launchctl", "bootout", domain, str(plist_path)])
    run_command(["launchctl", "bootstrap", domain, str(plist_path)])


def configure_machine(
    repo: Path,
    state_dir: Path,
    install_roots: Sequence[Path],
    launch_agents_dir: Path,
    *,
    load_agent: bool = True,
) -> BootstrapResult:
    repo = repo.resolve()
    state_dir = state_dir.resolve()
    report = validate_repository(repo)
    if not report.ok:
        raise RuntimeError(f"repository validation failed:\n{report.render()}")
    if not install_roots:
        raise ValueError("at least one install root is required")

    run_command(["git", "config", "core.hooksPath", ".githooks"], cwd=repo)
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "logs").mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup_root = state_dir / "backups" / f"{stamp}-{uuid.uuid4().hex[:8]}"
    backups: list[Path] = []
    symlinks: list[Path] = []

    for root_index, install_root in enumerate(install_roots):
        install_root = install_root.resolve()
        install_root.mkdir(parents=True, exist_ok=True)
        for skill in load_manifest(repo):
            source = (repo / skill.repo_path).resolve()
            destination = install_root / skill.install_name
            if destination.is_symlink() and destination.resolve() == source:
                symlinks.append(destination)
                continue
            if destination.exists() or destination.is_symlink():
                backup = backup_root / f"root-{root_index}" / skill.install_name
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(destination), str(backup))
                backups.append(backup)
            destination.symlink_to(source, target_is_directory=True)
            symlinks.append(destination)

    payload = build_launch_agent(repo, state_dir, install_roots)
    plist_path = launch_agents_dir.resolve() / f"{LAUNCH_AGENT_LABEL}.plist"
    _write_plist(plist_path, payload)
    if load_agent:
        _load_launch_agent(plist_path)
    return BootstrapResult(tuple(symlinks), tuple(backups), plist_path)
