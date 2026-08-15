# MD-Website design primitives (source: shipped RevOps refresh, Aug 2026)

## File map (survey it FIRST — the whole file is the reference, not one page)

The plugin page-list (`figma.root.children`) shows 40+ pages; the get_metadata no-nodeId
listing TRUNCATES it — don't trust that. Key pages (Aug 2026):

| Page                                                           | Holds                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **🎨 Design System (40000555:2358)**                           | THE first stop. Organized in Figma Sections: 00 Cover+TOC (dark) · 01 Colors (all named MD/ tokens) · 02 Typography (BOTH scales) · 03 Spacing, Radii, Shadows & Motion (semantic roles + MP effect/motion/focus tokens) · 04 Badges & Accreditations (Badge Library clone) · 05 Nav & Footer (desktop+mobile) · 06 Components Desktop · 07 Components Mobile (flat REFRESH language) · 08 Mobbin Inspiration Shelf                                                                                     |
| **🏢 Client Logos (40000570:2358)**                            | ALL client logos in 3 tiers (T1 enterprise/global · T2 scale-ups/SaaS · T3 software houses/consultancies), industry caption on every card, "Index by industry" text block. White logo variants sit on #222222 cards. **Base = BaseLinker rebrand** — never label it Basecamp. 164×40 optical box. Section 05 "Variant matrix" (`40000598:2358`) is **NOT DONE** — holds rejected Brandfetch rasters, needs the vector+recolor rebuild (see `figma-mcp-playbook.md` → "True white/black mono variants"). |
| **💬 Testimonials (40000572:2358)**                            | Every attributed quote: 11 case-study cards + 2 website cards (real portraits from hubfs where they exist — itCraft, Amsterdam Standard, XPlus, Gürtl, Ciprandi; initials avatars otherwise, never stock) + all 28 HubSpot Marketplace reviews (5.0★) with reviewer, industry, size, services.                                                                                                                                                                                                          |
| **✨ Decorative Elements (40000579:2358)**                     | Motif library: local SVG assets + in-file motifs cloned from live designs + Mobbin inspiration shelf. Rule: max ONE motif per section, behind content, flat only.                                                                                                                                                                                                                                                                                                                                       |
| Badges & Awards — assets (40000311:2403)                       | Badge/award artwork MASTER (Badge Library frame 40000311:2404). DS chapter 04 holds a clone — edit the master here.                                                                                                                                                                                                                                                                                                                                                                                     |
| RevOps Refresh — AI draft (40000296:2358)                      | Latest shipped design: desktop 40000296:2359 (1512w), mobile 40000329:2358 (360w), state references (case pagination 40000385:2358 / 40000459:2693, playbooks 40000444:2420)                                                                                                                                                                                                                                                                                                                            |
| 👨‍💻 Service Page (10036:710)                                    | Older service designs + component stock (popups, tabs, cards, faces, logo crops)                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 🏠 Homepage - 2025 / 🟢 Homepage 2024 (5375:3848)              | Homepage designs; Homepage_v2 mobile 360w confirms the breakpoint pair                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 👨‍💻 Case Study · 📋 Blog · ☑️ Pricing (4209:25289) · Nav - 2025 | Their page families                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| LP pages (ABM personas/verticals, Sprint, Events, PPC, NL)     | Landing-page families                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Playground 2023 · Symbols                                      | Legacy component stock                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ⛔️-prefixed pages                                              | ARCHIVED — reference only, never extend                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

New work goes on a draft page named "«Page» — AI draft". When designing for a family,
spec-check THAT family's latest approved frames with `get_design_context` and match them.
Consistency = match the file, not one page.

### Local asset folders (macOS)

- Client logos (true-vector SVGs, per-client subfolders): `~/Documents/Marketing & Sales/Design/Assets/Client Logos/`
- Decorative elements (SVG): `~/Documents/Marketing & Sales/Design/Assets/Decorrative Elements/`
- Envato downloads land in: `~/Documents/Marketing & Sales/Design/Assets/Envato/<asset-name>/`

Import via `upload_assets` (multipart curl, `type=image/svg+xml`) — SVGs arrive as editable
vectors on the CURRENT page, so `setCurrentPageAsync` the target page first. Many client
logos are white variants: check the render and flip the card to #222222 when invisible.

## Implementation layer: Magic Patterns "MAN Digital" design system

`list_design_systems` → **ds-f7177682-6ec6-4ce2-bc21-f46ad4e9e37a** (active) →
`get_design_system` → `read_design_system_files`. ~100 components (Nav/MegaMenu/
MobileNavigation, Footer, Hero/CTA/Pricing/Playbook/Challenge/Team/Testimonial sections,
Button/Badge/TabList/Accordion/Modal/DataTable…) + rules. READ BEFORE DESIGNING:
`rules/figma-source-of-truth.md` (named color variables, canonical section patterns),
`rules/brand-and-color.md`, `rules/typography-rules.md`, `rules/spacing-and-misc-tokens.md`,
`rules/figma-component-coverage.md` (maps every legacy Figma frame to its canonical
component — do NOT invent new components for copied frames), `rules/release-quality-gates.md`.

**DEPRECATED:** the old Service-Page stock (Roadmap/Onboarding popups, Tab Button Light,
revops-card…) is the pre-refresh language with interactions/shadows — do not reuse. The
current standard is the FLAT, no-interaction language of the REFRESH frames.

### System facts to obey

- Headings are **#222222 — never #0A0A0A** (that's footer/darkest surfaces only) and never pure black.
- #999999 = MD/Charcoal Light (tertiary/captions in design); web implementation swaps it
  to #767676/#6b6b6b for WCAG. Discovery Orange states: hover #E85C18, active #DE5818;
  Employer Orange #F26419 is employer-brand only. Cyan #2DE4E6 decoration only.
- Spacing primitives: 0/4/8/12/16/24/32/40/56/80/96 — 18/20/28/30/48/60/72 are BANNED as
  page rhythm. Semantic roles: gutter 24/40/80, standard section 56/80/96, grid gap 24/32,
  card padding 16–40. Web containers 1120/1280/720 (Figma canvas 1512/1348).
- Radius 4/8/12/16/24/999 · controls 36/44/52 · icons 16/20/24 · nav bar 72 · motion 180ms ·
  elevation 0 8px 24px rgba(0,15,196,.08) · client logos in a 164×40 optical box.
- Decoration: BrandMotif set only (dot grids, orange circle, routed lines, diamonds),
  max one per section. No gradients, blobs, textures, or illustrated people.

## Palette (exact — never approximate)

| Token     | Use                                                                                                                                                     |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `#000FC4` | Primary blue: hero/section backgrounds, links, active states                                                                                            |
| `#333FD0` | Secondary blue: featured tiles, icon fills                                                                                                              |
| `#5963D9` | Blue tint: borders on dark, secondary accents                                                                                                           |
| `#C8CCF2` | Light blue: muted text on dark                                                                                                                          |
| `#E4E6F9` | Pale blue: muted text on featured blue cards, chips                                                                                                     |
| `#F7F7FF` | Ghost: tinted section/card backgrounds                                                                                                                  |
| `#161654` | Dark navy: mobile quote cards                                                                                                                           |
| `#F26620` | Orange: CTAs, markers — conversion elements only                                                                                                        |
| `#222222` | Headings (dark charcoal — the brand heading color)                                                                                                      |
| `#434343` | Body text                                                                                                                                               |
| `#0a0a0a` | Near-black alt heading/footer                                                                                                                           |
| Grey rule | Muted text: `#767676` passes contrast ONLY on pure white; on tinted bg (#F7F7FF) use `#6b6b6b`. Never `#999999` — it fails WCAG and web will reject it. |

Fonts: **Montserrat** (headings, weights 400–800; italics are synthesized on web — don't
design real Montserrat italics), **Lato** (body, 400/700 + italics).

## Frames & naming

- Desktop frame **1512w**, content column **1348**. Sections named `«Thing» Section`
  ("Revenue Workflows Section", "Case Studies — Proof Section").
- Mobile frame **360w**, side padding 16–20. Sections `m-hero`, `m-case-studies`,
  `m-fix-banner`, `m-onboarding`… Components like `m-case-card — hubraum (1 of 12)`.
- Mobile derives from desktop: same section order; intros under H2s may be omitted;
  copy may be shortened (web keeps full copy — this is a design-density choice).

## Type scales — TWO, pick by page family

**(A) General web scale (Magic Patterns system):** Display 72/80 · H1 64/72 · H2 44/52 ·
H3 32/40 · H4 24/32 · H5 20/28 (Montserrat 700 for Display–H2, 600 for H3–H5) · Lead 20/32 ·
Body 18/28 · Body-S 16/24 · Label 14/20 Lato 700 · Caption 12/16 · Action 16/20 Lato 700 ·
Metric 56/60. Mobile: H1 44/48, H2 36/42, H3 28/36, Metric 48/52. One H1 per page; body
never below 16px; sentence case.

**(B) Service-LP shipped scale (the REFRESH frames — table below):** tighter, verified in
production. Use for service/LP family pages; use (A) elsewhere unless the family's frames
say otherwise.

| Element                     | Desktop                                  | Mobile (360)                             |
| --------------------------- | ---------------------------------------- | ---------------------------------------- |
| Hero H1                     | 60 / 600 / -2.59px                       | **34 / 700 / -1px / lh 1.15**            |
| Section H2                  | 44 / 700 / -2px (Montserrat)             | **26 / 700 / -1px / lh 1.2**             |
| Eyebrow                     | 14–16, Lato 700, tracking 2px, uppercase | **11 / 700 / tracking 2px**, single line |
| Hero paragraph              | 20 / 1.4, 80–85% white                   | **16 / 24 / rgba(255,255,255,.85)**      |
| Body / intro                | 18 / 28 Lato                             | **16 / 24 Lato**                         |
| FAQ question                | 20 / 700                                 | **16 / 600 / -0.3px**                    |
| Full-width statement banner | 44 / 700, two lines                      | **24 / 700 / -1px / 1.25**, natural wrap |
| Card title                  | 16–17 / 600 Montserrat                   | 16 / 600                                 |
| Card copy                   | **16 / 24 Lato minimum**                 | **16 / 24 Lato minimum**                 |

**Reading-size floor:** website body copy, card copy, table cells, form guidance, and
FAQ answers are never smaller than **16px / 24px** at either breakpoint. Reserve smaller
type only for compact labels, captions, metadata, and uppercase eyebrows.

## Recurring patterns

- **Canonical component source map:** read `component-canon.md` before creating team,
  strategy-call form, FAQ, credentials or decorative sections. Clone the listed source
  nodes; do not substitute a simplified lookalike.
- **Founder CTA chip:** founder photo (53px) + orange `#F26620` panel, title 16/600 +
  subline 12; compact variant on mobile. Lives in hero + used site-wide.
- **Cards:** white, 1px `#E4E6F9`-family border, 4–6px radius. Featured card = blue
  border (`#000FC4`) or `#F7F7FF` fill. Mobile credential/list cards: horizontal rows,
  40px badge left, min 14/16 padding, single column stack.
- **Client logos:** uniform optical size in trays; white variants on blue. Check every
  logo asset — prefer real SVGs; a "SVG" can wrap a giant raster (see mcp playbook).
- **Quote cards:** desktop white with big `#000FC4` quote mark (56/800); mobile dark
  `#161654`, left rule, 36px avatar, name 700 + role in `#C8CCF2`.
- **Carousel/pager:** round arrow buttons + `1 / N` counter (desktop) or dots (mobile),
  controls above the tray with next-card peek.
- **Decorative:** dot-grid pattern on blue, orange/blue circles as accents — sparingly,
  copied from `✨ Decorative Elements (40000579:2358)` rather than redrawn. Use at most
  one composite motif per section, insert it behind content, and keep it clear of text.
- **Long capability scope:** if the preceding section is a tabbed process, use a static
  bento/grouped-card system instead of another master-detail selector. Show every
  capability from the brief and state that final scope follows discovery.
- **Credential hierarchy:** feature the credential most specific to the service first
  (for Quote-to-Cash, the Quote-to-Cash Capability); keep Elite status and implementation,
  onboarding and integration accreditations as supporting proof.
