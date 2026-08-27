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
TRANSCRIPT_API_PACKAGE = "youtube-transcript-api==1.2.4"
YT_DLP_PACKAGE = "yt-dlp"
WHISPER_PACKAGE = "faster-whisper>=1.1,<2"


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


def format_timestamp(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    whole_seconds, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d}.{milliseconds:03d}"


def parse_transcript_api_json(value: str) -> tuple[str, int]:
    """Normalize youtube-transcript-api JSON into timestamped Markdown."""
    payload = json.loads(value)
    if isinstance(payload, list) and len(payload) == 1 and isinstance(payload[0], list):
        payload = payload[0]
    if not isinstance(payload, list):
        raise ValueError("youtube-transcript-api returned an unexpected JSON shape")
    output: list[str] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        caption = clean_caption(str(item.get("text") or ""))
        if not caption:
            continue
        try:
            start = float(item.get("start") or 0)
        except (TypeError, ValueError):
            start = 0
        output.append(f"[{format_timestamp(start)}] {caption}")
    if not output:
        raise ValueError("youtube-transcript-api returned an empty transcript")
    return "\n\n".join(output) + "\n", len(output)


def tool_command(executable: str, package: str) -> list[str]:
    """Use an installed CLI or run the pinned free package ephemerally with uvx."""
    installed = shutil.which(executable)
    if installed:
        return [installed]
    uvx = shutil.which("uvx")
    if uvx:
        return [uvx, "--from", package, executable]
    raise ValueError(
        f"{executable} is unavailable; install it or install uv so the skill can run it ephemerally"
    )


def transcript_language(language: str) -> str:
    return language.rstrip(".*") or "en"


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
    *, guest_image: str | None, linkedin_url: str | None, og_image: str | None,
    require_open_graph: bool = True,
) -> dict[str, object]:
    provided = {
        "guestImage": guest_image,
        "linkedinProfile": linkedin_url,
        "openGraphImage": og_image,
    }
    required = {"guestImage", "linkedinProfile"}
    if require_open_graph:
        required.add("openGraphImage")
    missing = [name for name, value in provided.items() if name in required and not value]
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


def fetch_youtube_metadata(source_url: str) -> dict[str, object]:
    command = tool_command("yt-dlp", YT_DLP_PACKAGE)
    metadata_run = subprocess.run(
        command
        + [
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
    if not str(metadata.get("id") or ""):
        raise ValueError("yt-dlp metadata did not include a video ID")
    return metadata


def run_transcript_api(video_id: str, language: str) -> tuple[str, str, int]:
    selected_language = transcript_language(language)
    command = tool_command("youtube_transcript_api", TRANSCRIPT_API_PACKAGE)
    result = subprocess.run(
        command
        + [
            video_id,
            "--languages",
            selected_language,
            "--format",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    content, segment_count = parse_transcript_api_json(result.stdout)
    return content, selected_language, segment_count


def run_yt_dlp_captions(
    source_url: str, language: str, metadata: dict[str, object]
) -> tuple[str, str, int]:
    command = tool_command("yt-dlp", YT_DLP_PACKAGE)
    video_id = str(metadata.get("id") or "")
    with tempfile.TemporaryDirectory(prefix="rli-youtube-") as temp_dir:
        output_template = str(Path(temp_dir) / "%(id)s.%(ext)s")
        subprocess.run(
            command
            + [
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
    return content, language_code, content.count("\n\n") + 1


def run_local_whisper(
    source_url: str, metadata: dict[str, object], *, model: str
) -> tuple[str, str, int]:
    """Download audio and transcribe locally. This is opt-in because models are large."""
    yt_dlp = tool_command("yt-dlp", YT_DLP_PACKAGE)
    uv = shutil.which("uv")
    if not uv:
        raise ValueError("local Whisper fallback requires uv")
    video_id = str(metadata.get("id") or "")
    helper = Path(__file__).with_name("local_whisper_transcribe.py")
    with tempfile.TemporaryDirectory(prefix="rli-whisper-") as temp_dir:
        output_template = str(Path(temp_dir) / "%(id)s.%(ext)s")
        subprocess.run(
            yt_dlp
            + [
                "-f",
                "bestaudio/best",
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
        candidates = sorted(Path(temp_dir).glob(f"{video_id}.*"))
        if not candidates:
            raise ValueError("yt-dlp did not produce audio for local Whisper")
        result = subprocess.run(
            [
                uv,
                "run",
                "--with",
                WHISPER_PACKAGE,
                "python",
                str(helper),
                str(candidates[0]),
                "--model",
                model,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    payload = json.loads(result.stdout)
    segments = payload.get("segments") if isinstance(payload, dict) else None
    if not isinstance(segments, list):
        raise ValueError("local Whisper returned an unexpected JSON shape")
    content, segment_count = parse_transcript_api_json(json.dumps(segments))
    return content, str(payload.get("language") or "unknown"), segment_count


def ingest_youtube(
    source_url: str,
    output_dir: Path,
    *,
    language: str,
    embed_video: bool,
    guest_image: str | None,
    linkedin_url: str | None,
    og_image: str | None,
    whisper_fallback: bool = False,
    whisper_model: str = "small",
) -> dict[str, object]:
    if not is_youtube_url(source_url):
        raise ValueError("YouTube source must be a youtube.com or youtu.be URL")
    if og_image:
        raise ValueError("YouTube sources use the YouTube thumbnail for Open Graph; omit --og-image")
    metadata = fetch_youtube_metadata(source_url)
    video_id = str(metadata["id"])
    attempts: list[dict[str, str]] = []
    provider = "youtube-transcript-api"
    try:
        content, language_code, segment_count = run_transcript_api(video_id, language)
    except (ValueError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        attempts.append({"provider": provider, "result": f"failed: {exc}"})
        provider = "yt-dlp"
        try:
            content, language_code, segment_count = run_yt_dlp_captions(
                source_url, language, metadata
            )
        except (ValueError, OSError, subprocess.CalledProcessError) as fallback_exc:
            attempts.append({"provider": provider, "result": f"failed: {fallback_exc}"})
            if not whisper_fallback:
                raise ValueError(
                    "YouTube captions were unavailable. Re-run with --whisper-fallback "
                    "to download the audio and transcribe it locally."
                ) from fallback_exc
            provider = "faster-whisper"
            content, language_code, segment_count = run_local_whisper(
                source_url, metadata, model=whisper_model
            )
    attempts.append({"provider": provider, "result": "success"})
    generated = provider == "faster-whisper" or subtitle_kind(metadata, language_code) == "automatic-captions"
    thumbnail = str(metadata.get("thumbnail") or "") or None
    if not thumbnail:
        raise ValueError("YouTube metadata did not provide a thumbnail for Open Graph")
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
        "transcriptProvider": provider,
        "transcriptIsGenerated": generated,
        "transcriptSegmentCount": segment_count,
        "transcriptFallbacksAttempted": attempts,
        "youtube": {
            "videoId": video_id,
            "watchUrl": f"https://www.youtube.com/watch?v={video_id}",
            "embedUrl": f"https://www.youtube-nocookie.com/embed/{video_id}",
            "thumbnailUrl": str(metadata.get("thumbnail") or ""),
        },
        "embedVideo": embed_video,
        "openGraphCandidate": {
            "image": thumbnail,
            "imageSource": "youtube-thumbnail",
        },
        **prompt_inputs(
            guest_image=guest_image,
            linkedin_url=linkedin_url,
            og_image=None,
            require_open_graph=False,
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
    parser.add_argument(
        "--whisper-fallback",
        action="store_true",
        help="If captions fail, download audio and transcribe locally with faster-whisper",
    )
    parser.add_argument(
        "--whisper-model",
        default="small",
        help="faster-whisper model used only with --whisper-fallback (default: small)",
    )
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
                whisper_fallback=args.whisper_fallback,
                whisper_model=args.whisper_model,
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
