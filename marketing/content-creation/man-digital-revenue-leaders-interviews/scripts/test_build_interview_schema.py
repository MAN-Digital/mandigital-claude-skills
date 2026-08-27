#!/usr/bin/env python3
"""Regression tests for managed Revenue Leaders Interview JSON-LD."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = SKILL_DIR / "assets" / "carol-chen"
SPEC = importlib.util.spec_from_file_location(
    "build_interview_schema", SKILL_DIR / "scripts" / "build_interview_schema.py"
)
SCHEMA = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(SCHEMA)


class InterviewSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.metadata = json.loads(
            (EXAMPLE_DIR / "metadata.example.json").read_text(encoding="utf-8")
        )
        self.source = json.loads(
            (EXAMPLE_DIR / "source.json").read_text(encoding="utf-8")
        )
        self.page_url = "https://www.man.digital/blog/carol-chen-schema-test"

    def graph(self) -> dict:
        return SCHEMA.build_interview_graph(
            self.metadata,
            self.source,
            page_url=self.page_url,
        )

    def test_youtube_interview_graph_has_required_connected_nodes(self) -> None:
        graph = self.graph()
        self.assertEqual(graph["@context"], "https://schema.org")
        nodes = graph["@graph"]
        types = [node["@type"] for node in nodes]
        self.assertEqual(types.count("Person"), 2)
        for required in ("ImageObject", "VideoObject", "WebPage", "BreadcrumbList", "Article"):
            self.assertIn(required, types)
        self.assertNotIn("FAQPage", types)
        ids = [node["@id"] for node in nodes]
        self.assertEqual(len(ids), len(set(ids)))

    def test_guest_and_video_match_verified_source(self) -> None:
        nodes = self.graph()["@graph"]
        guest = next(node for node in nodes if node.get("@id", "").endswith("#guest"))
        video = next(node for node in nodes if node["@type"] == "VideoObject")
        article = next(node for node in nodes if node["@type"] == "Article")
        self.assertEqual(guest["name"], "Carol Chen")
        self.assertEqual(
            guest["sameAs"],
            [self.metadata["linkedinVerification"]["profileUrl"]],
        )
        self.assertEqual(video["embedUrl"], self.source["youtube"]["embedUrl"])
        self.assertEqual(video["uploadDate"], "2024-06-26")
        self.assertEqual(article["articleSection"], "Revenue Leaders Interviews")
        self.assertEqual(article["contributor"], {"@id": f"{self.page_url}#guest"})

    def test_non_video_interview_omits_video_object(self) -> None:
        metadata = dict(self.metadata)
        metadata["embedVideo"] = False
        graph = SCHEMA.build_interview_graph(metadata, {}, page_url=self.page_url)
        self.assertNotIn("VideoObject", [node["@type"] for node in graph["@graph"]])

    def test_wrapper_escapes_script_terminators(self) -> None:
        graph = self.graph()
        graph["@graph"][-1]["name"] = "Unsafe </script> text"
        block = SCHEMA.wrap_schema_graph(graph)
        self.assertEqual(block.count("</script>"), 1)
        self.assertIn("<\\/script>", block)

    def test_managed_region_appends_then_replaces_without_touching_other_html(self) -> None:
        first = SCHEMA.wrap_schema_graph(self.graph())
        merged = SCHEMA.inject_managed_schema('<meta name="x" content="y">', first)
        self.assertIn('<meta name="x" content="y">', merged)
        self.assertEqual(merged.count(SCHEMA.MARKER_START), 1)
        replacement = first.replace("Carol Chen", "Carol Chen Updated", 1)
        replaced = SCHEMA.inject_managed_schema(merged, replacement)
        self.assertIn('<meta name="x" content="y">', replaced)
        self.assertIn("Carol Chen Updated", replaced)
        self.assertEqual(replaced.count(SCHEMA.MARKER_START), 1)

    def test_corrupt_or_duplicate_markers_are_rejected(self) -> None:
        block = SCHEMA.wrap_schema_graph(self.graph())
        with self.assertRaises(ValueError):
            SCHEMA.inject_managed_schema(f"{block}\n{block}", block)
        with self.assertRaises(ValueError):
            SCHEMA.inject_managed_schema(SCHEMA.MARKER_START, block)

    def test_legacy_openclaw_marker_pair_is_migrated_in_place(self) -> None:
        block = SCHEMA.wrap_schema_graph(self.graph())
        legacy = block.replace(SCHEMA.MARKER_START, SCHEMA.LEGACY_MARKER_START).replace(
            SCHEMA.MARKER_END, SCHEMA.LEGACY_MARKER_END
        )
        merged = SCHEMA.inject_managed_schema(f"<meta name=\"x\">\n{legacy}", block)
        self.assertIn("<meta name=\"x\">", merged)
        self.assertNotIn(SCHEMA.LEGACY_MARKER_START, merged)
        self.assertEqual(merged.count(SCHEMA.MARKER_START), 1)


if __name__ == "__main__":
    unittest.main()
