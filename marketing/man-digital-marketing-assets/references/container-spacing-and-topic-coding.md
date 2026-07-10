# Container Spacing And Topic Coding

Use this before placing text inside pills, cards, frames, boxes, badges, callouts, table cells, or label bars, and before designing any graphic with multiple categories or topics.

## Container Padding Rules

Text should not merely fit. It needs visible breathing room at the final export size and in close-up audit.

Minimum internal padding:

| Container | Horizontal padding | Vertical padding | Notes |
| --- | ---: | ---: | --- |
| Pill/chip/badge | max(12 px, 0.75 x font size) | max(6 px, 0.35 x font size) | One short line only unless the component is intentionally a large label card. |
| Small label bar/pin | 12-18 px | 8-12 px | Keep labels to 1-3 words. |
| Callout box | 20-28 px | 16-24 px | Add more if there is heading plus body copy. |
| Diagram/card box | 24-40 px | 20-32 px | Larger cards need larger padding; do not center tiny text in huge empty cards. |
| Table/field cell | 16-24 px | 12-18 px | Use row height that survives mobile scaling. |
| Large frame/panel | 40-64 px | 32-56 px | Respect the source template rhythm if it is stronger. |

Hard rules:

- A text node inside a pill, badge, chip, card, frame, table cell, or callout must be measured against the actual container bounds.
- Single-line pill/chip/badge text must be vertically centered by geometry, not just visually close. Compare the rendered text centerline to the pill centerline and tolerate at most 2 px for layout-native text, or 4 px only when documented as optical compensation for the font. If the text sits high or low inside the rounded fill, the pill fails even when the text technically fits.
- Text that belongs to a container should be a child of a layout frame with `padding` and `gap` whenever possible. Do not build cards as a rectangle plus separate free-floating text siblings unless a copied source component intentionally uses absolute positioning and the padding is manually verified.
- A card/pill-heavy graphic where `search_all_unique_properties` returns no `padding` or `gap` is a hard warning. If that helper is unavailable, inspect the same construction with `batch_get` and `snapshot_layout(maxDepth: 3 or 4)`. If the construction is free-floating text over rectangles, rebuild with layout frames or a proper copied component.
- Left and right padding should match within 2 px unless the source component has an intentional icon slot, left rail, or optical compensation.
- Top and bottom padding should match within 2 px for single-line labels. For multi-line cards, the content stack can be top-aligned, but the stack still needs reserved bottom breathing room.
- Icon-plus-label pills need three measurements: icon left padding, icon-to-text gap, and text right padding.
- If a pill label wraps, it is usually not a pill anymore. Convert it to a larger badge/card or shorten the copy.
- One-word or short step/card labels must remain on one line unless the design brief explicitly calls for stacked typography. Regression `cV3XM` failed because a one-word label (`Measurement`) broke/wrapped inside a process step. For labels such as `Problem`, `Prototype`, `Measurement`, `Conversion Rate`, or `Scale Decision`, reserve enough width and height before export; do not accept accidental wrapping, clipped letters, or a title that pushes into the body copy.
- If copy is required and the box cannot hold the minimum padding, enlarge the box, reduce copy, raise the font size and simplify, or choose a different component.
- Do not approve a container because `snapshot_layout(problemsOnly)` is clean. It can still be visually cramped.

## Build-Time Method

Before creating or editing containers:

1. Decide the text role: key label, supporting label, metadata, callout, field, or category marker.
2. Set the font size from `readability-depth-gate.md`.
3. Compute the minimum padding from the table above.
4. Size the container from the text width/height plus padding, or shorten the copy until it fits.
5. For pills/chips/badges, prefer a layout frame with `alignItems: "center"` and `justifyContent: "center"` for the label group. If the runtime is not Pencil-native, calculate text ascent/descent and place the label from the text bounding-box center, not from a guessed y coordinate.
6. For repeated cards or pills, define one component rhythm and reuse it. Do not let each item have a different padding system.
7. Use rows/columns of padded frames for repeated criteria. Do not place three independent text nodes over each card and call that a card component.

## Audit Method

For every risky pill, card, frame, box, badge, callout, table cell, and label bar:

1. Use `batch_get` or `snapshot_layout` on the container and its text children.
2. Measure text left/right/top/bottom against the container.
3. Measure the label centerline against the pill/chip/badge centerline. A label that appears low in the fill or clipped by the rounded shape fails the audit.
4. Check the rendered screenshot, not only the geometry. Rounded pills can feel tighter than their bounds.
5. For every production graphic with pills/chips/badges, inspect at least one close-up crop of the most crowded pill and one representative repeated pill. Full-canvas screenshots are not enough.
6. Check the mobile/static-image preview when labels are key to understanding the graphic.
7. Fix by changing the component size or copy first. Do not solve padding by shrinking key text below the readability plan.

## Topic Differentiation Rule

When a graphic includes two or more distinct topics, departments, audiences, stages, systems, statuses, or ownership areas, the viewer should understand that they are different groups before reading every word.

Use restrained MAN Digital differentiation:

- Background tints: `#FFFFFF`, `#F7F7FF`, `#ECF1FB`, `#EEF0FB`, `#E4E6F9`, and very light cyan tint.
- Brand accents: Medium Blue `#000FC4` for the primary category, cyan `#2DE4E6` for signal/highlight, orange `#F26419` only as a restrained accent.
- Pillar accents sparingly when content semantics justify them: green for revenue/growth, orange/amber for enablement or employee experience, red/yellow only for risk, warning, or compliance.
- Structural cues: section headers, lanes, left rails, top bars, icon medallions, border colors, category chips, grouped background panels, or separate connector lanes.
- Visibility rule: each structural cue must contrast with its immediate parent surface. A top bar, left rail, chip, pill, divider, icon medallion, connector mark, or category cue with the same fill as the card/lane/background is invisible and fails the topic-coding audit.

Do not use random rainbow palettes. Keep most surfaces light and use color as a semantic cue, not decoration.

## Common Patterns

- Sales / Marketing / Customer Success: use three grouped lanes or cards with distinct chips/rails/icons. Example: Sales as blue, Marketing as cyan/light-blue, Customer Success as green or blue-300 depending on topic. Use orange only if one category is explicitly a warning or enablement motion.
- Input / Process / Output: use subtle surface differences plus directional connectors. Inputs can be light blue, process can use white cards with blue rails, outputs can use a stronger blue or cyan highlight.
- Risk / Fix / Result: use restrained warning accent for risk, blue for fix, cyan/green for result.
- Before / After: separate with two background panels, labels, and a clear connector or divider. Do not make both halves identical unless the point is sameness.

## Cue Contrast Check

When auditing topic coding, inspect cue fills against parent fills:

- Accent/top bar fill versus card fill.
- Pill/chip fill versus card fill and text fill.
- Left rail/divider fill versus panel fill.
- Icon medallion fill versus card fill and icon fill.
- Connector mark/arrowhead fill versus canvas and nearby shapes.

If a cue disappears because it matches its background, replace it with an approved brand or semantic accent instead of leaving it as a technically present but visually absent node.
- Departments or ownership: use lanes or swimlanes, not only repeated neutral cards.

## Bluntness Failure

A graphic fails the topic-coding gate when:

- Distinct departments, topics, stages, or statuses all use the same box style with no labels, lane, color, icon, border, or grouping cue.
- The only difference between categories is long body text.
- Process or framework stage cards repeat the same generic labels under each stage instead of showing stage-specific roles, inputs, gates, risks, metrics, or outcomes.
- The graphic feels minimal but inert: one flat section of identical rectangles with no visual hierarchy or semantic cue.
- Category colors exist but are arbitrary, too saturated, or inconsistent with MAN Digital brand tokens.
- The color coding competes with the main idea, connectors, or text readability.

Minimalism is still required. The goal is not more decoration; it is faster comprehension.
