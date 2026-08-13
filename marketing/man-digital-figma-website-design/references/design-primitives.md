# MD-Website design primitives (source: shipped RevOps refresh, Aug 2026)

## File map

- File key: `IOhToZi5UBH5vNFV741HP3` (MD-Website). Work happens on draft pages
  ("«Page» — AI draft"); reference examples: desktop `40000296:2359`
  ("Service Page-Desktop_v2 — REFRESH", 1512w), mobile `40000329:2358` (360w),
  state references: case pagination `40000385:2358` / `40000459:2693` (mobile),
  playbooks master-detail states `40000444:2420`, client logos tray `40000429:29215`.

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

## Type scale (from shipped node specs)

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
