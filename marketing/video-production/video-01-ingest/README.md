# video-01-ingest — Premiere Ingest & Timeline Prep

First stage of the video pipeline (video-00 conducts it as stage 1). Normalizes freshly
imported talking-head footage in Premiere Pro so every video file lands on the timeline with
one mono audio clip, labels each camera, and runs the v1→v2→v3 timeline prep including
two-camera waveform synchronization.

## What does this skill do?

- Remaps audio channels on project items by camera policy: Panasonic A-cam (`PANA*.MOV`)
  collapses from 4 mono channels to **one mono audio clip on channel 1**; Fujifilm B-cam
  (`DSCF*.MOV`) is already correct and never touched; anything else is flagged and asked
  about, never assumed. Mono mapping also eliminates the Fill Left/Right step from the
  dialogue speed-up SOP.
- Sets camera color labels at project-item level (PANA → Violet, DSCF → Iris, whole-file
  unsynced footage → Mango) so every future timeline insert inherits its camera color.
- Rebuilds the user's manual `_v1` assembly as `_v2` with the fixed audio mapping (channel
  mapping only affects clips added to sequences *afterwards* — v1 stays untouched as the
  reference).
- For two-camera projects, builds `_v3`: computes the true A/B offset by audio
  cross-correlation of the **source files** (`scripts/audio_sync_offset.py`), then places the
  B-cam clips via a previewed edit plan — with a confidence gate (low-confidence clips are
  routed to Premiere's native Synchronize instead) and a marker-assisted manual fallback when
  the edit-plan path is unavailable or trusted less.
- Keeps unsynced footage parked after the synced content under an orange marker — never
  silently deleted.
- Hosts the **Premiere MCP capability map** (`references/premiere-mcp-map.md`, folded in
  from the memory layer 2026-08-06): the live-tested record of which bridge tools work,
  lie, or destroy, version-pinned to PPro 26.3 + MCP 1.4.0 — the single source that
  video-00/03/04/05 point at for bridge-capability questions.
- Verifies everything by read-back (and a scratch-sequence test insertion when certainty
  matters).

## When should I use it?

Right after media import, **before** any clip is added to a sequence — and again on a v1
assembly for the v2 rebuild and v3 camera sync. Any request about clip audio channel format
("set clips to mono", "fix the audio channels") or two-camera synchronization ("sync the
cameras", "build v2/v3"). It cannot fix clips already cut into a timeline — mapping is not
retroactive, and the skill says so rather than pretending.

## What inputs does it need?

- Freshly imported project items, ideally in the template ingest bins
  (`01_Raw_Media/@A_Roll`, `@B_Roll`).
- For timeline-first prep: the user's manually assembled `…_v1` sequence (for two cameras,
  each camera on its own tracks).
- For waveform sync: the two source media files on disk and the sequence fps (25 in Diogo's
  projects).

## What does it produce?

- Remapped project items (one mono audio clip each) with camera color labels, plus a report
  of items changed and the channel used.
- A `…_v2` sequence — the same assembly with fixed audio — and, for two cameras, a `…_v3`
  sequence with the B-cam placed at the computed offset, both filed into
  `00_Timelines/01_Active_Cuts`.
- Orange markers flagging kept-but-unsynced footage.
- The highest v-number sequence is the working sequence the transcript stage targets.

## Prerequisites

- The **premiere-pro MCP server** connected to a running Premiere Pro. The clip-count fix
  requires ExtendScript execution — either the server's `unsafe-script` capability
  (`PREMIERE_MCP_CAPABILITIES`, already in Diogo's user config) or the CEP bridge temp-folder
  fallback (`cmd_<id>.jsx` / `res_<id>.json`).
- **python3 with numpy** for `scripts/audio_sync_offset.py` and `scripts/sync_matrix.py`.
- **ffmpeg and ffprobe on PATH** — the sync scripts decode source audio through them.
- The MAN Digital template bin structure for filing (degrades gracefully without it).
