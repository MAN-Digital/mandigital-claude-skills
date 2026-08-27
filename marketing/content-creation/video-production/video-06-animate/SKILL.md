---
name: video-06-animate
description: >
  Creates animation for React, CSS, and HubSpot modules and deterministically renders HTML,
  Pencil exports, or components to MP4, MOV, ProRes, or PNG sequences at 25 or 50 fps. Use for
  UI motion, transitions, hover effects, route transitions, reveals, easing, frame-by-frame
  capture, Playwright screenshots, ffmpeg encoding, or timeline assets. Also handles fitting
  blog-shaped designs into 16:9, full-frame and split-screen variants, vertical Short-first
  layouts, alpha overlays, and rebasing master transcript timecodes to animation-local cues.
---

# Animate

Two tracks. Decide which one you're in before writing anything, because the rules conflict.

| | **Web track** | **Render track** |
|---|---|---|
| Output | live UI a user interacts with | video file for a timeline |
| Read | this file + `references/web-motion.md` | this file + `references/canvas-fit.md` + `references/render-contract.md` + `references/video-export.md` |
| Frame rate | variable, target 60 | fixed 25 or 50 |
| Canvas | whatever the page is | **three fixed canvases — full-frame 1920×1080 CSS @2x (default), ⅔ split 1280×1080, ⅓ split 640×1080 — pick via the format pass, then fit the design to it** |
| Property budget | `transform` + `opacity` only | anything |
| Duration unit | milliseconds | frames |

If the user is building UI, you're in the web track. If they said video, MP4, render, export, or
named a frame rate, you're in the render track. If they're building a UI *that will later be
rendered*, work in the web track but follow the render contract from the start — retrofitting it
is more work than writing it that way.

---

## Where output goes — settle this before writing anything

**Everything this skill produces lives next to the design it came from.** Animation HTML, PNG
frames, `segments.csv`, and the encoded video belong inside the user's project, beside the source
file — never in the skill directory, never in `~/.claude`, never in the scratchpad, never wherever
the shell happens to be.

**Step 1 — find the design root.** It's the directory holding the file you were given: the `.pen`
file, the exported HTML, the component, the folder the user pointed at. If the user named a design
without a path, ask for it before rendering — don't guess and don't fall back to cwd.

**Step 2 — create one output folder there,** named after the design:

```
/Users/you/Projects/acme-launch/
  hero-chart.pen              ← the design you were given
  hero-chart-animation/       ← everything you make goes here
    hero-chart.html           the animation source
    frames/                   PNG sequence + segments.csv/.json/.md
    hero-chart.mov            the encoded output
```

For layered renders, `frames/` becomes `layers/card/`, `layers/title/`, and so on, still inside
that same folder. Re-runs of the same iteration go back into the same folder — don't scatter.
But once a version has been delivered for review, **revisions go into a new sibling folder**
(`hero-chart-animation-v2/`): the reviewed version stays on disk untouched — the user deletes
retired versions, never you — and the project's placement manifest points at the current
candidate. Keep that manifest (asset · current version · place-at · length) true after every
delivery and every user deletion: it lists exactly what's on disk, nothing else.

**Version labels start at v1 (Diogo, 2026-08-01).** The *first* iteration of every design and
animation is explicitly labeled v1 — in the folder name (`B5A-animation-v1/`), the output
filename (`…_16x9_v1.mov`), and the design frame name (`… (built v1)`, `… (vertical v1)`) —
so the reviewed baseline is unambiguous before a v2 ever exists. Feedback and disapprovals are
**always applied as a new version (v2, v3, …), never as edits to the reviewed original** — for
designs this means duplicating the frame inside the .pen and revising the copy; the v1 frame
stays untouched.

**One subfolder per segment (Diogo, 2026-08-01).** Every design/animation segment gets its own
subfolder inside the project's Working_Graphics — never share a folder between assets. When one
spoken list spans several reading-away windows ("one animation which is technically several"),
deliver it as letter-suffixed sibling assets (`B4A…B4D`), each with its own folder and design
document, sharing one visual family (same eyebrow, watermark, band language).

**Step 3 — pass absolute paths to every command.** `--out` defaults to `frames`, which is relative
to the working directory; that default is what scatters renders. Resolve the design root into a
variable and use it:

```bash
DESIGN_DIR="/Users/you/Projects/acme-launch"
OUT="$DESIGN_DIR/hero-chart-animation"
mkdir -p "$OUT"
python ~/.claude/skills/video-06-animate/scripts/render_frames.py --file "$OUT/hero-chart.html" --fps 25 --out "$OUT/frames"
python ~/.claude/skills/video-06-animate/scripts/encode.py --frames "$OUT/frames" --fps 25 --profile edit --out "$OUT/hero-chart.mov"
```

The skill directory is read-only working material — scripts, references, `assets/harness.js`.
Nothing you generate is written into it. The scratchpad is fine only for a throwaway probe you
will never hand back; anything the user might want again goes in the design folder.

Every command example further down this file and in the references is written with short relative
paths for readability. Substitute the absolute design-folder paths above when you actually run
them.

---

## Golden rules

Each rule has a counterexample. The counterexample is the part that makes it stick.

1. **Exits run faster than entrances** — about 75% of the enter duration. Something arriving
   deserves attention; something leaving is already decided.
   ✗ `enter 200ms / exit 200ms` — the dismissal feels sluggish.
   ✓ `enter 200ms / exit 150ms`

2. **On the web, animate only `transform` and `opacity`.** They're composited on the GPU and skip
   layout and paint entirely.
   ✗ `transition: height 200ms` / `top`, `left`, `width`, `margin` — these force layout on every
   frame and will drop frames on a mid-range laptop.
   ✓ `transition: transform 200ms` with `translateY()` / `scaleY()`.
   In the **render track this rule is void** — you're not running in real time, so animate
   `filter`, `box-shadow`, `clip-path`, whatever looks right.

3. **200–300ms is the sweet spot.** Under 100ms reads as a jump cut; over 500ms feels like the
   interface is thinking.
   ✗ `transition: all 1s ease` on a dropdown.
   ✓ `transition: transform 240ms var(--ease-out-quint)`

4. **Never animate `all`.** It animates properties you didn't intend, including expensive ones
   you can't see.
   ✗ `transition: all 300ms`
   ✓ `transition: transform 300ms, opacity 300ms`

5. **Always respect reduced motion on the web.** Ship this with every animation — inline, now,
   not from a reference file:

   ```css
   @media (prefers-reduced-motion: reduce) {
     *, *::before, *::after {
       animation-duration: 0.01ms !important;
       animation-iteration-count: 1 !important;
       transition-duration: 0.01ms !important;
       scroll-behavior: auto !important;
     }
   }
   ```
   Not applicable in the render track — there's no user preference inside a video file.

6. **Springs for interruptible motion, durations for choreography.** A drag or a toggle a user can
   reverse mid-flight wants a spring. A timed sequence wants a duration.
   In the **render track, avoid springs** — you need a known end time, and spring settling is
   awkward to pin to a frame count.

7. **Never crop content to make it fit the frame.** Render track only. The frame is fixed at
   1920×1080 CSS px; the design is what bends. If something leaves the frame, the layout is wrong.
   ✗ Fit-to-height, centre it, let the title run past the right edge — "the voiceover covers it".
   ✓ Reflow so the title has room. If reflow genuinely can't hold it, stop and ask — a crop is
   never the answer you pick on your own. `references/canvas-fit.md`.

---

## Easing

```css
:root {
  --ease-out-quint:    cubic-bezier(.23, 1, .32, 1);
  --ease-in-out-cubic: cubic-bezier(.645, .045, .355, 1);
  --ease-out-cubic:    cubic-bezier(.33, 1, .68, 1);
}
```

| Motion | Easing | Web duration | Frames @25 | Frames @50 |
|---|---|---|---|---|
| Element entering | `ease-out` | 200–300ms | 5–8 | 10–15 |
| Element moving on screen | `ease-in-out` | 200–300ms | 5–8 | 10–15 |
| Element exiting | `ease-in` | 150–200ms | 4–5 | 8–10 |
| Hover / press | `ease` | 100–150ms | (web only) | (web only) |
| Opacity only | `linear` | varies | varies | varies |
| **Value arriving at a number** | **`ease-out-expo`** | 600–1000ms | **24–30** | 48–60 |

That last row is its own rule. Counters, percentages, bar fills, gauges — anything landing on a
figure — covers most of its distance almost immediately and then decelerates hard into the final
units, like a wave running up wet sand. `ease-out-cubic` ticks up too evenly and reads as an
odometer. And a bar and its label must be driven by **one** progress value, or the number stops
describing the bar. See `references/timing-and-easing.md`.

**Ease-out for entrances is the single highest-leverage default.** It decelerates into place, which
reads as the element arriving rather than being thrown.

At 25 fps one frame is 40 ms. Round every render-track duration to whole frames, and treat
**3 frames (120ms) as the floor** — anything shorter reads as a pop, not motion. The web's 100ms
press is invisible at 25 fps. Full conversion table in `references/timing-and-easing.md`.

---

## House motion language — render track

Standing feedback from review rounds. Apply without being asked; violating these is what gets a
version rejected:

- **Soft focus-in reveals**, never discrete per-word pops.
- A multi-line headline is **one gesture** — one cue with heavy overlap, not one event per line.
- **Ambient drift lives on decorative layers only** (depth ellipses, dot-grid shimmer — the "soul"
  layer); structural elements hold still.
- No **content** the transcript or the source design doesn't support — labels, claims, numbers,
  captions. Check the spoken words for the window before inventing a text element; an unsupported
  label gets the version rejected.
- **The soul layer is expected, not optional** — this rule is about content, never about life.
  Every final clip carries ambient motion on its decorative layers (a drifting depth ellipse, a
  slow dot-grid shimmer), and craft additions that express the data harder — a ball riding the tip
  of a line as it draws — are welcome and have *upgraded* approved designs. What gets cut is
  decoration doing no work (a divider duplicating an edge the layout already draws), never depth
  and life. An animation with correct cues and no soul reads as weaker work, not safer work.
- A container and its text arrive **together** — an element that shows up empty and fills later
  needs a spoken-word reason (the speaker hasn't listed the items yet), not a stylistic one.
  Long empty-frame stretches before the first element are dead air: compress them.
- Un-anchored (free) cues get placed to close dead air, never left to drift.
- When review feedback is about *timing* ("show it earlier", "faster") — **retime the approved
  design, don't redesign it.** A new treatment in response to a scheduling note reads as a
  regression and wastes a round.

---

## Choosing an approach

| Scenario | Approach |
|---|---|
| Hover, focus, press, simple state change | CSS transitions |
| HubSpot module, email, no build step | CSS only — see `references/hubspot-modules.md` |
| Enter/exit of mounting components | Motion + `AnimatePresence` |
| Layout / size / position change | Motion `layout` prop |
| Shared element across views | Motion `layoutId` |
| Orchestrated multi-element sequence | Motion variants + `staggerChildren` |
| Drag, scroll-linked | Motion gestures / `useScroll` |
| Anything being exported to video | Render contract — `references/render-contract.md` |

The library is **Motion** (formerly Framer Motion). Install `motion`, import from `motion/react`.
`framer-motion` still resolves but is the old name — don't write it into new code.

```bash
pnpm add motion
```

```tsx
import { motion, AnimatePresence } from "motion/react";
```

In Next.js App Router, any file using `motion.*` needs `"use client"` at the top. Motion components
carry event handlers and state, so they cannot be server components — this is the most common
Next.js motion bug.

---

## Formats — full frame, ⅔, ⅓, overlay

One design, up to three deliverables. The format set is decided **before the fit pass**, because
each format is its own canvas and its own fit.

| Format | Author (CSS @2x) | Output | Occupies | Premiere pairing |
|---|---|---|---|---|
| **Full frame** (default) | 1920×1080 | 3840×2160 | whole frame | `MD3 Graphic Slide <side> Full In/Out` — footage needs no dodge |
| **⅔ split** | 1280×1080 | 2560×2160 | exact ⅔; speaker in the other ⅓ | graphic `MD3 Graphic <side> 2/3 In/Out` + footage `MD2 Slide <opposite> 2/3 In/Hold/Back` |
| **⅓ split** | 640×1080 | 1280×2160 | exact ⅓; speaker in the other ⅔ | graphic `MD3 Graphic <side> 1/3 In/Out` + footage `MD2 Slide <opposite> 1/3 In/Hold/Back` |
| **Overlay** | 1920×1080, alpha | 3840×2160 ProRes 4444 | floats over footage | drop on a higher track |
| **Vertical** (on demand) | 640×1080 | 1280×2160 | Short-first designs; otherwise only on Diogo's explicit repurpose ask | used in the vertical edit, not the horizontal cut |

Split widths are exact thirds of 3840 **on purpose** — the MD preset kit's offsets assume them, so
the editor gets the whole choreography by dropping presets. These splits are *not* the
9:16 Shorts-convertible panel (2160×3840 placed at 56.25%) — that's a separate spec in
`video-07-graphics-placement/references/geometry.md`; don't mix their numbers.
**This table is the single canonical source for these canvas numbers and preset
pairings** — video-07's format call cites it by name instead of restating them
(consolidated 2026-08-06); change a number or preset string HERE and nowhere else.

**Every asset ships a full-frame master. A split variant is built in addition, from the approved
master, only where the split earns it:**

- **Split works** — single-column content: a headline over a device shell, a stacked list, a
  chapter menu; naturally vertical material; a long talking stretch where the speaker should stay
  on screen. **⅔** when the graphic should dominate, **⅓** when the speaker should and the content
  is a compact column.
- **Full frame only** — anything that spends the width: wide tables, maps, fans, mirrored/crossing
  layouts, a strike travelling a long line; and any clip that hands off into another full-frame
  graphic (the join must happen full-frame).
- **Overlay** — a quote or short stat that punctuates rather than explains; alpha over the speaker
  works over any layout and needs no variant. A quote can take full frame instead when it deserves
  total focus.

Split-variant rules: reflow to the narrow canvas (usually side-by-side → stacked) but **keep the
master's cue table verbatim** — same transcript anchors, same local frames — so the editor swaps
master ↔ variant at the same timecode with zero timing work. A reflow never rewords: data, copy
and reading order are fixed. Canvas numbers and safe margins in `references/canvas-fit.md`.

**Vertical is on demand, not a standing deliverable (Diogo, 2026-08-06 — supersedes the
2026-08-01 every-asset rule).** Build a 1280×2160 vertical only when vertical is the master
format for that design — a Short-first asset, with every cue derived from the Short's own
word-level transcript (a 16:9 master's cue table never transfers). Full-frame, ⅔ and ⅓
masters ship with no vertical; repurposing an existing horizontal design to vertical happens
only when Diogo asks for it explicitly. When one is built the two-step rule holds: the design
gets its own vertical variant first, then the fit pass and animation run on it — a vertical is
never a squeezed horizontal. 1280×2160 is deliberately not 9:16 (the user's chosen export): in
the Shorts edit it's either side-cropped to true 9:16 or downscaled onto a background — so
design it to survive both. For a Short whose reading-away windows are too short to hold an
entrance (≲30f), deliver one continuous narration-correct render the editor cuts in and out
of — every window IN must land on a settled, readable state — never per-window insert clips.
Margins and crop numbers in `references/canvas-fit.md`.

**Backgrounds are opaque everywhere except quote overlays (Diogo, 2026-08-01).** Full-frame
masters, ⅔ and ⅓ splits, and vertical exports always carry a solid opaque background —
including full-frame graphics that take the whole frame simply because the content wouldn't fit
a split, not to hide anything. Transparency is reserved for one job: overlay accents that bring
an important quote to life — floating the quote, and any elements designed to go with it, over
the footage to pull focus. If it isn't that, it isn't transparent.

---

## Two clocks — master time vs animation time

Cue specs (from the transcript / the placement pass) arrive in **master** timecode — the sequence
clock. The animation is authored in **local** frames starting at 0. They are never the same clock;
the bridge is the clip's *place-at*:

```
local = master − place-at        (in frames, at sequence fps, converted once)
```

- **Rebase every anchor up front** into a per-asset table (master · local · word) and keep it with
  the project as the `CUE REBASE` doc. The editor thinks in master, `Timeline.cues` thinks in
  local; nobody converts in their head mid-review.
- **Verify anchors against the word-level transcript JSON, not against the cue sheet that proposed
  them.** For each cue, print what is actually being said at its master frame. Anchors drift by a
  word (15–30 frames) far more often than they're wrong outright, and only this check catches it —
  one pass caught six drifted anchors that the cue sheet swore were right.
- **A re-cut or a moved place-at invalidates local anchors.** Word-synced beats are baked into
  rendered frames; when the cut moves the words, the affected clip is re-derived and
  **re-rendered** — never slid, never hold-stretched. Final clips carry ambient motion, so there
  is no clean frame to freeze. Budget the pass instead (~12 min for fifteen 4K clips).
- **Chained multi-state assets** (one system delivered as N butt-joined clips) carry a per-state
  offset from the group's IN, so phase-continuous elements animate on *asset-global* time and every
  join matches to the frame — full contract in `references/timeline-and-layers.md`.

---

## Coverage windows — reading-away inserts

When the user supplies a timecode window because the speaker is reading off-camera ("Romeo is
looking away from 00:20:49:24 to 00:21:08:05"), that window is **minimum coverage, not an exact
placement**: the graphic may start earlier and/or end later when the transcript supports it, but
it may **never start later or end earlier** than the given window (Diogo, 2026-08-01). In
practice: pull the IN back to the start of the sentence that introduces the on-screen content
(a given IN often lands mid-word), and extend the OUT the few frames needed for the last spoken
word of the covered content to finish. Record both the given window and the chosen window in the
asset's design notes, with the reason for each deviation.

**Reading-away inserts must fully hide the video.** When the user gives a timecode window
because the speaker is reading off-camera, the graphic exists to cover that footage completely:
a full-frame design with a solid, fully opaque background over the whole frame, from the first
frame of the window to the last — no area and no moment where the video shows through. Elements
inside the design still fade and reveal on their cues; the solid background is what does the
covering. (Diogo, 2026-08-01: "it needs to have a full design… I cannot stress this enough.")

---

## Render track workflow

Defaults: **1920×1080 CSS @2x → 3840×2160 output, 25 fps, ProRes 422 HQ.** Do these in order — a
4K minute is 1500 frames.

**Author in the 1920×1080 CSS space.** `--width`/`--height` are the design's own coordinate system;
`--scale` multiplies it into real pixels. The two are multiplied, not chosen between: 1920×1080 @2x
and 3840×2160 @1x both output 3840×2160 and are equally sharp, but a 4K canvas *with* the default
2× scale is 7680×4320 — four times the disk and render time. The script now refuses that unless you
pass `--allow-oversize`. Pencil exports arrive around 1536×1024, so the 1920 space is also the
smaller rescale when you reflow.

0. **Create the output folder beside the design** and write the animation HTML into it, before you
   start iterating. See *Where output goes* above. Every path below is relative to that folder.
1. **Fit the design to the frame — before you write a single line of motion.** The design almost
   never arrives at 1920×1080: Pencil exports are 1536×1024, blog graphics are portrait or square,
   with 12–16px type meant for a scrolling column. Measure it, reflow it, and check it while it's
   still static.
   ```bash
   python scripts/render_frames.py --file design.html --check-fit --out fit/
   ```
   It reports what crosses the frame edge, what's under the 27px legibility floor, and how much of
   the frame the content is actually using — no render contract needed, so it runs on the raw
   design. Then **show the user `fit/fit-check.png` and get a yes before animating.**
   Data, wording, values and reading order are fixed; position, scale, wrapping, spacing and
   layout structure are yours to change. Escalate in order — scale, then reposition, then reflow —
   and if the frame still can't hold it, ask rather than crop. Full method, arithmetic and safe-box
   numbers in `references/canvas-fit.md`.
2. **Calibrate against golden samples, then get the animation right in the browser.** Before
   writing motion, open the newest *approved* animation HTMLs from this project (earlier approved
   assets in the project's Working_Graphics folders; `examples/` as fallback) and match their
   level — the soul layer, the reveal language, the easing feel. The most recently approved clip
   is the bar; an animation authored cold from the rules alone comes out flatter. If no approved
   sample is reachable (project drive unmounted), say so before starting. Then iterate live;
   rendering is slow feedback.
3. **Allocate slots.** Give every element its own non-overlapping window followed by a static
   hold, so the edit can retime each one independently. Declare timestamps if you know them —
   the cue list is then the single source of truth and the render can't drift from the spec.
   ```js
   const tl = Timeline.cues({
     fps: 25, compact: true,
     cues: [
       { name: "rect1", at: "0:00", anim: "1s"  },
       { name: "rect2", at: "0:20", anim: "1s"  },
       { name: "rect3", at: "0:40", anim: "15s" },
     ],
   });
   window.__renderAt = (t) => { rect1.style.opacity = tl.p("rect1", t); /* ... */ };
   tl.table();     // print the plan; check it against the cue sheet
   tl.export();
   ```
   **Pacing and speed are different.** *When* an element appears is fully recoverable by time
   remapping — render holds short. *How long it takes to animate* is not: stretching 20 frames
   across 15 seconds gives staccato or interpolation mush. If a bar should take 15 seconds to
   fill, render 375 frames of it. Pay render time for motion, never for stillness.
   Overlapping cues throw rather than producing an un-remappable render.
   `references/timeline-and-layers.md`.
4. **Add the render contract** — WAAPI-scrubbable animations or `window.__renderAt(t)`.
   `references/render-contract.md`. Copy in `assets/harness.js`.
5. **Confirm fps with the user.** 25 to match the timeline; 50 only if they want slow-motion
   headroom. Canvas follows the format pass (see *Formats* above): full-frame 1920×1080 @2x unless
   you're building a ⅓ or ⅔ split variant. Only override the coordinate system for a design
   already written in 4K coordinates (`--width 3840 --height 2160 --scale 1`), and never add
   `--scale 2` on top of that.
6. **Check before rendering** — all three are fast and each catches a failure that otherwise
   surfaces after twenty minutes of rendering:
   ```bash
   python scripts/render_frames.py --file anim.html --check-fit     # nothing leaves the frame
   python scripts/render_frames.py --file anim.html --verify        # determinism
   python scripts/render_frames.py --file anim.html --check-holds   # holds are static
   ```
   Re-run `--check-fit` here even though you ran it in step 1 — motion moves things, and it now
   measures the settled end state.
   **`--check-fit` sees frame edges and the type floor only.** It cannot see element-on-element
   overlap, text escaping its container, or a connector floating away from the box it points at —
   the defects reviews actually reject. Before delivering: still key frames from the raw HTML,
   contact-sheet the encoded render, and zoom each element separately. When the same clip fails
   review twice for layout, stop patching instances and fix the **class** of defect (auto widths
   that never align, stubs attached to buses that end elsewhere) — fixed dimensions and mirrored
   geometry fix classes.
7. **Render**, then **encode**:
   ```bash
   python scripts/render_frames.py --file anim.html --fps 25 --out frames/
   python scripts/encode.py --frames frames/ --fps 25 --profile edit --out animation.mov
   ```

Default output is **ProRes 422 HQ**, not H.264 — this goes into an editor, and 8-bit 4:2:0 is a poor
intermediate for flat-colour graphics with hard edges. `--profile web` for previews,
`--profile edit-alpha` for overlays. Alpha, shutter-angle blur, and gotchas in
`references/video-export.md`.

The render writes `segments.csv` alongside the frames with two timecodes per slot: where it sits in
the file, and where it belongs in the finished video. Remapping is then mechanical — keyframe at
*renders at*, move to *place at* — rather than scrubbing to find boundaries.

Keep the PNG sequence until the edit is locked. It's the lossless master and every NLE imports it
directly.

---

## References

- `references/canvas-fit.md` — the fit pass: measuring a design against the frame, the reflow ladder, safe box and type floors, plus the ⅓ / ⅔ split-canvas numbers
- `references/timing-and-easing.md` — frame conversion tables, easing curves, when each applies
- `references/web-motion.md` — CSS patterns and Motion/React recipes, corrected imports
- `references/render-contract.md` — the two deterministic modes, and how to make an existing page conform
- `references/timeline-and-layers.md` — slot allocation, time remapping, layered alpha alternative, and the chained multi-state continuity contract
- `references/video-export.md` — Playwright capture, ffmpeg profiles, alpha, motion blur, gotchas
- `references/hubspot-modules.md` — animation inside HubSpot custom modules, no build step
- `assets/harness.js` — drop-in render contract implementation
- `scripts/render_frames.py`, `scripts/encode.py` — the pipeline
