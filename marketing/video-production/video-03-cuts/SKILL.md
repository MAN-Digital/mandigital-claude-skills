---
name: video-03-cuts
description: Executes timeline cuts in Adobe Premiere Pro via the premiere-pro MCP server, following a strict safety protocol (duplicate first, back-to-front execution, mandatory read-back audit). Use whenever the user asks to execute cuts, apply a cut decision sheet, ripple delete ranges, split clips, or "make the cuts" in Premiere — including cut sheets produced by the video-02-script-optimization skill and cuts derived from green clip markers. Also use when the user says "run the cuts", "apply the cut sheet", "cut at my markers", or hands over timecodes to remove from a sequence.
when_to_use: Any request to perform destructive timeline edits in Premiere via MCP. Cut-sheet execution after video-02-script-optimization. Marker-driven cutting.
---

# Premiere Cut Execution Protocol

Executes cut decisions on a Premiere timeline through the `premiere-pro` MCP server. The mechanical tools work; the failure mode is **model arithmetic and rationalization**, not the bridge. This protocol exists because a July 2026 test over-deleted ~40s of keep-content and then invented false math to justify the result. Never let that happen again.

**Bridge capability map: `video-01-ingest/references/premiere-mcp-map.md`** (folded in
2026-08-06) — which tools lie or destroy, pinned to PPro 26.3. Two entries matter most
here: `ripple_delete`'s single-track semantics on layered timelines, and the proven
multi-track range-cut path (target-all → in/out → `extract_selection`, duration-delta
as the sync detector, ranges executed descending — frame-exact on 11 tracks,
2026-08-05). Consult the map before cutting anything with more than one track.

## Prime directives

1. **Never edit the original sequence.** Always `duplicate_sequence` first, work on the copy (`set_active_sequence` to it). The original is the rollback.
2. **Narration is untrusted — only read-backs count.** After editing, verify with fresh reads. If actual ≠ expected, STOP and report the discrepancy. Never explain away a mismatch; an unexpected result is an error until proven otherwise.
3. **Execute cuts back-to-front** (highest timecode first). Earlier positions never shift, so no rebasing arithmetic is ever needed. Sort the cut list descending by start time before touching the timeline.

## Input contract

The preferred input is a **CUT ORDER** file produced by the video-02-script-optimization skill's cut lock (`<transcript basename>.cutorder.md`, recognizable by its `# CUT ORDER` header). It arrives pre-sorted descending with a baseline check, per-cut seconds, an expected final duration, and a fence — execute exactly it: the Cuts table only, never the Deferred section.

**Refuse raw decision sheets.** If handed a cut *decision sheet* (open Tier-2 branches, listen-checks, A/B options) or any input containing unresolved choices, do not execute and do not resolve the choices yourself. Tell the user to lock it first: answer the open items in the video-02-script-optimization session and say "lock the cut", which produces the CUT ORDER file. Ad-hoc cut lists dictated directly by the user (plain timecodes, marker-driven requests) are fine — the refusal applies only to documents with decisions still open.

If the CUT ORDER's `baseline_duration_seconds` does not match the actual timeline within one frame, STOP before duplicating anything — the order was locked against a different timeline state (likely already-rippled media or the wrong sequence) and every timecode in it is suspect.

## Procedure

### 1. Baseline (before any edit)
- `get_timeline_summary` + `get_full_sequence_info`: record sequence name, id, total duration, clip list with start/end times, track layout.
- Confirm frame rate. Diogo's projects are **25 fps**: `seconds = HH*3600 + MM*60 + SS + FF/25`.
- Write out the cut list in absolute original-timeline seconds, sorted **descending**.
- Compute `expected_final_duration = baseline_duration − Σ(range lengths)` and the expected surviving clip map (which clips survive, as how many pieces, at what final positions). Show this table to the user BEFORE cutting.

### 2. Duplicate
- `duplicate_sequence`, then rename the copy by **incrementing the version suffix**. Diogo's timelines end in `_vN` (e.g. `2026-07-21_ManDigital_BlogHubSpotContractsObject_16x9_v1`): strip the trailing `_vN`, replace with `_v(N+1)` — so `..._16x9_v3` duplicates to `..._16x9_v4`. If a sequence with that name already exists anywhere in the project, keep incrementing until the name is free. If the source name has no `_vN` suffix at all, append `_v2` and mention the anomaly to the user. Then `set_active_sequence` to the copy.
- **Respect the bin template.** Diogo's projects use a template bin structure where working timelines live in `00_Timelines/01_Active_Cuts`. After duplicating, locate the copy in the project panel (`find_project_item_by_name` on the new `_vN` name) and check its bin. If it did not land in `01_Active_Cuts`, move it there with `move_item_to_bin` (find the bin via `get_bin_contents` / `find_project_item_by_name` on `01_Active_Cuts`). If the project has no such bin (non-template project), leave the copy where Premiere put it — never create bins uninvited. Verify the move with a read-back of the bin contents.
- Re-read `get_timeline_summary` to confirm the active sequence is the copy (match by id, not name).

### 3. Execute (descending order)
For each cut range, working from the latest to the earliest:
- `split_clip` at range end, `split_clip` at range start, then `ripple_delete` the enclosed range.
- "Delete everything before X" = split at X, ripple delete 0→X. "Delete everything after X" = split at X, delete X→end.
- After each range, `get_timeline_summary` and check the duration dropped by exactly that range's length (±0.04s = 1 frame at 25fps). On mismatch: STOP immediately, report, do not attempt the remaining ranges.

### 4. Audit (mandatory, never skipped)

(Step 5, post-execution, follows a PASSING audit only.)
- `get_full_sequence_info`: actual final duration and clip list.
- Diff against the step-1 expectation table: duration delta, surviving clips, piece counts.
- Report the audit table to the user. Only after it matches, `save_project`.
- **Retire the pre-cut original.** After the audit passes and the project is saved, move the source sequence (the one that was duplicated) from `01_Active_Cuts` to `00_Timelines/05_Old_&_Unused_Timelines` via `move_item_to_bin`, so only the live cut sits in `01_Active_Cuts`. Verify with a bin-contents read-back and mention the move in the report. Never do this before the audit passes — until then the original IS the rollback and stays put. Skip silently if the project lacks the template bins.
- If it does not match: report exactly what differs, and offer `undo` (repeat as needed) or deleting the new `_vN` copy — the original is untouched either way.

### 5. Post-execution (after a passing audit + save)

1. **Archive the superseded timeline.** Move the pre-cut original sequence into the `05_Old_&_Unused_Timelines` bin (`move_item_to_bin`; create the bin if the project lacks it). Never delete it — it is the rollback and the splice source.
2. **Pull the conformed transcript of the cut sequence** via the UXP bridge (`transcript.has` → `transcript.export` on the cut sequence's project item) and save it as `<cut sequence name>.json` in `<project root>/04_Project_Assets/Transcripts/` (overwrite same-name; distinct sequence names prevent collisions). If the bridge is unavailable, ask the user for a manual export to that exact path — don't block.
3. **Hand off to video-02-script-optimization's post-cut verification** (content, seams, duration against the CUT ORDER), then place the YELLOW review markers it returns (sequence markers, color index 4 — yellow = machine review notes; orange = machine-estimated positions; green = the user's own cut points). Report the verification verdict with the audit table.

## Marker seeds (from a CUT ORDER)

A CUT ORDER may carry a `## Marker seeds` section: estimated sub-row boundaries in **post-cut** coordinates with a ± tolerance. Only after the audit passes, place each as an **orange sequence marker** (`add_marker`, color index 3) at its `post_cut_s`, named with its label, comment carrying the locate string and tolerance. Report the placed markers with the audit table. Never cut at a seed — the user nudges each marker by ear first, then requests the cut in a later pass ("cut at my markers"). Orange = machine-estimated, unverified; the user's own cut markers are green — never confuse the two.

## Punch plan (from a video-04-pause-pass CUT ORDER)

A CUT ORDER may carry a `## Punch plan` section: per final segment, an alternating wide/tight state with a scale and Δy (a simulated second camera masking the jump cuts). Execute it only after the audit passes: `set_clip_properties` (Motion scale, and position when Δy ≠ 0) on each listed segment, then verify every segment's properties by read-back and report the applied table. For such orders the fence reads "cuts + punch plan" — the punch plan is in-scope, everything else stays out. If the plan's values are marked uncalibrated, apply to the FIRST tight segment only, stop, and ask the user to tune scale/Δy by eye before rolling it across the timeline.

## Marker-driven cuts ("cut at my markers")

Diogo places **green clip markers** at intended cut points; they sit ~1 frame after the true cut point. These are markers on the project item (source), read via `find_project_item_by_name` → `get_clip_markers` with `item_id`. Positions are in **source time**: convert to timeline time via the clip's timeline start and in-point from `get_full_clip_info` before using them. Confirm the derived cut list with the user before executing — markers mark points; the user must say which side of each point dies.

Clip markers live on the source item, so they survive timeline deletion and stay addressable by `item_id` even after their clip is cut out. To recolor: delete + re-add at the same source position (no update tool for clip markers).

## Known traps

- `split_clip` (QE razor) can silently no-op on Premiere 26.3 — verify every split with a read-back before relying on it. The reliable alternative, proven on a full 9-cut run (July 2026): set sequence in/out around the range and extract. Prefer it.
- Clearing sequence in/out points via the bridge fails on Premiere 26.3 (parameter bug). Leftover in/out marks are harmless; tell the user Option+X clears them.
- `ripple_delete` behavior at clip boundaries: always create both split points explicitly first; never assume range-granularity.
- Multiple audio tracks follow the video ripple only if track sync is intact — verify audio clip counts in the audit, not just video.
- The bridge executes ExtendScript with `Result: OK` even when the *edit logic* was wrong — OK means "script ran", not "edit correct". Only the audit proves correctness.
- Premiere's undo stack covers MCP edits: `undo` tool or Cmd+Z both work for recovery.
