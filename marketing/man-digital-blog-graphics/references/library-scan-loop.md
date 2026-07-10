# Library Scan Loop

Use this before choosing a layout and again during audit. The MAN Digital Playground and component registry are the design memory for this skill. They should make graphics consistent, faster, and more polished without making every output look identical.

## Required Loop

1. Identify the output type and visual job: blog hero, OG image, inline explainer, architecture map, flowchart, A4, slide graphic, LinkedIn post, or carousel-derived social graphic.
2. Run `playground-candidate-roster.md` and name exact node IDs for a primary layout candidate, an alternate layout family, and a supporting component/depth candidate. Do not satisfy this with generic phrases like "use the design system."
3. For HubSpot, RevOps, CRM, signal, routing, scoring, AI, revenue-engine, workflow, pipeline, or operating-model graphics, read `master-template-fit-map.md` and evaluate `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, and `llyux` before searching broader templates.
4. Search the written registry before building:
   - `component-index.md`
   - `figma-patterns.md` when a Figma reference is supplied or when tall card/pill explainer grammar fits
   - `master-template-fit-map.md`
   - `template-coverage.md`
   - `playground-candidate-roster.md`
   - `selection-guide.md`
   - `deep-dives.md`
   - `preview-manifest.md`
   - relevant files under `references/components/`
5. Search by both format and semantics. Useful terms include: `blog`, `Open Graph`, `HubSpot`, `RevOps`, `signal`, `flow`, `architecture`, `flywheel`, `process`, `timeline`, `matrix`, `scorecard`, `stack`, `callout`, `pin`, `connector`, `logo`, `decoration`, `dot-grid`, `radar`, `arc`, `ellipse`, `background plane`, `medallion`, `outside vs inside`, `sync rules`, `do not`, `outcome band`, and any topic-specific words from the prompt.
6. Inspect the live Playground with Pencil MCP before building from a selected candidate. Use `batch_get` against the chosen primary node ID, selected alternate when useful, reusable nodes, or relevant top-level frames. Do not read `.pen` files directly.
7. Compare at least three candidate sources when the prompt is open-ended:
   - one primary layout/template candidate
   - one alternate layout family
   - one supporting component candidate such as icon treatment, pill, label pin, connector system, card, visual-depth element, or logo placement
8. Pick a component lineage before building. State internally what will be reused: whole frame, card system, connector system, icon treatment, label pins, callout anatomy, screenshot treatment, logo placement, or spacing model.
9. Pick a text-scale plan from `readability-depth-gate.md` before committing to a dense layout. If the selected component would force key labels to tiny sizes, choose a larger or simpler component family.
10. Pick a production-quality-floor plan from `production-quality-floor.md`: main visual anchor, content specificity, brand presence, and how repeated stages/categories will avoid placeholder repetition.
11. Build from the selected lineage by copying components or adapting their anatomy. Only create new primitives for genuine gaps.
12. During audit, compare the finished graphic back to the selected source candidates. If the output looks generic, boring, off-brand, or weaker than the source component, revise toward the library.

## High-Value Roster Gate

For MAN Digital blog and HubSpot/RevOps graphics, these nodes are not buried examples. They are the first roster to consider:

- Signal-to-revenue/system explainers: `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, `llyux`.
- Prospecting Agent vs Outbound explainers: `S20AXj`, `l5NNCU`, `EdtGZ`, `LZkoW`, `sQ8TR`, `pAw6X`, `fKn3K`.
- Prospecting-Agent 4:5 sequence: `PPpdM`, `s2ZqRB`, `v5aVuG`, `lLDFt`, `SbBJV`, `G7EWZ`, `G6YkCq`, `nia9w`, `DJN2N`, `jNmrp`, `NhErk`, `Y3Tzyc`, `zuu8y`, `lP11x`, `HoOjV`.

If none of these are used for a blog/HubSpot/RevOps/prospecting graphic, the audit must name the different Playground node used and explain why it fit better. "Used MAN Digital design system" is not an acceptable substitute.

## Variation Rules

Consistency does not mean repetition.

- Reuse the component system, not necessarily the exact composition.
- Vary one major dimension at a time: layout family, crop, logo position, label placement, diagram density, callout count, or color emphasis.
- Keep brand constants stable: Montserrat/Lato, Medium Blue, Ghost White, cyan accent, approved logo assets, and clean B2B structure.
- Avoid overusing the same recent nodes just because they were named in the conversation. Check the full registry and Playground coverage each time.
- Avoid overusing the same decoration just because it was easy in the last graphic. Rotate among mapped depth systems when they fit: dot grids, radar arcs, planes, Gemini decorations (`VsypW`, `xOLUX`, `p4Dtt`, `GogdW`), icon medallions, screenshot shells, and clean no-decoration layouts.
- Do not force a favorite template when the prompt needs a different grammar. A data model, Lucidchart flow, flywheel, stack, matrix, and editorial cover should not all become the same card layout.
- If three candidates all feel wrong, simplify the concept or inspect more of the Playground before building from scratch.

## Audit Questions

Before final export, answer these internally:

- Which Playground or registry components shaped the design?
- Which exact node IDs were selected in the Playground candidate roster pass?
- Was the selected primary node inspected live with Pencil `batch_get` before building?
- For HubSpot/RevOps/signal/CRM prompts, how did `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, and `llyux` score in the master-template scan?
- Was the best-fit component family selected for the requested format and narrative?
- Did the build reuse mature parts such as cards, icons, pins, connector systems, screenshot frames, or logo treatments?
- Did the build include an approved visual-depth system when the composition would otherwise be a plain primitive diagram?
- Are the key labels readable in the intended output context, especially the 375 px preview for mobile-sensitive blog graphics?
- Did the design avoid becoming a generic primitive layout?
- Did the design avoid becoming a title plus repeated identical cards?
- Does each framework/process/stage card contain stage-specific information, or is the repetition intentionally structured as a matrix/checklist?
- Did the design avoid becoming a stale copy of the last successful graphic?
- Are any new primitives justified by a real gap in the library?
- Does the finished result look like it belongs to the MAN Digital library while still matching this prompt?

If the answer is weak, the audit is not complete.
