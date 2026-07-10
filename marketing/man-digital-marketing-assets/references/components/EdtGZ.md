# EdtGZ - Prospecting Operating Architecture

Source: `/Users/romeoman/Documents/Marketing/Design/Pencil/Playground.pen`

Observed frame: `Prospecting Agent vs Outbound-03`, 1190 x 1684.

## Role

Use for operational architecture diagrams that show how signal inputs, HubSpot context, research/qualification, outbound execution, deliverability, and handoff connect.

## Visual Structure

- Vertical blog/explainer frame.
- Header: `The Hybrid Prospecting Architecture`.
- Left/top card: Signal Inputs.
- Middle/top card: HubSpot lane.
- Left/lower card: Research + Qualification Layer.
- Middle/lower card: Outbound lane.
- Center diamond decision: `Known account with strong intent?`.
- Right insight cards: best-practice context note and deliverability checklist.
- Bottom bar: Engagement + Handoff sequence.
- MAN Digital light-card styling with blue connectors and orange emphasis for HubSpot-side items.

## Architecture Content

| Area | Node ID | Content |
| --- | --- | --- |
| Signal Inputs | `qJDgf` | Visitor intent, buying intent, CRM history, firmographic enrichment, company news, job changes. |
| HubSpot lane | `qBrvo` | Owner visibility, warm outreach, tasking and sequencing, sales coordination. |
| Research + Qualification Layer | `NvBTs` | FitSpot context, prospecting agent, Apify/ZoomInfo, personalization research. |
| Outbound lane | `L4Tph8` | Multiple inboxes, domain setup, warm-up, mailbox rotation, plain-text cold email, scaled campaigns. |
| Decision | `tMycI` | Known account with strong intent? |
| Yes path | `qctTA` | Routes toward HubSpot lane. |
| No / need scale path | `L4BsQ` | Routes toward outbound lane. |
| Best-practice note | `LcGj0` | Keep execution split, but keep context connected. |
| Deliverability checklist | `NMnG1` | SPF/DKIM/DMARC, warming, no-link copy, reply management. |
| Handoff bar | `wTMqf` | Positive reply -> booked meeting -> create lead in HubSpot -> associate to company/contact -> handoff to AE. |

## Editing Notes

Use when the article needs an operational decision flow. Keep the decision diamond visually obvious, preserve the split between HubSpot coordination and outbound infrastructure, and keep connector labels short.

Read `EdtGZ-anatomy.md` before reusing individual lane, decision, connector, or footer nodes.
