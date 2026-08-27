#!/usr/bin/env python3
"""Normalize YouTube, Markdown, or Granola interview sources into a draft manifest."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse


YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
CONTENT_KINDS = {"transcript", "notes", "notes-and-transcript"}
TIMING_RE = re.compile(
    r"^(?P<start>(?:\d{2}:)?\d{2}:\d{2}[.,]\d{3})\s+-->\s+"
)
TAG_RE = re.compile(r"<[^>]+>")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def is_https_url(value: str) -> bool:
    return urlparse(value).scheme == "https"


def is_youtube_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and parsed.netloc.lower() in YOUTUBE_HOSTS


def clean_caption(value: str) -> str:
    value = TAG_RE.sub("", value)
    value = html.unescape(value).replace("\u200b", " ")
    return " ".join(value.split())


def remove_word_overlap(previous: str, current: str) -> str:
    """Remove rolling-caption overlap while preserving genuinely new words."""
    if not previous or not current:
        return current
    previous_words = previous.split()
    current_words = current.split()
    limit = min(len(previous_words), len(current_words))
    for size in range(limit, 0, -1):
        if [word.casefold() for word in previous_words[-size:]] == [
            word.casefold() for word in current_words[:size]
        ]:
            return " ".join(current_words[size:])
    return current


def parse_vtt(path: Path) -> str:
    """Convert WebVTT captions into readable timestamped Markdown."""
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    cues: list[tuple[str, str]] = []
    current_time = ""
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_time, current_lines
        if current_time and current_lines:
            text = clean_caption(" ".join(current_lines))
            if text:
                cues.append((current_time.replace(",", "."), text))
        current_time = ""
        current_lines = []

    for line in lines:
        timing = TIMING_RE.match(line.strip())
        if timing:
            flush()
            current_time = timing.group("start")
            continue
        stripped = line.strip()
        if not stripped:
            flush()
        elif current_time and not stripped.isdigit():
            current_lines.append(stripped)
    flush()

    output: list[str] = []
    previous_full = ""
    for timestamp, caption in cues:
        if caption.casefold() == previous_full.casefold():
            continue
        new_text = remove_word_overlap(previous_full, caption)
        if new_text:
            output.append(f"[{timestamp}] {new_text}")
        previous_full = caption
    return "\n\n".join(output).strip() + "\n"


def first_heading(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback


def validate_optional_url(name: str, value: str | None) -> None:
    if value and not is_https_url(value):
        raise ValueError(f"{name} must be an HTTPS URL")


def prompt_inputs(
    *, guest_image: str | None, linkedin_url: str | None, og_image: str | None
) -> dict[str, object]:
    provided = {
        "guestImage": guest_image,
        "linkedinProfile": linkedin_url,
        "openGraphImage": og_image,
    }
    missing = [name for name, value in provided.items() if not value]
    return {"provided": provided, "missingPromptInputs": missing}


def write_bundle(output_dir: Path, content: str, manifest: dict[str, object]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    content_path = output_dir / "source-content.md"
    content_path.write_text(content, encoding="utf-8")
    manifest["contentFile"] = content_path.name
    manifest["contentSha256"] = sha256_text(content)
    (output_dir / "source.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def ingest_markdown(
    source: Path,
    output_dir: Path,
    *,
    source_type: str,
    content_kind: str,
    source_url: str | None,
    guest_image: str | None,
    linkedin_url: str | None,
    og_image: str | None,
) -> dict[str, object]:
    if not source.is_file():
        raise ValueError(f"source file does not exist: {source}")
    content = source.read_text(encoding="utf-8-sig", errors="replace").strip() + "\n"
    if not content.strip():
        raise ValueError("source file is empty")
    if source_type == "granola" and content_kind not in CONTENT_KINDS:
        raise ValueError(f"Granola content kind must be one of {sorted(CONTENT_KINDS)}")
    manifest: dict[str, object] = {
        "schemaVersion": 1,
        "sourceType": source_type,
        "sourceLocator": source_url or source.name,
        "sourceTitle": first_heading(content, source.stem),
        "contentKind": (
            f"granola-{content_kind}" if source_type == "granola" else content_kind
        ),
        "youtube": None,
        "embedVideo": False,
        "openGraphCandidate": {
            "image": og_image,
            "imageSource": "prompt" if og_image else None,
        },
        **prompt_inputs(
            guest_image=guest_image, linkedin_url=linkedin_url, og_image=og_image
        ),
    }
    write_bundle(output_dir, content, manifest)
    return manifest


def subtitle_kind(metadata: dict[str, object], language: str) -> str:
    subtitles = metadata.get("subtitles") or {}
    if isinstance(subtitles, dict) and any(
        key == language or key.startswith(language.rstrip(".*")) for key in subtitles
    ):
        return "manual-subtitles"
    return "automatic-captions"


def choose_vtt(directory: Path, video_id: str) -> Path:
    candidates = sorted(directory.glob(f"{video_id}*.vtt"))
    if not candidates:
        raise ValueError("YouTube video has no downloadable captions for the requested language")
    candidates.sort(
        key=lambda path: (
            ".en.vtt" not in path.name,
            ".en-orig.vtt" not in path.name,
            len(path.name),
            path.name,
        )
    )
    return candidates[0]


def run_yt_dlp(source_url: str, language: str) -> tuple[dict[str, object], str, str]:
    executable = shutil.which("yt-dlp")
    if not executable:
        raise ValueError("yt-dlp is required for YouTube ingestion but is not installed")
    metadata_run = subprocess.run(
        [
            executable,
            "--dump-single-json",
            "--skip-download",
            "--no-playlist",
            "--",
            source_url,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    metadata = json.loads(metadata_run.stdout)
    video_id = str(metadata.get("id") or "")
    if not video_id:
        raise ValueError("yt-dlp metadata did not include a video ID")
    with tempfile.TemporaryDirectory(prefix="rli-youtube-") as temp_dir:
        output_template = str(Path(temp_dir) / "%(id)s.%(ext)s")
        subprocess.run(
            [
                executable,
                "--skip-download",
                "--write-subs",
                "--write-auto-subs",
                "--sub-langs",
                language,
                "--sub-format",
                "vtt",
                "--no-playlist",
                "-o",
                output_template,
                "--",
                source_url,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        vtt_path = choose_vtt(Path(temp_dir), video_id)
        content = parse_vtt(vtt_path)
        if not content.strip():
            raise ValueError("downloaded captions produced an empty transcript")
        language_code = vtt_path.name.removeprefix(f"{video_id}.").removesuffix(".vtt")
    return metadata, content, language_code


def ingest_youtube(
    source_url: str,
    output_dir: Path,
    *,
    language: str,
    embed_video: bool,
    guest_image: str | None,
    linkedin_url: str | None,
    og_image: str | None,
) -> dict[str, object]:
    if not is_youtube_url(source_url):
        raise ValueError("YouTube source must be a youtube.com or youtu.be URL")
    metadata, content, language_code = run_yt_dlp(source_url, language)
    video_id = str(metadata["id"])
    thumbnail = og_image or str(metadata.get("thumbnail") or "") or None
    manifest: dict[str, object] = {
        "schemaVersion": 1,
        "sourceType": "youtube",
        "sourceLocator": str(metadata.get("webpage_url") or source_url),
        "sourceTitle": str(metadata.get("title") or ""),
        "sourceAuthor": str(metadata.get("uploader") or metadata.get("channel") or ""),
        "sourcePublishedDate": str(metadata.get("upload_date") or ""),
        "sourceDescription": str(metadata.get("description") or ""),
        "contentKind": subtitle_kind(metadata, language_code),
        "contentLanguage": language_code,
        "youtube": {
            "videoId": video_id,
            "watchUrl": f"https://www.youtube.com/watch?v={video_id}",
            "embedUrl": f"https://www.youtube-nocookie.com/embed/{video_id}",
            "thumbnailUrl": str(metadata.get("thumbnail") or ""),
        },
        "embedVideo": embed_video,
        "openGraphCandidate": {
            "image": thumbnail,
            "imageSource": "prompt" if og_image else "youtube-thumbnail",
        },
        **prompt_inputs(
            guest_image=guest_image,
            linkedin_url=linkedin_url,
            og_image=thumbnail,
        ),
    }
    write_bundle(output_dir, content, manifest)
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize a YouTube, Markdown, or Granola interview source."
    )
    parser.add_argument("source", help="YouTube URL or local Markdown/text file")
    parser.add_argument("--output", required=True, type=Path, help="Output directory")
    parser.add_argument(
        "--source-type",
        choices=("auto", "youtube", "markdown", "granola"),
        default="auto",
    )
    parser.add_argument(
        "--content-kind",
        choices=tuple(sorted(CONTENT_KINDS)),
        default="transcript",
        help="Whether a local source contains a transcript, notes, or both",
    )
    parser.add_argument("--source-url", help="Optional original Granola/share URL")
    parser.add_argument("--language", default="en.*", help="YouTube subtitle language")
    parser.add_argument("--no-embed-video", action="store_true")
    parser.add_argument("--guest-image")
    parser.add_argument("--linkedin-url")
    parser.add_argument("--og-image")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        for name, value in (
            ("guest image", args.guest_image),
            ("LinkedIn URL", args.linkedin_url),
            ("Open Graph image", args.og_image),
            ("source URL", args.source_url),
        ):
            validate_optional_url(name, value)
        source_type = args.source_type
        if source_type == "auto":
            source_type = "youtube" if is_youtube_url(args.source) else "markdown"
        if source_type == "youtube":
            manifest = ingest_youtube(
                args.source,
                args.output,
                language=args.language,
                embed_video=not args.no_embed_video,
                guest_image=args.guest_image,
                linkedin_url=args.linkedin_url,
                og_image=args.og_image,
            )
        else:
            manifest = ingest_markdown(
                Path(args.source).expanduser().resolve(),
                args.output,
                source_type=source_type,
                content_kind=args.content_kind,
                source_url=args.source_url,
                guest_image=args.guest_image,
                linkedin_url=args.linkedin_url,
                og_image=args.og_image,
            )
    except (ValueError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    missing = manifest.get("missingPromptInputs") or []
    print(f"OK: {args.output.resolve()}")
    if missing:
        print("PROMPT_REQUIRED: " + ", ".join(str(item) for item in missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
