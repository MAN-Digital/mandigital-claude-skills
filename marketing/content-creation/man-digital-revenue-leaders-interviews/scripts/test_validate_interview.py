#!/usr/bin/env python3
"""Regression tests for the Revenue Leaders Interview validator."""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = SKILL_DIR / "assets" / "carol-chen"
SPEC = importlib.util.spec_from_file_location(
    "validate_interview", SKILL_DIR / "scripts" / "validate_interview.py"
)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


class ValidatorTests(unittest.TestCase):
    def validate_with(self, *edits: tuple[str, str, str]) -> list[str]:
        with tempfile.TemporaryDirectory(prefix="rli-validator-test-") as temp_dir:
            asset_dir = Path(temp_dir) / "interview"
            shutil.copytree(EXAMPLE_DIR, asset_dir)
            for filename, old, new in edits:
                path = asset_dir / filename
                content = path.read_text(encoding="utf-8")
                self.assertIn(old, content, f"mutation target missing in {filename}")
                path.write_text(content.replace(old, new, 1), encoding="utf-8")
            return VALIDATOR.validate(asset_dir)

    def assert_rejected(self, message: str, *edits: tuple[str, str, str]) -> None:
        errors = self.validate_with(*edits)
        self.assertTrue(errors)
        self.assertTrue(any(message in error for error in errors), errors)

    def test_reference_example_passes(self) -> None:
        self.assertEqual(VALIDATOR.validate(EXAMPLE_DIR), [])

    def test_source_derived_youtube_bundle_passes(self) -> None:
        metadata = json.loads(
            (EXAMPLE_DIR / "metadata.example.json").read_text(encoding="utf-8")
        )
        source = json.loads((EXAMPLE_DIR / "source.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["editorialState"], "draft-source-derived")
        self.assertEqual(source["transcriptProvider"], "youtube-transcript-api")
        self.assertTrue(source["transcriptIsGenerated"])
        self.assertEqual(VALIDATOR.validate(EXAMPLE_DIR), [])

    def test_changed_question_wording_is_rejected(self) -> None:
        self.assert_rejected(
            "question wording/order",
            (
                "interview-body.html",
                "How do you define revenue operations to someone who has not had it before?",
                "What is RevOps?",
            ),
        )

    def test_mixed_root_states_are_rejected(self) -> None:
        self.assert_rejected(
            "rli-article must declare exactly",
            (
                "interview-body.html",
                'data-rli-editorial-state="draft-source-derived"',
                'data-rli-editorial-state="approved"',
            ),
        )

    def test_approved_state_with_illustrative_answers_is_rejected(self) -> None:
        self.assert_rejected(
            "data-answer-state=approved",
            (
                "interview-intro.html",
                'data-rli-editorial-state="draft-source-derived"',
                'data-rli-editorial-state="approved"',
            ),
            (
                "interview-body.html",
                'data-rli-editorial-state="draft-source-derived"',
                'data-rli-editorial-state="approved"',
            ),
            (
                "metadata.example.json",
                '"editorialState": "draft-source-derived"',
                '"editorialState": "approved"',
            ),
        )

    def test_missing_source_notice_is_rejected(self) -> None:
        self.assert_rejected(
            "exactly one visible rli-source-notice",
            ("interview-body.html", 'class="rli-source-notice"', 'class="removed-notice"'),
        )

    def test_wrong_campaign_id_is_rejected(self) -> None:
        self.assert_rejected(
            "canonical Revenue Leaders Interviews campaign",
            (
                "metadata.example.json",
                "38b1a8b6-07c6-48e4-84de-16de94802392",
                "00000000-0000-0000-0000-000000000000",
            ),
        )

    def test_non_youtube_source_cannot_enable_video_embed(self) -> None:
        self.assert_rejected(
            "only YouTube sources may enable embedVideo",
            (
                "metadata.example.json",
                '"sourceType": "youtube"',
                '"sourceType": "markdown"',
            ),
        )

    def test_sample_source_cannot_claim_reviewed_state(self) -> None:
        self.assert_rejected(
            "sample sourceType is only valid",
            (
                "metadata.example.json",
                '"editorialState": "draft-source-derived"',
                '"editorialState": "draft-transcript-reviewed"',
            ),
            (
                "metadata.example.json",
                '"sourceType": "youtube"',
                '"sourceType": "sample"',
            ),
        )

    def test_linkedin_link_without_svg_is_rejected(self) -> None:
        self.assert_rejected(
            "inline SVG icon",
            ("interview-intro.html", "<svg xmlns=", "<span data-removed-svg="),
        )

    def test_malformed_metadata_is_reported_cleanly(self) -> None:
        self.assert_rejected(
            "invalid metadata.example.json",
            ("metadata.example.json", "{", "not-json",),
        )


if __name__ == "__main__":
    unittest.main()
