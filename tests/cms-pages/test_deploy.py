from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "cms-pages" / "fixtures"
SKILL_SCRIPTS = REPO_ROOT / "marketing" / "web-development" / "man-digital-cms-pages" / "scripts"


def validated_zip(tmp: Path) -> Path:
    theme = tmp / "mini-theme"
    if theme.exists():
        shutil.rmtree(theme)
    shutil.copytree(FIX / "mini-theme", theme)
    out = tmp / "dist"
    out.mkdir(exist_ok=True)
    env = dict(os.environ)
    env["HS_BIN"] = str(FIX / "fake-hs")
    subprocess.run(
        [str(SKILL_SCRIPTS / "validate-theme.sh"), str(theme), "--inventory", str(FIX / "mini-inventory.json")],
        text=True, capture_output=True, env=env, check=True,
    )
    packaged = subprocess.run(
        [str(SKILL_SCRIPTS / "package-zip.sh"), str(theme), str(out), "--date", "20260926"],
        text=True, capture_output=True, check=True,
    )
    return Path(packaged.stdout.strip().removeprefix("PACKAGED: ").strip())


class DeployTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.zip = validated_zip(self.tmp)
        self.config = FIX / "portals.yaml"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_deploy(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = dict(os.environ)
        env["HS_BIN"] = str(FIX / "fake-hs")
        env["HUBSPOT_BIN"] = str(FIX / "fake-hs")
        return subprocess.run(
            [str(SKILL_SCRIPTS / "deploy.sh"), *args],
            text=True, capture_output=True, env=env, input="",
        )

    def test_no_yes_stops_after_plan(self) -> None:
        result = self.run_deploy("--portal", "staging", "--zip", str(self.zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run")
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn("AUTHORIZATION REQUIRED", result.stdout)
        self.assertIn("DRY-RUN", result.stdout)

    def test_dry_run_with_yes_lists_all_steps(self) -> None:
        result = self.run_deploy("--portal", "prod", "--zip", str(self.zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        for step in ("verify evidence", "upload images", "upload theme", "pages", "menus", "blog", "forms"):
            self.assertIn(step, result.stdout)

    def test_refuses_unvalidated_zip(self) -> None:
        bad = self.tmp / "bad.zip"
        shutil.copy(self.zip, bad)
        subprocess.run(["zip", "-d", str(bad), "mini-theme/QA-EVIDENCE.json"],
                       text=True, capture_output=True, check=True)
        result = self.run_deploy("--portal", "staging", "--zip", str(bad), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QA-EVIDENCE", result.stderr + result.stdout)

    def test_unknown_portal_is_usage_error(self) -> None:
        result = self.run_deploy("--portal", "nope", "--zip", str(self.zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
