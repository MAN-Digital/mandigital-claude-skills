# Lucid Workflow & Tool Reference

All tools prefixed `mcp__bab947f5-61a4-4385-bbab-d73ba922fdd4__`. Load schemas via `ToolSearch` `select:<name>` before calling.

## Tools at a glance

| Tool                                      | Purpose                                                                         | Brand notes                                                                                                                                                                               |
| ----------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lucid_convert_svg_to_diagram`            | SVG → editable Lucid diagram. **Primary path for flow/process/architecture.**   | Inline hex + theme classes (`c-blue`/`c-teal`/`c-coral`/`c-purple`/`c-green`/`c-amber`/`c-red`/`c-pink`/`c-gray`) pass through. Pass the SVG verbatim.                                    |
| `lucid_create_diagram_from_specification` | Standard Import JSON → diagram. For BPMN/swimlane/UML-class/named cloud shapes. | **Read `lucid://diagram-specification` first.** Set per-shape `style` hex. No font field → restyle loop for fonts. Set `use_assisted_layout:false` to avoid the white container artifact. |
| `lucid_create_org_chart`                  | Flat nodes `{id,name,managerId,role}` → org chart. Exactly one root.            | ⚠️ **Unbrandable** — `TreeNodeBlock`s ignore `lucid_edit_item` (edits report success, change nothing). Build org charts as SVG instead.                                                   |
| `lucid_create_mind_map`                   | Flat nodes `{id,text,parentId}` → mind map. Exactly one root.                   | ⚠️ Same tree-creator family — treat as unbrandable; build as SVG.                                                                                                                         |
| `lucid_create_sequence_diagram`           | PlantUML sequence markup → diagram.                                             | **Read `lucid://sequence-diagram-specification` first.** Style via PlantUML `skinparam`; finish in restyle loop.                                                                          |
| `fetch`                                   | Read document content → item IDs, text, colors, pages/regions.                  | Use before the restyle loop and to find the assisted-layout container.                                                                                                                    |
| `lucid_search_document`                   | Find which (pageIndex, regionIndex) hold given label text.                      | Cheaper than paging `fetch` on big docs.                                                                                                                                                  |
| `lucid_edit_item`                         | Restyle/move one block or line. **The brand-enforcement workhorse.**            | `font_family`, `fill_color`, `line_color`, `text_color`, `bold`, sizing.                                                                                                                  |
| `lucid_add_block` / `lucid_add_line`      | Add a shape/connector (e.g. an extra node, a legend item).                      | `block_type` e.g. `TextBlock`, `RectangleBlock`, `ShapeDiamondBlock`.                                                                                                                     |
| `lucid_delete_items`                      | Delete items _within_ a doc (e.g. assisted-layout container, stray nodes).      | No whole-document delete exists.                                                                                                                                                          |
| `lucid_export_document_as_PNG`            | Render a page → PNG for QA.                                                     | Mandatory before handoff.                                                                                                                                                                 |
| `lucid_update_document`                   | Rename / retag.                                                                 | `parent` for non-root is **broken** (rejects int folder id). Title only reliable field.                                                                                                   |
| `lucid_create_folder`                     | Make a folder.                                                                  | You can create it, but you can't reliably move docs into it (see above).                                                                                                                  |

## Standard flow (every chart)

1. **Decide tool** by chart type (SKILL.md routing table).
2. **Create** with brand color injected where possible:
   - SVG path → author from `svg-templates.md` with brand hex inline.
   - Spec path → per-shape `style` hex; `use_assisted_layout:false`.
   - org chart / mind map → build as SVG (the `create_org_chart`/`create_mind_map` tools yield unbrandable nodes).
   - sequence → accept Lucid structure + skinparams, finish text in the loop.
3. **`fetch`** the doc → collect item IDs (note the container artifact if assisted layout was on).
4. **Restyle loop:** `lucid_edit_item` per item → `font_family` (Montserrat headings / Lato labels, `bold` headings) + role colors from `brand-tokens.md`.
5. **Export PNG** → audit against the Brand Gate → fix → re-export.
6. **No brand mark:** do NOT add a "MAN Digital" wordmark/footer/logo block. Brand identity is the palette + type + structure only.
7. **Report:** document ID + edit URL, the tools/args used, the actual fonts/colors in the PNG, any fallback, and the manual-cleanup note for test docs.

## Gotchas (confirmed in testing)

- **Org/mind tree creators are unbrandable:** `lucid_create_org_chart` and `lucid_create_mind_map` emit `TreeNodeBlock`s that silently ignore every `lucid_edit_item` (color, font, all return `success:true` and no-op). Build hierarchies/mind maps as SVG, whose ProcessBlocks _are_ editable.
- **Assisted-layout container:** `use_assisted_layout:true` wraps the diagram in an auto white `RectangleBlock`. Turn it off, or `fetch` → identify it → `lucid_delete_items` (or recolor to `#F7F7FF`).
- **SVG full-canvas background `<rect>` → "Process" watermark:** a page-filling `<rect>` becomes a labeled `ProcessBlock` that renders as a giant centered watermark + container box. Omit the background rect (use the page background); if present, `fetch` → `lucid_delete_items` it.
- **SVG connector strokes drop to black:** `convert_svg_to_diagram` discards `<line>`/`<path>` stroke colors. After import, run a `lucid_edit_item` pass setting each edge's `line_color`. (Node fills/text/borders from `<rect>`/`<text>` _do_ survive.)
- **Fonts never auto-set:** no creator writes a font; Standard Import has no font field. Montserrat/Lato come only from the `lucid_edit_item` loop. The canvas may fall back if the font isn't in the org — confirm in the PNG.
- **Folders unreliable / no doc delete:** can't move docs into folders via API; can't delete docs via API. Test docs → title `TEST DELETE - …` and tell the user to trash them manually.
- **Encoding:** ASCII hyphen `-` in titles (em dash → `?`); `>=` not `≥` in shape text.
- **PNG is the proof:** a clean tool response doesn't prove brand compliance; inspect the render, zoom risky/small labels.
- **`lucid_edit_item` endpoint styles use capitalized canonical names** — `"None"`, `"Arrow"`, `"CFN ERD Many Arrow"`, `"CFN ERD One Arrow"`, `"CFN ERD Zero Or More Arrow"`, etc. The lowercase spec values (`"none"`/`"arrow"`/`"many"`) are rejected with a validation error, and the call fails atomically (text/other fields in the same call don't apply either). Use this to switch crow's-foot ERD endpoints to plain arrows (`Arrow`/`None`) for non-technical audiences.
