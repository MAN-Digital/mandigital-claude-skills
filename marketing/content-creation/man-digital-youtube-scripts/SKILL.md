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

Three scripts Romeo rewrote himself and then read fluently on camera are the calibration
standard for this skill: see
[references/golden-samples.md](references/golden-samples.md). When any rule here feels
ambiguous, match those samples.

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
  source video file/YouTube/Loom URL → go to
  [references/script-templates.md](references/script-templates.md), "Brain-dump transform
  mode." Never translate line-by-line — identify what's actually happening on screen, then
  re-narrate it the way MAN Digital would explain it. If a real video file, YouTube URL, or
  Loom URL is provided (not just typed transcript text) and it has many on-screen frames, read
  [references/video-grounded-storyboard.md](references/video-grounded-storyboard.md) first —
  it grounds the walkthrough sequence and the Cue Sheet in the actual footage instead of
  guessed screen actions.

## Step 3 — Ground the voice and positioning

Read [references/voice-and-positioning.md](references/voice-and-positioning.md) before
drafting. It has MAN Digital's real positioning ladder, the ICP, and Romeo's own voice
calibration sentences (quoted verbatim from his writing) — not an invented "RevOps
consultancy" tone.

## Step 4 — Fact-check with online research (mandatory, twice)

This runs in two passes, and both are required:

**Pass 1 — before drafting.** Verify every product fact the script will state — feature
names, where the feature lives in the UI, plan/tier requirements, beta status, permissions.
Use web search or current HubSpot docs; a brain-dump source video may be months old and
wrong.

**Pass 2 — after the draft is finished.** Go back online and re-verify the *finished
script*, claim by claim: every date, number, price, feature name, UI location, and factual
statement that made it into the final text. Drafting introduces facts that were never part
of Pass 1 — examples get invented, numbers get rounded, settings paths get paraphrased.
Nothing ships until every checkable claim in the delivered text has been confirmed current
and factual. Fix or flag anything that fails — never leave a stale fact in and never
silently drop a claim (use the Flags section of the output contract).

Real failure this rule exists for: a delivered script said price books live "under
Commerce." Commerce Hub had been rebranded to Revenue Hub about a month earlier. Romeo
caught it mid-recording and the take was lost. His instruction on set: "Fact-check
everything from this script with research."

Always state in the script, near the start of the walkthrough:

- Which plan/tier the feature needs ("Price books require Revenue Hub Professional or
  Enterprise").
- Whether it's a beta and what to do if the viewer doesn't see it ("If you don't have it,
  request the beta").
- Any permission gate ("Only a Super Admin can edit this").

## Step 5 — Write for a non-native speaker reading aloud

Read [references/non-native-readability.md](references/non-native-readability.md). Core
rules: one idea per sentence, 8–15 words, no stacked clauses, no idioms, no insider jargon,
plain complete sentences — not clipped aphorisms.

## Step 6 — Give an instant concrete example for every abstract term

This is a term-level rule, not just a claim-level rule. The moment the script names an
abstract concept, the next line makes it concrete. Romeo, on set: "If you see something
plain — theory — give an example. For each and every element."

❌ "Use one naming pattern across all books."
✅ "Use one naming pattern across all books. For example: 'Direct - UK - GBP' and
'Partners - Germany - EUR.'"

❌ "That new company is a referral customer."
✅ "That new company is a referral customer. They came through someone who knows your
business."

❌ "Multi-market teams build one book per market."
✅ "Multi-market teams build one book per market. For example: DACH, Benelux, Scandinavia,
Latin America."

❌ "A messy library causes problems."
✅ "A messy library has duplicates and unclear names. For example: 'Onboarding,'
'Onboarding New,' and 'Onboarding Final.'"

Terms that always need this treatment: any segment name, any naming convention, any
"clean/messy" judgment, any market or region reference, any HubSpot object or setting the
viewer may not know. In tutorials, also show the finished artifact at the end (the completed
price book, the finished workflow) — note it in the Cue Sheet.

## Step 7 — Enforce the word blocklist

Read [references/banned-words.md](references/banned-words.md). Scan the finished draft
against every entry before delivering it. The list is absolute — no exceptions, no softened
variants of the same word.

## Step 8 — Use the right structure

Read [references/script-templates.md](references/script-templates.md) for the shorts /
long-form × tutorial / promotional / case-study structures.

## Step 9 — Deliver into the Drive project folder

Read [references/output-export-contract.md](references/output-export-contract.md) before
delivering anything. Every script ends as **two separate documents** — Document A (Reader
Script — teleprompter-only, zero visual references) and Document B (Visual Cue Sheet — the
video editor's storyboard, synced to Document A by verbatim anchor quotes) — never merged.
Physically that is five files: `ReaderScript.txt` (the only file the prompter loads),
`ReaderScript.pdf` (review copy), `CueSheet.md`, `CueSheet.pdf` (rendered twin), and
`readme.txt` (source video link, full source transcript, fact-check status).

All four are filed into the Drive Video project tree (§7.4 of the export contract): reuse
the topic's project folder if one exists, otherwise copy the pristine
`[ New Project Template ]` into `01_Active_Projects/`, rename it
`YYYY-MM-DD_ManDigital_{{Topic}}` (HubSpot source material → `Hubspot`-prefixed topic, e.g.
`HubspotBillingPortal`), and place the files in
`01_Pre_Production/Storyboards_&_Scripts/`.

The Reader Script's teleprompter layout (max two lines per chunk, blank line between
chunks, visible enumeration markers, chapter separators) is defined there and is a hard
requirement — Romeo stops recording when it's violated. Run the file's §7.6 pre-export
checklist before delivering.

## Quick reference — self-check before delivering

| Check                                               | Rule                                                         |
| --------------------------------------------------- | ------------------------------------------------------------ |
| Clarifying questions asked first                    | shorts/long-form + tutorial/promo/case-study                 |
| Product facts verified by research (Pass 1)         | feature names, UI location, tier, beta status, permissions   |
| Finished draft re-verified online (Pass 2)          | every date, number, price, and claim in the final text       |
| Every abstract term followed by a concrete example  | term-level, inline, "For example: …"                         |
| Sentence length                                     | 8–15 words, one idea each                                    |
| Idioms and insider jargon                           | zero — no "earns its keep," no "bow tie" without explanation |
| Audience-directed questions ("Sound familiar?")     | zero — structural self-answered questions are allowed        |
| Hedging words (might, maybe, seems, perhaps)        | zero — direct claims only; "may/can" OK for real possibility |
| Passive voice                                       | zero — active voice only                                     |
| Hypothetical conditionals ("imagine if", "what if") | zero — real branching "if" (system states) is allowed        |
| Self-deprecating asides ("I know it's boring, but") | zero — Romeo refuses to read them                            |
| Blocklist words                                     | zero — cross-check references/banned-words.md                |
| Triplet overuse ("X, Y, and Z" repeated)            | vary list length/structure across the script                 |
| Company intro / mid-video selling                   | zero — no "We are MAN Digital…" block; one soft CTA at end   |
| Chunk size in Reader Script                         | max 2 lines, then a blank line — no exceptions               |
| Enumerations                                        | one item per line, spoken ordinal marker ("One: …")          |
| Third-party case studies                            | never — use MAN Digital's own client work only               |
| Output                                              | 5 files (ReaderScript.txt+.pdf, CueSheet.md+.pdf, readme.txt), never merged |
| Filed on Drive                                      | project folder from pristine template → Storyboards_&_Scripts |
| Reader Script contains a visual reference           | zero — export failure, see output-export-contract.md §7.6    |

## Common mistakes

- Writing the full script before asking the two format questions.
- Skipping the research pass and repeating a stale product fact from the source video
  (the Commerce → Revenue Hub rebrand was missed exactly this way).
- Merging the Reader Script and Visual Cue Sheet into one file, or letting a `[VISUAL]`
  marker or timecode leak into the Reader Script — the reader will say it out loud.
- Fat paragraphs: 3+ lines with no blank line between chunks. The reader loses his place,
  has no time to breathe, and stops the take. Max two lines per chunk.
- Enumerations buried in prose ("four groups: identity, dates, ownership, risk") instead of
  one item per line with a visible "One: / Two: / Three:" marker.
- Idioms ("earns its keep") and insider jargon ("the right side of the bow tie") — a
  non-native reader can't parse the idiom mid-scroll, and the audience doesn't know the
  jargon. Four consecutive takes died on "earns its keep."
- Clipped telegraphic phrases ("Today, three things." / "What this object actually
  changes") — they read as robotic and confuse the reader. Write the full natural sentence:
  "In today's video, let's talk about what this object changes inside your HubSpot."
- Narrating demo footage impersonally ("The example names it referral customers") — say
  "In the example shown here, …" so the reader knows he's talking over a screen recording.
- Sentences with 2+ embedded clauses or em-dash asides — unreadable aloud for a non-native
  speaker, even when they read fine silently on a page.
- Audience-directed rhetorical hooks ("Sound familiar?", "Pretty slick, right?") — banned.
  Structural teaching questions the narrator answers himself ("First, what is a tax rate
  library? It is one list of the taxes your team uses.") are allowed and encouraged.
- Copying a brain-dump transcript's structure and phrasing instead of re-deriving MAN
  Digital's own angle on the same screen actions.
- Falling back to generic "RevOps consultancy" voice instead of the specific positioning in
  references/voice-and-positioning.md.
- Repeating the same "one X, one Y, and one Z" triplet sentence pattern more than once or
  twice in a script — it reads as AI-written and it's harder to deliver smoothly out loud
  than it looks on the page.
