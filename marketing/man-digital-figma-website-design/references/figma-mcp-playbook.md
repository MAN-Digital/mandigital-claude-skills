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
