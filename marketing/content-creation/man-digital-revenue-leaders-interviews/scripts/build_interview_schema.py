#!/usr/bin/env python3
"""Build and safely merge managed JSON-LD for a Revenue Leaders Interview."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


MARKER_START = "<!-- schema-graph:start -->"
MARKER_END = "<!-- schema-graph:end -->"
LEGACY_MARKER_START = "<!-- openclaw-schema-graph:start -->"
LEGACY_MARKER_END = "<!-- openclaw-schema-graph:end -->"
SERIES_NAME = "Revenue Leaders Interviews"
SITE_URL = "https://www.man.digital"
ORGANIZATION_ID = f"{SITE_URL}/#organization"
WEBSITE_ID = f"{SITE_URL}/#website"


def _https_url(value: object, field: str) -> str:
    text = str(value or "").strip()
    parsed = urlparse(text)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"{field} must be an absolute HTTPS URL")
    return text.rstrip("/")


def _iso_upload_date(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError("YouTube schema requires sourcePublishedDate")
    if len(text) == 8 and text.isdigit():
        parsed = dt.datetime.strptime(text, "%Y%m%d").date()
        return parsed.isoformat()
    try:
        return dt.date.fromisoformat(text).isoformat()
    except ValueError as exc:
        raise ValueError("sourcePublishedDate must use YYYYMMDD or YYYY-MM-DD") from exc


def _schema_config(metadata: dict[str, Any]) -> dict[str, Any]:
    config = metadata.get("schema")
    if not isinstance(config, dict) or config.get("enabled") is not True:
        raise ValueError("metadata.schema.enabled must be true")
    if config.get("mode") != "managed-graph":
        raise ValueError("metadata.schema.mode must be managed-graph")
    return config


def build_interview_graph(
    metadata: dict[str, Any],
    source: dict[str, Any],
    *,
    page_url: str,
    published_iso: str = "",
    modified_iso: str = "",
) -> dict[str, Any]:
    """Return the connected schema.org graph for one interview post."""
    config = _schema_config(metadata)
    page_url = _https_url(page_url, "page_url")
    if not page_url.startswith(f"{SITE_URL}/blog/"):
        raise ValueError("page_url must use the canonical https://www.man.digital/blog/ path")

    article_title = str(metadata.get("articleTitle") or "").strip()
    description = str(metadata.get("metaDescription") or "").strip()
    image_url = _https_url(metadata.get("openGraphImage"), "openGraphImage")
    if not article_title or not description:
        raise ValueError("articleTitle and metaDescription are required")

    author = config.get("author")
    if not isinstance(author, dict):
        raise ValueError("metadata.schema.author must be an object")
    author_name = str(author.get("name") or "").strip()
    author_url = _https_url(author.get("url"), "schema.author.url")
    author_same_as = author.get("sameAs")
    if not author_name or not isinstance(author_same_as, list) or not author_same_as:
        raise ValueError("schema.author requires name and at least one sameAs URL")
    author_same_as = [_https_url(value, "schema.author.sameAs") for value in author_same_as]

    guest = metadata.get("guest")
    if not isinstance(guest, dict):
        raise ValueError("metadata.guest must be an object")
    guest_name = str(guest.get("name") or "").strip()
    guest_title = str(guest.get("jobTitle") or "").strip()
    guest_company = str(guest.get("company") or "").strip()
    guest_image = _https_url(guest.get("image"), "guest.image")
    profile_url = _https_url(
        (metadata.get("linkedinVerification") or {}).get("profileUrl"),
        "linkedinVerification.profileUrl",
    )
    if not guest_name or not guest_title or not guest_company:
        raise ValueError("guest requires name, jobTitle, and company")

    author_id = f"{author_url}#person"
    guest_id = f"{page_url}#guest"
    image_id = f"{page_url}#primaryimage"
    webpage_id = f"{page_url}#webpage"
    breadcrumb_id = f"{page_url}#breadcrumb"
    article_id = f"{page_url}#article"

    nodes: list[dict[str, Any]] = [
        {
            "@type": "Person",
            "@id": author_id,
            "name": author_name,
            "url": author_url,
            "sameAs": author_same_as,
            "worksFor": {"@id": ORGANIZATION_ID},
        },
        {
            "@type": "Person",
            "@id": guest_id,
            "name": guest_name,
            "jobTitle": guest_title,
            "image": guest_image,
            "worksFor": {"@type": "Organization", "name": guest_company},
            "sameAs": [profile_url],
        },
        {
            "@type": "ImageObject",
            "@id": image_id,
            "url": image_url,
            "contentUrl": image_url,
        },
    ]

    video_id = ""
    if metadata.get("embedVideo") is True:
        youtube = source.get("youtube")
        if not isinstance(youtube, dict):
            raise ValueError("embedded-video schema requires source.youtube")
        video_id = f"{page_url}#video"
        nodes.append(
            {
                "@type": "VideoObject",
                "@id": video_id,
                "name": str(source.get("sourceTitle") or article_title).strip(),
                "description": description,
                "thumbnailUrl": [image_url],
                "uploadDate": _iso_upload_date(source.get("sourcePublishedDate")),
                "embedUrl": _https_url(youtube.get("embedUrl"), "youtube.embedUrl"),
                "isPartOf": {"@id": article_id},
            }
        )

    nodes.extend(
        [
            {
                "@type": "WebPage",
                "@id": webpage_id,
                "url": page_url,
                "name": str(metadata.get("seoTitle") or article_title).strip(),
                "description": description,
                "isPartOf": {"@id": WEBSITE_ID},
                "primaryImageOfPage": {"@id": image_id},
                "breadcrumb": {"@id": breadcrumb_id},
                "mainEntity": {"@id": article_id},
                "inLanguage": "en",
            },
            {
                "@type": "BreadcrumbList",
                "@id": breadcrumb_id,
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": SITE_URL,
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Blog",
                        "item": f"{SITE_URL}/blog",
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": article_title[:120],
                        "item": page_url,
                    },
                ],
            },
        ]
    )

    article: dict[str, Any] = {
        "@type": "Article",
        "@id": article_id,
        "headline": article_title[:110],
        "name": article_title,
        "description": description,
        "mainEntityOfPage": {"@id": webpage_id},
        "isPartOf": {"@id": WEBSITE_ID},
        "image": {"@id": image_id},
        "author": {"@id": author_id},
        "publisher": {"@id": ORGANIZATION_ID},
        "contributor": {"@id": guest_id},
        "about": {"@id": guest_id},
        "articleSection": SERIES_NAME,
        "inLanguage": "en",
    }
    if video_id:
        article["video"] = {"@id": video_id}
    if published_iso:
        article["datePublished"] = published_iso
    if modified_iso:
        article["dateModified"] = modified_iso
    nodes.append(article)

    return {"@context": "https://schema.org", "@graph": nodes}


def wrap_schema_graph(graph: dict[str, Any]) -> str:
    body = json.dumps(graph, separators=(",", ":"), ensure_ascii=False)
    body = body.replace("</", "<\\/")
    return (
        f"{MARKER_START}\n"
        f'<script type="application/ld+json">{body}</script>\n'
        f"{MARKER_END}"
    )


def inject_managed_schema(existing_head_html: str, new_block: str) -> str:
    """Append or replace one marker-bounded region without touching other HTML."""
    if not existing_head_html:
        return new_block
    variants = (
        (MARKER_START, MARKER_END),
        (LEGACY_MARKER_START, LEGACY_MARKER_END),
    )
    present: list[tuple[str, str]] = []
    for marker_start, marker_end in variants:
        start_count = existing_head_html.count(marker_start)
        end_count = existing_head_html.count(marker_end)
        if start_count != end_count or start_count > 1:
            raise ValueError(
                "headHtml must contain zero or one complete schema-graph marker pair"
            )
        if start_count == 1:
            present.append((marker_start, marker_end))
    if len(present) > 1:
        raise ValueError("headHtml contains both current and legacy schema marker pairs")
    if not present:
        separator = "" if existing_head_html.endswith("\n") else "\n"
        return f"{existing_head_html}{separator}{new_block}"
    marker_start, marker_end = present[0]
    start = existing_head_html.index(marker_start)
    end = existing_head_html.index(marker_end)
    if end < start:
        raise ValueError("schema-graph end marker appears before its start marker")
    end += len(marker_end)
    return f"{existing_head_html[:start]}{new_block}{existing_head_html[end:]}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asset_dir", type=Path)
    parser.add_argument("--page-url", required=True)
    parser.add_argument("--published-at", default="")
    parser.add_argument("--modified-at", default="")
    parser.add_argument("--existing-head-html", type=Path)
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    metadata = json.loads((args.asset_dir / "metadata.example.json").read_text(encoding="utf-8"))
    source_path = args.asset_dir / "source.json"
    source = json.loads(source_path.read_text(encoding="utf-8")) if source_path.is_file() else {}
    graph = build_interview_graph(
        metadata,
        source,
        page_url=args.page_url,
        published_iso=args.published_at,
        modified_iso=args.modified_at,
    )
    rendered = wrap_schema_graph(graph)
    if args.existing_head_html:
        existing = args.existing_head_html.read_text(encoding="utf-8")
        rendered = inject_managed_schema(existing, rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
