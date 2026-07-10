---
name: man-digital-marketing-assets
description: Create production-grade, editable MAN Digital marketing graphics in Pencil/Pencil.dev — LinkedIn post images, LinkedIn event covers, LinkedIn personal and company banners, Facebook ads and posts, Instagram posts, Stories/Reels, YouTube thumbnails, and Open Graph / social share images — using the local MAN Digital design system and the saved Pencil Playground component library. Use when asked to design, build, resize, or adapt a branded social or marketing asset from supplied copy, when the output must hit an exact platform size and safe zone, avoid flattened image-only canvases, and leave clearly-labeled placeholders for photos the user must add. The user supplies the copy. Not for blog/article in-body graphics or HubSpot placement (use man-digital-blog-graphics) and not for LinkedIn carousels (route to the carousel skill).
---

# MAN Digital Marketing Assets

Use this skill to build branded MAN Digital marketing and social assets in Pencil from copy
the user supplies. It reuses the **same Playground.pen component library, the same MAN Digital
design system, and the same brand rules** as the blog-graphics and carousel skills — only the
output type is different. These are standalone social/marketing assets, **not** blog in-body
graphics and **nothing to do with HubSpot**.

## Platform Note

- Read the `references/*.md` support docs with the normal file Read tool. They are plain markdown.
- Inspect and edit every `.pen` design file ONLY through the Pencil MCP tools
  (`mcp__pencil__get_editor_state`, `batch_get`, `batch_design`, `snapshot_layout`,
  `get_screenshot`, `export_nodes`, `get_variables`, `set_variables`, `get_guidelines`).
  `.pen` files are encrypted — never open them with Read, Grep, `cat`, or any raw file read.
- Call `mcp__pencil__get_editor_state(include_schema: true)` first if you do not already have
  the current `.pen` schema in this conversation.

## Scope & Inherited References

This skill was built from the MAN Digital design-system doctrine shared with
`man-digital-blog-graphics`. The `references/` folder carries that shared component library and
design discipline. **Two scope rules:**

1. **Ignore any HubSpot, blog-placement, `man-graphic-placeholder`, fetch/publish, or
   article-context instructions** found inside inherited reference files. This skill never
   fetches posts, never patches HubSpot, and never inserts graphics into an article. Those
   sections do not apply here.
2. **Asset sizing is governed by `references/asset-specs.md`, not by any blog/OG defaults in
   the inherited files.** Where an inherited file (e.g. an old output-types table) names a
   blog size, `asset-specs.md` wins.

## Routing

| Request                                                                                                                                                                                                                                                                                | Route                                                                                                                                                                                                                                                                                                 |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LinkedIn / social **carousel**, slide-by-slide deck, multi-page PDF                                                                                                                                                                                                                    | **Use the `carousel` skill** (it owns the builder/auditor flow). This skill is brand/Pencil support only. **Read `references/carousels.md` for format + the CTA-link conventions (always add the link; LinkedIn=PDF clickable, Facebook=images-only so put `www.man.digital/blog` as visible text).** |
| Blog / article **in-body** graphic, explainer inserted into a post, or any **HubSpot** placement                                                                                                                                                                                       | **Use `man-digital-blog-graphics`.**                                                                                                                                                                                                                                                                  |
| LinkedIn post image, event cover, profile/company banner, Facebook ad/post, Instagram post, Stories/Reels, **YouTube thumbnail**, **Open Graph / social share image**, **Luma (lu.ma) event cover** (square 1:1, corner-safe), or resizing an existing brand visual to a platform spec | **Use this skill.**                                                                                                                                                                                                                                                                                   |

If the user asks for a carousel, hand off to `carousel` and stop — do not build slides here.

## Source Order

When sources disagree, use this order:

1. **MAN Digital design system** — brand authority.
2. **Pencil `Playground.pen`** — component and layout authority.
3. **`references/asset-specs.md`** — canvas size, ratio, and safe-zone authority.
4. **Gemini carousel registry** — reusable component memory and build discipline.
5. **User prompt / copy** — headline, body, CTA, target channel, and final intent.

## Required Startup

1. Read `references/asset-specs.md` — confirm the exact asset type, canvas size, ratio, and safe zones **before** designing.
2. Read `references/brand-rules.md` — colors, type, logos, decoration.
3. Read `references/source-paths.md` — design-system, Playground, and output-folder paths.
4. Read `references/pencil-workflow.md` — build discipline and Pencil MCP usage.
5. Read `references/editable-pencil-source.md` — the never-flatten rule.
6. Read `references/image-placeholders.md` — how to leave photo/product placeholders and brief the user.
7. Read `references/selection-guide.md` and `references/component-index.md` — choose a Playground component lineage.
8. Read `references/style-variants.md` — **pick a style variant** (don't auto-default to solid blue); for a set, plan to mix variants.
9. Read `references/gemini-pencil-learnings.md` for social-native covers, safe zones, and footer/indicator conventions.
10. Read `references/readability-depth-gate.md` and `references/container-spacing-and-topic-coding.md` before setting text scale and placing text in pills/cards.
11. Read `references/audit-loop.md` and `references/qa-checklist.md` before finalizing.
12. Load only the relevant files under `references/components/` for the selected direction.

## Study the Live Library First (MANDATORY — do not design from memory)

Before building any asset, open `Playground.pen` and actually look. Reading reference markdown is
not enough — the real design language lives in the file.

1. **Open `Playground.pen`** (`open -a Pencil`) and confirm it is the active editor.
2. **Pull the real color variables** with `get_variables`. The MAN Digital palette is:
   Primary Blue `#000FC4`, Orange `#F26419`, Subtle Blue `#5963D9`, Ghost White `#F7F7FF`,
   MD Black `#434343`, plus light `#C8CCF2` for subtitles. **Cyan `#2DE4E6` is NOT a Playground
   variable** — do not default to cyan eyebrows/rails/dots; use Orange and Subtle Blue as accents.
3. **Screenshot 2–3 real components** that match the asset (e.g. the `dI0RZ` / `qIQkx` covers for a
   post) and absorb how they are actually composed: huge bold titles, medium-weight subtitles,
   restrained palette, one orange icon/badge, generous spacing.
4. **`batch_get` a real decoration to copy its exact values.** The signature MAN Digital
   decoration is **large soft tonal circles**, not dot-grids: e.g. an Orange `#F26419` ellipse at
   **~0.15 opacity** (~500 px, bottom-right, bleeding off-canvas) plus a soft white **glow**
   ellipse — linear gradient `#ffffff33 → #ffffff00`, rotation ~45°, **~0.2 opacity** (~900 px).
   A Subtle-Blue circle at ~0.12 works as a second tonal accent. Also available: the decor SVGs in
   `MAN Digital Design System/assets/decor/` (`circle-shadow-fade`, `ellipse-fading`,
   `etched-sphere`, `dot-mesh`, `diamond-hollow`, `circle-orange-filled`, `squiggle-yellow`,
   `chevron-orange`). Recreate the chosen decoration's editable anatomy in the output file.
5. **Typography from the real covers (reference point):** a 1080×1350 cover title is Montserrat
   **bold ~90–110 px**; the subtitle is **weight 500, ~50 px** (medium, NOT bold); gaps are
   generous (~76). **Vary weight — bold the title, keep subtitles/secondary at weight 500.** Do
   not make everything bold; over-bolding looks cheap.

## Default Workflow

1. **Identify the asset type first.** Map the request to a row in `asset-specs.md`, lock the
   canvas size, aspect ratio, and safe zones. If the asset is a carousel → route to `carousel`.
   If the user names a size that conflicts with the spec, prefer the spec unless they are explicit.
2. **Get the copy.** The user supplies the headline/body/CTA/labels. Wire their copy in
   verbatim; do not invent marketing copy. If copy is missing, ask for it before building.
3. **Plan the safe zone.** For every asset, mark the platform's crop/overlap zones from
   `asset-specs.md` (avatar overlap, duration badge, Stories/Reels reserves, OG center-66%) and
   keep all load-bearing content — headline, logo, faces, CTA — inside the safe band.
4. **Scan the Playground library and pick a component lineage (MANDATORY — do not skip).**
   Building chips, cards, pills, or decorations from raw primitives without first scanning the
   library is a failure. Steps:
   - Read `component-index.md` and `selection-guide.md`; name at least one primary layout
     candidate **and** one supporting/depth component (cover frame, eyebrow chip, card, icon
     medallion, **decoration**) by node ID.
   - For decoration/depth, pull from the registered vocabulary — dot-grids (`c1w4M`, `VsypW`,
     `tvqbC`, `VJCMg` …), radar arcs, pale planes, soft circles — read the matching
     `references/components/<id>.md`. **Never invent scattered pale circles** (the `egabQ`
     regression). If no decoration fits, use none and strengthen the layout.
   - Inspect the live candidates: **open `Playground.pen`** (`open -a Pencil`), confirm it is the
     active editor, then `batch_get` + `get_screenshot` the candidate node so you actually see it.
   - Cross-file copy is **not supported**, so recreate the component's editable anatomy in the
     output file (e.g. a dot-grid = a grid of ~2.8px ellipses at ~17.9px × ~12.8px spacing, low
     opacity), recolored to the asset's palette. Then re-open the output `.pen` to build.
5. **Pick a style variant (do not auto-default to solid blue).** From `style-variants.md`, choose
   the treatment that fits the topic/channel — Solid Blue, Blue Gradient, Dark Spotlight,
   Pill-Eyebrow/Left, Left Accent Bar, White-Cards-on-Blue, or Light/Ghost-White. State which and
   why. **For a multi-asset set, mix variants** (at least one light/gradient alongside the dark/blue
   ones); record the variant per asset so the next deliberately differs. Then set the text-scale
   plan: treat the output as a static image at its smallest real display size (a YouTube thumbnail
   shows ~168–320 px wide; a banner is read on mobile). Few, large words for covers; respect the
   feed-post type minimums; vary weight (bold title, weight-500 subtitle).
6. **Choose and OPEN the output `.pen`.** One `.pen` per asset under the Marketing Assets output
   folder (see `source-paths.md`). Never build in `Playground.pen`; never reuse a prior asset's
   file. **Pencil's `filePath` argument is unreliable — it reads/writes the _active editor_, not
   the path you pass.** So: create the file (copy a blank seed), **`open -a Pencil "<file>"`**,
   then `get_editor_state` and confirm the active editor path matches before any write. For a
   short banner (e.g. 1776×444 event cover), stack the frame with `justifyContent:"start"` and
   fixed `gap`s — `space_between` silently overflows and clips content when copy grows.
7. **Build with native, editable Pencil objects.** Text as text nodes, cards/pills/frames as
   frames, connectors as paths. Copy mature components and override copy/icons/colors. **Never
   flatten the design into a single image fill.** Raster fills are only for real image assets
   (approved logos, screenshots, user-supplied/placeholder photos).
8. **Handle missing imagery as a placeholder.** If the asset needs a photo (a person, a product
   shot) or imagery the brand library cannot supply, first check the design-system
   `assets/`/`uploads/` for an approved existing image. If none exists, build a clearly-named,
   correctly-cropped placeholder frame in the exact slot and **tell the user precisely what to
   add** (subject, crop ratio, background). Do not AI-generate a real person's likeness. Icons
   come from the Streamline-style library already in the Playground, not from stock art.
9. **Audit + critique loop (MANDATORY — never export on a single full-canvas screenshot).** Run
   `audit-loop.md`, `zoom-audit.md`, and `qa-checklist.md`:
   - First run `snapshot_layout(problemsOnly:true)` — fix any clipped/overflowing content. (A
     short banner that overflows is invisible; treat "fully clipped" content nodes as a hard fail.)
   - **OVERLAP CHECK (every time):** `snapshot_layout(problemsOnly:false)` does NOT catch text
     sitting on top of another element — absolute siblings can overlap with no reported problem.
     Compare the rendered rectangles of every text node against its neighbours and any visual zone
     (orbit/ring/circle, card, decoration). No text may touch or sit over another node. A title
     that crowds the hero visual, or a label that grazes the ring/node, is a hard fail.
   - **ALIGNMENT CHECK (every time) — align by the edge that faces the anchor, not blindly by x.**
     A label sitting BESIDE a node/icon/dot must be aligned on its _inner_ edge (the one toward the
     anchor), so the gap to the anchor is identical for every label and no glyph touches it:
     - **Labels on the LEFT of their anchor → RIGHT-align them** (`textGrowth:"fixed-width"`,
       fixed `width`, `textAlign:"right"`, positioned so the right edge sits on a shared rail a
       fixed gap left of the dots). Left-aligning them is the bug: the longest word (e.g.
       "Payments", width 177) runs into its dot while a short word ("Quoting", 145) leaves a big
       gap — their right edges (163 vs 195) don't line up and the long one overlaps.
     - **Labels on the RIGHT of their anchor → LEFT-align them** at a shared left x, a fixed gap
       right of the dots.
     - **Labels ABOVE/BELOW → center them** on the anchor's x.
     - Paired labels share a y; each label is vertically centered on its node (label-box center y
       = node center y). Eyebrow/title/subtitle/CTA share the column's left edge.
       Compute the rail from the real `width`/`x` numbers in `snapshot_layout`/`batch_get` — measure,
       don't eyeball. Confirm each label's inner edge clears its dot by the same margin.
   - `get_screenshot` the full frame, then **zoom each element separately** — header/logos,
     title, subtitle, CTA, the chip/lifecycle/orbit zone, and any decoration — and **critique each**:
     Is text legible at the smallest real size? Is every label inside its container with padding?
     Do logos render (not broken boxes)? Does decoration sit behind content, not over text?
     Does it actually look designed, or flat/primitive?
   - Fix what the critique finds by **editing the existing nodes** (`Update`/`Replace`), never by
     deleting and rebuilding from scratch, then re-screenshot and re-critique until clean.
   - Confirm the source is still editable (not a flattened image) and that the last
     `batch_design` reported no `issues detected` before trusting any screenshot.
10. **Export per spec.** Export each asset as its own file at the `asset-specs.md` format and
    size: PNG/JPG sRGB for most, **JPG ~85–90% and ≤2 MB for YouTube thumbnails**, JPG/PNG (not
    WebP) for Open Graph. The `.pen` stays editable; only the export is flattened. Hand the user
    the export path(s) plus any "add this image here" placeholder notes.

## Final Verification Gate — pass EVERY line before saying "done"

Never declare an asset finished on a glance. Go through this list explicitly, item by item, using
the actual `snapshot_layout` / `batch_get` numbers and zoomed screenshots — not vibes. If any line
fails, fix it and re-verify. Small misses (a 7px label/dot overlap, an off-rail label, the same
style as the last asset) are exactly what this gate exists to catch.

- [ ] **Size:** exported dimensions match the `asset-specs.md` row exactly (`sips`-verified), correct format/cap.
- [ ] **No clipping:** `snapshot_layout(problemsOnly)` clean for content (decoration bleed is OK).
- [ ] **No overlap:** every text node's rectangle compared to neighbours and visual zones — nothing touches/overlaps (titles clear the hero; labels clear their dots by an equal margin).
- [ ] **Alignment:** groups share rails; labels aligned by the edge facing the anchor (left labels right-aligned, right labels left-aligned, above/below centered); paired labels share a y centered on their node; eyebrow/title/subtitle/CTA on the column edge — all confirmed from real x/width numbers.
- [ ] **Type:** meets feed-post minimums; weight varied (bold title, weight-500 subtitle); legible at smallest real display size.
- [ ] **Brand:** real color variables; logos render (not broken boxes); no `MAN Digital` as plain text.
- [ ] **Logo legibility:** co-brand logos meet the minimums in `asset-specs.md` (≥44 px stacked / ≥200 px lockup at 1080-wide, scaled up on bigger canvases), comparable visual weight, wordmarks readable at mobile scale — not token-small. Zoom the header to confirm.
- [ ] **Decoration:** from the library vocabulary (soft circles + glow / dot-grid / decor SVG), behind content, never over text.
- [ ] **Style variety:** a deliberate variant from `style-variants.md` was chosen, and it differs from the previous asset in the set (light + dark both represented across a kit).
- [ ] **Editable + clean:** source not flattened; last `batch_design` had no `issues detected`; no `TEST/TMP/scratch` nodes left.
- [ ] **Zoomed each element** (header, title, subtitle, CTA, hero/orbit, decoration) and critiqued each — it looks designed, not primitive.

Only when every box is checked do you export-and-report. State that the gate passed.

## Output & Naming

- One `.pen` per asset in the Marketing Assets output folder (see `source-paths.md`).
- Name the `.pen` and the top-level frame for the asset, e.g.
  `MAN Digital - LinkedIn Event Cover - {Topic}` or `MAN Digital - YouTube Thumbnail - {Topic}`.
- Build at 1× the spec, or design large at the same ratio (e.g. company cover at 4200 × 700)
  when crispness against heavy crop matters; export to the exact spec size.

## Format Defaults

Defer to `references/asset-specs.md` for every dimension and safe zone. When the user does not
specify orientation: LinkedIn/Facebook/Instagram single posts default to **1080 × 1350 (4:5
portrait)**; YouTube thumbnails **1280 × 720**; Open Graph **1200 × 630**; Stories/Reels
**1080 × 1920**; **Luma (lu.ma) event cover 1080 × 1080 (square, corner-safe, minimal text)**.
LinkedIn event cover **1920 × 1080 (16:9)**, personal banner **1584 × 396**, company cover **1128 × 191**.

## Mobile-First Reality

Social assets are mostly consumed on phones, and exported images do not become responsive.

- **Feed posts (LinkedIn / Facebook / Instagram, 1080×1080 / 1080×1350) need BIG, BOLD text.**
  A 1080 image renders ~390 px wide on a phone (~0.36×), so small/thin type vanishes. Follow the
  **Feed-Post Type Minimums** table in `asset-specs.md` — titles **≥ 56 px (700–800)**, supporting
  lines **≥ 34 px (weight 500–600)**, in-graphic labels **≥ 30 px**, CTA **≥ 26 px**; **hard floor
  30 px** for any meaning-bearing text. A thin 22 px subtitle on a feed post is a failure.
- **Vary weight — don't bold everything.** Bold (700–800) the title only; keep subtitles and
  secondary copy at **weight 500** (the real covers use 500/50 px subtitles). Over-bolding looks
  cheap. Solve small/weak text by making it _bigger_, not by bolding everything.
- **Logos are type too — size them for mobile.** A co-brand logo's wordmark downscales ~0.36× on a
  phone just like text. Don't size logos as tokens: ≥44 px tall (stacked mark) / ≥200 px wide
  (one-line lockup) at 1080-wide, scaled up on bigger canvases (~70 px / ~280 px on a 1920 cover).
  Keep both co-brand marks at comparable visual weight and zoom the header to confirm legibility.
- Keep load-bearing copy large and high-contrast; a cover or thumbnail must read at thumbnail size.
- Respect the platform safe zones in `asset-specs.md` — design around the avatar overlap,
  duration badge, and Stories/Reels UI reserves rather than hoping they won't crop.
- Reduce words before shrinking type. Covers and thumbnails win with 3–6 words, not sentences.

## Non-Negotiables

- **Confirm the asset type and lock the `asset-specs.md` size + safe zones before building.**
  Guessing a platform size is the most common failure, and platforms change specs (e.g. the
  LinkedIn event cover is now **16:9 / 1920 × 1080**, not the old 4:1). When the user shows a
  current platform upload dialog/spec, trust it over the table and update the spec. Verify every time.
- **Carousels route to the `carousel` skill.** Do not build slide decks or multi-page PDFs here.
- **No HubSpot, no blog-body placement.** This skill produces standalone exported assets.
- Use **Montserrat** for headings and **Lato** for body unless a source component defines otherwise.
- **Use the Playground's real color variables** (`get_variables`): Primary Blue `#000FC4`
  (anchor), Orange `#F26419` (accent/CTA), Subtle Blue `#5963D9`, Ghost White `#F7F7FF`,
  MD Black `#434343`, light `#C8CCF2` (subtitles). **Cyan `#2DE4E6` is not a Playground variable
  — do not default to cyan** eyebrows/rails/dots; use Orange and Subtle Blue as accents.
- **Vary the style — never ship the same look every time.** Pick a treatment from
  `style-variants.md` (Solid Blue, Blue Gradient, Dark Spotlight, Pill-Eyebrow/Left, Left Accent
  Bar, White-Cards-on-Blue, Light/Ghost-White). Across a multi-asset set, **mix variants** — light
  AND dark must both appear; don't render seven copies of one solid-blue centered layout. Keep the
  brand system constant (fonts, logo, accent palette), vary background + layout + eyebrow + decoration.
- **Decoration = large soft tonal circles, the library way.** Recreate the real cover decoration:
  an Orange `#F26419` ellipse at ~0.15 opacity + a soft white glow gradient ellipse at ~0.2,
  bottom-right and bleeding off-canvas; optionally a Subtle-Blue circle at ~0.12. Or use the decor
  SVGs in `assets/decor/`. Never default to cyan dot-grids or invented scattered pale circles.
- **Scan the Playground library before building, every time.** Use Playground components first —
  cover frames, eyebrow chips, cards, pills, icons, and the registered **decoration** vocabulary
  (dot-grids, soft circles, radar arcs, planes). Open `Playground.pen` and inspect candidates;
  recreate their editable anatomy when cross-file copy isn't possible. A graphic built from raw
  primitives that skips the library scan fails — even if it looks fine. Never invent scattered
  pale-circle decorations (`egabQ`).
- **Always run the audit + critique loop before export.** `snapshot_layout(problemsOnly)` →
  full screenshot → zoom and critique each element (logos, title, CTA, chips, decoration) → fix
  by editing existing nodes → re-audit. A single full-canvas screenshot is never sufficient proof.
- **Every audit checks text OVERLAP and ALIGNMENT explicitly.** No text may sit on or touch
  another node (titles must not crowd the hero visual; labels must not graze a ring/node/card) —
  absolute siblings overlap without any reported layout problem, so compare rendered rectangles.
  And anything that reads as a group must share rails: left labels one left x, right labels one
  right rail, paired labels one y, each label vertically centered on its node, and
  eyebrow/title/subtitle/CTA on the column's left edge. Set off-rail nodes to the exact same
  coordinate from `batch_get`/`snapshot_layout` numbers — never eyeball alignment.
- The Pencil source must stay **editable**. Never flatten the asset, text, cards, or
  decorations into one image. Raster fills only for true image assets and placeholders.
- **Never AI-generate a real person's likeness.** Leave a labeled photo placeholder and tell
  the user exactly what to supply.
- Use approved **logo assets** from the design system for brand marks; never type `MAN Digital`
  as plain text in a finished asset.
- Respect each platform's **file format and size cap** from `asset-specs.md` — especially the
  YouTube **2 MB hard cap** (export JPG ~85–90%) and the Open Graph **no-WebP** rule.
- One `.pen` per asset; never build in `Playground.pen`; confirm the active editor before writing.
- Never ignore Pencil `batch_design` `issues detected` / missing-icon / invalid-property
  warnings. A clean screenshot is not proof when the tool reported a build issue.
