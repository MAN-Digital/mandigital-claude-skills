# video-02-script-optimization — Post-Recording Script Optimization

Stage 3 of the video pipeline (after ingest and transcript, before cuts). Reviews timecoded
transcript exports of recorded sessions and returns a cut **decision sheet** for the human —
then, at the user's "lock the cut", converts the decided sheet into a machine-executable
**CUT ORDER** file for the video-03-cuts skill.

## What does this skill do?

- Classifies every export before reading it (marked-up / rippled / re-transcribed /
  hand-corrected), because each state changes what timecodes and locate strings still mean.
- Runs ordered analysis passes via `scripts/diagnostics.py`: diff against the previous
  export, repetition and take-contest scan, seam classification (CLEAN / TRIM / BREAK),
  integrity audits (enumeration counts, promise/payload debts, asset misfiling), and — once
  seams are stable — the narrative layer (agenda, cold-open candidacy, closers).
- Applies a strict evidence discipline: every finding declares its tier. Tier 1 is
  text-verifiable and decided alone; Tier 2 is delivery-dependent, so both branches go to the
  user; Tier 3 (whether a word is actually in the audio) is only ever routed as a
  listen-check. Ungrammatical spans are treated as transcription hypotheses first (Gate 2),
  not delivery failures.
- Prefers Premiere's word-level JSON export, converting it to row CSVs for the diagnostics
  scripts (`scripts/json_to_rows.py`); can auto-pull the transcript over the UXP bridge when
  the session has the `transcript.*` tools.
- **User-decision gate ("lock the cut"):** a CUT ORDER is emitted only when every gating
  Tier-2 branch is chosen and every boundary listen-check is confirmed or waived — otherwise
  it refuses and lists exactly what is still open. Interpolated sub-row boundaries never
  enter the Cuts table; they ship as marker seeds for the user to nudge by ear.
- After video-03 executes, runs the post-cut verification: content, seam, and duration checks
  against the conformed transcript, plus a YELLOW review-marker list.

## When should I use it?

Whenever a transcript export appears after a recording, or a follow-up export of a file
already under review arrives. Requests about repetition, stumbles, restarts, duplicate takes,
take selection, cold-open selection, seam checking, runtime decisions — and "lock the cut" /
"lock it" once decisions are made.

## What inputs does it need?

- A transcript export of the working sequence, preferring **Premiere word-level JSON** over
  SRT over row-level CSV. Discovery is automatic: `<sequence name>.json` in
  `<project root>/04_Project_Assets/Transcripts/`, or pulled via the UXP bridge; failing
  both, the user is asked to export it there.
- The previous export (for the diff pass) and, when ordering matters, the source document.
- The user's branch decisions and listen-check confirmations before any lock.

## What does it produce?

- A decision sheet following the output contract: export state and runtime, the direct answer
  first, what closed, what is open by severity (timecode + raw locate string + tier +
  remedy), a "what got worse" section, batched listen-checks, and a runtime projection.
- On lock: `<transcript basename>.cutorder.md` next to the transcript — baseline and expected
  durations with a checksum, a pre-sorted descending Cuts table, a fence, marker seeds in
  post-cut coordinates, and a Deferred section video-03 must not execute.
- Post-cut: a pass/mismatch verification verdict plus the YELLOW marker list.

## Prerequisites

- **python3** (standard library only) for `scripts/diagnostics.py` and
  `scripts/json_to_rows.py`; `references/rulebook.md` and `references/glossary.json` ship
  with the skill.
- A transcript generated in Premiere's Text panel — generation itself is a **manual user
  click** (no public API).
- Optional, for auto-pull: the **premiere-pro MCP server** with `PREMIERE_UXP_TOKEN` set and
  the UXP "Premiere Pro MCP Bridge" panel connected to `ws://localhost:7777/uxp`
  (`localhost`, not `127.0.0.1`). Falls back to a manual export ask — never blocks on the
  bridge.
- Downstream: the CUT ORDER is consumed by **video-03-cuts**.
