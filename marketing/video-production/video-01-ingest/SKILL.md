---
name: video-01-ingest
description: Project front end for Premiere Pro via the premiere-pro MCP — post-import audio prep (each clip carries ONE mono audio clip, eliminating the Fill Left/Right step from the dialogue speed-up SOP), camera color labels, and the timeline-first v1→v2→v3 prep including two-camera waveform synchronization. Use after importing footage, or when the user says "prep the imports", "fix the audio channels", "set clips to mono", "one audio track per clip" — and for two-camera work: "sync the cameras", "synchronize by waveform", "make the sync", "simulate multicam", "build v2/v3", "prepare the timeline", or when a timeline holds two cameras stacked unsynced.
when_to_use: Right after media import, BEFORE any clip is added to a sequence; and again on a v1 assembly for the v2 rebuild + v3 camera sync. Any request about clip audio channel format or two-camera synchronization.
---

# Premiere Ingest — audio channel prep

Normalizes freshly imported talking-head footage so every video file lands on the timeline with **one audio clip, mono, carrying the recorded channel**.

**The bridge capability map lives in this skill: `references/premiere-mcp-map.md`** —
the live-tested record of which premiere-pro MCP tools work, lie, or destroy
(version-pinned to PPro 26.3 + MCP 1.4.0; folded in from memory 2026-08-06). Read it
before using any bridge tool you haven't already used this session. This skill is the
map's home; video-00/03/04/05 point here.

## Why mono

The mic records on one channel; the other is empty or a duplicate. Mono mapping means: one audio clip per video on the timeline (not A1+A2), no phantom empty channel, and — the compounding win — the **Fill Left with Right / Fill Right with Left step in the dialogue speed-up SOP becomes unnecessary**, because there is no empty channel to fill. Stereo Clip Channel Format is the fallback only when a clip genuinely carries two distinct channels worth keeping.

## The one hard constraint

**Channel mapping applies to project items and only affects clips added to sequences AFTERWARDS.** Clips already on a timeline keep their old mapping. So this runs immediately after import, before any editing. If footage is already cut in, changing the mapping fixes nothing retroactively — say so instead of pretending.

## Camera policies (Diogo's fleet — confirmed from project inspection 2026-07-28)

| Files | Camera | Source layout (file default) | Action |
|---|---|---|---|
| `PANA*.MOV` | Panasonic A-cam (talking head) | Mono ×4 channels → 4 audio clips | Remap: **Mono, 1 audio clip**, source = mic channel (below) |
| `DSCF*.MOV` | Fujifilm B-cam | Stereo, 1 clip | **None** — already correct, never touch |
| anything else | screen recs, external audio, music | varies | Flag and ask, never assume |

**PANA mic channel: CONFIRMED (Diogo, 2026-07-29) — use channel 1.** The source is a DJI Mic receiver feeding the camera; ch1 and ch2 carry the *same* recording, so ch1 is safe unconditionally. If the DJI safety-track mode is ever enabled, ch2 becomes a −6dB duplicate of ch1 — channel 1 remains the primary either way. No need to ask; only re-open this if PANA footage ever arrives with visibly different content on ch1 vs ch2. The unused channels remain in the project item's source media — recoverable later by re-mapping or from the source monitor, so collapsing to 1 clip loses nothing permanently.

## Procedure

1. Identify the newly imported items — `get_bin_contents` on the ingest bin (Diogo's structure: `01_Raw_Media/@A_Roll`, `@B_Roll`) or `find_project_item_by_name` / `list_project_items`.
2. Apply the camera policy by filename pattern. For PANA items: audio fix per the working method above (ExtendScript `audioClipsNumber = 1`). DSCF items: audio untouched. **Every prepped item also gets its camera color label** (`set_color_label`): PANA → Violet (index 0), DSCF → Iris (index 1). Labels live on the project item, so every future timeline insert inherits its camera color automatically — no per-clip work, ever. Unknown filename patterns: ask.
3. Verify by read-back on at least one item, and by dropping one clip into a scratch sequence if certainty matters: it must produce exactly one mono audio clip.
4. Report the items changed and the channel used. Flag any item whose audio looks genuinely stereo (music, ambient recordings) rather than silently forcing it mono.

## Timeline-first prep (v1 → v2 → v3) — Diogo's actual start-of-project flow

The user assembles the first timeline BEFORE audio prep: A-roll (1–2 cameras) laid out manually as `…_v1`. Prep ritual for two cameras: each camera on its own video track, and the second camera dropped **into the empty space** below the last audio track / above V1 so Premiere auto-creates fresh tracks — never onto occupied audio tracks at the same position (default drag is overwrite and would punch holes in camera 1's audio). Which track *numbers* the audio lands on is irrelevant; the v2 rebuild normalizes the layout. The skill then fixes what the channel-mapping constraint would otherwise block:

1. **Inspect v1.** Read its clips (order, positions, tracks) and map each to its project item.
2. **Fix the project items.** Apply the camera policy (above) to those items — mapping changes affect future timeline adds only, which is exactly what steps 3–4 exploit. **Working method (proven 2026-07-29):** the MCP's `set_project_item_audio_channel_mapping` maps routing but CANNOT change the clip count. The count change needs ExtendScript — `item.getAudioChannelMapping` → `m.audioClipsNumber = 1; m.setMappingForChannel(0,0)` → `it.setAudioChannelMapping(m)` (do NOT touch `audioChannelsType` — read-only, throws). Run it via `execute_extendscript` (needs `PREMIERE_MCP_CAPABILITIES=...,unsafe-script` in the server env — already in Diogo's user config) or, in a session whose server lacks the capability, by writing a `cmd_<id>.jsx` directly into the CEP bridge temp folder and polling `res_<id>.json` (bootstrap line: `$.evalFile` the `helpers_*.jsx` in that folder; return via `__result(...)`). Verify with a test insertion on an empty track: exactly ONE audio clip must appear.
3. **Build v2 = same assembly, fixed audio.** `duplicate_sequence` v1 → rename `…_v2` → remove its clips → re-add the SAME project items in the same order and positions. The fresh instances inherit the fixed mapping. Verify by read-back: every PANA clip now carries exactly one mono audio clip. (Never modify v1 — it is the reference.)
4. **Two cameras → build v3 = synced.** `duplicate_sequence` v2 → `…_v3`, B-cam clip stacked on the next video/audio tracks, both starting at 0. Then compute the true offset from the SOURCE FILES:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/audio_sync_offset.py A_CAM.MOV B_CAM.MOV --fps 25
   ```
   **Placement (PROVEN method, full run 2026-07-29): `preview_edit_plan` → `apply_edit_plan`** with `remove_clip` (old unsynced instances) + `insert_clip` at the computed targets. It places exactly where told. Laws learned by live failure — follow all of them:
   - **Always set `sequence_id` in the plan** — without it the plan hits whatever sequence has focus, and the user clicking a timeline tab mid-run misroutes destructive ops (it happened; two sequences were cross-damaged and repaired).
   - **Node ids are EPHEMERAL** — every mutation reassigns them. Fetch ids via `get_full_sequence_info` immediately before the plan, never reuse ids across mutations, and re-fetch + retry once on "Clip not found".
   - **`insert_clip` SPLITS what it lands on and RIPPLES the remainder downstream** (it does not truncate-delete). When a B-cam file spans a gap in A-cam recording, the overlapped tail reappears as fragments pushed later on the track. Therefore: **full-track audit after placement** (`get_active_sequence` clip list), never spot-probes only — count clips per track and account for every fragment.
   - **Unsynced-content convention (Diogo's rule):** footage with no sync counterpart (recorded while the other camera was stopped) is KEPT, parked after the synced content, flagged with an **orange marker** explaining what it is; stray mid-timeline slivers of the same material are removed. If an entire file has no sync home, additionally set its project-item label to a third color (Mango, index 9). Never silently delete unsynced footage.
   - **Still forbidden** (Premiere 26.3 + MCP 1.4.0): `move_clip` (stretches instead of translating), `overwrite_clip` (ignores track/time params, lands at track 0 / 0:00), bridge `undo` (broken; recovery = user's ⌘Z).
   - Ask the user to keep hands off Premiere during the run; verify the active sequence by NAME in read-backs.
   **Fallback placement (restored 2026-08-01 — use when `apply_edit_plan` is unavailable, regressed by an MCP update, or trust is low):** place a labeled sequence marker (`add_marker`, orange, name = the B clip's filename) at each computed target position, then have the user drag each B-cam clip to its marker with snapping on — the machine does the math, the human does the 30-second drag pass. Verify final positions by read-back against the computed targets (±1 frame).
   **Confidence gate:** `reliable: false` (ratio < 3) → do NOT auto-place that clip; tell the user to run Premiere's native Synchronize for it (select both clips → right-click → Synchronize → Audio — works on separate tracks within ONE sequence). The script also reports drift for long takes (warn past ~1 frame per 10 minutes) — but the drift-check code path is UNVERIFIED on real footage; treat drift warnings as advisory until validated on a genuine long take.
   Single camera → skip v3; v2 is the working sequence.
5. **Housekeeping (all three learned from the first live run):**
   - **Bins:** duplicated sequences land at project root — always `move_item_to_bin` them into the bin the original lives in (Diogo's structure: `00_Timelines/01_Active_Cuts`; the tool takes `target_bin` by NAME). v1 moves to `05_Old_&_Unused_Timelines` only after the user approves the synced result — never before.
   - **Camera color labels:** set at PROJECT-ITEM level so rebuilt instances inherit — A-cam (PANA) = Violet (index 0), B-cam (DSCF) = Iris (index 1), whole-file-unsynced = Mango (index 9). Per-clip labels are not API-reachable (`set_color_label` is item-only); fragment-level flags use markers instead.
   - The highest v-number is the working sequence the transcript stage targets.

## Never

- Run after clips are already cut into the working sequence and imply it fixed them
- Guess the recorded channel
- Force mono on items that genuinely carry two distinct channels without flagging it
