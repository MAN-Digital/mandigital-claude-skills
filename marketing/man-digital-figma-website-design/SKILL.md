---
name: man-digital-figma-website-design
description: Use when designing new website pages or sections, redesigning existing pages, or editing designs in the MAN Digital MD-Website Figma file (file key IOhToZi5UBH5vNFV741HP3) — service pages, landing pages, or section refreshes that must ship in BOTH desktop and mobile frames, stay consistent with the live man.digital brand and past page designs, and hand off exact specs to web development. Also use when asked to add case-study/proof sections, hero refreshes, master-detail patterns, or when pulling assets and components from the file or the live site into a new design.
---

# MAN Digital — Figma Website Design

Design pages for www.man.digital inside the **MD-Website** Figma file
(`IOhToZi5UBH5vNFV741HP3`). The file is the design source of truth for the HubSpot site;
what you draw here becomes a dev contract, so exactness beats artistry.

## Doctrine

1. **Refresh, don't reinvent.** New designs reuse the live site's tokens, real hubfs
   assets, and the file's existing components. A from-scratch design system reads as
   AI slop and gets rejected. Screenshot the live page, harvest its real logos/photos,
   and extend what exists.
2. **Desktop first, then mobile — both are mandatory.** Build and get approval on the
   desktop frame (1512px), then derive the mobile frame (360px) from the approved
   desktop. A page without its mobile frame is not done.
3. **Desktop copy is canonical.** Mobile frames may shorten copy and omit section intro
   paragraphs by design — but when the two frames disagree on wording, desktop wins.
   Never invent copy; flag inconsistencies instead of silently changing approved text.
4. **Interactive patterns need STATE reference frames.** Carousels, tabs, master-detail,
   pagination: draw the states (selected tile, page 2 of N, open panel) in separate
   reference frames next to the page so development knows the behavior, not just the
   look. Content-heavy disclosure patterns must keep all content designed-in — the site
   requires it in the DOM (AEO).
5. **Present variants for structural decisions.** When adding a new kind of section
   (e.g. leadership, proof), design 2–3 labeled variants (Variant A/B/C), show renders,
   and let the owner pick before detailing. For novel patterns, pull real shipped
   inspiration from **Mobbin** first, then restyle into MAN Digital tokens.

## Workflow

0. **Read the brief.** Pages usually come with a writer's/design brief (Google Doc or
   YAML) whose content-plan table IS the wireframe: section order (binding), per-section
   format, audience, and which existing page's pattern each section reuses. Extraction
   guide: `references/brief-format.md`. No brief? Ask for one or draft the section table
   yourself and get it approved first.
1. **Survey the file first**: `get_metadata` (no nodeId) to list pages, then screenshot
   the latest approved frames of the page FAMILY you're designing for (service page,
   homepage, LP, nav — see the file map in the references). Work on a draft page
   ("«Page» — AI draft"); duplicate the nearest existing page/section as the starting
   point — never a blank frame.
2. Harvest: live-page screenshots for layout truth, hubfs URLs for real assets,
   `get_design_context` on existing nodes for exact specs. Upload external images with
   `upload_assets`.
3. Build desktop sections at 1512 (content column 1348), naming them "«Thing» Section".
4. Get approval → build the mobile frame at 360 with `m-` section names (`m-hero`,
   `m-case-studies`), applying the mobile primitives (type scale, compact CTA, omitted
   intros) from `references/design-primitives.md`.
5. Add state reference frames for anything interactive.
6. **QA gate — run `references/qa-checklist.md` on every frame** (tokens, type scale,
   spacing, components-not-redrawn, both breakpoints, no clipped text) and iterate until
   it passes. Screenshot-verify; a frame you haven't rendered is not done.
7. Handoff: the node specs ARE the contract — development reads them with
   `get_design_context`; make sizes/spacings deliberate, not eyeballed.

**REQUIRED SUB-SKILLS:** load `figma:figma-use` before any `use_figma` call and
`figma:figma-design-to-code` before any `get_design_context` call.
Start every job at the **🎨 Design System page (40000555:2358)** in the file. Read
`references/design-primitives.md` (tokens, type scales, naming, file map),
`references/magic-patterns-tokens.md` (the FULL canonical token set — extended palette,
semantic/status tokens, shadows, motion, themes),
`references/figma-mcp-playbook.md` (tool traps + the toolbelt: Mobbin for inspiration,
Envato MCP for stock assets, vector creation, image pipeline),
`references/brief-format.md` (how briefs spec pages) and `references/qa-checklist.md`
(the per-frame QA gate) before touching the file.
