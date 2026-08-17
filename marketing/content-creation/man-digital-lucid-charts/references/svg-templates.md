# Branded SVG Templates for `lucid_convert_svg_to_diagram`

The SVG path is the default for flow / process / RevOps-architecture **and org charts / mind maps** (the `create_org_chart` / `create_mind_map` tools yield unbrandable nodes). Inline brand hex on `<rect>`/`<text>` passes through to Lucid, giving full color + layout control in one call.

**Two parser quirks to plan for (confirmed in testing):**

- **No full-canvas background `<rect>`** — a page-filling rect becomes a labeled "Process" block that renders as a giant watermark + container box. Rely on the page background; if a background slips in, `fetch` → `lucid_delete_items` it.
- **`<line>`/`<path>` stroke colors are dropped** (edges import black). After convert, run a `lucid_edit_item` pass to set each connector's `line_color`. Node fills/text/borders survive; fonts may fall back — verify the PNG and finish fonts with `lucid_edit_item`.

Map shapes to `brand-tokens.md` roles: `<rect>`→process/terminator, `<polygon>` diamond→decision, `<ellipse>`/`<circle>`→start/end, `<line>`/`<path>`→connector, `<text>`→label.

## Vertical flow (mobile/article-friendly — preferred for RevOps lead flow)

```svg
<svg viewBox="0 0 520 760" xmlns="http://www.w3.org/2000/svg" font-family="Lato, sans-serif">
  <!-- NO full-canvas background rect: it becomes a "Process" watermark. Use the page background. -->
  <!-- entry / terminal: Medium Blue -->
  <rect x="160" y="24" width="200" height="60" rx="30" fill="#000FC4" stroke="#000FC4"/>
  <text x="260" y="60" fill="#F7F7FF" text-anchor="middle" font-size="18">New Inbound Lead</text>
  <!-- process: white card on blue -->
  <rect x="160" y="124" width="200" height="60" rx="10" fill="#FFFFFF" stroke="#000FC4" stroke-width="2"/>
  <text x="260" y="160" fill="#222222" text-anchor="middle" font-size="16">Enrich · Firmographics</text>
  <!-- signal/scoring moment: cyan accent -->
  <rect x="160" y="224" width="200" height="60" rx="10" fill="#ECF1FB" stroke="#2DE4E6" stroke-width="3"/>
  <text x="260" y="260" fill="#222222" text-anchor="middle" font-size="16">Score Lead</text>
  <!-- decision: neutral card + blue border, NOT orange -->
  <polygon points="260,324 360,384 260,444 160,384" fill="#FFFFFF" stroke="#000FC4" stroke-width="2"/>
  <text x="260" y="390" fill="#222222" text-anchor="middle" font-size="15">Score &gt;= 80?</text>
  <!-- yes path: single CTA = orange (the one accent) -->
  <rect x="300" y="484" width="190" height="60" rx="10" fill="#F26419" stroke="#F26419"/>
  <text x="395" y="520" fill="#F7F7FF" text-anchor="middle" font-size="16">Route to AE</text>
  <!-- no path: neutral nurture -->
  <rect x="30" y="484" width="190" height="60" rx="10" fill="#434343" stroke="#434343"/>
  <text x="125" y="520" fill="#F7F7FF" text-anchor="middle" font-size="16">Nurture Sequence</text>
  <!-- terminal -->
  <rect x="160" y="584" width="200" height="60" rx="30" fill="#000FC4" stroke="#000FC4"/>
  <text x="260" y="620" fill="#F7F7FF" text-anchor="middle" font-size="18">Sync to CRM</text>
  <!-- connectors: light purple default, blue for primary path -->
  <line x1="260" y1="84"  x2="260" y2="124" stroke="#000FC4" stroke-width="2"/>
  <line x1="260" y1="184" x2="260" y2="224" stroke="#000FC4" stroke-width="2"/>
  <line x1="260" y1="284" x2="260" y2="324" stroke="#000FC4" stroke-width="2"/>
  <line x1="320" y1="414" x2="395" y2="484" stroke="#F26419" stroke-width="2"/>
  <line x1="200" y1="414" x2="125" y2="484" stroke="#C8CCF2" stroke-width="2"/>
  <line x1="395" y1="544" x2="320" y2="600" stroke="#C8CCF2" stroke-width="2"/>
  <line x1="125" y1="544" x2="200" y2="600" stroke="#C8CCF2" stroke-width="2"/>
  <text x="350" y="470" fill="#F26419" font-size="13">Yes</text>
  <text x="150" y="470" fill="#434343" font-size="13">No</text>
  <!-- No brand wordmark/footer — brand comes from palette + type only -->
</svg>
```

## Org chart (use this, NOT `lucid_create_org_chart`)

A hierarchy is a tree of `<rect>`+`<text>` nodes joined by `<line>`s. Root = Medium Blue terminal; mid-tier = white-card-on-blue; leaves = quiet `#ECF1FB`/`#5963D9`. Re-set the connector colors after import (parser drops `<line>` strokes).

```svg
<svg viewBox="0 0 720 420" xmlns="http://www.w3.org/2000/svg" font-family="Montserrat, sans-serif">
  <!-- root -->
  <rect x="290" y="20" width="140" height="56" rx="8" fill="#000FC4" stroke="#000FC4"/>
  <text x="360" y="52" fill="#F7F7FF" text-anchor="middle" font-size="16">CEO</text>
  <!-- tier 2: white card on blue -->
  <rect x="150" y="150" width="160" height="56" rx="8" fill="#FFFFFF" stroke="#000FC4" stroke-width="2"/>
  <text x="230" y="182" fill="#222222" text-anchor="middle" font-size="15">VP RevOps</text>
  <rect x="410" y="150" width="160" height="56" rx="8" fill="#FFFFFF" stroke="#000FC4" stroke-width="2"/>
  <text x="490" y="182" fill="#222222" text-anchor="middle" font-size="15">VP Marketing</text>
  <!-- tier 3: quiet leaves -->
  <rect x="70"  y="300" width="150" height="52" rx="8" fill="#ECF1FB" stroke="#5963D9" stroke-width="2"/>
  <text x="145" y="330" fill="#222222" text-anchor="middle" font-size="14">RevOps Manager</text>
  <rect x="240" y="300" width="150" height="52" rx="8" fill="#ECF1FB" stroke="#5963D9" stroke-width="2"/>
  <text x="315" y="330" fill="#222222" text-anchor="middle" font-size="14">SDR Lead</text>
  <rect x="425" y="300" width="150" height="52" rx="8" fill="#ECF1FB" stroke="#5963D9" stroke-width="2"/>
  <text x="500" y="330" fill="#222222" text-anchor="middle" font-size="14">Content Lead</text>
  <!-- connectors: blue exec layer, purple report layer (re-apply colors post-import) -->
  <line x1="360" y1="76" x2="230" y2="150" stroke="#000FC4" stroke-width="2"/>
  <line x1="360" y1="76" x2="490" y2="150" stroke="#000FC4" stroke-width="2"/>
  <line x1="230" y1="206" x2="145" y2="300" stroke="#C8CCF2" stroke-width="2"/>
  <line x1="230" y1="206" x2="315" y2="300" stroke="#C8CCF2" stroke-width="2"/>
  <line x1="490" y1="206" x2="500" y2="300" stroke="#C8CCF2" stroke-width="2"/>
  <!-- No brand wordmark/footer -->
</svg>
```

## RevOps / system-architecture lane idea

Three vertical lanes — Sources, Engine, Destinations. Lane headers in Medium Blue `#000FC4` (white text); system nodes as white cards with `#000FC4`/`#C8CCF2` borders; the one scoring/signal node in cyan `#2DE4E6`; connectors `#C8CCF2`, primary data path `#000FC4`. Keep each node a separate `<rect>`+`<text>` so it stays editable. Use no orange unless one node is the explicit conversion/CTA point.

## Sequence diagram styling (PlantUML)

`lucid_create_sequence_diagram` auto-applies Lucid blue. To push toward brand, include skinparams, then finish text in the restyle loop:

```
@startuml
skinparam backgroundColor #F7F7FF
skinparam sequence {
  ParticipantBackgroundColor #000FC4
  ParticipantFontColor #F7F7FF
  ActorBackgroundColor #000FC4
  LifeLineBorderColor #C8CCF2
  ArrowColor #000FC4
}
actor Lead
participant "Enrichment" as E
participant "Scoring Engine" as S
participant CRM
Lead -> E : inbound
E -> S : firmographics
S -> CRM : score >= 80 routes to AE
@enduml
```

Read `lucid://sequence-diagram-specification` for the full participant/arrow vocabulary before calling.
