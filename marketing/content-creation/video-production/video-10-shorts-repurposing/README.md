# video-10-shorts-repurposing — Skill

Mines a finished long-form video's transcript for short-form vertical candidates and
returns a scored, ready-to-judge slate per platform — then, once Diogo picks, emits
the exact CUT ORDERs that build each short.

This is a **standalone post-approval skill, not a pipeline stage**. It never runs
automatically from the video pipeline — Diogo asks for it, at or after approval of
the long-form cut. It is strictly read-only on the long-form: every short is a new
deliverable built from a duplicated sequence.

## What does this skill do?

- Runs an ASR-correction pass on the transcript, then mines the video **twice**,
  through two deliberately different lenses:
  - **YouTube Shorts** (sound-on autoplay): candidates must open with a spoken hook
    in the first 1–2 seconds, carry one concrete imageable idea, stand alone without
    the long-form context, and ideally loop. Target 15–60 s.
  - **LinkedIn vertical** (sound-off feed): candidates must carry the point on mute
    via first frame + first caption line, lead with a sharp POV the ICP (Founders,
    CROs, RevOps leaders) reacts to, and end on a comment-inviting thought. 30–90 s.
- Scores every qualifying moment fully — no candidate cap, no padding to a quota,
  and genuine rejects are listed as one-line Near-misses so the judgment stays
  inspectable.
- Gives each candidate a Hook/Core/Close blueprint, word-exact spans with frame
  timecodes, CTRL+F locate strings (raw source words, ASR errors included, so the
  editor can find them in Premiere), runtime checksums, and a CTA back to the
  long-form.
- Ships the **attention stack** per YouTube candidate: a suggested title (feed text —
  the promise; seed for video-09's upload-time title pass), **first-frame cover copy**
  (an in-frame graphic between the speaker's face and the subtitles — a vertical
  uploads no thumbnail file, so the first frames do that job, and the copy has to
  exist at edit time), and the spoken hook (audio — the claim that pays both off).
  All derived from the candidate's own script, three surfaces in one niche, each
  leveraging its own medium, never duplicating one another.
- On Diogo's selection ("build Y1 and L2"), emits one CUT ORDER per short in the
  video-02 format for execution by video-03-cuts on a duplicated 9:16 sequence.

## When should I use it?

- After a long-form cut is locked (ideally approved) and its transcript exists, when
  asked to "make shorts from this", "repurpose the long-form", "find the reels",
  or "cut a vertical from this".
- On a mid-edit transcript only with the explicit warning that any recut voids every
  timecode issued.
- Not for building the vertical itself — reframing and graphics route to video-06,
  captions to video-08, upload subtitles to video-09 (Shorts mode), and Shorts
  metadata / LinkedIn post copy are out of scope entirely.

## What inputs does it need?

- The **conformed word-level transcript JSON** of the final cut (preferred — gives
  word-exact boundaries placed in silence gaps). A back-catalog SRT/CSV is accepted
  with degraded precision: estimated boundaries, ± tolerances, cut-by-locate-string.
- The project's **long-form CTA line** — supplied per project, never invented or
  reused; the skill asks if it's missing.
- Both platform lenses are mined every run unless Diogo explicitly skips one.

## What does it produce?

Into `04_Project_Assets/Shorts_Repurposing_Scripts/`:

- `<transcript basename>.shorts-youtube.md` — the Shorts-lens slate
- `<transcript basename>.shorts-linkedin.md` — the LinkedIn-lens slate
- A rendered `.pdf` twin of each slate for one-click visual preview

Each slate is self-contained: header (source transcript, cut state, fps, CTA line,
timecode validity), ranked candidates with scores/blueprints/spans/build notes,
Near-misses, and a pickup list if any. Marginal candidates carry a "Worth building?"
for/against block. After selection: one CUT ORDER file per chosen short.

In Premiere, each short that gets built is filed into `00_Timelines/01_Active_Cuts`
and colour-labelled by platform — **Rose** for the YouTube Shorts series, **Blue** for
the LinkedIn series — in the same pass that cuts it, so a session that produces eight
shorts still reads at a glance in the project panel.

## Prerequisites

- Python 3 for the two bundled scripts:
  - `scripts/span_times.py` — verifies every span and boundary gap against the JSON
  - `scripts/render_pdf.py` — renders the PDF twins (pandoc when installed, else
    markdown → styled HTML → headless Chromium-family print; a failed render is
    flagged, never blocks the `.md` delivery)
- A locked long-form cut with its transcript export on disk.
- The Claude Project backup (Document 3, "Transcript Optimization") lives in Drive
  under `Video/04_Internal_SOPs/` as the craft reference for edge cases — useful,
  not required.
