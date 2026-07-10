# MAN Digital Brand Rules For Blog Graphics

## Voice And Visual Positioning

MAN Digital graphics should feel like modern B2B strategy work: structured, credible, minimal, and operationally clear. Structure comes first, decoration second.

Do not use generic SaaS decoration, emoji, hand-drawn/whiteboard style, marker style, playful illustration, or random stock imagery.

## Core Colors

- Medium Blue: `#000FC4` - anchor color and primary brand surface.
- Fluorescent Cyan: `#2DE4E6` - sharp accent, highlights, signal marks.
- Ghost White: `#F7F7FF` - soft page and panel background.
- Black: `#0A0A0A` - high-contrast text.
- Dark Text: `#222222` or `#434343` - common Pencil component text.
- Light Blue Surface: `#ECF1FB` or `#EDF2FB` - card and diagram backgrounds.
- Light Purple Stroke: `#C8CCF2` - borders and connector lines.
- Orange: `#F26419` - restrained CTA/accent. Do not let it dominate blog graphics.
- Muted Indigo: `#5963D9` - quiet tab, label, and category accent when Medium Blue is too dominant.
- Neutral Charcoal: `#434343` - subdued category accent, rule panel text, or secondary visual cue.

For tabbed comparisons, grouped departments, or multi-topic explanations, the preferred muted accent set is `#5963D9`, `#F26419`, and `#434343`, supported by Medium Blue `#000FC4` for headings and Dark Text `#222222` for body copy.

## Semantic Differentiation

When a graphic compares or groups distinct topics, departments, stages, statuses, systems, or audiences, use color and structure to make the groups scannable while staying minimal.

Prefer subtle surfaces and accents:

- Primary/anchor group: Medium Blue `#000FC4` or a white card with blue rail.
- Signal/highlight group: cyan `#2DE4E6` or a light cyan tint.
- Secondary neutral group: light blue surfaces `#ECF1FB`, `#EEF0FB`, or `#E4E6F9`.
- Revenue/growth group: restrained green from the pillar accents when the content semantics justify it.
- Enablement/warning group: restrained orange/amber only when it clarifies the concept.

Use structural cues before adding more color: lanes, section headers, label chips, left rails, icon medallions, border colors, and grouped background panels. Avoid arbitrary rainbow palettes.

## Component Visibility

Every structural cue must be visible against its immediate background. Before passing a component, compare the fill of each accent bar, chip, rail, divider, medallion, connector mark, and label surface against its parent/card/lane/canvas fill.

- Do not set an accent bar, chip, pill, or divider to the same color as its containing card or panel.
- Do not rely on the outliner to prove a visual cue exists; if it cannot be seen in the screenshot or close-up export, it fails.
- When a copied component inherits `#FFFFFF` inside a white card, change the cue to an approved MAN Digital accent such as Medium Blue `#000FC4`, Fluorescent Cyan `#2DE4E6`, Light Blue Surface `#ECF1FB`, or a semantic restrained pillar accent.
- For subtle cues, use enough contrast to be perceptible at the final export size. A nearly invisible cue is not minimalism; it is a missing component.

## Typography

- Headings: Montserrat, usually bold or semibold.
- Body and labels: Lato.
- Editorial/blog body copy outside diagrams may use Charter only when the design system specifically calls for editorial text.

Common observed Pencil sizes:

- Large vertical cover titles: about 56 to 63 px in 1190 x 1684 frames.
- Section headings: about 36 to 41 px.
- Diagram card headings: about 20 to 24 px.
- Labels and pills: about 16 to 18 px.

LinkedIn carousel body text from the Gemini skill uses larger accessibility minimums, often 44 px. Do not force that size into dense blog diagrams; use the source component scale.

## Layout Patterns

- White cards on blue are a core pattern.
- Blue frames with white typography are acceptable for covers and strong article lead visuals.
- Light blue/white diagrams are preferred for explanatory blog graphics.
- Use modular hierarchy: clear title, concise subtitle, a structured diagram, and restrained footer or logo.
- Use generous spacing, but keep diagrams dense enough to communicate workflow and comparison.
- Use minimal outline icons, ideally the existing Streamline-style icons already in the Pencil file.
- Icon strokes should be thin and clean. Use the `GoNGR`, `id7JG`, `g0Gr3`, `OY5Hk`, and `vvog0` style family as the benchmark: outline-first, not bold, not chunky, and not filled unless the source component requires it.
- For pills and small signal labels, use the `XlJSz`, `pDKxe`, `wcgGl`, and `D4tA8` family as the benchmark: Lato Regular, roughly 18 px in vertical infographic compositions, 140% line height, tight internal padding, and enough left/right padding that text never crowds the icon or pill edge.

## Decorative Elements

Decoration must come from the registry or a documented Figma/Pencil reference. Do not add generic repeated circles, pale blobs, or arbitrary background ornaments just because a canvas feels empty.

Approved decoration families include:

- Soft Circle: `VsypW`
- Orange dotted triangle circle: `GogdW`
- Orange circle-line system: `p4Dtt`
- Dot pattern field: `xOLUX`
- Subtle MAN Digital panel: `linear-gradient(270deg, rgba(0, 15, 196, 0.00) 36.57%, rgba(0, 15, 196, 0.11) 100%), #F7F7FF`, with about `1.095px` `rgba(200, 204, 242, 0.45)` stroke and `0.5` opacity.

The `egabQ` regression is a hard warning pattern: do not invent unregistered pale circle decorations or repeat one decoration style across unrelated graphics. If no registered decoration fits the content, use no decoration and strengthen the layout instead.

## Asset Rules

Use assets from:

`/Users/romeoman/Documents/Marketing/Design/MAN Digital Design System/assets/`

Prefer:

- `logo-color.png` on light backgrounds.
- `logo-mono-blue.png` on light backgrounds when a quiet footer/logo mark is needed.
- `logo-white.svg` or `logo-mono-white.png` on blue backgrounds.
- HubSpot badges and logos from the design system assets only when relevant to HubSpot, RevOps, CRM, or integration topics.

Do not type `MAN Digital` as footer text in a finished graphic. Use an approved logo asset from the design-system folder. In Pencil, place the logo as an image fill on a frame/rectangle and screenshot the logo node directly if its footer size makes it hard to inspect on the full canvas.

Logo placement can vary by composition. Use a top logo when the graphic is brand-led, cover-like, or has a strong dark header. Use a bottom logo when the diagram, callout labels, or annotation bars need the header area. Do not always force the logo into the same corner, and do not let the logo occupy the place where a needed label, pin, or callout should go.

Do not introduce off-brand icons or external imagery unless the user explicitly requests it.
