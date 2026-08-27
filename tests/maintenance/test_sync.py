from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.maintenance.sync import SyncError, sync_checkout
from tests.maintenance.helpers import GitFixture


class SyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = GitFixture(Path(self.temporary.name))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_clean_checkout_fast_forwards_after_candidate_validation(self) -> None:
        old = self.fixture.managed_head
        new = self.fixture.push_valid_change()

        result = sync_checkout(self.fixture.managed, self.fixture.state, [])

        self.assertTrue(result.changed)
        self.assertEqual(result.commit, new)
        self.assertNotEqual(self.fixture.head(self.fixture.managed), old)

    def test_dirty_checkout_is_preserved(self) -> None:
        marker = self.fixture.managed / "local-note.txt"
        marker.write_text("unfinished", encoding="utf-8")
        before = self.fixture.head(self.fixture.managed)

        with self.assertRaisesRegex(SyncError, "dirty"):
            sync_checkout(self.fixture.managed, self.fixture.state, [])

        self.assertEqual(marker.read_text(encoding="utf-8"), "unfinished")
        self.assertEqual(self.fixture.head(self.fixture.managed), before)

    def test_non_main_branch_is_preserved(self) -> None:
        from tests.maintenance.helpers import git

        git(["switch", "-c", "machine/test/change"], self.fixture.managed)
        before = self.fixture.head(self.fixture.managed)

        with self.assertRaisesRegex(SyncError, "main"):
            sync_checkout(self.fixture.managed, self.fixture.state, [])

        self.assertEqual(self.fixture.head(self.fixture.managed), before)

    def test_invalid_remote_commit_does_not_advance(self) -> None:
        self.fixture.push_invalid_skill()
        before = self.fixture.head(self.fixture.managed)

        with self.assertRaisesRegex(SyncError, "validation"):
            sync_checkout(self.fixture.managed, self.fixture.state, [])

        self.assertEqual(self.fixture.head(self.fixture.managed), before)

    def test_existing_lock_prevents_overlap(self) -> None:
        lock = self.fixture.state / "sync.lock"
        lock.mkdir(parents=True)

        with self.assertRaisesRegex(SyncError, "already running"):
            sync_checkout(self.fixture.managed, self.fixture.state, [])
