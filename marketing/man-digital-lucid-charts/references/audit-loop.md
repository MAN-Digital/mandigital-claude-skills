# Audit & Critique Loop

Run this before showing any Lucid chart to the user. A clean tool response and your sizing math are **not** a pass — Lucid renders text larger than naive math predicts, auto-fits boxes, and routes connectors in ways you didn't intend. The export is the truth, and you must **loop**: screenshot → measure → critique → fix → re-screenshot.

## The mindset (non-negotiable)

> An engineer built this. Is it a _nice way to present it to a human?_

Technically-fits ≠ presentable. Look at the export the way a designer or an exec would: Is it calm or cramped? Does text breathe? Is anything overlapping, clipped, or spilling out? Could you put this on a slide without wincing? Be harsh. Most first drafts from a spec look like an engineer's dump — your job is to make it look designed.

## Tools (the Lucid equivalents of blog-graphics' screenshot/measure stack)

1. `lucid_export_document_as_PNG` — the full-canvas screenshot. Study it as a designer, not just for technical fit.
2. `fetch` — every item's `BoundingBox` + text + colors. This is your measurement tape (the `snapshot_layout`/`batch_get` equivalent). Compute the rect/overflow checks from it.
3. **Zoom (no per-shape crop tool exists).** Lucid has no "render this one shape" API — `lucid_fetch_item_image` only returns images _attached to image-type items_, not a crop of a rectangle. So "zoom" = study the full PNG closely at the trouble spot **and** measure that item from `fetch` geometry (its `BoundingBox` vs its text). When in doubt, temporarily move a suspect box to empty space, re-export, inspect, move it back — or just trust the geometry math.
4. `lucid_search_document` — locate which region holds a given label so you can measure/inspect it.

## The loop (up to 3 rounds — Lucid surprises you, so re-export every time)

1. **Export** the PNG. **Fetch** geometry.
2. **Critique** against the scorecard below. Write a short, strict internal critique. Name the exact offending items.
3. **Zoom** every risky region with `lucid_fetch_item_image` (any box with multi-line text, any connector label, any header with a long name).
4. **Fix** the critical issues (resize box, drop font, shorten copy, re-align, move a box out of a connector's path, blank/relocate a crowded label).
5. **RE-EXPORT and re-critique.** Do not declare done from the first export. Loop until it passes or 3 rounds; if still imperfect, tell the user the exact remaining limitation — never ship-and-stay-silent.

## Scorecard (1–10 each; pass = every dimension ≥ 8)

| Dimension                   | What "good" means                                                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Breathing room**          | Boxes aren't cramped; text has clear padding top/bottom/sides; nothing kisses an edge; generous gaps between boxes; the canvas feels calm, not packed. |
| **Text fit**                | No glyph crosses a box border; nothing clipped, wrapped-and-clipped, or spilling out; no oversized text dominating a box.                              |
| **No overlaps**             | No box, label, or connector overlaps another box or text (header/body pair excepted).                                                                  |
| **Connector clarity**       | Lines run in clean lanes, land on box edges, never pass _through_ a box; labels sit on empty canvas; no spaghetti/crossings.                           |
| **Hierarchy & readability** | Clear scale: title > section label > entity name > body. Scannable in ~3 seconds. Consistent type.                                                     |
| **Alignment**               | Boxes share a grid; columns line up; section labels align to their column; nothing floats off-axis.                                                    |
| **Brand**                   | `#000FC4` anchor, Ghost White surfaces, restrained cyan/orange, Montserrat headers / Lato body.                                                        |
| **Presentation polish**     | Would you put this in front of a client without apologizing? No "engineer dump" feel.                                                                  |

`≥8` all → pass. `6–7.9` → fix criticals and re-loop. `<6` → the layout/spacing is wrong; rethink it (wider canvas, fewer words, bigger gaps), don't nudge.

## Hard fails (any one = not done, even if the tool response was clean)

- Any text crosses, touches, or spills out of its box border. **(The #1 "it's a mess" complaint.)**
- A connector line passes _through_ a box, or a connector label sits on top of a box/another label.
- Connector labels are scattered at elbow jogs or floating in odd spots. Labels pin to the line midpoint and can't be moved via the API — fix this by **spacing boxes generously** so each midpoint lands in the open gap (and use a standalone `TextBlock` only if one label truly needs a fixed spot). **Do NOT delete a meaningful label (associations like `linked to` included) to reduce clutter — keep the information, fix the placement.**
- Two boxes overlap (except a header on its body).
- A title or section label is truncated or wrapped-and-clipped.
- A box is cramped — text touching the edges, no breathing room.
- Text is so large it wraps unexpectedly or dominates the box (Lucid auto-sizes big — set `font_size` down explicitly and verify on the PNG).
- Inconsistent box sizes / drifting alignment that reads as an engineer's dump rather than a designed layout.
- You declared it done from a single export without a second audit round.

## Breathing-room rules (the user's core complaint, made mechanical)

- **Text occupies ≤ ~50% of its box.** Leave generous padding above and below — the box should look half-empty. If text fills more than half, the box is too small or the copy/font is too big — enlarge the box, shorten the copy, or drop the font; never accept edge-to-edge text.
- **Set font sizes down explicitly.** Lucid's default/auto sizing renders large. Body 13–15, header 15–16, title 22–26 — and confirm on the PNG, because the renderer may still go bigger than the number implies.
- **Fewer words per box.** One idea, a short phrase. Whitespace carries calm; density carries stress.
- **Generous gaps:** ≥ 60–80 px between boxes and columns so the diagram breathes.
- **Math is a floor, the PNG is truth.** Add ~25% margin to every width estimate, and always re-export after any text/size/box change.

```
overflow check (per text box, from fetch):
  estimated_text_width  = longest_line_chars × font_size × 0.6 × 1.25   (the 1.25 = Lucid renders bigger)
  estimated_text_height = rendered_lines × font_size × 1.5
  FAIL if estimated_text_width  > box_w − 24
  FAIL if estimated_text_height > box_h − 16
```

## Internal critique format (keep it short, be strict)

```
### Audit round N
Status: PASS | FIX-AND-RELOOP | FAIL
Breathing room: N/10 · Text fit: N/10 · Overlaps: N/10 · Connectors: N/10
Hierarchy: N/10 · Alignment: N/10 · Brand: N/10 · Polish: N/10
Critical fixes:
  - <item id / region>: <exact issue> -> <exact change>
Remaining after fix:
  - <what still isn't perfect, if anything>
```

Only surface the audit report to the user when they ask or when a real limitation remains. Otherwise just fix it and show the clean result.
