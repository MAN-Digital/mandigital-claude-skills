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
            "metadata questions",
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

    def test_reader_facing_source_notice_is_rejected(self) -> None:
        self.assert_rejected(
            "must not include reader-facing draft notices",
            (
                "interview-body.html",
                "<p>MAN Digital invited",
                '<p class="rli-source-notice">Generated from automatic captions.</p>\n\n  <p>MAN Digital invited',
            ),
        )

    def test_fewer_than_seven_questions_is_rejected(self) -> None:
        self.assert_rejected(
            "require 7-8 complete questions; got 6",
            (
                "interview-body.html",
                '<h2 class="rli-question" id="retention-focus">Why has retention become a bigger part of the RevOps agenda?</h2>',
                '<h3 id="removed-question">Why retention matters</h3>',
            ),
            (
                "interview-body.html",
                '<h2 class="rli-question" id="tool-roi">How should RevOps decide which tools deserve a place in the stack?</h2>',
                '<h3 id="removed-question-two">How tools earn a place</h3>',
            ),
        )

    def test_more_than_eight_questions_is_rejected(self) -> None:
        self.assert_rejected(
            "require 7-8 complete questions; got 9",
            (
                "interview-body.html",
                '<div class="rli-article" data-rli-editorial-state="draft-source-derived">',
                '<div class="rli-article" data-rli-editorial-state="draft-source-derived"><h2 class="rli-question" id="extra-question">Extra supported question</h2>',
            ),
        )

    def test_missing_evidence_coverage_is_rejected(self) -> None:
        self.assert_rejected(
            "missing questions are not allowed",
            ("evidence-map.json", '"coverage": "direct"', '"coverage": "missing"'),
        )

    def test_placeholder_is_rejected_in_any_state(self) -> None:
        self.assert_rejected(
            "must not include draft placeholders",
            (
                "interview-body.html",
                '<div class="rli-answer">',
                '<div class="rli-answer"><div class="rli-draft-placeholder">Unsupported</div>',
            ),
        )

    def test_question_selection_must_be_source_adapted(self) -> None:
        self.assert_rejected(
            "questionSelectionMethod must be source-adapted",
            (
                "metadata.example.json",
                '"questionSelectionMethod": "source-adapted"',
                '"questionSelectionMethod": "fixed-template"',
            ),
        )

    def test_video_wrapper_cannot_add_black_background(self) -> None:
        self.assert_rejected(
            "must not add a black background",
            ("interview-post.css", "background: transparent;", "background: #0a0a0a;"),
        )

    def test_video_and_lead_image_cannot_be_rendered_together(self) -> None:
        self.assert_rejected(
            "must not render a separate lead image",
            (
                "interview-body.html",
                '<div class="rli-video">',
                '<figure class="rli-article__lead"><img src="https://example.com/duplicate.jpg" alt="Duplicate"></figure>\n\n  <div class="rli-video">',
            ),
        )

    def test_youtube_open_graph_provenance_is_enforced(self) -> None:
        self.assert_rejected(
            "openGraphImageSource must be youtube-thumbnail",
            (
                "metadata.example.json",
                '"openGraphImageSource": "youtube-thumbnail"',
                '"openGraphImageSource": "user-provided-image"',
            ),
        )

    def test_hubspot_preview_wrapper_must_expand(self) -> None:
        self.assert_rejected(
            "must expand HubSpot's iframe preview wrapper",
            ("interview-post.css", ".mce-preview-object", ".removed-preview-object"),
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
