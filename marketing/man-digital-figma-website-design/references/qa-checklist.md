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
- [ ] Montserrat headings / Lato body. No real Montserrat italics.
- [ ] No clipped/overflowing text (screenshot check — resize-after-set collapses text nodes).

## Layout & spacing
- [ ] Frame widths exactly 1512 / 360; content column 1348 on desktop.
- [ ] Spacing values on the scale (4/8/12/16/20/24/32/40/56/64/100) — no 13px gaps.
- [ ] Auto-layout used for structurally-related children (no absolute-positioned stacks).
- [ ] Nothing overflows the frame horizontally.

## Components & consistency
- [ ] Recurring elements are CLONES of the Design System page / source-page components,
      not redraws (CTA chip, cards, pagers, badges, quote cards).
- [ ] Section naming: desktop "«Thing» Section", mobile `m-*`.
- [ ] Both breakpoints exist and agree in section order; mobile density rules applied
      (intros omitted where the pattern says so, compact CTA).
- [ ] Interactive patterns have their state reference frames.

## Content
- [ ] Copy matches the brief/approved source verbatim; [TO BE ADDED] markers preserved,
      nothing invented.
- [ ] Real assets (hubfs originals, provided photos, Envato-licensed) — no watermarked
      previews left in final frames.
