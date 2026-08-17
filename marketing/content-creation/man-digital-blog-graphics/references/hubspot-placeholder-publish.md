# HubSpot Placeholder Publish

Use this reference only after the graphics are finished, audited, exported, and the user explicitly asks to upload them or replace HubSpot placeholders.

## Purpose

Upload finished exported graphics to HubSpot Files and replace the matching `div.man-graphic-placeholder` blocks in the HubSpot blog draft. This is a publication/update workflow, not a design workflow.

If the draft has already been patched before, the original placeholders may no longer exist. In that case, replace the existing `<figure class="man-blog-graphic" data-man-graphic-number="...">` blocks by `data-man-graphic-number` instead of trying to rediscover the old prompts or renumbering the graphics.

## Safety Defaults

- Patch the draft only by default. Never update the live blog post or push a draft live unless the user explicitly asks for that separate action.
- Require explicit user confirmation before any `PATCH` to HubSpot.
- Create local backups of the original `postBody`, patched `postBody`, and upload manifest before patching.
- Never hard-code a post ID, folder path, image path, or token in the skill.
- Read tokens from the same HubSpot token sources used by the OpenClaw blog pipeline: repo-local `openclaw.json` or environment variables. Never print tokens.
- If the placeholder count and exported graphic count do not match, stop. Do not guess.
- If using a subset, require explicit user instruction and preserve the original placeholder numbers.
- If replacing an existing subset of published/draft figures, match by `data-man-graphic-number`, not by current visual order alone. This preserves Graphic 4 and Graphic 6 placement when only those graphics are being corrected.
- Do not replace the final editable `.pen` source with uploaded images. HubSpot receives exported PNG/WebP/JPEG assets; Pencil deliverables remain editable source files.
- For HubSpot upload assets, WebP is required by default. Export Pencil frames as 1x WebP with quality 100/lossless when possible; if the source export is PNG/JPEG, prepare a lossless WebP copy before upload.
- Use SEO-friendly file names/titles derived from the graphic title. Do not upload generic names like `FyExL.png`, `image.png`, `test.webp`, or raw node IDs.
- HubSpot Files API upload options do not carry image alt text for blog rendering. Put alt text in the replacement `<img alt="...">` markup and store the SEO title in the file name plus image `title` attribute.

## Folder ID Convention (Default Publish Behavior)

When the user supplies a HubSpot Files folder ID (a numeric ID, e.g. "add it to folder 214142018977") for graphics that were just fetched/built in this session, treat that as a complete publish instruction. Do not ask the user to disambiguate folder-vs-post or to re-confirm the patch. A human normally gives the folder ID and expects you to know the rest.

Default interpretation when a folder ID is given:

- Upload target: the supplied Files folder ID.
- Patch target: the DRAFT of the in-context post — the HubSpot post fetched and whose placeholder graphics were built in this session.
- Scope: replace the placeholder(s) for the graphic(s) already produced, matched by `display_number` / `data-man-graphic-number`. Leave all other `div.man-graphic-placeholder` blocks and their prompts untouched. The only thing removed is the Figma-prompt placeholder block being replaced.
- The folder ID itself is the user's request and confirmation. Proceed with upload + draft patch. Always write the local before/after `postBody` backups first.

Still draft-only and safe (do not weaken these):

- Patch the draft endpoint only. Never patch or push live unless the user gives a separate explicit live instruction.
- Keep all other safety defaults: count-mismatch stop, `source_pen_path` traceability, WebP, SEO file names, backups, no deletion of any non-placeholder article content.

Only ask a clarifying question when the situation is genuinely ambiguous:

- No in-context fetched post exists, so there is no post to patch.
- Two or more fetched posts are plausible targets and the user did not say which.
- The user asks to publish live, delete non-placeholder content, or replace a different post than the one in context.

Resolving "is this number a folder or a post?": the in-context fetched post is the patch target; the newly supplied number is the Files folder. If only one number is ever provided and no post is in context, then ask.

## Required Inputs

Before replacing placeholders, collect:

- HubSpot post ID, editor URL, public URL, or slug.
- Target HubSpot Files folder path or folder ID.
- Exported image file for each placeholder.
- Source `.pen` file for each placeholder graphic. This must be a real prompt-specific editable Pencil file, not `Playground.pen`, not one shared multi-graphic file, and not a publication-only renderer artifact.
- Graphic order mapping, normally from `*.graphic-placeholders.json`.
- Alt text for each image, derived from the graphic title and article section unless the user provides better alt text.
- SEO title/file name for each image, derived from the graphic title unless the user provides better naming.
- Explicit confirmation to patch the draft.

## API Contract

Use current HubSpot APIs:

- Upload each asset with Files API: `POST /files/v3/files`.
- Patch only the draft blog body with CMS Blog Posts API: `PATCH /cms/blogs/2026-03/posts/{postId}/draft` with `{"postBody": "<updated html>"}`.
- If the account or existing local tooling still uses legacy CMS v3 paths, the equivalent draft endpoint is `/cms/v3/blogs/posts/{postId}/draft`; prefer the date-versioned endpoint first and fall back only when needed.

## Export And Upload Flow

1. Export each final top-level Pencil frame with `export_nodes`.
2. Export or prepare upload files as WebP:
   - Preferred Pencil export: `format: "webp"`, `scale: 1`, `quality: 100`.
   - Treat WebP quality 100 as the high-quality/lossless publication target for this workflow.
   - If only PNG/JPEG exists, run the helper with default `--prepare-webp --webp-lossless --webp-quality 100`; it writes SEO-named WebP assets under the publish output folder before upload.

3. Name upload files using SEO-friendly, title-derived names:

   ```text
   graphic-01-{graphic-title-name}.webp
   ```

   Keep the local `.pen` filename in the placement convention, but make uploaded image file names short, descriptive, lowercase, and hyphenated.

4. Build an asset mapping JSON:

   ```json
   {
     "graphics": [
       {
         "index": 1,
         "display_number": 1,
         "image_path": "/absolute/path/graphic-1.webp",
         "source_pen_path": "/Users/romeoman/Documents/Marketing/Design/Pencil/Skill Tests/Blog Title - 123 - Graphic 1 - GTM Handoff Before AI.pen",
         "title": "GTM Handoff Before AI",
         "alt": "GTM process map showing Marketing, Sales, and Customer Success handoffs",
         "width": 1536,
         "height": 1024
       }
     ]
   }
   ```

5. Use the helper script when possible:

   ```bash
   cd /Users/romeoman/Documents/Dev/OpenClaw/openclaw-infra/blog-pipeline
   PYTHONPATH=src .venv/bin/python \
     /Users/romeoman/.codex/skills/man-digital-blog-graphics/scripts/hubspot_placeholder_publish.py \
     --post-id "<POST_ID>" \
     --manifest "output/hubspot-fetches/<POST>.graphic-placeholders.json" \
     --assets-json "/absolute/path/assets.json" \
     --folder-path "/MAN Digital/blog-graphics/<POST_ID>" \
     --prepare-webp \
     --webp-lossless \
     --webp-quality 100 \
     --upload \
     --patch-draft
   ```

   By default, the helper refuses `--upload` or `--patch-draft` when any asset lacks `source_pen_path`, when two graphics point to the same `.pen`, when the source path is `Playground.pen`, or when the `.pen` filename does not include the preserved graphic number. This prevents publication-only images from becoming untraceable blog assets.

   `--allow-missing-pen-source` is an emergency override only. Use it only when the user explicitly approves a non-editable publication fallback, and state the limitation in the handoff. Do not use it to work around Pencil file hygiene problems silently.

6. Review the output paths, prepared WebP assets, file sizes, and returned HubSpot file URLs.

## Replacement Markup

Replace each placeholder with clean image markup. Include metadata attributes so reruns are auditable:

```html
<figure
  class="man-blog-graphic"
  data-man-graphic-number="1"
  data-hubspot-file-id="123456"
>
  <img
    src="https://..."
    alt="..."
    title="..."
    loading="lazy"
    decoding="async"
    width="1536"
    height="1024"
  />
</figure>
```

Use the `graphics[*].index` order from the placeholder manifest. The first `div.man-graphic-placeholder` maps to `Graphic 1`, the second maps to `Graphic 2`, and so on.

When a draft has already had earlier placeholders replaced and only a subset of `div.man-graphic-placeholder` blocks remains, keep two numbers separate:

- `index`: the position among the currently remaining placeholder blocks, starting at 1.
- `display_number`: the original article graphic number used for `data-man-graphic-number` and SEO filenames, such as `graphic-02-...webp`.

Example: if Graphic 1 is already replaced and the next remaining placeholder is original Graphic 2, use `"index": 1, "display_number": 2`.

When no `div.man-graphic-placeholder` blocks remain because the draft contains existing blog graphic figures, use the same asset mapping but replace only the figures whose `data-man-graphic-number` equals `display_number`. Do not replace all figures in order unless the asset count equals the full figure count and that is the explicit requested operation.

## Pre-Patch Checklist

- The draft post was fetched fresh, not reused from stale local HTML.
- The manifest `placeholder_count` equals the number of exported images unless the user explicitly requested a subset.
- For already-patched drafts, the existing figure count may be larger than the replacement subset. Verify that every replacement asset maps to an existing `data-man-graphic-number`, and after patching verify those figure numbers contain the new HubSpot file IDs while the other figures remain present.
- Each image was audited and exported from the correct final Pencil frame.
- Each image maps to a real prompt-specific `source_pen_path` and that `.pen` file exists.
- For fetched HubSpot placeholder graphics, each `source_pen_path` filename and final top-level frame follow `{Blog Title} - {Blog Post ID} - Graphic {Number} - {Graphic Title Name}`.
- The exported image was produced from the matching `.pen` frame. If Pencil screenshot/export returns blank, stale, or incomplete content, stop and fix the Pencil source/export path before upload. Do not silently replace it with an untraceable renderer-only image.
- The graphic passed a real pre-publication visual audit, not just `snapshot_layout(problemsOnly)`. Before upload, inspect the full frame, a close-up of the riskiest/densest child region, and the exported WebP/PNG. Stop on tiny gate labels, cramped cards, weak process-map structure, shallow generic layouts, or any issue a reader would notice in the blog. Regression `l9vKx` is the failure case.
- No graphic shares a `.pen` source with another placeholder unless the user explicitly asked for a single multi-frame Pencil file; normal HubSpot placeholder runs require one `.pen` per graphic.
- Each upload asset is WebP, exported/prepared at 1x, lossless/high-quality, and SEO-named from the graphic title.
- Each file upload returned a usable HubSpot URL.
- Each alt text is concise and describes the image, not the internal prompt.
- Each replacement `<img>` includes alt text and a title derived from the image title.
- The new HTML contains no `Prompt to use in Figma:`, `Article context:`, prompt rationale, or internal audit copy.
- The local backup files exist before patching.
- The patch target is the draft endpoint, not the live endpoint.

## Failure Conditions

- Patching without explicit user confirmation.
- Patching live content or pushing draft changes live when the user only asked to place graphics.
- Uploading assets into an unknown/default/root folder when the user gave a folder path or folder ID.
- Uploading PNG/JPEG exports when WebP preparation is available.
- Uploading raw node-ID/test filenames instead of SEO-friendly title-derived filenames.
- Replacing placeholders by text search alone when nested placeholder HTML could cause a partial replacement.
- Reordering graphics manually instead of using the manifest order.
- Replacing fewer or more placeholders than expected without explicit subset approval.
- Uploading or patching graphics that do not have a traceable editable `.pen` source per placeholder.
- Using a publication-only render fallback after Pencil export failed without explicit user approval and a handoff limitation.
- Losing the original `postBody` backup.
- Using visible prompt text as image alt text.
- Assuming HubSpot Files API metadata sets blog-image alt text. The alt text must be in the `<img>` tag that replaces the placeholder.

## Published-Post Republish And CDN Cache

This matters whenever the in-context post is already `PUBLISHED` (not a never-published draft). Learned from post `213989842831` on 2026-06-02.

Two distinct states exist and must not be confused:

- **Published record** — the post object returned by `GET /cms/v3/blogs/posts/{id}`. This is the source of truth for "is the content published."
- **Rendered public page** — the HTML served at the public URL. HubSpot serves a **prerendered** copy through a Cloudflare edge cache (`x-hs-prerendered: <timestamp>`, `x-hs-cf-cache-status: HIT`, `resolver: PreRenderedContentResolver`, `s-maxage` often 36000 = 10h).

Key failure mode: for an already-published post, patching `/{id}/draft` then `POST /{id}/draft/push-live` (HTTP 204) **updates the published record but does not reliably purge the prerender/edge cache**. The public URL keeps serving the old prerender (its `x-hs-prerendered` timestamp stays frozen at the pre-edit time), so the change looks invisible even though it is genuinely published. Do not conclude "the graphic was not added" — distinguish the record from the cached render.

Required workflow for a published post:

1. Make edits to the draft and `push-live` (or PATCH the published `/{id}` endpoint directly).
2. **Verify against the published record**, not the public page: `GET /cms/v3/blogs/posts/{id}` and confirm the new markup is in `postBody`. That is the authoritative success check.
3. **Verify the public render separately** with a cache-busted request and inspect headers: `x-hs-prerendered` should advance to the new publish time and `x-hs-cf-cache-status` should eventually `MISS`/refresh. If `x-hs-prerendered` is still the old timestamp, the page is cache-stale, not unpublished.
4. **To force the public page to refresh**, a UI publish is the reliable trigger: in HubSpot open the post → **Update/Publish** (or **Actions → Clear cache**), which purges the `edge-cache-tag: CT-{postId}` and re-prerenders. An API `push-live` alone may not fire this. Otherwise the edge cache self-expires at its `s-maxage` TTL.

Reporting rule: when the published record contains the change but the public page is still cached, say exactly that — "published in the record; public render is CDN-cache-stale, force a re-publish/clear-cache in the HubSpot UI to see it immediately." Never report a cache lag as a failed insert, and never silently re-patch trying to fix a caching artifact.

## Handoff Note

When reporting a publish/patch run, include:

- Post ID and whether draft was patched.
- HubSpot folder path or folder ID.
- Number of placeholders found and replaced.
- Local backup path.
- Upload manifest path.
- Any skipped placeholders or remaining manual tasks.

Do not include access tokens or private config values.
