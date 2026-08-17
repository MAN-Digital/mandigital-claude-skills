# Editable Pencil Source

Use this before building and during audit. The `.pen` file is the editable source of truth. The user must be able to edit text, notes, cards, callouts, labels, connectors, and diagram objects after the design is delivered.

## Core Rule

Do not create a final design by exporting a PNG/JPEG/WebP/PDF and inserting that image back into the Pencil canvas. Do not flatten the whole graphic or major editable sections into an image fill.

Build the production frame with native Pencil objects:

- text as `text` nodes;
- cards, pills, badges, callouts, boxes, table cells, and panels as `frame`, `rectangle`, or component/ref nodes;
- connectors and arrows as paths/shapes/icons that can be edited;
- labels, notes, annotations, and stage names as text inside editable frames;
- decorative elements as editable shapes, paths, or copied library components where possible.

## Allowed Raster/Image Uses

Raster or image fills are allowed only when the content is inherently an image asset:

- approved MAN Digital logo files;
- approved HubSpot/provider logos or badges;
- product screenshots, CRM screenshots, or UI screenshots;
- user-provided photos or generated imagery explicitly requested by the user;
- placeholder frames for future screenshots/images.

Even then, surrounding labels, callouts, annotations, arrows, captions, notes, cards, and explanatory text must stay editable Pencil nodes.

## Export Boundary

`get_screenshot` and `export_nodes` are audit/publication tools. They are not a build method.

Allowed:

- export a PNG to inspect mobile readability;
- export the final frame for publication after the `.pen` source is complete;
- use preview PNGs only for visual routing and template selection.

Not allowed:

- export the design and paste the exported bitmap into the same `.pen` as the final deliverable;
- use an image of a diagram instead of editable diagram nodes;
- use an image of text/notes to avoid layout work;
- replace a copied Playground component with a screenshot of that component;
- leave the user with only a flat image when the underlying design should be editable.

## HubSpot Publication Traceability

For fetched HubSpot placeholder graphics, every placeholder graphic must have its own source `.pen` file before upload or CMS patching.

Required:

- one prompt-specific `.pen` per placeholder graphic;
- `.pen` filename and final top-level frame follow `{Blog Title} - {Blog Post ID} - Graphic {Number} - {Graphic Title Name}`;
- exported WebP/PNG/JPEG is generated from that matching audited frame;
- asset mapping includes `source_pen_path` for every uploaded/replaced image.

Hard fail: Pencil screenshot/export renders blank, stale, missing child layers, or the wrong frame. Stop and fix the Pencil source/export state. Do not silently create a renderer-only WebP and patch HubSpot, because the user loses traceability and editability.

Emergency fallback is allowed only after explicit user approval, and the handoff must state that the published asset has no editable `.pen` source. This should not be used for normal skill tests or production blog graphics.

## Audit Checks

Before handoff:

1. Inspect the final output subtree for large image-filled rectangles or frames that cover most of the canvas.
2. Confirm key text exists as text nodes, not pixels inside an image.
3. Confirm notes/labels/callouts are editable nodes.
4. Confirm cards, pills, connectors, and diagram pieces can be selected and edited separately.
5. Confirm any image node has a legitimate reason: logo, screenshot, approved photo/generated image, or placeholder.

Hard fail: a final frame whose main content is one large image node, with no editable text/card/connector structure underneath.

## Placeholder Rule

If an image is needed but not available, leave a clearly named placeholder frame. Tell the user what belongs there. Do not generate or insert a flattened stand-in unless the user explicitly asks for generated imagery.

Example:

`Right screenshot placeholder: add an approved HubSpot data-model screenshot here before publication.`
