---
name: man-digital-youtube-scripts
description: Use when writing a YouTube video script for MAN Digital or Romeo Man — tutorials, promotional videos, or case studies, in shorts or long-form, either from a fresh topic/brief or by transforming ("brain dump" mode) another video's transcript or source video into MAN Digital's own narration over similar footage. Delivers a teleprompter Reader Script and a synced Visual Cue Sheet for the video editor.
---

# MAN Digital YouTube Script Creation

## Overview

Writes YouTube scripts in Romeo's direct, fact-first operator voice and MAN Digital's
documented positioning. Two triggers: (1) a topic/brief for a NEW script, or (2) a pasted
transcript/script from another video to TRANSFORM into MAN Digital's own narration over
similar footage (brain-dump mode — about 90% of these are HubSpot tutorial screen-shares).
Every instruction in this skill is backed by a concrete before/after example, not theory.

## Step 1 — Ask before writing anything (mandatory, every time)

Do not draft a single line until both are answered:

1. **Shorts or long-form?**
2. **Tutorial, promotional, or case study?**

If it's fresh mode and no topic/brief exists yet, ask for that too. Use the AskUserQuestion
tool if it's available; otherwise ask directly in chat.

Skipping this produces a script in the wrong length and format — the reader has to redo it.
This happens even to a careful writer who guesses: a baseline test on this exact task
defaulted to a 15-minute tutorial with a full production shot-list nobody asked for, purely
because the format was never confirmed.

## Step 2 — Determine the mode

- **Fresh mode**: user gives a topic/brief → write from scratch.
- **Brain-dump mode**: user pastes another video's transcript/script, or hands you an actual
  source video file/YouTube URL → go to
  [references/script-templates.md](references/script-templates.md), "Brain-dump transform
  mode." Never translate line-by-line — identify what's actually happening on screen, then
  re-narrate it the way MAN Digital would explain it. If a real video file or YouTube URL is
  provided (not just typed transcript text) and it has many on-screen frames, read
  [references/video-grounded-storyboard.md](references/video-grounded-storyboard.md) first —
  it grounds the walkthrough sequence and the Cue Sheet in the actual footage instead of
  guessed screen actions.

## Step 3 — Ground the voice and positioning

Read [references/voice-and-positioning.md](references/voice-and-positioning.md) before
drafting. It has MAN Digital's real positioning ladder, the ICP, and Romeo's own voice
calibration sentences (quoted verbatim from his writing) — not an invented "RevOps
consultancy" tone.

## Step 4 — Write for a non-native speaker reading aloud

Read [references/non-native-readability.md](references/non-native-readability.md). Core
rule: one idea per sentence, 8–15 words, no stacked clauses, no rhetorical questions to
camera.

## Step 5 — Enforce the word blocklist

Read [references/banned-words.md](references/banned-words.md). Scan the finished draft
against every entry before delivering it. The list is absolute — no exceptions, no softened
variants of the same word.

## Step 6 — Use the right structure

Read [references/script-templates.md](references/script-templates.md) for the shorts /
long-form × tutorial / promotional / case-study structures.

## Step 7 — Deliver two files, not one

Read [references/output-export-contract.md](references/output-export-contract.md) before
delivering anything. Every script ends as **two separate files**: Document A (Reader
Script — teleprompter-only, zero visual references) and Document B (Visual Cue Sheet — the
video editor's storyboard, synced to Document A by verbatim anchor quotes). Never merge them
into one file. Run the file's §7.6 pre-export checklist before delivering.

## Quick reference — self-check before delivering

| Check                                               | Rule                                                         |
| --------------------------------------------------- | ------------------------------------------------------------ |
| Clarifying questions asked first                    | shorts/long-form + tutorial/promo/case-study                 |
| Every claim backed by a concrete example            | no unsupported theory or generic statements                  |
| Sentence length                                     | 8–15 words, one idea each                                    |
| Rhetorical or audience-directed questions           | zero — state the fact instead                                |
| Hedging words (might, could, maybe, seems, perhaps) | zero — direct claims only                                    |
| Passive voice                                       | zero — active voice only                                     |
| Conditionals ("if you...", "imagine if")            | zero                                                         |
| Blocklist words                                     | zero — cross-check references/banned-words.md                |
| Triplet overuse ("X, Y, and Z" repeated)            | vary list length/structure across the script                 |
| Third-party case studies                            | never — use MAN Digital's own client work only               |
| Output                                              | two separate files (Reader Script + Cue Sheet), never merged |
| Reader Script contains a visual reference           | zero — export failure, see output-export-contract.md §7.6    |

## Common mistakes

- Writing the full script before asking the two format questions.
- Merging the Reader Script and Visual Cue Sheet into one file, or letting a `[VISUAL]`
  marker or timecode leak into the Reader Script — the reader will say it out loud.
- Sentences with 2+ embedded clauses or em-dash asides — unreadable aloud for a non-native
  speaker, even when they read fine silently on a page.
- Rhetorical hooks ("Sound familiar?", "Pretty slick, right?") — these are banned
  question-forms even when they feel like natural filler.
- Copying a brain-dump transcript's structure and phrasing instead of re-deriving MAN
  Digital's own angle on the same screen actions.
- Falling back to generic "RevOps consultancy" voice instead of the specific positioning in
  references/voice-and-positioning.md.
- Repeating the same "one X, one Y, and one Z" triplet sentence pattern more than once or
  twice in a script — it reads as AI-written and it's harder to deliver smoothly out loud
  than it looks on the page.
