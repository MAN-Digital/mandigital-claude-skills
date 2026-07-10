# MAN Digital Lucid Charts — Skill

Creates on-brand MAN Digital diagrams in Lucidchart / Lucid via the `@lucid` MCP connector — flowcharts, process maps, RevOps/CRM system-architecture diagrams, org charts, mind maps, funnels, lifecycles, and UML sequence diagrams.

## When to use it

- Any request for a Lucidchart/Lucid diagram, flowchart, process map, RevOps/CRM architecture diagram, signal-engine map, org chart, mind map, funnel, lifecycle, or sequence diagram.
- The user says "make this in Lucid", mentions `@lucid`/"Lucidchart", or pastes a `lucid.app` URL.
- **Not for** Pencil `.pen` blog/social graphics — route those to `man-digital-blog-graphics` or `man-digital-marketing-assets` instead. Lucid is for editable structured diagrams, not hero images or carousels.

## What it needs

- The `@lucid` (Lucidchart) MCP connector connected and authenticated.
- No other MCP tools or API keys required.

## What it produces

A Lucid document containing a brand-styled diagram — MAN Digital palette and fonts applied via the mandatory brand-restyle + font loop (not Lucid's default blue theme), verified with a screenshot-measure-critique-fix audit loop before it's considered done.

## Key references

- `references/brand-tokens.md` — MAN Digital palette, fonts, semantic color-role map (source of truth, don't improvise).
- `references/lucid-workflow.md` — tool routing, the restyle loop, parameters, gotchas.
- `references/svg-templates.md` — SVG-based diagram authoring (the default path for flowcharts, org charts, mind maps).
- `references/layout-and-fit.md` — deterministic sizing/spacing/placement math.
- `references/audit-loop.md` — the mandatory screenshot → measure → critique → fix → re-screenshot QA loop.
