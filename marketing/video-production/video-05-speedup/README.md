# video-05-speedup — Talking-Head Dialogue Speed-Up (Pitch-Preserved)

Measures a sequence's delivery pace in words per minute, recommends a modest
pitch-preserved speed-up, and applies Diogo's SOP for it in Premiere. Pipeline stage 05:
the **last timeline operation** — after all cuts and the pause pass, before graphics cue
derivation.

## What does this skill do?

- Computes the sequence's wpm from the word-level transcript JSON
  (`word count / speaking span × 60`) and compares it against the target band of
  **140–165 effective wpm**, aiming low-to-middle because MAN Digital's audience is
  partly non-native English.
- Recommends a speed via `min(1.10, 140 / measured_wpm)`, snapped down to the nearest
  SOP table row (103 / 105 / 108 / 110%). Measured ≥ 140 wpm → stays at 100%. When even
  110% can't reach 140 wpm, it says so and marks the remainder as a recording-pace item
  for the next shoot — not something post can fix.
- Implements the canonical SOP (Google Drive:
  `…/Video/04_Internal_SOPs/SOPs/SOP - Talking-Head Dialogue Speed-Up (Pitch-Preserved).md`):
  clip speed **without** Maintain Audio Pitch (which produces metallic artifacts on
  speech), then a Pitch Shifter correction with speed-matched semitone/cents values from
  the SOP table (e.g. 105% → 0 st / −84 cents; any other speed is computed, never
  guessed).
- Executes via the premiere-pro MCP where possible — duplicate the sequence first (the
  rollback), `speed_change` / `set_clip_speed_qe` per dialogue clip with ripple on, then
  verify by read-back — and hands the user an exact manual checklist for whatever the
  bridge can't set (track-level inserts, effect parameters, stereo channel fill).
- Finishes with the SOP's QC pass (natural voice, no chipmunk or metallic swirl, matched
  meters, gestures reading naturally at ≤110%).

## When should I use it?

- After all cuts and pause passes are done — "the pacing is slow", "speed up the video",
  "run the speedup", "check the wpm", or any question about delivery pace.
- As the LAST timeline operation: it voids every timecode (transcripts, cut orders,
  markers, cue sheets), so graphics cue derivation (video-07) happens afterwards on a
  fresh transcript export of the sped sequence (or existing cues are rebased by ÷speed,
  stated explicitly).
- Never stack speedups — clip speed is checked to be 100% first; if not, the compound is
  computed and flagged.

## What inputs does it need?

- The sequence's **word-level transcript JSON** (for the wpm measurement).
- The Premiere project open with the sequence, reachable via the premiere-pro MCP.
- **The user's speed pick** — the skill reports measured wpm, its recommendation, and
  the projected runtime, but the user chooses the speed. Hard cap: never above 110% for
  master edits.

## What does it produce?

- The wpm measurement, speed recommendation, and projected runtime report.
- A duplicated, sped-up sequence with the audio chain applied (or the exact Pitch
  Shifter / channel-fill values as a manual checklist where the MCP bridge can't set
  them).
- An honest automated-vs-manual step report — it never claims the audio chain is done
  unless the pitch values were actually applied.

## Prerequisites

- **premiere-pro MCP server** connected to the open project (manual fallback documented
  for the steps the bridge can't drive).
- **Upstream artifacts:** all cuts (video-03) and the pause pass (video-04) executed,
  plus a word-level transcript JSON of the conformed sequence.
- Mono audio prep from **video-01-ingest** lets the channel-fill step be skipped
  entirely; stereo clips with one recorded channel need the manual fill insert.
- The canonical SOP document on Google Drive — read when anything in the skill is
  insufficient; the SOP wins on conflict.
