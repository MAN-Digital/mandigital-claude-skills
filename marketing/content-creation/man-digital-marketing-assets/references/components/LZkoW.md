# LZkoW - Outreach To HubSpot Sync Model

Source: `/Users/romeoman/Documents/Marketing/Design/Pencil/Playground.pen`

Observed frame: `Prospecting Agent vs Outbound-04`, 1190 x 1684.

Figma lineage: this is the Playground canonical implementation of the Figma-derived `Prospecting Agent vs Outbound-04` pattern documented in `../figma-patterns.md` from Figma node `1091:3034`.

## Role

Use for HubSpot sync, outbound-to-CRM, enrichment, governance, and "what should enter the CRM?" workflow graphics.

## Visual Structure

- Vertical blog/explainer frame.
- Header: `When to Sync Cold Outreach Into HubSpot`.
- Left column: Outside HubSpot activity.
- Center column: Sync Rules.
- Right column: Inside HubSpot records and processes.
- Bottom band: `Why this matters` benefits.
- Blue connectors run from outside systems through sync rules into HubSpot actions.

## Column Content

| Area | Main role | Visible content |
| --- | --- | --- |
| Outside HubSpot | Cold outreach activity before CRM sync | Target account lists, cold prospects, outbound campaigns, deliverability metrics, mailbox infrastructure. |
| Sync Rules | Governance filter | Sync when any of these happen: positive reply received, meeting booked or requested, target account confirmed, manual/AI engagement scored or advanced, owner assigned. Do not sync everything: avoid workflow overload, avoid irrelevant rows, reduce duplicates, protect data hygiene. |
| Inside HubSpot | CRM-side actions after qualification | Create lead object, enrich/dedupe, associate to company/contact, pre-sales follow-up, AE handoff, opportunity. |
| Why this matters | Bottom outcome strip | Cleaner CRM, safer automation, better ownership, clearer pipeline. |

## Editing Notes

This is the best base for CRM integration and governance topics. Use real HubSpot assets from the design system when adding or changing HubSpot marks. Keep the center sync rules strict; this frame is about protecting CRM quality, not pushing every contact into HubSpot.

## Reuse Guidance

- Use `LZkoW` as the canonical source, not a separate test `.pen` file or a recreated scratch frame.
- Inspect live with Pencil `batch_get` before adapting it.
- Copy the smallest useful anatomy into the prompt-specific output `.pen`: the three-column governance model, the sync-rule center panel, the outcome strip, the icon-plus-text cards, or the connector marks.
- Do not paste a screenshot of `LZkoW` into a new file. Keep cards, text, rules, icons, connectors, and outcome cells editable.
- If the requested graphic is not about outside/inside governance, sync rules, or CRM entry criteria, compare `LZkoW` against `EdtGZ`, `sQ8TR`, `pAw6X`, and the master nodes before choosing it.

## Audit Risks

- The bottom `Why this matters` strip must remain part of the vertical flow. It should not overlap lower cards or feel detached by a large dead gap.
- Center rule content should be concise; too many rules make the middle column dense and reduce mobile readability.
- The connectors are intentionally minimal. Do not turn this into a web of long spaghetti lines.
