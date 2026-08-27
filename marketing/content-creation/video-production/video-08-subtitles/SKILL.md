---
name: video-08-subtitles
description: Subtitle QA and delivery pass — cross-references the DaVinci Resolve SRT caption export against the Premiere Pro transcript JSON (per-word confidence), fixes caption mistakes with evidence, and builds a punctuation-free FLOW version with sentence-clean cuts and no mid-sentence caption gaps. Use when the user says "check the subtitles", "fix the captions", "caption QA", "cross-reference the transcript", "clean the srt", "make the flow version", "remove the dots and commas", "extend the subtitles", "no mistakes in the captions", or when a DaVinci .srt and a Premiere transcript .json for the same cut are both present.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*) Read Glob Grep Write
---

# Subtitle QA & Flow — two ASR engines, one correct caption file

The 08↔09 boundary, stated once (Diogo, 2026-08-04): **this skill makes the review
captions for the edit suite** — CORRECTED + FLOW SRTs that go back into DaVinci on the
conformed, pre-approval cut. **video-09 makes everything YouTube needs after approval** —
the multi-language subtitle tracks and the optimization package (title, description,
tags, first comment). Both produce .srt files; different lifecycle moment, different
destination. Approval is the border: before it, this skill; after it, video-09.

Two independent speech-to-text engines transcribed the same audio: DaVinci (in the styled SRT)
and Premiere (in the transcript JSON, with per-word `confidence`). They disagree exactly where
one of them is wrong — align them, arbitrate every difference with confidence + context, and
almost the whole QA pass needs no listening at all.

**DaVinci is the base and the deliverable.** The caption template lives in DaVinci — responsive,
word-by-word as narrated, visually interesting — and cannot be replicated in Premiere yet
(revisit someday). The Premiere JSON is *evidence*: confidences for arbitration and word
timestamps for cut timing. Never swap these roles: empirically DaVinci wins ~180 of ~220
disputes (v7 baseline, 2026-08-01).

## Inputs

| file | from | notes |
|---|---|---|
| `*.json` transcript | Premiere: Text panel → Transcript → ⋯ → Export → JSON | word-level `start`/`duration`/`confidence`; the tail may carry outro takes past the SRT end — the aligner isolates them, disregard |
| `*.srt` captions | DaVinci: timeline with the caption track → Export Subtitle | inline style tags (currently `<b><font color='#ff0000'>`) ride along from the export — preserved byte-exact through Stage A/B editing, stripped from deliverables in Stage C (the DaVinci track template owns the look — Diogo, 2026-08-03) |

Sanity: first spoken word within ~0.2 s in both files; drift stays ≤ ~0.2 s throughout when the
cuts really match. If it doesn't, one export is from a stale timeline — stop and re-export.

## Procedure

### Stage A — CORRECTED.srt (the QA reference, punctuation intact)

1. **Align:**
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/align_report.py TRANSCRIPT.json "CAPTIONS.srt" > report.txt
   ```
2. **Review every diff section** with the arbitration rules below. Build the edit spec
   `Transcripts/_srt build scripts/<ver> edits.json` — `edits` (old→new inner text, must match
   exactly once), `retime`, `inserts` (new timed blocks), `forbid` (residue strings that must
   not survive, e.g. the misspellings found). The spec IS the review output and the per-project
   artifact; scripts are generic.
3. **Apply + validate:**
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/apply_edits.py "CAPTIONS.srt" "<ver> edits.json" "CAPTIONS CORRECTED.srt"
   ```
   Validation is built in (unique matches, wrapper integrity, timing sanity, width law,
   residue). Then re-run `align_report.py` against the corrected file — matched words must go
   UP and every disappeared diff must be an intended fix.
4. **Write the changelog** (`<name> CORRECTED — changelog.md` beside the SRTs): fixes table
   with timestamps, restored-words list, polish list, ⚑ flags, deliberately-not-changed note.

### Stage B — FLOW version (the delivery file)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/flow_build.py "CAPTIONS CORRECTED.srt" TRANSCRIPT.json "CAPTIONS CORRECTED FLOW.srt"
```

What it does, in order — defaults chosen 2026-08-02, all CLI-overridable:

1. **Sentence-clean cuts** — any block where a sentence ends mid-caption is split at the
   boundary, cut time from the JSON word timestamps (character-proportional where the engines
   diverge). Pieces ≥ 0.24 s — matching the template's own single-word pop rhythm.
2. **Punctuation strip** — prose commas and sentence-final dots removed. KEPT: question marks
   (they carry meaning on screen; `--strip-questions` exists if Diogo asks), thousands
   separators (2,750), apostrophes, hyphens, URL dots (man.digital/blog).
3. **Gap closure** — mid-sentence caption gaps always close (the caption extends until the next
   starts; no blank frames inside a running sentence). Sentence-boundary gaps ≥ 0.5 s are
   deliberate breathing pauses and STAY caption-free (each kept pause is listed). The script
   prints the gap histogram first — read it: a post-pause-pass timeline normally has only
   jitter gaps and comes out fully contiguous.
4. **Hard guarantee** — word content is verified identical to CORRECTED before writing.
   FLOW changes punctuation, cuts, and timing. Never words.

### Stage C — de-tag the deliverables (2026-08-03)

The DaVinci subtitle-track template owns all styling (font, colour, bold), so the SRT that
goes back into DaVinci — and everything filed as a deliverable — carries no inline tags:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/detag.py "CAPTIONS CORRECTED.srt" "CAPTIONS CORRECTED FLOW.srt"
```

Runs after Stage B and after every flag-verdict rebuild (in-place, idempotent,
structure-validated). Tags still exist during Stages A/B — the raw DaVinci export carries
them, `apply_edits.py`'s wrapper-integrity validation runs on the styled text, and
`edits.json` inner-text matching is unchanged. Only the filed deliverables go clean.

### Deliverables & naming

`<orig> CORRECTED.srt` · `<orig> CORRECTED FLOW.srt` · `<orig> CORRECTED — changelog.md` ·
`_srt build scripts/<ver> edits.json` — all beside the source exports in
`04_Project_Assets/Transcripts/`. After flag verdicts: update the spec, re-run Stage A then
Stage B — seconds, deterministic. FLOW always regenerates from CORRECTED; never hand-edit
either output.

## Arbitration rules (Stage A review)

- **Default: DaVinci stands.** Change it only with evidence.
- **Engine error signatures.** DaVinci flubs *names and homophones*: brand/jargon garbling
  (HOPSPOT, Mando Digital, XQL, ARK, filmographic) and sound-alikes (builds/bills, feels/peels,
  insurance/assurance, quality/quarterly, government's/governance, free/pre, chose/choose).
  Premiere drops *small words* (articles, conjunctions, "CFO" after "your") and butchers terms
  (MKL, sea level, Read, room, tear, arrows, held, stress, centrist in). Match the error type
  to the engine before deciding.
- **Confidence:** a Premiere word at conf 1.00 that DaVinci lacks was probably really spoken —
  restore it. Premiere conf < 0.7 → trust DaVinci. Both agreeing ≈ what was said, even when it
  reads oddly (then flag, don't change).
- **Skipped clauses:** DaVinci sometimes drops a whole spoken clause during a long caption hold
  (~3 s on 3 words is the tell). Restore as new timed block(s) using JSON word times.
- **Fillers stay dropped:** sentence-start "So"/"But", stutters, false starts Premiere heard
  are normal caption cleanup — keep them out.
- **Brand & jargon glossary** (grep the final file for violations; extend per project):
  HubSpot · MAN Digital · man.digital/blog · MQL / SQL (never MKL/XQL/SQA) · RevOps ·
  ARC model · firmographic · C-level · SDRs · pre-sales · go-to-market · lifecycle (one word) ·
  mid-market · "peel the onion".
- **Numbers:** thousands separators (30,000 not "30 000"/"30000"); keep the spoken currency
  wording ("100 euro" stays, don't invent "€100").
- **⚑ Flag, don't guess:** coin-flips (both readings grammatical, meaning differs), brand
  spellings needing Diogo (ARC vs ARK), restored clauses worth an ear check, and oddities both
  engines agree on. Every flag: timestamp + current pick + alternative. The flags section is
  part of the deliverable, not an afterthought.

## The two template laws (violating either breaks the look)

- **Width law:** the template renders ONE line, max width = the export's own measured maximum
  (currently 18 chars). Never exceed it; never merge words across blocks to fix spelling
  ("sales people" stays split — "salespeople" is 21). Rebalance words across neighboring
  blocks with JSON-timed boundaries instead, or revert the cosmetic fix.
- **Rhythm law:** minimum caption duration = the export's own floor (0.119 s exists in v7).
  New pieces target ≥ 0.24 s; short single-word pops are the template's style, not a defect.

## Sequencing laws

- Runs LAST: after video-03 cuts, video-04 pause pass, video-05 speedup — any retime voids
  every timecode in both exports. Fresh exports after ANY timeline change.
- The caption template must already be applied in DaVinci (SRT carries its inline tags).
- Re-import: DaVinci Media Pool → Import Subtitle onto the caption track; the track style
  governs the look either way since the inline tags mirror it. SRT is the right round-trip
  format — no DaVinci export carries word confidences, so nothing better exists.

## Never

- Treat Premiere as default-correct — it is the evidence, DaVinci is the base
- Change content words in FLOW, or ship it without the word-identity check passing
- Exceed the measured line width, or merge words across caption blocks
- Hand-edit a generated SRT — fix the edit spec and rebuild
- Strip question marks unless Diogo explicitly asks
- Silently resolve a coin-flip — flag it with timestamp
- Close a sentence-boundary gap ≥ 0.5 s (breathing pauses are deliberate) or leave a
  mid-sentence gap open
- Ship without running the validations, or ignore a failed one
