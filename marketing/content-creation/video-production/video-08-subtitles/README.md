# video-08-subtitles — Subtitle QA & Flow

Cross-references the DaVinci Resolve caption export against the Premiere transcript to
produce one verified caption file, then builds the punctuation-free FLOW delivery
version. Pipeline stage 08: the **final caption QA stage** — after the cut is locked,
the pause pass and speedup are executed, and the DaVinci caption template is applied.

## What does this skill do?

- Exploits two independent ASR engines that transcribed the same audio: DaVinci (the
  styled SRT — the base and the deliverable) and Premiere (the transcript JSON with
  per-word confidence — the evidence). They disagree exactly where one is wrong, so
  almost the whole QA pass needs no listening.
- **Stage A — CORRECTED.srt:** aligns the two exports (`align_report.py`), arbitrates
  every diff using engine error signatures (DaVinci flubs names/homophones; Premiere
  drops small words), confidence thresholds, a brand/jargon glossary, and number rules;
  captures the decisions in a per-project edit spec (`edits.json`); applies and
  validates with `apply_edits.py` (unique matches, wrapper integrity, timing sanity,
  width law, residue); writes a changelog with fixes, restored words and flags.
- **Stage B — FLOW version:** `flow_build.py` makes sentence-clean caption cuts using
  JSON word timestamps, strips prose commas and sentence-final dots (question marks,
  thousands separators, apostrophes, hyphens and URL dots are kept), closes every
  mid-sentence caption gap while keeping deliberate sentence-boundary breathing pauses
  (≥ 0.5 s), and hard-guarantees word content identical to CORRECTED.
- **Stage C — de-tag:** `detag.py` strips the inline style tags from the filed
  deliverables (the DaVinci track template owns the look).
- Enforces the two template laws: never exceed the export's measured one-line width
  (currently 18 chars), never merge words across blocks; minimum caption durations
  follow the export's own rhythm.
- **Flags instead of guessing:** coin-flip readings, brand spellings, restored clauses
  worth an ear check, and oddities both engines agree on are flagged with timestamp,
  current pick and alternative for Diogo's verdict — silently resolving one is
  forbidden. After verdicts, the spec is updated and Stages A→B rerun deterministically.

## When should I use it?

- "Check the subtitles", "fix the captions", "caption QA", "clean the srt", "make the
  flow version", "remove the dots and commas" — or whenever a DaVinci .srt and a
  Premiere transcript .json for the same cut are both present.
- LAST in the pipeline, and re-triggered whenever a fresh SRT export arrives after
  timeline changes. Never mid-edit — any recut voids every timecode in both exports.

## What inputs does it need?

- **Premiere transcript JSON** of the conformed cut (Text panel → Transcript → Export →
  JSON), with word-level start/duration/confidence.
- **DaVinci SRT export** of the same cut, from the timeline with the caption track
  (inline style tags ride along and are preserved through editing).
- Both exports must come from the **same conformed cut** — a built-in sanity check
  (first word within ~0.2 s, drift ≤ ~0.2 s throughout) stops the pass and demands
  re-export when one is stale.
- Diogo's verdicts on the ⚑ flags (the user-decision gate; the pass ships with flags
  open, verdicts trigger a rebuild).

## What does it produce?

Filed beside the source exports in `04_Project_Assets/Transcripts/`:

- `<orig> CORRECTED.srt` — the QA reference, punctuation intact, de-tagged
- `<orig> CORRECTED FLOW.srt` — the delivery file, de-tagged, ready to re-import onto
  the DaVinci caption track
- `<orig> CORRECTED — changelog.md` — fixes table with timestamps, restored words,
  polish list, ⚑ flags, deliberately-not-changed notes
- `_srt build scripts/<ver> edits.json` — the reusable edit spec (outputs are never
  hand-edited; the spec is fixed and everything rebuilds)

## Prerequisites

- **python3** — the whole pass runs through `scripts/` (`align_report.py`,
  `apply_edits.py`, `flow_build.py`, `detag.py`).
- **Upstream pipeline complete:** video-03 cuts, video-04 pause pass, video-05 speedup
  all executed, and the DaVinci caption template already applied to the timeline.
- DaVinci Resolve for the SRT export and re-import; Premiere Pro for the JSON export.
  No MCP server is needed — this skill works on the exported files.
