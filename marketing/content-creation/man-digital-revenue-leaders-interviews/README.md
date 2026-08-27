# MAN Digital Revenue Leaders Interviews

Creates and validates complete MAN Digital Revenue Leaders Interview posts as HubSpot blog drafts. It can start from a public YouTube video, copied Granola call, Markdown transcript, or reviewed copy while preserving the approved Figma structure and editorial safeguards.

## When to use it

Use this skill when creating, updating, or QA-checking a post in the `Revenue Leaders Interviews` series. It is specific to interview blog posts; it does not create the interview landing-page theme or replace the general blog-production workflow.

## Inputs

- Approved desktop and mobile Figma frames
- YouTube URL, Granola transcript/notes export, Markdown transcript, or reviewed answers
- Verified guest details, portrait, company information, and LinkedIn URL
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

`assets/carol-chen/` contains the tested Carol Chen draft example, including the intro, article body, CSS, LinkedIn SVG, and metadata contract. Its answers and unverified guest facts are visibly marked as draft placeholders and must not be published as quotations.

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

YouTube intake automatically captures captions, video metadata, a thumbnail/Open Graph candidate, and an optional embed. Granola and Markdown intake reports the guest image, LinkedIn URL, or Open Graph image that still needs to be supplied in the prompt.

## Prerequisites

- `man-digital-design-system` for brand decisions
- `man-digital-cms-pages` for HubSpot CMS source validation and uploads
- Native Chrome access for final live preview checks when available
- `yt-dlp` for public YouTube transcript and metadata intake
- Explicit authorization before creating a replacement campaign, scheduling, or publishing

Read `SKILL.md` for the complete workflow and hard gates.
