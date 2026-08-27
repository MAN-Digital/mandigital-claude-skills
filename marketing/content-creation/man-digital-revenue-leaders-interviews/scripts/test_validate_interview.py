#!/usr/bin/env python3
"""Regression tests for the Revenue Leaders Interview validator."""

from __future__ import annotations

import importlib.util
import hashlib
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
        with tempfile.TemporaryDirectory(prefix="rli-youtube-validator-test-") as temp_dir:
            asset_dir = Path(temp_dir) / "interview"
            shutil.copytree(EXAMPLE_DIR, asset_dir)
            metadata_path = asset_dir / "metadata.example.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata.update(
                {
                    "editorialState": "draft-source-derived",
                    "sourceType": "youtube",
                    "embedVideo": True,
                }
            )
            metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

            intro_path = asset_dir / "interview-intro.html"
            intro_path.write_text(
                intro_path.read_text(encoding="utf-8").replace(
                    'data-rli-editorial-state="draft-sample-answers"',
                    'data-rli-editorial-state="draft-source-derived"',
                ),
                encoding="utf-8",
            )
            body_path = asset_dir / "interview-body.html"
            body = body_path.read_text(encoding="utf-8")
            body = body.replace(
                'data-rli-editorial-state="draft-sample-answers"',
                'data-rli-editorial-state="draft-source-derived"',
            ).replace(
                'class="rli-sample-notice"', 'class="rli-source-notice"'
            ).replace(
                'data-answer-state="illustrative"',
                'data-answer-state="source-derived"',
            ).replace(
                'data-editorial-state="illustrative"',
                'data-editorial-state="source-derived"',
            )
            body = body.replace(
                "</figure>",
                """</figure>
  <div class="rli-video"><iframe src="https://www.youtube-nocookie.com/embed/example123" title="Interview with Carol Chen"></iframe></div>""",
                1,
            )
            body_path.write_text(body, encoding="utf-8")

            content = "[00:00:01.000] Source evidence.\n"
            (asset_dir / "source-content.md").write_text(content, encoding="utf-8")
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            source = {
                "sourceType": "youtube",
                "embedVideo": True,
                "missingPromptInputs": [],
                "contentFile": "source-content.md",
                "contentSha256": content_hash,
                "youtube": {
                    "embedUrl": "https://www.youtube-nocookie.com/embed/example123"
                },
            }
            (asset_dir / "source.json").write_text(
                json.dumps(source, indent=2) + "\n", encoding="utf-8"
            )
            evidence = {
                "sourceSha256": content_hash,
                "questions": [
                    {
                        "question": question,
                        "sourceRefs": ["00:00:01"],
                        "evidence": ["Source evidence."],
                        "coverage": "direct",
                    }
                    for question in metadata["approvedQuestions"]
                ],
            }
            (asset_dir / "evidence-map.json").write_text(
                json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
            )
            self.assertEqual(VALIDATOR.validate(asset_dir), [])

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
                'data-rli-editorial-state="draft-sample-answers"',
                'data-rli-editorial-state="approved"',
            ),
        )

    def test_approved_state_with_illustrative_answers_is_rejected(self) -> None:
        self.assert_rejected(
            "data-answer-state=approved",
            (
                "interview-intro.html",
                'data-rli-editorial-state="draft-sample-answers"',
                'data-rli-editorial-state="approved"',
            ),
            (
                "interview-body.html",
                'data-rli-editorial-state="draft-sample-answers"',
                'data-rli-editorial-state="approved"',
            ),
            (
                "metadata.example.json",
                '"editorialState": "draft-sample-answers"',
                '"editorialState": "approved"',
            ),
        )

    def test_missing_sample_notice_is_rejected(self) -> None:
        self.assert_rejected(
            "exactly one visible rli-sample-notice",
            ("interview-body.html", 'class="rli-sample-notice"', 'class="removed-notice"'),
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
                '"embedVideo": false',
                '"embedVideo": true',
            ),
        )

    def test_sample_source_cannot_claim_reviewed_state(self) -> None:
        self.assert_rejected(
            "sample sourceType is only valid",
            (
                "metadata.example.json",
                '"editorialState": "draft-sample-answers"',
                '"editorialState": "draft-transcript-reviewed"',
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
