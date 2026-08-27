# Fitting a design to the frame

The pass that happens **before any animation exists**. A design that came out of Pencil is 1536×1024;
one that came from a blog post was authored for a scrolling column — portrait or square, 800–1600px
wide, 12–16px type. The frame is **1920×1080 CSS px** and fixed. Those two things do not agree, and
the disagreement has to be resolved by changing the layout, not by dropping content off the edge.

**Every number on this page is CSS px in the 1920×1080 authoring canvas.** The render is
`--scale 2`, so the file that lands on the timeline is 3840×2160 — a 27px caption here is 54 real
pixels there. Author against the CSS numbers and let the scale factor do the rest; don't do the
doubling in your head and don't write 4K coordinates into the design.

Do this while the design is still static. Motion on a badly fitted frame is wasted work, and
retiming won't rescue a cut title.

---

## The hard rule

**Nothing is cropped. Ever.**

Not the title, not a legend, not the last row of a table. If content leaves the frame, the layout
is wrong — the frame isn't too small.

✗ Title runs 260px past the right edge, so it gets clipped and the voiceover covers the meaning.
✓ Title reflows to two lines, or the block below moves into the horizontal slack to give it room.

**Voiceover is not a licence to cut.** "They'll hear it anyway" makes a graphic that fails silently
for anyone watching muted, on a phone, or on a thumbnail. If the frame genuinely can't hold the
content, that's a Tier 3 conversation with the user — see below — not a crop.

---

## What may change, and what may not

| May change | May not change |
|---|---|
| Position of any block | The words, in any element |
| Scale of any block, and type sizes | Numbers, units, precision, rounding |
| Stack → columns, columns → rows, grid column count | Which elements exist (the user already cleaned) |
| Line breaks and text wrapping | Reading order — top-left → bottom-right |
| Margins, padding, gaps | Brand colours, typeface, corner radii, chart type |
| Stroke and border weights (upward, to clear the floor) | Data-to-mark mapping — bar lengths stay proportional |

Reading order is on the right-hand column for a reason: it's the order the elements animate in, and
that order is what the voiceover follows. Reflowing a vertical stack into two columns is fine.
Swapping which block comes first is not.

The user removes blog-only elements (CTAs, share rows, author bylines) before handing the design
over. **Don't remove anything further on your own initiative.** If a block has to go for the frame
to work, ask.

---

## 1. Measure first

One command, before you touch anything. It needs no render contract, so it runs on the raw design.

```bash
python scripts/render_frames.py --file design.html --check-fit --out fit/
```

It reports the native document size, everything that crosses the frame edge, every text element
under the legibility floor, every hairline stroke, and how much of the frame the content actually
occupies. It also writes `fit/fit-check.png` — the still you show the user.

Record three numbers before deciding anything:

- **Source canvas** `w × h` and its aspect
- **Fit scale** `S = min(1920/w, 1080/h)` — the largest uniform scale that keeps everything inside
- **Smallest type in the source**, in source px

---

## 2. Two arithmetic tests decide the tier

**Test A — how much of the frame does a uniform fit use?**

`fillW = (w × S) / 1920`

**Test B — does the smallest type survive that scale?**

`smallest_source_type × S ≥ 27px`

If B fails, uniform scaling is already impossible: the type needs `27 / smallest_source_type` as a
scale, and the fit only gives you `S`. The ratio between them is how much relative density the
layout has to shed. **The standard Pencil case:** a 1536×1024 design with 12px captions needs 2.25×
for the type but fits at 1.055× — the layout has to give up 2.13× of its density, and no amount of
scaling does that for you. (That ratio is what matters and it is scale-invariant: the same design
measured in 4K space needs 4.5× against a 2.11× fit, which is the same 2.13×.)

| | fillW | Test B | Tier |
|---|---|---|---|
| Source is already 16:9-ish | ≥ 0.92 | passes | **0 — scale only** |
| Landscape but narrow (3:2, 4:3) | 0.75–0.92 | passes | **1 — scale + reposition** |
| Square or portrait | < 0.75 | usually fails | **2 — reflow** |
| Anything, once reflow is exhausted | — | still fails | **3 — stop and ask** |

Common sources against the 1920×1080 canvas:

| Source | Aspect | Fit scale S | Fits to | Horizontal slack | Tier |
|---|---|---|---|---|---|
| 1920×1080 | 1.78 | 1.000 | 1920 | 0 | 0 |
| 1200×675 | 1.78 | 1.600 | 1920 | 0 | 0 |
| **1536×1024 (Pencil)** | **1.50** | **1.055** | **1620** | **300** | **1** |
| 1200×900 | 1.33 | 1.200 | 1440 | 480 | 1–2 |
| 1080×1080 | 1.00 | 1.000 | 1080 | 840 | 2 |
| 1080×1350 | 0.80 | 0.800 | 864 | 1056 | 2 |

Work the ladder in order and stop at the first tier that passes the check. Don't jump to a full
relayout when moving one block sideways does it.

---

## 3. Tier 0 — scale only

Source is 16:9 already. **Don't wrap it in a CSS transform** — render it at its native CSS size and
let the device scale factor do the work. Whole-viewport scaling is guaranteed crisp; a scaled
subtree is not.

```bash
python scripts/render_frames.py --file design.html --fps 25 --out frames/
```

That's the default canvas, so there are no size flags to pass. Output is 3840×2160.

If the design is genuinely authored in 4K coordinates — 54px type, a 3456px content box — render it
in its own space instead, and **do not add `--scale 2`**:

```bash
python scripts/render_frames.py --file design-4k.html --fps 25 --width 3840 --height 2160 --scale 1
```

Both produce 3840×2160 and are equally sharp; only the coordinate system differs. The type floor
follows the CSS canvas automatically — 27px at `--height 1080`, 54px at 2160 — so `--check-fit`
stays correct either way, and a 4K canvas left on the default 2× scale is refused rather than
silently rendered at 7680×4320.

## 4. Tier 1 — scale, then spend the slack

Fit to height, then you have horizontal slack. Two ways to spend it, in this order:

1. **Widen the content.** Let blocks grow into the extra width — a headline that wrapped to three
   lines now takes two, a chart gets longer bars, a table gets breathing room. This costs nothing
   and usually clears the type floor on its own.
2. **Move a block sideways.** Title over chart becomes title left / chart right. Legend under chart
   becomes legend beside chart. KPI stack becomes a strip along the top.

What you must not do is fit-to-height, centre it, and accept the pillarboxing. That's the move that
holds type small: the content ends at 60% of the width while the type sits at 40px, and both
problems have the same fix.

The stage wrapper, when the design's own markup has to stay intact:

```html
<style>
  html, body { margin: 0; }
  #stage  { position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #fff; }
  #design { position: absolute; left: 50%; top: 50%; width: 1536px; height: 1024px;
            transform: translate(-50%, -50%) scale(1.055); }  /* S, to 3 dp */
</style>
<div id="stage"><div id="design"><!-- original markup --></div></div>
```

`--check-fit` still sees overflow through `overflow: hidden`, because it measures geometry rather
than pixels. Once the fit is more than a scale, stop using the wrapper and rewrite the dimensions
natively in the 1920×1080 space — you can't fix type-relative-to-layout through a transform.

For the 1536×1024 Pencil case this is a ~1.06× wrapper, close enough to 1:1 that rewriting natively
is usually easier than reasoning through the transform. Prefer the rewrite.

## 5. Tier 2 — reflow

Square and portrait sources. The layout changes; the content doesn't. Moves that work, roughly in
order of how often they're the answer:

- Vertical stack of N cards → row of N cards
- 2-column grid → 3 or 4 columns
- Title/subtitle block above content → title column on the left, content on the right
- Legend below → legend beside, one item per line
- Wrapped headline → one or two lines, now that width is available
- Long body copy → two columns
- Tall bar chart (bars stacked vertically) → horizontal bars, or the same bars wider

Then set type from the frame, not from the source: 27px floor, 32px comfortable for labels, and
scale headings up from there. Keep every border at 1px or above — at 2× that renders as 2 real
pixels, and anything thinner shimmers on motion and vanishes on compression.

Preserve reading order through all of it.

## 6. Tier 3 — the frame genuinely can't hold it

Reached when the content still won't sit inside 1728×864 at 27px type after a real reflow. Don't
crop, and don't shrink below the floor. Put the options to the user:

1. **Split into two frames** that animate in sequence — often the best answer, and the render track
   handles it natively as two slots or two files.
2. **Move a block to a second graphic** — the user decides which one.
3. **Drop a decorative element** — ask; the user did the cleanup pass and knows what's load-bearing.
4. **Type at exactly 27px** everywhere, accepting a dense frame.

State which one you'd pick and why, with the measured numbers behind it. This is a 30-second
decision for the user and it beats discovering the crop in the edit.

---

## 7. Verify, then show the still

```bash
python scripts/render_frames.py --file fitted.html --check-fit --out fit/
```

Acceptance, all of them:

- No content element crosses the frame edge — the check fails hard on this
- No text under 27px
- Content inside the safe box, or a deliberate reason it isn't
- No stroke under 1px
- Content uses ≥75% of the frame width
- Every word, number and element from the source is still present, in the same order

Then **show the user `fit-check.png` and get a yes before animating.** It's one still and it costs
nothing. Every fit problem is cheap here and expensive after 1500 frames have rendered.

---

## Split canvases — the ⅓ and ⅔ variants

A split variant is a **second fit of an already-approved full-frame master** (SKILL.md → Formats
decides which assets get one). The frame changes; every rule on this page still applies.

| | ⅓ split | ⅔ split |
|---|---|---|
| Author (CSS px) | 640 × 1080 | 1280 × 1080 |
| Output (@2x) | 1280 × 2160 | 2560 × 2160 |
| `--check-fit` flags | `--width 640 --height 1080` | `--width 1280 --height 1080` |
| Side margins (5% of width) | 32px | 64px |

Height is unchanged, so every height-derived number holds as-is: **27px type floor**, 54px top
margin, **162px bottom margin** — subtitles run across the full video frame and pass under the
panel, so the subtitle band clears here too.

The reflow is almost always side-by-side → stacked: labels move above their tracks, legends go
one item per line, a headline block sits over its content instead of beside it. Data marks keep
their exact fractions. **The words never change** — a reflow that comes back reworded has failed;
restore the exact copy.

The cue table stays the master's, verbatim — same anchors, same local frames. The variant is a
swap for the editor, never a re-time.

**`--check-fit` is blinder here than usual.** It measures frame edges and the type floor; it
cannot see two elements overlapping, and a narrow column makes overlaps far more likely. Still
the layout and look at it, element by element, before rendering.

### The 640×1080 canvas doubles as the vertical (Shorts) deliverable

Every asset ships a **1280×2160 vertical** for Shorts repurposing; for assets with a ⅓ split it's
the same file. It is deliberately not 9:16 — in the Shorts edit it's either **side-cropped to
true 9:16** (a centred 1215 of the 1280 output survives; 32.5px lost per side) or **downscaled
onto a 9:16 background** (everything survives, platform UI still overlays). Design for both:

- Content inside the 32px CSS side margins (content ≤ 576 CSS = 1152 output) clears the 1215
  crop with ~30px to spare per side — the margin the user asked for.
- Keep must-survive content **mid-frame vertically**: run as a full Short, platform UI covers
  roughly the top 9% (~97px CSS) and the bottom 20% (~216px CSS).

The vertical starts at the **design stage** — every graphic gets a horizontal and a vertical
design variant, and the fit pass runs per variant. A vertical is a reflow of the design's
content, never a scaled or squeezed horizontal.

---

## Reference numbers — full-screen 16:9

Author against the **CSS px** column. The device px column is what lands on the timeline; it is
never something you type into the design.

| | CSS px (author here) | Device px (output) | Derivation |
|---|---|---|---|
| Frame | 1920 × 1080 | 3840 × 2160 | 16:9, `--scale 2` |
| Safe margin, top | 54px | 108px | 5% |
| Safe margin, left / right | 96px | 192px | 5% |
| Safe margin, bottom | 162px | 324px | 15% — subtitle band |
| Content box | 1728 × 864 | 3456 × 1728 | frame minus margins |
| Type floor | 27px | 54px | 2.5% of frame height |
| Type, comfortable | 32px+ | 64px+ | labels and captions |
| Stroke floor | 1px | 2px | below this it shimmers on motion |

`--check-fit` derives all of these from `--width`/`--height`, so they follow automatically if you
ever render a design in its own 4K coordinate space — the right-hand column then becomes the one
you author against.

**Native 9:16 panels are a different spec again** — and no longer the default vertical path (the
house vertical is the 1280×2160 export above). Build one only when a true 9:16 master is
explicitly requested: authored at 1080×1920 CSS @2x and placed at 56.25%, so everything shrinks —
type floor 48px, stroke floor 2px, safe margins 173/130/384/60. Pass
`--width 1080 --height 1920 --type-floor 48 --safe 173,130,384,60` to `--check-fit`, and read
`~/.claude/skills/video-07-graphics-placement/reference/geometry.md` for the placement maths.
The ⅓ split / vertical renders at native size (27px CSS floor holds); the 9:16 panel shrinks at
placement (96px source floor). Pick by destination, never mix the numbers.
