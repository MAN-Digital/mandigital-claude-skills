# Pencil Workflow

## Safety

`.pen` files are encrypted. Use Pencil MCP tools for inspection and editing. Do not read, parse, or modify `.pen` file contents with shell, Python, or text editors. File-level copying/renaming of a known blank seed is allowed only to create a separate output file; after copying, open the copied `.pen` in Pencil/LivePen and confirm the active editor path before any Pencil MCP write.

Use the primary Playground file as the component library only. Do not put test, proof, or finished graphic frames into the primary library. For every prompt/run/graphic, create a separate `.pen` file under:

`/Users/romeoman/Documents/Marketing/Design/Pencil/Skill Tests/`

Do not reuse a previous output file for a new prompt. One prompt equals one `.pen` file unless the user explicitly asks to continue editing that exact file.

For fetched HubSpot placeholder graphics, the output file name and top-level output frame name must use the article placement convention from `hubspot-post-fetch.md`: `{Blog Title} - {Blog Post ID} - Graphic {Number} - {Graphic Title Name}`. Use the placeholder's original top-to-bottom number from the post, even when only a subset is generated or edited.

Do not call Pencil write operations against a non-existent target `.pen` path and assume Pencil will create or switch to that file. In testing, `batch_design(filePath=...)` against a missing path edited the active document instead. Before creating, deleting, replacing, or building frames:

- Ensure the target `.pen` file exists.
- Open the target file in Pencil.app/LivePen when switching outputs. On this Mac the
  application name is `Pencil.app`, so shell open commands should use `open -a Pencil`
  with the iCloud-backed file path if the Finder-style `/Users/romeoman/Documents/...`
  path is empty.
- Call `get_editor_state` and confirm the active editor path matches the intended file.
- Only then delete seed frames or build the new graphic.
- If a copied seed file is used to make a new `.pen`, the final output must contain only the intended graphic, not copied seed content.

Treat every Pencil write response as a build log. If `batch_design` returns `issues detected`, invalid icon names, unsupported properties, missing assets, or warnings that affect rendering, fix those issues immediately and rerun the relevant audit. Do not proceed to visual QA or handoff with unresolved write warnings.

Do not leave temporary probes in any production or proof frame. If you create a node to test rendering, name it with a temporary prefix only while testing, then delete it before the next user-facing export. Production outliners must not contain `TEST`, `TMP`, `temporary`, `scratch`, `debug`, or `probe` nodes.

## Open And Inspect

1. Call `get_editor_state` with schema when available.
2. If inspecting library components, call `open_document` for:

   `/Users/romeoman/Documents/Marketing/Design/Pencil/Playground.pen`

   Use it read-only by default. For new output, create/open the prompt-specific `.pen` under `Skill Tests/` instead of the primary Playground file.

3. For component reads, pass `filePath` explicitly so the correct file is used even if the active editor reports another temporary file.
4. Use `batch_get` for exact node IDs. Use `readDepth: 2` or `3` for frames and `readDepth: 4` or deeper for icons, pills, and nested component details.
5. Use `snapshot_layout` for a compact overview and `get_screenshot` or `export_nodes` when visual verification is needed.
6. For QA, screenshot both the final frame and any risky child nodes. If a component has stacked text, callouts, arrows, or connector endpoints, inspect that component directly instead of trusting only the full-frame screenshot.
7. For selected or named text nodes, inspect the parent region too. Text collisions often happen between sibling nodes such as a heading and support line, not only inside one card.
8. For selected or named header nodes, inspect the parent and the first visual-zone siblings below the header. Compare rendered header/support bottom against panel, label, card, screenshot, connector, and diagram-background tops; `snapshot_layout(problemsOnly)` can miss these absolute sibling collisions.
9. For selected or named alignment issues, inspect the node with its parent and siblings. Measure its left/right/center rails against the panel edge, card grid, logo rail, label rail, or connector centerline before editing.
10. Before building, inspect enough of the Playground and registry to choose a component lineage. For open-ended prompts, compare at least three candidates rather than defaulting to the last-used frame.

## Build Discipline

- Copy existing mature components instead of rebuilding them from primitives.
- Use `C` operations for cloning and `U`/`R` operations for updates/replacements.
- Keep batches small, following the Gemini carousel limit of about 25 operations per batch.
- Do not use `G()` groups for production construction.
- Keep new graphics in their prompt-specific output `.pen` and name the top-level frame clearly.
- For HubSpot placeholder outputs, rename the working `.pen` and final top-level frame before handoff to the exact article-placement convention. Do not leave the user with old slug/test names.
- For HubSpot placeholder outputs, record the final `.pen` path as `source_pen_path` in the asset mapping before upload/patch. Normal placement requires one unique `.pen` source per placeholder graphic.
- If Pencil `get_screenshot` or `export_nodes` returns a blank, stale, or incomplete render while node data exists, stop and fix the file/export state. Do not patch HubSpot with a renderer-only fallback unless the user explicitly approves losing editable-source traceability.
- Confirm `get_editor_state` reports the intended output file before any destructive cleanup, seed-frame deletion, or new build operation. A correct file name in the `filePath` argument is not enough if the active editor is still another document.
- For copied/new Skill Tests files, do not rely on `batch_design(filePath=...)` alone.
  In the 2026-05-28 post-213626239140 rebuild, a write using a non-opened new file path
  resolved to the stale active editor. Required sequence: create/copy the `.pen`, open
  that exact file in Pencil.app, confirm with `get_editor_state`, then run the write
  against the confirmed active file.
- Never create new graphics in `Playground.pen` unless the user explicitly asks to update the component library.
- Preserve the source component's spacing model unless the target format requires a deliberate adaptation.
- Treat alignment as a system. If a label, pin, logo, card, or context chip is off-grid, identify the intended rail and align the related group; do not make isolated visual nudges that leave sibling nodes drifting.
- Reuse the Playground creatively. Carry forward mature component anatomy, icon treatment, cards, label pins, connectors, and spacing, but vary the composition to fit the current prompt instead of producing the same-looking graphic each time.
- For flowcharts and process-step diagrams, place cards first, reserve connector lanes, then draw connectors. Do not add lines until card positions are final.
- Use consistent connector ports and routing. Lines should look like a designed system, not manually threaded paths.
- At card/hub/surface intersections, route endpoints must be flush. In Pencil, use `stroke.cap: "none"` for stroked route endpoints that touch surfaces, or place the route behind the endpoint surface so the fill clips the line cap.
- For connector experiments, use a sandbox frame or delete every test node immediately after verification. Do not leave random arcs, arrows, shape probes, disabled experiments, or hidden scratch layers inside the final output node.
- For cards with stacked text, use enough width or height for the longest label. Do not position secondary labels where a wrapped title could collide.
- Build heading/support copy as a vertical text-stack frame when practical. If inherited absolute positioning is used, measure the rendered heading height before positioning the support line or visual zone.
- Build top headers and their following visual systems as a measured pair. Before placing the first panel, lane label, card, screenshot, connector, or visual-depth plane, compute the bottom of the final support text and reserve at least 32 px of clear gap. If later copy wraps and increases header height, move the whole visual system down as one group so rails and connectors stay aligned.
- Use logo assets from the MAN Digital design system for footer/brand marks. In Pencil, place the logo on a frame/rectangle as an image fill and screenshot the logo node when the full canvas makes it too small to inspect.

## Schema Notes

Use Pencil schema property names, not Figma or CSS names:

- `textAlign`, not `textAlignHorizontal`.
- `textGrowth`, not `textAutoResize`.
- `fontFamily`, `fontSize`, `fontWeight`, `fill`, `stroke`, `cornerRadius`.
- `fill_container` sizing is valid inside flex layouts.

Text must have visible fill, enough contrast, and no overflow. Validate buttons, pills, cards, and labels specifically.

## QA Checklist

Before finishing:

- Screenshot the output.
- Screenshot risky child components when the full output is too zoomed out to reveal text or line collisions.
- Check no text overlaps or clips.
- Check heading/support and support/visual spacing using rendered rectangles.
- Check header/support-to-visual-zone spacing using sibling rectangles, not just the header's own layout. If the support text is within 32 px of panels, lane labels, cards, connectors, screenshots, or visual-depth planes, fix before export.
- Check named/problem nodes against parent and sibling rails, not only the full screenshot.
- Check line-to-card intersections in close-up. A rounded cyan cap bleeding into a blue/white card is a production failure.
- Check logo contrast and placement.
- Check pill/chip/badge label centering in close-up when those labels are part of the graphic's logic.
- Check color usage against `brand-rules.md`.
- Check icon consistency.
- Check that dense diagrams still read at the requested output size.
- If using a copied component, confirm all old topic-specific labels were updated.
- Confirm the final design can be traced back to the selected Playground/registry candidates, and that any primitive-only sections fill real library gaps.
- Search the final output subtree for temporary names before handoff: `TEST|TMP|temporary|scratch|debug|probe`. The result must be empty.
- Confirm no disabled scratch/probe nodes remain inside the final output. Disabled source-library components are only acceptable outside the exported/proof frame.
- For HubSpot placeholder outputs, confirm the actual `.pen` path and the final top-level frame name match the fetched article title, post ID, original placeholder number, and graphic title.
- For HubSpot placeholder outputs, confirm every exported upload image has exactly one matching prompt-specific `source_pen_path`.
- Confirm the active editor path was checked before build and the final document has no leftover seed frames from copied or previous outputs.
- Confirm the last Pencil write operation produced no unresolved `issues detected` report. Unsupported icon names are not harmless; they leave missing or inconsistent icon slots.
