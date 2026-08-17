# Design briefs — how MAN Digital specs a page

Pages usually arrive with a **writer's/design brief** (Google Doc, sometimes a machine-readable
YAML twin named like `brief-lp-<page>-FINAL.yaml`). Treat the brief as the wireframe spec.
Example: "LP Pillar: RCxQuote-to-Cash" (14-section landing page).

What to extract, in order:

1. **Content plan table** — one row per section with: # (order is BINDING), on-page heading,
   Format (this IS the wireframe: "H1, verification line, subhead, 3 tags, badges, CTA,
   client logos" / "6-row table across 5 columns" / "3 tiers with price + deliverables
   table"), word count, audience, and the section's job.
2. **Pattern source column** — each section is marked *Existing pattern* (naming which live
   page it copies: "the 5-step onboarding module from /revops-service"), *Pattern changed*
   (with the reason, often AEO extractability), or *New element*. Existing-pattern sections:
   CLONE the section from the source page's Figma frames or screenshot the live page —
   never redesign them. New elements: Mobbin inspiration → variants → owner picks.
3. **Reader's-path table** — which question each section answers; explains and locks the order.
4. **Implementation requirements** — real tables as tables (not images), visible content
   (no display:none), heading hierarchy, ids, JSON-LD; these constrain the DESIGN too
   (e.g. a comparison must be designed as a real table, disclosure content designed-in).
5. **Audience per section** — drives density/tone of the design (CFO sections = tables and
   numbers; CRO sections = narrative + proof).

YAML briefs mirror the doc (template_metadata, lp_identity, section list) — same extraction.
The brief's copy is often placeholder-final ("[TO BE ADDED]" markers stay visible in the
design as labeled placeholders — never invent data, quotes, or numbers to fill them).
