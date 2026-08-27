# video-04-pause-pass — Pause Pass

Tightens overlong pauses in a talking-head Premiere sequence so breathing room stops
delaying content — without flattening delivery. Pipeline stage 04: runs after the spine
cut (video-02 decisions, executed by video-03) is locked and executed, and before
video-05-speedup.

## What does this skill do?

- Analyzes inter-word silence in the **conformed word-level transcript JSON** of the
  already-cut sequence, using `scripts/gap_analysis.py`.
- Only touches gaps at or above a threshold (default 1.0 s), and never deletes a pause
  to zero — long gaps are tightened to a residual (default 0.7 s after a sentence end,
  0.4 s mid-sentence). Pauses under ~1 s are treated as delivery, not defect.
- Emits a standard **CUT ORDER** of frame-snapped micro-trims (descending, checksummed,
  fenced — same format as the video-02 cut lock), executed downstream by video-03-cuts
  under its duplicate/back-to-front/audit protocol.
- Optionally appends a **punch plan** that masks the resulting jump cuts by alternating
  a simulated second-camera framing (Motion Scale + Position, e.g. wide Scale 100 vs
  tight Scale 130) across the surviving segments. Default mode is shot-change; `none`
  leaves intentional jump cuts; micro-punch (Scale 103–105) exists only on explicit
  request and ships with a 30-degree-rule warning.

## When should I use it?

- After the spine cut is executed, when the video still drags: "tighten the pauses",
  "clean the breathing spaces", "pause pass", "remove dead air", or any request to speed
  up delivery without changing the content.
- **Never** on a raw session export — dead air between takes is the spine cut's job
  (video-02-script-optimization).
- Always **before** video-05-speedup and before graphics cue derivation: a speed change
  voids every timecode this analysis produces.

## What inputs does it need?

- The conformed **word-level transcript JSON** of the cut sequence (fresh export from
  Premiere after the spine cut was executed).
- Optional per-run overrides for threshold, end-of-sentence residual, mid-sentence
  residual, and mask policy (`auto-punch` / `broll-flag` / `none`).
- Two user decisions are built in:
  - **Trim veto** — every proposed trim is presented with its seam words
    (`word → word`) and gap type; the user strikes any pause doing rhetorical work
    (e.g. after a punchline) before the CUT ORDER is emitted.
  - **First-seam punch confirmation, every session** — the tight framing values are
    footage-dependent, so the tight state is applied to the first seam only and
    confirmed (or recalibrated) by the user before rolling across the plan.

## What does it produce?

- `<sequence>.pausepass.cutorder.md` beside the transcript — the CUT ORDER, plus the
  punch plan section (mask policy `auto-punch`) or per-seam graphics-coverage notes in
  Deferred (mask policy `broll-flag`).
- A report of total reclaimable time and projected runtime.
- Handoff to video-03-cuts for execution. After execution, the sequence needs a fresh
  transcript export before any further transcript-keyed work.

## Prerequisites

- **Upstream artifact:** a locked and executed spine cut, with the word-level transcript
  JSON exported from the conformed sequence.
- **python3** — runs `scripts/gap_analysis.py` for the gap analysis.
- **video-03-cuts** (and its premiere-pro MCP server connection) downstream — this skill
  plans the trims and the punch; video-03 performs the timeline edits and applies the
  punch values (`set_clip_scale` / `set_clip_position`) with read-back verification.
- Studio talking-head framing for the stored punch defaults (last calibrated
  2026-07-28); other framings need the first-seam recalibration.
