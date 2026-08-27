# Zoom Audit

Use this before approving any dense Pencil graphic. A full-canvas screenshot is not enough for text-fit, callout, connector, arrow, or small-component quality.

## When Required

Run a zoom audit when the graphic contains any of these:

- Flowcharts, process steps, arrows, connector lines, callouts, or labels.
- Cards, pills, badges, or table cells with more than one text layer.
- Font sizes below 24 px on a 1536 px or wider canvas.
- Any node the user names as problematic.

## Required Passes

1. Screenshot the full output node.
2. Run `snapshot_layout` on the output node with `problemsOnly: true`.
3. Run `snapshot_layout` on the output node with `maxDepth: 3` or `4` to inspect text/card anatomy.
4. Use `batch_get` on all risky cards, pills, callouts, connectors, and arrow groups. Include their child text nodes.
5. Screenshot the risky child nodes directly with `get_screenshot`, not only the full canvas.
6. Export the final node and inspect a 375 px wide preview for mobile readability.
7. For every user-named or audit-named problem node, inspect the node, parent, and sibling group with `batch_get` and `snapshot_layout`. Determine the intended alignment rail before moving it.
8. Search the final output subtree for temporary/probe names: `TEST|TMP|temporary|scratch|debug|probe`. Any match inside the exported frame is a failure.

## Text Collision Rules

- For every component with multiple text children, compare the child node sizes, `x/y`, widths, font sizes, and line-height assumptions.
- For every important heading/support pair, use `snapshot_layout` rendered rectangles and enforce: `heading.y + heading.height + 16 <= support.y`.
- For support copy followed by a diagram, table, screenshot, or card grid, enforce: `support.y + support.height + 24 <= visual.y`.
- For a top header/support stack followed by a main visual zone, audit sibling rectangles rather than trusting component-local checks. Compute the rendered bottom of the last header/support text and compare it to the top of all first visual-zone siblings: panel backgrounds, lane labels, cards, screenshots, connectors, and visual-depth shapes that can merge with the header. Require at least 32 px clear gap.
- Check these pairs specifically when present: eyebrow/title, title/support, support/visual, card heading/card caption, pill label/icon, footer note/logo.
- A title that can wrap must not share vertical space with a note, caption, badge, icon, connector, or next label.
- Avoid `fixed-width-height` for text unless clipping is intentional. Prefer `fixed-width` and enough parent height.
- Short labels may use `auto`; longer labels need enough width to stay on one line or a layout that reserves two-line height.
- If a heading may wrap, reserve at least `fontSize * lineHeight * lineCount + 10px` before the next text layer.
- Treat near-touching text as a failure. The fix is to increase width, increase height, reduce copy, lower font size within the prompt minimum, or change layout.

## Heading / Support Regression

If a selected or named pair looks like `Content heading` and `Content support`, audit the pair before anything else. The failure mode is easy to measure:

- Read both nodes with `batch_get`.
- Read their rendered rectangles with `snapshot_layout`.
- Compute heading bottom plus gap.
- If the support starts above that value, the graphic fails even if the full screenshot looks mostly acceptable.
- Fix by using a vertical text-stack frame, widening the heading, reducing copy, or moving the support and visual zone down.

## Header / Visual Zone Regression

If a named node is a header frame, like `g2Emw`, inspect more than the header's internal children. Read the header, the parent frame, and the first visual-zone siblings below it with `batch_get` and `snapshot_layout(maxDepth: 3 or 4)`.

- Measure absolute bottom of the final header/support text: `header.y + child.y + child.height`.
- Measure the earliest top edge of main visual-zone siblings: panel backgrounds, lane labels, cards, screenshots, callouts, connectors, and meaningful decorative planes.
- Enforce `lastHeaderTextBottom + 32 <= earliestVisualTop`.
- If a panel intentionally starts high as a soft background, the visible lane labels, cards, connectors, and high-contrast visual elements must still start below the header/support stack with a clear gap. If the background reads as a competing visual zone, it also counts.
- If the gap fails, move the whole visual system, not just one label. Preserve card, connector, lane-label, and panel rails together.
- Take a close crop of the header-to-visual boundary whenever the measured gap is under 80 px or the user names a header/visual overlap. Full-canvas screenshots are too forgiving here.

Regression case: `g2Emw` had header/support bottom at y=327, first panels at y=304, and lane labels at y=330. `snapshot_layout(problemsOnly)` returned no problems, but the support text visually collided with the visual system. This must be a hard fail in future audits.

## Named Node Alignment Rules

When the user names a node, or when an audit identifies a suspicious node, do not judge it from the full screenshot alone.

- Read the node with `batch_get`.
- Read the parent with `snapshot_layout(maxDepth: 2 or 3)`.
- Identify nearby rails: parent safe-area edge, panel edge, card grid edge, logo rail, label/pin rail, or connector centerline.
- Compare the node's left edge, right edge, horizontal center, top edge, and vertical center against the relevant rail. For hard alignment, tolerate at most 2 px. For optical compensation, tolerate at most 4 px and document why.
- Check the node with its sibling set, not in isolation. A top context chip, footer logo, callout pin, or label bar should share a visible alignment system.
- Fix the parent/sibling alignment system when multiple nodes drift. Do not make one-off nudges that leave the next related node off-grid.
- If no coherent rail exists, rebuild that part as a small layout group or grid before final export.

Regression case: a top context label like `nSf7c` can look acceptable at full size while its x-position floats between the title/panel/logo rails. The audit must compare it against the parent frame, panel edge, and logo/context rail and fail it if it is not intentionally aligned.

## Connector And Arrow Close-Up Rules

- For routed flowcharts, inspect the actual route nodes, not only the visible screenshot. Confirm whether the export is driven by production route paths or by many small connector fragments.
- Screenshot connector-heavy child regions separately. Do not rely on a whole-canvas screenshot to judge line quality.
- For every user-named connector, inspect the path geometry and then inspect the rendered crop. Node data can look plausible while the export renders as broken fragments.
- If any connector has an arrowhead, tip, endpoint cap, or directional marker, create a close-up crop/export of that tip region. This is mandatory, not optional.
- The connector-tip crop must show the tip point, arrowhead base, route body endpoint, final-segment tangent, and nearby background/card edge. If those details are not visible, zoom in further.
- A route line visibly continuing under a triangle arrowhead fails. The route must stop at the arrowhead base, be hidden behind the arrowhead, or be built as one integrated arrow shape.
- Check that arrows and lines start and end at intended ports, not random card interiors.
- Check each connector/card intersection at close zoom. The line must stop flush at the card, hub, screenshot, logo, or panel edge; a rounded cap bleeding into the fill is a failure.
- Check that connectors do not pass under text, icons, field labels, badges, or values.
- Check that arrowheads have space around them and do not visually merge with strokes, cards, or labels.
- Check arrowhead centerline alignment against the connector segment, not just whether the arrow points in the right direction.
- Check every place a curve approaches a straight rail, panel border, card edge, or connector trunk. The curve must either keep a clean visible gap or form a deliberate junction. Near-tangent collisions, dark seams, doubled strokes, hooked caps, and partial overlaps fail.
- Check for fake-gap routing: a single connector path with disconnected `M`/`m` subpaths can render as unrelated curve stubs. If a connector is meant to cross or pass near a panel border, the close-up must show a continuous route, a deliberate port/notch, or separately named audited segments. Broken fragments fail even when `snapshot_layout` reports no problems.
- Check every elbow and junction at zoom. Segment gaps, tiny offsets, uneven overlaps, or icon-font arrow optical drift are failures.
- Check for route-artifact failures such as hollow tee dots, stacked bars showing through, inconsistent thickness, or old disabled fragments accidentally remaining visible.
- For smooth connector routes, inspect the route node data: open stroked paths must have transparent fill, round joins, flush caps at surface endpoints, and Bezier or rounded bends. In Pencil, use `stroke.cap: "none"` where the route touches a card/hub/screenshot surface. Arrowheads should be separate closed/filled paths or verified visible copied icons.
- Reject any smooth route that exports as filled wedges, triangles between segments, blobs at joins, or decorative arcs that do not clarify the flow.
- Check the outliner around the connector region. Random arcs, probe shapes, disabled experiments, and temporary nodes are audit failures even when the screenshot looks fine.
- If zoomed screenshots reveal line clutter, simplify routing before exporting.

## Regression Case

The autonomous signal-routing test exposed the failure mode: output-card nodes such as `NzeXF` and `TNll6` had title text in a narrow box and a secondary label placed too close below it. A whole-canvas screenshot was not strict enough. The audit must inspect those card nodes directly and verify title/caption separation from node anatomy.
