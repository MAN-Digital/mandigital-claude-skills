---
name: video-02-script-optimization
description: Reviews timecoded transcript exports from recorded video sessions and returns a cut decision sheet — what to remove, where the structure breaks, what needs checking by ear. Use this whenever a transcript CSV or export appears after a recording, or when the user says "review this cut", "tighten this", "what should I remove", "does this still work", "review the narrative", "here's the new export", or drops a second/later version of a transcript already under review. Also use for take selection, repetition removal, seam checking, cold-open selection, and runtime decisions on recorded footage. Also handles "lock the cut" / "lock it" — converting a finished decision sheet plus the user's branch decisions into a machine-executable CUT ORDER file for the video-03-cuts skill.
when_to_use: Any transcript export arriving after a recording. Any follow-up export of a file already reviewed. Requests about repetition, stumbles, restarts, duplicate takes, or whether a cut still makes sense. "Lock the cut" after decisions are made.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/diagnostics.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/json_to_rows.py *) Read Glob Grep Write
---

# Post-Recording Script Optimization

Full rules: `${CLAUDE_SKILL_DIR}/references/rulebook.md`. Read it when a case is not covered below.

## Transcript discovery — before asking the user for a file

Transcripts live at `<project root>/04_Project_Assets/Transcripts/`, named after the sequence (`<sequence name>.json`). Derive the project root from the open `.prproj` path — it sits at `<root>/03_Project_Files/Adobe/`. When no transcript path is given:

1. Look in that folder for `<active sequence name>.json` (word-level JSON preferred; then `.csv`).
2. Found → use it. Not found → ask the user to generate the transcript in Premiere (Text panel → Generate — not automatable, no public API) and export the JSON to exactly that path and name.
**Overwrite policy:** pulling a transcript overwrites `<sequence name>.json` for the same sequence — Premiere's internal transcript is the source of truth. Distinct sequences (e.g. the `_CUT_v1` duplicate) produce distinct filenames, so post-cut exports never collide with the original's.

3. **Auto-pull via the UXP bridge (PROVEN 2026-07-29, end to end):** when `transcript`-named MCP tools are present in the session (the server registers them because `PREMIERE_UXP_TOKEN` is set in the user-scope config), replace step 2's export ask with: probe `transcript.has` on the sequence's project item, pull via `transcript.export` (returns the full word-level JSON in the response), and save it to the template path yourself — the user only ever clicks Generate in the Text panel. Prerequisite on the Premiere side: the **UXP** "Premiere Pro MCP Bridge" panel must be loaded (via UXP Developer Tools; Premiere Settings → Plugins → developer mode ON) and connected to **`ws://localhost:7777/uxp`** — `localhost`, not `127.0.0.1`; Premiere 26.3's permission matcher rejects IP-literal origins. If the tools are absent or the panel is disconnected, fall back to asking for a manual export; never block on the bridge.

## The prime directive

You read text. The user hears audio. Every finding declares its tier.

- **Tier 1 — decide alone.** Text-verifiable: duplication, referential dependency, sentence boundaries, ordering against a source doc, promise/payload mismatch, enumeration counts, runtime arithmetic.
- **Tier 2 — propose, they decide.** Delivery-dependent: whether a clause ending on a comma lands, whether a pause reads as a full stop, which of two complete takes is better delivered. Give both branches, never one recommendation.
- **Tier 3 — never decide.** Whether a word is present in the audio. Predict, route as a listen-check, never write into the cut.

A Tier 3 item reported as a Tier 1 finding is a defect in your output even when the guess is right.

## Gate 1 — classify the export before reading it

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/diagnostics.py classify CURRENT.csv --source SOURCE.csv
```

Four states, and they change what everything downstream means:

| State | Means | Consequence |
| --- | --- | --- |
| **A** marked-up | rows deleted, media NOT cut | nothing lost, all source timecodes valid, cannot audition by playback |
| **B** rippled | timeline genuinely shortened | previously issued timecodes are VOID, re-conform any timing doc |
| **C** re-transcribed | ASR re-run, new row boundaries | earlier row indices void |
| **D** hand-corrected | user typed over the ASR | **locate strings from earlier passes no longer match, re-verify all** |

Report the state in one line before anything else. Never assume the previous export is still on disk; re-derive by diffing against the original source.

## Timing granularity — text carries the analysis, timestamps only carry boundaries

Accept three export formats, preferring the finest: **Premiere word-level JSON** > **SRT captions** > **row-level CSV**. All analysis (contests, seams, supersets) is text work and identical across formats — granularity only matters when a boundary becomes a number.

**The preferred input is Premiere's Transcript panel JSON export** (`{language, segments[], speakers[]}`, each segment carrying `words[]` with `start`, `duration`, `confidence`, `eos`, `tags`). It upgrades four things:

- **Sub-row boundaries are Tier 1.** Any sentence/clause boundary has an exact word-onset time — no interpolation, no marker seeds. Place cut points in the **silence gap** between words (previous word's `start+duration` → next word's `start`), not on the word onset itself.
- **`eos` flags** give explicit sentence segmentation — use them for seam boundary tests instead of inferring from punctuation.
- **`confidence`** drives Gate 2: low-confidence words are the ASR's own suspect list.
- **`tags: ["disfluency"]`** marks stumbles/filler machine-readably; distinct `speaker` ids separate off-mic chatter from takes.

The diagnostics scripts consume row CSVs — derive one from the JSON first and run them on that:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/json_to_rows.py TRANSCRIPT.json --fps 25 -o rows.csv
```
Row texts match Premiere's own CSV export; row *end* times are true speech ends (Premiere's CSV pads ends to abut the next row, hiding trailing silence) — expect end-time diffs when comparing against an old CSV, and treat the JSON's ends as correct.

With the state line, report granularity: word-level, or for row-only exports the median and max row duration — **coarse** when boundaries the cut needs fall inside rows longer than ~10s.

**When a needed boundary is sub-row and only a coarse export exists**, in this order:
1. Ask the user for the JSON export of the sequence — Premiere has word timing internally; the CSV discarded it.
2. If not available, **interpolate**: boundary position ≈ row start + (words before boundary / row word count) × row duration, weighted toward long words. Label it an ESTIMATE with ± tolerance (assume ±2s). Interpolated times are never Tier 1, never enter a CUT ORDER's Cuts table, and never appear without their tolerance. They ship as **marker seeds** (see cut lock) so the user nudges a pre-placed marker by ear instead of scrub-hunting the row.

## Gate 2 — an ungrammatical span is a transcription hypothesis, not a finding

This is the rule most likely to be skipped and the one whose absence does the most damage.

In the engagement this skill derives from, nine spans were flagged as possible transcription failures. **Nine out of nine were transcription failures, not delivery failures.** `for technical fit` was "Fourth thing: technical fit". `where we are processes` was "where we architect processes". `managed` was "MAN Digital".

Suspicion becomes near-certainty when the break sits at:

- an **ordinal or list-position word** (ASR fuses them into the following noun)
- a **brand, product, or domain term** (lower corpus frequency, higher failure rate)
- the **terminal word of a clause** (unstressed sentence-final words get clipped)
- a **numeral or unit bound** (`and €30,000.` missing its floor, `2000 to 10,000 a` missing "month")

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/diagnostics.py suspect CURRENT.csv --glossary glossary.json
```

With a word-level JSON in hand, rank suspects by the words' `confidence` field first — the ASR's own uncertainty is the primary suspect list, and the heuristics above catch what it was confidently wrong about. `disfluency` tags separate stumbles from content before the repetition scan.

Predict the true reading, batch as listen-checks, never write predictions into the cut. When one is confirmed, scan for siblings of the same class and batch them into one round trip.

**Referencing law:** the search string is the raw ASR text including its errors, because that is what the transcript panel searches. The correction rides beside it in brackets and never overwrites it.

## The passes, in order

**1. Diff against the previous export.**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/diagnostics.py diff PREVIOUS.csv CURRENT.csv
```
Classify every change: applied / applied-differently / not-applied / **new**. The "new" bucket is the regression report. Report it under a "what got worse" heading that is present even when empty.

**2. Repetition scan.**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/diagnostics.py repeats CURRENT.csv
```
Before scoring any take contest, scan the raw transcript for on-mic self-direction from the speaker ("let's cut this part", "I'll say that again"). It outranks your judgment on that decision.

Take contest tests, in order, stop at the first that discriminates: completeness → content superset → fluency density (rows per second; fragmentation proxies restarts) → concreteness → landing.

If a losing take holds exactly one idea the winner lacks, extract the clause. Do not keep the whole take.

**3. Seam classification.**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/diagnostics.py seams CURRENT.csv --source SOURCE.csv
```
Three verdicts only: **CLEAN** (report as a set, the user needs to know what they can ignore), **TRIM** (Tier 2, both branches), **BREAK** (Tier 1, restore spec with timecodes and verbatim text).

Three tests for any removal or lift:
- **A. Boundary** — full stop on both sides
- **B. Reference** — does anything after point back at what was removed
- **C. Structural load** — was it a bridge, a landing, a payoff, an antecedent

C is the one usually skipped and where the risk sits. Report C failures separately, since they need a replacement beat rather than a restore, and the replacement is often visual.

**4. Integrity audits.** Cheap, mechanical, catch what seam-by-seam reading structurally cannot.
- **Enumeration integrity** — count every announced list against what survives. Collateral loss is invisible at the seam and visible only in the count.
- **Promise/payload** — every quantifier creates a debt ("a few symptoms", "three models"). Audit delivery.
- **Asset misfiling** — sessions produce material for other outputs. Flag, name the correct destination, **never propose deletion**. Assume it was parked on purpose.

**5. Visual escape hatch.** Before recommending a cut or a pickup, ask whether an on-screen asset can carry the defect. Dropped numbers, unpaid promises, and missing ordinals are all cheaper to solve on screen. When one asset solves two problems at the same frame, say so.

**6. Narrative layer — only when seams are stable.** Findings here go stale whenever a block moves.
- Agenda audit: is every promised item delivered, in order
- Time to first stake: runtime before anything is at risk; flag above ~25%
- Section shape: rise-land vs rise-stop-reset
- Cold-open candidacy: strongest falsifiable, visualisable claim in the body, tested as frame one
- Deflating closers, self-sabotage lines near a CTA, outro audit

When the source is a reference document, the primary remedy is chapter markers, not restructuring.

## Output contract

1. Export state and runtime, one line
2. **Direct answer to whatever was asked, before anything else**
3. What closed since last pass
4. What is open, by severity: timecode, raw-verbatim locate string, tier, specific remedy
5. What got worse (heading always present)
6. Listen-checks, batched, with predicted readings
7. Runtime projection if open items are actioned

Verify every quoted string before shipping:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/diagnostics.py verify CURRENT.csv --strings strings.txt
```

## The cut lock — execution handoff to video-03-cuts

The decision sheet is for the human. The **CUT ORDER** is for the machine (the `video-03-cuts` skill driving the Premiere Pro MCP). They are never the same document, and the second is generated only through a decision gate:

**When to emit.** Only when every open item that touches a cut boundary is closed: all Tier-2 branches chosen by the user, and any Tier-3 listen-check that sits inside a kept region's first frame or adjacent to a cut point either confirmed or explicitly waived by the user. If the sheet has zero such items, offer the lock in the same pass. Otherwise emit only when the user says "lock the cut" / "lock it" / states their branch decisions — and if items remain unresolved, refuse and list exactly what is still open. Cosmetic listen-checks (domain-term ASR errors away from any seam) never gate the lock.

**What goes in.** Cuts whose boundaries are exact at the export's granularity: row boundaries always; sub-row cuts (mid-row clauses, stumble trims) ONLY when a word-level JSON supplies their times — then they are ordinary Tier 1 cuts, placed in silence gaps. From a row-level CSV alone, sub-row cuts CANNOT be placed — route them to Deferred as marker seeds, never approximate them to row boundaries. Splices and restores are always Deferred: they pull from the original sequence, which survives the cut.

**Format** — save as `<transcript basename>.cutorder.md` in the same folder as the transcript, and echo it in chat:

```markdown
# CUT ORDER — <video/project name>
locked: <date> · source_transcript: <filename> (export state <A-D>)
sequence: <sequence name, or "active sequence">
fps: <fps>
baseline_duration_seconds: <n>   # executor must abort if actual differs by more than one frame
expected_final_duration_seconds: <n>

## Cuts — execute top to bottom (pre-sorted descending, no rebasing needed)
| # | delete from (TC) | delete to (TC) | from_s | to_s | length_s |

## Fence
Execute ONLY the cuts above. No other edits of any kind.

## Marker seeds — place only after cuts pass audit (post-cut coordinates)
| label | post-cut TC | post_cut_s | tolerance_s | locate string (raw) |

## Deferred — do NOT execute
- <sub-row cuts pending marker nudge, splices, pickups>
```

**Marker seeds** are interpolated sub-row boundaries (or any position the user must verify by ear) expressed in **post-cut** coordinates — computed by subtracting the removed span lengths that precede each estimate. The executor places them as orange sequence markers after a passing audit; the user nudges them by ear; the cuts at those markers happen in a later pass. Omit the section when there are none. A seed never graduates to the Cuts table without the user confirming its exact position.

**Math law.** Every timecode converted to seconds at the stated fps, and the checksum must hold before shipping: `baseline − Σ length_s = expected_final`. State B exports: baseline is the rippled timeline, and say so on the baseline line.

## Post-cut verification (runs after video-03-cuts finishes)

Inputs: the executed CUT ORDER + the conformed word-level JSON of the cut sequence (pulled via the bridge or exported manually). This formalizes the verification that proved the first pipeline run:

1. **Content check** — every removed span's locate string absent from the cut transcript; every keeper (including take-winning ad-libs) present. Check against the CUT ORDER's removal spec, NOT its locate strings (locate strings quote context around a cut — building absence checks from them creates false alarms).
2. **Seam check** — the words on each side of every join read exactly as the cut order predicted.
3. **Duration check** — last word ends inside the expected final duration; transcript span matches the audit.
4. **Verdict + yellow markers.** Report pass/mismatch per check. Then emit a review-marker list for the premiere session to place as **YELLOW sequence markers** (color index 4), one per item needing human attention: cuts executed with no-silence or 1-frame-gap in-points (audition), pending listen-checks inside kept material, pickup insert points still unresolved, and any check that mismatched. Marker name = short imperative note ("audition: state→status trim"); comment = detail.

**Marker color taxonomy** (shared across the pipeline): GREEN = Diogo's own cut points · ORANGE = machine-estimated positions (seeds, GFX/pickup anchors) · YELLOW = machine review notes for Diogo's ear/eye.

## Never

- Emit a CUT ORDER while a gating branch or boundary listen-check is unresolved, or bury one inside a decision sheet
- Report an ungrammatical span as a content defect without applying Gate 2
- Issue timecodes without saying which export they are keyed to
- Reuse a locate string across exports without re-verifying
- Propose a cut for a defect the visual layer can carry
- Answer a narrow question with a broad analysis
- Report only problems; report the clean seams as a set
- Propose deleting anything that looks like a parked asset
- Pad a findings list, or treat runtime as a target rather than an outcome
