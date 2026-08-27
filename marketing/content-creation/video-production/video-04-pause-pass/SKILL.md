---
name: video-04-pause-pass
description: Tightens long pauses in a talking-head Premiere sequence so breathing room stops delaying content — analyzes inter-word silence from the word-level transcript JSON, emits a CUT ORDER of micro-trims, and optionally a punch plan that masks each jump cut by alternating a simulated second-camera crop (Motion scale + Y). Use when the user says "tighten the pauses", "clean the breathing spaces", "pause pass", "remove dead air", "the video drags", or asks to speed up delivery without changing the content.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/gap_analysis.py *) Read Glob Grep Write
---

# Pause Pass — tighten breathing without killing delivery

Runs on the **conformed word-level JSON** of an already-cut sequence. Produces a standard CUT ORDER (executed by `video-03-cuts` under the full duplicate/back-to-front/audit protocol) plus, optionally, a **punch plan** that masks the resulting jump cuts.

When execution questions about the Premiere bridge arise (what a tool actually does,
what lies): the capability map at `video-01-ingest/references/premiere-mcp-map.md`
(folded in 2026-08-06) is authoritative.

## Philosophy

Pauses under ~1s are delivery, not defect — sentence landings need their beat. This pass never deletes silence to zero (that's the machine-gun feel of Premiere's native pause tool); it *tightens* long gaps to a residual. Jump cuts are acceptable in online formats; masked jump cuts are better. The user vetoes individual trims — a pause after a punchline may be load-bearing.

## Parameters (defaults, user-overridable per run)

| parameter | default | meaning |
|---|---|---|
| threshold | 1.0s | only gaps at or above this are touched |
| eos residual | 0.7s | pause left after a sentence end (`eos` flag) |
| mid residual | 0.4s | pause left mid-sentence (hesitations) |
| mask policy | auto-punch | `auto-punch` / `broll-flag` / `none` |

Mid-sentence gaps are the priority targets (they read as hesitation); sentence-end gaps are the ones to be conservative about.

## Procedure

1. **Analyze:**
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/gap_analysis.py CUT_SEQUENCE.json --threshold 1.0 --eos-residual 0.7 --mid-residual 0.4 --fps 25
   ```
   Output is frame-snapped, descending, CUT ORDER-ready, with seam words per trim.
2. **Present the trim list for veto** — every row shows `word → word` and gap type. The user strikes any trim whose pause is doing rhetorical work. Report total reclaimable time and projected runtime.
3. **Emit a CUT ORDER** (same format and rules as the video-02-script-optimization cut lock: baseline check, checksum, fence, descending). Name it `<sequence>.pausepass.cutorder.md` beside the transcript. With mask policy `auto-punch`, append the Punch plan section (below). With `broll-flag`, list each seam in Deferred as a graphics-coverage note instead.
4. Hand to `video-03-cuts` for execution.

## Punch plan — masking jump cuts as a simulated second camera

After the trims, the surviving segments alternate between two framings, so each seam reads as a camera change instead of a skip:

```markdown
## Punch plan — apply after audit passes
alternation: wide → tight → wide … (segment 1 = wide)
mode: shot-change   wide: Scale 100, Position (1920, 1080)   tight: Scale 130, Position (1920, 1144)
| segment (final s) | state | scale | position |
```

Two modes — default **shot-change**:

- **shot-change (default; last calibrated 2026-07-28, studio talking-head framing):** the tight state is a genuine B-camera close-up. **Wide = Scale 100, Position (1920, 1080) · Tight = Scale 130, Position (1920, 1144).** Adjust **Position only, never Anchor Point** (stays 1920, 1080). Scale 130 in a UHD-in-UHD sequence is interpolated upscale — accepted for YouTube delivery.
- **none:** leave every seam an unmasked jump cut — legitimate online grammar, and per the 30-degree rule (below) better than a timid punch.
- **micro-punch (Scale 103–105) exists only on explicit user request, with this warning attached:** it violates the 30-degree principle — consecutive shots of the same subject must differ *substantially* in size or angle, or the cut reads as an error. Perceptually, big change > no change > small change: a 130 close-up reads as a B-camera, a plain jump cut reads as intentional grammar, but a barely-different frame reads as a stutter. Never offer micro-punch as the recommendation.

Rules:
- Alternation covers **all** seams in the final timeline — including seams inherited from the spine cut, which are also unmasked jump cuts. List every surviving segment.
- Segments shorter than ~1.5s don't flip state (a 1s "camera change" reads as a glitch) — extend the current state across them and note it.
- **First-seam confirmation, EVERY session** — the right tight values are footage-dependent (framing, headroom), so never roll stored defaults blind. Apply the tight state to the FIRST seam only, ask the user whether the stored values hold for this footage or need adjusting, and only then roll the confirmed values across the plan. If they changed, record the new values here as the current defaults.
- Executor applies it via `set_clip_scale` / `set_clip_position` (or `set_clip_properties`) per segment and verifies by read-back — values are absolute, so any manual test framings get overwritten. The CUT ORDER fence for a video-04-pause-pass order reads: "Execute ONLY the cuts and the punch plan listed."

## Sequencing laws

- Run **after** the spine cut, on the conformed JSON of the cut sequence.
- Run **before** video-05-speedup (speed changes void every timecode in this analysis) and before graphics cue derivation.
- After execution, the sequence needs a fresh transcript export for any further transcript-keyed work.

## Never

- Delete a pause to zero, or touch gaps below threshold
- Ship a trim without its seam words for veto
- Emit punch values that haven't been calibrated on this framing at least once
- Run on a raw session export — that's video-02-script-optimization's job
