# MAN Digital Revenue Leaders Interviews

Creates and validates complete MAN Digital Revenue Leaders Interview posts as HubSpot blog drafts. It can start from a public YouTube video, copied Granola call, Markdown transcript, or reviewed copy while preserving the approved Figma structure and selecting 7–8 questions that fit the source.

## When to use it

Use this skill when creating, updating, or QA-checking a post in the `Revenue Leaders Interviews` series. It is specific to interview blog posts; it does not create the interview landing-page theme or replace the general blog-production workflow.

## Inputs

- Approved desktop and mobile Figma frames
- YouTube URL, Granola transcript/notes export, Markdown transcript, or reviewed answers
- Guest details, portrait, company information, and a LinkedIn candidate URL to verify with Apollo.io or Exa
- HubSpot access for saving and reviewing the draft
- The canonical `Revenue Leaders Interviews` campaign and tag

## Outputs

- Scoped intro, article HTML, and post-specific CSS
- Normalized source manifest and question-by-question evidence map
- Optional responsive privacy-enhanced YouTube embed
- A complete HubSpot draft with SEO and Open Graph metadata
- Automatic association with the canonical `Revenue Leaders Interviews` campaign
- Static validation results and responsive HubSpot preview QA

## Included example

`assets/carol-chen/` contains the tested Carol Chen draft example, including the intro, article body, CSS, LinkedIn SVG, metadata contract, evidence map, and cross-source LinkedIn identity record. It demonstrates eight complete source-adapted questions, a clean full-width video embed, and internal draft-state tracking without reader-facing generation notices.

## Validation

From this skill directory, run:

```bash
python3 scripts/test_ingest_interview_source.py
python3 scripts/test_validate_interview.py
python3 scripts/validate_interview.py assets/carol-chen
```

To normalize a source before drafting:

```bash
python3 scripts/ingest_interview_source.py SOURCE --output work/guest-name
```

YouTube intake uses `youtube-transcript-api` first, `yt-dlp` captions second, and an opt-in local `faster-whisper` fallback. It captures captions, video metadata, a thumbnail/Open Graph candidate, provider history, and an optional privacy-enhanced embed. Granola and Markdown intake reports the guest image, LinkedIn URL, or Open Graph image that still needs to be supplied in the prompt.

## Prerequisites

- `man-digital-design-system` for brand decisions
- `man-digital-cms-pages` for HubSpot CMS source validation and uploads
- Native Chrome access for final live preview checks when available
- Apollo.io no-credit people search or Exa people search for guest identity verification
- `uv`/`uvx`, or preinstalled `youtube-transcript-api` and `yt-dlp`, for public YouTube intake
- CPU/disk capacity for the optional `--whisper-fallback`; it is never triggered silently
- Explicit authorization before creating a replacement campaign, scheduling, or publishing

Read `SKILL.md` for the complete workflow and hard gates.
