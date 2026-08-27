# Readability And Visual Depth Gate

Use this before building and during audit for blog graphics, article visuals, Open Graph images, HubSpot/RevOps diagrams, and any graphic that must stay clear at mobile widths.

## Portrait-First Default (overrides prompt size)

In-article blog graphics are scrolled and read on phones. Choose orientation for mobile legibility, not for the size string in the prompt or placeholder.

- Default to portrait (`1024 x 1366` 3:4, or `1080 x 1350` 4:5) for any table, matrix, 4+ rows, multi-column comparison, list, swimlane, or stacked-step graphic. A 1024 px-wide portrait renders at ~37% on a 375 px phone vs ~24% for 1536 px landscape — about 1.5x more legible.
- Reserve landscape (`1536 x 1024`) for a wide website hero, an OG/share image, a genuine 3-5 item horizontal comparison that stays readable, or an explicit slide/user request.
- When converting to portrait: stack horizontal zones vertically, turn left-to-right arrows into top-to-bottom arrows, and cut wide tables to 3-4 columns (push detail into a sub-label) before reducing font size.
- This rule is mandatory; see SKILL.md `Mobile-First Sizing`. A graphic that matches the prompt's stated landscape size but is unreadable on mobile fails the gate.

## Text Scale Rule

Canvas font size alone is not enough. Judge important text after scaling the final graphic to the expected viewing width.

Formula:

`mobile_px = fontSize * preview_width / canvas_width`

For a 375 px mobile preview:

| Canvas width | 20 px source text becomes | Practical rule                                     |
| ------------ | ------------------------: | -------------------------------------------------- |
| 1200         |                    6.3 px | Key labels usually need 34-40 px source or larger. |
| 1536         |                    4.9 px | Key labels usually need 42-56 px source or larger. |
| 1920         |                    3.9 px | Key labels usually need 54-70 px source or larger. |

If a text layer explains the concept, names a step, labels a card, or carries a user-requested field, it is key text. Do not ship it at 20 px in a 1536 px wide blog graphic. Enlarge it, reduce copy, increase the element size, or remove the text and let icon/shape hierarchy carry the detail.

Small metadata can stay small only when the graphic still works without reading it.

## Build-Time Guardrails

- Limit key copy to what can be made readable: usually one headline, one support line, 3-5 short labels, and optionally 1-3 callouts.
- For process cards, prefer icon plus a large one-to-three-word title. Do not add tiny explanatory captions unless the output is meant for large desktop/print use.
- If four or more cards need explanations, switch to a larger inline explainer format, a vertical frame, or a simplified flow instead of shrinking text.
- For pills, chips, badges, cards, callouts, and table cells, do not shrink key text to solve bad padding. Use `container-spacing-and-topic-coding.md` to enlarge the container or simplify the copy.
- Use `fixed-width` text inside layout frames and let height grow. Avoid fixed text boxes that only appear to fit at full canvas size.
- For prompt-required mobile readability, export or screenshot a 375 px wide preview and inspect it. If key labels are not readable in three seconds, the design fails.

## Static Image Reality

Pencil exports a single image. It will not become responsive inside a blog post, CMS card, LinkedIn preview, or mobile viewport. A 2x export can improve crispness, but it does not change the visual size of text after the browser scales the image down.

Design against the smallest expected display width:

- Blog body mobile: assume 343-375 px.
- Blog hero or OG preview: assume 375-600 px visible width.
- LinkedIn mobile feed: assume fast scanning below full device width.
- A4/print: mobile rules may not apply, but print-safe type still matters.

If the image will be read on mobile, simplify the model before shrinking type. Use fewer labels, larger cards, stronger icons, and one clear visual path. If the concept needs many readable details, choose a taller inline explainer or ask whether the communication can become multiple graphics.

## Visual Depth Rule

MAN Digital graphics should not be primitive-only unless the prompt explicitly asks for extreme minimalism. A mature graphic normally has:

- one primary visual system: screenshot frame, architecture map, flow, matrix, flywheel, stack, or large field-card system;
- one supporting library system: icon medallions, label pins, callout bars, connector lane, background plane, dot grid, radar arc, pale ellipse, screenshot shell, or approved logo treatment;
- when multiple topics/categories exist, one restrained differentiation system: lane tint, chip, rail, icon medallion, grouped panel, border, or section header;
- restrained decoration placed behind content or in negative space.

A plain row of outlined rectangles with tiny icon-label text is a fail when the Playground has suitable components.

Read `production-quality-floor.md` when the composition is mostly cards, process steps, framework boxes, or a simple sequence. Visual depth cannot rescue a shallow concept with repeated placeholder copy.

## Mapped Depth Sources

Use these before inventing decoration:

- Dot grids: `VJCMg`, `tvqbC`, `c1w4M`, `U625h3`, `B7kMJ`, `gLgmf`, `rIUUB`, `vS0eG`, `Hc1B4`, `Lj0X5`, `DdguX`, `a757nP`, `zYRe1`, `zRszE`.
- Radar/orbit/signal arcs: `MRO7A`, `Jm3qM`, `V5C2Z`, `DEXIR`, `kC04H`.
- Pale depth shapes and background planes: `xLkzv`, `NZhqk`, `i8rgC`, `I6QCPl`, `HQP5q`, `oCVLE`, `EzX4X`.
- Gemini/carousel decoration references: `VsypW` soft circles, `xOLUX` blue geometric pattern, `p4Dtt` orange union accent, and `GogdW` orange/blue circle-path accent. Verify availability in the active Pencil file; if unavailable, recreate the same editable anatomy only when it fits the composition.
- Icon and stage systems: `KVqAt-stage-medallions`, `KVqAt-pill-rows`, `b8SoH-central-hub`, `llyux-capability-tiles`, `nRPmP` orbit steps.
- Logo/brand marks: approved assets in `/Users/romeoman/Documents/Marketing/Design/MAN Digital Design System/assets/`, especially `logo-mono-blue.png`, `logo-mono-white.png`, and `logo-color.png`.
- Design-system decor assets: `assets/decor/dot-mesh.svg`, `dot-column.svg`, `ellipse-fading.svg`, `etched-sphere.svg`, `circle-shadow-fade.svg`, `ellipse-thin-stroke.svg`, `diamond-hollow.svg`, and restrained orange chevrons/circles when the composition needs a small directional accent.

Keep these elements low contrast and behind content. Do not add random shapes that are not traceable to the Playground, Gemini carousel registry, Figma source, or design-system asset library.

Decoration variation is required. Do not keep using the same made-up pale circle/ellipse motif just because it worked once. Regression `egabQ` is the model failure: it was not traced to a documented component and did not add meaning. Select an approved depth source for the current prompt, or leave the background clean.

## Dead-Space And Brand-Block Gate

Visual depth must earn its footprint. A decorative plane, sidebar, brand block, rail, or background shape fails when it reduces the usable area for the main visual without adding comprehension.

- Treat a non-content block larger than roughly 10-12% of the canvas as suspect. It must contain content, define a section/lane, or frame the main visual in a way that improves comprehension.
- Do not reserve a full-height or full-width slab only for the MAN Digital logo. Use a compact approved logo asset instead.
- Brand color can appear through cards, accent rails, connector systems, header/footer treatment, and small depth elements. It does not need a dead side panel.
- If the main visual could be larger, clearer, or more mobile-readable by removing the block, remove or shrink it.
- Regression case `ZBw56`: a 236 px wide full-height Medium Blue plane on a 1536 px canvas consumed about 15% of the width while carrying only a logo. That is a hard fail for future blog graphics unless converted into a content-bearing lane.

## Audit Requirements

Run these checks before handoff:

1. Use `search_all_unique_properties` on the final output for `fontSize`, `fontFamily`, `fontWeight`, and colors when the active Pencil MCP exposes it. If it is unavailable, use `batch_get` on the final frame and risky child nodes plus `snapshot_layout(maxDepth: 3 or 4)` to inspect text sizes and geometry.
2. Use `batch_get` on every key text node below the practical source-size rule and decide whether it is truly incidental. If not, fix it.
3. Export or inspect a 375 px preview for mobile-sensitive blog graphics.
4. Identify the visual-depth source used. If none exists, either add an approved mapped element or explain why the prompt requires a fully minimal treatment.
5. Confirm the container-spacing plan was used for text inside pills/cards/boxes and that key text was not shrunk to compensate for cramped containers.
6. Confirm the topic-differentiation plan was used when the prompt has multiple categories, departments, stages, systems, statuses, or audiences.
7. Confirm the static-image scaling was considered. The audit must reject text that would only work if the layout could reflow.
8. Confirm large decorative planes, rails, and brand blocks are content-bearing or compositionally necessary. Remove dead slabs that steal space from the main visual.
9. Reject outputs that look like generic primitive diagrams, even when alignment and overflow checks pass.

## Failure Examples

- Regression case `b7aJDH`: a 1536 x 1024 HubSpot RevOps diagnosis graphic was built in `Playground.pen` with key labels `OyaTH`, `u1c4n`, `SRGaY`, and `cjSnq` at 20 px Lato. It passed basic layout but failed because those labels shrink to about 5 px in a 375 px preview, the output belonged in its own `.pen`, and the visual system was only primitive rectangles plus tiny captions.
- Regression case `ZBw56`: a full-height Medium Blue brand slab consumed about 15% of a 1536 x 1024 blog graphic without carrying content. It made the diagram smaller and should have been replaced by a compact logo or content-bearing lane.
- A 1536 x 1024 frame with four 240 px cards, 20 px captions, and a dark outcome card. The structure is technically aligned, but the key labels become unreadable on mobile and the graphic has no MAN Digital depth.
- A flowchart made from new rectangles and connector fragments when a Playground architecture, stage-card, or connector system already exists.
- A three-department diagram where Sales, Marketing, and Customer Success are identical white boxes with no lane, chip, rail, tint, icon, or grouping cue.
- A pill or badge where text nearly touches the rounded edge or the icon gap is inconsistent across repeated pills.
- A stage framework where every card repeats the same labels and the design has no stronger visual anchor than the repeated cards.
- Decorative dots placed over small text, or radar arcs competing with connector lines.
- A generic pale circle/ellipse decoration repeated across unrelated graphics with no registry lineage or concept role.
