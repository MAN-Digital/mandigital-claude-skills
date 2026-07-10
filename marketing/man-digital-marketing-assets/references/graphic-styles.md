# Graphic Styles

Use this before designing a MAN Digital blog graphic. Blog graphics are not one fixed template style; choose one visual system before building.

## Style Families

| Style | Use when | Build discipline |
| --- | --- | --- |
| Lucidchart-style flow | Process, routing, handoff, governance, decision path | 3-7 nodes, clean lanes, orthogonal connectors, no paragraph-heavy cards |
| Architecture map | Systems, data model, integrations, RevOps stack | Group by layer or system boundary, use restrained connectors, keep labels short |
| Annotated screenshot | Product/UI/data model proof | Screenshot or UI mockup is the main object; use 1-3 callouts unless labels are integrated |
| Data-model table/card | HubSpot fields, CRM attributes, lifecycle fields | Treat it as a simplified UI, not a dense real table; use large field cards and highlights |
| Matrix/scorecard | Comparison, criteria, readiness, assessment | Avoid arrows; use rows/columns, badges, and color hierarchy |
| Layer stack | Foundation-to-activation, maturity model | Vertical bands, clear section labels, minimal connectors |
| Flywheel/lifecycle | Loops, operating models, compounding process | Use existing circular/flywheel components; do not casually change step count |
| Timeline/roadmap | Sequence over time | Use one axis and equal intervals; avoid branching |
| Editorial cover | Blog hero/thesis/contrarian claim | Strong headline plus one visual anchor; no slide footer/page chrome |

## Selection Gate

Before creating nodes, decide:

1. Output type and size.
2. One style family from the table.
3. Closest Playground component/template for that family.
4. Which parts come from the MAN Digital design-system assets.
5. Which visual-depth system will keep the graphic from feeling primitive: mapped dot grid, radar arc, pale ellipse, background plane, label pins, icon medallions, screenshot shell, or approved logo treatment.
6. Which text-scale plan applies from `readability-depth-gate.md`.
7. Which container-spacing and topic-differentiation plan applies from `container-spacing-and-topic-coding.md`.
8. Which audit references apply: `flow-connectors.md`, `zoom-audit.md`, image placeholders, or component anatomy.

If no Playground template exactly matches, still use Playground elements first: cards, pills, icon treatments, connector styles, panel surfaces, title systems, and logo treatment. Create primitives only for the missing structure.

## Visual Depth

Structure comes first, but a finished MAN Digital graphic should still feel designed. Use one quiet supporting depth system when the canvas otherwise becomes a plain diagram:

- light backgrounds: pale ellipses, dot grids, label pins, screenshot frames, restrained shadows, cyan connector accents;
- dark backgrounds: dot grids, orbit/radar arcs, diagonal planes, white cards, stronger logo contrast;
- HubSpot/RevOps topics: HubSpot sprocket/logo assets, signal medallions, field cards, routing pins, and stage icons.

Do not invent random decorative shapes. Use the mapped Playground/design-system elements listed in `readability-depth-gate.md`, keep them behind content, and remove them if they compete with labels or connectors.

## Composition Efficiency

Negative space is valuable only when it improves the reading path, hierarchy, or focus. Large colored blocks are not brand quality by themselves.

- Do not add a full-height sidebar, brand slab, empty color plane, or oversized rail just to show Medium Blue or hold a logo.
- A large plane larger than roughly 10-12% of the canvas must carry meaningful content, create an intentional section/lane, frame the main visual, or materially improve the composition.
- If a plane only repeats brand color, replace it with a compact logo asset, small accent rail, dot grid, pale ellipse, header/footer treatment, or a content-bearing panel.
- A logo can sit on the canvas, in the header, or in the footer without needing a dedicated slab. The logo should not steal space from the main visual.
- Regression case: node `ZBw56` from the 1536 x 1024 GTM handoff test was a full-height Medium Blue left brand plane that occupied useful content width while carrying only a small logo. That is wasted space and must fail future audits unless the plane is redesigned as a content-bearing lane.

## Composition Zones

Use explicit zones rather than free-floating text:

- Header zone: eyebrow, heading, support copy.
- Visual zone: diagram, screenshot, architecture map, matrix, or chart.
- Footer/brand zone: approved MAN Digital logo asset only, or a user-requested/source-required caption. Do not add article-context, prompt-rationale, or internal planning notes.

Heading/support text should be placed in a vertical text-stack frame whenever possible. If absolute positioning is inherited from a Playground template, measure the rendered heading height before placing the support line or visual zone.

## Labels, Pins, And Callout Bars

Some blog graphics need small labels, bars, pins, or tags before the viewer reaches the main object or route. Use them to name regions such as inputs, governance layer, outputs, risk points, or proof points.

- Plan these labels as part of the visual system, not as decoration.
- Keep labels short: one to three words when possible.
- Use label bars/pins where they clarify the object before the connector path starts.
- Do not use the logo slot for these labels; move the logo to the top or bottom based on composition needs.
- Audit labels with the same close-up rules as cards: no overlap, enough padding, and no connector line running through them.

## Multi-Topic Differentiation

When the graphic includes multiple departments, audiences, stages, systems, statuses, or topic families, design a restrained differentiation system before placing cards.

- Use lanes, grouped panels, chips, left rails, icon medallions, border colors, or light tints to make categories scannable.
- Keep brand minimalism: most surfaces should stay white, Ghost White, or light blue; accents should clarify category meaning.
- Do not rely on body text alone to show that Sales, Marketing, Customer Success, risk, fix, output, input, or ownership groups are different.
- Do not create arbitrary rainbow palettes. Use the brand and pillar tokens in `brand-rules.md` and the measurement rules in `container-spacing-and-topic-coding.md`.

## Anti-Patterns

- Mixing a screenshot, table, card grid, callout web, connector map, and footer strip at equal visual weight.
- Building a flowchart by threading lines after cards are already crowded.
- Treating a full-canvas screenshot as proof that small text and arrows are clean.
- Treating technically aligned but tiny 20 px labels as readable in a 1536 px wide mobile-sensitive blog graphic.
- Shipping a primitive row of outlined rectangles when mapped Playground cards, medallions, pins, dots, arcs, and depth shapes could have made the idea feel like MAN Digital.
- Shipping multiple distinct topics in identical boxes with no visual coding, grouping, lanes, labels, icons, or color/tint cues.
- Placing text in pills, badges, cards, boxes, or callouts without measured internal padding.
- Typing `MAN Digital` as footer text instead of using the approved logo asset.
- Adding a big Medium Blue side block or full-height brand plane that does not carry content, guide the diagram, or create a meaningful lane.
- Choosing a slide/deck composition for a blog graphic without removing slide grammar.
- Adding visible `Article context: ...`, prompt rationale, section rationale, or audit/planning notes inside a blog graphic. The article already gives that context.
