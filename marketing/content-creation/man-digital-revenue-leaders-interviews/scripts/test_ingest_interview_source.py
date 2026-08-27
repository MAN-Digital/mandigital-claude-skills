#!/usr/bin/env python3
"""Regression tests for Revenue Leaders Interview source ingestion."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).with_name("ingest_interview_source.py")
SPEC = importlib.util.spec_from_file_location("ingest_interview_source", SCRIPT_PATH)
INGEST = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(INGEST)


class SourceIngestionTests(unittest.TestCase):
    def test_vtt_parser_removes_rolling_caption_overlap(self) -> None:
        with tempfile.TemporaryDirectory(prefix="rli-vtt-test-") as temp_dir:
            path = Path(temp_dir) / "video.en.vtt"
            path.write_text(
                """WEBVTT

00:00:01.000 --> 00:00:03.000
Revenue operations starts with shared definitions.

00:00:03.000 --> 00:00:05.000
shared definitions. Then the forecast becomes inspectable.

00:00:05.000 --> 00:00:07.000
shared definitions. Then the forecast becomes inspectable.
""",
                encoding="utf-8",
            )
            transcript = INGEST.parse_vtt(path)
        self.assertIn("[00:00:01.000] Revenue operations starts", transcript)
        self.assertIn("[00:00:03.000] Then the forecast becomes inspectable.", transcript)
        self.assertEqual(transcript.count("forecast becomes inspectable"), 1)

    def test_markdown_ingestion_records_missing_prompt_inputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="rli-markdown-test-") as temp_dir:
            root = Path(temp_dir)
            source = root / "interview.md"
            source.write_text("# Interview with Ada\n\nA complete transcript.\n", encoding="utf-8")
            output = root / "bundle"
            manifest = INGEST.ingest_markdown(
                source,
                output,
                source_type="markdown",
                content_kind="transcript",
                source_url=None,
                guest_image=None,
                linkedin_url=None,
                og_image=None,
            )
            saved = json.loads((output / "source.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["sourceTitle"], "Interview with Ada")
        self.assertEqual(saved["sourceType"], "markdown")
        self.assertEqual(
            saved["missingPromptInputs"],
            ["guestImage", "linkedinProfile", "openGraphImage"],
        )
        self.assertEqual(len(saved["contentSha256"]), 64)

    def test_granola_notes_are_not_mislabeled_as_transcript(self) -> None:
        with tempfile.TemporaryDirectory(prefix="rli-granola-test-") as temp_dir:
            root = Path(temp_dir)
            source = root / "granola.md"
            source.write_text("# Call notes\n\nForecast discussion.\n", encoding="utf-8")
            output = root / "bundle"
            manifest = INGEST.ingest_markdown(
                source,
                output,
                source_type="granola",
                content_kind="notes",
                source_url="https://notes.granola.ai/example",
                guest_image="https://example.com/guest.jpg",
                linkedin_url="https://www.linkedin.com/in/example/",
                og_image="https://example.com/og.jpg",
            )
        self.assertEqual(manifest["contentKind"], "granola-notes")
        self.assertFalse(manifest["embedVideo"])
        self.assertEqual(manifest["missingPromptInputs"], [])

    def test_youtube_url_detection_is_host_scoped(self) -> None:
        self.assertTrue(INGEST.is_youtube_url("https://youtu.be/abc123"))
        self.assertTrue(
            INGEST.is_youtube_url("https://www.youtube.com/watch?v=abc123")
        )
        self.assertFalse(INGEST.is_youtube_url("https://example.com/youtube.com/abc"))

    def test_transcript_api_json_becomes_timestamped_markdown(self) -> None:
        content, count = INGEST.parse_transcript_api_json(
            json.dumps([[{"text": " Hello &amp; welcome ", "start": 61.25, "duration": 2}]])
        )
        self.assertEqual(content, "[00:01:01.250] Hello & welcome\n")
        self.assertEqual(count, 1)

    @mock.patch.object(INGEST, "run_transcript_api")
    @mock.patch.object(INGEST, "fetch_youtube_metadata")
    def test_youtube_prefers_transcript_api(self, metadata_mock, transcript_mock) -> None:
        metadata_mock.return_value = {
            "id": "abc123",
            "title": "Interview",
            "webpage_url": "https://www.youtube.com/watch?v=abc123",
            "automatic_captions": {"en": [{}]},
            "thumbnail": "https://i.ytimg.com/vi/abc123/maxresdefault.jpg",
        }
        transcript_mock.return_value = ("[00:00:00.000] Hello\n", "en", 1)
        with tempfile.TemporaryDirectory(prefix="rli-youtube-test-") as temp_dir:
            manifest = INGEST.ingest_youtube(
                "https://www.youtube.com/watch?v=abc123",
                Path(temp_dir),
                language="en.*",
                embed_video=True,
                guest_image=None,
                linkedin_url=None,
                og_image=None,
            )
        self.assertEqual(manifest["transcriptProvider"], "youtube-transcript-api")
        self.assertTrue(manifest["transcriptIsGenerated"])
        self.assertEqual(manifest["transcriptSegmentCount"], 1)
        self.assertEqual(manifest["openGraphCandidate"]["imageSource"], "youtube-thumbnail")
        self.assertNotIn("openGraphImage", manifest["missingPromptInputs"])

    @mock.patch.object(INGEST, "run_yt_dlp_captions")
    @mock.patch.object(INGEST, "run_transcript_api", side_effect=ValueError("blocked"))
    @mock.patch.object(INGEST, "fetch_youtube_metadata")
    def test_youtube_falls_back_to_yt_dlp_captions(
        self, metadata_mock, _transcript_mock, captions_mock
    ) -> None:
        metadata_mock.return_value = {
            "id": "abc123",
            "title": "Interview",
            "subtitles": {"en": [{}]},
            "thumbnail": "https://i.ytimg.com/vi/abc123/maxresdefault.jpg",
        }
        captions_mock.return_value = ("[00:00:00.000] Hello\n", "en", 1)
        with tempfile.TemporaryDirectory(prefix="rli-youtube-test-") as temp_dir:
            manifest = INGEST.ingest_youtube(
                "https://youtu.be/abc123",
                Path(temp_dir),
                language="en",
                embed_video=False,
                guest_image=None,
                linkedin_url=None,
                og_image=None,
            )
        self.assertEqual(manifest["transcriptProvider"], "yt-dlp")
        self.assertFalse(manifest["transcriptIsGenerated"])
        self.assertEqual(manifest["transcriptFallbacksAttempted"][0]["provider"], "youtube-transcript-api")

    @mock.patch.object(INGEST, "run_local_whisper")
    @mock.patch.object(INGEST, "run_yt_dlp_captions", side_effect=ValueError("none"))
    @mock.patch.object(INGEST, "run_transcript_api", side_effect=ValueError("none"))
    @mock.patch.object(INGEST, "fetch_youtube_metadata")
    def test_whisper_is_only_used_when_explicitly_enabled(
        self, metadata_mock, _transcript_mock, _captions_mock, whisper_mock
    ) -> None:
        metadata_mock.return_value = {
            "id": "abc123",
            "title": "Interview",
            "thumbnail": "https://i.ytimg.com/vi/abc123/maxresdefault.jpg",
        }
        with tempfile.TemporaryDirectory(prefix="rli-youtube-test-") as temp_dir:
            with self.assertRaisesRegex(ValueError, "--whisper-fallback"):
                INGEST.ingest_youtube(
                    "https://youtu.be/abc123",
                    Path(temp_dir),
                    language="en",
                    embed_video=False,
                    guest_image=None,
                    linkedin_url=None,
                    og_image=None,
                )
            whisper_mock.assert_not_called()
            whisper_mock.return_value = ("[00:00:00.000] Hello\n", "en", 1)
            manifest = INGEST.ingest_youtube(
                "https://youtu.be/abc123",
                Path(temp_dir),
                language="en",
                embed_video=False,
                guest_image=None,
                linkedin_url=None,
                og_image=None,
                whisper_fallback=True,
            )
        self.assertEqual(manifest["transcriptProvider"], "faster-whisper")
        self.assertTrue(manifest["transcriptIsGenerated"])


if __name__ == "__main__":
    unittest.main()
