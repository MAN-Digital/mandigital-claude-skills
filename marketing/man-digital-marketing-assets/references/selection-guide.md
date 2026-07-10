# Selection Guide

Use this before choosing a Pencil base. Prefer the closest existing template over creating a new composition.

Read `graphic-styles.md` first. Choose the graphic style family before choosing a specific node. Then read `playground-candidate-roster.md` and name exact candidate node IDs before building. For HubSpot, RevOps, CRM, signal, routing, scoring, AI, revenue-engine, workflow, pipeline, or operating-model graphics, read `master-template-fit-map.md` before choosing outside `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, or `llyux`.

## Mandatory Library Scan

Before selecting a base, run `library-scan-loop.md`.

- Search the registry and preview files by output type, narrative pattern, and prompt-specific terms.
- Run the high-value candidate roster pass from `playground-candidate-roster.md`; choose a primary, alternate, and supporting node by ID.
- For HubSpot/RevOps/signal/CRM prompts, score `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, and `llyux` as primary, secondary, depth, or not-fit before considering primitives.
- Inspect live Playground candidates with Pencil `batch_get` when the written references are not enough.
- Inspect the selected primary candidate with Pencil `batch_get` even when the written reference looks clear. The live Playground is the source of truth.
- Compare at least three candidates for open-ended prompts: primary layout, alternate layout family, and supporting component system.
- Choose the smallest mature component that fits: whole frame, card system, connector system, icon treatment, label pins, callout anatomy, screenshot frame, logo treatment, or spacing model.
- Do not start from blank or primitive-only construction until the scan shows the library does not have a useful base.

## By Output Channel

| Need | Default base family |
| --- | --- |
| Blog graphic / article image | Start from blog-safe 1200 x 630 composition; adapt a cover component only after removing slide/deck chrome |
| Blog hero / Open Graph | 1200 x 630 composition using cover visual language from `V55uo`, `El1Np`, `1GRXD`, `x73R0`, `loMOa` as inspiration, not slide grammar |
| Website hero, explicit 16:9 | 16:9 covers: `V55uo`, `El1Np`, `1GRXD`, `x73R0`, `loMOa` |
| Blog inline explainer | 1190 x 1684 explainer frames: `KVqAt`, `tMsEe`, `b8SoH`, `llyux`, `S20AXj` series |
| LinkedIn feed single image | 1080 x 1350: cover 4:5 variants or Prospecting-Agent sequence |
| LinkedIn carousel slide | Slide 2-7 pattern families, matching the requested format |
| Square post | 1080 x 1080 cover or Slide 2-7 square templates |
| HubSpot/RevOps architecture | `KVqAt`, `tMsEe`, `b8SoH`, `LZkoW`, `pAw6X` |
| Summary/takeaway | `fKn3K`, `LGDxt`, `RXIfB`, `HoOjV` |
| Lucidchart-style flow/system diagram | `KVqAt`, `tMsEe`, `b8SoH`, `llyux`, `EdtGZ`, `VSVo4`, `wTMqf`, `IfWXj`, `ONaC7` |
| Prospecting Agent / outbound article explainer | `S20AXj`, `l5NNCU`, `EdtGZ`, `LZkoW`, `sQ8TR`, `pAw6X`, `fKn3K`, `PPpdM`, `s2ZqRB` |
| Screenshot-driven walkthrough | `G7EWZ`, `G6YkCq`, `nia9w`, `DJN2N`, `jNmrp` |
| Setup / prerequisite / rollout model | `SbBJV`, `NhErk`, `Y3Tzyc`, `zuu8y`, `lP11x` |

## By Narrative Pattern

| Narrative | Prefer |
| --- | --- |
| Strong cover / thesis | `V55uo`, `El1Np`, `nXTXW`, `dI0RZ`, `S20AXj`, `PPpdM` |
| Signal system / revenue engine | `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, `llyux` |
| Prospecting architecture / outbound system | `EdtGZ`, `LZkoW`, `v5aVuG`, `lLDFt`, `PPpdM` |
| Prospecting setup / workflow walkthrough | `SbBJV`, `G7EWZ`, `G6YkCq`, `nia9w`, `DJN2N`, `jNmrp` |
| Rollout / prerequisites / economics | `NhErk`, `Y3Tzyc`, `zuu8y`, `lP11x` |
| Problem and fix | `5MGHD`, `lk5IY`, `nYhge`, `s2Djt`, `S83Yn`, `sW4Qc` |
| List of points | `M9Mwq`, `AGj6s`, `xzcQj`, `KTCK6`, `xrbbT`, `69qqe` |
| Step-by-step process | `VqQ1q`, `XU9Jh`, `IfWXj`, `DSNAg`, `Ss4XV`, `enyqD` |
| Before/after comparison | `MEygm`, `pNnmc`, `pArwu`, `4XjgY`, `PCERa`, `Gagt6` |
| Data or metric story | `V5iH8`, `rOwJz`, `1LmMQ`, `ANwLg`, `Wn3fM`, `TEAdJ` |
| Contrarian claim | `chxsV`, `Uyaly`, `kRJNr`, `mGR6X`, `OxE0i`, `6YYmt` |
| Decision criteria | `dSYM9`, `5kXd2`, `VoeXd`, `sLRvD`, `uGUnu`, `IqpRv` |
| Timeline / roadmap | `9QojL`, `WsUV2`, `UE3nt`, `fVYda` |
| Priority stack / layers | `ul9DN`, `DIdDa`, `r4XvN`, `1wobI`, `pAw6X`, `llyux` |
| Lifecycle / loop | `jWyvs`, `u7BvG`, `sQ8TR` |
| Scorecard / assessment | `gASqb`, `RXIfB` |
| Pitfalls / warnings | `ffT7v`, `DW3dd` |

## Selection Rules

1. Match format first, narrative second, decoration last.
2. If the user asks for a blog graphic but gives no size, use 1200 x 630. Use 1190 x 1684 only when the prompt clearly asks for an inline explainer or dense diagram.
3. If the user asks for LinkedIn without specifying carousel, use 1080 x 1350.
4. If a template exists in the right size, do not resize a different format unless the user asks for a custom format.
5. Because the exported graphic is a static image, choose a size/layout that stays readable at the smallest likely display width. If a 1190 x 1684 explainer is adapted to a 1200 x 630 hero, simplify the content rather than shrinking labels.
6. When unsure between two visually similar templates, inspect their previews in `assets/previews/playground/`.
7. For carousel-derived work, read `gemini-pencil-learnings.md` and apply the cover/content/footer/indicator rules.
8. If adapting a slide/cover component into a blog graphic, remove page numbers, footer bars, slide labels, and carousel indicators.
9. Brand-system-only builds fail. The selected base must identify exact Playground node lineage or explain which non-roster Playground node was inspected and used.
