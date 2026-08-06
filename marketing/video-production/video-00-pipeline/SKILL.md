---
name: video-00-pipeline
description: Conductor for the MAN Digital video editing pipeline — chains the video-01…video-08 skills in order (ingest → transcript → script optimization → cuts → pause pass → speedup → graphics → subtitles) with the user's decision stops formalized, detects the current stage from the project's artifacts, and resumes from wherever the project stands. Use when the user says "run the pipeline", "continue the edit", "next stage", "where does this project stand", or wants a full edit run from raw footage to graphics-ready cut. Also "run the pipeline from <stage>".
when_to_use: Any request to run or resume the whole edit process rather than one step. Status questions about where a video project stands. Never for a single-step request — the stage skills trigger directly on those.
---

# Video Pipeline Conductor

This skill owns **sequencing and state only**. Every stage's actual rules live in its numbered skill — load that skill via the Skill tool when its stage begins and follow it fully. Never bypass a stage skill's internal gates (locks, audits, vetoes, calibrations); the conductor adds no shortcuts, only order.

For any direct Premiere-bridge interaction between stages, the live-tested capability
map at `video-01-ingest/references/premiere-mcp-map.md` (folded in 2026-08-06) says
which MCP tools work, lie, or destroy — consult it rather than trusting a tool's name.

## The map

Project root comes from the open `.prproj` (`<root>/03_Project_Files/Adobe/`); transcripts and pipeline log live in `<root>/04_Project_Assets/Transcripts/`. The folder **is** the state — detect the stage from artifacts, never from memory of past sessions:

| # | Stage (skill) | Runs when | Stop / gate |
|---|---|---|---|
| 1 | Ingest + timeline prep (`video-01-ingest`) | raw media imported without channel mapping, OR a `…_v1` assembly exists whose clips still carry raw audio mapping | none — camera policy decides; two cameras → waveform-sync builds v3 (confidence-gated, falls back to a named manual Synchronize) |
| 2 | Transcript | no `<working sequence>.json` in Transcripts/ (working sequence = highest `_vN` from stage 1) | if Premiere holds no transcript: **USER clicks Generate** (Text panel), then pull via bridge |
| 3 | Analysis + lock (`video-02-script-optimization`) | transcript JSON exists, no `.cutorder.md` derived from it | **USER: branch decisions + gating listen-checks → "lock the cut"** |
| 4 | Spine cut (`video-03-cuts`) | CUT ORDER exists and live timeline still matches its baseline | audit gates internally; post-execution auto-runs archive + conformed pull + verification + yellow markers |
| 5 | Pause pass (`video-04-pause-pass`) | conformed `<cut sequence>.json` exists, gaps not yet trimmed | **USER: trim veto + first-seam punch confirmation** |
| 6 | Speedup (`video-05-speedup`) | pause pass done or explicitly skipped | **USER: speed pick**; Track Mixer steps returned as manual checklist |
| 7 | Final transcript | after the last timeline mutation | — (pull via bridge; overwrite policy applies) |
| 8 | Graphics assets + format variants (`video-06-animate`) | assets in Working_Graphics/ still needed | optional; may run any time after the lock, in parallel — masters first, then the format pass (full / ⅔ / ⅓ / overlay + the standing 1280×2160 vertical) once masters are approved |
| 9 | Placement (`video-07-graphics-placement`) | final-pace transcript + assets exist | — |
| 10 | Subtitles (`video-08-subtitles`) | DaVinci caption template applied; SRT + final-pace transcript JSON exported from the same cut | **USER: exports the SRT from DaVinci; reviews ⚑ flags** |
| 11 | Handoff report | pipeline exhausted | list: pickups pending, marker checklist, review export next |

Sequencing laws (from the stage skills, restated because the conductor enforces order): speedup is the **last timeline operation**; every timeline mutation voids downstream timecodes, so transcripts are re-pulled after 4, and after 6 before placement; graphics cues derive only from the final-pace transcript. Subtitles (stage 10) also key off the final-pace transcript and run last of all — any later timeline change forces fresh exports and a re-run.

Post-pipeline (NOT a stage — the conductor never runs it): once Diogo approves the review export, `video-09-youtube-delivery` builds the upload-ready YouTube tracks (punctuated EN + EN-GB + six translations) into `06_Final_Delivery/Transcripts_&_Subtitles/`. It starts only on Diogo's explicit request, because approval happens outside the pipeline; the handoff report (stage 11) may mention it as the next step when the FLOW srt exists.

## Conduct

1. **Locate + report.** Determine project root and active sequence, scan the artifacts, and announce the detected stage and the remaining ladder in 3–5 lines before doing anything. If detection is ambiguous, ask — never guess a destructive stage.
2. **One stage at a time.** Load the stage's skill, run it to its own completion (including its internal gates), report the outcome in 2–4 sentences, then proceed — automatically through gateless stages, stopping wherever the table says USER.
3. **Batch the questions when possible.** If several user decisions are foreseeable (branches + veto + speed), offer them together at the first stop so later stages run unattended — but never invent answers for an unasked question.
4. **Log progress.** Append one line per completed stage to `Transcripts/pipeline-log.md`: `YYYY-MM-DD HH:MM · stage · key numbers (duration, cuts, wpm…)`. This file is the resume anchor for future sessions — read it during step 1.
5. **Failures stop the line.** A failed audit, a mismatched verification, or an unavailable bridge stops the pipeline at that stage with a report; never auto-advance past a failure, never retry destructive operations without the user.
6. **Named manual steps** — say them plainly when reached, never work around them silently: Generate transcript (Text panel), Track Mixer inserts (fill/Pitch Shifter), pickups to record, UDT panel re-Load after a Premiere restart.

## Never

- Skip, reorder, or merge stages without the user asking
- Answer a stage's USER gate yourself — including "obvious" vetoes and speed picks
- Run pause-pass or speedup math on a stale transcript (re-pull after every timeline mutation)
- Treat a missing artifact as permission to redo a destructive stage — investigate first (the log, the bins, the sequence list)
- Continue past a stage whose skill reported failure, even if the next stage could technically run
