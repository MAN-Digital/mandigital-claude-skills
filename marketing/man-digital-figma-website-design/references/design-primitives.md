# MD-Website design primitives (source: shipped RevOps refresh, Aug 2026)

## File map (survey it FIRST — the whole file is the reference, not one page)

The plugin page-list (`figma.root.children`) shows 40+ pages; the get_metadata no-nodeId
listing TRUNCATES it — don't trust that. Key pages (Aug 2026):

| Page | Holds |
|---|---|
| **🎨 Design System (40000555:2358)** | THE first stop: color tokens, both type scales as live specimens, spacing scale, cloned core components (CTA chip, case card, tab buttons, revops/roadmap/onboarding cards). Extended system lives in Magic Patterns; this page mirrors the production-verified subset |
| Badges & Awards — assets (40000311:2403) | Badge/award artwork |
| RevOps Refresh — AI draft (40000296:2358) | Latest shipped design: desktop 40000296:2359 (1512w), mobile 40000329:2358 (360w), state references (case pagination 40000385:2358 / 40000459:2693, playbooks 40000444:2420) |
| 👨‍💻 Service Page (10036:710) | Older service designs + component stock (popups, tabs, cards, faces, logo crops) |
| 🏠 Homepage - 2025 / 🟢 Homepage 2024 (5375:3848) | Homepage designs; Homepage_v2 mobile 360w confirms the breakpoint pair |
| 👨‍💻 Case Study · 📋 Blog · ☑️ Pricing (4209:25289) · Nav - 2025 | Their page families |
| LP pages (ABM personas/verticals, Sprint, Events, PPC, NL) | Landing-page families |
| Playground 2023 · Symbols | Legacy component stock |
| ⛔️-prefixed pages | ARCHIVED — reference only, never extend |

New work goes on a draft page named "«Page» — AI draft". When designing for a family,
spec-check THAT family's latest approved frames with `get_design_context` and match them.
Consistency = match the file, not one page.

## Palette (exact — never approximate)

| Token | Use |
|---|---|
| `#000FC4` | Primary blue: hero/section backgrounds, links, active states |
| `#333FD0` | Secondary blue: featured tiles, icon fills |
| `#5963D9` | Blue tint: borders on dark, secondary accents |
| `#C8CCF2` | Light blue: muted text on dark |
| `#E4E6F9` | Pale blue: muted text on featured blue cards, chips |
| `#F7F7FF` | Ghost: tinted section/card backgrounds |
| `#161654` | Dark navy: mobile quote cards |
| `#F26620` | Orange: CTAs, markers — conversion elements only |
| `#222222` | Headings (dark charcoal — the brand heading color) |
| `#434343` | Body text |
| `#0a0a0a` | Near-black alt heading/footer |
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

## Type scale (from the latest shipped exemplar's node specs — re-verify against the family you're designing in)

| Element | Desktop | Mobile (360) |
|---|---|---|
| Hero H1 | 60 / 600 / -2.59px | **34 / 700 / -1px / lh 1.15** |
| Section H2 | 44 / 700 / -2px (Montserrat) | **26 / 700 / -1px / lh 1.2** |
| Eyebrow | 14–16, Lato 700, tracking 2px, uppercase | **11 / 700 / tracking 2px**, single line |
| Hero paragraph | 20 / 1.4, 80–85% white | **15 / 1.5 / rgba(255,255,255,.85)** |
| Body / intro | 16–18 Lato / 1.5 | 15 Lato / 1.5 |
| FAQ question | 20 / 700 | **15 / 600 / -0.3px** |
| Full-width statement banner | 44 / 700, two lines | **24 / 700 / -1px / 1.25**, natural wrap |
| Card title | 16–17 / 600 Montserrat | 16 / 600 |
| Card copy | 13–14 Lato | 13 Lato |

## Recurring patterns

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
  copied from existing frames rather than redrawn.
