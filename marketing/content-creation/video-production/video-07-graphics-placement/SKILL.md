---
name: video-07-graphics-placement
description: Maps existing visual assets onto an already-locked video cut and emits a dual-timecode cue sheet. Use whenever design assets and a timecoded transcript are both present, or when the user asks "where do the graphics go", "place these graphics", "which asset goes where", "build me a cue sheet", "graphics map", "when should this animation enter". Also use when a new transcript export arrives and existing cue timings need re-deriving, when an asset is split into multiple files, or when checking whether the audio actually supports a graphic. Also covers proposing NEW graphics for uncovered stretches — "suggest graphics for this section", "fill the script with graphics", "which graphics are worth building" — emitting the full recommendation map plus a prioritized cut. Covers asset-to-speech matching, cue derivation, hold durations, motion-graphics rebasing, format calls, and canvas/type-floor checks. Also the texture pass over the merged timeline — "is the pacing right", "does this drag", "build the texture map".
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/cues.py *) Read Glob Grep
---

# Graphics Placement

Full rules: `${CLAUDE_SKILL_DIR}/references/rulebook.md`. Geometry: `${CLAUDE_SKILL_DIR}/references/geometry.md`. Read them when a case is not covered here.

## What this skill does

Assets already exist. The cut is already locked. The question is which asset goes where, whether the audio supports it, and what timecodes the editor and the motion designer each need.

This is **matching and verification**, not design. Never comment on aesthetics.

## The prime directive

> You read the transcript and the asset file. You cannot see the frame.

- **Tier 1 — decide alone.** Does the audio support this asset, where, in what order, for how long. All timecode arithmetic.
- **Tier 2 — propose, they decide.** Whether a hold is too long, whether two cues are too close to cut between, whether a graphic competes with the speaker.
- **Tier 3 — never.** Anything about how it looks.

## Gate 1 — classify every asset: walkthrough or illustration

**Test:** does the speaker name the asset's units, in the asset's own printed order, inside its window? Exclude the reveal sentence, which often names every unit at once and produces a false out-of-order result.

- **Yes → WALKTHROUGH.** Progressive build, one unit per cue, in the graphic's order.
- **No → ILLUSTRATION.** Single reveal, hold, out. No per-unit build — any reveal order would invent a narration sequence that does not exist.

Under the walkthrough standard an illustration always appears to "fail" — it has units the speaker never names. **That is a classification error, not an asset defect.** If an asset resists per-unit cueing, re-run the classification instead of patching the treatment.

Confirmed independently by layout: walkthrough ↔ sequential ↔ side-panel-able; illustration ↔ comparative ↔ full screen. If the two disagree, one classification is wrong.

## The format call

Every placed asset gets a format in the placement table: **full frame** (default) · **⅔ split** · **⅓ split** · **alpha overlay**. Canvas sizes and Premiere preset pairings are CANONICAL in video-06-animate's format table (SKILL.md § "Formats — full frame, ⅔, ⅓, overlay") — cite formats by name here, never restate the numbers (consolidated 2026-08-06 so the sizes live in exactly one place).

- Width-spending layouts (wide tables, maps, fans, crossings, long strikes) and any clip handing into another full-frame graphic: **full frame only**.
- Single-column / naturally vertical content (stacked lists, chapter menus, headline-over-shell): split-able. **⅔** when the graphic should dominate or the talking stretch is long; **⅓** when the speaker should dominate and the content is a compact column.
- Quotes and short stats that punctuate rather than explain: **alpha overlay** over the speaker (works over any layout) — or full frame when they deserve total focus. Whether a borderline asset is worth full frame is Tier 2: propose with the reason.
- A split variant is authored by video-06 from the approved master and **keeps the master's cue table verbatim** — swapping master ↔ variant costs the editor zero timing work, so propose splits freely where the audio stretch suits a visible speaker.

Name the preset pairing with the call, so the editor drops rather than builds — take the exact graphic + footage preset strings from video-06's format table (one source since 2026-08-06; the shape: MD3 graphic In/Out + MD2 footage dodge at the same fraction on the opposite side, `Hold` on clips between, `Back` at exit; full frame needs no footage dodge). Which side the graphic sits on is the editor's call (Tier 3); the fraction is yours (Tier 1).

Verticals are **on demand** (Diogo, 2026-08-06): built only for Short-first designs, or on Diogo's explicit repurpose ask (policy, canvas size and the ⅓-split-shares-the-canvas equivalence live in video-06's format table) — placement tables no longer track missing verticals. Geometry in `references/geometry.md`.

Cross-check against Gate 1: a split call on an illustration, or full-frame-forced on a clean walkthrough column, is a flag that one of the two classifications is wrong.

## Gate 2 — search concepts, never labels

A speaker never says a graphic's internal caption. Labels are written artefacts; speech is conceptual.

A panel labelled *"Lifecycle stage drift · 62% match"* was reported unsupported because "drift" and "% match" returned nothing. What the speaker actually said, inside the window: `when you go to new markets, which might have different processes, different lifecycle stages`. The panel's own caption read *"MQL–SQL rules vary by region."* Same idea, different words.

For each unit, derive a **concept probe set** before searching: the idea in plain speech, its synonyms, and the situation that produces it. "Stale owner fields" → "data capture", "reps don't fill it in", "nobody updates". Never the label alone.

**A negative from a label search is worth nothing.** Never report "not spoken" without a concept search.

Grade every unit: **exact** (names it) · **concept** (says the idea) · **thematic** (adjacent) · **absent**. Only *absent* justifies dropping a unit.

## The passes

**1. Parse the assets.** Canvas dimensions and aspect, every type size, repeat units (design files store these as reference nodes — a naive text read returns the first instance and silently drops the rest), and MD5. Hash outputs against inputs: a "modified" file with an unchanged hash means the modification step did nothing.

**2. Scope every claim to the window.**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cues.py window TRANSCRIPT.csv --in TC --out TC
```
Coverage is only meaningful inside the asset's own window. A global keyword match is coincidence, not support. A unit absent from its own window but strong elsewhere is a **relocation candidate**, not a failure.

**3. Verify ordering with unanchored probes.**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cues.py unique TRANSCRIPT.csv CUES.txt
```
Searching forward from each previous match guarantees results in order — sequence found that way is an artifact of the method, not a finding. Re-test every reveal probe independently. Report probe uniqueness: one occurrence is a reliable anchor, several is a guess.

*Corollary:* when a source document (blog, deck, outline) structured the recording, asset order in the document predicts asset order in the video. Verify once with unanchored probes; if it holds, placement becomes near-deterministic.

**4. Establish granularity before proposing treatment.** One file or several? A monolithic asset can only reveal in its printed order; independent files can each land on the moment its own concept is spoken, in **audio order**. When per-unit support exists but printed order conflicts with audio order, **propose splitting the asset** rather than compromising placement. When granularity changes, re-derive from scratch — do not patch.

Spacing floor: animation duration plus ~6s. Cues closer than that strobe; keep one, relocate the other. A reprise is legal — an asset with two independent supports may appear twice. An empty frame is a valid output; holding a stale graphic through a section it no longer describes is worse than no graphic.

Reading floor: a word-synced appearance must leave enough window to be read. A unit whose anchor word lands under ~2s before its window ends is unreadable no matter how it animates (one landed 23 frames out — half a second of screen time). Flag it (Tier 2) and propose early arrival **with full content** — compress the dead air ahead of it and let the anchor word pass over an element already on screen. Sync yields to legibility; never fix it by inventing a new treatment when a reschedule of the existing one does it.

**5. Emit dual timecodes.**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cues.py resolve TRANSCRIPT.csv CUES.txt [--lead FRAMES]
```

| Column | Base | Consumer |
| --- | --- | --- |
| **Master cue** | sequence 00:00:00:00 | editor placing in Premiere/Resolve |
| **Cue for motion graphics** | the asset's own IN point | motion designer building the animation |

`MG = master − asset IN`, in frames, converted once at the end. Frame rate is detected from the data, never assumed.

Emit both, always. Master-only forces the designer to do arithmetic; MG-only makes the cue unplaceable. Either omission causes a time-remapping pass in the edit.

Rebase strictly against the asset's own IN. A forward reference to another asset's window rebases against **that** asset. For a split asset each file's internal cue is `0:00:00`; the MG column then carries each file's offset from the group's first entry — state which convention is in use.

## Proposing new graphics — gap-fill mode

Only on request ("suggest graphics for the rest", "fill the script", "what else is worth building"). The base skill maps *existing* assets; this mode proposes new ones for the uncovered stretches — and it proposes content, message, format and cue, never how anything looks (the prime directive holds).

1. Run the normal passes first, so every gap is named with its window and duration.
2. Per gap, propose: the spoken idea the graphic would carry (locate string attached), an archetype (stat, list build, quote card, comparison, process/diagram), a format call, entry cue and hold.
3. **Emit two layers, always:**
   - **Recommendations** — the full coverage map, up to filling the entire script if asked.
   - **Priorities** — the shortlist you would actually implement, ranked, with every dropped proposal named and reasoned. Drop anything not strong enough to beat the alternative of the speaker holding the frame alone: no real payload (it restates the sentence without adding a number, structure, or comparison), a window under the spacing floor, or a third graphic in a minute that already carries two. The empty-frame rule extends to proposals — the speaker alone is often the right recommendation.
4. The user chooses from the layers; chosen items go to video-06 with window, format and anchors. The recommendations layer stays full-size — the priority layer is an *added* filter, never a reason to suggest less.

## The texture pass

Runs **last**, over the merged plan — existing placements plus accepted proposals, sorted by timecode. Two documents that each read well can merge into a monotonous timeline; nothing upstream ever sees the union.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cues.py texture PLACEMENTS.txt
```

Four signals, all arithmetic over cue tables already emitted:

| Signal | Measures | Working flag [C] |
| --- | --- | --- |
| Static interval | time inside one asset with no cue firing | > 40s |
| Archetype run | consecutive placements sharing a treatment | 3+ |
| Size run | consecutive placements in the same duration band | 2+ over 3min |
| Overlay spread | where the callout/quote inventory sits | all inside one band |

**Duration is a proxy; the static interval is the signal.** In the source engagement one panel ran 3:21 with 15 cues (mean gap 0:14, worst 0:38) and read as dense; another ran 3:35 with 9 cues and one 1:26 hold, and read as drift. Same length, opposite experience. Flag intervals, not lengths.

Format interacts: a static interval in ⅔/⅓ split is carried by the live speaker; in full frame it is a still. Weight full-frame holds harder.

**Remedies, cheapest first. The pass redistributes; it does not generate.**

1. **Re-cue** an asset's own internal steps to break its dead air — asset unchanged, only the cue table moves.
2. **Relocate** an already-proposed card from a crowded band into a starved one.
3. **Return the frame to the speaker** — an empty stretch is itself a texture change, and is already a valid output.
4. **Reprise** — let a long asset go out and come back.
5. **Propose a new card** as normal, through gap-fill's own payload test. A card whose main value is rhythmic rather than informational is marked `[texture]` in the priorities layer, so the editor weighs it knowingly.

**Rails.**

- Gap-fill's contract wins on conflict: the recommendations layer stays full-size, and no recommendation is deleted for texture. Remedy 2 moves a card's *placement* and reports it as a relocation with both windows, like any other.
- A reading-away window is untouchable: minimum coverage, full-frame opaque (video-06's contract). Never relocate, shorten, split-convert or drop one for texture.
- Texture never overrides window-scoped evidence. A flagged stretch with no supportable remedy is reported as a flag, not fixed.
- Run **before** the video-06 build. A re-cue after render means a re-render — final clips carry ambient motion and cannot be freeze-retimed.
- Emitting the map is the deliverable; acting on it is Tier 2 — propose, they decide.

Thresholds are **[C]** — one video, 21 placements, no viewer data, same footing as the spacing floor. Falsification: run the map on the next two videos before the build and check whether the flagged stretches are the ones the editor independently marks as dragging.

## Re-cuts

Timecodes are keyed to one export; locate strings survive re-cuts, timecodes do not. On a new export **re-derive every cue from its locate string**. Never arithmetic-convert, never offset — a percentage speed change compounds (one pass here drifted +8s early to +113s at the end, so no fixed offset could work).

A re-cut also invalidates the *insides* of rendered animations: word-synced internal beats are baked at local frames (`master − place-at`), so when the words move, the affected clips are re-derived **and re-rendered** by video-06 — final clips carry ambient motion and cannot be freeze-retimed. Report which clips need the re-render pass, not just the new cue table.

After any bulk edit, cross-check section headers against their own tables. A double-conversion error surfaced only because a header disagreed with its first row.

## Transcript source

Cue precision is capped by row granularity. Premiere ASR gives ~4-word, ~1.6s rows, which supports per-unit cueing. A sentence-level export (~7s rows) collapses several cues into one and cues become sentence-accurate at best. Check granularity before quoting frame numbers:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cues.py window EXPORT.csv --in 00:18:19:00 --out 00:18:26:00
```

Six or seven short rows means fine granularity. One long row means say so rather than emitting precision the source cannot support.

Locate strings are **raw ASR verbatim including errors**, because that is what the transcript panel searches. Corrections ride alongside in brackets, never overwriting.

## Geometry

Read `references/geometry.md` before any canvas or type judgment. **Two panel systems exist — never mix their numbers.** *Split-screen thirds* (in-video, preset-paired): exactly 1280×2160 and 2560×2160, rendered native, output type floor 54px. *9:16 Shorts-convertible panels*: a true 9:16 at 2160 tall is **1215×2160**, not 1280 — design at 2160×3840, place at 56.25% (exact), so source type floor is ≥96px and strokes ≥4px. Type floor is ~2.5% of frame height in every system. Verify the source canvas first — assets built for the web are often neither 16:9 nor 9:16.

## Output contract

1. Export keyed to, runtime, coverage %
2. Placement table: asset, IN, OUT, hold, type, **format + preset pairing**
3. Per-asset cue sheet: step, locate string, **master cue**, **MG cue**
4. Evidence grade per unit
5. Named gaps, with reasons
6. Relocations, with both windows
7. Geometry warnings
8. Texture map: merged sequence, static-interval flags, archetype runs, overlay spread

## Never

- Report "not spoken" from a label search
- Claim coverage without naming a window
- Use sequential search as evidence of sequence
- Emit a master cue without its MG rebase
- Patch the same asset a third time — re-classify instead
- Comment on aesthetics
- Propose deleting an asset; relocate it, or leave it out with a stated reason

## The escalation tell

Two position reversals on the same asset means the **frame** is wrong, not the answer. Stop patching and re-run Gate 1. In the source engagement four reversals on one asset all traced to a single classification error.
