# HubSpot Post Fetch

Use this reference when the user's prompt names a HubSpot post ID, HubSpot editor URL, public blog URL, slug, "draft post", or asks to create a graphic from the actual blog/article content.

## Purpose

Fetch the live/draft HubSpot post content before selecting a visual direction. A prompt-specific article should drive the graphic's content, not generic HubSpot assumptions or a stale cached example.

## Dynamic Target Rule

- Extract the target from the current user prompt: numeric post ID, HubSpot editor URL, public blog URL, or slug.
- Do not hard-code a post ID in this skill or in a graphic workflow.
- Do not reuse a previous fetched artifact unless its post ID/URL/slug exactly matches the current prompt.
- If multiple post targets are present, fetch all named targets or ask which one should drive the graphic if the intent is ambiguous.
- If the user says "draft", pass `--version draft`. Otherwise use `--version auto`, which tries the draft endpoint first and falls back to current.

## Fetch Tool

Preferred local fetcher:

```bash
cd /Users/romeoman/Documents/Dev/OpenClaw/openclaw-infra/blog-pipeline
PYTHONPATH=src .venv/bin/python scripts/fetch_hubspot_blog_post.py "<TARGET_FROM_PROMPT>" --version auto
```

For an explicit draft:

```bash
cd /Users/romeoman/Documents/Dev/OpenClaw/openclaw-infra/blog-pipeline
PYTHONPATH=src .venv/bin/python scripts/fetch_hubspot_blog_post.py "<TARGET_FROM_PROMPT>" --version draft
```

The script reads `HUBSPOT_ACCESS_TOKEN` or `HUBSPOT_API_KEY` from the repo-local `openclaw.json` first and then environment variables. It writes:

- `output/hubspot-fetches/hubspot-blog-post-<id>-<version>-<slug>.json`
- `output/hubspot-fetches/hubspot-blog-post-<id>-<version>-<slug>.html`
- `output/hubspot-fetches/hubspot-blog-post-<id>-<version>-<slug>.summary.md`
- `output/hubspot-fetches/hubspot-blog-post-<id>-<version>-<slug>.article-context.md`
- `output/hubspot-fetches/hubspot-blog-post-<id>-<version>-<slug>.graphic-placeholders.json`
- `output/hubspot-fetches/hubspot-blog-post-<id>-<version>-<slug>-graphic-prompts/graphic-XX-<title>.prompt.md`

## What To Extract Before Designing

Read the summary first, then read the article context file, then inspect the graphic placeholder manifest. The fetcher extracts every:

```html
<div class="man-graphic-placeholder">
```

and finds the prompt that follows:

```html
<strong>Prompt to use in Figma:</strong>
```

Use the extracted `graphics[*].prompt` values as the source prompts for the blog graphics. Do not manually hunt through the whole HTML when the manifest exists.

## Whole Article Context Rule

The extracted placeholder prompt is not standalone. It is the local brief for one graphic inside a larger article.

Before planning, selecting components, editing, or auditing any placeholder graphic:

- Read the matching `*.article-context.md` file written by the fetcher.
- Use the article title, H2/H3 outline, full article text, named objects, terminology, and surrounding argument to shape the graphic.
- Use the placeholder's `section_heading` to localize the graphic to the right part of the article, but still keep the whole post in mind.
- Use the prompt file's `Article context:` path as the required context source when delegating or batching work.
- Keep each output focused on its one placeholder; do not merge unrelated placeholder briefs just because they share one article context.

The article context is private planning context, not visible footer/caption copy. The finished graphic replaces the `div.man-graphic-placeholder` block in the article, where the prompt and surrounding prose already explain why the graphic exists. Do not render `Article context:`, the prompt-file context path, required-context instructions, prompt rationale, section rationale, `Reason X...` explanation, or internal planning notes inside the final graphic. Use context to choose content, terminology, and visual emphasis, then let the article page carry the surrounding explanation.

Then inspect the JSON/HTML enough to identify:

- Article title and slug.
- Intended section or use case from the user prompt.
- H2/H3 structure and any visible process/framework sequence.
- Named HubSpot objects, fields, dashboards, integrations, lifecycle stages, deal stages, owner/source fields, or health-score ideas.
- Any screenshot/image opportunity. If the post references a real UI/screenshot but no image is provided, use an editable placeholder and tell the user where to add or generate the screenshot.
- Candidate visual type: flywheel, process flow, data model, comparison, metric cards, maturity model, operating model, callout screenshot, or inline explainer.
- Copy constraints for a static image: reduce paragraphs into short labels; do not paste long article prose into the graphic.

## Multi-Graphic Queue

When a fetched post has `N` graphic placeholders, create `N` graphics unless the user explicitly asks for only a subset.

- If there are 2 placeholders, create 2 graphics.
- If there are 3 placeholders, create 3 graphics.
- If there are 6 placeholders, create 6 graphics.
- Each placeholder gets its own prompt-specific `.pen` file under `/Users/romeoman/Documents/Marketing/Design/Pencil/Skill Tests/`.
- Each placeholder prompt file must be paired with the same fetched `*.article-context.md`; read that context before building the prompt-specific `.pen`.
- Each `.pen` file must stay editable and must pass the full audit loop independently.
- Each finished export must record its source `.pen` path as `source_pen_path` for later HubSpot publication. If this cannot be provided, the graphic is not ready for upload/patch.
- Each final graphic must be clean replacement art for the placeholder. It should not include the placeholder prompt label, `Prompt to use in Figma:`, `Article context:`, or any meta-instruction from the fetcher.
- Do not build all placeholder graphics into one canvas unless the user explicitly requests a combined board. Even then, preserve one final export frame per graphic.
- Work in parallel only when the tool/runtime supports separate files safely. Never parallelize by writing multiple outputs into `Playground.pen` or reusing one `.pen` for multiple prompts.

If the user later asks to upload/place these finished graphics into the HubSpot post, switch to `hubspot-placeholder-publish.md` after all Pencil QA/export work is complete. Fetching and designing are read-only/creation workflows; uploading and draft patching are separate publication actions that require explicit confirmation.

## Placement Naming

For every fetched HubSpot placeholder graphic, the user must be able to identify where the output belongs in the article without opening the article or guessing from a slug.

Use this exact naming convention for both the `.pen` filename and the final top-level output frame:

```text
{Blog Title} - {Blog Post ID} - Graphic {Number} - {Graphic Title Name}
```

- `{Blog Title}` is the fetched article title.
- `{Blog Post ID}` is the exact fetched HubSpot post ID.
- `{Number}` is the placeholder's top-to-bottom order in `graphics[*]` / the article, starting at `1`.
- `{Graphic Title Name}` is the extracted placeholder title or a concise title derived from that placeholder prompt.
- If the user asks for only some graphics, preserve the original article order numbers. For example, if only placeholders 1, 2, and 5 exist as `.pen` files, they remain `Graphic 1`, `Graphic 2`, and `Graphic 5`; do not compress them to 1, 2, 3.
- Do not leave final deliverables with generic names like `skill-test`, date-only names, slug-only names, or internal prompt names.
- After renaming a `.pen`, reopen or screenshot the renamed path before handoff when possible. The deliverable name must match the file the user will actually open.

## Placeholder Prompt vs Reference Links

The prompt inside the placeholder is authoritative for content intent, but not for component source hierarchy.

- Use the extracted placeholder prompt as the brief for that graphic.
- Treat `References:` links inside the placeholder as context only. They may explain the intended visual family, but they must not override the MAN Digital design system, `Playground.pen`, or this skill's mapped component registry.
- Still run `library-scan-loop.md`, `master-template-fit-map.md`, `selection-guide.md`, `graphic-styles.md`, and relevant `references/components/` for every placeholder.
- If the placeholder prompt says "Figma", translate that into Pencil/Pencil.dev execution while preserving the design intent.
- If the placeholder prompt asks for a HubSpot UI screenshot and the post does not provide a real screenshot, create an editable UI simulation or a clearly editable screenshot placeholder. Do not flatten the prompt text or UI into a raster image.

## Failure Conditions

- Designing from generic knowledge when a fetchable post ID/URL/slug was supplied.
- Using a fixed example post ID in the skill, reference files, or future graphics.
- Fetching a post but not using article-specific terminology in the quality brief.
- Reading only `graphics[*].prompt` or a per-graphic prompt file and ignoring the fetched `*.article-context.md`.
- Ignoring `div.man-graphic-placeholder` blocks and missing one or more requested blog graphics.
- Combining all extracted prompts into one generic graphic when the post has separate placeholder prompts.
- Creating a graphic from the fetched HTML as a flattened image instead of editable Pencil text, cards, connectors, and shapes.
- Reusing old fetch output from a different post because it exists locally.
- Letting placeholder `References:` images replace the Playground/component registry scan.
- Rendering the fetched article context, prompt context path, placeholder prompt label, prompt rationale, section rationale, `Reason X...` explanation, or an `Article context:` note as visible text inside the graphic.
- Shipping fetched-post graphics with ambiguous, generic, slug-only, date-only, or renumbered filenames/top-level frame names that do not match the placement naming convention.

## Handoff Note

When reporting work, include the fetched post ID, version (`draft` or `current`), placeholder count, local summary path, and graphic-placeholder manifest path. Do not print tokens or sensitive config values.
