from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.maintenance.status import collect_status
from tests.maintenance.helpers import GitFixture


class StatusTests(unittest.TestCase):
    def test_status_reports_branch_commit_and_dirty_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))

            clean = collect_status(fixture.managed, fixture.state, [])
            (fixture.managed / "local-note.txt").write_text("unfinished", encoding="utf-8")
            dirty = collect_status(fixture.managed, fixture.state, [])

            self.assertEqual(clean["branch"], "main")
            self.assertEqual(clean["commit"], fixture.managed_head)
            self.assertFalse(clean["dirty"])
            self.assertTrue(dirty["dirty"])


if __name__ == "__main__":
    unittest.main()
