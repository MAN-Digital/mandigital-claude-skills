# MAN Digital YouTube Scripts — Skill

Writes YouTube video scripts in Romeo's direct, fact-first voice and MAN Digital's
documented positioning — grounded in real source material and examples, not generic
marketing theory.

## What it does

- Asks two mandatory questions before writing anything: shorts or long-form, and
  tutorial/promotional/case study.
- Writes a fresh script from a topic or brief.
- Or transforms ("brain-dump mode") a pasted transcript, source video file, or YouTube URL
  from another video — usually a HubSpot tutorial screen-share — into MAN Digital's own
  narration over the same footage, without translating it line-by-line.
- For a real source video (not just typed transcript text), can run it through Gemini's
  video-understanding API to ground the walkthrough sequence in the actual footage instead
  of a guessed one — see `references/video-grounded-storyboard.md`.
- Enforces a hard word/phrase blocklist and a non-native-speaker readability standard (short,
  single-idea sentences meant to be read aloud, not silently).
- Delivers the finished script as **two separate files**, never one: a teleprompter Reader
  Script and a Visual Cue Sheet for the video editor, synced by verbatim anchor quotes.

## When to use it

Any time you're asked to write a YouTube script for MAN Digital or Romeo — tutorial,
promotional, or case-study, shorts or long-form — including adapting another company's video
into MAN Digital's own version.

## Inputs

- A topic or brief, **or** a pasted transcript/script from another video to adapt.
- Answers to the two gating questions (the skill asks for these itself if missing).

## Output

Two files, per [`references/output-export-contract.md`](references/output-export-contract.md):
a teleprompter Reader Script (zero visual references) and a Visual Cue Sheet for the video
editor (timecodes, anchors, what's on screen). Never delivered as one merged file.

## Prerequisites

None required for a fresh-mode or transcript-based script. For full grounding depth (real
client case-study data, the full positioning canvas/ICP docs), this skill reads MAN
Digital's private `openclaw-infra` repo if your environment has it checked out — see
[`references/voice-and-positioning.md`](references/voice-and-positioning.md) for the exact
paths and the fallback behavior when that repo isn't available.

**Only for video-grounded storyboard mode** (analyzing a real source video, not just a
transcript):

- Python 3 with `pip install -r scripts/requirements.txt` (`google-genai` + `python-dotenv`)
- A Gemini API key — get one free at `https://aistudio.google.com/apikey`
- See [`references/video-grounded-storyboard.md`](references/video-grounded-storyboard.md)
  for cost notes and known limits (this script hasn't been run against a live video in this
  environment yet — verify it on a sample clip first).

### Setting up your API key

The script looks for `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) as an environment variable. Set
it up **one of two ways** — pick whichever fits how you work:

**Option 1 — shell profile (persists across every terminal and Claude Code session):**

```bash
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.zshrc   # or ~/.bashrc if you use bash
source ~/.zshrc
```

**Option 2 — a local `.env` file scoped to just this skill:**

```bash
cd marketing/man-digital-youtube-scripts   # this skill's folder
cp .env.example .env
# open .env and paste your real key after GEMINI_API_KEY=
```

The script loads this `.env` automatically (via `python-dotenv`) — no export needed. `.env`
is covered by this folder's own `.gitignore`, so it can't be committed by accident even if
you copy this skill folder somewhere else.

**Either way:**

- Never paste a real key into `SKILL.md`, any `references/*.md` file, `.env.example`, or a
  commit message — those are all version-controlled and, for this skill, public.
- If you ever paste a key into chat with an AI assistant by mistake, revoke it at
  `https://aistudio.google.com/apikey` and generate a new one.
- Everyone on the team installing this skill needs their own key set up this way before
  video-grounded storyboard mode will run — there's no shared/embedded key.

## Files

- `SKILL.md` — the Claude-readable spec (steps, gating questions, self-check table).
- `references/voice-and-positioning.md` — MAN Digital's positioning ladder, ICP, and Romeo's
  actual voice calibration sentences.
- `references/banned-words.md` — the absolute word/phrase blocklist.
- `references/non-native-readability.md` — sentence-writing rules with before/after
  rewrites, for a presenter reading the script aloud in a second language.
- `references/script-templates.md` — structures for shorts/long-form × tutorial/promotional/
  case-study, plus the brain-dump transcript-transform workflow.
- `references/output-export-contract.md` — the two-file (Reader Script + Cue Sheet) output
  shape and export/QA process.
- `references/video-grounded-storyboard.md` — how to ground the Cue Sheet in an actual
  source video using Gemini's video-understanding API.
- `scripts/analyze_source_video.py` + `requirements.txt` — the Gemini video-analysis script.
- `.env.example` — documents the `GEMINI_API_KEY` variable name; never contains a real key.
