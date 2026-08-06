# video-07-graphics-placement — Graphics Placement

Maps existing visual assets onto an already-locked video cut and emits a dual-timecode
cue sheet for the editor and the motion designer. Pipeline stage 07: runs on the locked,
pause-passed, sped-up cut — matching and verification, never design (the skill cannot
see the frame and never comments on aesthetics).

## What does this skill do?

- Classifies every asset as **walkthrough** (speaker names its units, in its printed
  order, inside its window → progressive per-unit build) or **illustration** (single
  reveal, hold, out) — the foundational call that most placement errors trace back to.
- Verifies audio support by **concept, never label**: for each unit it derives a concept
  probe set (plain-speech phrasing, synonyms, the situation that produces the idea) and
  grades support **exact / concept / thematic / absent**. A negative from a label-only
  search is worth nothing.
- Scopes every claim to the asset's own transcript window, verifies ordering with
  unanchored probes, and applies spacing (~animation + 6 s) and reading floors.
- Makes the **format call** per asset — full frame (default), ⅔ split, ⅓ split, or
  alpha overlay — with the MD2/MD3 preset pairing named so the editor drops rather
  than builds. Verticals are on demand (2026-08-06): Short-first designs or an
  explicit repurpose ask only. (Canvas sizes and exact preset strings are canonical
  in video-06-animate's format table since 2026-08-06.)
- Emits **dual timecodes** for every cue: master cue (from sequence zero, for the
  editor) and MG cue (rebased to the asset's own IN point, for the motion designer).
- On request, runs **gap-fill mode** — proposes NEW graphics for uncovered stretches as
  two layers: the full recommendations map plus a ranked priorities shortlist with every
  drop reasoned.
- Runs the **texture pass** last over the merged plan: static-interval, archetype-run,
  size-run and overlay-spread flags, with redistribution remedies (re-cue, relocate,
  return frame to speaker, reprise) — it redistributes, it does not generate.
- On a re-cut, **re-derives every cue from its locate string** — never offsets or
  arithmetic-converts — and reports which rendered animations need a video-06 re-render.

## When should I use it?

- Whenever design assets and a timecoded transcript of a locked cut are both present:
  "where do the graphics go", "place these graphics", "build me a cue sheet", "when
  should this animation enter".
- When a fresh transcript export arrives and existing cue timings must be re-derived,
  when an asset is split into multiple files, or to check whether the audio actually
  supports a graphic.
- For proposing and prioritizing new graphics against a locked cut ("fill the script",
  "which are worth building") and for the texture pass ("is the pacing right", "does
  this drag").

## What inputs does it need?

- The **locked cut's timecoded transcript export** (CSV). Cue precision is capped by row
  granularity — Premiere ASR's ~4-word rows support per-unit cueing; sentence-level
  rows only support sentence-accurate cues, and the skill checks and says which.
- The **design asset files** themselves (canvas dimensions, type sizes, repeat units,
  MD5 are parsed from them).
- User decisions at Tier 2: borderline format calls, long holds, close cues, reading-
  floor reschedules, and the pick from gap-fill's recommendation/priority layers are
  proposed with reasons — the user decides. Texture remedies are likewise
  propose-only.

## What does it produce?

A placement report per the output contract:

1. Export keyed to, runtime, coverage %
2. Placement table — asset, IN, OUT, hold, type, format + preset pairing
3. Per-asset cue sheet — step, locate string, master cue, MG cue
4. Evidence grade per unit
5. Named gaps with reasons; relocations with both windows
6. Geometry warnings; vertical-variant status
7. Texture map — merged sequence, static-interval flags, archetype runs, overlay spread
8. In gap-fill mode: the recommendations layer plus the ranked priorities layer; chosen
   items go to video-06 with window, format and anchors

## Prerequisites

- **Upstream artifacts:** a locked cut (video-03 + video-04 + video-05 executed) with a
  fresh timecoded transcript export, plus the existing design assets.
- **python3** — all window/ordering/cue/texture arithmetic runs through
  `scripts/cues.py` (`window`, `unique`, `resolve`, `texture` subcommands).
- The skill's own reference docs: `references/rulebook.md` (full rules) and
  `references/geometry.md` (the two panel systems' canvas numbers and type floors).
- No Premiere/MCP access needed — this skill plans; the editor and video-06 execute.
