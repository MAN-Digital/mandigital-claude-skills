#!/usr/bin/env python3
"""Validate a Revenue Leaders Interview asset directory without network access."""

from __future__ import annotations

import hashlib
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
        self.iframes: list[dict[str, str | None]] = []
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
        if tag == "iframe":
            self.iframes.append(values)

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
        "editorialState", "sourceType", "embedVideo", "leadMediaMode", "seoTitle", "metaDescription", "openGraphTitle",
        "openGraphDescription", "openGraphImage", "openGraphImageSource", "tag", "campaign", "campaignId",
        "questionSelectionMethod", "designReference", "questions", "draft",
    }
    absent = sorted(required_metadata - metadata.keys())
    if absent:
        errors.append(f"missing metadata keys: {', '.join(absent)}")

    qa_count = sum("rli-qa" in item for item in parser.classes)
    question_count = len(parser.question_texts)
    answer_count = sum("rli-answer" in item for item in parser.classes)
    notice_count = sum("rli-sample-notice" in item for item in parser.classes)
    source_notice_count = sum("rli-source-notice" in item for item in parser.classes)
    approval_notice_count = sum("rli-approval-notice" in item for item in parser.classes)
    video_wrapper_count = sum("rli-video" in item for item in parser.classes)
    lead_image_count = sum("rli-article__lead" in item for item in parser.classes)
    if question_count == 0 or len({qa_count, question_count, answer_count}) != 1:
        errors.append(f"Q/A structure mismatch: sections/questions/answers={qa_count}/{question_count}/{answer_count}")
    if not 7 <= question_count <= 8:
        errors.append(f"interviews require 7-8 complete questions; got {question_count}")
    if len(parser.question_ids) != question_count or any(not value for value in parser.question_ids):
        errors.append("every question requires a stable non-empty ID")
    if len(parser.ids) != len(set(parser.ids)):
        errors.append("HTML IDs must be unique across intro and body")

    selected_questions = metadata.get("questions")
    if not isinstance(selected_questions, list) or not selected_questions or not all(
        isinstance(item, str) and item.strip() for item in selected_questions
    ):
        errors.append("questions must be a non-empty list of exact source-adapted question strings")
    elif not 7 <= len(selected_questions) <= 8:
        errors.append(f"metadata questions require 7-8 items; got {len(selected_questions)}")
    elif parser.question_texts != selected_questions:
        errors.append("rendered question wording/order must exactly match metadata questions")
    if metadata.get("questionSelectionMethod") != "source-adapted":
        errors.append("questionSelectionMethod must be source-adapted")
    design_reference = metadata.get("designReference", "")
    parsed_source = urlparse(design_reference) if isinstance(design_reference, str) else urlparse("")
    if parsed_source.scheme != "https" or parsed_source.netloc != "www.figma.com" or "node-id=" not in parsed_source.query:
        errors.append("designReference must be an HTTPS Figma node URL")

    editorial_state = metadata.get("editorialState")
    allowed_states = {
        "draft-source-derived", "draft-sample-answers",
        "draft-transcript-reviewed", "approved",
    }
    if editorial_state not in allowed_states:
        errors.append(f"editorialState must be one of {sorted(allowed_states)}")
    for root_class, states in parser.root_states.items():
        if states != [editorial_state]:
            errors.append(f"{root_class} must declare exactly the metadata editorialState")

    expected_answer_state = {
        "draft-source-derived": "source-derived",
        "draft-sample-answers": "illustrative",
        "draft-transcript-reviewed": "transcript-reviewed",
        "approved": "approved",
    }.get(editorial_state)
    if expected_answer_state and (
        len(parser.qa_answer_states) != qa_count
        or set(parser.qa_answer_states) != {expected_answer_state}
    ):
        errors.append(f"every Q/A section must use data-answer-state={expected_answer_state}")

    if editorial_state == "draft-source-derived":
        if source_notice_count or notice_count or approval_notice_count:
            errors.append("source-derived drafts must not include reader-facing draft notices")
    elif editorial_state == "draft-sample-answers":
        if source_notice_count:
            errors.append("sample drafts must not include rli-source-notice")
        if notice_count != 1:
            errors.append("sample drafts require exactly one visible rli-sample-notice")
        if approval_notice_count:
            errors.append("sample drafts must not include rli-approval-notice")
    elif editorial_state == "draft-transcript-reviewed":
        if source_notice_count or notice_count:
            errors.append("transcript-reviewed drafts must not include source or sample notices")
        if approval_notice_count != 1:
            errors.append("transcript-reviewed drafts require exactly one visible rli-approval-notice")
    elif editorial_state == "approved":
        if source_notice_count or notice_count or approval_notice_count:
            errors.append("approved content must not include draft notices")
    if parser.draft_placeholder_count:
        errors.append("interview content must not include draft placeholders")

    expected_quote_state = {
        "draft-source-derived": "source-derived",
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

    source_type = metadata.get("sourceType")
    allowed_source_types = {"sample", "youtube", "markdown", "granola"}
    if source_type not in allowed_source_types:
        errors.append(f"sourceType must be one of {sorted(allowed_source_types)}")
    if source_type == "sample" and editorial_state != "draft-sample-answers":
        errors.append("sample sourceType is only valid for draft-sample-answers")
    if source_type in {"youtube", "markdown", "granola"} and editorial_state == "draft-sample-answers":
        errors.append("transcript-backed sourceType cannot use draft-sample-answers")
    embed_video = metadata.get("embedVideo")
    if not isinstance(embed_video, bool):
        errors.append("embedVideo must be a boolean")
    if source_type != "youtube" and embed_video is True:
        errors.append("only YouTube sources may enable embedVideo")
    lead_media_mode = metadata.get("leadMediaMode")
    if embed_video is True:
        if lead_media_mode != "video":
            errors.append("embedded video posts must use leadMediaMode=video")
        if lead_image_count:
            errors.append("embedded video posts must not render a separate lead image above the player")
    elif embed_video is False:
        if lead_media_mode != "image":
            errors.append("posts without an embedded video must use leadMediaMode=image")
        if lead_image_count != 1:
            errors.append("posts without an embedded video require exactly one user-provided rli-article__lead image")

    if source_type in {"youtube", "markdown", "granola"}:
        source_path = asset_dir / "source.json"
        evidence_path = asset_dir / "evidence-map.json"
        source_content_hash: str | None = None
        if not source_path.is_file():
            errors.append("transcript-backed assets require source.json")
        else:
            try:
                source_manifest = json.loads(source_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"invalid source.json: {exc}")
                source_manifest = {}
            if source_manifest.get("sourceType") != source_type:
                errors.append("source.json sourceType must match metadata sourceType")
            if source_manifest.get("embedVideo") is not embed_video:
                errors.append("source.json embedVideo must match metadata embedVideo")
            missing_inputs = source_manifest.get("missingPromptInputs")
            if not isinstance(missing_inputs, list):
                errors.append("source.json missingPromptInputs must be a list")
            elif missing_inputs:
                errors.append("resolve every source.json missingPromptInputs item before validation")
            content_file = source_manifest.get("contentFile")
            content_path = asset_dir / str(content_file or "")
            if not content_file or not content_path.is_file():
                errors.append("source.json must reference an existing contentFile")
            else:
                content_hash = hashlib.sha256(content_path.read_bytes()).hexdigest()
                source_content_hash = content_hash
                if source_manifest.get("contentSha256") != content_hash:
                    errors.append("source.json contentSha256 must match contentFile")

            youtube = source_manifest.get("youtube")
            if source_type == "youtube":
                if not isinstance(youtube, dict):
                    errors.append("YouTube source.json requires a youtube object")
                    embed_url = ""
                else:
                    embed_url = str(youtube.get("embedUrl") or "")
                    parsed_embed = urlparse(embed_url)
                    if parsed_embed.scheme != "https" or parsed_embed.netloc != "www.youtube-nocookie.com":
                        errors.append("YouTube embedUrl must use https://www.youtube-nocookie.com")
                    thumbnail_url = str(youtube.get("thumbnailUrl") or "")
                    if urlparse(thumbnail_url).scheme != "https":
                        errors.append("YouTube thumbnailUrl must use HTTPS")
                open_graph_candidate = source_manifest.get("openGraphCandidate")
                if not isinstance(open_graph_candidate, dict):
                    errors.append("YouTube source.json requires an openGraphCandidate")
                else:
                    if open_graph_candidate.get("imageSource") != "youtube-thumbnail":
                        errors.append("YouTube Open Graph image must be identified as youtube-thumbnail")
                    if open_graph_candidate.get("image") != metadata.get("openGraphImage"):
                        errors.append("YouTube Open Graph image must match the source candidate")
                if embed_video is True:
                    if video_wrapper_count != 1 or len(parser.iframes) != 1:
                        errors.append("enabled YouTube embeds require exactly one rli-video wrapper and iframe")
                    elif parser.iframes[0].get("src") != embed_url:
                        errors.append("rendered YouTube iframe must match source.json embedUrl")
                    elif not parser.iframes[0].get("title"):
                        errors.append("YouTube iframe requires an accessible title")
                elif video_wrapper_count or parser.iframes:
                    errors.append("disabled YouTube embeds must not render rli-video or iframe")
            elif youtube is not None:
                errors.append("non-YouTube source.json must set youtube to null")
            if source_type != "youtube" and (video_wrapper_count or parser.iframes):
                errors.append("Markdown and Granola sources must not render a YouTube embed")

        if not evidence_path.is_file():
            errors.append("transcript-backed assets require evidence-map.json")
        else:
            try:
                evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"invalid evidence-map.json: {exc}")
                evidence = {}
            evidence_questions = evidence.get("questions")
            if source_content_hash and evidence.get("sourceSha256") != source_content_hash:
                errors.append("evidence-map sourceSha256 must match source content")
            if not isinstance(evidence_questions, list):
                errors.append("evidence-map.json questions must be a list")
            else:
                mapped_questions = [item.get("question") for item in evidence_questions if isinstance(item, dict)]
                if mapped_questions != selected_questions:
                    errors.append("evidence-map questions must exactly match metadata questions")
                for item in evidence_questions:
                    if not isinstance(item, dict):
                        errors.append("each evidence-map question must be an object")
                        continue
                    if item.get("coverage") not in {"direct", "partial"}:
                        errors.append("evidence-map coverage must be direct or partial; missing questions are not allowed")
                    if not item.get("evidence"):
                        errors.append("every evidence-map entry requires evidence")
                    if not item.get("sourceRefs"):
                        errors.append("every evidence-map entry requires sourceRefs")

    elif video_wrapper_count or parser.iframes:
        errors.append("sample assets must not render a YouTube embed")
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
    expected_og_source = "youtube-thumbnail" if source_type == "youtube" else "user-provided-image"
    if metadata.get("openGraphImageSource") != expected_og_source:
        errors.append(f"openGraphImageSource must be {expected_og_source}")

    try:
        svg_root = ET.fromstring((asset_dir / "linkedin-icon.svg").read_text(encoding="utf-8"))
        if not svg_root.tag.endswith("svg") or not any(element.tag.endswith("path") for element in svg_root.iter()):
            errors.append("linkedin-icon.svg must contain an SVG path")
    except (OSError, ET.ParseError) as exc:
        errors.append(f"invalid linkedin-icon.svg: {exc}")

    css = (asset_dir / "interview-post.css").read_text(encoding="utf-8")
    for selector in (
        ".rli-intro", ".rli-article", ".rli-question", ".rli-answer",
        ".rli-linkedin", ".rli-sample-notice",
        ".rli-approval-notice", ".rli-video",
    ):
        if selector not in css:
            errors.append(f"CSS is missing required selector {selector}")
    if "RLI_BLOG_DRAFT_PREVIEW_CSS_START" not in css or "RLI_BLOG_DRAFT_PREVIEW_CSS_END" not in css:
        errors.append("CSS requires stable start/end replacement markers")
    compact_css = "".join(css.lower().split())
    if ".rli-video{" not in compact_css or "width:100%" not in compact_css:
        errors.append("rli-video must span 100% of the blog body width")
    if ".mce-preview-object" not in compact_css:
        errors.append("rli-video CSS must expand HubSpot's iframe preview wrapper")
    if "background:#0a0a0a" in compact_css or "background:black" in compact_css:
        errors.append("rli-video must not add a black background around the player")
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
