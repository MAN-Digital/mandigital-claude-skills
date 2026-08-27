# video-03-cuts — Premiere Cut Execution Protocol

Stage 4 of the video pipeline: the executor. Takes the CUT ORDER locked by
video-02-script-optimization (or an ad-hoc cut list) and performs the destructive timeline
edits in Adobe Premiere Pro via the premiere-pro MCP server, under a safety protocol built
after a July 2026 test over-deleted ~40s of keep-content and rationalized the result.

## What does this skill do?

- **Duplicate-first safety protocol:** never edits the original sequence. It duplicates,
  increments the `_vN` version suffix, files the copy into `00_Timelines/01_Active_Cuts`,
  and works only on the copy — the original is the rollback.
- Executes cuts **back-to-front** (highest timecode first, so earlier positions never shift),
  as split → split → ripple delete, checking the duration drop after every range and
  stopping immediately on any mismatch.
- Trusts only read-backs, never its own narration: a mandatory post-execution audit diffs
  actual duration, surviving clips, and piece counts against the expectation table shown to
  the user before cutting. Only a passing audit is followed by save, archiving the pre-cut
  original to `05_Old_&_Unused_Timelines`, a conformed transcript pull, and the handoff to
  video-02's post-cut verification (whose YELLOW review markers it places).
- Places a CUT ORDER's marker seeds as **orange** sequence markers after a passing audit —
  never cutting at a seed; the user nudges each by ear first.
- Executes a video-04 pause-pass punch plan (Motion scale / position per segment) when the
  CUT ORDER carries one, first-segment-only if uncalibrated.
- Handles marker-driven cutting from Diogo's **green clip markers**, converting source-time
  marker positions to timeline time and confirming the derived cut list before executing.
- Works around known Premiere 26.3 traps: silent `split_clip` no-ops (prefers the proven
  in/out extract method), the unclearable in/out bug, and the bridge's `Result: OK` meaning
  "script ran", not "edit correct".

## When should I use it?

Any request to perform destructive timeline edits in Premiere via MCP: "run the cuts",
"apply the cut sheet", "make the cuts", "cut at my markers", ripple-deleting ranges, or
executing the CUT ORDER produced by video-02's cut lock. It **refuses raw decision sheets** —
any document with open Tier-2 branches or unresolved listen-checks is sent back to video-02
to be locked first; only ad-hoc cut lists dictated directly by the user bypass that.

## What inputs does it need?

- Preferred: a **CUT ORDER** file from video-02 (`<transcript basename>.cutorder.md`) —
  pre-sorted descending, with a baseline duration the live timeline must match within one
  frame (otherwise it stops before touching anything), an expected final duration, and a
  fence limiting execution to the Cuts table.
- Alternatively: plain timecodes from the user, or green clip markers plus the user's answer
  on which side of each point dies.
- The target sequence open in Premiere (25 fps in Diogo's projects).

## What does it produce?

- A new `_v(N+1)` cut sequence in `01_Active_Cuts`; the untouched pre-cut original archived
  to `05_Old_&_Unused_Timelines` after the audit passes (kept as rollback and splice source,
  never deleted).
- The pre-cut expectation table and the post-cut audit table reported to the user.
- The conformed transcript of the cut sequence saved as `<cut sequence name>.json` in
  `<project root>/04_Project_Assets/Transcripts/` (via the UXP bridge, or a manual-export
  ask).
- Orange marker-seed placements, YELLOW review markers from the verification handoff, and —
  when present — the applied punch-plan table.

## Prerequisites

- The **premiere-pro MCP server** connected to a running Premiere Pro (CEP bridge for edits;
  the UXP WebSocket bridge on `ws://localhost:7777/uxp` for the conformed transcript pull —
  optional, with a manual-export fallback).
- Upstream: a CUT ORDER locked by **video-02-script-optimization**, unless the user dictates
  cuts directly.
- The MAN Digital template bin structure for filing (skipped silently when absent — bins are
  never created uninvited).
