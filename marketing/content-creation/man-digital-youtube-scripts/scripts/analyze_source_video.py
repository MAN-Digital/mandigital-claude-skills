#!/usr/bin/env python3
"""Analyze a source video with Gemini's video-understanding API and emit a
timestamped, structured event list for building a video-grounded Visual Cue
Sheet. See ../references/video-grounded-storyboard.md for the full workflow
and how to fold the output into the Blueprint and Cue Sheet.

Setup:
    pip install -r requirements.txt

    Then set your API key ONE of two ways (see ../README.md "Setting up your
    API key" for the full walkthrough):
      1. Export it in your shell profile, so every terminal/session has it:
             export GEMINI_API_KEY="..."
      2. Or copy ../.env.example to ../.env (same folder as SKILL.md) and put
         the key there -- this script loads that file automatically. ../.env
         is gitignored; never commit it.

Usage:
    python analyze_source_video.py /path/to/video.mp4 --out video-events.json
    python analyze_source_video.py "https://www.youtube.com/watch?v=XXXX" --out video-events.json
    python analyze_source_video.py "https://www.loom.com/share/XXXXXXXX..." --out video-events.json

No length limit -- long videos just cost more (Gemini bills roughly 300
tokens per second of video at default resolution; see
../references/video-grounded-storyboard.md for the cost breakdown).

Loom download: tries Loom's undocumented `transcoded-url` endpoint first; if
that returns anything other than 200 (observed to happen for some
videos/workspaces), falls back to reassembling the video from the signed HLS
stream on the public embed page. The HLS fallback requires ffmpeg on PATH.

Verified end-to-end against a real API key and a real Loom video (both the
transcoded-url path failing over to the HLS fallback, and the resulting file
being correctly analyzed by Gemini). YouTube URLs and the primary
transcoded-url download path follow Gemini's/Loom's documented and
widely-used patterns but have not themselves been separately tested here.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
from pathlib import Path

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load ../.env (the skill folder root, next to .env.example) if present.
# An already-exported shell variable always wins -- load_dotenv() never
# overrides an existing os.environ value.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

LOOM_ID_RE = re.compile(r"loom\.com/(?:share|embed)/([a-f0-9]{32})", re.IGNORECASE)

EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "events": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "timestamp": {
                        "type": "string",
                        "description": "MM:SS position in the source video",
                    },
                    "screen_or_context": {
                        "type": "string",
                        "description": "What tool, screen, or state is visible",
                    },
                    "action": {
                        "type": "string",
                        "description": "What the presenter does: click, type, toggle, scroll",
                    },
                    "on_screen_text": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Visible UI labels, field names, or button text",
                    },
                    "notes": {
                        "type": "string",
                        "description": "Anything unclear or worth flagging before relying on this event",
                    },
                },
                "required": ["timestamp", "screen_or_context", "action"],
            },
        }
    },
    "required": ["events"],
}

PROMPT = """You are extracting a structured storyboard from a screen-share tutorial video.

Go through the video and list every distinct on-screen action or screen change, in order,
with an MM:SS timestamp for each. For each one, note what screen or tool is visible, what
action the presenter takes, and any on-screen text a video editor would need to reference
(button names, field values, tab names).

Be literal about what is visible. Do not infer business reasoning or narration intent --
only describe what is shown on screen. If something is ambiguous or too small to read
clearly, say so in that event's notes field instead of guessing.

Return only the JSON described by the response schema. No prose outside the JSON."""


def get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        sys.exit(
            "No API key found. Set GEMINI_API_KEY (or GOOGLE_API_KEY) before running this "
            "script -- get one at https://aistudio.google.com/apikey. Never commit a real "
            "key to this repo."
        )
    return genai.Client(api_key=api_key)


def _sign_relative_uri(base_dir: str, query: str, line: str) -> str:
    """Rewrite a relative HLS playlist line to an absolute URL carrying the same
    signed query string as its parent. Loom's CloudFront signature covers a
    wildcard resource path, but naive HLS clients (including ffmpeg) won't
    propagate a parent playlist's query string down to the children it
    references -- so relative sub-playlist/segment URIs 403 unless we do it
    ourselves."""
    line = line.strip()
    if not line or line.startswith("#") or line.startswith("http"):
        return line
    return f"{base_dir}/{line}?{query}"


def _localize_playlist(playlist_url: str, out_path: str) -> None:
    base_dir = playlist_url.split("?")[0].rsplit("/", 1)[0]
    query = urllib.parse.urlparse(playlist_url).query
    text = requests.get(playlist_url, timeout=30).text
    signed = [_sign_relative_uri(base_dir, query, line) for line in text.splitlines()]
    with open(out_path, "w") as f:
        f.write("\n".join(signed))


def _download_loom_via_embed_hls(video_id: str) -> str:
    """Fallback for when Loom's transcoded-url endpoint doesn't return a download
    link. Pulls the signed HLS manifest straight out of the public embed page --
    the same one any anonymous viewer's browser uses to actually play the video
    -- and reassembles video + audio into an MP4 with ffmpeg. Requires ffmpeg on
    PATH."""
    if shutil.which("ffmpeg") is None:
        sys.exit(
            "This Loom video needs the HLS fallback path, which requires ffmpeg "
            "(brew install ffmpeg on a Mac). Install it and try again, or download "
            "the video manually from Loom's UI and pass the local file path instead."
        )

    embed_html = requests.get(
        f"https://www.loom.com/embed/{video_id}",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    ).text
    match = re.search(r'https://luna\.loom\.com/[^"\']*\.m3u8\?[^"\']*', embed_html)
    if not match:
        sys.exit(
            "Could not find a playable stream on Loom's embed page either. This video "
            "may genuinely be access-restricted -- download it manually from Loom's UI "
            "and pass the local file path instead."
        )
    master_url = match.group(0)
    master_base_dir = master_url.split("?")[0].rsplit("/", 1)[0]
    query = urllib.parse.urlparse(master_url).query
    lines = requests.get(master_url, timeout=30).text.splitlines()

    audio_url = None
    audio_line = next(
        (l for l in lines if l.startswith("#EXT-X-MEDIA") and "TYPE=AUDIO" in l), None
    )
    if audio_line:
        uri_match = re.search(r'URI="([^"]+)"', audio_line)
        if uri_match:
            audio_url = f"{master_base_dir}/{uri_match.group(1)}?{query}"

    best_bandwidth, best_video_uri = -1, None
    for i, line in enumerate(lines):
        if line.startswith("#EXT-X-STREAM-INF"):
            bw_match = re.search(r"BANDWIDTH=(\d+)", line)
            bw = int(bw_match.group(1)) if bw_match else 0
            uri = lines[i + 1].strip() if i + 1 < len(lines) else None
            if uri and bw > best_bandwidth:
                best_bandwidth, best_video_uri = bw, uri
    if best_video_uri is None:
        sys.exit("Could not find a video stream in Loom's HLS manifest.")
    video_url = f"{master_base_dir}/{best_video_uri}?{query}"

    tmp_dir = tempfile.mkdtemp(prefix="loom_hls_")
    video_playlist = os.path.join(tmp_dir, "video.m3u8")
    _localize_playlist(video_url, video_playlist)

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-protocol_whitelist", "file,http,https,tcp,tls,crypto", "-i", video_playlist,
    ]
    if audio_url:
        audio_playlist = os.path.join(tmp_dir, "audio.m3u8")
        _localize_playlist(audio_url, audio_playlist)
        ffmpeg_cmd += ["-protocol_whitelist", "file,http,https,tcp,tls,crypto", "-i", audio_playlist]
        ffmpeg_cmd += ["-map", "0:v", "-map", "1:a"]

    out_path = os.path.join(tempfile.gettempdir(), f"loom_{video_id}_hls.mp4")
    ffmpeg_cmd += ["-c", "copy", out_path]

    print(f"Reassembling Loom video {video_id} from its HLS stream via ffmpeg...", file=sys.stderr)
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if result.returncode != 0 or not os.path.exists(out_path):
        sys.exit(
            "ffmpeg failed to reassemble the Loom video from its HLS stream. ffmpeg "
            f"stderr (last 2000 chars):\n{result.stderr[-2000:]}"
        )
    return out_path


def resolve_loom_video(source: str) -> str:
    """Download a public Loom share/embed URL to a temp local MP4 and return its path.

    Tries Loom's undocumented `transcoded-url` endpoint first (fast, simple, and
    what several independent open-source Loom downloaders use). If that doesn't
    return a usable link -- observed to happen for some videos/workspaces, returning
    204 with no body -- falls back to reassembling the video from the public embed
    page's signed HLS stream instead."""
    match = LOOM_ID_RE.search(source)
    if not match:
        sys.exit(
            f"Could not find a Loom video ID in: {source}\n"
            "Expected a URL like https://www.loom.com/share/<32-char-hex-id>"
        )
    video_id = match.group(1)

    resp = requests.post(f"https://www.loom.com/api/campaigns/sessions/{video_id}/transcoded-url")
    if resp.status_code == 200:
        download_url = resp.json()["url"]
        tmp_path = os.path.join(tempfile.gettempdir(), f"loom_{video_id}.mp4")
        print(f"Downloading Loom video {video_id}...", file=sys.stderr)
        with requests.get(download_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(tmp_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 20):
                    f.write(chunk)
        return tmp_path

    print(
        f"Loom's transcoded-url endpoint returned HTTP {resp.status_code} for this "
        "video -- falling back to reassembling it from the embed page's HLS stream.",
        file=sys.stderr,
    )
    return _download_loom_via_embed_hls(video_id)


def upload_local_file(client: genai.Client, path: str) -> types.Part:
    print(f"Uploading {path} to Gemini's File API...", file=sys.stderr)
    uploaded = client.files.upload(file=path)

    # Video processing is asynchronous -- poll until it's ACTIVE before referencing it.
    while uploaded.state.name == "PROCESSING":
        time.sleep(3)
        uploaded = client.files.get(name=uploaded.name)

    if uploaded.state.name != "ACTIVE":
        sys.exit(f"Upload did not become ACTIVE (state: {uploaded.state.name}).")

    return types.Part(
        file_data=types.FileData(file_uri=uploaded.uri, mime_type=uploaded.mime_type)
    )


def build_video_part(client: genai.Client, source: str) -> types.Part:
    if source.startswith("http://") or source.startswith("https://"):
        if "loom.com" in source:
            local_path = resolve_loom_video(source)
            return upload_local_file(client, local_path)

        if "youtube.com" in source or "youtu.be" in source:
            return types.Part(file_data=types.FileData(file_uri=source))

        sys.exit(
            "Only YouTube and Loom URLs are supported directly. For any other hosted video "
            "(Vimeo, a direct file link), download it first and pass the local file path "
            "instead -- the Gemini API does not fetch arbitrary URLs."
        )

    if not os.path.exists(source):
        sys.exit(f"File not found: {source}")

    return upload_local_file(client, source)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source", help="Local video file path, a public YouTube URL, or a public Loom share URL"
    )
    parser.add_argument("--out", default="video-events.json", help="Output JSON path")
    parser.add_argument(
        "--model",
        default="gemini-2.5-flash",
        help="gemini-2.5-flash (default, cheaper) or gemini-2.5-pro (more careful read)",
    )
    parser.add_argument(
        "--media-resolution",
        default="default",
        choices=["default", "low"],
        help="'low' cuts cost roughly 3x but often can't read small on-screen text -- "
        "avoid for UI walkthroughs with field names/labels",
    )
    args = parser.parse_args()

    client = get_client()
    video_part = build_video_part(client, args.source)

    config_kwargs = {
        "response_mime_type": "application/json",
        "response_schema": EVENT_SCHEMA,
    }
    if args.media_resolution == "low":
        config_kwargs["media_resolution"] = "MEDIA_RESOLUTION_LOW"

    print(f"Analyzing with {args.model}...", file=sys.stderr)
    response = client.models.generate_content(
        model=args.model,
        contents=[video_part, PROMPT],
        config=types.GenerateContentConfig(**config_kwargs),
    )

    data = json.loads(response.text)
    with open(args.out, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Wrote {len(data.get('events', []))} events to {args.out}")


if __name__ == "__main__":
    main()
