from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class RepositoryWiringTests(unittest.TestCase):
    def test_hooks_delegate_to_versioned_doctor(self) -> None:
        pre_commit = (REPO_ROOT / ".githooks/pre-commit").read_text(encoding="utf-8")
        pre_push = (REPO_ROOT / ".githooks/pre-push").read_text(encoding="utf-8")

        self.assertIn("scripts/skills-doctor --repo . --quick", pre_commit)
        self.assertIn("scripts/skills-doctor --repo .", pre_push)

    def test_workflow_has_pr_push_and_monday_schedule(self) -> None:
        workflow = (REPO_ROOT / ".github/workflows/validate-skills.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("pull_request:", workflow)
        self.assertIn("push:", workflow)
        self.assertIn("cron: '0 7 * * 1'", workflow)
        self.assertIn("macos-latest", workflow)
        self.assertIn("python3 -m unittest discover -s tests/maintenance -v", workflow)

    def test_readme_links_to_maintenance_guide(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("[Multi-machine maintenance](./MAINTENANCE.md)", readme)


if __name__ == "__main__":
    unittest.main()
