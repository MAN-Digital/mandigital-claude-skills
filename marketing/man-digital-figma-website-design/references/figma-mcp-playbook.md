# Figma MCP playbook for MD-Website (hard-won)

- **Exact specs:** `get_design_context` on the node (load `figma:figma-design-to-code`
  first). Do NOT trust node-NAME scans from `get_metadata` to know what a frame contains —
  names lie/vary; verify content by RENDER (`get_screenshot`). A "missing" intro that was
  actually present in the frame got a live page changed wrongly once.
- **Tall frames:** a full page frame (e.g. 360×13966) screenshotted at maxDimension caps
  renders ~68px wide — useless. Screenshot per-SECTION nodes instead; `original_width/height`
  in the response tells you when to re-request.
- **Screenshots don't upscale** beyond the node's natural size — request the node, not a
  scaled parent.
- **Exports:** `exportAsync` SVG bytes >45KB can't come back through the plugin channel.
  For images, use node screenshots as PNG (2x display size) or `download_assets`.
- **`figma.flatten` on masked groups produces solid boxes.** To crop a logo out of a
  masked composition: compute the crop from child offsets and use
  `resizeWithoutConstraints` — never flatten. Beware "light background" heuristics when
  deleting fills: light-colored GLYPHS (e.g. #EDF1F4) get eaten.
- **Raster-in-SVG:** a 2.5KB-looking logo may be a 272KB SVG wrapping a 4096px raster
  `<pattern>`. Check for `<image>`/base64 before using; extract + resize the raster instead.
- **`upload_assets`** puts external images (live-site screenshots, hubfs downloads,
  processed photos) into the file for placement.
- **use_figma** (writes: create/edit nodes, variables, auto-layout) requires loading
  `figma:figma-use` first — every time.
- **Asset acquisition:** prefer the live site's hubfs originals (public URLs, no resize
  params = original). LinkedIn photos: open the profile-photo VIEWER for the 800×800
  variant (thumbnail tokens are size-bound; sidebar avatars navigate to the WRONG
  profile — verify the licdn asset id). Extraction details: `hubspot-cms-pages` skill.
- **Figma-internal inconsistencies happen** (desktop and mobile frames disagreeing on
  copy, dot palettes differing from the approved legend). Desktop + what's shipped live
  are canonical; flag, don't silently pick.

## Vectors

- YES, real vectors are possible: `figma.createNodeFromSvg(svgString)` (via `use_figma`)
  imports an SVG string as native vector nodes — for icons, logos, decorative shapes.
  Also available: `createVector`, boolean ops, `createNodeFromSvg` + recolor via fills.
- Prefer READY-MADE first: the 🎨 Design System page, Badges & Awards page, hubfs SVGs,
  then Envato graphics; draw from scratch last.

## The designer's toolbelt (beyond Figma)

- **Mobbin MCP** (`search_screens` / `search_sections` / `search_flows`): pull real shipped
  UI patterns per SECTION — use it whenever a brief marks a section "New element" or the
  user asks for inspiration. Search by pattern name + industry ("pricing tiers b2b saas"),
  screenshot candidates, restyle the chosen pattern into MAN Digital tokens.
- **Magic Patterns MCP** (VERIFIED CONNECTED): `list_design_systems` → the active
  "MAN Digital" system `ds-f7177682-6ec6-4ce2-bc21-f46ad4e9e37a` → `get_design_system` →
  `read_design_system_files` for rules/* and component sources. It is the deduplicated
  implementation layer of this Figma file — read its rules before designing.
- **Mobbin MCP** (VERIFIED CONNECTED): returns inline section/screen images + mobbin_url.
  Curated picks live on the Design System page "Inspiration Shelf" — refresh per project.
- **Envato MCP** (`https://mcp.envato.com/mcp`, installed user-scope, VERIFIED — search
  works unauthenticated): 14 search tools —
  `search_photos`, `search_graphics`, `search_fonts`, `search_web_templates`, etc.
  Argument is `searchTerms` (not query). Returns titles/authors/preview URLs (watermarked)
  + item URLs. NO downloads via MCP — pick via preview, download licensed originals from
  elements.envato.com with the team subscription, then `upload_assets` into Figma.
  Never leave watermarked previews in final frames.
- **Real photos**: hubfs originals first (public URL without resize params), LinkedIn
  photo-viewer for people (see hubspot-cms-pages skill), Envato for stock.
- **Local image pipeline** (Bash): `sips` resize/convert, `cwebp`, Pillow `quantize` for
  flat art (85→30KB on a dot pattern), raster-extraction from fake SVGs. Resize to ~2x
  display size before `upload_assets`.

## QA gate

Every finished frame goes through `references/qa-checklist.md` — render, check tokens/type/
spacing/components against the 🎨 Design System page, fix, re-render. A frame that hasn't
been screenshot-verified is not done (the credentials-section lesson).

## Envato download pipeline (scripted — keep browser use to one click)

1. Search + preview via the Envato MCP (`search_*`, arg `searchTerms`); LOOK at the
   cover_image and run the brand critique BEFORE downloading. Banned: stock people
   photos, dated office imagery. Preferred: flat vectors, device mockups, textures
   that pass the brand rules.
2. Download needs the logged-in elements.envato.com/app.envato.com browser session:
   open the item URL, one click on Download ("Automatically licensed" toast = license
   registered). Do NOT drive multi-step UI flows — if the button needs more than one
   click + one confirmation, stop and report.
3. Organize by script (never by hand): unzip to
   `~/Documents/Marketing & Sales/Design/Assets/Envato/<asset-name>/`,
   one subfolder per asset, keep the license context in a note if provided.
4. Then `upload_assets` into Figma for placement. Never leave watermarked previews.

## Cloning gotchas (each cost a broken component)
Two more, caught by the full-page audit loop:
- **Clones collapse to 1px height** when the source's FILL sizing loses its parent
  context — set `layoutSizingVertical='FIXED'` + `resize()` to source dims after append.
- **Selector-picked clones can be the WRONG NODE** (a "CTA chip" findAll matched the hero
  paragraph). Verify every clone two ways: render it AND sanity-check node type/size
  against the source. Text collapse trap: `resize()` after setting characters kills
  autoresize height — re-set `textAutoResize='HEIGHT'` and verify height > 30 for
  paragraphs.
- **Verify token swatches programmatically** (read fills, compare to label hex) — small
  screenshots wash out saturated colors and lie.


A cloned responsive frame appended into an auto-layout wrap can get SQUEEZED and its
internal auto-layout re-wraps (1512×778 footer became 344×4234). After appending a
big clone: set `layoutSizingHorizontal = 'FIXED'` and `resize()` to the source width,
then screenshot-verify. A clone you haven't rendered is not done.


## Verified workflows (Aug 2026 session 2)

- **SVG import**: `upload_assets count=N` → one curl per submitUrl with
  `-F "file=@logo.svg;type=image/svg+xml;filename=nice-name.svg"`. Lands as an editable
  vector tree on the CURRENT page (filename = layer name). Raster + `nodeId` = sets a fill
  on that node (used for portraits/inspiration shots).
- **White-logo detection**: after building logo cards, SCREENSHOT the grid — white/faint
  brand marks vanish on white; flip those cards to #222222 with white captions. Never
  recolor the mark itself.
- **Marketplace reviews extraction** (app.hubspot.com listing): the on-page list renders
  only 2 reviews; click "See all customer reviews" (opens 5/page modal), then click the
  numbered/Next pagination harvesting `document.body.innerText` per page. Reviewer format
  is "Lastname, I." with optional industry + company-size lines before "Helpful (0)". The
  `/api/ecosystem/v1/reviews/search` POST exists but rejects guessed payloads — pagination
  harvesting is the reliable path.
- **Chapter organization**: wrap DS chapters in `figma.createSection()` nodes stacked at
  x=0 with ~200px gaps. If a chapter's content grows, RESTACK all following sections —
  section frames don't auto-flow.
- **Cross-page cloning without page-switch**: `await sourcePage.loadAsync()` (no
  setCurrentPageAsync needed), then `getNodeByIdAsync(...).clone()` and append into the
  current page. One setCurrentPageAsync per call still applies.
