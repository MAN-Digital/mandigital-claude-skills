#!/usr/bin/env python3
"""Validate a Revenue Leaders Interview asset directory without network access."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_SERIES = "Revenue Leaders Interviews"


class InterviewParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.classes: list[set[str]] = []
        self.ids: list[str] = []
        self.editorial_states: list[str] = []
        self.root_states: dict[str, list[str]] = {"rli-intro": [], "rli-article": []}
        self.qa_answer_states: list[str] = []
        self.question_ids: list[str] = []
        self.question_texts: list[str] = []
        self.pull_quote_states: list[str] = []
        self.draft_placeholder_count = 0
        self.linkedin_links: list[dict[str, str | None]] = []
        self.linkedin_svg_count = 0
        self.image_sources: list[str] = []
        self._in_question = False
        self._question_parts: list[str] = []
        self._in_linkedin = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        classes = set((values.get("class") or "").split())
        self.classes.append(classes)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if values.get("data-rli-editorial-state"):
            state = values["data-rli-editorial-state"] or ""
            self.editorial_states.append(state)
            for root_class in self.root_states:
                if root_class in classes:
                    self.root_states[root_class].append(state)
        if "rli-qa" in classes:
            self.qa_answer_states.append(values.get("data-answer-state") or "")
        if tag == "h2" and "rli-question" in classes:
            self._in_question = True
            self._question_parts = []
            self.question_ids.append(values.get("id") or "")
        if "rli-pull-quote" in classes:
            self.pull_quote_states.append(values.get("data-editorial-state") or "")
        if "rli-draft-placeholder" in classes:
            self.draft_placeholder_count += 1
        if tag == "a" and "rli-linkedin" in classes:
            self.linkedin_links.append(values)
            self._in_linkedin = True
        if tag == "svg" and self._in_linkedin:
            self.linkedin_svg_count += 1
        if tag == "img" and values.get("src"):
            self.image_sources.append(values["src"] or "")

    def handle_data(self, data: str) -> None:
        if self._in_question:
            self._question_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2" and self._in_question:
            self.question_texts.append(" ".join("".join(self._question_parts).split()))
            self._in_question = False
            self._question_parts = []
        if tag == "a" and self._in_linkedin:
            self._in_linkedin = False


def validate(asset_dir: Path) -> list[str]:
    errors: list[str] = []
    required = {
        "interview-body.html",
        "interview-intro.html",
        "interview-post.css",
        "metadata.example.json",
        "linkedin-icon.svg",
    }
    missing = sorted(name for name in required if not (asset_dir / name).is_file())
    if missing:
        return [f"missing files: {', '.join(missing)}"]

    parser = InterviewParser()
    parser.feed((asset_dir / "interview-intro.html").read_text(encoding="utf-8"))
    parser.feed((asset_dir / "interview-body.html").read_text(encoding="utf-8"))

    try:
        metadata = json.loads((asset_dir / "metadata.example.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid metadata.example.json: {exc}"]

    required_metadata = {
        "editorialState", "seoTitle", "metaDescription", "openGraphTitle",
        "openGraphDescription", "openGraphImage", "tag", "campaign", "campaignId",
        "approvedQuestionSource", "approvedQuestions", "draft",
    }
    absent = sorted(required_metadata - metadata.keys())
    if absent:
        errors.append(f"missing metadata keys: {', '.join(absent)}")

    qa_count = sum("rli-qa" in item for item in parser.classes)
    question_count = len(parser.question_texts)
    answer_count = sum("rli-answer" in item for item in parser.classes)
    notice_count = sum("rli-sample-notice" in item for item in parser.classes)
    approval_notice_count = sum("rli-approval-notice" in item for item in parser.classes)
    if question_count == 0 or len({qa_count, question_count, answer_count}) != 1:
        errors.append(f"Q/A structure mismatch: sections/questions/answers={qa_count}/{question_count}/{answer_count}")
    if len(parser.question_ids) != question_count or any(not value for value in parser.question_ids):
        errors.append("every question requires a stable non-empty ID")
    if len(parser.ids) != len(set(parser.ids)):
        errors.append("HTML IDs must be unique across intro and body")

    approved_questions = metadata.get("approvedQuestions")
    if not isinstance(approved_questions, list) or not approved_questions or not all(
        isinstance(item, str) and item.strip() for item in approved_questions
    ):
        errors.append("approvedQuestions must be a non-empty list of exact question strings")
    elif parser.question_texts != approved_questions:
        errors.append("rendered question wording/order must exactly match approvedQuestions")
    question_source = metadata.get("approvedQuestionSource", "")
    parsed_source = urlparse(question_source) if isinstance(question_source, str) else urlparse("")
    if parsed_source.scheme != "https" or parsed_source.netloc != "www.figma.com" or "node-id=" not in parsed_source.query:
        errors.append("approvedQuestionSource must be an HTTPS Figma node URL")

    editorial_state = metadata.get("editorialState")
    allowed_states = {"draft-sample-answers", "draft-transcript-reviewed", "approved"}
    if editorial_state not in allowed_states:
        errors.append(f"editorialState must be one of {sorted(allowed_states)}")
    for root_class, states in parser.root_states.items():
        if states != [editorial_state]:
            errors.append(f"{root_class} must declare exactly the metadata editorialState")

    expected_answer_state = {
        "draft-sample-answers": "illustrative",
        "draft-transcript-reviewed": "transcript-reviewed",
        "approved": "approved",
    }.get(editorial_state)
    if expected_answer_state and (
        len(parser.qa_answer_states) != qa_count
        or set(parser.qa_answer_states) != {expected_answer_state}
    ):
        errors.append(f"every Q/A section must use data-answer-state={expected_answer_state}")

    if editorial_state == "draft-sample-answers":
        if notice_count != 1:
            errors.append("sample drafts require exactly one visible rli-sample-notice")
        if approval_notice_count:
            errors.append("sample drafts must not include rli-approval-notice")
    elif editorial_state == "draft-transcript-reviewed":
        if notice_count:
            errors.append("transcript-reviewed drafts must not include rli-sample-notice")
        if approval_notice_count != 1:
            errors.append("transcript-reviewed drafts require exactly one visible rli-approval-notice")
    elif editorial_state == "approved":
        if notice_count or approval_notice_count:
            errors.append("approved content must not include draft notices")
        if parser.draft_placeholder_count:
            errors.append("approved content must not include draft placeholders")

    expected_quote_state = {
        "draft-sample-answers": "illustrative",
        "draft-transcript-reviewed": "transcript-reviewed",
        "approved": "approved",
    }.get(editorial_state)
    if not parser.pull_quote_states:
        errors.append("at least one rli-pull-quote is required")
    elif expected_quote_state and set(parser.pull_quote_states) != {expected_quote_state}:
        errors.append(f"every pull quote must use data-editorial-state={expected_quote_state}")

    if not parser.linkedin_links:
        errors.append("at least one rli-linkedin link is required")
    if parser.linkedin_svg_count != len(parser.linkedin_links):
        errors.append("every rli-linkedin link must contain an inline SVG icon")
    for link in parser.linkedin_links:
        rel = set((link.get("rel") or "").split())
        href = link.get("href") or ""
        if urlparse(href).scheme != "https" or "linkedin.com/" not in href:
            errors.append(f"invalid LinkedIn URL: {href!r}")
        if link.get("target") != "_blank" or not {"noopener", "noreferrer"}.issubset(rel):
            errors.append("LinkedIn links must use target=_blank and rel=noopener noreferrer")
        if not link.get("aria-label"):
            errors.append("LinkedIn links require an aria-label")

    for source in parser.image_sources:
        if source.startswith(("data:", "file:")) or "figma.com" in source:
            errors.append(f"non-publishable image source: {source}")
        if urlparse(source).scheme != "https":
            errors.append(f"image source must be HTTPS: {source}")

    if metadata.get("tag") != REQUIRED_SERIES or metadata.get("campaign") != REQUIRED_SERIES:
        errors.append(f"tag and campaign must both be {REQUIRED_SERIES!r}")
    if metadata.get("campaignId") != "38b1a8b6-07c6-48e4-84de-16de94802392":
        errors.append("campaignId must reference the canonical Revenue Leaders Interviews campaign")
    if metadata.get("draft") is not True:
        errors.append("the bundled example must remain a draft")
    seo_title = metadata.get("seoTitle", "")
    description = metadata.get("metaDescription", "")
    if not 30 <= len(seo_title) <= 60:
        errors.append(f"SEO title must be 30-60 characters; got {len(seo_title)}")
    if not 120 <= len(description) <= 160:
        errors.append(f"meta description must be 120-160 characters; got {len(description)}")
    if metadata.get("openGraphTitle") != seo_title:
        errors.append("Open Graph title must match SEO title in the series template")
    if metadata.get("openGraphDescription") != description:
        errors.append("Open Graph description must match meta description in the series template")
    if urlparse(metadata.get("openGraphImage", "")).scheme != "https":
        errors.append("Open Graph image must use HTTPS")

    try:
        svg_root = ET.fromstring((asset_dir / "linkedin-icon.svg").read_text(encoding="utf-8"))
        if not svg_root.tag.endswith("svg") or not any(element.tag.endswith("path") for element in svg_root.iter()):
            errors.append("linkedin-icon.svg must contain an SVG path")
    except (OSError, ET.ParseError) as exc:
        errors.append(f"invalid linkedin-icon.svg: {exc}")

    css = (asset_dir / "interview-post.css").read_text(encoding="utf-8")
    for selector in (
        ".rli-intro", ".rli-article", ".rli-question", ".rli-answer",
        ".rli-linkedin", ".rli-sample-notice", ".rli-approval-notice",
    ):
        if selector not in css:
            errors.append(f"CSS is missing required selector {selector}")
    if "RLI_BLOG_DRAFT_PREVIEW_CSS_START" not in css or "RLI_BLOG_DRAFT_PREVIEW_CSS_END" not in css:
        errors.append("CSS requires stable start/end replacement markers")
    return errors


def main() -> int:
    default_dir = Path(__file__).resolve().parents[1] / "assets" / "carol-chen"
    asset_dir = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else default_dir
    if not asset_dir.is_dir():
        print(f"ERROR: not a directory: {asset_dir}", file=sys.stderr)
        return 2
    errors = validate(asset_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {asset_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
