# Magic Patterns "MAN Digital" tokens — full extraction (index.css, Aug 2026)

Design system id `ds-f7177682-6ec6-4ce2-bc21-f46ad4e9e37a`. These are the CANONICAL
variable names + values. Re-read via `read_design_system_files(["index.css",
"tailwind.config.js"])` when in doubt — this snapshot may age.

## Core colors
--medium-blue #000FC4 · --blue-700 #333FD0 · --blue-500 #5963D9 · --blue-300 #C8CCF2 ·
--blue-200 #E4E6F9 · --blue-100 #EEF0FB · --blue-050 #ECF1FB · --ghost-white #F7F7FF ·
--white #FFFFFF · --ink #222222 · --ink-secondary #434343 · --ink-tertiary #999999 ·
--black #0A0A0A · --stroke #CFCFCF · --hairline #EDEEF7 ·
--cyan-accent #2DE4E6 · --cyan-300 #96DDF3 · --cyan-200 #C5F2F3 · --cyan-100 #96F2F3 ·
--discovery-orange #F26620 (hover #E85C18, active #DE5818; primary-blue hover #000AA8) ·
--revenue-green #33BB68 · --revenue-mint #2DE6A8 ·
--employer-orange #F26419 · --employer-amber #F6AE2D ·
--community-red #E62D30 · --community-yellow #F9CD41

## Status pairs (bg + text)
positive #E8F7EE/#176B37 · warning #FFF4E5/#7A3E00 · critical #FDEBEC/#9E1C21 ·
info #E4E6F9/#000FC4

## Semantic sets
Backgrounds: page=ghost-white, surface=white, subtle=blue-100, brand=medium-blue, dark=black.
Text: primary=ink, secondary=ink-secondary, tertiary=ink-tertiary, on-brand=white.
Borders: soft=hairline, strong=blue-300, focus=black.
Actions: primary blue (hover #000AA8), secondary outline-blue, tertiary text-blue,
inverse (white outline on dark), discovery orange (hover/active above).
Themes: `brand` (blue page, cyan primary action, white text) and `dark` (black page).

## Space / radius / size / motion
Space: 0,4,8,12,16,24,32,40,56,80,96 (`--md-space-*`). Gutters 24/40/80. Sections
56/80/96 (compact 40/56/80, tight 32/40/56). Region 40/56. Grid 24/32. Card padding
16/24/32/40. Control gap 8, inline 12, nav 32. Stacks 4→40.
Radius: 4/8/12/16/24/999. Controls 36/44/52. Icons 16/20/24. Header 72.
Containers: content 1120, wide 1280, copy 720.
Shadows: chip 0 3px 6px rgba(0,0,0,.04) · card 0 8px 24px rgba(0,15,196,.08) ·
raised 0 12px 40px rgba(0,15,196,.12).
Motion: fast 120 / standard 180 / slow 240ms, ease cubic-bezier(0.2,0,0,1).
Focus: 3px #0A0A0A inner, offset 2, white halo. Disabled opacity .4.
Logo box 164×40.

## Type (md-type-web-*)
Display 72/80 · H1 64/72 · H2 44/52 ls -0.5 · H3 32/40 · H4 24/32 · H5 20/28
(Montserrat 700/600) · body-lg 20/32 · body 18/28 · body-sm 16/24 · label 14/20 Lato 700
ls .25 · caption 12/16 · action 16/20 Lato 700 · metric 56/60 (+metric-lg 64/68).
Deck scale (`md-type-deck-*`) is decks-only — never websites.

## Known discrepancy
MP web css: H2 letter-spacing **-0.5px**; the Figma frames + figma-source-of-truth rule:
**-2px**. In FIGMA follow the Figma frames (-2px); the web layer implements its own.
Same class of thing as #999999 (design) vs #767676/#6b6b6b (web AA).
