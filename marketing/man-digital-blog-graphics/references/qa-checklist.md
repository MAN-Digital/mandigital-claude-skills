# QA Checklist

Run this before finishing a Pencil graphic.

## Required Checks

- Run `audit-loop.md` first. This checklist is the final gate after critique and improvement rounds.
- Screenshot the final node.
- Run `snapshot_layout` on the final node with `problemsOnly: true`.
- Confirm the output format matches the requested channel.
- Confirm the graphic was created in a unique prompt-specific `.pen` file. It must not be in `Playground.pen` and must not reuse a previous prompt's output file unless the user explicitly requested continuing that exact file.
- For fetched HubSpot placeholder graphics, confirm the `.pen` filename and final top-level frame name exactly match `{Blog Title} - {Blog Post ID} - Graphic {Number} - {Graphic Title Name}`. The number must be the original top-to-bottom placeholder order from the manifest; do not renumber a subset.
- Confirm the active Pencil editor path was checked before build/destructive edits. If the target `.pen` was created from a copied seed file, confirm the final document contains only the intended output frame and no leftover seed frame/content.
- Confirm the final Pencil write responses had no unresolved `batch_design` `issues detected`, unsupported icon names, invalid properties, missing assets, or render-affecting warnings.
- Confirm `library-scan-loop.md` was run before build and during audit.
- Confirm `playground-candidate-roster.md` was run for MAN Digital blog, HubSpot, RevOps, CRM, AI, workflow, prospecting, outbound, signal, carousel-derived, or article graphics.
- Confirm the candidate pass named exact node IDs for primary layout, alternate layout family, and supporting component/depth source.
- Confirm the selected primary Playground candidate was inspected live with Pencil `batch_get` before building.
- Confirm the selected Playground/registry lineage is clear: primary template/layout, alternate considered, and supporting component system.
- For HubSpot/RevOps/signal/CRM graphics, confirm `master-template-fit-map.md` was used and each master node has a decision: `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, and `llyux`.
- Confirm `readability-depth-gate.md` was used to set source font sizes and choose a visual-depth source.
- Confirm `production-quality-floor.md` was used and the output has a specific takeaway, a strong visual anchor, library DNA, brand presence, and no shallow repeated-card construction.
- Confirm `editable-pencil-source.md` was used and the final `.pen` remains editable.
- Confirm `container-spacing-and-topic-coding.md` was used for any text inside pills, chips, badges, cards, boxes, frames, table cells, callouts, or label bars.
- Confirm the final graphic uses existing MAN Digital library components or anatomy where available, instead of generic primitive-only construction.
- Confirm the final graphic has explicit Playground lineage. Brand colors, fonts, and logo assets alone do not count as component usage.
- Confirm the graphic has an approved visual-depth lineage when needed: dot grid, radar arc, pale ellipse, background plane, label pins, medallions, screenshot shell, connector system, or logo treatment from the Playground/design-system library.
- Confirm composition efficiency: large sidebars, brand slabs, rails, color planes, and decorative blocks must carry content, define a meaningful lane, frame the main visual, or improve comprehension. A full-height logo-only brand block like regression `ZBw56` fails.
- Confirm the design is not a stale repeat of the last successful graphic; at least one meaningful dimension should be adapted to the prompt, such as layout family, crop, logo position, label/pin placement, connector density, or visual rhythm.
- For blog graphics, confirm the frame reads as a website/article asset, not a slide: no page number, slide footer, proof badge, carousel progress, or deck-only chrome unless explicitly requested.
- Confirm all old inherited copy was replaced.
- Confirm visible graphic titles use the right artifact noun. Do not title a conceptual scorecard, report, model, or framework as a `dashboard` unless the visual clearly behaves like a dashboard UI. For HubSpot-related graphics, `dashboard` implies an actual HubSpot dashboard or dashboard-like screenshot; use `scorecard`, `report`, `measurement model`, or `framework` for conceptual visuals.
- Confirm the MAN Digital logo is a real approved logo asset from the design system and is visible at the final size. Do not use typed footer text as the logo.
- Confirm the main graphic is not a flattened image. Text, notes, labels, cards, callouts, connectors, and diagram objects must be editable Pencil nodes.
- Confirm any image-filled node has a legitimate role: approved logo, product screenshot, provider badge, user-provided/generated image, or named placeholder. A pasted export of the whole design is a hard fail.
- Confirm source font sizes were inspected with `search_all_unique_properties` when available, or with `batch_get` plus `snapshot_layout(maxDepth: 3 or 4)` when that helper is not exposed by the active Pencil MCP. Key labels in a mobile-sensitive blog graphic must not rely on tiny source type; 20 px labels in a 1536 px wide output fail unless they are incidental metadata.
- Confirm the static-image mobile reality was considered. The exported graphic will scale as one image; no text, label, connector, or card can depend on responsive reflow.
- Confirm text does not clip, overlap, overflow, touch, or visually merge with neighboring text. Near-overlap is a failure.
- Confirm title/subtitle/eyebrow line heights and spacing were checked in the screenshot, not only in bounding-box layout output.
- Confirm heading/support pairs pass rendered-rectangle spacing: at least 16 px from heading bottom to support top, and at least 24 px from support bottom to the visual zone.
- Confirm the header/support stack passes a sibling-zone collision audit. Use `snapshot_layout(maxDepth: 3 or 4)` to compute the rendered bottom of the last header/support text and compare it to the top of every first visual-zone sibling below it: panels, cards, lane labels, screenshots, connectors, diagram backgrounds, and decorative planes that read as part of the main visual. Require at least 32 px of clear gap. Regression `g2Emw` failed because the header ended at y=327 while panels began at y=304 and labels at y=330, yet `snapshot_layout(problemsOnly)` reported no problems.
- Confirm risky child nodes were inspected directly when a card, pill, badge, table cell, callout, or process step contains stacked text. Whole-canvas screenshots are not enough.
- Confirm container padding was measured, not guessed. Text inside pills, chips, badges, cards, boxes, frames, table cells, callouts, and label bars must have visible left/right/top/bottom breathing room.
- Confirm pill/chip/badge labels are vertically centered by measurement and close-up proof. A status pill or label chip whose text sits high/low inside the rounded fill fails even when the full-canvas screenshot looks acceptable.
- Confirm text belongs to its container structurally. For new cards/pills/cells, text should live inside a padded layout frame instead of floating over a separate rectangle.
- Confirm `search_all_unique_properties` was checked for `padding` and `gap` when available. If unavailable, use `batch_get` on the card/pill-heavy parents and verify `padding`/`gap` or manually measured copied-component spacing. If none are present, the audit must prove the construction is copied intentionally and padding was measured manually.
- Confirm icon-plus-label pills have enough icon left padding, icon-to-text gap, and text right padding.
- Confirm at least one close-up crop was inspected for the most crowded pill/chip/badge and one representative repeated pill/chip/badge.
- Confirm long labels have either enough width for one line or enough reserved height for two lines before the next text layer starts.
- Confirm one-word and short process/card labels are intentionally one-line. If a single word like `Measurement` wraps, breaks, clips, or uses an unexpected second line, widen the label zone, shorten the wording, or rebuild the card before export. Regression `cV3XM` is the failure case.
- Confirm pills, cards, labels, and buttons are not stretched by long copy.
- Confirm every text node has a visible fill.
- Confirm Montserrat/Lato are used unless the source component intentionally differs.
- Confirm Medium Blue `#000FC4` remains the anchor color.
- Confirm orange is restrained.
- Confirm icons match the existing Streamline/lucide/material style of the base component.
- Confirm alignment and padding were measured, not just eyeballed, when the design uses tables, callouts, cards, or multiple annotations.
- Confirm every user-named or audit-named problem node was measured against its parent and sibling alignment rails. Do not pass a node because it looks acceptable in a full-canvas screenshot.
- Confirm labels, pins, context chips, logo marks, callout bars, cards, and diagram nodes align to explicit rails: parent safe area, panel edge, card grid, logo rail, label rail, or connector centerline.
- Confirm right-aligned or left-aligned nodes match their intended rail within 2 px unless there is documented optical compensation. Floating off-grid labels fail the audit.
- Confirm no callout, connector, card, icon, or decoration crosses through important text or data.
- Confirm full-frame section fit after all close-up checks. Outcome bands, footer/impact strips, brand rails, and lower content blocks must not overlap, crowd, or detach from the main graphic through excessive empty space.
- For flowcharts and process diagrams, confirm connectors follow `flow-connectors.md`: consistent ports, clear lanes, uniform color/thickness, no crossings, and no spaghetti paths.
- For flowcharts and process diagrams, confirm connector routes are production geometry: measured ports, shared centerlines where intended, smooth joins, centered arrowheads, no hollow artifacts, no accidental thickness changes, and no disabled fragment layers driving the exported result.
- For smooth connector routes, confirm open route paths use transparent fill, round joins, flush caps where they meet surfaces, and Bezier or rounded bends. In Pencil, surface-touching route endpoints should use `stroke.cap: "none"` or be layered behind the endpoint surface. Arrowheads must be separate closed/filled paths or verified visible copied icons, not filled open-path artifacts.
- Confirm connector endpoints do not bleed into cards, hubs, screenshots, logos, or panels. Zoom into each line-to-surface intersection before passing the graphic.
- Confirm every connector has a purpose. Remove lines that do not clarify flow, sequence, ownership, or handoff.
- Confirm process steps connect card-to-card or port-to-port in a cohesive order; do not connect to random card interiors.
- Confirm curves do not graze straight rails, panel borders, card edges, or connector trunks. Every close approach must either keep a clean visible gap or form an intentional tee/Y/integrated junction. Reject dark seams, doubled strokes, hooked caps, and partial overlaps.
- Confirm no connector uses disconnected subpaths to fake a rail/border gap. A path with multiple move commands for one logical connector must either be rebuilt as one continuous route, turned into separate named audited segments, or shown in a zoom crop as a deliberate port/notch. Regression `vfWSz` is the model failure.
- Confirm arrows, arrowheads, connector endpoints, elbows, and bus junctions were checked in close-up when they are part of the visual logic.
- Confirm arrowhead tips were audited as geometry, not just as visible icons: each tip lands on the intended port/gutter, each base meets the connector segment cleanly, each arrowhead points along the final segment tangent, and each arrowhead is scaled to the gap instead of reading as a blunt wedge.
- Confirm every connector tip/arrowhead/endpoint marker has zoom proof. The close-up must show the tip, base, route endpoint, final-segment tangent, and nearby background/card edge. Full-canvas screenshots do not count.
- Confirm the route does not visibly continue under a triangle arrowhead. The connector must stop at the arrowhead base, be hidden behind the marker, or be built as one integrated arrow shape. Regression `DyGGb` is the model failure.
- Confirm connector quality at both zoom levels: full graphic for reading order, and close-up crops for alignment, arrowhead fit, elbow smoothness, and line-to-card port accuracy.
- Confirm the exported close-up has no rounded-cap endpoint intrusion, filled triangles/wedges, hollow tee dots, random arcs, or stale connector fragments.
- Confirm any label bars, pins, or callouts are planned parts of the composition and do not compete with the logo placement.
- Confirm the design is not merely a row of primitive cards with tiny text. If it feels boring compared with the Playground references, revise with a mapped component or depth system before handoff.
- Confirm the design would still pass a human pre-publication critique, not only a structural audit. Regression `l9vKx` failed this gate: the node had no Pencil layout problems but looked weak because the process cards, connector labels, and operating-rule chips were too small and under-designed for a HubSpot blog graphic.
- Confirm the candidate roster result: identify the exact selected node IDs from `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, `llyux`, `S20AXj`, `l5NNCU`, `EdtGZ`, `LZkoW`, `sQ8TR`, `pAw6X`, `fKn3K`, `PPpdM`, `s2ZqRB`, `v5aVuG`, `lLDFt`, `SbBJV`, `G7EWZ`, `G6YkCq`, `nia9w`, `DJN2N`, `jNmrp`, `NhErk`, `Y3Tzyc`, `zuu8y`, `lP11x`, `HoOjV`, or explain the different inspected Playground node used.
- Confirm the design is not padded with dead brand color. If removing a large block would make the main visual larger or clearer without losing meaning, remove or shrink the block.
- Confirm no visible article-context, prompt-rationale, section-rationale, placeholder label, prompt/context path, or internal audit/planning note was added to the graphic. Regressions `bczuO` and `zshts` belong in planning notes, not in the rendered blog graphic. A HubSpot placeholder graphic replaces the placeholder block in the article, so the article provides that context.
- Confirm process/framework/stage cards do not repeat the same placeholder labels. Repeated criteria must become a matrix/checklist or be replaced with stage-specific content.
- Confirm multi-topic graphics are not blunt. If the prompt includes departments, audiences, stages, systems, statuses, or ownership areas, there must be restrained visual differentiation through tints, lanes, labels, rails, icons, borders, or grouped panels.
- Confirm every visible cue actually contrasts with its immediate background: accent bars, top bars, rails, chips, pills, dividers, icon medallions, connector marks, and label surfaces must not share the same fill as their card/lane/canvas. Regression `o204D` is the model failure: a white top accent inside a white card is invisible and does not count as a cue.
- Confirm the graphic has one clear primary visual system. If it uses many field cards plus many external callouts, simplify before export.
- Confirm a 375 px preview is readable for mobile-sensitive blog graphics; if not, reduce annotation count and text density.
- Confirm the final output subtree contains no temporary or random nodes. Search for `TEST|TMP|temporary|scratch|debug|probe`; the result must be empty before handoff.
- Confirm no temporary render experiments, disabled connector fragments, old arrows, hidden shape probes, or random leftover layers remain inside the exported/proof frame.
- Confirm the final exported WebP/PNG itself was inspected after export, not only the Pencil screenshot. Reject exports where chart bars, progress fills, labels, or cards render stacked on top of text even if the live Pencil screenshot looked acceptable.
- Confirm all critical audit findings were fixed or explicitly disclosed.

## HubSpot Placement Readiness

Run this only when the user explicitly asks to upload finished graphics or replace HubSpot placeholders.

- Confirm `hubspot-placeholder-publish.md` was used.
- Confirm every uploaded/replaced graphic has a `source_pen_path` in the asset mapping, the file exists, the file is not `Playground.pen`, and no two graphics share the same `.pen` source.
- Confirm publication does not proceed when Pencil export/screenshot returns blank, stale, or missing child layers. Fix the `.pen` source/export or get explicit user approval for a non-editable emergency fallback before using `--allow-missing-pen-source`.
- Confirm each final graphic was exported from the audited top-level Pencil frame, not from a stale screenshot or draft crop.
- Confirm the pre-upload audit includes the final top-level screenshot, a close-up of the densest/riskiest child region, and the final exported WebP/PNG. If any of those show tiny labels, weak process cards, connector-label crowding, or a shallow/generic visual, stop and rebuild before uploading. `l9vKx` is the regression case.
- Confirm the exported image count matches `placeholder_count` in the fetched `*.graphic-placeholders.json` unless the user explicitly approved a subset.
- Confirm the asset mapping uses original placeholder indexes, not a manually renumbered subset.
- Confirm upload assets are WebP, prepared/exported at 1x, quality 100/lossless when possible, and not generic PNG/JPEG leftovers.
- Confirm upload file names are SEO-friendly, title-derived, lowercase/hyphenated, and not raw node IDs or `test` names.
- Confirm the user provided a HubSpot Files `folderPath` or `folderId`.
- Confirm local original and patched `postBody` backups are written before any `PATCH`.
- Confirm the patch target is the draft endpoint, not the live endpoint.
- Confirm the replacement HTML uses clean `<figure class="man-blog-graphic">` and `<img>` markup with concise descriptive alt text, SEO title attribute, image dimensions when known, and `data-man-graphic-number`.
- Confirm no visible placeholder prompt, article context, prompt rationale, or audit note remains in the replacement markup.

## Export Readiness

- For blog graphic/article image: default export should be 1200 x 630 unless the user or CMS requires another size.
- For blog hero/OG: title must remain readable at 1200 px wide.
- For LinkedIn 4:5: title and key labels must remain readable on mobile.
- For dense explainers: reduce copy before shrinking font size.
- For carousels: preserve footer/page-number logic unless the user asks for a standalone graphic.

## Failure Modes

- If the chosen template cannot absorb the content without crowding, switch templates instead of forcing it.
- If the user asks for a component from the library but it is not formal `reusable`, copy the top-level frame by node ID.
- If a preview is stale, trust the live Pencil node and refresh previews.
- If any temporary test node is found in the final output, delete it and re-export before responding.
