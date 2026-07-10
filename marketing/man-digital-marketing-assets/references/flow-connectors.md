# Flow Connectors

Use this before building any flowchart, process diagram, lifecycle, signal-routing map, funnel, or card-to-card sequence. Connector quality is production-critical, not decoration.

## Connector Principles

- Connectors must make the process feel intentional, calm, and readable.
- Use a small number of planned routes. Do not draw ad hoc lines from every object to every other object.
- Prefer smooth routing: single clean horizontal lines for simple flows; rounded orthogonal or Bezier-routed bends for branch/merge flows. Hard square elbows are allowed only when copied from a high-quality source component and verified at zoom.
- Lines should connect from consistent ports on cards: center-right to center-left for left-to-right flows, bottom-center to top-center for vertical flows.
- Connector endpoints should land near the card edge or icon anchor, not inside text.
- Cyan `#2DE4E6` is the preferred active connector color. Use `#C8CCF2` for secondary/passive connectors.
- Connector thickness should usually be 3-4 px at 1536/1920 widths and 2-3 px at 1200 widths.
- Smooth connector routes should use rounded joins or Bezier bends. Use `stroke.cap: "none"` for any open route endpoint that touches a card, panel, hub, screenshot, or logo surface; round caps are only acceptable for free-floating endpoint marks. The rendered curve must not show kinks, flat spots, hollow dots, wedge artifacts, or cap intrusion into adjacent surfaces.
- Smooth curves must not graze or ride along vertical/horizontal rails, panel borders, card edges, or other connector trunks. A near-tangent overlap creates a dark seam, doubled stroke, hooked cap, or accidental merge and must be rerouted.
- Do not fake rail clearance by splitting one logical connector into disconnected subpaths inside a single path node. A geometry such as `M... m...` can export as two floating curve fragments, which is worse than the original rail collision. Use one continuous route that crosses or joins intentionally, or build separate named connector segments with a visible port/junction and close-up proof.
- Dots, arrowheads, or endpoint caps are optional. Use them only when they clarify direction.
- Direction markers must not create visual noise. If arrowheads are used, keep them integrated with the route geometry and aligned to the line center.
- Arrowheads must align to the connector centerline. If a 4 px line is at `y`, a 20 px arrowhead should usually sit around `y - 8` so both centers match.
- Arrowhead tips are measured endpoints, not decoration. The tip must land on the intended port, lane endpoint, or target gutter, and the arrowhead must point along the final segment tangent. For curved or loopback routes, use the tangent at the route end, not the overall direction of the loop.
- Arrowhead scale must match the connector gap and stroke. For a 4 px connector in a narrow card gap, a 16-18 px arrowhead is usually enough; 24-26 px arrowheads often become blunt wedges or standalone visual debris.
- If an arrowhead sits between cards, stop the visible connector segment at the arrowhead base. Do not run a long connector line under the arrowhead unless the overlap is intentional, hidden behind surfaces, and verified in a close-up export.
- Prefer simple path or polygon arrowheads when icon-font arrows look optically off-center. If icon-font arrows are used, verify and nudge them by close-up screenshot.
- In existing Pencil frames, direct `I()` inserts for new path/polygon/icon arrowheads can fail to render in export even when `batch_get` sees them. When adding visible arrowheads to an existing rendered component, copy a known visible icon with `C()` and then update `iconFontName`, `x`, `y`, `width`, `height`, and `fill`. Verify the copied arrowhead in an exported close-up.

## Mandatory Arrow-Tip Zoom Gate

Any connector with a tip, arrowhead, endpoint cap, or directional marker must get a close-up/zoom audit before handoff.

- Export or screenshot the smallest useful region around each connector tip. If several tips use identical geometry in the same repeated flow, audit one representative tip plus any tip on a curve, loopback, branch, or different background.
- Full-canvas screenshots do not count as arrow-tip proof. The crop must be close enough to see the tip, arrowhead base, stroke end, final-segment tangent, and nearby grid/card/background.
- The route body must stop at the arrowhead base, sit behind the arrowhead in a way that is invisible, or be integrated into a single clean arrow shape. A line visibly running under a triangle, as in regression `DyGGb`, is a failure.
- The tip must not read as a pasted shape. It should feel like the end of the connector: tangent-matched, centered, proportional, and clean at export scale.
- If the close-up exposes a bad tip, fix the connector geometry and re-export the close-up. Do not pass the graphic because the full view looks acceptable.

## Production Rules

- Lay out cards first on a grid, then route connectors through reserved lanes.
- Compute connector ports before drawing: card centerlines, hub centerline, branch endpoints, and arrowhead tips. Do not eyeball these values from the screenshot.
- Write down or infer the port math from node geometry: source/card edge, route lane, arrowhead base/tip, final-segment tangent, and target edge. A connector that looks "close" but is not mathematically aligned is not production-ready.
- For loopback or curved return connectors, audit the arrowhead against the final curve direction with a close-up crop. A route that arrives vertically needs an up/down arrowhead; a route that arrives horizontally needs a left/right arrowhead. Sideways tips on vertical curve endpoints fail.
- For hub or bus diagrams, make one intentional centerline through the main hub. The source merge point, hub input, hub output, and downstream tee should either share the same centerline or have a visibly intentional elbow.
- For any route that approaches a rail, border, card edge, or connector trunk, choose one of two clean treatments: keep a clear visible gap, or make an intentional junction. Do not let the curve drift into the rail or partially overlap it.
- Default separation: keep at least one full connector stroke width from unrelated rails/borders, and preferably 2-3x stroke width at close zoom. If the route is meant to join a trunk, trim both paths to a clean tee/Y junction or build the join as one integrated path so no doubled stroke or hook appears.
- If you need a visual gap around a panel border, create a deliberate construction: a true port, a masked/notched border, or two separate named segments whose endpoints are aligned and audited. Do not hide the problem by putting multiple disconnected `M`/`m` subpaths inside one route node.
- Reserve connector gutters between cards. Default minimum: 24 px between a connector and any text block; 16 px absolute minimum for small diagrams.
- Use one routing mode per graphic: straight process line, orthogonal elbows, hub-and-spoke, or layered swimlane. Do not mix modes unless the source component already does so cleanly.
- For process steps, prefer a single left-to-right or top-to-bottom line touching each step in order.
- For hub-and-spoke diagrams, keep spokes symmetric and short. If there are more than 4 inputs, group inputs first rather than drawing a web.
- Avoid diagonal spaghetti lines. Diagonal lines are allowed only when inherited from a high-quality source template and visually calm.
- Never let connector lines cross through text, icons, logos, numeric values, pills, or card interiors unless the card is explicitly designed as a line endpoint.
- Never let connector lines overlap each other unless they intentionally merge into a trunk line with a visible junction.
- Never let a curved connector run nearly parallel against a straight rail/trunk/edge. Near-tangent collisions are worse than crossings because they look like broken geometry, not routing.
- Connector elbows should meet cleanly. Segment ends should touch or overlap by 1-2 px; visible gaps at bends, junctions, or arrowheads fail the audit.
- Connector endpoints must not render on top of card fills, hub fills, screenshot fills, logos, or panel boundaries. If a stroked route touches a surface, use a flush cap (`stroke.cap: "none"` in Pencil) or layer the route behind the endpoint surface so the surface clips the cap cleanly.
- Smooth bends should have enough radius to look intentional. For 1200 px blog graphics, use roughly 20-32 px bend radius for major bus turns unless the component style calls for tighter geometry.
- Align repeated connector segments to shared x/y centerlines. A routed bus should look engineered, not hand-threaded.
- If the connector path cannot be clean at the requested size, simplify the concept: reduce nodes, group nodes, or use numbered rows instead of a flowchart.

## Pencil Production Method

Use this method when a connector system must look production-grade in Pencil exports:

1. Build the visible connector system as one to three production `path` nodes, not many independent rectangles. Copy a known rendered rectangle with `C()`, then `R()` it into a `path`; this avoids direct-insert render failures.
2. Keep the route node viewBox equal to the parent frame, then write geometry in parent coordinates. This makes audit math straightforward.
3. For smooth routes, use stroked open paths with transparent fill, `stroke.join: "round"`, and quadratic/cubic Bezier bends. Use `stroke.cap: "none"` where the route meets a card/hub/screenshot surface; use round caps only for intentionally exposed endpoint marks. Put arrowheads in a separate filled production path so open route paths do not create filled wedge artifacts.
4. For strictly orthogonal routes, use filled capsule subpaths for horizontal and vertical lanes, plus integrated filled arrowheads. Avoid separate icon-font arrows unless copied from a known visible icon and verified in export.
5. Never leave `fill` enabled on an open stroked route path; it can render as huge filled triangles/wedges between route segments. Use `fill: "#00000000"` for the route and a separate filled arrowhead path.
6. Avoid multiple disconnected move commands in a single route geometry for one connector. If the route contains more than one move command, the audit must prove each segment is intentional, named in the outliner, and rendered as a clean port/junction rather than broken line debris.
7. Delete or move legacy rectangle fragments after the route path is verified. Keeping disabled fragments inside the final output node is allowed only during active debugging, never at handoff.
8. Do not use SVG circle subpaths as tee covers unless exported and verified; they can render as hollow artifacts. Prefer overlapping capsule lanes or copied rendered ellipses.
9. Export the parent and mandatory close-up crops after the route change. Inspect every arrow tip, not only the route body. The route only passes when the full view and close-up both show aligned ports, tangent-matched arrowheads, proportional arrowhead scale, the route stopping cleanly at the arrowhead base, smooth bends, no cap intrusion into cards/surfaces, no hollow artifacts, no wedges, no gaps, and no accidental line thickness changes.
10. Delete temporary probes after testing. The final output node must not contain random arcs, test arrowheads, disabled connector experiments, or nodes named `TEST`, `TMP`, `temporary`, `scratch`, `debug`, or `probe`.

### Rail And Trunk Join Pattern

When a curved connector needs to meet or pass near a straight rail, panel edge, card edge, or connector trunk:

- Use a real junction if the flow merges: same centerline, trimmed route endpoints, no doubled stroke, no rounded cap protrusion, and no visible seam.
- Use a clear bypass if the flow does not merge: the curve should stay visibly separated from the rail/trunk at zoomed export size.
- Prefer one integrated path for a merge when Pencil layering creates darker overlaps.
- If two separate path nodes meet, use flush caps and trim them so the end points meet cleanly without one path sitting under the other.
- Close-up export the join. A full-canvas screenshot cannot prove the rail/junction is clean.

### Smooth Route Pattern

For a branch/merge flow, prefer this structure:

- `Production smooth source connector route`: stroked path, transparent fill, flush caps at card/hub edges, round joins, Bezier bends from source ports into the hub lane.
- `Production smooth output connector route`: stroked path, transparent fill, flush caps at card/hub edges, round joins, Bezier bends from the hub lane to output ports.
- `Production smooth connector arrowheads`: filled path containing only closed arrowhead triangles, with tips aligned to target card edges.

Audit these nodes by name with `batch_get` and close-up exports. If the smooth route creates loops that look decorative instead of functional, simplify to a clean horizontal/vertical route rather than adding more curves.

## Recommended Patterns

| Pattern | Use when | Connector treatment |
| --- | --- | --- |
| Linear process | 3-6 steps in order | One horizontal/vertical line, equal step spacing, small endpoint marks |
| Hub and spoke | Many inputs route into one decision | Inputs align in a column/grid, short connectors merge into one hub, no crossing spokes |
| Swimlane | Different teams/systems own steps | One lane per team/system, connectors stay inside lane or move through defined handoff points |
| Stack/layer model | Foundation to activation | Vertical connectors or bracket marks, no crisscrossing |
| Matrix/map | Comparison or fields | Avoid connectors; use alignment, grouping, and highlights instead |

## Connector Audit

Before export, inspect the screenshot and answer:

- Can a viewer trace the flow in under 3 seconds?
- Do connectors touch the exact intended card/step, not a random area?
- Do all similar connectors use the same thickness, color, bend radius/shape, and endpoint logic?
- Are arrowheads centered on their lines, with no optical jump at the end of the segment?
- Does each arrowhead tip land on the intended port, lane endpoint, or target gutter instead of floating in the gap?
- Does each arrowhead point along the final segment tangent, including curved loopbacks and return paths?
- Is each arrowhead proportional to the connector stroke and available gap, rather than reading as a blunt wedge or separate shape?
- Does the route stop cleanly at the arrowhead base, or is there an unintended line running underneath the arrowhead?
- Are arrowheads truly visible in the export, not only present in node data?
- Are elbows and junctions smooth at close-up, with no gaps or accidental offsets?
- Do curves keep a clean gap from unrelated rails/borders/trunks, or merge through a deliberate tee/Y junction?
- Are there any near-tangent rail collisions, doubled strokes, dark seams, hooks, or partial overlaps where a curve meets or passes a straight line?
- Does any route use disconnected subpaths to fake a gap? If yes, does the close-up show an intentional port/junction, or does it read as broken fragments like regression `vfWSz`?
- Do route endpoints stop cleanly at card/hub/surface edges, with no rounded cap bleeding into the surface?
- For smooth routes, are the bends visibly rounded and consistent, with no filled wedge artifacts from open paths?
- Are connector routes production-clean in the outliner, with no leftover test or random nodes inside the exported frame?
- Are connector lanes clear of text and key values?
- Are there any unnecessary lines that can be replaced by proximity, numbering, or grouping?
- At 375 px preview, does the flow still read as a flow, or does it become visual noise?

If the answer to any of these is bad, the design does not pass.
