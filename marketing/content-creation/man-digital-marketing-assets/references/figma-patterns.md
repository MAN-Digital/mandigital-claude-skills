# Figma-Derived Pencil Patterns

Use this file when the user provides a MAN Digital Figma reference or when a blog graphic needs a more mature editorial/infographic system than a plain row of cards.

## Source

Figma reference inspected on 2026-05-28:

- File: `Marketing--Copy-`
- URL: `https://www.figma.com/design/vnYBGA0YlYEG10B4Ycbf8u/Marketing--Copy-?node-id=1091-3034&m=dev`
- Node: `1091:3034`
- Frame name: `Prospecting Agent vs Outbound-04`
- Natural frame size: `1190 x 1684`

## What The Reference Teaches

This is not just a slide. It is a tall article/social explainer with:

- a thin top rule and a compact footer/brand row;
- a large Montserrat title and separate Lato support copy;
- three white bordered columns, each with a clear role;
- repeated icon-plus-text cards with real padding and gap;
- a middle rule/guidance column with soft gradient callout panels;
- thin blue connector marks between columns;
- a bottom "why this matters" outcome band with four icon medallion outcomes;
- subtle low-contrast background depth, not random decorative circles.

Use this family when the prompt asks for:

- outside vs inside system comparisons;
- what should stay out of HubSpot vs what belongs in HubSpot;
- "sync rules", governance, rules of engagement, or do/don't logic;
- a tall inline article explainer where 1536 x 1024 would force tiny labels;
- a Lucidchart-like process graphic with readable blocks and a strong rules column.

Do not use this family for a simple OG/hero image unless the user asks for a tall explainer or the graphic is embedded inline in the article.

## Pencil Translation

Rebuild as editable Pencil nodes. Do not paste the Figma screenshot into Pencil.

- Top-level frame: use the requested output size. For this exact family, `1190 x 1684` is approved.
- Background: white or Ghost White. Keep visual depth subtle.
- Column frame: white fill, `#C8CCF2` stroke, about `1.39 px`, `4 px` corner radius.
- Column padding: `24 px` top/bottom, `17-24 px` side depending on width.
- Column gap between item cards: `24 px`.
- Item card: light blue fill `#ECF1FB`, stroke `#C8CCF2`, `4 px` corner radius, `24 x 16 px` padding, horizontal layout, `16 px` icon/text gap.
- Item card icon slot: 32 x 32, Medium Blue `#000FC4` or semantic orange `#F26419` only when the item is a warning/negative action.
- Item card heading: Montserrat SemiBold, about `20 px`, line height `1.2`, `#222222`.
- Item card body: Lato Regular, about `18 px`, line height `1.4`, `#222222`. The Figma reference uses `-0.18 px` letter spacing; preserve only when matching this Figma family, otherwise default to the local component's type rhythm.
- Main title: Montserrat SemiBold, about `48 px`, line height `1.2`, `#222222`.
- Support copy: Lato Regular, about `22 px`, line height `1.4`, `#222222` at roughly 80% opacity.
- Footer metadata: Lato Regular `16 px`, line height `1.4`; page/sequence number in `#000FC4`, label in `#222222`.
- Outcome label: Montserrat SemiBold `20 px`; outcome body Lato Regular around `14.8 px`, line height `1.3`, `#434343`.

## Canonical Playground Reference

The canonical Pencil version of this Figma-derived pattern already lives in the Playground library:

- File: `/Users/romeoman/Documents/Marketing/Design/Pencil/Playground.pen`
- Node: `LZkoW`
- Frame name: `Prospecting Agent vs Outbound-04`
- Component reference: `components/LZkoW.md`

Use `LZkoW` as the source of truth for this family. Inspect it live with Pencil `batch_get` before adapting it, then copy/recreate the relevant anatomy in the prompt-specific output `.pen`. Do not create a separate permanent reference `.pen` for this pattern unless the user explicitly asks for a new variant that does not already exist in Playground.

The temporary `knF6I` frame and `MAN Digital Figma Prospecting Agent Sync Pattern - 1091-3034.pen` file were proof artifacts from a test run, not canonical library sources. They may be kept as historical test evidence or deleted, but future production work should use `LZkoW` and the Playground registry.

Learnings from the test run:

- Passing close-up crops is not enough. The full-frame screenshot initially exposed section-fit problems that child screenshots did not show.
- Outcome bands and footer-like impact sections must sit in the vertical flow. They should not overlap the lower column/card system, crowd it, or create a large dead gap below the main visual.
- Pencil may report unsupported icon names in `batch_design` output. Those warnings must be fixed before the icon system can count as production-ready.
- If a new file path has not been created and opened, Pencil MCP can write into the active editor. Confirm the active path before deleting seed frames or building the reference.

## Color System From Reference

Use these as approved semantic accents, not a random palette:

| Token | Value | Use |
| --- | --- | --- |
| Medium Blue | `#000FC4` | Main title accent, connector lines, primary icons. |
| Primary 400 | `#5963D9` | Softer blue/purple topic cue, low-contrast category tint. |
| Orange | `#F26419` | Warning, "do not", risk, or negative path. |
| Dark Charcoal | `#222222` | Primary body/text and most labels. |
| Charcoal | `#434343` | Secondary captions/outcome bodies. |
| Secondary Purple | `#C8CCF2` | Strokes, borders, dividers. |
| White | `#FFFFFF` | Card and column surfaces. |

When a prompt compares multiple departments, systems, topics, or statuses, apply the colors as semantic cues:

- blue / primary 400 for preferred, inside-system, approved, or active path;
- orange for "do not", risk, overload, negative path, or warning;
- charcoal for neutral or supporting labels;
- purple border/tint for structural grouping.

## Card And Panel Patterns

### Information Card

Use for a reusable icon-plus-text card.

Pencil equivalent:

- frame, horizontal layout;
- fill `#ECF1FB`;
- stroke `#C8CCF2`, thickness about `1.39`;
- corner radius `4`;
- padding `[16, 24]`;
- gap `16`;
- icon 32 x 32;
- text stack vertical with `6 px` gap.

Reject cards where text floats over a rectangle or where each repeated card has a different padding rhythm.

### Rules Panel

Use for a middle guidance/rule panel.

Positive/approved rules:

- fill: subtle vertical gradient from `rgba(0,15,196,0.12)` to transparent, or a pale blue/purple surface;
- heading: Lato Bold `20 px`, `#222222`;
- bullets: small `#000FC4` 8 px dots and Lato Regular `18 px` body.

Negative/do-not rules:

- fill: vertical gradient from `rgba(242,100,25,0.15)` to transparent;
- heading: Lato Bold `20 px`, `#CB4F0D` or `#F26419`;
- bullets: 8 px orange x/mark plus Lato Regular `18 px` body.

Do not put a generic "article context" or rationale block here. This panel is for the viewer-facing rule itself.

### Outcome Band

Use for "why this matters", benefits, or final impact.

- horizontal band with top/bottom `#C8CCF2` rules;
- four outcome cells, each centered;
- 72 px pale icon medallion with 32 px icon;
- short title plus one short support sentence;
- enough gap so the band does not feel like a slide footer.

## Connector Pattern

Use minimal connector marks between columns:

- stroke width `1.5 px`;
- stroke `#000FC4`;
- horizontal centerline aligned to column header or card port;
- small arrow/diamond/chevron marker only when direction must be explicit;
- no spaghetti routes, no diagonal web, no connector crossing text.

For process diagrams with longer paths, follow `flow-connectors.md` and `zoom-audit.md` instead of stretching this small connector mark.

## Decoration Rule

The Figma node uses a large subtle background vector plane. This is a content-supporting depth element, not permission to invent random circles.

Before adding background decoration:

1. Choose from the mapped decoration registry in `component-index.md` and `readability-depth-gate.md`.
2. Use the least visible element that improves balance or depth.
3. Keep it behind content.
4. Do not repeat the same pale ellipse/circle in every graphic.
5. Reject any decorative node that cannot be traced to the Playground, Gemini carousel registry, design-system assets, or a user-provided Figma source.

Regression note: `egabQ` was a made-up pale decor ellipse in a blog graphic. Do not keep creating that same unregistered circle motif. Replace it with a mapped depth source such as `VsypW`, `xOLUX`, `p4Dtt`, `GogdW`, a dot-grid, a subtle plane, or no decoration.

## Icon Style Rule

The Figma node uses thin Streamline-style line icons. For Pencil:

- Prefer existing Streamline-style icons already embedded in Playground components.
- Use 32 px icons for item cards and medallions.
- Keep strokes visually thin and clean. Avoid bold filled icon blobs.
- Use Medium Blue for standard/positive icons and Orange only for warning/negative categories.
- If the exact icon node is unavailable, use a closest semantic icon from existing Playground components before creating a new icon primitive.

When user names icon-example nodes such as `GoNGR`, `id7JG`, `g0Gr3`, `OY5Hk`, or `vvog0`, treat them as style references for thin outline icons, not as mandatory semantic choices for every prompt.

## Audit Additions

For this family, the audit must check:

- all columns share top edge, width rhythm, and stroke/corner radius;
- repeated item cards share padding, icon slot, text stack gap, and fill/stroke;
- middle positive and negative panels use distinct semantic fills;
- connector marks sit exactly on the intended column/header rail;
- outcome band is not mistaken for a carousel footer, does not overlap the column system, and does not leave a large dead vertical gap;
- the MAN Digital logo is an approved asset or built from approved brand mark anatomy, not typed footer text;
- decoration is mapped and varied, not the same unregistered circle motif.
