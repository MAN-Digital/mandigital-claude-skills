# Post-Recording Script Optimization — Rulebook for Skill Creation

**Purpose.** This document converts the reasoning used across one full optimization cycle into transferable rules. It is a design input for a Claude Code skill, not the skill itself. It records what was decided, why, which decisions generalise, and which do not.

**Source engagement.** MAN Digital, HubSpot Consulting Guide, 16:9 long-form. Raw 55:51 (903 ASR rows) to locked 39:39 (71% retained, 16:13 removed) across six review passes and seven distinct export states.

**Scope boundary.** This covers the cut of an already-recorded script. It does not cover writing scripts, metadata, or post-lock visual placement. It assumes the recording exists and cannot be economically re-shot, with pickups as the only recording-level remedy.

---

## PART 0 — SKILL IDENTITY

**What it does.** Takes a timecoded transcript export of a recorded session and returns a cut decision sheet: what dies, what survives, where the structure breaks, what needs verification by ear, and what needs a pickup.

**When it triggers.** Any of: a transcript export arrives after a recording; the person says "review this cut," "tighten this," "what should I remove," "does this still work"; a second or later export of a script already under review; the person describes repetition, stumbles, or restarts in a recording.

**Core output.** A decision sheet with three confidence tiers made explicit (see Part 1), every reference string reproduced raw-verbatim, and every claim measured against the file rather than recalled.

**Critical inversion.** The naive version of this skill reads a transcript, finds ungrammatical text, and reports it as a defect. That is wrong, and it is wrong most of the time. See Part 3.

---

## PART 1 — THE PRIME DIRECTIVE: THREE TIERS OF AUTHORITY

Everything else in this document is downstream of one fact: **the model reads text, the human hears audio.** Every rule must declare which of those two things it depends on. Failing to declare it is the primary failure mode of this task.

### Tier 1 — Model decides alone

Text-verifiable properties. No audio required. The model should state these as findings, not as questions.

- Duplication of content across the file
- Referential dependency across a proposed cut ("this," "that same problem," "another one")
- Sentence-boundary integrity at a seam
- Ordering against a source document (blog, brief, outline)
- Promise-to-payload mismatch (quantifiers, "here are some X")
- Enumeration integrity (items promised vs items surviving)
- Runtime arithmetic, retention ratios, section durations
- Repetition scanning, diffing between exports

### Tier 2 — Model proposes, human decides

Delivery-dependent. The text is ambiguous and only the audio resolves it. The model must present these as an either/or with both branches specified, never as a single recommendation.

- Whether a clause ending on a comma lands as a finished sentence
- Whether a pause reads as a full stop or a hesitation
- Which of two complete takes is better delivered
- Whether a self-correction can be cropped cleanly
- Whether an intonation supports a splice
- Whether a throat-clear is a throat-clear or a deliberate frame

### Tier 3 — Model must not decide

The model has no evidence at all. Asserting here destroys trust and costs the human real edit time.

- Whether a word is present in the audio
- Whether a proper noun was said correctly
- What a garbled ASR span actually says
- Whether an apparent grammatical break is a delivery break

**Rule 1.1.** Every finding carries its tier. A Tier 3 item written as a Tier 1 finding is a defect in the output, regardless of whether the guess happens to be right.

**Rule 1.2.** When a Tier 2 or Tier 3 item blocks a Tier 1 recommendation, state the Tier 1 recommendation conditionally and name the condition. Do not withhold the analysis pending verification.

**Rule 1.3.** Never report a Tier 3 item as a content problem. Report it as a verification item with a predicted resolution, and say what changes in each branch.

---

## PART 2 — EXPORT CLASSIFICATION (RUN FIRST, ALWAYS)

An export does not announce what it is. In this engagement, four structurally different artefacts arrived under the same filename and the same column headers. Analysing the wrong one produces confident nonsense.

Classify before reading. All four tests are mechanical.

### The four states

**A. Marked-up transcript.** Rows deleted from the transcript, timeline untouched. The removed durations get absorbed into the preceding row's end time.
*Detection:* total duration unchanged from source; rows are contiguous; some rows have absurd duration-to-word ratios. In this engagement, `portal.` was one word spanning 67.2 seconds and `any HubSpot consultant.` was three words spanning 110 seconds.
*Implication:* nothing has actually been cut. Playback still contains everything. Every restore is available. Source timecodes remain valid.

**B. Rippled cut.** The timeline has genuinely shortened.
*Detection:* total duration matches source minus the sum of removals; no rows with anomalous duration-to-word ratios.
*Implication:* all previously issued timecodes are now wrong by a cumulative, growing offset. Text search strings still work. Any downstream timing document must be re-conformed.

**C. Re-transcribed cut.** ASR re-run on the new sequence.
*Detection:* row count rises sharply while duration falls; row boundaries do not align with the previous export's boundaries.
*Implication:* row indices from earlier analysis are void. Text may differ from earlier exports even where the audio is identical.

**D. Hand-corrected transcript.** The human has typed over the ASR.
*Detection:* word-level diff against source shows substitutions that improve rather than remove (`for` becomes `Fourth thing`, `managed` becomes `MAN Digital`).
*Implication:* **raw-verbatim locate strings from earlier passes no longer match.** This is the state that silently breaks the referencing discipline.

### Rules

**Rule 2.1.** Run the classification before reading a single line for content. Report the state to the human in one sentence, because it changes what they can and cannot do next.

**Rule 2.2.** Detect state A with two checks: `duration(export) ≈ duration(source)` and `max(row_duration / word_count)`. A ratio above roughly 1.5 seconds per word on a multi-second row means absorbed material.

**Rule 2.3.** On state B, declare every previously issued timecode void and offer re-conforming. Do not silently reuse them.

**Rule 2.4.** On state D, re-verify every locate string against the new export before reusing it. A locate string is valid only against the export that generated it.

**Rule 2.5.** Never assume the previous export is still on disk. Re-derive state by diffing against the original source, which is the only stable reference.

---

## PART 3 — THE ASR TRUST MODEL

This is the highest-value section in the document and the one most likely to be got wrong by a naive implementation.

### The empirical result

Across this engagement, nine spans were flagged as possible transcription failures rather than content defects. **Nine out of nine came back from the human's audio check as transcription failures.** Zero were genuine delivery problems.

| Transcript read | Actually said |
| --- | --- |
| `for technical fit.` | "Fourth thing: technical fit." |
| `Going live doesn't mean the project,` | "...doesn't mean the project ended," |
| `Second, HubSpot and Sugden` | "Second, HubSpot consultants" |
| `human things, the system after going like` | "Who maintains the system after going live" |
| `and how success is` | "and how success is measured" |
| `maintaining it in managed. We use the Arc model` | "maintaining it. In MAN Digital we use the ARC model" |
| `where we are processes` | "where we architect processes" |
| `inside the pops` | "inside the HubSpot" |
| `that's a huge red` | "that's a huge red flag" |

Sample size is nine, one speaker, one ASR engine, one session. Treat the direction as robust and the rate as indicative.

### Where ASR fails

The failures are not random. They cluster in three places, and all three are places where structural meaning lives.

**Ordinals and list scaffolding.** "Fourth thing" became "for." The video enumerated six criteria as first, second, third, fourth, fifth, sixth, and the ASR dropped exactly one of them: the one where the ordinal was fused to a following noun phrase.

**Brand, product, and domain terms.** "MAN Digital" became "managed." "HubSpot consultants" became "HubSpot and Sugden." "MQL" and "SQL" became "MKL" and "X shell." "firmographics" became "Fillmore graphics." The lower the term's frequency in general English, the higher the failure rate, which means the terms carrying the most specific meaning fail most often.

**Terminal words of a clause.** "measured," "ended," "flag," "a month," "the hour," "€6,000." Unstressed sentence-final words get clipped. This is the class that makes a complete sentence look truncated.

### The inversion

A naive reading of "for technical fit." concludes: the fourth criterion lost its number, the list is broken, flag as a content defect. That conclusion is confidently wrong, it sends the human hunting for a problem that does not exist, and it costs credibility that the genuine findings then have to re-earn.

**Rule 3.1.** A grammatical break in a transcript is a transcription hypothesis, not a content finding. Default to transcription failure, not delivery failure.

**Rule 3.2.** Raise transcription suspicion to near-certainty when the break sits at any of: an ordinal or list-position word; a brand, product, or domain term; the terminal word of a clause; a numeral or unit.

**Rule 3.3.** Predict the likely true reading, state it as a prediction, and route it to the human as a listen-check. Never write it into the cut, and never treat the prediction as established in later reasoning.

**Rule 3.4 (referencing law, inherited and reinforced).** The search string is the raw ASR text including its errors, because that is what the transcript panel searches. The correction sits beside it in brackets. The correction never overwrites the string.

**Rule 3.5 (sibling scan).** When one instance of a class is confirmed, scan for siblings of the same class and batch them into a single listen-check. In this engagement, confirming `for` was `Fourth thing` justified checking every other ordinal-adjacent and brand-adjacent span, which closed four more flags in one round trip.

**Rule 3.6.** Where an ASR failure has dropped a load-bearing number or term (`and €30,000.` missing its floor, `2000 to 10,000 a` missing "month"), the remedy is on-screen text at that frame, not a cut and not a pickup. See Part 8.

---

## PART 4 — TAKE CONTESTS

When the same content was recorded more than once, the tests below run in order. Stop at the first that discriminates.

**Test 1 — Completeness.** Does the take finish its own thought? A take that breaks mid-clause loses to a complete one even when it is tighter and better phrased. Worked case: a governance restatement was tighter than its rival but ended on "Going live doesn't mean the project," and lost on that basis. It later turned out the ASR had dropped "ended" (Rule 3.1 applies), which is why Test 1 must be re-run after any transcription correction.

**Test 2 — Content superset.** Does the winner cover everything the loser did? Enumerate the losses explicitly. Do not let a take win on fluency while quietly dropping an idea.

**Test 3 — Fluency density.** Rows per second of runtime. A take delivered in five long runs beats one delivered in sixty-five one-second fragments, because fragmentation in the ASR row structure is a reliable proxy for restarts, hesitation, and false starts. Worked case: the consultant/admin/agency section existed as a 65-row, 1:48 fragmented pass and an 8-row, 2:52 fluent pass. The fluent pass won despite the fragmented one containing two extra ideas.

**Test 4 — Concreteness.** Prefer the take carrying the checkable specific: a number, a named example, a falsifiable claim.

**Test 5 — Landing.** Prefer the take that ends on its own payoff rather than trailing into the next topic.

**Test 6 — Self-direction.** If the speaker gave an on-mic instruction to the editor, it outranks the model's judgment on that specific decision. Worked case: "Let's cut this part with can-they-support run-the-model, and I would say again do they challenge weak requirements politely so you can mix it." That single line resolved a three-way ordering question. Always scan the raw transcript for these before scoring, and always name them when honouring them.

### The one-new-clause rescue

**Rule 4.1.** When a losing take contains exactly one idea the winner lacks, do not keep the whole take. Extract the clause, or flag it as an optional insert with its own timecode, and let the human decide.

Worked case: a losing governance restatement was 95% repetition, but contained one new clause, "that's usually when the problems start," which supplied the reason behind a red flag the winning take only asserted. The recommendation moved from "cut 15.5 seconds" to "cut 10 seconds and keep the reason." That refinement only appeared on the second pass, which is an argument for Part 9.

**Rule 4.2.** An optional insert must state that it comes from a different take, and must be flagged for frame and energy match, which is a Tier 2 check.

---

## PART 5 — SEAM LAW

### Three verdicts, and only three

Every seam created by a removal gets exactly one:

- **CLEAN** — no action. Say so explicitly. In this engagement ten of fourteen seams were clean, and reporting that was as useful as reporting the four that were not.
- **TRIM** — resolvable by cropping inside a row. Tier 2, because it depends on delivery. Specify both branches.
- **BREAK** — content is genuinely missing. Tier 1. Specify the restore with timecodes and verbatim text.

**Rule 5.1.** Report the clean seams as a set, not individually. The human needs to know what they do not have to look at.

### The three tests for any removal or lift

**Test A — Sentence boundary.** Full stop on both sides of the seam. A seam joining two full stops is structurally safe regardless of content.

**Test B — Referential dependency.** Does anything after the seam point back at the removed material? Scan forward for demonstratives without a new antecedent: "this," "that," "the same," "another one," "as I said."

**Test C — Structural load.** This is the test that is usually skipped and it is where the real risk sits. Ask what job the removed span was doing beyond conveying its own content. Was it a bridge, a landing, a payoff, a transition, an antecedent?

Worked case: lifting the CFO test out of the middle of the video to use as a cold open passed A and B cleanly. It failed C in a way that mattered: that passage was the landing of an escalation ladder (symptoms, then worse with AI, then messier with new markets, **then the one test that settles it**, then the detail). Removing it left the ladder climbing and then stopping. The seam was fine. The section shape was not.

**Rule 5.2.** Report Test C failures separately from Test A and B failures, because they need a different remedy. A and B failures need a restore or a re-cut. C failures usually need a replacement beat, which is often visual rather than verbal.

**Rule 5.3.** When the person asks "does this seam work," answer the seam question first and directly, then raise the structural-load finding as a separate observation. Do not let a shape concern read as a refusal to answer the question asked.

---

## PART 6 — INTEGRITY AUDITS (RUN AFTER EVERY PASS)

These are cheap, mechanical, Tier 1, and they catch things a seam-by-seam read does not.

### 6.1 Enumeration integrity

Count every list the speaker announces and verify the delivered items against the count.

Worked case: seven regional-fit questions were announced. After a cut pass, six survived. The seventh had been sitting between a duplicate and an on-mic direction note, and went out as collateral when both neighbours were removed. Nothing in the seam analysis flagged it, because the seam either side was clean. Only counting caught it.

**Rule 6.1.** After every pass, re-count every enumerated set against the source document and against the speaker's own stated count. Collateral loss is invisible at the seam and visible only in the count.

### 6.2 Promise and payload

Every quantifier creates a debt: "a few symptoms," "here are some scenarios," "there are four components," "three models."

Worked case: "There are a few symptoms" was followed by one symptom, delivered for twenty-five seconds. The other two lived in a take that had correctly lost a contest. The audio could not pay the debt.

**Rule 6.2.** Audit every quantifier against what follows. Where the audio cannot pay, check whether an on-screen asset can (Part 8) before proposing a cut or a pickup.

### 6.3 Collateral damage detection

**Rule 6.3.** Diff every new export against the previous one at word level and classify each change as: applied as specified, applied differently, not applied, or new. The "new" bucket is the one that earns trust and it is the one a naive implementation omits.

### 6.4 Asset misfiling

Sessions produce material for outputs other than the one being cut. It arrives in the same file.

Worked case: a Shorts call to action ("We talk about this and much more in a longer form video") sat at the end of the long-form timeline. On the long-form it tells the viewer to go and watch the video they are already watching. It was correctly parked there deliberately by the editor as a colour-coded reference clip, which is a good practice, but the skill must still flag it every time and must route rather than delete.

**Rule 6.4.** Detect misfiled assets by: content referring to the current output as external; a CTA whose platform grammar does not match the output; production chatter adjacent to a clean take. Flag, name the correct destination, and never propose deletion. The default assumption is that the human parked it on purpose.

### 6.5 Repetition scan

**Rule 6.5.** Run a sliding-window similarity scan across the whole file after every pass, not only at the start. The scan should report zero surviving repetition before a cut is called locked. In this engagement, one repetition survived to the fifth pass because every earlier scan had correctly deprioritised it behind larger ones.

---

## PART 7 — THE NARRATIVE LAYER

Everything above operates at the seam. This operates above it, and it is a separate pass with a separate trigger. Do not attempt it until the seams are stable, because narrative findings become void every time a block moves.

### 7.1 Agenda audit

If the speaker states an agenda, check that every promised item is delivered, in order. Worked case: six promised, six delivered, in order, no drift. That is a finding worth reporting as a strength, and it is also what makes chapter markers viable.

### 7.2 Time to first stake

Measure the runtime before anything is at risk. Enumeration, taxonomy, and definition are not stakes.

Worked case: eleven minutes of mechanism before the first pain beat, in a forty-minute video. Minutes 2:21 to 11:17 were two consecutive enumerations, four components then seven lifecycle stages. Nine minutes of list at the point where viewers decide whether to stay.

**Rule 7.1.** Report time-to-first-stake as a ratio of runtime. Above roughly a quarter, raise it.

### 7.3 The shape diagnosis, and the cheap fix

A video derived from a reference document inherits the document's shape. A reader of a reference document jumps to the section they want. A viewer cannot.

**Rule 7.2.** When the source is a reference document, the primary remedy is chapter markers rather than restructuring, because chapters restore the scannability the format lost. Propose the restructure only as a second option and cost it honestly.

**Rule 7.3 (cold-open candidacy).** Scan the body for the strongest falsifiable, visualisable claim and test it as frame one. Criteria: it survives without setup, it names a specific failure the target viewer recognises in themselves, and no one else could sign it. Worked case: "if your CFO doesn't trust the revenue data in your HubSpot, they do different calculation in Excel, that means that your system has a problem," lifted from 13:15 to 0:00.

**Rule 7.4 (frame-one audit).** Once a cold open exists, audit its first two seconds for throat-clears and its last eight for mush. Both were present in the first attempt here. The tail of the lifted passage was eight seconds of self-correction sitting in the most valuable position in the video.

### 7.4 Section shape

**Rule 7.5.** For each section, classify the shape as rise-land, rise-stop-reset, or flat. Rise-stop-reset usually means a landing beat is missing or was cut.

**Rule 7.6 (deflating closer).** Flag any section that peaks and then adds a weak summary. Worked case: a section built to "a good consultant will always say no" and then closed on "So these are just one of the questions that you could ask." Cutting twelve seconds moved the section close onto its own peak and improved the transition into the next chapter.

**Rule 7.7 (self-sabotage scan).** Flag any line where the speaker undercuts their own material, especially near a CTA. Worked case: "this is something that is boring, I know" sat thirty seconds before the call to action.

### 7.5 Outro audit

**Rule 7.8.** Check the close for: a recap that names nothing; a double close (content close followed by CTA close); a missing destination; no forward path. Where a motion graphic will carry the CTA visually, the audio recap becomes redundant rather than merely weak, and cutting it improves the handoff. Worked case: cutting eight seconds of empty recap left the graphic cued by "and that's how you are bringing more revenue in your organizations," which is a payoff line.

---

## PART 8 — THE VISUAL ESCAPE HATCH

Some text-level defects cannot be fixed by cutting and do not justify a pickup. Check the visual layer before proposing either.

**Rule 8.1.** Before recommending a cut or a pickup for a defect, ask whether an on-screen asset can carry it. Three categories qualify:

- **Dropped data.** ASR-clipped numbers and units. The graphic supplies "€6,000" and "per month" and the audio gap becomes invisible.
- **Unpaid promises.** A four-panel graphic delivers the "few symptoms" the audio names one of.
- **Missing structure.** A numbered column lights up and supplies an ordinal the speaker never said, or that the ASR dropped.

**Rule 8.2.** When a single asset solves two independent problems at the same frame, treat that as strong evidence it belongs there, and say so. Worked case: one graphic simultaneously paid the "few symptoms" debt and supplied the landing beat lost when the CFO test was lifted.

**Rule 8.3.** A visual remedy is a placement constraint, not a suggestion. Record it as a requirement on the graphics map with its cue string, because the cut now depends on it.

---

## PART 9 — ITERATION PROTOCOL

This engagement took six passes. The protocol is most of why it converged.

**Rule 9.1 — One export at a time, with a review gate.** Never analyse two states at once.

**Rule 9.2 — Four-way change classification.** Every item from the previous pass is reported as applied, applied differently, not applied, or superseded. Nothing silently disappears.

**Rule 9.3 — Report what got worse.** Every pass produces regressions. Two examples from this engagement: a trim pass clipped the word "flag" off a red-flag payoff; another trimmed four function words out of a single sentence and left "where we are processes," "Then run then we compound," and "we add AI top of it." Both were introduced by tightening, not present in the source. A skill that only reports progress will not be trusted on the pass where it matters.

**Rule 9.4 — Credit the better solution.** When the human solves something differently and better, say so plainly. Worked case: the integration repeat was solved by cutting the first instance rather than the second, which also disposed of an orphaned connector. Another: dropping "Or they are." made "they are actually ashamed. They fear that..." read as one thought, which was better than the proposed trim.

**Rule 9.5 — Re-run the Tier 1 audits every pass.** Enumeration, promise/payload, repetition scan, and word-level diff. Cheap, and they catch regressions.

**Rule 9.6 — Answer the asked question first.** When the human asks a specific question ("does this seam work"), lead with a direct verdict, then add findings. Analysis offered in place of an answer reads as evasion.

**Rule 9.7 — Runtime is an outcome, reported every pass.** 55:51, 45:02, 45:06, 44:55, 40:18, 40:09, 39:39. Never a target.

---

## PART 10 — VERIFICATION DISCIPLINE

**Rule 10.1.** Every number is measured from the file in the current turn. Never recalled from an earlier turn, never estimated. Timecodes drift, exports change, and a stale number is worse than no number.

**Rule 10.2.** Every quoted string is verified to exist verbatim in the source before it ships. In this engagement an automated check caught two strings where an ellipsis had been introduced into what was supposed to be a raw search string.

**Rule 10.3.** Parse defensively. Transcript CSVs carry multi-line fields and non-standard delimiters. Line-count commands lie. Use a real CSV parser with the field size limit raised.

**Rule 10.4.** Derive frame rate from the data, by taking the maximum frame value observed, rather than assuming.

**Rule 10.5.** Prefer difflib over regex for structural comparison. Word-level `SequenceMatcher` between two exports produces the change list directly.

---

## PART 11 — WHAT DOES NOT GENERALISE

Stating the limits is what makes the rest usable.

**Speaker-specific.** This speaker's pause patterns, restart habits, and the specific ASR error signature belong to one voice and one engine. The nine-for-nine result on transcription failures is directional, not a constant. A different speaker or engine changes the base rate.

**Domain-specific.** The brand and product terms that break ASR are specific to this vocabulary. The skill should accept a domain glossary as an input rather than hard-coding a list.

**Format-specific.** Time-to-first-stake thresholds, acceptable enumeration density, and runtime norms differ between a pillar guide, a case study, and a vertical. These belong in a per-format configuration, not in the rules.

**Judgment that stayed human.** Which of two well-delivered takes has better energy. Whether a pause carries weight. Whether a self-deprecating line is charming or costly. Whether a proprietary framework is worth a pickup. The skill's job is to surface these cleanly with both branches costed, not to resolve them.

**One engagement.** Every rule here derives from a single project. Rules earned from one case are hypotheses with a falsification path, not laws. They should be graded as such and revised as more cycles run.
---

## PART 12 — SUGGESTED SKILL ARCHITECTURE

A recommendation for how to slice this into a skill, based on what actually carried weight in the engagement.

### Triggering

The description should be pushy, because this skill will undertrigger. It should fire on any transcript export arriving after a recording, not only on an explicit "optimize this script." Phrases observed in this engagement that should trigger it: "review it once again," "just tightened the v3," "here's the final export," "review the narrative," "does this still work without that sentence."

It should also fire on the second and subsequent exports of a file already under review, because iteration is the mode where most of the value appeared.

### Body structure

Order the SKILL.md so the model cannot skip the two gates that prevent confident nonsense:

1. **Gate 1: classify the export** (Part 2). Mechanical, cheap, and it changes everything downstream.
2. **Gate 2: declare the tier model** (Part 1). Every finding carries a tier.
3. Then the analysis passes, in order: transcription-suspicion scan, repetition scan, seam classification, integrity audits, narrative layer.
4. Then output assembly.

Put the ASR trust model (Part 3) high in the body rather than in a reference file. It is the rule most likely to be skipped and the one whose absence does the most damage.

### Bundled resources

- **`diagnostics.py`** (provided alongside this document). Export classification, repetition scan, seam extraction, word-level diff between exports, enumeration audit, runtime arithmetic. Everything mechanical should be a script rather than a model judgment, both for accuracy and for token cost.
- **`glossary.json`** per client. Brand terms, product names, framework names, and their common ASR corruptions. Populated from confirmed corrections as cycles accumulate. From this engagement: MAN Digital (managed, man digital), MQL (MKL, MQ), SQL (X shell, QL), HubSpot consultants (HubSpot and Sugden), firmographics (Fillmore graphics), go-live (go life, going like), ARC model (Arc), Romeo Mann (Romeo Man), peel the onion (build the onion), errors and routing (arrows and routine), governance (governments).
- **`format-profiles.json`**. Per output format: expected runtime band, time-to-first-stake threshold, enumeration density ceiling, whether a cold open is expected.
- **`output-template.md`**. The decision sheet structure, so the shape stays stable across passes and the human can diff one pass against the next.

### Output contract

Every pass returns, in this order:

1. **Export state and runtime**, one line.
2. **Direct answer** to any question the human asked, before anything else.
3. **What closed** since the last pass, as a list.
4. **What is open**, ordered by severity, each with: timecode, raw-verbatim locate string, tier, and the specific remedy.
5. **What got worse**, always present as a heading even when empty.
6. **Listen-checks**, batched, with predicted readings.
7. **Runtime projection** if the open items are actioned.

The "what got worse" heading being present when empty is deliberate. It signals the check was run.

### Anti-patterns to encode as negative instructions

- Do not report an ungrammatical span as a content defect without first applying Rule 3.1.
- Do not issue timecodes without declaring which export they are keyed to.
- Do not reuse a locate string across exports without re-verifying it.
- Do not propose a cut for a defect the visual layer can carry.
- Do not answer a narrow question with a broad analysis.
- Do not report only the problems. Report the clean seams as a set.
- Do not recommend deleting anything that looks like a parked asset. Route it.
- Do not pad a findings list. A pass with three findings is a pass with three findings.

---

## PART 13 — DECISION FLOW

Compressed to a routable sequence.

```
INPUT: transcript export (+ optional: source doc, previous export, glossary)

1  CLASSIFY EXPORT ....................... Part 2
   A marked-up | B rippled | C re-transcribed | D hand-corrected
   -> report state; void stale timecodes; re-verify locate strings if D

2  IF previous export exists:
     WORD-LEVEL DIFF .................... Rule 6.3
     -> classify every change: applied / applied-differently / not-applied / new
     -> the "new" bucket is the regression report

3  TRANSCRIPTION SUSPICION SCAN ......... Part 3
   flag spans at: ordinals | brand+domain terms | clause-terminal words | numerals
   -> predicted reading + batch as listen-checks (Tier 3)
   -> DO NOT classify any of these as content defects

4  REPETITION SCAN ...................... Rule 6.5
   sliding window similarity, whole file
   -> take contests -> Part 4 tests in order
   -> scan raw transcript for on-mic self-direction FIRST (Test 6 outranks)

5  SEAM CLASSIFICATION .................. Part 5
   for each removal: Test A boundary | Test B reference | Test C structural load
   -> CLEAN (report as set) | TRIM (Tier 2, both branches) | BREAK (Tier 1, restore spec)

6  INTEGRITY AUDITS ..................... Part 6
   enumeration count | promise vs payload | asset misfiling
   -> these catch what seam analysis structurally cannot

7  VISUAL ESCAPE HATCH .................. Part 8
   for each unresolved defect: can an on-screen asset carry it?
   -> if yes, convert to a placement constraint, not a cut

8  NARRATIVE LAYER ...................... Part 7
   ONLY when seams are stable
   agenda audit | time-to-first-stake | section shapes | cold-open candidacy
   | deflating closers | self-sabotage | outro audit

9  ASSEMBLE OUTPUT ...................... Part 12 output contract
   runtime projection; every string verified verbatim; every number measured
```

---

## APPENDIX A — WORKED CASES

Few-shot material. Each pairs a decision with the rule it exercises.

**A1. The export that had not been cut.**
Second export arrived, 216 rows shorter, duration unchanged at 55:48. Detection: `portal.` spanned 67.2 seconds as a single word. Diagnosis: marked-up transcript, media intact. Consequence reported to the human: nothing destroyed, every restore available, all source timecodes still valid, but the flow cannot be auditioned by playback yet. *Exercises: Rules 2.1, 2.2.*

**A2. "for technical fit."**
Read as a broken fourth item in a six-item enumeration and reported as a structural break. The human checked the audio: "Fourth thing: technical fit." The enumeration was never broken. The correct handling was to predict the reading and route it as a listen-check. This single case reframed the whole engagement and produced Part 3. *Exercises: Rules 3.1, 3.2, 3.3.*

**A3. The seventh question that vanished.**
A duplicate take and an on-mic direction note were removed in one pass. A distinct question sat between them and went with them. Both resulting seams were clean, so seam analysis could not detect it. Counting the enumerated set against the source document did. *Exercises: Rule 6.1.*

**A4. The take that won on completeness and then lost the argument.**
A governance restatement was rejected because it ended on "Going live doesn't mean the project," judged incomplete. Later a transcription correction revealed "project ended," making it a well-formed sentence. The recommendation survived, but on repetition grounds rather than grammatical grounds, and the stated reason had to be corrected. *Exercises: Rules 3.1, 4.1, and the requirement to re-run Test 1 after corrections.*

**A5. The one-new-clause rescue.**
The same passage was 95% repetition but contained "that's usually when the problems start," which supplied the reason behind a red flag the surviving take only asserted. The recommendation shifted from a fifteen-second blanket cut to a ten-second cut preserving the reason. *Exercises: Rule 4.1.*

**A6. The lift that passed two tests and failed the third.**
Moving the CFO test to a cold open passed the sentence-boundary test and the referential-dependency test cleanly. It failed structural load: the passage was the landing of an escalation ladder. The answer to the human's question ("is this solid enough?") was yes, followed by a named cost and a visual remedy. *Exercises: Rules 5.1, 5.2, 5.3, 8.2.*

**A7. The graphic doing two jobs at one frame.**
A four-panel health-monitor graphic simultaneously paid the "a few symptoms" debt the audio could not, and supplied the landing beat lost to A6. Reported as evidence the asset belonged at that exact cue. *Exercises: Rules 6.2, 8.1, 8.2.*

**A8. Tightening that broke four things.**
A tightening pass removed function words across one sentence, leaving "where we are processes," "Then run then we compound," "we add AI top of it," and "so that compounds." All four were introduced by the pass, none present in the source. Reported under "what got worse." Three were later restored; the fourth turned out to be an ASR failure ("where we architect"). *Exercises: Rules 9.3, 3.1.*

**A9. The word that got clipped.**
A trim removed roughly six seconds around a red-flag payoff and the transcript read "that's a huge red." Flagged as a possible clipped word rather than a content problem. The human confirmed the audio was intact. *Exercises: Rules 3.1, 3.3, 9.3.*

**A10. The parked asset.**
A Shorts CTA sat at the end of the long-form timeline across several exports. Flagged each time as misfiled, with the correct destination named and deletion never proposed. It turned out to be deliberately parked, colour-coded in the timeline, so as not to lose the clip before the vertical cut. The flag was still correct to raise, and the handling (route, never delete) was what made it harmless. *Exercises: Rule 6.4.*

**A11. The human's better solution.**
An integration repeat was proposed for removal by cutting the second instance. The human cut the first instance instead, which also resolved an orphaned connector left dangling by an earlier pass. Credited plainly. *Exercises: Rule 9.4.*

**A12. Runtime pushback, graded.**
A 45:00 first cut was measured against the channel catalogue: every long-form over forty minutes was a podcast-format interview at 11 to 187 views, while the one breakout long-form was 27 minutes. Reported as measured-from-our-files, with the confound named explicitly (length was entangled with format and vintage), and three specific trim spans offered rather than a vague "make it shorter." *Exercises: Rules 9.7, 10.1, and evidence grading.*

---

## APPENDIX B — EVIDENCE GRADES ON THE RULES

| Rule area | Grade | Basis |
| --- | --- | --- |
| Export classification (Part 2) | **A** | Four states observed and mechanically distinguished in one engagement |
| ASR trust model (Part 3) | **A** for direction, **C** for rate | 9/9 confirmed, n=9, one speaker, one engine |
| Take contest ordering (Part 4) | **B** | Inherited from the existing SOP, validated against eleven contests |
| Seam law three tests (Part 5) | **A** for A and B, **C** for C | A and B are mechanical; structural load is a heuristic with one strong case |
| Enumeration integrity (6.1) | **A** | Caught a real loss that seam analysis structurally could not |
| Promise/payload (6.2) | **B** | Two clear instances |
| Visual escape hatch (Part 8) | **C** | Compelling but derived from three cases in one project |
| Narrative thresholds (Part 7) | **D** | Craft heuristics, no measurement behind the specific numbers |
| Iteration protocol (Part 9) | **B** | Six passes converged; the counterfactual is untested |

Grades follow the project convention: **[A]** measured from our files, **[B]** external validated, **[C]** hypothesis with a falsification path, **[D]** craft heuristic.

---

## APPENDIX C — OPEN QUESTIONS FOR THE SKILL BUILD

Worth resolving during skill creation rather than discovering in production.

1. **Where does the source document fit?** This engagement compared the transcript against a published blog post throughout, and the comparison drove enumeration audits, ordering checks, and the graphics map. Should the source document be a required input, an optional one, or a separate mode?

2. **How much should be script versus model?** Everything in Part 6 is mechanical. Pushing it into `diagnostics.py` improves accuracy and cuts cost, but risks the model treating script output as the whole finding rather than as input to judgment.

3. **Does the narrative layer belong in the same skill?** It has a different trigger, a different cadence, and it goes stale whenever a block moves. A separate skill invoked at lock might be cleaner.

4. **Should listen-checks block?** Nine out of nine resolved as predicted. That argues for proceeding on the prediction while flagging it. It also argues the opposite: a 100% rate means asking is cheap and reliable. Probably: proceed conditionally, never write the prediction into the cut.

5. **How does the glossary get populated?** Manually per client, or accumulated automatically from confirmed corrections across cycles? The second is more valuable and needs a persistence decision.

6. **What is the stopping rule?** This engagement stopped when the human declared v5 final. A skill should have a defensible position on when a cut is locked: probably zero surviving repetition, zero open Tier 1 findings, all enumerations intact, and every listen-check resolved.
