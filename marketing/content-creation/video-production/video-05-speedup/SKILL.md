---
name: video-05-speedup
description: Measures a talking-head sequence's words-per-minute from the transcript JSON, recommends a pitch-preserved speed-up (105-110%), and applies Diogo's SOP — clip speed without Maintain Audio Pitch, mono fill if needed, Pitch Shifter with speed-matched semitone/cents values — via the premiere-pro MCP where possible. Use when the user says "the pacing is slow", "speed up the video", "run the speedup", "check the wpm", or asks whether a cut should be delivered faster.
---

# Talking-Head Dialogue Speed-Up (Pitch-Preserved)

Implements the canonical SOP: `…/Video/04_Internal_SOPs/SOPs/SOP - Talking-Head Dialogue Speed-Up (Pitch-Preserved).md` (Google Drive). Read it when anything here is insufficient — the SOP wins on conflict. Rationale: Premiere's "Maintain Audio Pitch" time-stretch produces metallic artifacts on speech; this separates the time-stretch from the pitch correction.

A vendored copy of that SOP lives at `references/SOP - Talking-Head Dialogue Speed-Up (Pitch-Preserved).md` (self-containment pass, 2026-08-04): read the Drive original first — it is the living version and still wins on conflict — and fall back to the vendored copy when Drive is unreachable; after a successful Drive read that shows differences, refresh the vendored copy and say so.

## 1. Measure and recommend

From the sequence's word-level JSON: `wpm = word count / (last word end − first word start) × 60`.

**Target band: effective 140–165 wpm.** Grounding (verified July 2026): conversational English averages ~150 wpm (National Center for Voice and Speech); comfortable presentation pace is 140–160; TED talks average ~163–173 wpm; comprehension research puts the retention optimum at ~150–160 wpm with degradation past ~180. MAN Digital's audience is partly non-native English — the same reason blog copy targets Flesch-Kincaid 60–70 — so aim at the **low-to-middle of the band**, never above it.

Recommendation formula: `speed = min(1.10, 140 / measured_wpm)`, snapped down to the nearest SOP table row (103 / 105 / 108 / 110). Measured ≥ 140 → leave at 100%. The 1.10 cap is the SOP's artifact ceiling (clipped breathing, jittery gestures), not a comprehension limit — when even 110% cannot reach 140 wpm, say so explicitly and note the remainder is a **recording-pace item for the next shoot**, not something post can fix.

Report the measured wpm, the recommendation, and the projected runtime (`duration / speed`). The user picks the speed; **never exceed 110% for master edits**.

## 2. Speed → Pitch Shifter values (from the SOP, formula-verified)

| Speed | Semitones | Cents | Ratio |
|---|---|---|---|
| 103% | 0 | −51 | 0.97 |
| 105% | 0 | −84 | 0.95 |
| 108% | −1 | −33 | 0.93 |
| 110% | −1 | −65 | 0.91 |

Any other speed: `total cents = 1200 × log₂(1 ÷ speed)`, split into whole semitones + remaining cents; ratio = 1 ÷ speed. Always compute, never guess.

## 3. Execute

**Via MCP (attempt first, verify each step by read-back):**
1. Duplicate the sequence first (same rule as video-03-cuts — the pre-speedup cut is the rollback).
2. `speed_change` / `set_clip_speed_qe` on every dialogue clip: target speed, **maintain audio pitch OFF**, ripple ON. Verify: new duration = old ÷ speed (±1 frame per clip boundary).
3. Audio chain: if clips are **mono** (see `video-01-ingest`), skip the fill step entirely. If stereo with one recorded channel, the fill (Fill Left with Right / Fill Right with Left — the one that copies the *recorded* channel) is a Track Mixer insert, which the bridge CANNOT set (map-verified: track-level inserts are completely invisible to it) — hand it to the user as a manual step.
4. Pitch Shifter with the table values, Precision: High Precision, Pitch Settings: Individual Channels. Try `apply_audio_effect` per clip — **the capability map (`video-01-ingest/references/premiere-mcp-map.md`) records it as broken in 26.3** (`list_available_audio_effects` returns `[]`, so no audio effect can be applied), so EXPECT the manual path: hand the user the exact values as a manual checklist. The one cheap try stays because it self-detects a fixed bridge after an upgrade — a success there means the map needs updating, say so. Track-level insert (SOP default) is manual either way.
5. Report which steps ran automated vs. manual — never claim the audio chain is done without the pitch values actually applied.

**Track Mixer caveat (from the SOP):** track-level fill/pitch assumes every clip on that track shares the speed. Mixed speeds or music on the track → apply per-clip.

## 4. QC (from the SOP)

Play a dialogue-heavy section — natural voice, no chipmunk, no metallic swirl; meters show matched L/R if filled; gestures/blinks read naturally (they do at ≤110%). For hero clips where the Pitch Shifter isn't clean enough: Audition round-trip (iZotope Radius, stretch locked-pitch) per the SOP.

## Sequencing laws

- **This is the LAST timeline operation.** It voids every timecode: transcripts, cut orders, marker positions, cue sheets. Run after spine cut and pause-pass.
- Graphics cue derivation happens AFTER speedup, on a fresh transcript export of the sped sequence (or rebase existing cues by ÷speed and say so).
- Never stack with a previous speedup — check clip speed is 100% before applying; if not, compute the compound and warn.
