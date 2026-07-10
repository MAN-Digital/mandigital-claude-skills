---
name: man-digital-blog-graphics
description: Create production-grade, editable MAN Digital blog, article, LinkedIn, HubSpot, and RevOps graphics in Pencil/Pencil.dev using the local MAN Digital design system, the saved Pencil Playground component library, and the Gemini carousel component references. Use when asked to design or adapt MAN Digital blog graphics, post visuals, article hero images, explainer diagrams, signal-engine visuals, diagrams, or carousel-derived social graphics, especially when the output must avoid flattened image-only canvases, generic primitive diagrams, cramped text, weak category cues, stale placeholder copy, unbranded layouts, or bad designs that pass basic layout checks. Also use when asked to review, optimize, update, or self-improve this MAN Digital/Pencil graphics skill, registry, audit loop, or component references based on new outputs or regressions.
---

# MAN Digital Blog Graphics

Use this skill to create branded MAN Digital blog and social graphics in Pencil. It is optimized for graphics that need to reuse the real MAN Digital design system and the existing Pencil Playground components rather than inventing a new visual language.

## Platform Note (Claude Edition)

This is the Claude Code edition of the skill, ported from the Codex original. The rule hierarchy, source order, non-negotiables, audit loop, and QA gates are identical — do not weaken them.

- Read the `references/*.md` and `references/components/*.md` support docs in this skill folder with the normal file Read tool. They are plain markdown.
- Inspect and edit every `.pen` design file ONLY through the Pencil MCP tools (`mcp__pencil__get_editor_state`, `mcp__pencil__batch_get`, `mcp__pencil__batch_design`, `mcp__pencil__snapshot_layout`, `mcp__pencil__get_screenshot`, `mcp__pencil__export_nodes`, `mcp__pencil__get_variables`, `mcp__pencil__set_variables`, `mcp__pencil__get_guidelines`). `.pen` files are encrypted — never open them with Read, Grep, `cat`, or any raw file read.
- Call `mcp__pencil__get_editor_state(include_schema: true)` first if you do not already have the current `.pen` schema in this conversation.
- Use the HubSpot MCP and the bundled `scripts/` for fetch and publish steps; never invent post IDs.

## Required Startup

1. Read `references/source-paths.md`.
2. Read `references/brand-rules.md`.
3. Read `references/pencil-workflow.md`.
4. Read `references/selection-guide.md`.
5. Read `references/component-index.md`.
6. Read `references/figma-patterns.md` when the user provides a Figma URL, asks to implement a Figma design in Pencil, or the graphic needs card/pill/icon/decoration guidance from approved Figma examples.
7. Read `references/output-types.md` before choosing format or routing.
8. Read `references/graphic-styles.md` before choosing the visual system.
9. Read `references/master-template-fit-map.md` before choosing the base for any HubSpot, RevOps, CRM, signal, routing, scoring, AI, revenue-engine, workflow, pipeline, or operating-model graphic.
10. Read `references/production-quality-floor.md` before planning or auditing any output.
11. Read `references/readability-depth-gate.md` before setting text scale or deciding whether the graphic has enough visual depth.
12. Read `references/container-spacing-and-topic-coding.md` before placing text inside pills, cards, frames, boxes, badges, callouts, table cells, or any graphic with multiple topics/categories.
13. Read `references/editable-pencil-source.md` before building or auditing any Pencil deliverable.
14. Read `references/template-coverage.md` before assuming the available component set is limited to the user's examples.
15. Read `references/image-placeholders.md` when a template has a screenshot/image area or the graphic may need generated imagery.
16. Read `references/hubspot-post-fetch.md` when the prompt names a HubSpot post ID, HubSpot editor URL, public blog URL, slug, draft post, or asks to base the graphic on an actual post.
17. Read `references/hubspot-placeholder-publish.md` when the user asks to upload finished graphics, place graphics into HubSpot, replace placeholders, patch the blog draft, or use the Files/CMS APIs for graphic insertion.
18. Read `references/preview-manifest.md` when choosing between visual variants.
19. Read `references/current-playground-audit.md` when choosing from the current Playground template library.
20. Read `references/playground-candidate-roster.md` before choosing a base for any MAN Digital blog, HubSpot, RevOps, CRM, AI, workflow, prospecting, outbound, signal, carousel-derived, or article graphic.
21. Read `references/library-scan-loop.md` before choosing a base component and again during final audit.
22. Read `references/deep-dives.md` for the high-value templates before cloning them.
23. Read `references/gemini-pencil-learnings.md` for carousel-derived social graphics or when reusing Gemini frames.
24. Read `references/audit-loop.md` before finalizing any graphic.
25. Read `references/flow-connectors.md` before building or auditing flowcharts, process diagrams, lifecycle maps, or card-to-card sequences.
26. Read `references/zoom-audit.md` before finalizing any dense graphic, flowchart, callout system, process diagram, or component with small labels.
27. Read `references/skill-optimization-protocol.md` when the request is to review, optimize, update, or self-improve this skill, its registry, its audit loop, or its component references.
28. Load only the relevant files under `references/components/` for the selected direction.
29. Use the Pencil MCP for all `.pen` inspection or editing. Never read `.pen` files directly from disk.

## Source Order

When sources disagree, use this order:

1. MAN Digital design system: brand authority.
2. Pencil `Playground.pen`: component and layout authority.
3. Gemini carousel skill: reusable component registry and build discipline.
4. Fetched HubSpot post content: article-specific facts, headline, body language, and graphic opportunities when the prompt provides a dynamic post target.
5. User prompt: copy, topic, format, and final intent.

## Routing Rules

- If the user asks for a LinkedIn carousel, social carousel, slide-by-slide carousel, or carousel copy/design, use the `carousel` / Gemini carousel workflow and this skill only as MAN Digital blog/social/Pencil design-system support.
- If the user asks for a single blog graphic, article visual, inline explainer, Open Graph image, A4 page, flowchart, infographic, slide-deck graphic, or web-page graphic, use this skill directly.
- Treat "blog graphic" as a website/article asset, not a slide. Do not add slide footers, page numbers, proof pills, or deck cover grammar unless the user explicitly asks for a slide or deck.
- Do not bias toward only the deep-dive nodes the user recently named. Check `template-coverage.md`, `component-index.md`, and the Gemini carousel registry before deciding.
- If the user asks whether the skill is ideal, asks to check/optimize/update it, or reports a new failure from another session, run `skill-optimization-protocol.md`. Passing validators alone does not prove there is nothing to improve.

## Skill Optimization Mode

Use this mode when improving the skill itself rather than creating a graphic.

1. Read `references/skill-optimization-protocol.md`.
2. Look for new user feedback, recent Pencil outputs, exported screenshots, memory entries, and registry gaps.
3. Convert every new failure or successful correction into a concrete rule, reference update, registry entry, audit check, or validator improvement unless the skill already prevents it explicitly.
4. A no-op is allowed only with evidence: no new feedback/artifacts, no uncoded regression, no startup/reference gap, a representative prompt walkthrough passes, and validators pass.
5. Report changed files and validation results, or give the no-op evidence. Do not answer "nothing to improve" because basic registry validators passed.

## Default Workflow

1. Identify the requested output before designing: blog hero/featured image, Open Graph image, blog inline explainer, LinkedIn post, carousel-derived image, HubSpot image, slide graphic, A4 page, or diagram.
2. If the prompt names a HubSpot post ID, HubSpot editor URL, public blog URL, slug, or draft post, fetch that exact dynamic target before designing using `references/hubspot-post-fetch.md`. Do not use a fixed example ID or stale cached post unless the prompt target matches it.
3. Extract article-specific graphic opportunities from fetched post content: headline, H2/H3 structure, process language, named systems, fields, metrics, screenshots/image needs, and the section the requested graphic should support. Treat the whole fetched article as context for every graphic, not only the nearest placeholder block.
4. If the fetch output includes `*.graphic-placeholders.json`, treat `graphics[*]` as the production queue. Each `div.man-graphic-placeholder` prompt becomes a separate graphic unless the user explicitly asks for a subset. Before designing each queued graphic, read the linked `*.article-context.md` file and use the whole post to preserve terminology, argument, audience, and sequence. Use the prompt after `Prompt to use in Figma:` as the local brief, but do not design from that prompt alone; keep Playground/design-system/component registry authority above any `References:` links in the placeholder.
   - Blog replacement rule: the finished graphic replaces the `div.man-graphic-placeholder` block in the article. The placeholder prompt, `Article context:` path, required-context instruction, and any article rationale are private planning inputs only.
   - Visible output rule: do not place `Article context: ...`, prompt rationale, section rationale, audit notes, "Reason X..." explanations, placeholder labels, or internal planning explanations inside the final graphic. The surrounding blog article already carries that context. Add a caption/source note only when the user explicitly asks for one or the prompt requires a real external source citation.
   - Placement naming rule: for every fetched HubSpot placeholder output, use the fetched placeholder order as the graphic number and name both the `.pen` file and the final top-level frame exactly: `{Blog Title} - {Blog Post ID} - Graphic {Number} - {Graphic Title Name}`. The number is the top-to-bottom placeholder index in the post/manifest. If only a subset is generated or edited, preserve the original placeholder number; do not renumber `Graphic 5` to `Graphic 3`.
5. Run the Playground candidate roster pass: name at least one primary layout candidate, one alternate layout family, and one supporting component/depth candidate from `playground-candidate-roster.md`. The pass must name exact node IDs, not just "design system" or "brand style."
6. Run the library scan loop: search the registry, preview manifest, template coverage, deep dives, and relevant component refs; inspect live Playground candidates with Pencil. For the selected primary candidate, live `batch_get` inspection is mandatory before building.
7. For HubSpot/RevOps/signal/CRM graphics, run the master-template fit map across `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, and `llyux`. Pick a primary, secondary, depth, or not-fit result for each before building.
8. Write a quality-floor brief from `production-quality-floor.md`: visual job, audience takeaway, main visual anchor, component lineage, content specificity, differentiation system, and brand/logo treatment.
9. Choose one graphic style family with `graphic-styles.md`, then choose a base component with `selection-guide.md`, using previews when the choice is visual.
10. Compare at least three candidate sources for open-ended prompts: a primary layout, an alternate layout family, and a supporting component such as icons, pins, connectors, cards, or logo placement.
11. Choose a visual-depth source from `readability-depth-gate.md` and `figma-patterns.md`: a dot-grid, radar arc, background plane, pale ellipse, Gemini decoration (`VsypW`, `xOLUX`, `p4Dtt`, `GogdW`), label pin system, icon medallion set, screenshot frame, or logo treatment that fits the style family. Do not invent a new decoration because the canvas feels empty.
12. Set a text-scale plan before building. Treat the output as a static image: for mobile-sensitive blog graphics, do not rely on labels that collapse below readable size at 343-375 px; simplify copy or enlarge the visual instead.
13. Set a container-spacing plan from `container-spacing-and-topic-coding.md` before putting text into a pill, frame, box, badge, card, callout, table cell, or label bar.
14. If the prompt has two or more concepts, departments, audiences, stages, systems, or statuses, set a topic-differentiation plan from `container-spacing-and-topic-coding.md`: tint, label chip, stripe, icon medallion, lane, border, or section header.

- Use the approved semantic accent set when useful: `#5963D9`, `#F26419`, `#434343`, `#000FC4`, `#222222`, and `#C8CCF2`. Keep color coding subtle and purposeful; do not make a random rainbow palette.

15. Set a composition-efficiency plan from `graphic-styles.md` and `readability-depth-gate.md`: any large color plane, sidebar, rail, or decorative block must either carry content or materially improve the main visual. Do not add a full-height brand slab just to hold a logo or color.
16. Inspect the selected base component with Pencil `batch_get` before editing. Use `readDepth` 2 or 3 for layout components and deeper reads for icons or pills.
17. Export or screenshot the chosen base and compare against the preview manifest.
18. For composite frames such as `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, `llyux`, `EdtGZ`, `LZkoW`, `sQ8TR`, `pAw6X`, `fKn3K`, `PPpdM`, `s2ZqRB`, `v5aVuG`, `lLDFt`, `SbBJV`, `G7EWZ`, `G6YkCq`, `nia9w`, `DJN2N`, `jNmrp`, `NhErk`, `Y3Tzyc`, `zuu8y`, `lP11x`, and `HoOjV`, read the component/anatomy reference and choose the smallest reusable subcomponent that fits the prompt: whole frame, flywheel, stage card, source card, action chain, layer row, process strip, screenshot carrier, input card, pill, icon, connector, or decoration.
19. For any flowchart or process-step graphic, plan card positions and connector lanes with `flow-connectors.md` before drawing lines.
20. Choose the output `.pen` before making edits. Every prompt/run/graphic gets its own new `.pen` file under `/Users/romeoman/Documents/Marketing/Design/Pencil/Skill Tests/` unless the user gives a specific new output file. Do not reuse an old prompt file for a new graphic.

- For fetched HubSpot placeholder graphics, do not leave slug-only, date-only, or old test names as deliverables. Before handoff, rename the prompt-specific `.pen` and the final top-level frame to the placement naming convention so the user can match graphics to the article from top to bottom.
- File targeting guard: do not trust `batch_design(filePath=...)` against a non-existent `.pen` path. Pencil can ignore that path and edit the active document. Before destructive edits or new builds, ensure the target `.pen` exists, open it in LivePen when needed, and call `get_editor_state` to confirm the active editor path is the intended file. If a seed file is used to create a new `.pen`, delete/replace the seed content only after the active path is confirmed, and the final file must contain only the intended graphic.

21. Treat `/Users/romeoman/Documents/Marketing/Design/Pencil/Playground.pen` as read-only library/source by default. Inspect it, screenshot it, and read components from it, but do not insert, update, or delete nodes in it unless the user explicitly asks to edit the Playground library.
22. Copy or recreate existing component anatomy in the output file and override copy, icons, colors, and layout properties. Do not recreate mature components from scratch unless the library scan shows a real gap.
23. Keep the working `.pen` editable: text must be text nodes, cards/pills/callouts must be frames/shapes, connectors must be paths/shapes, and notes/labels must remain editable. Do not export the whole design as an image and place that image back into the canvas.
24. Use MAN Digital design-system assets from `/Users/romeoman/Documents/Marketing/Design/MAN Digital Design System/assets/`.
25. Use an approved MAN Digital logo asset for footer/brand marks. Do not type `MAN Digital` as plain text in finished graphics.
26. For every pill, chip, badge, or label bar, run the container-spacing and pill-alignment gate before export: text must be inside or measured against the container, centered vertically, padded on all sides, and verified with a close-up crop when the label matters to the graphic. Prefer the `KVqAt` pill rhythm (`XlJSz`, `pDKxe`, `wcgGl`, `D4tA8`) for signal/input pills unless another inspected component fits better. A miscentered status pill such as `Draft mode` fails.
27. Run the audit-and-improve loop in `references/audit-loop.md`: screenshot, measure, critique, fix critical issues, and re-audit. Include the zoom audit when any text/card/callout/connector detail could be missed at full-canvas scale. If the graphic has connector tips, arrowheads, endpoint caps, or directional markers, zoom/audit those tip regions directly; a full-canvas screenshot never passes connector-tip QA.
28. During audit, run the Playground candidate roster and library scan loop again: compare the finished graphic to the selected component lineage and confirm it is library-based, brand-consistent, and not a stale repeat of the last design.
29. During audit, run the production quality floor, editable-source gate, text-scale, composition-efficiency, container-spacing, and visual-depth gate. Use `search_all_unique_properties` for font sizes, padding, gap, large rectangles/frames, and occupied canvas area when the local Pencil MCP exposes it; if unavailable, use `batch_get`, `snapshot_layout(maxDepth: 3 or 4)`, and targeted screenshots of the final node plus risky children. Flattened image-only construction, tiny key labels, dead brand slabs, zero-padding card construction, cramped pills/cards, stale copy, or a boring primitive-only composition fail.
30. During audit, verify topic differentiation for graphics with two or more categories, departments, audiences, stages, systems, or statuses. A viewer should tell categories apart before reading every label.
31. Run the structural text-zone gate before judging screenshots: use `snapshot_layout(maxDepth: 3 or 4)` and `batch_get` to compare every header/eyebrow/title/support stack against the first visual-zone sibling below it. `snapshot_layout(problemsOnly)` is not enough because absolute sibling zones can overlap without being reported.
32. For every risky component and every heading/support pair, screenshot or inspect the child nodes and parent region directly. Whole-canvas screenshots do not prove text-fit or connector quality.
33. For every named/problem node from the user or audit, inspect the node, its parent, and relevant siblings with `batch_get` and `snapshot_layout`. Measure the intended left/right/center rail; do not fix isolated nodes by eye.
34. Before handoff, search the final output subtree for temporary or random test nodes (`TEST`, `TMP`, `temporary`, `scratch`, `debug`, `probe`) and delete them. Do not leave disabled experiments or hidden scratch connector fragments inside the exported frame.
35. Treat every Pencil MCP write response as part of QA. If `batch_design` reports `issues detected`, missing icons, unsupported properties, invalid fills, missing assets, or warnings that affect rendering, fix them before using screenshots as proof. A clean screenshot is not enough when the tool already reported a construction issue.
36. Run a full-frame section-fit audit after close-up QA. Outcome bands, footers, brand strips, sidebars, and section blocks must not overlap the main columns/cards and must not create large dead whitespace. If a band crowds the main visual or sits far away from it, move or resize the whole section system, not just a single node.
37. Run the QA checklist in `references/qa-checklist.md` before finishing.
38. If the user asks to upload/place the graphics into HubSpot, OR supplies a HubSpot Files folder ID for the in-context post, run `references/hubspot-placeholder-publish.md` after all design QA passes. A supplied folder ID is itself the request and confirmation: upload to that folder and patch the in-context fetched post's draft, replacing only the built graphic(s)' placeholders, without re-asking folder-vs-post or re-confirming (see the Folder ID Convention in that reference). Export final frames as 1x WebP with quality 100/lossless when possible, use SEO-friendly title-derived file names, write descriptive alt text into the replacement `<img>` tags, upload files to the user-specified HubSpot folder, replace `div.man-graphic-placeholder` blocks in manifest order, create local `postBody` backups, and patch only the draft endpoint unless the user separately asks to publish live. The asset mapping must include `source_pen_path` for every graphic. Do not upload or patch if Pencil export/screenshot is blank, stale, or missing child layers; fix the `.pen` source/export first. A publication-only fallback requires explicit user approval and must be disclosed.

For tests, experiments, proof runs, and normal new graphic creation, do not edit the primary Playground library and do not reuse a previous output file. Create one `.pen` per prompt/graphic under `/Users/romeoman/Documents/Marketing/Design/Pencil/Skill Tests/` or use the explicit new output file the user provides.

## Component Registry Maintenance

Use this when the user asks to analyze, break down, or add Pencil nodes to the component library.

1. Screenshot the whole node first so the full composition is understood before inspecting internals.
2. Use Pencil `batch_get` on the requested node at `readDepth: 2` or `3`, then inspect important child and grandchild nodes at deeper depth.
3. Create or update `references/components/<node-id>.md` for each reusable full node, subcomponent, pill, icon cluster, connector system, or content block.
4. For major composite frames, also create `references/components/<node-id>-anatomy.md` that maps the full visual hierarchy.
5. Each component reference should state: source node ID, visual role, structure/anatomy, when to reuse it, edit risks, and important child node IDs.
6. Update `references/component-index.md` so the component is discoverable by node ID and use case.
7. Update `references/deep-dives.md` when the node is a high-value template or part of a named sequence.
8. Run `scripts/check_required_nodes.py`, `scripts/check_registry.py`, and the system `quick_validate.py` before considering the skill update complete.

## Format Defaults

- Blog hero / featured article image: default to 1200 x 630 when the user says "blog graphic" or "article graphic" without a size. Use 1600 x 900 or 1920 x 1080 only when the placement is a wide website hero or the user asks for 16:9.
- Blog inline/explainer graphic: reuse the existing 1190 x 1684 vertical frame family or a contained article-module crop when the content needs explanation. Do not include slide page numbers.
- Open Graph image: default to 1200 x 630.
- LinkedIn feed graphic: use 1080 x 1350 when no other size is specified.
- Square carousel/post graphic: use 1080 x 1080 only when requested or when cloning a square component.
- Slide or deck graphic: use 1920 x 1080 and preserve slide grammar only when the user asks for slide, presentation, deck, or 16:9 slide.

## Mobile-First Sizing (MANDATORY)

Blog and article graphics are read inside a scrolling article, mostly on mobile. Readability on a phone outranks any size named in the prompt or placeholder. This section overrides `Format Defaults` and any size string in a fetched placeholder prompt.

- The size in a placeholder prompt (e.g. `1536x1024 landscape`, `1280x800 screenshot`) is a hint, not a constraint. Override it whenever a portrait/taller frame makes the content readable at mobile width.
- Default to portrait or tall formats for content-dense graphics: prefer `1024 x 1366` (3:4) or `1080 x 1350` (4:5) over landscape whenever the graphic has a table, matrix, 4+ rows, multi-column comparison, list, stacked steps, or a swimlane. A blog column renders a 1024 px-wide graphic at ~37% on a 375 px phone versus ~24% for 1536 px — portrait is roughly 1.5x more legible for the same content.
- Convert left-to-right flows into top-to-bottom flows when going portrait: `source -> translation -> target` reads cleanly as a vertical stack with down-arrows. A horizontal three-zone story becomes three stacked zones.
- Reduce columns before shrinking text. A wide table (6-7 columns) almost never survives mobile; cut to the 3-4 columns that carry the message, move secondary detail into a sub-label under the primary cell, and enlarge the rest.
- Minimum on-canvas type for a portrait blog graphic (1024-1080 px wide source): titles 40-48 px, section/zone titles 24-28 px, primary labels/object names 22-26 px, body/notes 16-18 px, pills/tags 13-15 px. For a landscape 1536 px graphic, scale these up about 1.4x. Never rely on sub-16 px body text to carry meaning on a mobile-read blog graphic.
- Landscape (1536x1024 / 16:9) is reserved for: a true wide website hero, an OG/social-share image, a genuine 3-5 item horizontal comparison that stays readable, or an explicit user/slide request. When in doubt for an in-article graphic, choose portrait.
- Treat "main visual >= 60% of canvas" as a floor, but never buy canvas coverage by shrinking key text below the minimums above.
- When overriding a placeholder's stated size, keep the same editable-source, naming, and `source_pen_path` rules; only the canvas dimensions and layout orientation change.

## Non-Negotiables

- Use Montserrat for headings and Lato for body text unless a source component already defines otherwise.
- Keep Medium Blue `#000FC4` as the anchor color.
- Use Ghost White, white cards, cyan accents, and restrained blue-tinted shadows.
- Avoid generic SaaS illustration, emoji, stock art, hand-drawn styling, and new unapproved decorative systems.
- Treat orange `#F26419` as a restrained accent or CTA color, not a general brand replacement.
- Prefer existing Streamline-style icons already embedded in the Pencil components.
- Prefer thin, clean Streamline-style icon treatment for cards, pills, and medallions. Use user-provided icon examples such as `GoNGR`, `id7JG`, `g0Gr3`, `OY5Hk`, and `vvog0` as style references for weight and cleanliness, but verify live availability before copying exact nodes.
- Use Playground components/elements first: templates, cards, icon treatments, pills, connectors, surfaces, and layout patterns. Only create primitives for gaps the Playground does not cover.
- Design-system compliance is not enough. Every finished MAN Digital graphic must have explicit Playground lineage: selected node IDs from `playground-candidate-roster.md`, `component-index.md`, `template-coverage.md`, or another inspected Playground node. A design that only uses brand colors, fonts, and logo assets but no named Playground component system fails.
- The Pencil source must remain editable. Never flatten the final graphic, diagram, notes, labels, cards, or connectors into one PNG/JPEG/WebP/image fill inside the `.pen`. Exports are review/publication artifacts outside the editable source, not the editable source itself.
- Use raster/image fills only for true image assets such as approved logos, product screenshots, provided photos, or explicit image placeholders. Do not use an image fill to represent editable text, cards, diagrams, annotations, or notes.
- When a prompt includes a HubSpot post target, use that exact target from the prompt for the fetch. Never hard-code a sample post ID, silently reuse the previous fetched post, or design from a generic blog topic when a real post is available.
- When a fetched HubSpot post contains `div.man-graphic-placeholder` blocks, generate one separate editable graphic per extracted placeholder prompt. Missing a placeholder, merging several placeholder prompts into one generic graphic, or letting placeholder `References:` images bypass the Playground/component registry scan is a production failure.
- Every extracted HubSpot placeholder graphic must use the full fetched article context. Read the matching `*.article-context.md` before planning, selecting components, writing the quality brief, or editing the `.pen`; a placeholder prompt without the surrounding article is incomplete.
- Every fetched HubSpot placeholder graphic must be named for article placement. The `.pen` filename and the final top-level output frame must match `{Blog Title} - {Blog Post ID} - Graphic {Number} - {Graphic Title Name}` using the real post title, post ID, top-to-bottom placeholder number, and extracted placeholder title. Preserve skipped numbers when only a subset exists, so the user knows where each graphic belongs in the blog post.
- Article context is private planning context, not visible graphic copy. Never add visible `Article context: ...`, `Reason X...`, prompt rationale, section rationale, audit notes, placeholder instructions, or explanatory footer text that states why the graphic exists. The graphic is inserted into the article in place of the placeholder, so the article supplies that explanation. Only add a caption/source note when the user explicitly asks for one or a real external source citation is required.
- HubSpot upload/placement is an explicit publication action, not an automatic part of graphic creation. Do not upload files or PATCH a post unless the user asks for it OR supplies a target HubSpot Files folder/ID. A supplied folder ID for the in-context post is itself the request and confirmation — do not re-ask folder-vs-post or re-confirm the patch. Default to the draft endpoint only; never patch or push live without a separate explicit instruction. Draft patching must use the placeholder manifest order, preserve local before/after backups, and fail on placeholder/image count mismatch unless the user explicitly approved a subset (a folder ID given for the specific in-context graphics implies an approved subset of exactly those graphics).
- HubSpot upload assets must be WebP by default: 1x export, quality 100/lossless when possible, high-quality WebP preparation for PNG/JPEG sources, SEO-friendly title-derived file names, and descriptive alt text in the replacement `<img>` markup. Do not rely on HubSpot Files API upload metadata for alt text.
- For HubSpot/RevOps/signal/CRM graphics, explicitly consider `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, and `llyux` before starting from another template or primitives.
- Never use the primary `Playground.pen` as the working canvas for a new graphic. It is the read-only component library unless the user explicitly requests a library update.
- Every prompt and every generated graphic must have its own separate `.pen` file. Reusing a prior output `.pen` for a different prompt is a production failure.
- HubSpot publication requires traceable editable sources: one unique prompt-specific `.pen` per placeholder graphic, recorded in the asset mapping as `source_pen_path`. A WebP/PNG without a matching `.pen` is not enough for normal upload/patch runs.
- Never call Pencil write operations against a non-existent target path and assume a new file was created. Confirm the actual active editor path before building, deleting, or replacing frames. Editing the active file by accident is a production failure.
- Never ignore Pencil MCP `batch_design` issues or warnings. Unsupported icons, invalid properties, missing assets, or render-affecting warnings are production failures until fixed and rechecked.
- Always scan the Playground and component registry before building. A graphic that could have used an existing mature component but was rebuilt from generic primitives fails the skill.
- Use the library creatively: preserve MAN Digital's component DNA while varying layout family, crop, logo placement, label pins, connector density, and visual rhythm to fit the prompt.
- A technically tidy but shallow diagram is still a failed design. The output needs a specific takeaway, a strong visual anchor, component/library lineage, stage-specific content, visual hierarchy, and brand presence.
- HubSpot upload requires a stricter pre-publication design audit than normal handoff. Do not upload because `snapshot_layout(problemsOnly)` is clean. Regression `l9vKx` passed layout checks but was visually weak: tiny process cards, tiny gate pills, shallow detail, and an under-audited process map. Before any HubSpot upload/patch, inspect the final frame, at least one risky close-up, and the exported WebP/PNG; if the graphic still feels primitive, cramped, tiny, or unaudited, rebuild before upload.
- Do not create large non-content brand blocks, full-height sidebars, or decorative slabs that consume useful canvas area. A brand plane larger than roughly 10-12% of the canvas must carry meaningful content, create an intentional section/lane, or be removed/reduced. A logo alone does not justify the slab.
- Repeated cards must not contain repeated placeholder copy unless the repetition is the actual point. Stage cards, department cards, and framework steps need stage-specific roles, inputs, gates, risks, metrics, or outcomes.
- Key text must be readable at the intended usage size, not only at canvas scale. For a 1536 px wide mobile-sensitive blog graphic, 20 px body labels are too small unless they are purely incidental metadata; enlarge, reduce copy, or switch layout.
- Static image reality is non-negotiable: exported graphics do not become responsive. A high-resolution PNG can still be unreadable when scaled into a mobile blog column.
- Mobile-first overrides prompt size: an in-article blog graphic must be sized and typeset for a scrolling mobile reader even when the prompt or placeholder names a specific (often landscape) size. Default to portrait `1024 x 1366` or `1080 x 1350` for any table, matrix, multi-row, multi-column, list, swimlane, or stacked-step content; reduce column count rather than shrink text; and meet the minimum type sizes in `Mobile-First Sizing`. A graphic that matches the prompt's named size but is unreadable on a 375 px phone is a production failure. See `Mobile-First Sizing` and `readability-depth-gate.md`.
- Single-word or short step/card labels must not wrap, break, or sit on two lines by accident. Regression `cV3XM` is the failure: a one-word label such as `Measurement` must stay on one line by widening the label zone, reducing copy, or using an appropriate one-line text mode before export.
- Use semantic graphic titles precisely. Do not call a scorecard, framework, report, or conceptual comparison a `dashboard` unless the visual actually depicts a dashboard UI that a reader would reasonably expect to match the source system. Use `scorecard`, `report`, `model`, `framework`, or `measurement view` when the graphic is conceptual.
- A row of plain rectangles with tiny icon-label text and no approved visual-depth system is a failed MAN Digital graphic. Use mapped Playground/design-system depth elements intentionally, such as dot grids, radar arcs, pale ellipses, background planes, label pins, medallions, screenshot frames, or logo treatments.
- Do not create unregistered background motifs such as repeated generic pale circles just because a previous graphic used them. Regression `egabQ` is the model failure. Pick from mapped Playground/Gemini/design-system/Figma decoration references (`VsypW`, `xOLUX`, `p4Dtt`, `GogdW`, dot grids, radar arcs, planes, approved decor SVGs) or use no decoration.
- Keep text inside containers with measured padding, especially pills, chips, badges, cards, callouts, frames, boxes, labels, table cells, and diagrams. Text that merely fits without breathing room fails.
- Pill/chip/badge text must be vertically centered and audited in close-up. A label sitting too low or too high inside the rounded fill is a production failure.
- Text should be structurally inside a layout frame with padding/gap when it belongs to a card, pill, badge, box, table cell, or callout. Free-floating text placed over a rectangle is a failure unless the source component intentionally requires absolute positioning and the padding has been measured.
- When a graphic compares or groups multiple topics, departments, audiences, stages, systems, statuses, or ownership areas, use restrained semantic differentiation: tints, label chips, left rails, icon medallions, borders, lanes, or section headers. Do not flatten distinct categories into identical boxes unless the concept explicitly requires sameness.
- Accent bars, pills, chips, rails, dividers, icon medallions, connector marks, and topic cues must visibly contrast with their immediate parent/background. A component part that uses the same fill as its card, lane, or canvas is invisible and fails even if the node exists in the outliner.
- Named labels, pins, context chips, logos, cards, and diagram nodes must align to explicit parent/sibling rails. A node floating a few pixels or one column off-grid is a production failure, not a preference.
- Keep flow connectors smooth, cohesive, and lane-based. Spaghetti lines, crossing connector webs, and lines touching text are production failures.
- Connector quality is a hard production gate: routes must have measured ports, aligned centerlines, smooth joins, tangent-matched arrowhead tips, proportional arrowhead scale, flush endpoint treatment at cards/surfaces, clean zoomed crops, transparent-fill open route paths when smoothed, no filled wedge artifacts, and no random/test nodes left in the frame.
- Connector tips require mandatory zoom proof. Any graphic with arrowheads, directional tips, endpoint caps, or connector markers must be audited with close-up screenshots/exports of each tip or repeated tip family. The route must stop at the arrowhead base or be intentionally hidden; a line visibly running under a triangle is a production failure.
- Connector-to-rail grazing is a production failure. Curved routes must not kiss, overlap, run parallel against, or visually merge into vertical/horizontal rails, panel borders, card edges, or other connector trunks unless there is a deliberate junction with clean geometry. Keep a visible gap or build one integrated route/junction; never leave a dark seam, doubled stroke, hooked cap, or accidental tangent collision.
- Do not solve connector/rail collisions by faking a gap with two disconnected subpaths inside one connector path. A connector like `M... m...` that renders as separate curve fragments is a production failure unless it is intentionally two named segments with a visible port/junction. Prefer one continuous leader route, a deliberate junction/notch, or separate audited connector nodes.
- Full-canvas screenshots are not enough for QA. If a graphic has small labels, arrows, callouts, or dense cards, audit the risky child nodes directly with `batch_get`, `snapshot_layout`, and close-up screenshots.
- Heading/support pairs must be measured as a pair. A heading that wraps into the support line is a hard fail even when Pencil reports no layout problems.
- Header/support stacks must be measured against the next visual zone as separate sibling geometry. A header like regression `g2Emw` can end at y=327 while panels start at y=304 and labels start at y=330; Pencil can still report no layout problems. For every header, compute the rendered bottom of the last header/support text and require at least 32 px of clear vertical gap before the first panel, card, label, screenshot, connector, or decorative visual zone that reads as the main graphic. If the gap is smaller, negative, or the screenshot shows the text merging into the visual system, move the whole visual system down or rebuild the header as a real vertical layout stack.
- Do not use Pencil `G()` groups for production build operations.
