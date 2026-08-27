#!/usr/bin/env python3
"""Small isolated faster-whisper runner used by ingest_interview_source.py."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from faster_whisper import WhisperModel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=Path)
    parser.add_argument("--model", default="small")
    args = parser.parse_args()
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(args.audio), vad_filter=True)
    payload = {
        "language": info.language,
        "languageProbability": info.language_probability,
        "segments": [
            {"start": segment.start, "duration": segment.end - segment.start, "text": segment.text}
            for segment in segments
        ],
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
