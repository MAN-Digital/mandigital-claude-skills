# Canonical website components

Use this map when a MAN Digital website page includes these recurring sections. Clone the
source node, preserve its visual grammar, and adapt only the approved copy and responsive
layout. Screenshot the result at both breakpoints.

## Source map

| Pattern | Canonical source | Required treatment |
| --- | --- | --- |
| Hero shell | `40000296:2361` | Reuse the service-page hero composition. When the service sits inside the revenue bow tie, highlight its exact position using `40000296:8615` as the process reference. |
| ARC method | Desktop `40000833:9341`; Mobile `40000836:3236` | ARC is MAN Digital's operating method: **Architect → Realise → Compound**. Instantiate the canonical component and follow the complete ARC contract below; never redraw it as generic process cards. |
| Delivery team | `40000296:9063`; compact row `40000299:30340` | Place the delivery team directly **under** accountable founder cards. Desktop uses the full compact row. Mobile uses a clipped horizontal carousel with a clear swipe cue; keep every team card in the scroll content. |
| Full strategy-call form | `40000308:2538` | Use the complete form composition, not a compact four-field substitute. Preserve first/last name, business email, phone, help, website, referral source, consent controls, privacy copy, reCAPTCHA and the orange primary CTA. Reflow vertically on mobile at the 16/24 reading floor. |
| FAQ | Full section `40000296:9168`; composition group `40000296:9169` | The user-linked `40000296:9170` is only the background rectangle. Clone the full composition: left headline/decorative rail plus right accordion, first answer open, blue plus/minus controls. Extend the accordion to the brief's exact visible questions and create open-state references. |
| Badges and accreditations | `40000311:2403` and Design System badge library | Feature the service-specific capability first. For Quote-to-Cash, make Quote-to-Cash Capability the dominant proof; Elite, Onboarding, CRM Implementation, Custom Integration and relevant industry badges support it. Never enlarge generic partner status above the service credential. |
| Decorative motifs | Page `40000579:2358` | Clone existing motif assets. Use at most one composite motif per section, behind content, distributed through long pages, flat and never over text. |
| Pagination | Component set `40000829:2707` | Reuse the Desktop Counter, Mobile Counter or Mobile Dots variant. Case Studies and Team must contain an instance of this family; never redraw their arrows, counter or dots. |
| Playbooks | Desktop component set `40000832:29581`; mobile component `40000836:3319` | Reuse the four category states and the coded 24-panel DOM contract. Mobile changes layout, not content or state semantics. |
| Quote-to-Cash outcome tabs | Desktop component set `40000832:30153`; rule source `40000823:2422` | Reuse the five governed states. No approved mobile component exists; do not invent or auto-stack one. |

The full numbered section inventory and HubSpot source mapping lives in
`canonical-page-sections.md`. Its component IDs override older reference-frame-only
chapters when a reusable asset exists.

## ARC component contract

Use this contract whenever a page explains MAN Digital's method, delivery model or
continuous-improvement approach.

1. **Reuse the source.** Instantiate Desktop `40000833:9341` and Mobile
   `40000836:3236`. Keep the instance attached. Put reusable structural corrections in
   the canonical source; use instance overrides only for page-owned copy. Never detach,
   redraw or create a parallel roadmap component. The mapped implementation remains
   `sections/06-roadmap.html` and `.rv-roadmap`.
2. **Keep ARC recognisable.** Preserve exactly three ordered phases—**Architect →
   Realise → Compound**—with phase numbers, one taxonomy label and exactly three concise
   actions per phase. Preserve the desktop legend and its bullet-colour mapping. Mobile
   uses the approved stacked cards and does not inherit desktop table decoration.
3. **Write for a landing page, not an app.** Treat source wording as illustrative.
   Replace the eyebrow, heading, introduction, taxonomy labels and actions with
   brief-owned copy, then run the editing checklist. Keep actions outcome-led and easy
   to scan; do not add UI commands such as “select a criterion,” helper instructions or
   unexplained labels. Do not invent claims, deliverables or process language.
4. **Use the service-page type contract.** The section eyebrow is Lato Bold **13/18
   desktop** and **11/16 mobile**, uppercase with 2px tracking. It remains a compact
   pre-heading, never a 20px lead. Action copy is Lato Regular **16/24 at both
   breakpoints**, fills the available cell width and never falls back to legacy 15px
   desktop or 14px mobile text. Headline and introduction inherit the Service-LP scale.
   Keep the approved alignment: centered section introduction on desktop and the
   canonical left-aligned mobile composition.
5. **Make the desktop cells optically even.** Use three equal phase cards. Every action
   cell has zero inter-row gap and equal **24px top and bottom padding** around the 24px
   text line. Do not simulate bottom padding with phase or parent `itemSpacing`; inspect
   the visible space above and below every bullet, not only the numeric frame height.
   Keep each bullet and its text vertically centred as one row.
6. **Close the table once.** Use one divider between the card header and the first action,
   then one divider between each action row. The final action has **no closing divider**:
   the card border already closes the group. A second line above the card bottom creates
   an awkward doubled ending.
7. **Keep colour roles semantic.** Use Primary Blue `#000FC4` for the normal ARC brand
   treatment and the approved workflow/adoption colours for bullets and legend. Dark
   Navy `#161654` remains mobile-quote-card-only and CTA Orange `#F26620` remains
   conversion-only; neither becomes an ARC phase or status colour.
8. **Verify source and use.** Screenshot the canonical source and at least one real page
   instance at each breakpoint after a structural edit. Confirm the instance inherited
   the change, all nine actions are visible, desktop rows align, mobile text does not
   clip, dividers do not double, and adjacent sections neither overlap nor acquire an
   unintended gap.

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

## Restricted colour roles

- Primary Blue `#000FC4`: normal hero, section, active and governed states.
- Dark Navy `#161654`: approved mobile quote cards only.
- CTA Orange `#F26620`: conversion actions only; never selected tabs, status or decoration.

Do not copy a legacy fill from an old frame into a new component without checking this
role map.
