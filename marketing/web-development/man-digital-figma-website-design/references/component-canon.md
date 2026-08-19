# Canonical website components

Use this map when a MAN Digital website page includes these recurring sections. Clone the
source node, preserve its visual grammar, and adapt only the approved copy and responsive
layout. Screenshot the result at both breakpoints.

## Source map

| Pattern | Canonical source | Required treatment |
| --- | --- | --- |
| Hero shell | `40000296:2361` | Reuse the service-page hero composition. When the service sits inside the revenue bow tie, highlight its exact position using `40000296:8615` as the process reference. |
| Implementation / Onboarding | Standard Desktop `40000833:9279`, Mobile `40000836:3188`; Detailed Desktop `40001088:3017`, Mobile `40001088:3144` | Use the visible five-stage timeline for project delivery. Choose Detailed when every stage needs work, client responsibility and a decision gate. Keep instances attached and apply the complete contract below. |
| ARC method | Desktop `40000833:9341`; Mobile `40000836:3236` | ARC is MAN Digital's operating method: **Architect → Run → Compound**. These phase names are canonical; `Realise` and `Build` are not valid substitutes for `Run`. Instantiate the canonical component and follow the complete ARC contract below; never redraw it as generic process cards. |
| Delivery team | `40000296:9063`; compact row `40000299:30340` | Place the delivery team directly **under** accountable founder cards. Desktop uses the full compact row. Mobile uses a clipped horizontal carousel with a clear swipe cue; keep every team card in the scroll content. |
| Full strategy-call form | `40000308:2538` | Use the complete form composition, not a compact four-field substitute. Preserve first/last name, business email, phone, help, website, referral source, consent controls, privacy copy, reCAPTCHA and the orange primary CTA. Reflow vertically on mobile at the 16/24 reading floor. |
| FAQ | Full section `40000296:9168`; composition group `40000296:9169` | The user-linked `40000296:9170` is only the background rectangle. Clone the full composition: left headline/decorative rail plus right accordion, first answer open, blue plus/minus controls. Extend the accordion to the brief's exact visible questions and create open-state references. |
| Badges and accreditations | `40000311:2403` and Design System badge library | Feature the service-specific capability first. For Quote-to-Cash, make Quote-to-Cash Capability the dominant proof; Elite, Onboarding, CRM Implementation, Custom Integration and relevant industry badges support it. Never enlarge generic partner status above the service credential. |
| Decorative motifs | Page `40000579:2358` | Clone existing motif assets. Use at most one composite motif per section, behind content, distributed through long pages, flat and never over text. |
| Pagination | Component set `40000829:2707` | Reuse the Desktop Counter, Mobile Counter or Mobile Dots variant. Case Studies and Team must contain an instance of this family; never redraw their arrows, counter or dots. |
| Playbooks | Desktop component set `40000832:29581`; mobile component `40000836:3319` | Reuse the four category states and the coded 24-panel DOM contract. Mobile changes layout, not content or state semantics. |
| Quote-to-Cash outcome tabs | Desktop component set `40000832:30153`; rule source `40000823:2422` | Reuse the five governed states. No approved mobile component exists; do not invent or auto-stack one. |
| Service Scope Disclosure | Desktop set `40001115:3242`; Mobile set `40001115:3473`; chapter `40001114:3012`; rules `40001114:3029` | Reuse the five-state responsive disclosure for grouped service capabilities. Canonical sets own all states; page instances stay attached and generic reference boards must not duplicate them. |

The full numbered section inventory and HubSpot source mapping lives in
`canonical-page-sections.md`. Its component IDs override older reference-frame-only
chapters when a reusable asset exists.

## Implementation / Onboarding contract

Use this contract when a page explains the stages of an implementation, onboarding or
other client delivery sequence. It is different from ARC: ARC explains the MAN Digital
method; Onboarding explains the concrete project run.

1. **Choose the density variant.** Use Standard Desktop `40000833:9279` and Mobile
   `40000836:3188` when each stage has a short output list. Use Detailed Desktop
   `40001088:3017` and Mobile `40001088:3144` when each stage must preserve three
   complete content slots: delivery work, client responsibility and decision gate.
   Instantiate the component and keep the page instance attached.
2. **Keep one visible sequence.** Desktop uses five equal columns under one continuous
   stage rail, ordered 01 through 05. Mobile stacks the same five cards in the same order.
   This is not a tab, carousel, accordion or app selector. Do not hide four stages behind
   a selected state and do not create pagination for a five-stage implementation.
3. **Preserve the content contract.** Every detailed stage contains: stage number, stage
   title, fixed `WORK → CLIENT → GATE` metadata, then exactly three bullets in that order.
   All brief-owned work, client input, dependencies and decisions remain represented.
   Tighten syntax only after an editing-checklist pass; never delete a field or decision
   to satisfy a fixed frame height. Cards and their section grow with content.
4. **Use the service-page type contract.** The section eyebrow is Lato Bold **13/18
   desktop** and **11/16 mobile**, uppercase with 2px tracking. Desktop H2 is 44/52;
   mobile H2 is 26/31.2. Introduction and stage bullets are at least **16/24** at both
   breakpoints; only stage markers and the fixed metadata may be smaller. Long mobile
   titles use a fixed content width with height auto-resize, never auto-width clipping.
5. **Keep colour and hierarchy semantic.** Stage 01 may use Primary Blue `#000FC4` with
   white type to establish the start; remaining cards use the approved light surface.
   Dark Navy `#161654` remains mobile-quote-card-only and CTA Orange `#F26620` remains
   conversion-only. Keep the rail and card rhythm simple; do not add decorative arches,
   connector webs or unrelated process illustrations.
6. **Align markers and checks as one system.** Detailed Desktop uses 12px stage dots
   vertically centred on a 2px timeline rule. The rule begins at the centre of Stage 01
   and ends at the centre of Stage 05; it never runs past the final marker. At both
   breakpoints, every bullet uses a transparent 16×24 icon slot aligned to the first
   24px text line, with the check path centred inside it and drawn with a 2px round stroke.
   Keep the slot unfilled: checks are white on the Primary Blue Stage 01 card and Primary
   Blue on light cards. Preserve the approved text start with a 6px desktop row gap and
   4px mobile row gap; do not top-align a bare 12–14px SVG frame beside multiline copy.
7. **Reuse the shipped implementation.** The component maps to
   `sections/05-onboarding.html` and `.rv-onboarding`. Extend that section's existing
   markup and styles for the Detailed content slots; do not create a second onboarding
   module or parallel class family. Render all five stages in source/DOM order. Use
   semantic list/card markup and stable stage IDs; desktop is a five-column layout and
   mobile is a natural vertical stack. JavaScript is not required for disclosure.
   Motion, if added, is progressive enhancement and must respect reduced-motion settings.
8. **Run the content and visual gates.** When an editor pass is requested, load
   `../../content-creation/editing-checklist/SKILL.md`, document all eight checks, and
   run both enforcement scripts before inserting final copy. Then screenshot the source
   and one real instance at each breakpoint. Verify all five stages, 15 detailed bullets,
   attached instances, 16/24 reading copy, title wrapping, equal desktop card heights,
   no clipping and no adjacent-section overlap.

## ARC component contract

Use this contract whenever a page explains MAN Digital's method, delivery model or
continuous-improvement approach.

1. **Reuse the source.** Instantiate Desktop `40000833:9341` and Mobile
   `40000836:3236`. Keep the instance attached. Put reusable structural corrections in
   the canonical source; use instance overrides only for page-owned copy. Never detach,
   redraw or create a parallel roadmap component. The mapped implementation remains
   `sections/06-roadmap.html` and `.rv-roadmap`.
2. **Keep ARC recognisable.** Preserve exactly three ordered phases—**Architect →
   Run → Compound**—with phase numbers, one taxonomy label and exactly three concise
   actions per phase. Preserve the desktop legend and its bullet-colour mapping. Mobile
   uses the approved stacked cards and does not inherit desktop table decoration.
   Never relabel the middle phase as `Realise` or `Build`; those words may appear only
   where the page brief legitimately uses them outside the ARC phase names.
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

## Service Scope Disclosure contract

Use this family when a service page needs to group a long, brief-owned capability scope
without turning the section into pricing cards, a dense bento grid, or application UI.

1. **Reuse the responsive source.** Instantiate Desktop set `40001115:3242` or Mobile
   set `40001115:3473` from chapter `40001114:3012`. Keep page use attached. Structural
   corrections belong in the canonical component; page instances override only approved
   copy. The complete in-canvas rules group is `40001114:3029`. Approved Quote-to-Cash
   page uses are Desktop instance `40001116:3030` and Mobile instance `40001116:3068`.
2. **Preserve the five-state content model.** Keep exactly five ordered `Open` variants:
   Commercial workflow, Contract to cash, Connected systems, Governance & insight, and
   Adoption that holds. Exactly one group is open in each state. Every brief-owned
   capability remains designed into its group and present in source/DOM order; never
   replace content with `+N more`, counts, package names, tier labels, or placeholder UI.
3. **Use it only for service scope.** This family describes what MAN Digital can shape,
   configure, connect, govern, and embed. It is not FAQ, Onboarding, ARC, Playbooks,
   outcome tabs, pricing, or a qualification flow. Reuse those canonical families for
   their own jobs.
4. **Keep the approved responsive geometry.** Desktop uses the wide horizontal section
   and Mobile uses the compact vertical stack. Preserve the source padding, dividers,
   open-state rhythm, icon alignment, and equal closed-row spacing. Group titles are
   Lato Bold 18/24; capability copy is Lato Regular 16/24. The normal section eyebrow
   remains 13/18 Desktop and 11/16 Mobile with the canonical uppercase tracking.
5. **Keep colours semantic.** Use Primary Blue `#000FC4` for the active/open treatment,
   the approved light neutral surfaces and standard body greys. Dark Navy `#161654` is
   mobile-quote-card-only. CTA Orange `#F26620` is conversion-only and must not mark an
   open row, disclosure icon, count, or decoration.
6. **Let the component sets own the state references.** The Desktop and Mobile component
   sets are the complete state documentation. Do not copy these ten states into generic
   `Interaction State References` boards, scatter page-local duplicates beside a layout,
   or create a second component family. The obsolete generic Desktop and Mobile reference
   boards were deleted; do not recreate them. Keep only the canonical component sets,
   attached page instances and one shared rules group for both breakpoints.
7. **Implement as an accessible disclosure.** Use headings containing native buttons,
   stable IDs, `aria-expanded`, and `aria-controls`; preserve logical source order and
   keep every capability in the source DOM for AEO. JavaScript progressively controls
   one-open-at-a-time behavior. Keyboard focus must remain visible, touch targets must
   meet 44px, and reduced motion must not block state changes.
8. **Verify HubSpot before coding.** As of 2026-08-19, no approved HubSpot module has
   been mapped to this family. Search the active theme for an equivalent disclosure
   before implementation. If none exists, mark the mapping `[future]` and implement the
   contract deliberately; do not borrow FAQ markup or styling without verification.
9. **QA every state and one real use.** Screenshot all five Desktop variants, all five
   Mobile variants, and at least one attached page instance at each breakpoint. Verify
   one open group, no clipped labels, all capabilities in the source component, 18/24
   titles, 16/24 body copy, approved colours, and no duplicate states in generic boards.

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

For adjacent sections, change the reading action when two selectors would compete. The
canonical Service Scope Disclosure is the default grouped-scope pattern, but it must be
composition-tested beside tabs, steppers and other disclosures. Keep every briefed
capability available and never collapse the remainder into `+N more`; if the page needs a
different rhythm, create a reviewed variant in the canonical family rather than a local
lookalike.

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
