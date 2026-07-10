# Production Quality Floor

Use this before planning and during audit. A graphic can be perfectly aligned and still be a bad MAN Digital design. This file defines the minimum craft level.

## Quality Brief

Before building, write a short internal brief:

1. **Visual job**: what the graphic must explain in one sentence.
2. **Audience takeaway**: what the viewer should understand in three seconds.
3. **Main visual anchor**: screenshot, flow, field system, architecture map, matrix, flywheel, stack, or annotated object.
4. **Component lineage**: which Playground/template/card/icon/pill/connector/logo/depth system shapes the output.
5. **Content specificity**: what makes each stage, card, department, field, or category different.
6. **Differentiation system**: tint, lane, chip, rail, icon medallion, grouped panel, border, connector lane, or section header.
7. **Brand presence**: approved MAN Digital logo asset and brand color hierarchy.

If any line is weak, improve the concept before drawing.

## Minimum Quality Gates

Every finished graphic needs:

- one clear visual anchor, not only a row of boxes;
- a specific narrative or operating model, not generic labels;
- at least two hierarchy levels: title/support plus main visual, or main visual plus annotation system;
- traceable MAN Digital/Pencil library DNA through components, spacing, icon treatment, card style, connector style, logo treatment, or visual-depth system;
- real brand presence with an approved logo asset unless the output is explicitly internal/no-logo;
- stage/category-specific content when showing a framework, sequence, process, department split, or audit model;
- editable Pencil source: notes, labels, cards, connectors, callouts, and text must remain native nodes;
- measured padding and layout hierarchy for text containers;
- selected decoration/icon style with traceable lineage when decoration or icons are used;
- mobile/static-image readability for key labels.

## Hard Fail Patterns

Reject these even when `snapshot_layout(problemsOnly)` says there are no issues:

- A top-level title plus identical cards is the whole graphic.
- Cards repeat the same placeholder phrases under different headings.
- A framework or process has no stage-specific role, input, gate, risk, metric, or outcome.
- A graphic could be made by any generic diagram tool and has no MAN Digital library DNA.
- There is no approved logo asset or deliberate brand mark placement.
- The design is a flat image pasted into Pencil, so the user cannot edit notes, labels, text, cards, connectors, or diagram parts.
- Text nodes are absolutely placed over rectangles instead of being children of padded layout containers.
- `search_all_unique_properties` shows no `padding` or `gap` in a card/pill-heavy graphic, unless the source component has a documented absolute layout and padding was measured manually. If that helper is not available in the active Pencil MCP, use `batch_get` and `snapshot_layout(maxDepth: 3 or 4)` to inspect the same parent/card/pill properties.
- The design uses only white fill, blue strokes, icons, and arrows without visual depth, semantic differentiation, or a stronger focal object.
- The graphic has a title but no subtitle, context label, proof object, or explanatory anchor when the concept needs framing.
- The same generic pale circle/ellipse decoration is repeated across graphics without a registered source or concept role.
- Icons are a mix of heavy filled icons and thin line icons inside the same repeated card/pill system.

## Figma Reference Pattern: `1091:3034`

Use `figma-patterns.md` as the source when adapting the Figma "Prospecting Agent vs Outbound-04" graphic into Pencil.

Important quality lessons:

- a tall inline explainer can support more readable text than a cramped 1536 x 1024 blog image;
- repeated icon cards must share one padding rhythm, icon slot, fill, stroke, and corner radius;
- positive rules and negative rules need semantic fill differences, not identical cards;
- outcome summaries can live in a bottom band without becoming a slide footer;
- thin Streamline-style icons look more polished than bold generic icons for this family;
- decoration should be selected from the registry or Figma source, not invented from scratch.

## Regression Case: `ddZDg`

`ddZDg` was a 1536 x 1024 "Deal Stage Audit Framework" graphic that passed basic layout checks but failed design quality.

Observed failures:

- no formal reusable components in the active file;
- no `padding` or `gap` properties found by `search_all_unique_properties`, or by `batch_get`/`snapshot_layout` fallback when that helper is unavailable;
- title plus four nearly identical vertical cards was the entire design;
- stage cards repeated `Buyer Proof`, `CRM Data`, and `Manager Gate` under every stage;
- no stage-specific audit logic, owner, risk, metric, or decision gate;
- no clear visual differentiation between stages beyond headings;
- no approved MAN Digital logo asset;
- minimal blue outline styling with weak visual depth and no strong anchor.

Required correction:

- choose a library-backed framework, flow, or architecture component before building;
- make each deal stage semantically different, such as entry signal, evidence needed, owner, risk, gate, or next action;
- use a real card/pill hierarchy with padding and gap, not floating text over rectangles;
- add restrained category coding or stage rail/chip/icon cues;
- add an approved logo treatment and one mapped visual-depth system;
- re-audit with the production quality floor, not only layout problems.

## Stage And Framework Content Rule

For process, lifecycle, audit, stage, or framework graphics:

- Each stage card needs unique content. Repetition is allowed only when the point is to compare the same audit criteria across stages, and then the repeated criteria must be structured as a matrix, checklist, or table, not four standalone repeated cards.
- Prefer one large visual structure over many small repeated labels.
- If the same three items apply to every stage, show those items as row labels or shared criteria, then encode stage-specific values, status, or emphasis.
- A viewer should understand the difference between stages without reading every small label.

## Audit Questions

Before handoff, answer internally:

- Would this still look credible if the user removed the title?
- Does each card or stage say something only that card or stage should say?
- Is there visible MAN Digital library DNA beyond color?
- Are text containers real padded containers, not text floating over rectangles?
- Can the user edit the important notes, labels, text, cards, connectors, and diagram parts directly in Pencil?
- Is there a clear reason for every icon, connector, label, and accent?
- Would this feel too generic if shown next to the Playground references?

If any answer is weak, revise before presenting the graphic.
