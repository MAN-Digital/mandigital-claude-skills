# Canonical website components

Use this map when a MAN Digital website page includes these recurring sections. Clone the
source node, preserve its visual grammar, and adapt only the approved copy and responsive
layout. Screenshot the result at both breakpoints.

## Source map

| Pattern | Canonical source | Required treatment |
| --- | --- | --- |
| Hero shell | `40000296:2361` | Reuse the service-page hero composition. When the service sits inside the revenue bow tie, highlight its exact position using `40000296:8615` as the process reference. |
| Delivery team | `40000296:9063`; compact row `40000299:30340` | Place the delivery team directly **under** accountable founder cards. Desktop uses the full compact row. Mobile uses a clipped horizontal carousel with a clear swipe cue; keep every team card in the scroll content. |
| Full strategy-call form | `40000308:2538` | Use the complete form composition, not a compact four-field substitute. Preserve first/last name, business email, phone, help, website, referral source, consent controls, privacy copy, reCAPTCHA and the orange primary CTA. Reflow vertically on mobile at the 16/24 reading floor. |
| FAQ | Full section `40000296:9168`; composition group `40000296:9169` | The user-linked `40000296:9170` is only the background rectangle. Clone the full composition: left headline/decorative rail plus right accordion, first answer open, blue plus/minus controls. Extend the accordion to the brief's exact visible questions and create open-state references. |
| Badges and accreditations | `40000311:2403` and Design System badge library | Feature the service-specific capability first. For Quote-to-Cash, make Quote-to-Cash Capability the dominant proof; Elite, Onboarding, CRM Implementation, Custom Integration and relevant industry badges support it. Never enlarge generic partner status above the service credential. |
| Decorative motifs | Page `40000579:2358` | Clone existing motif assets. Use at most one composite motif per section, behind content, distributed through long pages, flat and never over text. |

## Interaction content contract

For each process tab, create a separate named state at desktop and mobile with all five
fields designed in:

1. stage label/number;
2. stage title;
3. What we do;
4. What you own;
5. Decision gate.

Keep the full selector visible in every state and change only the selected treatment and
the five content fields. Do not provide one detailed state plus empty placeholder tabs.

### Outcome/transformation tabs

Use this contract when tabs compare "where revenue gets stuck" with a governed HubSpot
workflow:

1. Preserve the approved before/after statements for that tab; do not generalize or
   paraphrase the operating problem.
2. Draw the failure side as a concrete sequence: named source systems or artefacts outside
   the workflow, one visible broken-handoff marker, then the disconnected downstream
   object. Use the critical pair `#FDEBEC` / `#9E1C21`; orange remains CTA-only.
3. Draw the governed side with one Primary Blue (`#000FC4`) rule/core and straight,
   readable connectors into the named commercial objects. Connectors never cross labels.
4. Give every state its own sources, disconnected object, governed rule, object labels and
   icons. Never duplicate one diagram and merely relabel the tab.
5. Keep the visual grammar consistent across states: selector position, split point,
   spacing, card dimensions, state counter and 16px minimum content labels.
6. Create one complete named desktop state and one complete named mobile state for every
   tab. Group each breakpoint's states inside one Figma Section named
   `RULE · <page section> — <pattern> · <breakpoint> States 01–N`, with a compact rule
   header above the grid. Keep all state copy designed-in for DOM/AEO implementation.

Decorative arcs, ornamental pipelines and ambiguous AI-drawn vectors are not evidence of
a stuck workflow. Use them only as background decoration elsewhere; this pattern relies on
the broken handoff and disconnected object to communicate the failure immediately.

For adjacent sections, change the interaction model. If implementation uses a stepper or
master-detail tabs, present service scope as a Mobbin-informed bento/grouped-card system,
not another selector beside another detail panel. Every briefed capability stays visible;
do not collapse the remainder into `+N more`.

## Logo contrast

Use approved white/reversed logos on dark, navy, blue or other brand-colour backgrounds.
Use approved dark or full-colour logos on light backgrounds. Never mix treatments within
one logo row, proof strip or section.
