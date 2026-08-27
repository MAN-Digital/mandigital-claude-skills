# video-00-pipeline — Video Pipeline Conductor

Orchestrates MAN Digital's full video edit: it chains the stage skills video-01 through
video-08 in order (ingest → transcript → script optimization → cuts → pause pass → speedup →
graphics → subtitles), detects where a project stands from its on-disk artifacts, and resumes
from there. It owns **sequencing and state only** — every stage's actual rules live in that
stage's own skill, which the conductor loads and runs without shortcuts.

## What does this skill do?

- Detects the current stage from the project folder's artifacts (never from memory of past
  sessions) and announces the detected stage plus the remaining ladder before doing anything.
- Runs one stage at a time by loading that stage's skill and letting it finish, including all
  of its internal gates (locks, audits, vetoes, calibrations) — the conductor never bypasses
  them.
- Stops at every formalized USER gate: transcript generation (a manual click in Premiere's
  Text panel), video-02's branch decisions and "lock the cut", video-04's trim veto and punch
  confirmation, video-05's speed pick, and video-08's DaVinci SRT export.
- Batches foreseeable user decisions at the first stop so later stages can run unattended —
  but never invents an answer for an unasked question.
- Enforces the sequencing laws: speedup is the last timeline operation, every timeline
  mutation voids downstream timecodes (transcripts are re-pulled after cuts and after
  speedup), and graphics cues derive only from the final-pace transcript.
- Logs one line per completed stage to `Transcripts/pipeline-log.md` — the resume anchor for
  future sessions.
- Stops the line on any failure (failed audit, mismatched verification, unavailable bridge)
  and never auto-advances past it or retries destructive operations without the user.

## When should I use it?

Any request to run or resume the **whole** edit rather than one step — "run the pipeline",
"continue the edit", "next stage", "run the pipeline from <stage>" — and status questions
like "where does this project stand". Never for a single-step request; the stage skills
trigger directly on those. YouTube delivery (video-09) is post-pipeline and only ever starts
on Diogo's explicit request after approval — the conductor never runs it.

## What inputs does it need?

- An open Premiere project following the template layout: the `.prproj` sits at
  `<root>/03_Project_Files/Adobe/`, which is how the project root is derived.
- The project's artifacts in `<root>/04_Project_Assets/Transcripts/` (transcript JSONs, CUT
  ORDER files, `pipeline-log.md`) — the folder **is** the state.
- The user's answers at each USER gate listed in the stage table.

## What does it produce?

- A stage-detection report (3–5 lines) at the start of every run.
- Whatever each stage skill produces, in order — prepped sequences, cut decision sheets, CUT
  ORDERs, executed cuts, conformed transcripts, graphics cue sheets, subtitle files.
- An appended `pipeline-log.md` entry per completed stage (date, stage, key numbers).
- A final handoff report when the pipeline is exhausted: pickups pending, marker checklist,
  review export next (and, when the FLOW srt exists, a pointer to video-09 as the next step).

## Prerequisites

- The stage skills installed alongside it: `video-01-ingest` through `video-08-subtitles`
  (plus `video-06-animate` and `video-07-graphics-placement` for the graphics stages). Each
  stage's own prerequisites apply when its stage runs.
- The **premiere-pro MCP server** connected to a running Premiere Pro, since nearly every
  stage drives Premiere through it — including the UXP WebSocket bridge on
  `ws://localhost:7777/uxp` for transcript pulls.
- A project folder following the MAN Digital template structure (Adobe project under
  `03_Project_Files/Adobe/`, transcripts under `04_Project_Assets/Transcripts/`).
- A user at the keyboard for the named manual steps: Generate transcript (Text panel), Track
  Mixer inserts, pickups, and UDT panel re-Load after a Premiere restart.
