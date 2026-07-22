# MAN Digital YouTube Scripts — Skill

Writes YouTube video scripts in Romeo's direct, fact-first voice and MAN Digital's
documented positioning — grounded in real source material and examples, not generic
marketing theory.

## What it does

- Asks two mandatory questions before writing anything: shorts or long-form, and
  tutorial/promotional/case study.
- Writes a fresh script from a topic or brief.
- Or transforms ("brain-dump mode") a pasted transcript from another video — usually a
  HubSpot tutorial screen-share — into MAN Digital's own narration over the same footage,
  without translating it line-by-line.
- Enforces a hard word/phrase blocklist and a non-native-speaker readability standard (short,
  single-idea sentences meant to be read aloud, not silently).

## When to use it

Any time you're asked to write a YouTube script for MAN Digital or Romeo — tutorial,
promotional, or case-study, shorts or long-form — including adapting another company's video
into MAN Digital's own version.

## Inputs

- A topic or brief, **or** a pasted transcript/script from another video to adapt.
- Answers to the two gating questions (the skill asks for these itself if missing).

## Output

A complete, ready-to-record script structured per
[`references/script-templates.md`](references/script-templates.md), following the voice and
blocklist rules in `references/`.

## Prerequisites

None required to run. For full grounding depth (real client case-study data, the full
positioning canvas/ICP docs), this skill reads MAN Digital's private `openclaw-infra` repo
if your environment has it checked out — see
[`references/voice-and-positioning.md`](references/voice-and-positioning.md) for the exact
paths and the fallback behavior when that repo isn't available.

## Files

- `SKILL.md` — the Claude-readable spec (steps, gating questions, self-check table).
- `references/voice-and-positioning.md` — MAN Digital's positioning ladder, ICP, and Romeo's
  actual voice calibration sentences.
- `references/banned-words.md` — the absolute word/phrase blocklist.
- `references/non-native-readability.md` — sentence-writing rules with before/after
  rewrites, for a presenter reading the script aloud in a second language.
- `references/script-templates.md` — structures for shorts/long-form × tutorial/promotional/
  case-study, plus the brain-dump transcript-transform workflow.
