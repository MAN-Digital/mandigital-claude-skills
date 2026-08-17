# MAN Digital Brand Tokens for Lucid

Embedded so the skill never depends on locating a brand file. Authoritative source: `man-digital-blog-graphics/references/brand-rules.md`. If that skill updates, reconcile here.

## Palette (hex — use exactly)

| Token               | Hex                   | Use in a chart                                                                                               |
| ------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ |
| Medium Blue         | `#000FC4`             | **Anchor.** Entry/terminal nodes, primary node fills, key borders, emphasized connectors, headings on light. |
| Fluorescent Cyan    | `#2DE4E6`             | Sharp accent only — a highlighted node, signal mark, "active" state. Never a body fill for many nodes.       |
| Ghost White         | `#F7F7FF`             | Canvas background; text on blue fills; soft panel/surface.                                                   |
| Black               | `#0A0A0A`             | High-contrast text when `#222222` is too light.                                                              |
| Dark Text           | `#222222` / `#434343` | Body/label text on light surfaces. `#434343` also = neutral/secondary node fill.                             |
| Light Blue Surface  | `#ECF1FB` / `#EDF2FB` | Card / process-step / diagram-panel background ("white card on blue").                                       |
| Light Purple Stroke | `#C8CCF2`             | Default borders and connector lines on light surfaces.                                                       |
| Orange              | `#F26419`             | **Restrained** CTA/accent — at most one node or one critical marker. Never a whole branch/lane.              |
| Muted Indigo        | `#5963D9`             | Quiet category/secondary-group accent when Medium Blue is too dominant.                                      |
| Neutral Charcoal    | `#434343`             | Subdued category accent, neutral/nurture nodes, secondary cue.                                               |

Multi-topic accent set (tabs, departments, grouped lanes): `#5963D9`, `#F26419`, `#434343`, anchored by `#000FC4` headings + `#222222` body. Avoid rainbow palettes.

## Fonts

- **Montserrat** — headings, titles, node headers (`bold: true` / semibold).
- **Lato** — labels, body, pill/edge text.
- Set via `lucid_edit_item(font_family="Montserrat" | "Lato")`. The canvas falls back if the font is not installed in the user's Lucid org — verify in the exported PNG; if it falls back, say so rather than claiming Montserrat.

## Canonical Semantic Color-Role Map (do not improvise)

Apply per node by its role in the diagram:

| Node / element role                              | Fill                                       | Border (`line_color`)  | Text                  |
| ------------------------------------------------ | ------------------------------------------ | ---------------------- | --------------------- |
| Entry / start / terminal                         | `#000FC4`                                  | `#000FC4`              | `#F7F7FF`             |
| Standard process step ("white card on blue")     | `#F7F7FF` or `#ECF1FB`                     | `#000FC4` or `#C8CCF2` | `#222222`             |
| Decision diamond                                 | `#F7F7FF`                                  | `#000FC4`              | `#222222`             |
| Signal / highlight / "active" / positive outcome | `#2DE4E6` tint or `#ECF1FB` w/ cyan border | `#2DE4E6`              | `#222222`             |
| Secondary / nurture / neutral                    | `#434343` or `#5963D9`                     | same                   | `#F7F7FF`             |
| Single CTA / critical step (max one)             | `#F26419`                                  | `#F26419`              | `#F7F7FF`             |
| Connectors / lines (default)                     | —                                          | `#C8CCF2`              | `#222222` edge labels |
| Connectors needing emphasis (primary path)       | —                                          | `#000FC4`              | —                     |
| Canvas / page background                         | `#F7F7FF`                                  | —                      | —                     |

Rules:

- Every accent/border must visibly contrast its parent surface. Never set a border or chip to the same color as its card (e.g. white-on-white). On a white card, make the cue `#000FC4`, `#2DE4E6`, or `#5963D9`.
- Use structure (lanes, rails, section headers, label chips) before adding more color.
- Keep it minimal and credible — modern B2B strategy work, structure first, decoration second.

## RevOps domain defaults (MAN Digital's core)

For RevOps / CRM / signal-engine / lifecycle charts: anchor stages in Medium Blue, render system/data nodes as white-card-on-blue with blue borders, mark the one "signal" or "scoring" moment in cyan, and reserve orange for a single conversion/CTA point. This reads as the MAN Digital signal-engine aesthetic without inventing new motifs.
