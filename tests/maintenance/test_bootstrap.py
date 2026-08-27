from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.maintenance.bootstrap import build_launch_agent, configure_machine


REPO_ROOT = Path(__file__).resolve().parents[2]


class BootstrapTests(unittest.TestCase):
    def test_existing_install_is_backed_up_before_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install_root = root / "skills"
            existing = install_root / "auditing-web-vitals"
            existing.mkdir(parents=True)
            (existing / "local-change.txt").write_text("keep me", encoding="utf-8")

            result = configure_machine(
                REPO_ROOT,
                root / "state",
                [install_root],
                root / "LaunchAgents",
                load_agent=False,
            )

            self.assertTrue(existing.is_symlink())
            self.assertEqual(
                existing.resolve(),
                (REPO_ROOT / "marketing/web-development/auditing-web-vitals").resolve(),
            )
            self.assertTrue(
                any(
                    backup.name == "auditing-web-vitals"
                    and (backup / "local-change.txt").read_text(encoding="utf-8") == "keep me"
                    for backup in result.backups
                )
            )

    def test_launch_agent_runs_twice_daily(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            payload = build_launch_agent(REPO_ROOT, root / "state", [root / "skills"])

            self.assertEqual(
                payload["StartCalendarInterval"],
                [{"Hour": 9, "Minute": 0}, {"Hour": 17, "Minute": 0}],
            )
            self.assertEqual(payload["ProgramArguments"][0], sys.executable)
            self.assertEqual(
                payload["ProgramArguments"][1],
                str(REPO_ROOT / "scripts/skills-sync"),
            )

    @unittest.skipUnless(Path("/usr/bin/python3").is_file(), "system Python is unavailable")
    def test_maintenance_clis_start_with_macos_system_python(self) -> None:
        scripts = (
            "install-machine-maintenance",
            "publish-skill-changes",
            "skills-doctor",
            "skills-status",
            "skills-sync",
        )

        for script in scripts:
            with self.subTest(script=script):
                completed = subprocess.run(
                    ["/usr/bin/python3", str(REPO_ROOT / "scripts" / script), "--help"],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_repeated_bootstrap_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            arguments = (
                REPO_ROOT,
                root / "state",
                [root / "skills"],
                root / "LaunchAgents",
            )

            first = configure_machine(*arguments, load_agent=False)
            second = configure_machine(*arguments, load_agent=False)

            self.assertEqual(len(first.symlinks), 3)
            self.assertEqual(len(second.symlinks), 3)
            self.assertEqual(second.backups, ())
            self.assertEqual(first.plist_path, second.plist_path)


if __name__ == "__main__":
    unittest.main()
