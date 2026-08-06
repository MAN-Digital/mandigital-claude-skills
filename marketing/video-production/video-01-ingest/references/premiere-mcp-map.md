# Premiere MCP capability map — what the bridge can and cannot do

**The verified broken-tool map.** Live-tested facts, not documentation claims: which
premiere-pro MCP tools work, which lie, and which are dangerous. Folded in from the
memory layer on 2026-08-06 (Diogo's commission) so every Premiere-driving session sees
it — previously it lived only in memory files and skills still told sessions to try
dead calls.

**Version pin:** Premiere Pro **26.3.0** + premiere-pro-mcp **1.4.0** (server
self-reports 1.2.0), live-tested 2026-08-01/05 during the BlogHubspotConsulting v8
audio work and the S1 Short build. Every claim here is dated and falsifiable —
**re-verify on any Premiere or MCP upgrade** before trusting the map's negatives; a
fixed tool should be promoted here with its test evidence, through the skill-edit
protocol.

Pointed at by: video-01-ingest, video-03-cuts, video-04-pause-pass, video-05-speedup,
video-00-pipeline. This file is the single source — never copy its rows into a skill;
link them.

## Hard limits — Premiere's scripting architecture, no MCP tool can cross these

- **Audio Track Mixer inserts (track-level effects) are completely invisible**: cannot
  list, edit, reorder, keyframe, or even confirm they exist. Diogo mixes with track
  inserts (limiters/filters/reverbs at track level, clip volumes at 0 dB), so
  effect-chain work is ALWAYS manual.
- **Track fader / track automation:** no access.
- **Essential Sound panel:** no access.

## Broken or dangerous (tested, not hearsay)

| tool | behaviour | use instead |
|---|---|---|
| `set_clip_volume` | **DANGEROUS — MUTES the clip**: writes Volume to 0 (= −∞ dB) regardless of the dB passed, while echoing success with the requested value | `add_audio_keyframes` (one keyframe = flat level) |
| `apply_audio_effect` | cannot apply ANY audio effect in 26.3 ("Audio effect not found") — `list_available_audio_effects` returns `[]`, the QE audio effect list is gutted | manual checklist to the user |
| `add_tracks` | **false success** — returns `{added: true}`, adds nothing | tracks pre-exist in the project template, added by hand once |
| `add_track` | fails honestly: `seq.insertAudioTrackAt is not a function` | same |
| `add_to_timeline` | emits `seq.insertClip()` → **it RIPPLES the timeline**, and returns `{added:true}` unconditionally; the friendly name is a trap | `execute_extendscript`; FCPXML round trip as fallback |
| `overwrite_clip` / `overwrite_from_source` | pass a **ticks string where Adobe documents seconds** — the recorded "lands at track 0 / 0:00" bug; ignores track/time params | same |
| `move_clip` | stretches instead of translating | `execute_extendscript` |
| bridge `undo` | broken | the user's ⌘Z |
| `ripple_delete` on a multi-track sequence | single-clip, single-track semantics: closes the gap on ONE track and **desyncs every other track**. Fine on a single-track spine; never for range cuts on layered timelines | the multi-track extract path below |
| `get_sequence_in_out_points` | unreliable read-back: reads ~0 (4e-09) right after a successful set — the SET works, the READ lies | verify via the extract's duration delta |

## Reliable (verified by read-back)

- **`add_audio_keyframes` — the workhorse.** Sample-accurate (not frame-locked),
  clip-relative time, exact dB→amplitude math (verified: −10 dB → 0.3162278).
- Sequence ops: `duplicate_sequence` (no name arg — creates `<name> Copy`, rename via
  `rename_project_item`), `set_active_sequence` (accepts name), `save_project`.
- All structure reads: `get_track_info`, `get_sequence_settings`, `list_clip_effects`,
  `get_clip_properties`, `find_project_item_by_name`.
- `get_keyframes` on intrinsic Volume/Level — amplitude ratios, 1.0 = 0 dB.
- `speed_change` / `set_clip_speed_qe` (video-05's SOP path).
- `split_clip` (video-03's protocol: always create both split points explicitly).

## Multi-track range cuts — the solved path (2026-08-05, frame-exact on 11 tracks)

`set_all_tracks_targeted {targeted:true, track_type:"both"}` →
`set_sequence_in_out_points {in_seconds, out_seconds}` → `extract_selection`
(= `qeSeq.extract()`): removes the range across ALL targeted tracks and ripples them
together. Two extracts on an 11-track 9:16 timeline landed frame-exact, delta 0.000 s.
- **Duration is the sync detector**: sequence duration only drops by the full extracted
  length if EVERY track rippled; a partial ripple leaves it unchanged.
- Execute ranges **descending** (highest timecode first) so earlier numbers never shift.
- video-03-cuts owns the surrounding safety protocol (duplicate first, audit).

## Escape hatches

- **`execute_extendscript`** — the route for anything the typed tools can't do; it
  already rescued the mono-channel mapping (video-01) and is the designated SFX
  placement route. Needs `PREMIERE_MCP_CAPABILITIES=…,unsafe-script` in the server env
  (in Diogo's user config). No capability? video-01 documents the CEP-temp-folder
  `cmd_<id>.jsx` / `res_<id>.json` fallback.
- **FCPXML round trip** (`export_as_fcp_xml` / `import_fcp_xml`) — documented fallback
  for placement, **both still unused**: verify before first production use.
- Only **31 of 282** bridge tools are referenced anywhere in the skill library — the
  other 251 are unvetted. Treat an unlisted tool as unknown: test on a duplicate
  sequence and read back before first production use.

## Connection — the port-7777 single-instance rule

The server binds `127.0.0.1:7777` to reach the CEP bridge panel; only ONE instance can
run. **Most "MCP disconnected" states = a stale instance from an older session still
holding the port**, crashing the new one after the tool-list handshake. Fix: find the
holder with `lsof -nP -t -i :7777 -sTCP:LISTEN` and kill that PID — **NEVER
`pkill -f premiere-pro-mcp`** (the claude host process's own command line contains the
string; pkill kills the session). Manual stdio JSON-RPC drive is possible when the
session has lost the server (spawn the binary with the env from `ps`, `initialize` →
`notifications/initialized` → `tools/call`; the server is stateless, the CEP panel
must be running). Verify connectivity with `ping` — returns project name + active
sequence.

## Discipline — why read-back is mandatory

- **The bridge often echoes the request instead of the resulting state** — several
  tools report success without doing the work (`add_tracks`, `add_to_timeline`,
  `set_clip_volume`'s success-with-wrong-value). After EVERY write, read state back
  via a DIFFERENT tool before reporting success. video-03's audit rule applies to all
  Premiere MCP writes, not just cuts.
- **MCP-built sequences can vanish under you**: Premiere's undo stack covers MCP edits,
  so the user's ⌘Z presses can unwind the `duplicate_sequence` that created a
  deliverable even after `save_project` reported success (observed 2026-08-05 — an
  audited, saved sequence was gone by session end). Re-list sequences at the end of a
  multi-build run and confirm every earlier deliverable still exists by id.
- **Two dB scales, don't mix**: raw `list_clip_effects` values use Premiere's
  +15 dB-offset scale (0 dB reads 0.177828 = 10^(−15/20)); `get_keyframes` uses plain
  amplitude (0 dB = 1.0).
