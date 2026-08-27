# Frame Geometry Reference

Deterministic. Arithmetic, not judgment.

## Canvas

Three build types. Every graphic is exactly one, and the graphics map says which.

| Type | Design canvas | Used as |
| --- | --- | --- |
| **FULL SCREEN** | **3840 × 2160** (16:9 4K) | full frame in the horizontal cut only |
| **SPLIT ⅓ / ⅔** | **1280 × 2160** / **2560 × 2160** (native, exact thirds) | split-screen beside the speaker in the horizontal cut, driven by the MD preset kit; the ⅓ canvas doubles as the house vertical export |
| **VERTICAL** | **1280 × 2160** (standing deliverable, every asset) | Shorts repurposing — side-cropped to 9:16 or downscaled onto a background |
| **PANEL** | **2160 × 3840** (9:16 4K) | native 9:16 master — only when explicitly requested |

---

## Split-screen thirds (in-video)

The split widths are **literal thirds of 3840 on purpose**: 1280 = ⅓, 2560 = ⅔. The Premiere
preset kit is built around them, so the choreography is drag-and-drop:

- Graphic clip: `MD3 Graphic <side> 1/3|2/3 In` slides it in attached to its edge; `… Out` exits
  anchored to the clip's out point. Drop shadow onto the footage is included. Full-frame graphics
  use `MD3 Graphic Slide <side> Full In/Out` (the Full pair carries "Slide" in the name).
- Footage: `MD2 Slide <opposite side> 1/3|2/3 In` moves the shot to the exact centre of the
  uncovered slot — ±⅙ of frame width beside a ⅓ graphic, ±⅓ beside a ⅔ graphic — with `Hold` on
  every clip between and `Back` on exit. Full-screen graphics need no MD2 dodge — the footage is
  fully covered.

Speaker slot beside a ⅓ graphic: **2560×2160** (1.19:1, comfortable medium shot). Beside a ⅔
graphic: **1280×2160** — a tight vertical slot; the ⅔ split therefore suits stretches where the
graphic carries the frame and the speaker is presence, not subject.

Splits render **native** — no placement shrink — so floors are the full-screen ones: type ≥54px,
strokes ≥2px, top 108 / bottom 324 (subtitles cross the whole frame beneath the panel), sides 5%
of the panel's own width (64px on 1280, 128px on 2560).

A split is a reflow of an approved full-screen master and inherits its cue table verbatim (same
anchors, same local frames) — editor swaps master ↔ variant with zero timing work.

**1280×2160 is also the house vertical export** (the user's explicit choice, 2026-08-01 — aware
it is not 9:16). Every asset ships one for Shorts repurposing: in the vertical edit it is either
**side-cropped to true 9:16** — a centred 1215×2160 window, costing 32.5px per side — or
**downscaled onto a 9:16 background**. An asset with a ⅓ split already has its vertical (same
file); full-screen and ⅔ assets get a dedicated 1280×2160 adaptation, and that adaptation starts
at the **design stage** (each graphic gets a horizontal and a vertical design variant), never as
a squeeze of the horizontal. Content must clear the 1215 crop with margin: keep it inside the 5%
side margins (64px each side → content 1152) and keep critical content mid-frame — Shorts UI
covers roughly the top 9% and bottom 20%. The PANEL spec below remains for builds that must be
*native* 9:16 masters; it is no longer the default vertical path.

---

## Why the PANEL is 2160×3840 and not a literal third

A third of 3840 is 1280. But **1280×2160 is not 9:16.**

```
1280 / 2160 = 0.5926        9 / 16 = 0.5625
```

Build the panel at 1280 wide and promoting it to a 2160×3840 vertical master distorts it by **+5.3% horizontally**, or costs you a 65px crop or letterbox on every conversion. Which puts you back in rebuild territory, the exact thing the third-frame convention exists to avoid.

**The true 9:16 panel at 2160 tall is 1215×2160.** That is 31.6% of frame width, so "a third" is the right instinct, just 65px generous.

## The workflow that makes conversion free

Design in the vertical master, not the horizontal one.

```
SOURCE DESIGN     2160 x 3840   (9:16 4K native)
        |
        +-- place at 56.25% -->  1215 x 2160   in the 3840x2160 horizontal master
        |
        +-- place at 100%   -->  2160 x 3840   in the 9:16 vertical master
```

56.25% is exact (2160 ÷ 3840), so there is no distortion in either direction and no resampling artefact. You design once, place twice. Vertical conversion becomes a re-time and a re-layout of the lower third and subtitles, never an asset rebuild.

**Derived type floor.** Legibility floor is roughly 2.5% of frame height, so 54px in the 3840×2160 master. Since the panel sits at 56.25%, **the smallest type in your source design must be at least 96px.** Call it 100px for labels, and scale headlines from there. Anything that cannot hold its content at 100px minimum is carrying too much for a panel and belongs full screen.

**Speaker area beside a panel:** 2625×2160, aspect 1.22:1. Comfortable for a medium shot, slightly off-centre framing.

---


---

## Safe area for PANEL builds

The panel appears in two contexts with different obstructions. Design to the intersection of both.

| Margin | Source px | Driven by |
| --- | --- | --- |
| Top | **346** | Shorts progress bar / title |
| Bottom | **768** | Shorts caption + handle zone |
| Left | **120** | breathing room |
| Right | **259** | Shorts action rail (like / comment / share) |

**Content box: 1781 × 2726** — 59% of the panel. Nothing meaningful outside it.

Note on the bottom margin: subtitles run across the full 3840 frame in the horizontal cut, so they pass *underneath* the panel. That band needs 576px measured in source coordinates. The Shorts caption zone at 768px is deeper, so clearing the vertical requirement automatically clears the horizontal one. Design for 768.

---

## Minimums, non-negotiable

Panels are placed at 56.25% in the horizontal master, so everything shrinks. These floors exist so nothing disappears.

| | Source minimum | Lands at |
| --- | --- | --- |
| Type (smallest label) | **96px** | 54px, the legibility floor |
| Type (comfortable) | **114px** | 64px |
| Stroke / border | **4px** | 2.25px |
| Accent bar | **6px** | 3.38px |

**Hairlines do not survive.** A 1px border becomes 0.56px and a 2px border becomes 1.12px, which means it vanishes or shimmers on motion. If the existing blog designs use 1px or 2px card borders, dotted grid decorations or thin dividers, those all need thickening to 4px minimum.

If a panel cannot hold its content at 96px type and 4px strokes, it is carrying too much and should be split or moved to full screen.

---

## Two rules that make vertical conversion free

**Full-bleed background, inset content.** Build the background to the full 2160×3840 edge and keep every element inside the safe box. In horizontal the background reads as a solid side panel against the speaker; in vertical at 100% it already fills the frame. Nothing to add at conversion.

**No drawn divider.** Do not draw an edge between the panel and the speaker area. The background's own edge does that job in horizontal, and in vertical that same edge becomes the frame boundary, where a drawn divider looks like a mistake.

---

## Render

One comp, two outputs. Never scale in Premiere.

```
COMP  2160 × 3840
  ├─ Output A → resize to 1215 × 2160   (drops into the 16:9 timeline at 100%)
  └─ Output B → 2160 × 3840 at 100%     (vertical master)
```

56.25% is exact (2160 ÷ 3840), so neither output is distorted and neither is resampled twice. Design big, render small. Never build at 1215×2160 and upscale later: that is a 177.8% enlargement inventing 3.16× the pixels, and it is visible on type and thin strokes.

---

## Speaker area

With a panel placed, the speaker occupies **2625 × 2160**, aspect 1.22:1. Comfortable for a medium shot, slightly off-centre framing. Left or right placement both work; keep it consistent within a chapter.

---

---

## Full-screen assets (different numbers — do not let the panel spec leak)

| | Full screen 3840×2160 | Panel 2160×3840 |
| --- | --- | --- |
| Top | 108px | 346px |
| Left / right | 192px | 120 / 259px |
| Bottom | **324px** (subtitle band) | 768px |
| Content box | 3456 × 1728 | 1781 × 2726 |
| Type minimum | **54px** | 96px |
| Stroke minimum | **2px** | 4px |

Full-screen assets are far more generous because no 56.25% reduction applies.

## Verify the source canvas first

Assets built for the web are often neither 16:9 nor 9:16. A 1536×1024 (3:2) source fitted to a 3840×2160 frame leaves 600px blank at full height, or overflows by 400px at full width.

Check every type tier against the floor at the intended placement scale. Uniform scaling cannot rescue type that is already too small relative to its layout — the type must grow relative to the layout, which means the layout gives up density. That is the real adaptation work and it is invisible until measured.
