# Graphics Placement — Rulebook for Skill Creation

**Purpose.** Converts one full graphics-placement cycle into transferable rules. Design input for a Claude Code skill, not the skill itself.

**Source engagement.** MAN Digital, HubSpot Consulting Guide. 8 existing `.pen` assets from a published blog post, placed against a 37:43 locked cut. Six review passes, four position reversals on one asset, one methodological error that caused three of them.

**Scope.** Placing **existing** visual assets against an **already-recorded, already-locked** script. Not design. Not animation. Not script editing. The upstream skill (`script-optimization`) locks the cut; this one decides what goes on screen and when; a downstream motion skill builds the animation.

---

## PART 0 — WHY THIS SKILL DOES NOT EXIST YET

I searched for prior art before writing this. Everything in the ecosystem is **generative**:

| Project | What it does | Why it is not this |
| --- | --- | --- |
| `claude-remotion-skill` | writes React/Remotion, renders MP4 | creates video from a prompt; no existing assets, no existing script |
| `Claude-Code-Video-Toolkit` | Remotion, Manim, screen recording, FFmpeg | production pipeline; assumes you are authoring the visuals |
| `digitalsamba/claude-code-video-toolkit` | voiceover script → scenes → render | script drives generated slides, not existing assets |
| Hyperframes / HeyGen | HTML frames → timeline → MP4 | templated generation |
| `marketingskills/skills/video` | routes between generation tools | decision layer over generators |
| ElevenLabs Scribe + EDL agents | phrase-level transcript → EDL → FFmpeg | **closest architectural analogue** — transcript-driven reasoning over a timeline — but for *cutting*, not for placing graphics |

**The gap.** Every tool assumes the visual does not exist yet. The actual agency problem is the reverse: the assets exist (a designer made them, or they were built for a blog), the recording exists and is locked, and the question is *which asset goes where, and does the audio actually support it.*

That is a **matching and verification** problem, not a generation problem. The closest prior art is EDL-reasoning agents, and the useful borrowing from them is the pattern of treating the transcript as the authoritative index and emitting a machine-checkable placement list rather than prose.

**Implication for the build.** There is no skill to fork. But the architecture of `script-optimization` transfers directly: mechanical checks in a bundled script, judgment in the SKILL.md, tiered confidence, and verified-verbatim locate strings.

---

## PART 1 — THE PRIME DIRECTIVE

`script-optimization` has one: *the model reads text, the human hears audio.* This skill has a different one:

> **The model reads the transcript and the asset. It cannot see the frame.**

Everything follows. Three tiers again, but the axis is different.

**Tier 1 — model decides alone.** Does the audio support this asset? Where exactly? In what order? For how long? Does the asset's own content appear in the speech? Is the sequence internally consistent? All timecode arithmetic.

**Tier 2 — model proposes, human decides.** Whether a hold is too long to stay interesting. Whether two cues are too close to cut between. Whether a graphic competes with the speaker at that moment. Whether an asset is legible at its intended size.

**Tier 3 — model must not decide.** Anything about how it looks. Whether a colour reads. Whether an animation lands. Whether the frame is balanced.

**Rule 1.1.** Placement is Tier 1 and should be asserted. Aesthetics are Tier 3 and should not be mentioned unless asked.

**Rule 1.2.** The model's actual product is a *defensible mapping between spoken words and visual assets*, with the evidence attached. Not art direction.

---

## PART 2 — THE CORE TAXONOMY: WALKTHROUGH vs ILLUSTRATION

The single most valuable finding in the engagement, and the one that resolved a problem that had already survived three attempted fixes.

**Test:** does the speaker name the asset's units, in the asset's own printed order, inside the asset's window?

- **Yes → WALKTHROUGH.** The graphic's job is to track him. Treatment: progressive build, one unit per cue, in the graphic's order.
- **No → ILLUSTRATION.** The graphic's job is to show a state while he describes it in his own words. Treatment: single reveal, hold, out.

Result in this engagement: **7 of 8 walkthroughs, 1 illustration.**

| Asset | Units enumerated in order | Type |
| --- | --- | --- |
| Lifecycle Architecture | 7/7 | walkthrough |
| Ops Dashboard | **0/4** | **illustration** |
| Cost Table | 5/5 | walkthrough |
| Cost Drivers | 5/5 | walkthrough |
| Decision Tree | 4/4 | walkthrough |
| Partner Scorecard | 6/6 | walkthrough |
| Roadmap | 4/4 | walkthrough |
| Governance Rhythm | 3/3 | walkthrough |

**Rule 2.1.** Classify every asset before proposing any treatment. The two types need opposite treatments, and applying the walkthrough standard to an illustration is the failure mode that generated three wrong answers in this engagement.

**Rule 2.2.** Under the walkthrough standard, an illustration always "fails" — it has units the speaker never names. That apparent failure is a **classification error, not an asset defect.** If an asset resists per-unit cueing, stop trying to fix the asset and re-run the classification.

**Rule 2.3.** The taxonomy is independently confirmed by the layout framework: walkthrough ↔ sequential ↔ side-panel-able; illustration ↔ comparative ↔ full screen. When the two frameworks disagree, one of the classifications is wrong.

**Rule 2.4 (exclude the reveal line).** The reveal sentence often names every unit at once ("what's the difference between a consultant, an admin and an agency?"). Counting it produces a false out-of-order result. Exclude the reveal line before testing enumeration order.

---

## PART 3 — THE SEARCH ERROR THAT CAUSED EVERYTHING

Three of the four wrong positions in this engagement trace to one mistake.

**I searched for the asset's on-graphic labels instead of its concepts.**

The dashboard's drift panel is labelled *"Lifecycle stage drift"* with values *62% / 34% / 48% / 41% match*. I searched for "drift" and "% match", found nothing in 37:43, and reported the panel as unsupported.

What he actually says, inside the window:

> `things get even messier when you have product launches, when you go to new markets, which might have different processes, different lifecycle stages than what you did before`

The panel's own caption reads *"MQL–SQL rules vary by region, so handoffs slip."* Same idea. Different words.

**Rule 3.1.** A speaker never says a graphic's internal labels. Labels are written artefacts; speech is conceptual. Search for the **concept**, not the caption.

**Rule 3.2.** For each unit, derive a concept probe set before searching: the idea in plain speech, its synonyms, and the situation that produces it. "Stale owner fields" → "data capture", "reps don't fill it in", "nobody updates". Never the literal label alone.

**Rule 3.3.** A negative result from a label search is worth nothing. Only a negative result from a concept search is evidence. Never report "not spoken" from a label search.

**Rule 3.4.** State the evidence strength per unit: **exact** (names the thing), **concept** (says the idea in other words), **thematic** (adjacent, same territory), **absent**. Only *absent* justifies dropping a unit.

---

## PART 4 — SCOPE EVERY CLAIM TO THE WINDOW

Second methodological error, independent of the first.

I ran keyword coverage across the whole 37:43 and reported "7 of 8 complete". Constrained to each asset's own window, one asset dropped from 3/4 to 2/4. "Integration depth" had scored a hit from seven mentions spanning 1:10 to 36:20 — the entire video.

**Rule 4.1.** Coverage is only meaningful inside the asset's own window. A global match is not support; it is coincidence.

**Rule 4.2.** Report the window explicitly with every coverage claim. "Supported" without a window is meaningless.

**Rule 4.3.** A unit that is absent from its own window but strongly present elsewhere is not a failure — it is a **relocation candidate**. In this engagement the workflow-alerts panel had only thematic support in its own window and a near-exact match eight minutes later, in a different asset's window. It moved.

---

## PART 5 — GUARD AGAINST CIRCULAR SEARCH

I found the eight assets appeared in exactly blog order and reported it as a finding. Then I checked whether my method could have manufactured it.

It could have. My search took an `after` parameter and searched forward from the previous match. **Searching in order guarantees results in order.** The finding would have been an artifact of the method.

The fix: re-run every reveal probe **independently from 00:00:00** and count occurrences. All eight were unique in 37:43, so the ordering was a real property of the video. The finding survived, but only because it was tested.

**Rule 5.1.** Any claim about ordering must be verified with independent, unanchored searches. Sequential search cannot be used as evidence of sequence.

**Rule 5.2.** Report probe uniqueness. A probe with one occurrence is a reliable anchor; a probe with several is ambiguous and its placement is a guess.

**Rule 5.3 (the useful corollary).** When a source document (blog, deck, outline) was used to structure the recording, asset order in the document predicts asset order in the video. Verify it once with unanchored probes; if it holds, placement becomes near-deterministic and every subsequent asset is a narrow search rather than a hunt.

---

## PART 6 — ASSET GRANULARITY CHANGES WHAT IS POSSIBLE

Late in the engagement the editor split one four-panel dashboard into four independent animations. That invalidated my treatment, and correctly so.

A **monolithic** asset can only reveal in its own printed order. When the audio does not follow that order, the only honest treatment is a single reveal. That is a constraint of the asset, not of the content.

**Four independent assets have no such constraint.** Each can land on the moment its own concept is spoken, in **audio order** — which is a different and better order than the graphic's.

**Rule 6.1.** Treatment is a function of asset granularity, not just content. Establish granularity before proposing treatment: is this one file or several?

**Rule 6.2.** When per-unit concept support exists but the printed order conflicts with the audio order, **propose splitting the asset** rather than compromising placement. Splitting converts an order conflict into a non-problem.

**Rule 6.3.** When granularity changes, re-derive from scratch. Do not patch the previous answer.

**Rule 6.4 (spacing floor).** Independent assets need enough separation to read. Working figure from this engagement: animation duration plus ~6s. Two cues 5.4s apart with a 2s animation caused a rejected placement — three changes inside 12 seconds would strobe. Cues closer than the floor: keep one, relocate the other.

**Rule 6.5 (reprise is legal).** An asset with two independent supports may appear twice. It costs nothing (the asset exists) and often pays off a promise the audio under-delivers. In this engagement the forecast panel appeared at its weaker cue first and its strongest cue 56 seconds later.

**Rule 6.6 (empty frame is a valid output).** A 22.6s stretch with no matching asset was left to the speaker deliberately. Holding a stale graphic through a section it no longer describes is worse than no graphic. Name these gaps explicitly and say why.

---

## PART 7 — THE DUAL TIMECODE CONTRACT

Every cue must be emitted in **two coordinate systems**, because two different people consume it.

| Column | Base | Consumer |
| --- | --- | --- |
| **Master cue** | sequence 00:00:00:00 | editor, placing in Premiere/Resolve |
| **Cue for motion graphics** | the asset's own IN point | motion designer, building the animation |

`MG cue = master cue − asset IN`, at the sequence frame rate.

Worked: an asset entering at `00:18:19:22` with a step at `00:18:25:13` → the designer builds that step at `0:05:16`.

**Rule 7.1.** Emit both columns always. Master-only forces the designer to do the arithmetic; MG-only makes the cue unplaceable. Either omission causes a time-remapping pass in the edit, which is the cost this contract exists to remove.

**Rule 7.2.** Rebase strictly against the asset's own IN point. A forward reference to a different asset's window must rebase against *that* asset. Cross-section rebasing produced a nonsense value (`22:18:16`) in this engagement and had to be caught by hand.

**Rule 7.3.** For a split asset, each file's internal cue is `0:00:00`; the MG column then carries each file's offset from the group's first entry. State which convention is in use.

**Rule 7.4.** Frame rate is derived from the data, never assumed. Do the arithmetic in frames and convert once at the end.

---

## PART 8 — THE RE-CUT PROBLEM

Timecodes are keyed to one export. When the cut changes, every cue dies.

The v5 → v6 change here was a 105% speed pass. Drift ran from **+8s early to +113s at the end** — not a constant offset, because a percentage change compounds. Nothing could be shifted by a fixed amount.

**Rule 8.1.** Every cue table declares which export it is keyed to.

**Rule 8.2.** On a new export, re-derive every cue from its locate string. Never arithmetic-convert, never offset.

**Rule 8.3.** Locate strings survive re-cuts; timecodes do not. This is why the string is the primary key and the timecode is derived.

**Rule 8.4 (the double-conversion trap).** I once applied resolved timecodes correctly and then ran a blanket arithmetic conversion over the same document, dividing every value twice. It surfaced only because a section header disagreed with its own first row. **Cross-check headers against their own tables after any bulk edit.**

---

## PART 9 — DETERMINISTIC GEOMETRY

Not judgment. Arithmetic, and it should live in a script.

- A literal third of a 3840 frame is 1280, but `1280×2160` is **not** 9:16 (0.5926 vs 0.5625). A true 9:16 panel at 2160 tall is **1215×2160**.
- Design panels at **2160×3840**, place at **56.25%** (exact: 2160÷3840). Same file at 100% is the vertical master. No distortion, no double resample.
- Dual-context safe box, driven by platform UI: top 346, bottom 768, left 120, right 259 → content **1781×2726**.
- Type floor: legibility bottoms out near 2.5% of frame height (54px at 2160). A panel placed at 56.25% therefore needs **≥96px** source type. Strokes **≥4px** — a 1px border becomes 0.56px and shimmers.
- Full screen has different numbers: safe box 108/192/192/324, content 3456×1728, type floor 54px, stroke floor 2px. Do not let the panel spec leak onto full-screen assets.
- Downscale is cheap, upscale is expensive. Design big, render small.

**Rule 9.1.** Verify the source asset's canvas before anything else. The eight `.pen` files here were **1536×1024 (3:2)** — neither 16:9 nor 9:16. Fit to height leaves 600px blank; fit to width overflows by 400px.

**Rule 9.2.** Check every type tier against the floor at the intended placement scale. Six of nine tiers in these assets fell below it even at 2.5×. **Uniform scaling cannot fix this** — the type must grow relative to the layout, which means the layout gives up density. That is the real adaptation work and it is invisible until measured.

---

## PART 10 — READ THE ASSET FILE, NOT A PICTURE OF IT

I worked from blog PDF screenshots for most of the engagement. When the `.pen` files were finally provided, they answered questions the screenshots could not:

- exact canvas dimensions and aspect
- every type size, per element
- full content of repeated units, stored as `ref` nodes with descendant overrides and invisible to a visual read
- that a file believed to be adapted was **byte-identical to its source** (same MD5) — the adaptation instruction had silently failed

**Rule 10.1.** Parse the design source when available. Screenshots support classification but not measurement.

**Rule 10.2.** Hash outputs against inputs. A "modified" file with an unchanged hash means the modification step did nothing.

**Rule 10.3.** Design files store repeats as references. A naive text extraction returns the first instance and silently drops the rest — resolve reference nodes before claiming to know an asset's content.

---

## PART 11 — TRANSCRIPT SOURCE

This engagement used **Premiere Pro ASR only**. DaVinci Resolve was not tested, so nothing below is a comparison — it is the property list a source must satisfy.

What matters for this skill:

1. **Frame-accurate timecodes** matching the sequence, not wall-clock seconds.
2. **Fine row granularity.** Premiere's 1–3 word rows made per-unit cueing possible; sentence-level rows would floor cue precision at the sentence.
3. **Stable text across exports** so locate strings survive re-cuts. This breaks when a transcript is hand-corrected — corrected text no longer matches previously issued strings.
4. **Consistent failure modes.** Premiere ASR fails predictably: ordinals fused to nouns, brand terms, clause-terminal words. Documented in the `script-optimization` rulebook and directly reusable here, because cue strings inherit the errors.

**Rule 11.1.** The locate string is raw ASR verbatim including errors, because that is what the transcript panel searches. Corrections ride alongside in brackets.

**Rule 11.2.** If sources are mixed, note which one every cue was derived from. Strings are not portable across ASR engines.

**Rule 11.3 (open).** Establish whether Resolve's row granularity matches Premiere's. If it is sentence-level, cue precision drops and the skill should say so rather than emitting cues it cannot support.

---

## PART 12 — THE STEELMAN PROTOCOL

The engagement's most productive move was the editor asking me to argue against my own output.

What it caught: the circular-search risk (Part 5), the whole-video coverage inflation (Part 4), the label-vs-concept error (Part 3), and the walkthrough/illustration taxonomy (Part 2) — which only surfaced because I was forced to ask *why* one asset kept resisting instead of patching it a fourth time.

**Rule 12.1.** Before finalising, re-derive independently rather than re-reading the previous conclusion. Re-reading confirms; re-deriving tests.

**Rule 12.2.** For each claim, ask what method artifact could have produced it, then test that specifically.

**Rule 12.3.** Report what survived, what broke, and what the breakage implies — in that order. A steelman that finds nothing was not a steelman.

**Rule 12.4 (the escalation tell).** Four position reversals on one asset, each a patch on the previous, was the signal that the *frame* was wrong rather than the answer. **Two reversals on the same item should trigger re-classification rather than a third patch.** This is the highest-value operational rule in the document.

---

## PART 13 — SUGGESTED ARCHITECTURE

**Triggering.** Fire when a locked cut plus visual assets are present, or on: "where do the graphics go", "place these", "which asset goes where", "cue sheet", "graphics map". Also on any asset file arriving alongside a transcript.

**Body order** (gates that prevent confident nonsense first):
1. Parse assets — canvas, type tiers, repeat units, hashes (Part 10)
2. Classify walkthrough vs illustration (Part 2)
3. Derive concept probes per unit — never labels (Part 3)
4. Search window-scoped, verify probe uniqueness (Parts 4, 5)
5. Establish granularity, apply the spacing floor (Part 6)
6. Emit dual timecodes (Part 7)

**Bundled scripts.**
- `cues.py` — probe → master cue → MG rebase, with verbatim verification and probe-uniqueness reporting. Regenerates a whole cue table against a new export in one command.
- `assetparse.py` — canvas, aspect, type-tier histogram against the floor, reference resolution, MD5.
- `geometry.py` — panel maths, safe boxes, type floors (Part 9).

**Output contract.**
1. Export keyed to, runtime, coverage %
2. Placement table: asset, IN, OUT, hold, type
3. Per-asset cue sheet: step, locate string, master cue, **MG cue**
4. Evidence strength per unit (exact / concept / thematic / absent)
5. Named gaps with reasons
6. Relocations, with both windows
7. Geometry warnings — canvas mismatch, type below floor

**Anti-patterns.**
- Do not report "not spoken" from a label search
- Do not claim coverage without naming a window
- Do not use sequential search as evidence of sequence
- Do not emit a master cue without its MG rebase
- Do not patch the same asset three times — re-classify
- Do not comment on aesthetics
- Do not propose deleting an asset; relocate or leave it out with a reason

---

## APPENDIX A — WORKED CASES

**A1. The asset that resisted four treatments.** Full-screen four-panel reveal → split across four timestamps → drop entirely → dim the unsupported panel. Every position was a patch on the previous. The actual problem was that it was the only illustration among eight walkthroughs and was being held to the wrong standard. *Rules 2.1, 2.2, 12.4.*

**A2. The false negative that caused A1.** "Drift" and "% match" returned nothing; the concept was spoken plainly 34 seconds into the window. Label search, not concept search. *Rules 3.1, 3.3.*

**A3. Coverage inflation.** "7 of 8 complete" was measured across the whole video. Window-scoped, one asset dropped to 2/4. *Rule 4.1.*

**A4. The finding that nearly wasn't.** Blog order matched video order — possibly an artifact of forward-only search. Re-tested with unanchored probes: all eight reveal phrases unique. Finding survived. *Rules 5.1, 5.2.*

**A5. Granularity reversal.** The editor split a four-panel asset into four files, which legitimately invalidated the single-reveal treatment. Re-derived from scratch: three panels placed in audio order, one relocated eight minutes later, one panel reprised. *Rules 6.1, 6.3, 6.5.*

**A6. The relocation.** Workflow-alerts had thematic support in its own window and near-exact support in another asset's window (`arrows and routine issues` = "errors and routing"). Moved. *Rule 4.3.*

**A7. Compounding drift.** A 105% speed pass moved cues by +8s to +113s. No fixed offset could work; every cue re-derived from its locate string. *Rules 8.2, 8.3.*

**A8. Double conversion.** Correct values then a blanket arithmetic pass halved them again. Caught only because a section header disagreed with its own table. *Rule 8.4.*

**A9. The unchanged file.** An "adapted" asset was byte-identical to its source. The adaptation instruction had silently failed. *Rule 10.2.*

**A10. Type below floor.** Six of nine type tiers failed the legibility floor even at 2.5×. Invisible in screenshots, obvious once the file was parsed. *Rule 9.2.*

---

## APPENDIX B — EVIDENCE GRADES

| Area | Grade | Basis |
| --- | --- | --- |
| Walkthrough/illustration taxonomy | **A** | 8 assets, clean split, independently confirmed by the layout framework |
| Concept-not-label search | **A** | direct false negative, caused three reversals, fix verified |
| Window-scoped coverage | **A** | mechanical, changed a stated result |
| Circular-search guard | **A** | tested and survived |
| Dual timecode contract | **A** | arithmetic, verified against the editor's own hand calculations |
| Geometry and type floors | **A** | measured from source files |
| Granularity rules | **B** | one strong case |
| Spacing floor (~animation + 6s) | **C** | single observation, plausible, unmeasured |
| Reprise legality | **C** | one instance, worked |
| Steelman protocol | **B** | high yield here; counterfactual untested |

Convention: **[A]** measured from our files · **[B]** external validated · **[C]** hypothesis with a falsification path · **[D]** craft heuristic.

---

## APPENDIX C — OPEN QUESTIONS

1. **One skill or two?** Placement (transcript ↔ asset matching) and adaptation (geometry, type floors, canvas) have different triggers and different consumers. Adaptation may belong with the existing motion-graphics skill.
2. **How does the source document participate?** The blog drove structure, order, and copy. Required input, optional, or separate mode?
3. **Does asset parsing belong here?** `.pen` is one format; Figma, AE projects and SVG all differ. Possibly a separate asset-inspection skill this one calls.
4. **What is the stopping rule?** Proposed: every asset classified, every unit graded for evidence, every cue dual-stamped and verified verbatim, every gap named with a reason, zero geometry warnings unacknowledged.
5. **Does the taxonomy hold outside blog-derived content?** All eight assets here came from one article the speaker was reading from. Interview and webinar footage may not produce clean walkthroughs at all.
6. **Resolve granularity** — see Rule 11.3.
