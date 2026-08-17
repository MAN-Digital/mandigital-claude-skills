from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

from scripts.maintenance.publish import build_branch_name, publish_changes
from tests.maintenance.helpers import RecordingRunner, create_dirty_git_repo


class PublishTests(unittest.TestCase):
    def test_publisher_opens_draft_pr_and_never_merges(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = create_dirty_git_repo(Path(directory))
            runner = RecordingRunner(
                pr_url="https://github.com/MAN-Digital/mandigital-claude-skills/pull/99"
            )

            with redirect_stdout(io.StringIO()):
                url = publish_changes(
                    repo,
                    "studio-mac",
                    assume_yes=True,
                    runner=runner,
                )

            flattened = [argument for call in runner.calls for argument in call]
            self.assertIn("--draft", flattened)
            self.assertNotIn("merge", flattened)
            self.assertEqual(
                url,
                "https://github.com/MAN-Digital/mandigital-claude-skills/pull/99",
            )

    def test_branch_name_is_machine_scoped(self) -> None:
        value = build_branch_name(
            "Studio Mac",
            datetime(2026, 8, 17, 12, 30, tzinfo=timezone.utc),
        )

        self.assertEqual(value, "machine/studio-mac/20260817-123000")


if __name__ == "__main__":
    unittest.main()
