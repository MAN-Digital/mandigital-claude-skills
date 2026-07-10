# Playground Candidate Roster

Use this before choosing a base for MAN Digital blog, HubSpot, RevOps, CRM, AI, workflow, prospecting, outbound, signal, carousel-derived, or article graphics.

## Why This Exists

The MAN Digital design system defines brand rules. The Pencil Playground defines the actual reusable graphic language: mature compositions, cards, connectors, icons, pills, screenshot carriers, depth systems, and logo treatments.

Do not treat brand compliance as component usage. A graphic can use the right colors and fonts while still ignoring the Playground library. That fails this skill.

## Required Candidate Pass

For every open-ended graphic, run this pass before building:

1. Identify the narrative pattern: architecture, flow, loop, comparison, stack, diagnosis, setup, rollout, screenshot walkthrough, takeaway, cover, or CTA.
2. Review the high-value nodes below and pick at least:
   - one primary layout candidate,
   - one alternate layout family,
   - one supporting component/depth candidate.
3. Read each selected candidate's `references/components/<node-id>.md` file.
4. Inspect the selected primary candidate in live `Playground.pen` with Pencil `batch_get` before building.
5. If the final design does not use any listed candidate, record why the prompt is outside this roster and what other Playground node was used.

For HubSpot/RevOps/signal/CRM/system graphics, this pass is in addition to `master-template-fit-map.md`, not a replacement.

## High-Value Families

### Signal-To-Revenue / HubSpot System Explainers

Use these for AI + HubSpot, signal systems, revenue engines, operating models, routing, scoring, workflows, data layers, and CRM architecture.

| Node | Use when | Reuse parts |
| --- | --- | --- |
| `nRPmP` | Full revenue-engine, flywheel, lifecycle, or dark strategic poster. | Orbit/flywheel, dark depth, signal pills, sequential process strip, radar/dot decorations. |
| `KVqAt` | Inputs -> HubSpot data -> AI -> action -> revenue architecture. | Stage cards, medallions, pill rows, light connector path, pale ellipse, dot grid. |
| `tMsEe` | Source taxonomy feeding HubSpot engine and outcomes. | Native/integration/custom source cards, engine timeline, outcome rows, source-to-engine connectors. |
| `b8SoH` | Signal trigger becoming a sales play and action chain. | Central signal hub, play cards, action rows, bracket connectors, radar depth. |
| `llyux` | Layered implementation model, capability blueprint, governance checklist. | Layer rows, capability tiles, bottom outcome chain, blueprint connectors. |

### Prospecting Agent Vs Outbound Vertical Explainers

Use these for HubSpot Prospecting Agent, outbound platforms, hybrid GTM systems, governance, sync, operating models, loops, and takeaways.

| Node | Use when | Reuse parts |
| --- | --- | --- |
| `S20AXj` | Dark cover or thesis frame for Prospecting Agent vs outbound. | Editorial title block, dark background vectors, large visual placeholder, blue callout. |
| `l5NNCU` | Compare HubSpot strengths, outbound strengths, and best-practice hybrid. | Venn/circular comparison, overlap logic, hybrid recommendation pattern. |
| `EdtGZ` | Hybrid prospecting architecture across signals, HubSpot, research, outbound, decision, governance. | Lane system, decision diamond, handoff cards, connector logic. |
| `LZkoW` | Sync rules, outreach workflow, outside/inside HubSpot governance. | Outside/inside lanes, sync rules, governance benefits. |
| `sQ8TR` | Air-cover, brand/research loop, or reinforcement cycle. | Loop structure, feedback arrows, reinforcing elements. |
| `pAw6X` | Recommended layered operating model. | Five-layer model, icon row/layer rhythm, prescription structure. |
| `fKn3K` | Closing key takeaways or summary after a framework. | Takeaway card rhythm, closing hierarchy, final CTA-style emphasis. |

### Prospecting-Agent 1080x1350 Sequence

Use these when the graphic needs a taller social/article explainer, screenshot walkthrough, setup sequence, rollout path, or agent workflow.

| Node | Use when | Reuse parts |
| --- | --- | --- |
| `PPpdM` | Lead/cover frame for Prospecting Agent system overview. | Central system card, surrounding components, dark/light contrast. |
| `s2ZqRB` | Diagnose why Prospecting Agent underperforms. | Four failure circles: ICP, signals, data, workflow. |
| `v5aVuG` | Compare point tools against connected Prospecting Agent. | Left task stack vs right connected hub. |
| `lLDFt` | Show disconnected pre-sales tools and context loss. | Tool chain, context-loss annotations, CRM sync-back motif. |
| `SbBJV` | Explain prerequisites for agent success. | Four prerequisite nodes around central agent. |
| `G7EWZ` | Target market or ICP/account-filter setup. | Screenshot placeholders, tag rails, ICP filter labels. |
| `G6YkCq` | Buyer Intent activation or timing prioritization. | Large screenshot carrier, signal/research intent tags. |
| `nia9w` | Pull companies into working lists or active lists. | Dual screenshot placeholders, signal-to-action bridge. |
| `DJN2N` | Move accounts into Prospecting Agent workflow. | Large screenshot carrier, action labels, workflow handoff. |
| `jNmrp` | Review drafts and track replies, meetings, deals, or outcomes. | Approval/reporting screenshot carrier, result labels. |
| `NhErk` | Summarize setup layers. | Four-layer summary: signal, data, agent, workflow. |
| `Y3Tzyc` | 90-day rollout or staged implementation path. | Discover -> Plan -> Pilot -> Optimize -> Scale timeline. |
| `zuu8y` | CRM Ops prerequisites before enrollment. | Ops checklist, email verification/subscription concepts. |
| `lP11x` | Credits, economics, usage, or pricing story. | Credit/value/conversation/intents structure; verify current numbers before publishing. |
| `HoOjV` | Dark closing CTA, save-this, or final summary. | Dark closing hierarchy and CTA energy. |

## Candidate Note Template

Before building, write an internal note like:

```markdown
Playground candidate pass:
- Primary: `EdtGZ` - lane architecture matches signal -> research -> outbound -> HubSpot governance.
- Alternate: `KVqAt` - stage-card architecture fits AI/data/actions but less suited to outbound governance.
- Supporting: `pAw6X` - borrow layer-card rhythm and icon treatment.
- Live inspection: `EdtGZ` read with Pencil `batch_get`; selected lane/card/connector anatomy.
- Not using: `nRPmP` too circular for this sequence; `tMsEe` too source-taxonomy heavy.
```

The final audit must be able to trace the output back to the chosen node IDs or explain why a different Playground node was better.

## Hard Fail Conditions

- The design uses MAN Digital colors/fonts but no explicit Playground node lineage.
- The candidate pass mentions the registry but does not name exact node IDs.
- The selected node was not inspected live with Pencil before being copied or recreated.
- The output is built from generic rectangles/cards even though a listed node contains a suitable layout, connector, card, icon, screenshot, or depth system.
- The audit cannot say which Playground components shaped the result.
