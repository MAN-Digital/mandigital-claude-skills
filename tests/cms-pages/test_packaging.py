from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "cms-pages" / "fixtures"
SKILL_SCRIPTS = REPO_ROOT / "marketing" / "web-development" / "man-digital-cms-pages" / "scripts"


class PackagingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.theme = self.tmp / "mini-theme"
        shutil.copytree(FIX / "mini-theme", self.theme)
        self.out = self.tmp / "dist"
        self.out.mkdir()
        env = dict(os.environ)
        env["HS_BIN"] = str(FIX / "fake-hs")
        validated = subprocess.run(
            [str(SKILL_SCRIPTS / "validate-theme.sh"), str(self.theme), "--inventory", str(FIX / "mini-inventory.json")],
            text=True, capture_output=True, env=env,
        )
        self.assertEqual(validated.returncode, 0, validated.stderr)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_zip_name_and_roundtrip(self) -> None:
        result = subprocess.run(
            [str(SKILL_SCRIPTS / "package-zip.sh"), str(self.theme), str(self.out), "--date", "20260926"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        zips = list(self.out.glob("*.zip"))
        self.assertEqual(len(zips), 1)
        self.assertTrue(re.fullmatch(r"mini-20260926-[a-z0-9]+\.zip", zips[0].name), zips[0].name)
        with zipfile.ZipFile(zips[0]) as archive:
            self.assertIn("mini-theme/QA-EVIDENCE.json", archive.namelist())
            archive.extractall(self.tmp / "unpacked")
        diff = subprocess.run(
            ["diff", "-r", str(self.theme), str(self.tmp / "unpacked" / "mini-theme")],
            text=True, capture_output=True,
        )
        self.assertEqual(diff.returncode, 0, diff.stdout)

    def test_refuses_unvalidated_theme(self) -> None:
        (self.theme / "QA-EVIDENCE.json").unlink()
        result = subprocess.run(
            [str(SKILL_SCRIPTS / "package-zip.sh"), str(self.theme), str(self.out), "--date", "20260926"],
            text=True, capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QA-EVIDENCE", result.stderr)

    def test_failed_gates_refused_with_message(self) -> None:
        import json

        evidence_path = self.theme / "QA-EVIDENCE.json"
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        evidence["gates"]["g4"] = "fail"
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
        result = subprocess.run(
            [str(SKILL_SCRIPTS / "package-zip.sh"), str(self.theme), str(self.out), "--date", "20260926"],
            text=True, capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.out.glob("*.zip")), [])
        self.assertIn("gates not all pass", result.stderr)

    def test_date_flag_without_value_is_clean_error(self) -> None:
        result = subprocess.run(
            [str(SKILL_SCRIPTS / "package-zip.sh"), str(self.theme), str(self.out), "--date"],
            text=True, capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("unbound variable", result.stderr)

    def test_label_sanitized(self) -> None:
        import json

        theme_json = self.theme / "theme.json"
        data = json.loads(theme_json.read_text(encoding="utf-8"))
        data["label"] = "a/b c"
        theme_json.write_text(json.dumps(data), encoding="utf-8")
        env = dict(os.environ)
        env["HS_BIN"] = str(FIX / "fake-hs")
        validated = subprocess.run(
            [str(SKILL_SCRIPTS / "validate-theme.sh"), str(self.theme), "--inventory", str(FIX / "mini-inventory.json")],
            text=True, capture_output=True, env=env,
        )
        self.assertEqual(validated.returncode, 0, validated.stderr)
        result = subprocess.run(
            [str(SKILL_SCRIPTS / "package-zip.sh"), str(self.theme), str(self.out), "--date", "20260926"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        zips = list(self.out.glob("*.zip"))
        self.assertEqual(len(zips), 1)
        self.assertTrue(re.fullmatch(r"a_b_c-20260926-[a-z0-9]+\.zip", zips[0].name), zips[0].name)


if __name__ == "__main__":
    unittest.main()
