# Audit And Improvement Loop

Use this before exporting or presenting any MAN Digital blog, article, HubSpot, RevOps, infographic, web-page, A4, or social graphic. This adapts the Gemini carousel auditor pattern to single-image graphics: screenshot, measure, critique, fix, and re-audit.

## Required Tools

1. `get_screenshot` on the final node.
2. `snapshot_layout` on the final node with `problemsOnly: true`.
3. `snapshot_layout` on the final node with `maxDepth: 2` when alignment, padding, or hierarchy needs measurement.
4. `batch_get` for important text, card, callout, icon, and visual-anchor nodes when font size, fill, spacing, or semantics are uncertain.
5. `search_all_unique_properties` on the final node for `fontSize`, `fontFamily`, `fontWeight`, `fillColor`, and `textColor`; compare key text against `readability-depth-gate.md`.
6. `export_nodes` when a mobile readability check is needed; inspect a 375 px wide preview before finalizing dense blog graphics.
7. For flowcharts/process diagrams, read `flow-connectors.md` and audit connector routing as a separate production-quality dimension.
8. For dense cards, callouts, flowcharts, arrows, or named problem nodes, read `zoom-audit.md` and inspect child nodes directly. A full-canvas screenshot alone is not a pass.
9. For any connector with a tip, arrowhead, endpoint cap, or directional marker, export or screenshot a close-up of the tip region. The crop must show the tip, base, route endpoint, and final segment; otherwise zoom in further.
10. For heading/support pairs, use `snapshot_layout` rendered rectangles and verify vertical clearance before judging the screenshot.
11. For the header/support stack versus the main visual zone, use `snapshot_layout(maxDepth: 3 or 4)` and `batch_get` to compare sibling rectangles. The audit must compute the bottom of the final header/support text and the top of the first panel, card, label, screenshot, connector, or main visual. This catches absolute-position collisions that `snapshot_layout(problemsOnly)` misses.
12. For named/problem nodes, measure node geometry against its parent frame and sibling group. Record the intended rail before moving anything: parent safe-area edge, card grid edge, logo rail, label/pin rail, or connector port centerline.
13. Read `library-scan-loop.md` and compare the finished design against the selected Playground/registry component lineage.
14. For HubSpot/RevOps/signal/CRM graphics, read `master-template-fit-map.md` and confirm the output can be traced to the evaluated fit across `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, and `llyux`.
15. Read `production-quality-floor.md` and confirm the graphic has a strong visual anchor, specific content, library DNA, brand presence, and no shallow repeated-card construction.
16. Read `editable-pencil-source.md` and confirm the final `.pen` is editable native Pencil construction, not a flattened image pasted back into the canvas.
17. Read `readability-depth-gate.md` and identify the selected visual-depth source. If none exists, explicitly justify why the graphic should remain minimal.
18. Read `container-spacing-and-topic-coding.md`; measure container padding and confirm category/topic differentiation where the prompt has multiple groups.
19. If a Figma URL or Figma-derived reference was used, read `figma-patterns.md` and confirm the Pencil build translated the pattern into editable nodes with matching card, pill, icon, line, and decoration rules.
20. Audit composition efficiency: large brand planes, sidebars, rails, and decorative blocks must carry content, define a meaningful lane, or improve comprehension. A logo-only slab is a failure.
21. Confirm the output lives in a prompt-specific `.pen` file, not `Playground.pen` and not a previous prompt's output file.
22. For every pill/chip/badge/label bar, perform the pill alignment gate: measure label centerline against container centerline, verify left/right and top/bottom padding, and inspect a close-up crop of the most crowded label. A miscentered label inside a rounded pill is a hard fail.
23. Search the final output subtree for temporary/probe layers before handoff. `TEST`, `TMP`, `temporary`, `scratch`, `debug`, and `probe` nodes are hard failures inside the exported frame.
24. Review the last Pencil MCP write responses. Any `batch_design` `issues detected`, invalid icon name, unsupported property, missing asset, or render-affecting warning is a hard failure until fixed.
25. Run a full-frame section-fit check after child-node zoom checks. Outcome bands, footers, brand strips, sidebars, and section blocks must not overlap the main visual and must not create excessive dead vertical space. If the whole screenshot feels disconnected after close-up fixes, repair the section layout.

## Audit Loop

Run up to two improvement rounds.

1. **Round 1 audit**: screenshot and measure the graphic.
2. **Critique**: write a short internal critique using the scorecard below. Be strict; do not excuse weak spacing, vague hierarchy, cramped text, or off-brand choices.
3. **Fix critical issues**: apply targeted Pencil edits for alignment, padding, typography, content fit, callout clarity, visual hierarchy, and mobile readability.
4. **Round 2 audit**: screenshot and measure again after fixes.
5. **If still below pass threshold**: either do one final targeted fix when obvious, or tell the user the remaining limitation instead of silently shipping weak work.

Do not make broad redesigns after the second round unless the current concept is fundamentally wrong for the requested format.

## Scorecard

Score each dimension from 1-10.

| Dimension | Checks |
| --- | --- |
| Format Fit | Canvas size, requested channel, single/multi-panel constraint, blog-vs-slide grammar, crop safety |
| Brand Compliance | Medium Blue `#000FC4`, Ghost White `#F7F7FF`, cyan accent `#2DE4E6`, restrained orange, Montserrat headings, Lato body |
| Alignment & Padding | Consistent edge margins, grid discipline, aligned text/card axes, measured internal padding inside pills/cards/boxes, label/logo rails, no accidental offsets |
| Visual Hierarchy | One clear primary visual, clear reading order, strong but not crowded focal area, enough whitespace, distinct topics are visibly grouped |
| Content Fit | Copy fits containers, no inherited stale labels, component-level text anatomy passes, visual semantics match the prompt, no unnecessary text density |
| Mobile Readability | Key text remains readable at 375 px wide, source font sizes match the output scale, no tiny table-heavy details |
| Composition Efficiency | Large planes, rails, sidebars, and decorations earn their footprint; no dead brand slabs or logo-only blocks steal content area |
| Connector Quality | Flow lines are cohesive, routed through lanes, smooth where branched, consistent, traceable, and free of spaghetti crossings or path-fill artifacts |
| Library Use & Variation | Existing Playground/registry components were scanned, mature parts were reused, and the result is consistent with the library without repeating the last graphic by default |
| Visual Depth | A mapped Playground/design-system depth system supports the composition when needed, without competing with text or connectors |
| Concept Specificity | The content has a real takeaway, stage/category-specific meaning, and no stale placeholder repetition |
| Editability | Text, notes, labels, cards, callouts, connectors, and diagram parts remain editable native Pencil nodes |
| Polish | Professional craft, no AI-generic decoration, callout pointers land on targets, icons/lines/shadows feel intentional |

Pass threshold:

- `>= 8.0`: pass.
- `6.0-7.9`: fix all critical issues and re-audit.
- `< 6.0`: concept/layout is failing; revise the design direction or ask the user for guidance.

## Hard Fail Conditions

If any of these are true, the graphic fails even when `snapshot_layout(problemsOnly)` returns no layout problems:

- A callout, connector, card, icon, or decoration crosses through a headline, subtitle, paragraph, logo, field label, or primary data value.
- The main title or explanatory sentence is partly obscured by annotations, connectors, or decorative layers.
- Any text block visually touches, overlaps, or competes with another text block at full-size screenshot review or in the 375 px preview. Treat near-collisions as failures, not as polish issues.
- A heading/subheading or heading/support pair overlaps by geometry, including when the heading wraps farther down than expected.
- A header/support stack overlaps, touches, or visually merges with the first visual zone below it. Compute `lastHeaderText.y + lastHeaderText.height` against the top of every likely visual-zone sibling; require at least 32 px clear gap before panels, cards, labels, screenshots, connectors, and decorative planes that read as the main visual. Regression `g2Emw` is the model failure: header bottom 327, panels top 304, labels top 330, and `snapshot_layout(problemsOnly)` still passed.
- A bottom outcome band, footer strip, or impact section overlaps lower cards/columns, visually attaches to the wrong section, or creates a large dead gap from the main visual. Full-frame section fit must pass after close-up crops pass.
- Any risky child card, pill, badge, callout, or table cell has not been inspected directly when it contains stacked text or small labels.
- Text inside a pill, chip, badge, callout, card, frame, box, table cell, or label bar is cramped, visually touches the edge, lacks measured internal padding, or has mismatched left/right padding without an intentional icon slot or rail.
- Text inside a pill, chip, or badge is not visually and geometrically centered vertically. A label sitting low/high in the rounded fill, including a status pill like `Draft mode`, fails even when it is legible.
- A pill or badge label wraps because the container is too narrow. Convert it to a larger badge/card or shorten the copy instead of shrinking key text.
- A text node can wrap into the next sibling because its width is too narrow or its following label starts too close below it.
- Key labels, captions, or field names are too small for the intended usage size. For example, 20 px Lato labels in a 1536 px wide mobile-sensitive blog graphic collapse to about 5 px in a 375 px preview and fail.
- A headline wraps into another line without enough vertical space, causing the next line, subtitle, eyebrow, or diagram to visually merge with it.
- A named/problem node is not aligned to an explicit rail and has no intentional reason for being offset. This includes top context labels, pins, callout bars, logo marks, cards, icon tiles, and diagram nodes.
- A top/bottom brand or context element floats between grids instead of aligning to a parent edge, panel edge, card grid, or logo rail. Fix the alignment system, not just that one element.
- More than one visual system competes for attention at the same level, such as app chrome, field cards, side callouts, connector lines, footer strip, and decorative panels all carrying equal contrast.
- No Playground/registry scan was performed before building an open-ended graphic.
- A HubSpot/RevOps/signal/CRM graphic did not explicitly evaluate `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, and `llyux` before starting from primitives or a different template.
- A new prompt graphic was built inside `Playground.pen` or inside a reused output `.pen` from a different prompt.
- The final graphic was rebuilt from generic primitives even though the registry contains a suitable component, template, card system, connector system, icon treatment, label pin, screenshot frame, or logo treatment.
- The final graphic, main diagram, notes, labels, cards, or annotations are flattened into one image node or image fill instead of editable Pencil nodes.
- An exported screenshot/PNG/JPEG/WebP of the design was inserted back into the `.pen` as the working/final canvas.
- A copied Playground component was replaced by a screenshot of the component, making its text and nodes uneditable.
- The whole graphic is a title plus repeated identical cards with no stronger visual anchor, no library lineage, and no stage-specific content.
- A large brand slab, empty sidebar, color plane, or decorative block consumes useful canvas area without carrying content, defining a meaningful lane, or improving the main visual. Regression `ZBw56` is the model failure: logo-only full-height brand planes are wasted space.
- Stage, framework, process, or audit cards repeat the same placeholder copy under different headings without using a matrix/checklist structure to justify the repetition.
- Text appears to be floating over rectangles instead of living in padded layout containers, and no manual padding proof is recorded.
- `search_all_unique_properties` finds no `padding` or `gap` in a graphic dominated by cards, pills, boxes, or table cells.
- The graphic is technically aligned but visually boring because it is only primitive rectangles/text and ignores mapped Playground/design-system depth elements that fit the prompt.
- A graphic with multiple topics, departments, stages, statuses, systems, audiences, or ownership areas treats every group identically, with no restrained category cue such as lanes, chips, rails, tints, icons, borders, or section headers.
- A structural cue exists in the outliner but is invisible because its fill matches the immediate parent/background. This includes accent bars, top bars, left rails, dividers, chips, pills, icon medallions, connector marks, and label surfaces.
- The final output does not identify a visual-depth lineage when the design needs one, such as dot grids, radar arcs, pale ellipses, background planes, label pins, medallions, screenshot frames, or logo treatment.
- The background decoration is a repeated generic circle/ellipse motif with no mapped lineage. Regression `egabQ` is a hard fail unless the user explicitly asked for that exact motif.
- A Figma-derived design was flattened into an image instead of rebuilt as editable Pencil cards, text, icons, connectors, and decoration layers.
- A Figma-derived or icon-heavy build has unresolved Pencil MCP write warnings such as unsupported icon names. Tool-reported construction issues must be fixed before visual approval.
- The graphic blindly repeats the most recent successful layout when a different registry component family better fits the prompt.
- The graphic relies on many small labels to explain the concept. For mobile-readable blog graphics, simplify the concept instead of adding more labels.
- External callouts surround all sides of the main visual and make the canvas feel boxed in. Prefer either integrated labels inside the main visual or 2-3 high-value callouts.
- Connector lines create a web or cage around the content instead of directing attention to a few targets.
- Flowchart/process connectors are jagged, inconsistent, crossing, diagonal without intent, or visually read as spaghetti.
- Flowchart/process connectors are misaligned at card ports, have rough elbows, use inconsistent centerlines, have arrowheads that do not sit on the line center, or change thickness unexpectedly at joins.
- Arrowhead tips are misaligned, oversized for the gap, floating away from the intended port, pointing against the final segment tangent, or reading as separate wedges instead of route direction markers.
- Any connector tip/arrowhead was approved without a close-up crop/export of the tip region. Full-canvas screenshots do not count.
- A connector line visibly runs underneath an arrowhead triangle instead of stopping at the base, being hidden, or forming one integrated arrow shape.
- A curved connector grazes, overlaps, runs parallel against, or visually merges into a straight rail, panel border, card edge, or connector trunk without a deliberate clean junction. Dark seams, doubled strokes, hooked caps, or partial overlaps fail.
- Smooth connector routes use filled open paths, creating triangles/wedges, blobs, or other route-fill artifacts. Open stroked routes must have transparent fill and separate filled arrowheads.
- A connector endpoint or rounded stroke cap intrudes into a card, hub, screenshot, logo, or panel fill. This is a hard fail even if the line is otherwise smooth and aligned.
- Connector lines touch, pass under, or run too close to text, icons, logos, numbers, or important card content.
- Process-step cards are connected from inconsistent anchor points, making the direction of the process ambiguous.
- Temporary render-test layers, random arcs/shapes, disabled scratch fragments, or hidden experiment nodes remain inside the final exported/proof frame.
- The central visual is not immediately readable within 3 seconds at full size and in the 375 px preview.
- A visible footer/note says `Article context:`, `Prompt to use in Figma:`, `Reason X...`, prompt rationale, section rationale, audit rationale, placeholder instruction, or internal planning explanation. These are private planning inputs, not replacement-art content.

## Single-Graphic Measurement Checks

- Confirm the top-level node is exactly the requested canvas size.
- Confirm there is one final top-level output unless the user asked for variants.
- Confirm the main visual element occupies the requested share of the canvas; for mobile-readable blog graphics, target at least 60% when the prompt requires it.
- Check large non-content blocks. Any sidebar, slab, rail, color plane, or decorative shape larger than roughly 10-12% of the canvas must be content-bearing or clearly improve comprehension; otherwise shrink or remove it.
- Check source font sizes against the final canvas width. For mobile-sensitive graphics, key labels must survive the 375 px preview; do not approve 20 px key labels in a 1536 px wide output.
- Check edge safe area. Default minimum: 48 px for 1200 px wide assets, 64 px for 1536 px wide assets, 80 px for 1920 px wide assets, unless a source template intentionally uses a different system.
- Check sibling cards/callouts share equal widths or intentional rhythm.
- Check internal padding for every text container. Use `container-spacing-and-topic-coding.md` minimums for pills, chips, badges, cards, callouts, boxes, frames, table cells, and label bars.
- Check pill/chip/badge label centering as geometry: label centerline should match container centerline within 2 px for native layout, with 4 px allowed only for documented optical compensation. Screenshot the crowded pill crop before passing.
- Check icon-plus-label pills as three measurements: icon left padding, icon-to-text gap, and text right padding.
- Check all named/problem nodes with `batch_get` plus parent `snapshot_layout`: compare left edge, right edge, and centerline against siblings and parent rails. If the node is meant to be right-aligned, its right edge should match the rail within 2 px; if the source component has optical compensation, document the reason.
- Check context labels, pins, callout bars, and logos as a set. They should align to a shared top/bottom or left/right rail, not drift independently.
- Check visible non-graphic text. Remove article-context notes, prompt/context paths, placeholder labels, prompt rationale, audit notes, or "why this graphic exists" footers. A HubSpot placeholder graphic replaces the placeholder inside the article, so the article provides the context.
- Check callout bodies use short phrase-length copy. If the concept becomes text-heavy, simplify the concept rather than shrinking type.
- Check visual depth. Name the approved Playground/design-system depth source used, or document why a minimal treatment is intentional. A primitive-only row of cards is not enough for most MAN Digital blog graphics.
- Check decoration provenance. Name the exact mapped decoration source (`VsypW`, `xOLUX`, `p4Dtt`, `GogdW`, dot grid, radar arc, plane, approved decor SVG, or Figma source). If it cannot be named, remove it.
- Check topic coding. If the prompt has multiple categories, departments, stages, or statuses, identify the chosen differentiation system and confirm it is visible without reading all body text.
- Check component-cue contrast. Compare each accent bar, top bar, chip, pill, rail, divider, icon medallion, connector mark, and label surface against its immediate parent fill. Same-fill or near-invisible cues fail even when they are present in node data.
- Check production quality floor. The graphic must have a specific takeaway, a main visual anchor, library DNA, brand presence, and content that changes meaningfully by stage/category where relevant.
- Check repeated cards. If cards share the same internal labels, confirm the design is a matrix/checklist comparison; otherwise revise with stage-specific content.
- Check `padding` and `gap` properties for card/pill-heavy graphics. If absent, inspect whether text is incorrectly free-floating over rectangles.
- Check every text layer against neighboring text layers in the screenshot. There must be clear visible separation, not merely non-overlapping bounding boxes.
- Check heading/support pairs with rendered rectangles: heading bottom plus at least 16 px must be above support top; support bottom plus at least 24 px must be above the visual zone.
- Check the header/support stack against the first visual zone as sibling geometry: rendered support bottom plus at least 32 px must be above panels, cards, labels, screenshots, connectors, and decorative visual planes. If the first panel begins behind the header or a label sits inside the support zone, move the whole visual system or rebuild the header/visual relationship; do not accept a screenshot-only pass.
- Check risky cards, pills, badges, and callouts with `batch_get` and a direct child-node screenshot. Confirm stacked text children have enough vertical separation if the title wraps.
- Check connector lines point to the correct target and do not visually cross unrelated content.
- Check connector routing against `flow-connectors.md`: consistent ports, clear lanes, uniform thickness/color, no spaghetti, no text collisions.
- Check arrows and connector endpoints in close-up, including arrowheads, joins, and port positions.
- Check arrowhead tip geometry in close-up: tip point, base point, connector centerline, final-segment tangent, proportional scale, and target gutter. For curved loopbacks, the arrowhead direction must match the curve tangent at the endpoint.
- Check connector-tip zoom proof. Every arrowhead/tip/endpoint marker must have a close-up screenshot/export showing that the route stops cleanly at the base or is intentionally hidden/integrated.
- Check line smoothness at close-up: corners/tees must look intentional, no hollow artifacts, no visible segment gaps, no misaligned arrowheads, and no legacy fragments showing through.
- Check rail/trunk proximity at close-up. Any curve near a straight rail, panel edge, card edge, or connector trunk must either keep a clear visible gap or use an intentional tee/Y/integrated junction. Reject tangent grazing, doubled color, dark seams, hooks, and accidental overlaps.
- Check endpoint treatment at every card/hub/surface intersection. Stroked routes must use flush caps (`stroke.cap: "none"` in Pencil) or sit behind the endpoint surface so rounded caps cannot bleed into the fill.
- Check the route node anatomy for smooth lines: open path routes have transparent fill, round joins, flush caps at surfaces, Bezier or rounded bends, and arrowheads live in a separate closed/filled path or verified visible icon.
- Check process-step cohesion. A viewer should understand the order and direction without reading every label.
- Check stacked complexity: count distinct high-contrast systems. A blog graphic should usually have one primary visual system and one annotation system, not separate app chrome, table, cards, callouts, connector web, footer strip, and decoration all competing.
- Check annotation count. If the prompt names five fields, consider highlighting five fields inside the main visual and using only 1-3 external explanatory callouts.
- Check no slide-only elements appear in blog graphics: page numbers, deck footers, proof badges, carousel indicators, or slide labels.
- Check that finished brand marks use a real MAN Digital logo asset, not typed footer text.
- Check the library scan result: identify the selected component lineage and at least two alternatives considered when the prompt was open-ended.
- Check the master-template scan result for HubSpot/RevOps/signal/CRM prompts: each of `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, and `llyux` must have a primary, secondary, depth, or not-fit decision.
- Check that the final graphic reuses mature library DNA such as cards, icons, pins, connector systems, screenshot frames, spacing, or logo treatment, while varying the composition enough to fit the current prompt.
- Check editable source integrity. Key text, notes, labels, cards, callouts, connectors, and diagram pieces must be selectable/editable nodes, not pixels inside a single image.
- Check image nodes. Any image-filled node inside the final output must be a legitimate logo, screenshot, provided/generated image, or placeholder, not the flattened final design.
- Check file hygiene: the final graphic is in its own prompt-specific `.pen`, and `Playground.pen` was only used as a component source unless the user explicitly requested a library update.
- Check the layer/outliner hygiene of the final node: no temporary test names, no random leftover probes, no disabled scratch layers, and no hidden connector experiments inside the export frame.

## Internal Critique Format

Use this structure during the loop:

```markdown
### Audit Report
- Status: PASS | PARTIAL | FAIL
- Scores:
  - Format Fit: N/10
  - Brand Compliance: N/10
  - Alignment & Padding: N/10
  - Visual Hierarchy: N/10
  - Content Fit: N/10
  - Mobile Readability: N/10
  - Composition Efficiency: N/10
  - Connector Quality: N/10
  - Library Use & Variation: N/10
  - Visual Depth: N/10
  - Concept Specificity: N/10
  - Editability: N/10
  - Polish: N/10
- Overall Score: N/10
- Critical Fixes:
  - node/area: exact issue -> exact change
- Advisory Improvements:
  - node/area: optional improvement
- Re-audit Result:
  - what improved, what remains
```

Only include the audit report in the final user response when the user asks for it or when there are meaningful remaining limitations. Otherwise, summarize the pass/fail result briefly.
