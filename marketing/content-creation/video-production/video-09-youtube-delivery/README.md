# video-09-youtube-delivery — Skill

Turns an approved video's subtitle file into the full set of upload-ready YouTube
subtitle tracks: a verbatim English track, a polished British-English track, and six
European-language translations, all filed for final delivery.

This is a **standalone post-approval skill, not a pipeline stage**. It never runs
automatically from the video pipeline — it starts only when Diogo says the video is
approved and asks for the YouTube subtitles.

## What does this skill do?

- Asks one mandatory gating question before anything else: **Shorts or long-form?**
  (Never inferred — a short horizontal video can look exactly like a Short and not be
  one. Only Diogo knows the mode.)
- Builds the **verbatim EN track**: words identical to the approved file, punctuation
  is the only permitted change. Non-native phrasing stays as spoken.
- Builds the **EN-GB track**: sentence-level, conservatively polished British English
  (grammar and idiom fixes, British spellings — never rewritten meaning, never
  compressed or "improved").
- Builds **six translations** — PL, DE, FR, ES (es-ES), PT-PT, UA (Ukrainian) — from
  the EN-GB sentence scaffold with full-context awareness, never cue-by-cue. A fixed
  English glossary (HubSpot, RevOps, MQL/SQL, CRM, etc.) stays untranslated in every
  language.
- Validates everything: timing checks, a hard words-match gate on the EN track, span
  alignment on translations, minimum cue durations so YouTube can't silently drop
  blink-length cues.
- Writes an **upload map** telling the uploader exactly which YouTube subtitle
  language to pick for each file (including the UA-not-UK trap for Ukrainian).

## When should I use it?

- Only after Diogo approves the video and names or points at the SRT to prepare.
- When asked to "upload to YouTube", "generate the YouTube subtitles", "make the
  language versions", or "translate the subtitles".
- Never mid-edit (approval implies the cut is final) and never as an automatic
  pipeline continuation — video-08 produces the review artifact for DaVinci; this
  skill produces the approved deliverables for YouTube. Different meaning, different
  destination.

## What inputs does it need?

- The **approved SRT** — typically the pipeline's
  `04_Project_Assets/Transcripts/<name> CORRECTED FLOW.srt`. If the sibling
  `CORRECTED.srt` exists, it is the punctuation source of truth; without it the skill
  runs in orphan mode on any bare SRT, reconstructing punctuation and flagging every
  genuinely ambiguous sentence boundary instead of guessing.
- Diogo's answer to the **Shorts vs long-form** question.
- Optionally, project-specific glossary terms to keep in English.

Input files are never modified, and the skill never writes into `04_Project_Assets/`.

## What does it produce?

Nine files in `06_Final_Delivery/Transcripts_&_Subtitles/`:

| File | Content |
|---|---|
| `<video> EN.srt` | Verbatim English, punctuated (the default/original track) |
| `<video> EN-GB.srt` | Polished British English (the translation pivot) |
| `<video> PL/DE/FR/ES/PT-PT/UA.srt` | Six sentence-level translations |
| `<video> — upload map.md` | File → YouTube language selection, plus mode and source used |

## Prerequisites

- Python 3 — all SRT operations run through `scripts/youtube_srt.py` (strip-tags,
  sentence rebuild, wrapping, validation subcommands). No external APIs or keys.
- The approved SRT accessible on disk, ideally inside a standard project folder so
  the sibling punctuation source and `06_Final_Delivery/` destination resolve.
- Diogo's explicit approval of the video — that approval is the trigger, not a
  detail.
