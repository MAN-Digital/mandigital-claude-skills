---
name: man-digital-figma-website-design
description: Use when designing new website pages or sections, redesigning existing pages, or editing designs in the MAN Digital MD-Website Figma file (file key IOhToZi5UBH5vNFV741HP3) — service pages, landing pages, or section refreshes that must ship in BOTH desktop and mobile frames, stay consistent with the live man.digital brand and past page designs, and hand off exact specs to web development. Also use when asked to add problem/"THE PROBLEM", case-study/proof, hero, onboarding, roadmap, playbook, principles, leadership, team, credentials, form, FAQ, footer, or outcome-tab sections; their canonical aliases and desktop/mobile sources are indexed in references/canonical-page-sections.md.
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
3. **The brief owns the copy; Figma references own only the pattern.** Use source frames
   for structure, behavior, spacing, and visual treatment — never copy their headings,
   body text, labels, metrics, quotes, testimonials, or case-study details into the new
   page. Populate every section with the exact brief or other explicitly approved copy.
   If copy is missing or ambiguous, preserve an approved placeholder or stop and ask;
   never borrow content from the reference component. After target-page copy is approved,
   desktop is canonical when desktop and mobile wording disagree; mobile may shorten only
   where the approved pattern or brief explicitly allows it.
4. **Interactive patterns need STATE reference frames.** Carousels, tabs, master-detail,
   pagination: draw the states (selected tile, page 2 of N, open panel) in separate
   reference frames next to the page so development knows the behavior, not just the
   look. Content-heavy disclosure patterns must keep all content designed-in — the site
   requires it in the DOM (AEO).
5. **Present variants for structural decisions.** When adding a new kind of section
   (e.g. leadership, proof), design 2–3 labeled variants (Variant A/B/C), show renders,
   and let the owner pick before detailing. For novel patterns, pull real shipped
   inspiration from **Mobbin** first, then restyle into MAN Digital tokens.
6. **Match logo variants to background contrast.** On dark or brand-colour
   backgrounds, use the approved white/reversed logo variant. On light backgrounds,
   use the approved dark or full-colour variant. Never mix light and dark logo
   treatments within one logo row, proof strip, or section.
7. **Protect the reading-size floor.** Set website body copy, card copy, table cells,
   form guidance, and FAQ answers at **16px / 24px minimum on desktop and mobile**.
   Only compact labels, captions, metadata, and uppercase eyebrows may go below 16px.
8. **Give adjacent sections different information architectures.** Do not follow a
   stepper/master-detail section with another selector-and-detail section. Search Mobbin
   per new section, then choose a pattern that changes the reading action (for example:
   stepper -> bento capability grid -> principle rail -> proof feature). Keep every
   briefed item visible; never hide content behind a vague `+N more` summary.
9. **Use the canonical website components.** Team, form, FAQ, proof and decoration have
   approved source nodes. Clone and adapt them instead of redrawing substitutes. Read
   `references/component-canon.md` before editing those sections.
10. **Make transformation tabs explain the operating change.** For outcome or
   before/after tabs, design every state around its own revenue failure and governed
   resolution. The failure side shows its real sources outside the workflow, a broken
   handoff, and the disconnected downstream object; the governed side shows one Primary
   Blue rule/core connected directly to named revenue objects. Use critical red for the
   failure state, never CTA orange, and avoid decorative arches or abstract connectors.
   Follow the full state contract in `references/component-canon.md`.
11. **Treat component reuse as an implementation gate.** Before drawing or coding a
   recurring page section, open the canonical Desktop/Mobile chapters on the Design
   System page, locate the component, and verify its mapped HubSpot HTML, CSS and
   JavaScript source. If an implementation exists, instantiate or extend it; do not
   create parallel markup, pagination, tabs, forms, navigation or footer behavior.
   Resolve the request aliases in `references/canonical-page-sections.md` for the exact
   node and code map. "THE PROBLEM" routes to Revenue Workflows (`40000833:9074` +
   `40000836:3045`); "Case Studies"/proof routes to `40000833:9134` +
   `40000836:3082`. Node `40000836:3188` is Onboarding, not Case Studies. A registered
   pattern is clone-and-adapt, never a candidate for new structural variants.
12. **Do not improvise brand-colour roles.** Primary Blue `#000FC4` is the normal
   brand/section/active colour. Dark Navy `#161654` is restricted to approved mobile
   quote cards. CTA Orange `#F26620` is restricted to conversion actions. A source frame
   using a legacy colour does not authorize that colour in a new component.

## Workflow

0. **Read the brief.** Pages usually come with a writer's/design brief (Google Doc or
   YAML) whose content-plan table IS the wireframe: section order (binding), per-section
   format, audience, and which existing page's pattern each section reuses. Extraction
   guide: `references/brief-format.md`. No brief? Ask for one or draft the section table
   yourself and get it approved first. Do not use copy visible in a reference Figma frame
   to fill a content gap; reference-frame text is sample/source-page content, not approved
   copy for the page being designed.
1. **Survey the file first**: start at the canonical Desktop, Mobile and Interaction
   chapters on `🎨 Design System`, resolve the requested section in
   `references/canonical-page-sections.md`, then use `get_metadata` (no nodeId) to list
   pages and screenshot the latest approved frames of the page FAMILY you're designing
   for (service page, homepage, LP, nav — see the file map in the references). Work on a draft page
   ("«Page» — AI draft"); duplicate the nearest existing page/section as the starting
   point — never a blank frame.
2. Harvest: live-page screenshots for layout truth, hubfs URLs for real assets,
   `get_design_context` on existing nodes for exact specs. Upload external images with
   `upload_assets`.
3. Build desktop sections at 1512 (content column 1348), naming them "«Thing» Section".
   Instantiate the canonical component when one exists. When copy or content changes,
   override the instance or create an intentional variant; do not detach and redraw it.
4. Get approval → build the mobile frame at 360 with `m-` section names (`m-hero`,
   `m-case-studies`), applying the mobile primitives (type scale, compact CTA, omitted
   intros) from `references/design-primitives.md`.
5. Add state reference frames for anything interactive. Tabs and accordions require one
   complete desktop state and one complete mobile state for **every** tab/item that changes
   content. A process tab state always includes: stage label, title, What we do, What you
   own, and Decision gate. Name states so development can map content without guessing.
6. **QA gate — run `references/qa-checklist.md` on every frame** (tokens, type scale,
   spacing, components-not-redrawn, both breakpoints, no clipped text) and iterate until
   it passes. Screenshot-verify; a frame you haven't rendered is not done.
7. Handoff: the node specs ARE the contract — development reads them with
   `get_design_context`; make sizes/spacings deliberate, not eyeballed. The handoff must
   name the canonical component, source node, mapped HubSpot file/classes and any
   intentional divergence from the existing implementation.

**REQUIRED SUB-SKILLS:** load `figma:figma-use` before any `use_figma` call and
`figma:figma-design-to-code` before any `get_design_context` call.
Start every job at the **🎨 Design System page (40000555:2358)** in the file. Read
`references/design-primitives.md` (tokens, type scales, naming, file map),
`references/magic-patterns-tokens.md` (the FULL canonical token set — extended palette,
semantic/status tokens, shadows, motion, themes),
`references/figma-mcp-playbook.md` (tool traps + the toolbelt: Mobbin for inspiration,
Envato MCP for stock assets, vector creation, image pipeline),
`references/component-canon.md` (approved team, full form, FAQ, badge hierarchy,
interaction-state and decoration source nodes),
`references/canonical-page-sections.md` (request aliases, direct desktop/mobile sources,
atomic component shelves, Pagination and Playbooks families, Quote-to-Cash states, colour
restrictions and the Figma-to-HubSpot reuse gate),
`references/brief-format.md` (how briefs spec pages) and `references/qa-checklist.md`
(the per-frame QA gate) before touching the file.
