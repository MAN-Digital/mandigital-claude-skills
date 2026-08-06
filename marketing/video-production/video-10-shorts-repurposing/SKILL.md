---
name: video-10-shorts-repurposing
description: Mines a finished long-form video's transcript for short-form vertical candidates and returns a scored candidate slate per platform — YouTube Shorts (sound-on lens) and LinkedIn vertical (mute-hook lens) — each with a Hook/Core/Close blueprint, a suggested title plus first-frame cover copy (the attention triad with the spoken hook — three surfaces, one niche, never duplicating; cover burned in at edit time, title seeding video-09's upload pass), word-exact spans, locate strings, and a CTA back to the long-form; then, on Diogo's selection, per-short CUT ORDERs for video-03-cuts. Use when the user says "make shorts from this", "repurpose the long-form", "find the reels in this video", "shorts candidates", "what shorts can we get out of this video", "cut a vertical from this", or drops a long-form transcript asking for short-form extraction. Standalone — runs outside the pipeline, on request only.
when_to_use: After a long-form cut is locked (ideally approved) and its transcript exists — word-level JSON preferred, back-catalog SRT/CSV accepted with degraded precision. Any request to extract or repurpose short-form clips from long-form content. On a mid-edit transcript only with the explicit warning that any recut voids every timecode issued.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/span_times.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/render_pdf.py *) Read Glob Grep Write AskUserQuestion
---

# Shorts Repurposing — long-form transcript → scored vertical candidate slate

Ports **Document 3 (Repurposing: Shorts and LinkedIn)** of the Claude Project
"Transcript Optimization" into the skill library, upgraded with word-level timing and
CUT ORDER execution. The project backup (Documents 1–4, Shared Foundations, Roadmap,
Essentials) lives in Drive at
`Video/04_Internal_SOPs/📚 Claude Projects/📃 Transcript Optimization/` — consult it
when a craft question exceeds what is encoded here.

Vendored copies of the two documents this skill's craft derives from — Document 3
itself and Shared Foundations — live in `references/` (self-containment pass,
2026-08-04): consult the Drive originals first (living versions), fall back to the
vendored copies when Drive is unreachable, and refresh them when a Drive read shows
differences. The rest of the project backup (Documents 1, 2, 4, Roadmap, Essentials,
channel data) stays Drive-only — it belongs to other skills' territory.

This skill is **read-only on the long-form**. It never proposes changes to the
long-form cut and never runs as a pipeline stage — Diogo asks for it, at or after
approval. Each selected short becomes a NEW deliverable built from a duplicated
sequence; the long-form survives untouched.

## Step 0 — facts before mining

1. **Which cut is this transcript?** The conformed word-level JSON of the cut the
   shorts will be built from (typically the final 16:9, e.g. `<name>_16x9_v7.json` in
   `04_Project_Assets/Transcripts/`). Mid-edit transcript → first line of the slate
   says: **a recut voids every timecode here**.
2. **The long-form CTA line.** Supplied per project — never invent one, never reuse
   another project's. If absent, ask.
3. **Platform set.** Always mine BOTH lenses (Shorts + LinkedIn), separately, and ship
   both slate files every run — even when the request names one platform (Diogo,
   2026-08-03: both outputs together work best). Skip a lens only when Diogo
   explicitly says to skip it.
4. **Language matching.** The cut's audio, captions, and overlays stay in the
   transcript's language.

**No padding, no parking.** There is no candidate cap: write a FULL candidate entry
for every moment that passes the platform's gates — never park a qualifying moment in
Near-misses because assembling it looks like work (Diogo, 2026-08-03: seeing the whole
structured suggestion beats having to commission it blind). Equally, never invent a
fourth or fifth candidate to fill a slate — a weak one helps nobody. Near-misses hold
only genuine rejects: moments that FAIL a gate (no sound-on hook for Shorts, no mute
hook for LinkedIn, dangling references, ASR-broken load-bearing lines), one line each
so the judgment stays inspectable.

**Rank strongest → weakest.** Open each slate with a **Slate note**: how many
candidates, which are the confident builds, and where the line sits. Any candidate
below that line carries a **Worth building?** block — the case for and the case
against — so Diogo decides from the finished script.

## The two lenses — same source, two harvests

Both platforms are 9:16 and share almost nothing else. Mine the long video twice; the
strongest moments usually differ per lens.

**Shorts lens** (sound-on autoplay, loop-driven, served broad):
- **Gate — sound-on hook:** the first 1–2 spoken seconds land a line that passes the
  Three Rules (below). No spoken hook → not a Shorts candidate.
- **Concreteness:** one imageable idea — a number, a named build, a sharp claim.
- **Self-containment:** works without the long-video context; no dangling references
  ("as I said earlier", unresolved "it/that"). Internal trims may *remove* a
  reference; nothing may be spoken *into* the clip to repair one.
- **Loop potential:** the close can feed the open, or the payoff rewards a rewatch.
- Ideal 15–60 s; up to 3 min allowed by the platform, tighter loops better.

**LinkedIn lens** (sound-off by default, POV-driven, served to the ICP):
- **Gate — mute hook:** first frame + first burned-in caption line carry the point
  with sound off. Hook depends on audio → not a LinkedIn candidate.
- **POV sharpness:** a belief-conflict or insight the ICP (Founders, CROs, RevOps
  leaders) reacts to.
- **ICP relevance:** names a real Founder/CRO/RevOps pain.
- **Comment invitation:** ends on a thought that invites a reply.
- Ideal 30–90 s, POV-forward; audio is a bonus, not the carrier.

**Three Rules gate on every hook and opener:** can the viewer **visualize** it, can it
be **falsified**, and could **nobody else sign** it. Contrast/antithesis is licensed in
the 0–2 s opener (and marked quotables) only; connective lines below the hook stay
affirmative. Point-don't-talk throughout: the number, the build, the integration — not
the adjective.

## ASR pass and the locate-string rule

Apply the known error patterns before mining (Claude / cloud; tool names; `Romeo Man`
→ `Romeo Mann` in personal names only; never alter `MAN Digital`). Every extracted
segment carries a **CTRL+F locate string of the raw source words exactly, errors
included** — that is what the editor searches in Premiere's transcript panel.
Corrections ride beside it as a bracket flag, never overwriting it. Heavy ASR noise on
a load-bearing word: raw words stay in the locate string, the suspected reading is a
bracket flag, the selected audio is never guessed (Tier 3 — listen-check).

## Boundaries and tiers (the word-level upgrade over Document 3)

- From a **word-level JSON**, every span boundary is word-exact, and the cut point
  sits in the **silence gap** between words (previous word's end → next word's
  start), never on a word onset. `span_times.py` reports both gaps at every boundary —
  a near-zero gap is a listen-check, not a clean cut.
- From a back-catalog **SRT/CSV**, boundaries are estimates: mark every time with ±
  tolerance, ship no exact spans, and say the editor cuts by locate string.
- Tiers inherited from video-02: **Tier 1** text-verifiable (span content, references,
  runtime arithmetic) — decide alone. **Tier 2** delivery-dependent (does a cold-open
  reorder land, cliffhanger vs closed loop) — propose both branches, Diogo decides.
  **Tier 3** whether a word is in the audio — never decide, route as listen-checks.

Verify every span before shipping:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/span_times.py find --json T.json --phrase "exact spoken words"
python3 ${CLAUDE_SKILL_DIR}/scripts/span_times.py span --json T.json --from "first words" --to "last words"
```

Math law: per candidate, Σ part lengths − internal trims = stated runtime, checked
before the slate ships.

## The procedure

1. **ASR pass** (above) on the transcript.
2. **Mine with the Shorts lens** — up to 3 A-tier candidates.
3. **Mine with the LinkedIn lens** — usually different moments, up to 3.
4. **Score and build each candidate**: concept angle, STRONG/PARTIAL/WEAK on the
   platform's four dimensions, Hook/Core/Close blueprint, word-exact spans, Fixed
   elements vs Creative freedom.
5. **Recommend**: per platform, the pick and the runner-up, one line of why. Diogo
   chooses; the slate is the opinion to react to.

## CTA — the bridge back to the long-form

The CTA rides in the **Close** beat, after the payoff. Mechanisms, per candidate:

1. **Existing spoken line** — only if a transcript line qualifies as an outro (rare).
2. **Text overlay / end card** — the CTA line renders on screen; no new footage
   (vertical graphic via video-06's standing-vertical variants).
3. **Recorded pickup** — the speaker reads the CTA to camera; always a flagged
   pickup, never assumed to exist.

Spoken CTA counts inside the length target; overlay-only CTA rides the payoff's tail.
LinkedIn cuts: the conversion CTA lives in the **post copy**, which routes to the
LinkedIn project — the video's close invites the comment instead.

## The attention stack — title · cover copy · hook (Diogo, 2026-08-06)

A Y candidate owns THREE simultaneous attention surfaces, and they work as one
system in one niche while each leverages its own medium: the TITLE is feed text —
the promise, search-shaped, declarative; the COVER COPY is an in-frame graphic
(placed between the speaker's face and the subtitles) — the itch, the scroll-stop;
the SPOKEN HOOK is audio — the claim that pays both off. Connected, never
duplicating: a surface that restates another wastes one of three shots at
attention. Write all three per candidate and check them AS A SET. (L candidates
carry no title element — that surface is the LinkedIn post's first line, which
belongs to the LinkedIn project.)

A Short uploads no thumbnail file: the feed and grid show its FIRST FRAMES, so
thumbnail-grade copy burned into those frames does the job a thumbnail does for a
horizontal video — and it must exist at EDIT time, in the slate, not arrive at upload
time in video-09's package. Every candidate card carries a **Cover copy** line in its
Hook beat (template above):

- **Derived from that candidate's own script** — look at the suggested spans and write
  the line as: "if you want copy in the first frames acting as the call to watch, use
  this." Never generic, never imported from another candidate.
- **The thumbnail SOP contract, one stage earlier:** the spoken hook states the claim,
  the cover copy creates the itch — connected, never duplicating. Restating the hook
  overlay wastes the frame; protect the information gap (never disclose what the video
  enumerates). Contrast is licensed here (it is a 0–2 s surface).
- **Y-series: mandatory.** L-series: the mute-hook caption already owns the first
  frames, so cover copy appears only when it adds something the caption doesn't —
  redundancy is worse than absence there.
- Production: 3–6 words, phone-legible, safe-zone — type/canvas rules live with
  video-06; the editor burns it during the edit. At upload time video-09's
  thumbnail-copy pass treats burned cover copy as the EXISTING thumbnail (analysis
  mode, not a fresh proposal); for horizontal videos nothing changes — their
  thumbnail copy still arrives in video-09's package.

## Output contract — two slate files, one per platform

Deliver into `04_Project_Assets/Shorts_Repurposing_Scripts/` (template folder since
2026-08-03; create it for older projects):

- `<transcript basename>.shorts-youtube.md` — the Shorts-lens slate
- `<transcript basename>.shorts-linkedin.md` — the LinkedIn-lens slate

Each `.md` ships with a rendered `.pdf` twin, same basename, for one-click visual
preview (Diogo, 2026-08-03): `python3 ${CLAUDE_SKILL_DIR}/scripts/render_pdf.py
<slate.md> …` (pandoc when installed, else markdown → styled HTML → Chromium-family
headless print — the house chain from the youtube-scripts export contract). PDFs
render from the final `.md` and are never edited independently; re-render after every
slate edit. If rendering fails, deliver the `.md` and flag the missing PDF — don't
block delivery on it.

Two files so Diogo works the platforms one by one (Diogo, 2026-08-03). Each file is
self-contained: header (source transcript + cut state + fps, CTA line verbatim,
timecode validity), that platform's candidates in the format below, Near-misses
(one-line reject reasons), Pickup list if any. A dual-qualified moment appears in
BOTH files, scored by each platform's own grammar, with a cross-reference note.
Summarize both slates in chat:

**Heading levels are load-bearing** — `render_pdf.py` styles by level, so a candidate
written as flat labeled lines renders as one unreadable paragraph blob (Diogo,
2026-08-03). `##` section · `###` candidate (becomes a bordered card) · `####` block
label · `#####` blueprint beat (becomes an accent chip). Blank line between every
block; labels bolded inline; scores and spans as TABLES, never prose. Verdict tokens
STRONG/PARTIAL/WEAK, RECOMMENDED, GATING and ⚑ are auto-badged — write them as bare
uppercase words so the renderer catches them.

```
### [Y|L][n] · "[short label]" — RECOMMENDED (on the pick only)

**Source** [hh:mm:ss:ff – hh:mm:ss:ff] · **Runtime** [n]s body + [n]s CTA = **[n]s**
   (branches, when they exist, as a small table: Branch | Body | Total | Trade)

**Angle** — [one sentence: why this moment works on this feed]

**Suggested title (Y)** "[≤ ~55 chars, declarative — leverages the hook; repeats
   neither the spoken words nor the cover copy. Seed for video-09's title pass]"

#### Score · [Platform] grammar

| Dimension | Verdict | Why |     ← the platform's four dimensions, one row each

#### Blueprint

##### Hook · 0:00–0:0X
- **Audio** (Shorts) / **Caption, carries the hook on mute** (LinkedIn) "[exact line]"
- **CTRL+F** `[raw source words]`   [ASR flag if relevant]
- **Overlay** [3–5 words; Shorts supports the spoken hook, LinkedIn IS the hook]
- **Cover copy (first frames)** "[3–6 words, thumbnail-grade — creates the itch the
  hook pays off; never restates the Overlay or the spoken words. Mandatory on Y
  candidates; on L candidates only when it adds something the mute-hook caption
  doesn't already carry]"

##### Core · [range]
- **Audio** "[exact words — the one idea + seed-fact]" · **CTRL+F** · **Overlay**

##### Close · [range]
- **Audio** "[exact words]" · **Overlay/Caption** [Shorts: loop line or CTA |
  LinkedIn: the comment-inviting thought]

#### Spans — word-exact

| Part | From TC | To TC | from_s | to_s | length_s |

#### Build notes

- **Internal trims** [exact spans removed, or "none"]
- **Checksum** [the arithmetic, and it must hold]
- **CTA mechanism** [1/2/3 from above]
- **Fixed elements** [non-negotiable: the hook, the seed-fact]
- **Creative freedom** [editor autonomy: B-roll, core pacing, close visual]

#### Risks & listen-checks

- [tight boundary gaps, Tier-2 branches, Tier-3 checks; ⚑ GATING on anything
  that blocks the build]

#### Worth building?          ← marginal candidates only, omit on confident builds
- **For** [the case to build it]
- **Against** [the case to skip it]
```

## Vertical production rules (16:9 → 9:16)

Dedicated vertical edit — never rotate or letterbox a 16:9 file. Reframe key visuals
to center for the narrow viewport. Burned-in captions: decisive on LinkedIn, strongly
advised on Shorts (the DaVinci caption template, via video-08). Captions and logos
inside the safe zone, clear of platform UI at top and bottom. Enlarge type for phone
legibility. Never mix aspect ratios mid-video. Brand visuals (fonts, grade, canvas
variants) live with video-06.

## Edge cases

- **Source already Shorts-length but horizontal:** a re-crop, not an extraction — the
  whole video becomes one vertical cut; skip the slate, produce the single re-crop spec.
- **No A-tier moment for a platform:** output zero or one, with a note. Never force it.

## Selection gate → execution handoff

When Diogo picks ("build Y1 and L2"), emit **one CUT ORDER per short** in the
video-02 format, with two adaptations: `sequence:` names a duplicate the executor
creates first (`<project>_SHORT1_9x16`), and the Cuts table is the **complement** of
the keep-spans (everything outside the short's parts, pre-sorted descending, plus any
cold-open reorder noted as a Deferred move — reorders are not plain cuts).
video-03-cuts executes under its normal safety protocol. Downstream by reference:
vertical reframe + graphics → video-06 · caption template + QA → video-08 · upload
subtitle tracks → video-09 in **Shorts** mode. Final upload metadata stays
video-09's territory — the slate's per-candidate title is a SEED for that pass,
not a bypass. Description and pinned comment remain OUT of scope, as does LinkedIn
post copy (routed to the LinkedIn project).

### Filing and colour label — part of the build, not an afterthought

Every short sequence the executor creates is filed and labelled **in the same pass that
builds it** (Diogo, 2026-08-05), so the project panel stays readable when eight shorts
land in one session:

1. **Bin — `00_Timelines/01_Active_Cuts`.** Duplicating a sequence drops the copy beside
   the original, which on these projects means the project root. Move it with
   `move_item_to_bin` (target `01_Active_Cuts`) and confirm with a `get_bin_contents`
   read-back. This is the same bin template video-03-cuts already respects; shorts are
   working timelines and live there with everything else. If the project has no such bin
   (non-template project), leave the copy where Premiere put it — never create bins
   uninvited.
2. **Colour label — by platform, via `set_color_label`:**

   | Lens | Label | `color_index` |
   |---|---|---|
   | YouTube Shorts (Y-series) | Rose | `6` |
   | LinkedIn vertical (L-series) | Blue | `9` |

   The label is what makes the two slates tellable apart at a glance in the panel, so it
   tracks the *lens*, not the candidate. Leave the long-form master's own label alone.

Verify both by read-back before reporting the build — `set_color_label` and
`move_item_to_bin` are writes, and the Premiere bridge reports success for writes that
did not land.

## Never

- Modify, or propose modifying, the long-form cut or any input file
- Invent a CTA line, or carry one over from another project
- Write unspoken words into a span — hooks and CTAs come from spoken material,
  overlays, or flagged pickups only
- List a candidate that fails its platform's defining gate, pad a slate to a quota,
  or hide the near-misses
- Treat Shorts and LinkedIn as one target, or ship one resized file for both
- Present an interpolated (SRT/CSV) boundary as word-exact, or overwrite a locate
  string with its correction
- Issue timecodes without naming the export they are keyed to, or ship a slate whose
  runtime checksums don't hold
- Auto-run from the pipeline — this skill starts only on Diogo's explicit request
