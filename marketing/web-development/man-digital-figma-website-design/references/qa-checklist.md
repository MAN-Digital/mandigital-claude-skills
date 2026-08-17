# Design QA — run on EVERY frame before calling it done

Self-audit loop (like the Pencil/openclaw graphics QA): render → check → fix → re-render.
A frame passes only when every item below passes. Verify by SCREENSHOT + node specs, not
by memory of what you built.

## Tokens
- [ ] Every fill/stroke/text color is in the palette (design-primitives.md / the
      🎨 Design System page). No off-palette hexes, no near-misses (#0010C5 ≠ #000FC4).
- [ ] Grey text: #767676 only on pure white; #6b6b6b on tints; never #999999.
- [ ] Orange #F26620 only on conversion elements.

## Type
- [ ] Every text node matches a row of the type scale (family, weight, size, letter-spacing,
      line-height) for its breakpoint. No 28px H2s on mobile (scale says 26), no faux specs.
- [ ] Body copy, card copy, table cells, form guidance, and FAQ answers are at least
      16px / 24px on desktop and mobile. Only labels, captions, metadata, and eyebrows
      may use smaller type.
- [ ] Montserrat headings / Lato body. No real Montserrat italics.
- [ ] No clipped/overflowing text (screenshot check — resize-after-set collapses text nodes).

## Layout & spacing
- [ ] Frame widths exactly 1512 / 360; content column 1348 on desktop.
- [ ] Spacing values on the scale (4/8/12/16/20/24/32/40/56/64/100) — no 13px gaps.
- [ ] Auto-layout used for structurally-related children (no absolute-positioned stacks).
- [ ] Nothing overflows the frame horizontally.

## Components & consistency
- [ ] The Design System canonical chapters were checked first: Desktop `40000828:2707`,
      Mobile `40000828:2708`, and Interaction/Reuse `40000828:2709`.
- [ ] Every recurring section uses the canonical component or a documented variant; the
      corresponding HubSpot section, CSS classes and JavaScript behavior were inspected
      before new code was written.
- [ ] Case Studies and Team contain a `Pagination` instance (`40000829:2707`); arrows,
      counters and dots were not recreated locally.
- [ ] Playbooks reuse `40000832:29581` / `40000836:3319` and preserve all four categories,
      six items per category and all 24 detail panels in the DOM.
- [ ] Recurring elements are CLONES of the Design System page / source-page components,
      not redraws (CTA chip, cards, pagers, badges, quote cards).
- [ ] Section naming: desktop "«Thing» Section", mobile `m-*`.
- [ ] Both breakpoints exist and agree in section order; mobile density rules applied
      (intros omitted where the pattern says so, compact CTA).
- [ ] Interactive patterns have their state reference frames.
- [ ] Every tab/disclosure that changes content has a complete named state at desktop and
      mobile. Process states include stage label, title, What we do, What you own, and
      Decision gate.
- [ ] Outcome/transformation tabs use a unique semantic diagram per state: named sources
      outside the workflow -> broken handoff -> disconnected object, then a Primary Blue
      governed core -> straight connectors -> named revenue objects. Critical red marks
      failure; CTA orange is absent; connectors do not cross labels.
- [ ] Adjacent content-heavy sections do not repeat the same selector/master-detail UI.
      Mobbin was checked for each novel section and the chosen pattern was restyled into
      MAN Digital tokens.

## Content
- [ ] Copy matches the brief/approved source verbatim; [TO BE ADDED] markers preserved,
      nothing invented.
- [ ] Every briefed capability is visible; no `+N more` row hides required content.
- [ ] Real assets (hubfs originals, provided photos, Envato-licensed) — no watermarked
      previews left in final frames.

## Release gates (from Magic Patterns rules/release-quality-gates.md)
- [ ] Layouts pass at 320 / 390 / 768 / 1280 / 1440 with realistic long content.
- [ ] Discovery Orange CTAs: white Lato Bold 19/24 label; hover #E85C18, active #DE5818.
- [ ] 44px touch targets; two-color focus treatment (3px #0A0A0A inner + white halo).
- [ ] One FAQSection per page for public questions.
- [ ] Client logos in equal 164×40 optical boxes; only verified logos/quotes/claims.

## Asset & badge canon
- [ ] Primary Blue `#000FC4` is used for normal brand/section/active states; Dark Navy
      `#161654` appears only on an approved mobile quote card; CTA Orange `#F26620`
      appears only on conversion actions.
- [ ] Footer/credentials show the ELITE hexagon badge — never the old diamond badge
      (the old homepage designs still carry it; do not copy it forward). All THREE
      accreditations appear: Onboarding, CRM Implementation, Custom Integration.
- [ ] The service-specific capability is the dominant credential; general partnership
      and accreditation cards are visually secondary.
- [ ] Dark/brand-colour logo rows use approved white/reversed logos only; light sections
      use approved dark/full-colour logos. A row never mixes treatments.
- [ ] Founder cards appear before the canonical delivery-team row when both are present.
- [ ] Strategy-call and FAQ sections use the canonical source components listed in
      `component-canon.md`; the form keeps the full field/consent pattern.
- [ ] Decorative motifs come from `40000579:2358`, max one composite motif per section,
      behind content and never crossing readable text.
- [ ] No stock people photos or dated "office stock" imagery — banned outright (brand
      rule shared with the blog-graphics skill: no random stock imagery, no generic SaaS
      decoration). Real team photos, product screenshots, flat vectors, device mockups only.

## Brand critique loop (adapted from man-digital-blog-graphics audit-loop)
For every Envato pick AND every finished frame: render/preview → strict scorecard critique
(brand compliance, hierarchy, alignment/padding, content fit, mobile readability,
composition efficiency) → fix critical → re-check. Max 2 rounds, then either ship or state
the remaining limitation — never silently ship weak work. For assets: SEE the preview
before downloading; verdict must name the intended use case.
