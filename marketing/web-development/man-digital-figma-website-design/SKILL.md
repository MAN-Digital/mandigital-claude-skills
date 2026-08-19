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
6. **Match logo variants to background contrast.** On dark or brand-colour
   backgrounds, use the approved white/reversed logo variant. On light backgrounds,
   use the approved dark or full-colour variant. Never mix light and dark logo
   treatments within one logo row, proof strip, or section.
7. **Protect the reading-size floor.** Set website body copy, card copy, table cells,
   form guidance, and FAQ answers at **16px / 24px minimum on desktop and mobile**.
   Only compact labels, captions, metadata, and uppercase eyebrows may go below 16px.
   On service and landing pages, every section eyebrow uses **Lato Bold 13px / 18px
   on desktop and 11px / 16px on mobile**, uppercase with **2px tracking**. Reuse this
   token for ARC and other section pre-headings; never enlarge it into lead or heading
   scale. The approved hero pre-heading is a separate, hero-specific treatment.
   A canonical component with legacy 15px desktop or 14px mobile reading text is not an
   exception: correct the source or apply an explicit 16/24 override before reuse.
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
   Read `references/canonical-page-sections.md` for the exact node and code map.
12. **Do not improvise brand-colour roles.** Primary Blue `#000FC4` is the normal
   brand/section/active colour. Dark Navy `#161654` is restricted to approved mobile
   quote cards. CTA Orange `#F26620` is restricted to conversion actions. A source frame
   using a legacy colour does not authorize that colour in a new component.
13. **Use ARC for the MAN Digital method.** When a page explains how MAN Digital
   approaches, delivers, or improves revenue work, use the canonical ARC framework:
   **Architect → Run → Compound**. These phase names are fixed: never substitute
   `Realise` or `Build` for `Run`. Instantiate the approved Desktop
   `40000833:9341` and Mobile `40000836:3236` components, then replace their example
   copy with brief-owned content. Preserve the three-phase structure, numbers, taxonomy
   labels, colour-coded bullets, desktop legend, and mobile stack. Do not replace ARC
   with a one-off method diagram, generic process cards, or an unrelated roadmap. ARC
   action rows are Lato Regular **16px / 24px at both breakpoints** and fill the available
   cell width; only phase numbers, taxonomy labels, and the desktop legend may be smaller.
   Its `HOW WE WORK` eyebrow inherits the canonical service-page eyebrow token: Lato
   Bold **13px / 18px desktop and 11px / 16px mobile**, uppercase with 2px tracking.
   On desktop, group the three actions with zero inter-row gap and give every bounded
   cell equal **24px top and bottom padding**. Use one divider above the action region
   and dividers between action rows; never add a closing divider after the final action
   because the card border already closes the group. Never fake bottom padding with
   parent spacing. Apply the full acceptance contract in
   `references/component-canon.md#arc-component-contract`.
14. **Use Onboarding for an implementation sequence.** When a service page explains
   how a project runs, instantiate the canonical Onboarding family rather than drawing
   process tabs, a master-detail panel or another ARC section. Use Standard Desktop
   `40000833:9279` / Mobile `40000836:3188` for concise steps and Detailed Desktop
   `40001088:3017` / Mobile `40001088:3144` when every stage must show delivery work,
   client responsibility and a decision gate. Keep all stages visible: five equal
   timeline columns on desktop and the same five cards stacked on mobile. Never shorten
   approved copy to fit a fixed card; grow the canonical variant at the source. Page
   instances stay attached and implementation extends `sections/05-onboarding.html`
   and `.rv-onboarding` instead of creating a parallel module. Apply the full contract
   in `references/component-canon.md#implementation--onboarding-contract`. Detailed
   Desktop uses 12px stage dots centred on a 2px rule that begins and ends at the first
   and last dot centres. Detailed Desktop and Mobile use transparent 16×24 check slots
   aligned to the first 24px text line, with one rounded 2px check path inside.
15. **Use the canonical Service Scope Disclosure for grouped capability scope.**
   Instantiate Desktop set `40001115:3242` or Mobile set `40001115:3473` from Design
   System chapter `40001114:3012`; the complete behavior and content rules live in
   `40001114:3029`. Keep exactly five ordered groups, one open group at a time, every
   brief-owned capability designed into its state, and page uses attached as instances.
   Use title text at 18/24 and capability text at the 16/24 reading floor. Do not add
   package language, counts, pills, tiers, `+N more`, Dark Navy, or CTA Orange. These
   component sets own their responsive states: never copy their states into generic
   Interaction State Reference frames or create a second page-local component family.
16. **Keep design rationale off the published canvas.** Every visible line on a service
   or landing page must help the visitor understand the problem, offer, proof, outcome,
   next step, or an approved qualification. Do not publish self-referential captions or
   internal explanations such as “presented in the order it matters,” “this section
   shows,” “select a criterion,” hierarchy justifications, layout notes, implementation
   instructions, or component guidance. Put that information in layer names, component
   descriptions, rules groups, or handoff notes instead. Before completion, scan both
   breakpoints for meta-copy and remove it without inventing replacement copy.
17. **Finish with a developer-readiness pass.** Active implementation frames must be
   named clearly and contain only the approved, contiguous section sequence; hide or
   archive superseded variants. Resolve every missing font before handoff and use
   explicit SVG/vector or canonical component icons rather than icon-font glyphs. Keep
   pagination fully inside its section with deliberate bottom padding, and move
   decorative motifs clear of headings, body copy and controls. Document state counts,
   accessibility behavior, mapped HubSpot reuse and any unverified proof, URL, form or
   booking dependency as a release gate—never silently present an assumption as final.

## Workflow

0. **Read the brief.** Pages usually come with a writer's/design brief (Google Doc or
   YAML) whose content-plan table IS the wireframe: section order (binding), per-section
   format, audience, and which existing page's pattern each section reuses. Extraction
   guide: `references/brief-format.md`. No brief? Ask for one or draft the section table
   yourself and get it approved first.
1. **Survey the file first**: start at the canonical Desktop, Mobile and Interaction
   chapters on `🎨 Design System`, then use `get_metadata` (no nodeId) to list pages and screenshot
   the latest approved frames of the page FAMILY you're designing for (service page,
   homepage, LP, nav — see the file map in the references). Work on a draft page
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
   When a canonical component set already contains every responsive state, keep those
   states in the Design System family and use attached instances on pages; do not duplicate
   them inside generic Interaction State Reference boards.
   A linear implementation sequence is not a tab by default: use the canonical Onboarding
   component, keep all stages visible, and create interaction states only when the approved
   brief genuinely defines an interactive behavior.
6. **QA gate — run `references/qa-checklist.md` on every frame** (tokens, type scale,
   spacing, components-not-redrawn, both breakpoints, no clipped text) and iterate until
   it passes. Screenshot-verify; a frame you haven't rendered is not done.
7. Handoff: the node specs ARE the contract — development reads them with
   `get_design_context`; make sizes/spacings deliberate, not eyeballed. The handoff must
   name the canonical component, source node, mapped HubSpot file/classes and any
   intentional divergence from the existing implementation. It must also name every
   interactive state's count and accessible behavior, confirm that the active Desktop
   and Mobile frames are the only implementation targets, and list unresolved content
   proof, direct URLs, form IDs or booking endpoints as explicit release gates.

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
`references/canonical-page-sections.md` (the canonical Desktop/Mobile component chapters,
Pagination and Playbooks families, Quote-to-Cash states, colour restrictions and the
Figma-to-HubSpot reuse gate),
`references/brief-format.md` (how briefs spec pages) and `references/qa-checklist.md`
(the per-frame QA gate) before touching the file.
