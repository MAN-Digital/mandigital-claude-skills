---
name: video-09-youtube-delivery
description: Post-approval YouTube subtitle delivery — takes the approved video's SRT (pipeline FLOW file or any orphan SRT), builds the punctuated verbatim EN track, a conservatively polished EN-GB track, and six sentence-level translations (PL, DE, FR, ES, PT-PT, UA), all filed into 06_Final_Delivery/Transcripts_&_Subtitles/. Use when the user says "upload to YouTube", "generate the YouTube subtitles", "make the language versions", "translate the subtitles", "subtitle files for YouTube", or points at an approved SRT for upload prep. Standalone — runs outside the pipeline, on request only.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*) Read Glob Grep Write AskUserQuestion
---

# YouTube Delivery — approved video → upload-ready language tracks

video-08 produces the **review artifact** (clean, punctuation-free, goes back into DaVinci).
This skill produces the **approved deliverables** (punctuated, multilingual, go to YouTube).
Different meaning, different destination — never mix the two. This skill never writes into
`04_Project_Assets/Transcripts/` and never alters its input files.

## Step 0 — the mode gate (ALWAYS ask, NEVER infer)

Ask via AskUserQuestion before anything else: **Shorts or long-form?**

- **Shorts** — the video carries the animated DaVinci caption template (popcorn, ~18-char
  guideline). The EN track keeps that segmentation.
- **Long-form** — no burned-in subtitles; the uploaded files are the only subtitles.
  EN is rebuilt to standard reading cues.

Inference from duration, aspect ratio, or measured cue width is banned (Diogo, 2026-08-03):
a 1–2-minute horizontal video with no burned subs looks exactly like a Short by every
measurable signal and isn't one. The mode is an editorial fact only Diogo knows.

## Inputs & source resolution

1. Diogo points at the approved SRT — typically
   `04_Project_Assets/Transcripts/<name> CORRECTED FLOW.srt`.
2. Glob its folder for the sibling `<name> CORRECTED.srt`. If present, it is the
   **punctuation source of truth**: video-08's word-identity guarantee means FLOW and
   CORRECTED contain identical words, so punctuation transfers by word-to-word mapping —
   no guessing.
3. **Orphan mode** (no sibling): reconstruct punctuation from sentence context. Flag any
   genuinely ambiguous boundary (⚑ timestamp + both readings) instead of silently picking.
4. If the input carries inline tags (legacy exports), `strip-tags` first.

## Procedure

All script calls: `python3 ${CLAUDE_SKILL_DIR}/scripts/youtube_srt.py <subcommand>`.

### 1 · EN — verbatim, punctuated

Words must match the approved file exactly — punctuation is the ONLY permitted change.
Non-native phrasing stays as spoken; this is the accessibility-faithful default track.

- **Shorts:** keep cue count and timing untouched; add commas, periods, apostrophes where
  CORRECTED (or reconstruction) says they belong. The 18-char width law does NOT apply to
  this file — it never re-enters DaVinci, so a comma pushing a cue to 19–20 chars is fine.
- **Long-form:** punctuate, then `sentences`, then `wrap --max-lines 1 --max-line 32` —
  every cue is ONE line, normal reading width, never popcorn (YouTube silently drops
  blink-length cues — Diogo, 2026-08-03; 32 chars keeps a cue on a single rendered line
  even on phones). Then `check --min-dur 0.8`: any cue under ~0.8 s (a one-word sentence
  like "Right?") gets merged into its neighbouring cue so YouTube can't skip it.
- Gate: `check EN.srt --words-from <approved source>` must pass before anything derives
  from this file.

### 2 · EN-GB — polished British, the translation pivot

Always sentence-level (run `sentences` on the punctuated EN), both modes, then wrapped to
one-line cues after the polish (`wrap --max-lines 1 --max-line 32`). Conservative
treatment ONLY:

- fix non-native grammar and idiom (article slips, preposition slips, tense agreement);
- British spellings (organisation, optimise, colour);
- never rewrite meaning, never compress, drop, or add content, never "improve" the
  argument; sentence count and timing stay locked to the scaffold.

### 3 · Six translations — from EN-GB, never from verbatim EN

PL · DE · FR · ES (es-ES) · PT-PT · UA (Ukrainian). Built sentence-by-sentence on the
EN-GB sentence scaffold (same spans and timings), with full-context awareness — per-cue
popcorn translation is banned (German verb-final order, Slavic reordering). Each language
then wraps independently to one-line cues (`wrap --max-lines 1 --max-line 32`), so cue
counts may differ per language after wrapping; sentence spans stay aligned.

- **Register:** modern B2B marketing voice. DE: Sie. FR: vous. PL: direct "Ty" (lowercase).
  ES: tú (es-ES marketing norm). PT-PT: European Portuguese, impersonal constructions over
  você. UA: ви.
- **Glossary stays English in every language** (grep each output to enforce): HubSpot ·
  MAN Digital · man.digital/blog · RevOps · MQL / SQL · ARC model · C-level · SDRs ·
  pre-sales · go-to-market · mid-market · CRM. Extend per project; when a term is
  borderline, keep English and ⚑ flag it.
- Numbers/currency: keep source formatting (2,750 adapts to locale convention only if the
  language demands it — when unsure, keep as-is).

### 4 · Validate everything

- `check` on every output file (timing monotonic, no overlaps, no tags, no empties).
- EN: `--words-from` the approved source (hard gate, step 1).
- Translations: sentence spans identical to the EN-GB scaffold before wrapping; after
  wrapping, `check --min-dur 0.8` per file and glossary grep clean.
- Spot-read 3 cues per language against the EN-GB sentence for meaning drift.

## Deliverables & naming

Everything into `06_Final_Delivery/Transcripts_&_Subtitles/`:

```
<video> EN.srt · <video> EN-GB.srt · <video> PL.srt · <video> DE.srt
<video> FR.srt · <video> ES.srt · <video> PT-PT.srt · <video> UA.srt
<video> — upload map.md
```

`UA` in filenames means Ukrainian — never "UK" (ISO 639-1 for Ukrainian is `uk`, which
collides with UK-English; the filename dodges the trap, the upload map resolves it).

The upload map is a short table: file → YouTube subtitle-language selection (EN → "English"
[the default/original track], EN-GB → "English (United Kingdom)", PL → Polish, DE → German,
FR → French, ES → "Spanish (Spain)", PT-PT → "Portuguese (Portugal)", UA → Ukrainian) plus
the mode that was chosen and the source file used.

## Never

- Infer Shorts vs long-form — always ask (Step 0)
- Change, add, or drop words in the verbatim EN track (punctuation only)
- Translate cue-by-cue from popcorn segmentation
- Derive translations or EN-GB from the verbatim non-native text when building — the pivot
  chain is fixed: approved SRT → EN (punctuated) → EN-GB → translations
- Use "UK" in a filename to mean Ukrainian
- Write into `04_Project_Assets/` or modify any input file
- Ship a file that failed `check`, or skip the EN words-match gate
- Auto-run from the pipeline — this skill starts only on Diogo's explicit request
