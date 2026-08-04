# Output & Export Contract

This defines the _shape_ of the output and the export process for the two delivered files.
It contains no brand, product, or voice rules — those live in
[voice-and-positioning.md](voice-and-positioning.md),
[banned-words.md](banned-words.md), and
[non-native-readability.md](non-native-readability.md). This file governs format, file
boundaries, and handoff only.

Every script this skill produces ends in **two documents**, never one merged file: a Reader
Script for the person on camera, and a Visual Cue Sheet for the motion-graphics/video
editor. Physically that is **four files** (§7.2): the Reader Script `.txt`, the Cue Sheet
as `.md` plus a rendered `.pdf` twin, and a `readme.txt` recording the source video link,
transcript, and fact-check status. If the source material is a screen-share tutorial with many on-screen frames, see
[video-grounded-storyboard.md](video-grounded-storyboard.md) before building the Cue Sheet —
grounding the cue sheet in the actual source video keeps the two files in sync instead of
guessing at screen timing from a transcript.

---

## 1. Output contract

One run produces **one response** containing five parts, in this order:

| #   | Part                              | Form                   | Destination                              |
| --- | --------------------------------- | ---------------------- | ---------------------------------------- |
| 1   | Header                            | Inline in the response | Read once, discarded                     |
| 2   | Blueprint                         | Inline in the response | Sanity-check, discarded                  |
| 3   | **Document A — Reader Script**    | **Separate file**      | Teleprompter operator / on-camera reader |
| 4   | **Document B — Visual Cue Sheet** | **Separate file**      | Motion-graphics builder / video editor   |
| 5   | Flags                             | Inline in the response | Reviewer                                 |

Parts 1, 2, and 5 stay in the chat response. Parts 3 and 4 are **always exported as two
distinct files** — never merged, never a single file with two sections.

If the requester asks for "blueprint only," stop after part 2 and wait.

---

## 2. Header — template

```
Track: {{TRACK}}
Target length: {{MM:SS}} ({{WPM}} wpm → ~{{WORD_COUNT}} words)
Source: {{SOURCE_TITLE}} — {{SOURCE_URL_OR_FILENAME}}
Assumptions: {{WHAT_WAS_INFERRED_RATHER_THAN_GIVEN}}
```

State every inference explicitly. If track or length was inferred rather than supplied
(because the two gating questions in `SKILL.md` weren't asked or answered — they must be),
say so on its own line.

---

## 3. Blueprint — template

One row per beat. Budgets must sum to the target length. Map beats onto this skill's own
structures in [script-templates.md](script-templates.md) (cold open, why it matters,
walkthrough, mistakes, recap, CTA for long-form; single point → proof → CTA for shorts).

```
| # | Beat | Purpose (one line) | Budget | Words @ {{WPM}} wpm |
|---|------|--------------------|--------|---------------------|
| 1 | {{BEAT_NAME}} | {{WHY_THIS_BEAT_EXISTS}} | {{M:SS}} | {{N}} |
| 2 | ... | ... | ... | ... |
| — | **Total** | — | **{{MM:SS}}** | **{{TOTAL}}** |
```

Rules:

- Beat 1 carries the core promise. No rhetorical hook — state the consequence (see
  non-native-readability.md).
- No "Conclusion" or "References" beat.
- Word budget = budget in minutes × chosen wpm. Pick one wpm for the whole script and state
  it — 150 wpm is the MAN Digital default for a direct, unhurried delivery; adjust per
  presenter if needed.
- Running timecode for each beat starts at 00:00 and accumulates — the Cue Sheet depends on
  these numbers.
- If a source video was analyzed (see video-grounded-storyboard.md), use its event order to
  plan beats, but never copy its timestamps — this script has its own pacing.

---

## 4. Document A — Reader Script

### 4.1 What it is

The only file the person on camera sees. It scrolls on a prompter. Anything in it that is
not meant to be spoken is a hazard, because a reader under load will read it aloud.

### 4.2 Content rules

- One idea per line, 8–15 words (see non-native-readability.md). Hard line break after each.
- **Max two lines per chunk, then a blank line. No exceptions.** This is the single most
  repeated piece of on-set feedback: "Two lines, space, two lines, space is the best…
  if there is space between them, I have time to breathe." A chunk of 3+ consecutive lines
  scrolls too fast to read, and Romeo stops the take. The blank line IS the pacing — the
  reader breathes where the whitespace is.
- Beat separator (blank line, short marker, blank line) = full stop, new section. Beats are
  the script's chapters — every long-form script must have them, visible to the reader, so
  he always knows which chapter he is in.
- **Enumerations: one item per line, each opening with a spoken ordinal** — `One: …` /
  `Two: …` / `Three: …` (words, since they're read aloud; never bare digits, never a dash).
  Without a visible marker per item the reader loses his place mid-list and the delivery
  goes robotic: "we need these type of things, like one… because I don't know which one is
  it." Never bury a list inside a prose sentence.
- A line that must land (an emphasis beat like "This is where AI gets interesting.") sits
  **isolated — blank line above and below** — so the reader can pause and give it weight.
- Question lines keep their question mark — it carries the reader's intonation (see
  non-native-readability.md).
- **No visual references of any kind** — no `[VISUAL]` markers, no graphic numbers, no
  brackets pointing at anything on screen.
- No audience-directed questions, no hedging, no passive voice — enforced by
  non-native-readability.md (structural self-answered questions are allowed).
- Delivery cues default **OFF**: pace is encoded in layout only (blank-line rules above), and
  the file contains spoken lines exclusively. Turn ON only if the presenter specifically
  wants bracketed cues (`[pause]`, `[slow down]`, `[land this]`), sparse and never inside a
  spoken line.
- No colors, fonts, or display settings — those belong to the prompter operator's own SOP.
  (For reference: the settings that worked on set 2026-07-30 were scroll speed 75 / font
  size 73 — the operator's numbers, not the script's concern.)

### 4.3 Body template

```
{{SPOKEN LINE}}

{{SPOKEN LINE}}
{{SPOKEN LINE — continues the same thought, no breath between; a chunk NEVER exceeds two lines}}

{{SPOKEN LINE THAT MUST LAND — isolated by blank lines above and below}}

One: {{FIRST LIST ITEM ON ITS OWN LINE}}
Two: {{SECOND LIST ITEM ON ITS OWN LINE}}

Three: {{THIRD LIST ITEM — list items pair up in two-line chunks like everything else}}

---

{{FIRST SPOKEN LINE OF THE NEXT BEAT}}
```

Use `---` (or a single repeated character on its own line) as the beat separator **only if**
the prompter app strips or ignores it. If it does not, use two blank lines instead. Confirm
this once per prompter app and record the answer in §7.6.

### 4.4 Front matter

Keep it minimal and physically separated from line 1 of the script.

```
{{TITLE}} — Reader Script
{{VERSION}} · {{DATE}} · ~{{MM:SS}} @ {{WPM}} wpm

=== SCRIPT STARTS BELOW THIS LINE ===
```

The separator line exists so the operator can scroll past it and start the prompter on the
first spoken word.

---

## 5. Document B — Visual Cue Sheet

### 5.1 What it is

The only file the motion-graphics builder needs. It lists every visual in script order and
tells the builder exactly where in the narration each one lands.

### 5.2 Content rules

- Numbered sequentially, in the order the visuals appear.
- Every entry carries three things: **number**, **anchor**, **description**.
- The **anchor** is the join key between the two files: beat name + approximate timecode +
  the exact spoken line the graphic lands on, quoted verbatim from Document A.
- Describe **what the visual shows** (content), not how to design it.
- Mark each visual as a **rebuild** of a source graphic/video or **newly composed** from
  source text. If it's a rebuild of a screen from an analyzed source video, cite the
  video-events timestamp it came from (see video-grounded-storyboard.md) so the editor can
  check the original frame.
- Give every number-heavy or structurally dense point a visual anchor where one exists.
- **Not a second copy of the script.** No spoken lines beyond the short anchor quote.

### 5.3 Entry template

```
### V{{N}} — {{SHORT_LABEL}}

- **Beat:** {{BEAT_NAME}}
- **Timecode:** ~{{M:SS}}
- **Lands on line:** "{{EXACT_LINE_COPIED_FROM_DOCUMENT_A}}"
- **Origin:** {{Rebuild of source graphic/video {{ID}} at {{SOURCE_TIMESTAMP}} | Newly composed from {{SECTION}}}}
- **Shows:** {{WHAT_IS_ON_SCREEN — elements, relationships, labels, sequence}}
- **Holds for:** {{DURATION_OR_UNTIL_LINE}}
- **Notes:** {{CONSTRAINTS — e.g. figures illegible in source, do not quote numbers on screen}}
```

### 5.4 Compact table alternative

For short scripts, one table is acceptable in place of §5.3:

```
| # | Beat | ~TC | Lands on line | Origin | Shows |
|---|------|-----|---------------|--------|-------|
| V1 | {{BEAT}} | {{M:SS}} | "{{LINE}}" | {{Rebuild/New}} | {{CONTENT}} |
```

---

## 6. Flags — template

```
Flags:
- Source gap: {{WHAT_THE_SOURCE_LACKED_THAT_THE_SCRIPT_NEEDED}}
- Claim dropped: {{CLAIM}} — reason: {{UNSOURCED / PROJECTION / STALE}}
- Tension: {{WHERE_BRIEF_AND_SOURCE_DISAGREED_AND_WHICH_WON}}
- Open decision: {{WHAT_THE_REVIEWER_MUST_RESOLVE}}
```

If there are none, write `Flags: none.` Do not omit the line.

---

## 7. Export process

### 7.1 The firewall

The two files exist because two different people consume them under different conditions.
The reader is under performance load and reads whatever is on screen. The builder needs
placement precision the reader must never see.

|                   | Reader Script           | Cue Sheet            |
| ----------------- | ----------------------- | -------------------- |
| Spoken lines      | All of them             | Anchor quotes only   |
| Visual references | **None**                | All of them          |
| Timecodes         | None                    | Yes                  |
| Beat names        | Separator only, or none | Yes                  |
| Design direction  | None                    | Content, not styling |

A single visual marker leaking into the Reader Script is an export failure, not a cosmetic
one. Check for it explicitly (§7.6).

### 7.2 File naming

Every export is **five files**:

```
{{YYYY-MM-DD}}_{{SLUG}}_ReaderScript_v{{N}}.txt
{{YYYY-MM-DD}}_{{SLUG}}_ReaderScript_v{{N}}.pdf
{{YYYY-MM-DD}}_{{SLUG}}_CueSheet_v{{N}}.md
{{YYYY-MM-DD}}_{{SLUG}}_CueSheet_v{{N}}.pdf
readme.txt
```

Same date, same slug, same version number on the versioned four. A Reader Script edit that
moves or rewords an anchored line invalidates the matching Cue Sheet, so all of them
increment together. Each document ships as a working format plus a `.pdf` twin for human
review reading: the Reader Script's `.txt` is the **only** file the prompter ever loads
(its PDF is for review, never the prompter), and the Cue Sheet's `.md` is the source of
truth for the editor. PDFs are rendered from the final working files — identical content,
never edited independently.

**readme.txt** documents where the script came from. It contains:

- Generation date, mode (fresh / brain-dump), format and target length.
- The source video URL (Loom/YouTube) or the topic/brief for fresh mode.
- Fact-check status: which claims were verified, against what, on what date.
- The **full transcript of the source video** (from the Gemini analysis pass or a
  dedicated transcription call against the same uploaded file). If the source has no
  speech, say so and include the timestamped screen-event log instead.
- Any anonymization notes (demo account names, email addresses to blur when rebuilding
  frames).

### 7.3 Formats

**Reader Script — the constraint is the prompter app.**

- Default: `.txt`, UTF-8, plain. Most prompter apps ingest plain text cleanly and preserve
  hard line breaks.
- Also render a `.pdf` twin of the `.txt` for review reading (same chain as the Cue Sheet
  PDF below; preserve the line breaks and blank lines exactly — they are the pacing). The
  PDF never goes near the prompter.
- If the app requires it: `.docx` (single body style, no headings, no lists) or `.rtf`.
- If `.md` is used, the body must still contain **no markdown syntax** — no `#`, `*`, `_`,
  `>`, `-` at line starts.
- Straight quotes and apostrophes, not curly.
- No tabs. No trailing whitespace. No soft-wrapped paragraphs.
- Line length: short enough to display on one prompter line at the operator's font size.

**Cue Sheet — the constraint is human readability at a desk.**

- Source of truth: `.md`. Always also render the same `.md` to `.pdf` (§7.2).
- PDF rendering chain (first available wins): `pandoc` → Chromium-family browser headless
  (`"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"` or Google Chrome, with
  `--headless --print-to-pdf={{OUT}} --no-pdf-header-footer {{HTML}}`, converting the md to
  styled HTML first — the `markdown` pip module works for that) → `cupsfilter` as a last
  resort. If every option fails, deliver the `.md` and flag the missing PDF — don't block
  the export on it.
- Alternatives if the builder's tooling requires: `.csv` (use §5.4 columns) or a table in
  the team's doc tool.

### 7.4 Destination and delivery — the Drive project folder

Scripts are filed into MAN Digital's Video project tree on the shared Google Drive. With
Google Drive for Desktop it is mounted under your CloudStorage folder:

```
~/Library/CloudStorage/GoogleDrive-<you>@man.digital/<shared-drive-shortcut>/Video/
```

(Resolve the exact shortcut path on your machine once and keep using it; the folder IDs
live in the team's internal docs, not here.)

1. Build all four files (§7.2) in a working directory and verify against §7.6.
2. **Find or create the project folder** under `01_Active_Projects/`:
   - If a project folder for this video/topic already exists, use it — bump the version
     number on the files instead of creating a twin folder.
   - **Version bumps archive the old files.** When writing v{{N+1}} of any script files,
     create an `Old_Versions/` folder inside that project's `Storyboards_&_Scripts/` (if it
     doesn't exist yet) and move every superseded versioned file into it. The top level of
     `Storyboards_&_Scripts/` holds only the current version plus `readme.txt`. Update
     `readme.txt`: point its file list at the new version and append a short VERSION
     HISTORY entry saying what changed and that the old files moved to `Old_Versions/`.
   - Otherwise copy the **pristine template** at
     `01_Active_Projects/[ New Project Template ]/YYYY-MM-DD_[ClientName]_[ProjectSubject]/`
     (the inner folder) into `01_Active_Projects/` — never duplicate an old project (the
     SOP's Clean Origin Rule). Delete stray `.DS_Store` files from the copy. Leave the
     `[FolderName]_Master.*` project files untouched — existing projects keep them as-is.
3. **Rename** the copy `YYYY-MM-DD_ManDigital_{{Topic}}` — date = script creation date,
   topic in CamelCase. When the source material is HubSpot (a HubSpot tutorial/showcase
   Loom, a HubSpot feature), prefix the topic with `Hubspot`: e.g.
   `2026-07-30_ManDigital_HubspotBillingPortal`, matching siblings like
   `2026-07-29_ManDigital_HubspotPriceBooks`. For client case studies the client name
   replaces `ManDigital` (see `02_Archived_Projects_[COMPLETED_ONLY]/` for precedent —
   check both active and archived folders to stay consistent with existing naming).
4. Copy all four files into that project's `01_Pre_Production/Storyboards_&_Scripts/`.
5. Present the files to the requester in one action, **Reader Script first**, and say
   which project folder they were filed into.
6. Keep the response text after delivery to a short summary. The files carry the content.

**If Google Drive is offline or the mount is missing on this machine:** still run the full
export — all five files, all checks. Do not try to recreate the project-folder template
from scratch (the pristine template lives on Drive, so without it the tree would be a
guess). Deliver the files from the working directory with an explicit notification: Drive
is offline, the project folder still needs to be created from the template, and these
files need to be imported into its `01_Pre_Production/Storyboards_&_Scripts/`. Only do
this when Drive is actually unavailable — never as a shortcut.

### 7.5 Downstream consumption

- **Reader Script → prompter.** The operator loads the file and scrolls from the first
  spoken line.
- **Cue Sheet → motion graphics.** The builder works down the numbered list, finds each
  anchor line in the Reader Script, and times the graphic to that line. Anchors are the only
  sync mechanism, so they must be verbatim.

### 7.6 Pre-export checklist

Run all of these. Any failure blocks export.

- [ ] Two files, not one.
- [ ] No chunk in the Reader Script exceeds two lines; every chunk is followed by a blank
      line.
- [ ] Every enumeration is one item per line with a spoken ordinal ("One: …"), never buried
      in a prose sentence.
- [ ] Every interrogative line ends with a question mark.
- [ ] Fact-check Pass 2 (SKILL.md Step 4) run on the finished text: every date, number,
      price, feature name, and UI location re-verified online after drafting.
- [ ] Reader Script contains zero visual references — searched for `[`, `VISUAL`, `graphic`,
      `fig`, digits used as visual labels.
- [ ] Reader Script contains zero markdown syntax in the body.
- [ ] Every anchor quote in the Cue Sheet appears **verbatim** in the Reader Script.
- [ ] Cue Sheet visuals are numbered in script order, with no gaps.
- [ ] Every dense or number-heavy point has a visual anchor, or an explicit note saying why
      it does not.
- [ ] Cue Sheet carries no spoken lines beyond anchor quotes.
- [ ] Timecodes accumulate correctly and the final one is within tolerance of the target
      length.
- [ ] Word count ≈ blueprint total, and total runtime at the stated wpm ≈ target.
- [ ] Filenames match the §7.2 pattern; ReaderScript/CueSheet files share date, slug, and
      version.
- [ ] Both `.pdf` twins (Reader Script + Cue Sheet) rendered from the final working files
      (or their absence flagged per §7.3).
- [ ] `readme.txt` present with source link, transcript (or screen-event log for silent
      sources), and fact-check status.
- [ ] Files filed into the Drive project folder's `01_Pre_Production/Storyboards_&_Scripts/`
      per §7.4 — existing folder reused, or a fresh template copy named
      `YYYY-MM-DD_ManDigital_{{Topic}}` (Hubspot-prefixed topic for HubSpot material).
- [ ] On a version bump: superseded files moved into `Old_Versions/`, readme file list
      updated to the new version, VERSION HISTORY entry appended.
- [ ] Encoding is UTF-8; quotes are straight; no tabs; no trailing whitespace.
- [ ] Blocklist scan clean (banned-words.md).
- [ ] Beat separator confirmed to render or strip correctly in the target prompter app.
