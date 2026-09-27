from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "cms-pages" / "fixtures"
SCRIPT = REPO_ROOT / "marketing" / "web-development" / "man-digital-cms-pages" / "scripts" / "verify-fm.sh"


def run_verify(theme: Path, *args: str, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["HS_BIN"] = str(FIX / "fake-hs")
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [str(SCRIPT), str(theme), *args],
        text=True, capture_output=True, env=env,
    )


class VerifyFmTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.theme = self.tmp / "mini-theme"
        shutil.copytree(FIX / "mini-theme", self.theme)
        self.config = FIX / "portals.yaml"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_all_present_exits_zero(self) -> None:
        result = run_verify(self.theme, "--portal", "staging", "--config", str(self.config))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK /brand/x.jpg", result.stdout)
        self.assertIn("test-staging", result.stdout)  # hsAccount resolved from portals.yaml

    def test_missing_file_exits_one_naming_it(self) -> None:
        assets = self.theme / "assets.json"
        data = json.loads(assets.read_text(encoding="utf-8"))
        data["files"].append({"local": "images/hero/missing.jpg", "dest": "/brand/missing.jpg"})
        assets.write_text(json.dumps(data), encoding="utf-8")
        result = run_verify(
            self.theme, "--portal", "staging", "--config", str(self.config),
            env_extra={"FAKE_FM_MISSING": "/brand/missing.jpg"},
        )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("OK /brand/x.jpg", result.stdout)
        self.assertIn("MISSING /brand/missing.jpg", result.stdout)
        self.assertIn("/brand/missing.jpg", result.stderr)

    def test_unknown_portal_is_usage_error(self) -> None:
        result = run_verify(self.theme, "--portal", "nope", "--config", str(self.config))
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown portal", result.stderr)


if __name__ == "__main__":
    unittest.main()
