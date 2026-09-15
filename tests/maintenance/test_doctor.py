from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.maintenance.common import load_manifest
from scripts.maintenance.doctor import validate_repository


REPO_ROOT = Path(__file__).resolve().parents[2]


class DoctorTests(unittest.TestCase):
    def test_manifest_resolves_default_three(self) -> None:
        skills = load_manifest(REPO_ROOT)

        self.assertEqual(
            [skill.install_name for skill in skills],
            [
                "man-digital-cms-pages",
                "man-digital-figma-website-design",
                "auditing-web-vitals",
            ],
        )
        self.assertTrue(
            all((REPO_ROOT / skill.repo_path / "SKILL.md").is_file() for skill in skills)
        )

    def test_invalid_skill_frontmatter_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            skill = repo / "marketing" / "broken-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: broken-skill\nversion: 1\n---\n",
                encoding="utf-8",
            )

            report = validate_repository(repo, quick=True)

            self.assertFalse(report.ok)
            self.assertTrue(
                any(
                    "description" in issue.message or "version" in issue.message
                    for issue in report.issues
                )
            )

    def test_user_invocable_accepts_boolean_literals(self) -> None:
        for value in ("true", "false", "True", "False", "TRUE", "FALSE"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                repo = Path(directory)
                skill = repo / "marketing" / "example"
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(
                    "---\nname: example\ndescription: Example skill.\n"
                    f"user-invocable: {value}\n---\n", encoding="utf-8"
                )
                report = validate_repository(repo, quick=True)
                self.assertTrue(report.ok, report.render())

    def test_user_invocable_rejects_non_boolean_values(self) -> None:
        for value in ('"false"', "'true'", "yes", "tRuE", "fAlSe", "0", "null", "", "[]", "{}", ">\n  false"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                repo = Path(directory)
                skill = repo / "marketing" / "example"
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(
                    "---\nname: example\ndescription: Example skill.\n"
                    f"user-invocable: {value}\n---\n", encoding="utf-8"
                )
                report = validate_repository(repo, quick=True)
                self.assertFalse(report.ok)
                self.assertTrue(any(
                    "user-invocable must be a boolean" in issue.message
                    for issue in report.issues
                ), report.render())

    def test_current_repository_passes_quick_validation(self) -> None:
        report = validate_repository(REPO_ROOT, quick=True)

        self.assertTrue(report.ok, report.render())
        self.assertEqual(report.skill_count, 40)
        self.assertEqual(report.python_count, 43)
        self.assertEqual(report.shell_count, 6)


if __name__ == "__main__":
    unittest.main()
