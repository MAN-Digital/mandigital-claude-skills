---
name: man-digital-lucid-charts
description: Use when creating, editing, or branding any chart, diagram, flowchart, process map, lifecycle/funnel, RevOps or CRM/system-architecture diagram, org chart, mind map, or UML sequence diagram in Lucidchart / Lucid via the @lucid MCP connector — especially when the output must look MAN Digital branded rather than using Lucid's default theme.
---

# MAN Digital Lucid Charts

Create on-brand MAN Digital diagrams with the `@lucid` (Lucidchart) MCP connector.

**Core principle:** Lucid's creators apply _Lucid's_ blue theme and _Lucid's_ default font, never MAN Digital's. A chart is not on-brand until you (1) inject brand color at creation where the tool allows it, and (2) run the **brand restyle + font loop** afterward. Skipping the loop = a Helvetica, Lucid-blue chart that fails the brand gate. This was the exact failure in baseline testing.

`@lucid` tools are named `mcp__bab947f5-61a4-4385-bbab-d73ba922fdd4__lucid_*` plus a `…__fetch`. Load schemas on demand with `ToolSearch` query `select:<full_tool_name>`.

## When to Use

- Any request for a Lucidchart/Lucid diagram, flowchart, process map, RevOps/CRM architecture, signal-engine map, org chart, mind map, funnel, lifecycle, or sequence diagram.
- "Make this in Lucid", "@lucid", "Lucidchart", or a `lucid.app` URL is mentioned.
- **Not for** Pencil `.pen` blog/social graphics → use the MAN Digital Pencil graphics skill (`man-digital-blog-graphics` / `man-digital-marketing-assets`). Lucid is for editable structured diagrams (flow/architecture/hierarchy), not hero images or carousels.

## Required Startup

1. Read `references/brand-tokens.md` — the embedded MAN Digital palette, fonts, and semantic color-role map. **Do not improvise color roles or hunt for a brand file; this is the source of truth.**
2. Read `references/lucid-workflow.md` — tool routing, the restyle loop, parameters, and gotchas.
3. Read `references/svg-templates.md` when building a flowchart, process map, or architecture diagram (the SVG path carries brand color through at creation).
4. Read `references/layout-and-fit.md` — **mandatory.** Deterministic sizing/spacing/placement math. The starting point for geometry.
5. Read `references/audit-loop.md` — **mandatory.** The screenshot → measure → critique → fix → re-screenshot loop with a designer's eye. A chart is NOT done until you have run this loop (≥2 rounds) and it passes. Your sizing math is only a first guess; Lucid renders text bigger than the math and the PNG is the truth.

## Pick the Creation Tool by Chart Type

| Chart type                                                         | Primary tool                                                                                                      | Brand color at creation?                       |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Flowchart / process / lifecycle / **RevOps & system architecture** | `lucid_convert_svg_to_diagram` (author a brand-styled SVG — see `svg-templates.md`)                               | **Yes** — inline hex passes through            |
| **Org chart / reporting hierarchy**                                | `lucid_convert_svg_to_diagram` (a hierarchy is just `<rect>`+`<text>`+`<line>`). **NOT `lucid_create_org_chart`** | **Yes** — via SVG                              |
| **Mind map / topic tree**                                          | `lucid_convert_svg_to_diagram` (radial/tree of `<rect>`+`<line>`). **NOT `lucid_create_mind_map`**                | **Yes** — via SVG                              |
| Flowchart needing Lucid-native shapes (BPMN, swimlane, UML class)  | `lucid_create_diagram_from_specification` (read `lucid://diagram-specification` first; set per-shape `style` hex) | Yes (per-shape)                                |
| UML sequence                                                       | `lucid_create_sequence_diagram` (PlantUML; read `lucid://sequence-diagram-specification` first)                   | Partial via skinparam → finish in restyle loop |

**The SVG path is the default for almost everything.** It gives full control of color, layout, and labels in one call. Critically, **`lucid_create_org_chart` and `lucid_create_mind_map` produce `TreeNodeBlock`s that silently ignore `lucid_edit_item`** — every restyle call returns `success:true` and changes nothing, so they **cannot be branded** (confirmed in testing). Do not use them when brand fidelity matters; build the hierarchy as SVG instead. The Standard Import (`from_specification`) and sequence paths _are_ editable and only need the font/restyle finish.

## Audience: technical vs plain-language (decide first)

Ask or infer who reads the chart — it changes the content, not just the styling:

- **Technical / data reader → full ERD:** entity tables with PK/FK attribute rows, real field names, crow's-foot cardinality (endpoint styles `CFN ERD One Arrow` / `Many` / `Zero Or More`…).
- **Non-technical / exec / GTM / marketing reader → plain-language map:** one-line friendly description per box (no PK/FK, no `snake_case`), **simple arrows** (`endpoint2_style: "Arrow"`, `endpoint1_style: "None"` — not crow's foot), everyday relationship verbs ("becomes a", "if signed", "is paid by", "bills each cycle"), and **human section labels** ("WHO YOU SELL TO", "GETTING PAID" — not "CRM CORE", "CASH COLLECTION"). Centered descriptions, tighter boxes.

Default to plain-language for stakeholder/overview/marketing requests; build the formal ERD only when the reader is technical or explicitly asks for an ERD/schema. "Make it friendlier for non-engineers" = convert an ERD to the plain-language map above.

## Layout & Fit — compute BEFORE building (full math in `layout-and-fit.md`)

Most "bad chart" defects are arithmetic, not taste. Decide geometry before you emit any JSON:

- **Spec builds structure, the edit loop builds type.** `create_diagram_from_specification` collapses `\n` to spaces, ignores `textColor` on text shapes, and sets no font/size/align. So set only `boundingBox`/`fill`/`stroke` in the spec, then set real multi-line `text` + `font_family` + `font_size` + `text_align`/`text_v_align` + `text_color` in the `lucid_edit_item` pass. Newlines survive there.
- **Size every box to its worst-case (post-wrap) text:** `H ≥ rendered_lines × font_size × 1.5 + 20`; `W ≥ longest_line_chars × font_size × 0.6 + 24`. A long token (`subscription_id`) wraps and adds a line — size for it or widen the box.
- **Reserve a title band:** title (single line, box wide enough not to wrap) + subtitle at top; first content row ≥ 40 px below. Center the title on the whole diagram, not one column.
- **Gaps:** ≥ 80 px between columns, ≥ 40 px between stacked boxes. Headers sit flush on bodies.
- **Labels/pills sized to text** (`W ≥ chars × font_size × 0.62 + 24`) or Lucid wraps-then-clips them.
- **Connector labels** 1–2 words, nudged to an open segment (`position` 0.2–0.3 / 0.7–0.8) so they never land on a shape.

## The Brand Restyle + Font Loop (mandatory — never skip)

Even when color is set at creation, **no creator sets the font**. Run this loop on every chart:

1. **Create** the structure with the tool above.
2. **`fetch`** the document (and/or `lucid_search_document` to locate labels) to get every item's `id`.
3. **`lucid_edit_item`** per item to enforce brand tokens from `brand-tokens.md`:
   - `font_family`: `"Montserrat"` for title/header shapes and standalone heading text; `"Lato"` for label/body/edge text. **One font per shape** — a single node block has one font field, so you cannot mix Montserrat-header + Lato-body inside it; pick Montserrat for node/title shapes and reserve Lato for separate label/caption/edge items. `bold: true` on headings.
   - `fill_color`, `line_color`, `text_color` to the semantic role color (do not leave Lucid defaults).
   - **Connectors:** the SVG parser drops `<line>`/`<path>` stroke colors (edges import black), so always re-set every edge's `line_color` here even if the SVG specified it.
4. **`lucid_export_document_as_PNG`** and look at it.
5. **Audit** against the Brand Gate below → fix offenders with more `lucid_edit_item` calls → re-export. A clean tool response is not proof; the PNG is.

## Brand Gate (must all pass before handoff)

- Title/node shapes render in Montserrat, separate label/caption/edge text in Lato — verified in the PNG, not assumed. (One font per shape: don't claim a header/body split inside a single node block.)
- Medium Blue `#000FC4` is the anchor; Ghost White `#F7F7FF` surfaces; cyan `#2DE4E6` only as a sharp accent.
- **Orange `#F26419` is a single restrained CTA/accent — never a whole branch, lane, or >1 node.** (Baseline failure: orange flooded an entire path.)
- Color roles follow the canonical map in `brand-tokens.md`, not ad-hoc guesses.
- Decision diamonds are neutral (white/Ghost-White card + blue border), not orange-flooded.
- Connectors are clean and lane-based; no spaghetti; arrowheads land cleanly.
- Minimal, structured, B2B-strategy feel. No SaaS/emoji/stock/hand-drawn decoration.

## Audit Loop — run it, don't just checklist it (full procedure in `audit-loop.md`)

A chart is not done at first export. **Loop** with a designer's eye until it's genuinely presentable: _"an engineer built this — is it a nice way to present it to a human?"_

1. `lucid_export_document_as_PNG` → study it like a designer (calm or cramped? text breathing? anything overlapping/clipped/spilling?).
2. `fetch` geometry → run the overflow/overlap math. `lucid_fetch_item_image` → **zoom** every dense box and crowded connector-label region.
3. Critique strictly against the scorecard (breathing room, text fit, overlaps, connectors, hierarchy, alignment, brand, polish).
4. Fix the criticals → **RE-EXPORT and re-audit.** ≥2 rounds. Ship only when it passes, or state the exact remaining limitation.

Lucid renders text **larger** than your math predicts and auto-sizes big — set `font_size` down explicitly, leave text ≤ ~70% of box height, and verify on the PNG every round.

### Fit Gate (the non-negotiable checks inside the loop)

From `fetch` geometry + the PNG:

- **No text crosses its box border** — rendered text bottom ≤ box bottom − 10; longest line ≤ box width − 12. (Watch long tokens like `subscription_id` that wrap and add a line.)
- **No truncation** — every label/pill/zone tag shows its full text, not wrapped-and-clipped.
- **No overlaps** — run the rect test on every shape pair; only header/body may touch.
- **Title & subtitle single-line**, clear of zone labels/entities by ≥ 40 px.
- **Connector labels sit on empty canvas**, not on a shape, and are readable.
- Type meets the readability floor (body ≥ 13, header ≥ 15, title ≥ 22).

If any fails, resize/move/reflow and re-export. A clean tool response is not proof — the geometry + PNG are.

## Honesty & Cleanup Gates (verified limits of the @lucid connector)

- **Spec collapses `\n` to spaces and ignores `textColor` on `"type":"text"` shapes.** Author multi-line text, alignment, font, size, and text color in the `lucid_edit_item` pass — not in the spec JSON. (Confirmed: ERD attribute rows rendered as one blob; title/wordmark came out black, until fixed in the edit loop.)
- **Block/pill labels wrap-then-clip when the box is too narrow** ("SELLING & AGREEMENT" → "SELLING &"). Size label boxes to the text (Rule 4) before export.
- **Default connector-label position is the line midpoint** — if that sits over a shape it overlaps. Nudge the label to an open segment (Rule 5).

- **`use_assisted_layout: true` injects an auto-generated white Rectangle container** around the diagram. Prefer `use_assisted_layout: false` for flow/spec diagrams; if you keep it on, find that container via `fetch` and delete it (`lucid_delete_items`) or recolor it to a brand surface.
- **SVG full-canvas background `<rect>` → a labeled "Process" container + giant watermark.** Do **not** put a page-filling background rect in SVG for `convert_svg_to_diagram`; rely on the page background instead. If one slips in, `fetch` → `lucid_delete_items` it.
- **SVG `<line>`/`<path>` stroke colors are dropped on import** (edges arrive black). Always run a post-parse `lucid_edit_item` pass to set each connector's `line_color` (node block edits _do_ work; the org/mind tree creators do **not** — see routing).
- **You cannot reliably move a doc into a folder.** `lucid_update_document(parent=<int>)` rejects the integer folder id (tool bug, confirmed in testing); creators take no parent. Don't promise folder organization.
- **There is no delete-document tool.** `lucid_delete_items` only removes items _inside_ a doc. Test/throwaway documents must be trashed by hand in the Lucid UI — so **prefix test titles `TEST DELETE - …`** and tell the user they must empty trash manually.
- **Title encoding:** use plain ASCII hyphen `-` in titles (em dash `—` renders as `?`); use `>=` not `≥` in shape text.
- **No brand wordmark / footer.** Do **not** add a "MAN Digital" text wordmark, footer, or logo block. `@lucid` has no image-insertion tool so the logo PNG can't be placed either — brand identity comes entirely from the palette, type, and structure, not a footer mark. Leave the canvas clean.
- If `lucid_edit_item`/`convert`/`create` returns any warning, fix it before using the export as proof. Report what you actually shipped, including any default you fell back on.

## Common Mistakes

| Mistake                                        | Fix                                                                                  |
| ---------------------------------------------- | ------------------------------------------------------------------------------------ |
| Stop after `create_*` — "it has brand colors"  | Font is still Lucid default. Run the restyle + font loop.                            |
| Using `create_org_chart` / `create_mind_map`   | Their nodes ignore `lucid_edit_item` — unbrandable. Build the hierarchy as SVG.      |
| Edges import black after SVG convert           | Parser drops `<line>` strokes — re-set every `line_color` via `lucid_edit_item`.     |
| Guessing which color means what                | Use the semantic role map in `brand-tokens.md`.                                      |
| Orange everywhere                              | One restrained accent node max.                                                      |
| `use_assisted_layout: true` leaves a white box | Turn it off or delete the container.                                                 |
| Promising the chart is foldered / cleaned up   | Folders are broken; docs can't be deleted via API. State it.                         |
| Whole-canvas PNG as the only QA                | Zoom risky nodes; verify font + label fit.                                           |
| Text overflows / boxes cramped                 | Size boxes to worst-case wrapped lines (`layout-and-fit.md` Rule 2) before building. |
| Title wraps onto a zone label                  | Reserve a title band, single line, box wide enough not to wrap (Rule 3).             |
| Zone label/pill shows truncated text           | Size the box to the text or shrink font (Rule 4).                                    |
| Setting newlines/`textColor` in the spec JSON  | Spec collapses `\n` and ignores text-shape color — set them in the edit pass.        |
