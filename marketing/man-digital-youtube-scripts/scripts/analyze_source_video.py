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

NOTE: this script has not been run against a live API key or a real video in
this environment. It follows Gemini's documented File API and structured-
output patterns, but SDK parameter names have shifted between google-genai
versions before -- verify on a short sample clip before relying on it.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load ../.env (the skill folder root, next to .env.example) if present.
# An already-exported shell variable always wins -- load_dotenv() never
# overrides an existing os.environ value.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

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


def build_video_part(client: genai.Client, source: str) -> types.Part:
    if source.startswith("http://") or source.startswith("https://"):
        if "youtube.com" not in source and "youtu.be" not in source:
            sys.exit(
                "Only YouTube URLs are supported directly. For any other hosted video "
                "(Loom, Vimeo, a direct file link), download it first and pass the local "
                "file path instead -- the Gemini API does not fetch arbitrary URLs."
            )
        return types.Part(file_data=types.FileData(file_uri=source))

    if not os.path.exists(source):
        sys.exit(f"File not found: {source}")

    print(f"Uploading {source} to Gemini's File API...", file=sys.stderr)
    uploaded = client.files.upload(file=source)

    # Video processing is asynchronous -- poll until it's ACTIVE before referencing it.
    while uploaded.state.name == "PROCESSING":
        time.sleep(3)
        uploaded = client.files.get(name=uploaded.name)

    if uploaded.state.name != "ACTIVE":
        sys.exit(f"Upload did not become ACTIVE (state: {uploaded.state.name}).")

    return types.Part(
        file_data=types.FileData(file_uri=uploaded.uri, mime_type=uploaded.mime_type)
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Local video file path or a public YouTube URL")
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
