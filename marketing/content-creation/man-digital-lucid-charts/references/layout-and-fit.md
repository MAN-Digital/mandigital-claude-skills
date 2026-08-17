# Layout & Fit — compute before building

The goal: the **first** export is clean. No text out of its box, no overlaps, no truncation, no cramping. These are not taste calls — they are arithmetic. Do the math up front and the audit becomes a confirmation, not a rescue.

## Rule 0 — Spec builds STRUCTURE; the edit loop builds TYPE

`lucid_create_diagram_from_specification` is unreliable for text:

- **`\n` in spec `text` collapses to spaces** → multi-line content renders as one wrapped blob.
- **Text-type shapes (`"type":"text"`) ignore spec `textColor`** → titles/wordmarks come out black.
- Spec text has **no font, no size, no alignment** control.

Therefore: in the spec set only `boundingBox`, `fill`, `stroke`, and a placeholder `text`. Then in the **`lucid_edit_item` typographic pass**, set for every text-bearing item: real multi-line `text` (newlines survive here), `font_family`, `font_size`, `text_align`, `text_v_align`, `text_color`, `bold`. Treat this pass as mandatory, not optional polish.

## Rule 1 — Font sizes by role (readability floor)

| Role                  | font_size | family          | align          |
| --------------------- | --------- | --------------- | -------------- |
| Title                 | 22–26     | Montserrat bold | center         |
| Subtitle              | 13–15     | Lato            | center         |
| Entity / node header  | 15–16     | Montserrat bold | center         |
| Attribute / body line | 13–14     | Lato            | left, v-middle |
| Zone / section label  | 11–12     | Montserrat bold | center         |
| Connector label       | 11–12     | Lato            | —              |

Never go below these. If text won't fit at the floor size, the box is too small or the copy is too long — fix the box or the copy, never the readability.

## Roomy grid defaults (START HERE — generous space is the default, not an afterthought)

Cramped diagrams read as an engineer's dump. Default to lots of whitespace; tighten only if asked. These numbers produced a clean, breathing chart and are the baseline:

| Thing                                   | Default                                                                                                                                                          |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Box width                               | **300** (room for a 2-line description without wrapping mid-word)                                                                                                |
| Entity height                           | header **46** + body **96** = 142                                                                                                                                |
| **Column pitch** (box-left to box-left) | **≥ 560** (300 box + ~260 gap) — never less than 1.8× box width                                                                                                  |
| **Row pitch** (box-top to box-top)      | **≥ 320**, i.e. **≥ 180 px of clear vertical gap** between one box's bottom and the next box's top — never less than 2× entity height                            |
| Body font                               | **13** (Lato) · Header font **14** (Montserrat bold) · Title 22–26 · Section label 11                                                                            |
| **Text fill**                           | text must occupy **≤ ~50% of the box area** — short phrase, centered, oceans of padding. If a box looks more than half-full, enlarge the box or shrink the font. |

When unsure, **add space and shrink text** — never cram. A bigger canvas is free; a cramped one looks bad. Make the text smaller before you make a box tighter. More breathing room almost always reads better — err generous.

## Connector labels — they pin to the line midpoint and CANNOT be moved via the API

`lucid_edit_item` can set a connector's label **text** but not its position — Lucid always parks the label at the line's midpoint. When labels look "all over the place," that is a **placement** problem to fix, NOT a reason to delete the labels.

- **NEVER delete a meaningful relationship label to tidy the canvas.** Keep every relationship labeled — **associations included** (`linked to`, `belongs to`, `worked by`). The label carries information the reader (and the user) wants. Removing labels to reduce clutter is a regression, not a fix. (Real mistake: the Contact/Company→Deal `linked to` labels were deleted to "tidy up" — the user wanted them kept.)
- **Fix placement by spacing, not deletion.** With the roomy grid (≥260 px column gaps), the line's midpoint lands in the open gap between columns, so the label sits cleanly there. Tight layouts push the midpoint onto a box or an elbow jog — the answer is more space, not fewer labels.
- Keep labels to **1–2 words** so they fit in the gap.
- If a specific label genuinely must sit somewhere the midpoint won't reach, blank that connector's own label and add a standalone `TextBlock` placed by hand near the line — but keep the label.

## Rule 2 — Box sizing math (prevents text-out-of-box)

Constants: `LINE_H = font_size × 1.5`, `PAD_X = 12`, `PAD_Y = 10`. Character width ≈ `font_size × 0.6` (Lato) / `× 0.62` (Montserrat bold).

- **Width needed** (no wrap): `W_req = longest_line_chars × char_w + 2×PAD_X`.
- **Lines after wrap**: a logical line wraps if `line_chars × char_w > box_w − 2×PAD_X`. Count wrapped lines, not logical lines.
- **Height needed**: `H_req = rendered_lines × LINE_H + 2×PAD_Y`.

Rules:

- Set `box_w ≥ W_req` for the longest line so attribute rows stay **one line each** (preferred), OR accept the wrap and grow `box_h` to the post-wrap line count.
- Set `box_h ≥ H_req` using the **worst-case rendered line count**, not the attribute count. A long token (`subscription_id`, `payment_link_id`) wraps and silently adds a line — size for it.
- If a label is long, **widen the entity** (≈280–320 for ERD tables) or drop the body to 13 px before letting it wrap.
- Header sits flush on the body: `header.y + header.h = body.y`, identical `x` and `w`.

## Rule 3 — Spacing & grid (prevents overlap)

- **Title band:** title + subtitle live in a reserved strip at the top. The first content row starts **≥ 40 px below the subtitle's rendered bottom**. Title `box_w ≥ W_req` so it never wraps down into the content. Center the title on the **whole diagram** (`x_center = (minX+maxX)/2`), not over one column.
- **Column gap ≥ 80 px** between zone columns; **row gap ≥ 40 px** between stacked shapes in a column.
- Compute each shape's full rect `(x, y, x+w, y+h)` and verify **no two rects overlap** except a header/body pair. Two boxes overlap iff `ax < bx+bw AND ax+aw > bx AND ay < by+bh AND ay+ah > by`.
- Size the canvas to content + margin. Adding space always beats crowding.

## Rule 4 — Labels & pills (prevents truncation)

- A zone/section label or pill must have `box_w ≥ label_chars × char_w + 24`. If the box is narrower, Lucid wraps then clips it (this is how "SELLING & AGREEMENT" became "SELLING &"). Either widen the box or shrink the font until one line fits with margin.
- Block-type label boxes carry heavier internal padding than text boxes — give them ~24 px slack and `box_h ≥ LINE_H + 12` for one line.
- **Multi-word Block labels wrap even when the width would fit one line.** To force a single line, make the box generously wide AND keep `box_h ≤ 1.5 × LINE_H` so there is no vertical room for a second line. Confirmed fix: "SELLING & AGREEMENT" stayed truncated at `w=300,h=34` but rendered full at `w=360,h=30`. If you instead want a deliberate two-line label, set `box_h ≥ 2 × LINE_H + 12` so the second line is contained, not spilled as ghost text below the box.
- Place a zone label ≥ 12 px above its first entity, aligned to the column's left edge.

## Rule 5 — Connector labels (prevents label-on-shape)

- Keep labels 1–2 words.
- The default label position is the line midpoint — if that midpoint sits over a shape, move it: set the label `position` toward the open segment (`0.2`–`0.3` or `0.7`–`0.8`) and `side` `"top"`/`"bottom"` so it lands on empty canvas.
- Don't route a labeled connector through the gap a shape occupies; give parallel relationships separate corridors. Drop a redundant label rather than stack two over the same spot.

## Rule 6 — FIT GATE (run before claiming done — mechanical, not vibes)

From the `fetch` geometry **and** the export PNG (zoom risky nodes):

1. Every text shape: rendered bottom ≤ `box_h − PAD_Y` **and** longest line ≤ `box_w − PAD_X`. No glyphs crossing a border.
2. Every label/pill: full text visible, not truncated or wrapped-and-clipped.
3. Every shape pair: no overlap (except header/body). Run the rect test.
4. Title & subtitle: single line each, clear of zone labels and entities by ≥ 40 px.
5. Every connector label: sits on empty canvas, not on a shape, and is readable.
6. No box is more than ~40% empty (cramped is bad, but so is a near-empty box implying missing content).

If any check fails, fix the geometry (resize/move/reflow) and re-export. Only a passing gate + a clean PNG = done.

## Worked example (the HubSpot ERD)

- Entity tables `w=250–260`; long-token entities (Subscription, Invoice, Payment Link) widened or dropped to body 13 px + `h=120` so `subscription_id`/`payment_link_id` don't overflow.
- Title 22 px, single line, band y=0..50; subtitle 13 px at y=54; first entities at y≥120 → ≥ 40 px gap. (At 30 px the title wrapped onto the SELLING label — Rule 3 violation.)
- Zone pills sized to text: "SELLING & AGREEMENT" needs `w ≥ 19×7.4+24 ≈ 165`; at 11 px bold give it `w=300, h=34` for safety. (Earlier `w=250,h=30` clipped it — Rule 4.)
- Attribute bodies: Lato 14, left, v-middle; newlines set in the edit pass (Rule 0), not the spec.
