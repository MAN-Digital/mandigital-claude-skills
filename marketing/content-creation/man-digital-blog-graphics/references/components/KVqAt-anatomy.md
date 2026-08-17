# KVqAt Anatomy - HubSpot Signal Engine Architecture

Source: `/Users/romeoman/Documents/Marketing/Design/Pencil/Playground.pen`

Top node: `KVqAt`, 1190 x 1684, light blue architecture graphic.

## Composite Role

Use `KVqAt` when the graphic needs to explain how AI fits into a HubSpot signal system without implying AI replaces the whole system. The visual story is: signals enter, HubSpot data structures organize them, AI interprets them, actions are triggered, and revenue outcomes are measured.

This is a five-stage architecture diagram, not a generic card grid. It works best for educational blog graphics, RevOps diagrams, HubSpot process explainers, AI-in-GTM explainers, and LinkedIn carousel-derived architecture slides.

## Frame-Level Anatomy

| Node ID | Role | Description | Use when |
| --- | --- | --- | --- |
| `exi7v` | Logo group | Top-left MAN Digital logo. | Need a light-background brand mark in the header. |
| `kNIBf` | Main title | Large Montserrat title: `Where AI Fits in the HubSpot Signal Engine`. | Need a strong architecture headline. |
| `sQk0c` | Side thesis | Right-side statement: AI interprets signals and recommends actions, not replaces the system. | Need a short framing statement beside the title. |
| `xLkzv` | Background ellipse | Oversized pale blue ellipse behind the content. | Need soft structure on a light frame. |
| `Tfevq` | Main connector path | Large blue path connecting the top and bottom architecture rows. | Need the five cards to read as one connected system. |
| `voulE` | Stage card 1 | Signal Inputs card with four signal-source pills. | Need to show raw inputs feeding the system. |
| `GGxl2` | Stage card 2 | Signal HubSpot Data Layer card with five CRM/data pills. | Need to show HubSpot-owned structured data. |
| `rRoSd` | Stage card 3 | AI Interpretation card with five AI output pills. | Need to show AI analysis/recommendation layer. |
| `LQxPS` | Stage card 4 | Action Layer card with five activation pills. | Need to show GTM execution actions. |
| `l6jnb` | Stage card 5 | Revenue Outcome card with four outcome pills. | Need to show measurable revenue outputs. |
| `g0uwc` | Signal icon medallion | Pale circular medallion with signal/wifi icon above Signal Inputs. | Need a source/input stage marker. |
| `cRGY1` | Data icon medallion | Pale circular medallion with database icon above Data Layer. | Need a data/platform stage marker. |
| `CK187` | AI icon medallion | Pale circular medallion with sparkle icon above AI Interpretation. | Need an AI/recommendation stage marker. |
| `L6sz6` | Action icon medallion | Pale circular medallion with cursor/action icon above Action Layer. | Need an activation stage marker. |
| `CW9op` | Outcome icon medallion | Pale circular medallion with chart icon above Revenue Outcome. | Need a results/measurement stage marker. |
| `B7kMJ` | Dot decoration | Small top-right dot-grid cluster. | Need subtle texture in light negative space. |
| `gLgmf` | Dot decoration | Mid-right dot-grid cluster near the lower cards. | Need to balance the right side of the frame. |
| `rIUUB` | Dot decoration | Bottom-left dot-grid cluster. | Need to balance the lower-left negative space. |

## Stage Cards

All five stage cards use the same system: white rounded card, centered title, stacked light pills, Medium Blue icons, and pale blue pill strokes. Clone the whole card when changing a stage; clone individual pill rows only when adding a matching list item.

| Node ID | Stage | Card title node | Pill list node | Native pills |
| --- | --- | --- | --- | --- |
| `voulE` | Signal Inputs | `sPPV6` | `IkQ6X` | `XlJSz`, `pDKxe`, `wcgGl`, `D4tA8` |
| `GGxl2` | Signal HubSpot Data Layer | `yXx0Q` | `ubCCJ` | `QOl9O`, `FWG3n`, `p6I4L`, `STUSm`, `K9BnU` |
| `rRoSd` | AI Interpretation | `P6DPKX` | `Y6Cu9V` | `A4PRC0`, `DqvaN`, `K3lUTV`, `r4H9R`, `ppwVj` |
| `LQxPS` | Action Layer | `lVHUK` | `D2OKU` | `SFEJX`, `V4qUYI`, `aCh62`, `PmwYY`, `XRpJ2` |
| `l6jnb` | Revenue Outcome | `vthJB` | `Sc4jg` | `gNA5Z`, `gGhJq`, `naIqG`, `HPD8m` |

## Stage 1: Signal Inputs `voulE`

Use this card for raw signals before HubSpot structure or AI interpretation.

| Node ID | Label | Meaning | Use when |
| --- | --- | --- | --- |
| `XlJSz` | Visitor intent | Website behavior, anonymous visitor activity, intent activity. | The input is digital behavior. |
| `pDKxe` | Research intent | Search, content consumption, third-party research activity. | The input is buying research. |
| `wcgGl` | News & hiring signals | Company news, hiring, funding, expansion, business changes. | The input is external account activity. |
| `D4tA8` | Custom signals | Proprietary or configured signal definitions. | The input is custom to the client or workflow. |

## Stage 2: Signal HubSpot Data Layer `GGxl2`

Use this card for data that lives in or is synchronized into HubSpot.

| Node ID | Label | Meaning | Use when |
| --- | --- | --- | --- |
| `QOl9O` | Company properties | Account/company fields and firmographic data. | Explaining account records. |
| `FWG3n` | Contact properties | Person/contact fields and contact-level profile data. | Explaining contact records. |
| `p6I4L` | Custom events | Behavioral events, lifecycle events, or product/marketing events. | Explaining tracked events. |
| `STUSm` | Segments | Lists, audiences, or grouped accounts/contacts. | Explaining segmentation. |
| `K9BnU` | Lead scores | Fit, engagement, intent, or readiness scores. | Explaining scoring models. |

## Stage 3: AI Interpretation `rRoSd`

Use this card for what AI generates from the structured signal/data layer.

| Node ID | Label | Meaning | Use when |
| --- | --- | --- | --- |
| `A4PRC0` | Account summary | Condensed account context. | AI summarizes account state. |
| `DqvaN` | Buying-stage hypothesis | AI estimates where the buyer is in the journey. | AI interprets buying readiness. |
| `K3lUTV` | Pain-point hypothesis | AI infers likely business pain. | AI maps signals to pain points. |
| `r4H9R` | Suggested message | AI drafts or recommends messaging. | AI guides outreach copy. |
| `ppwVj` | Next best action | AI recommends what to do next. | AI supports workflow decisions. |

## Stage 4: Action Layer `LQxPS`

Use this card for execution channels and operational actions.

| Node ID | Label | Meaning | Use when |
| --- | --- | --- | --- |
| `SFEJX` | SDR task | A sales task or rep follow-up. | Routing to a person. |
| `V4qUYI` | Sequence | Sales/marketing sequence enrollment. | Triggering multi-step outreach. |
| `aCh62` | Email | One-to-one or automated email. | Sending message-based activation. |
| `PmwYY` | Ad audience | Paid-media or retargeting audience. | Syncing to advertising or audiences. |
| `XRpJ2` | Workflow | HubSpot workflow or automation. | Triggering automation. |

## Stage 5: Revenue Outcome `l6jnb`

Use this card for the measurable commercial result of the system.

| Node ID | Label | Meaning | Use when |
| --- | --- | --- | --- |
| `gNA5Z` | Meeting | Meeting booking or sales conversation. | The outcome is a meeting. |
| `gGhJq` | Opportunity | Qualified opportunity creation. | The outcome is pipeline creation. |
| `naIqG` | Pipeline | Pipeline volume or stage progression. | The outcome is pipeline movement. |
| `HPD8m` | ROI | Measurement of revenue return. | The outcome is performance proof. |

## Connectors

`Tfevq` is the main connector path that wraps from the top row to the lower row. Small connector pieces include `pG8kl`, `Erhgk`, `l3YDo`, `la9Lo`, `PMOiv`, and `Q0ykY8`.

Use the connector system when cards should read as one connected architecture. Do not delete connector pieces casually; if a card moves, adjust the connector path and screenshot the whole frame.

## Reuse Rules

- Clone `KVqAt` for a complete five-stage architecture.
- Clone a stage card when a new graphic needs one of the five conceptual buckets.
- Clone individual pill rows only inside a matching card style.
- Keep the stage order unless the prompt explicitly asks for a different model.
- Keep AI Interpretation between HubSpot Data Layer and Action Layer. That is the strategic point of this graphic.
- Use `nRPmP` instead if the story should feel like a flywheel; use `KVqAt` when the story is a system architecture.

## Coverage Boundary

This registry documents reusable semantic components: stage cards, pill rows, icon medallions, title/statement blocks, connector groups, and decorations. It does not create separate prose files for every raw vector path inside icons, logo glyphs, dot grids, or connector paths because those primitives are not useful standalone components.
