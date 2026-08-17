# Canonical page sections and implementation reuse

Last verified against Figma: **2026-08-17**.

This reference is the pre-design and pre-coding gate for MAN Digital website sections.
Use the reusable components on the `🎨 Design System` page before copying a page frame or
creating a new HubSpot module.

## Design System chapter map

Start at [🎨 Design System](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000555-2358&m=dev).

| Chapter | Figma source | Purpose |
| --- | --- | --- |
| 00 Cover & TOC | [40000581:2940](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000581-2940&m=dev) | Design System overview and maintenance context. |
| 01 Foundations — Color | [40000581:2941](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000581-2941&m=dev) | Named brand, extended and semantic colour tokens. |
| 02 Typography | [40000581:2942](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000581-2942&m=dev) | Desktop and mobile type scales. |
| 03 Spacing, Radii, Shadows & Motion | [40000581:2943](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000581-2943&m=dev) | Layout, focus, elevation and motion primitives. |
| 04 Badges & Accreditations | [40000581:2944](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000581-2944&m=dev) | Approved badge-library clone; edit the asset-page master. |
| 05 Navigation & Footer | [40000581:2945](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000581-2945&m=dev) | Desktop/mobile navigation, open mobile state and live footer structure. |
| 06 Components — Desktop | [40000581:2946](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000581-2946&m=dev) | Current flat desktop component language. |
| 07 Components — Mobile | [40000581:2947](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000581-2947&m=dev) | Current flat mobile component language. |
| 08 Inspiration Shelf — Mobbin | [40000581:2948](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000581-2948&m=dev) | Inspiration only; never a direct clone source. |
| 09 Canonical Page Sections — Desktop | [40000828:2707](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000828-2707&m=dev) | Approved 1512px components in page order. |
| 10 Canonical Page Sections — Mobile | [40000828:2708](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000828-2708&m=dev) | Approved 360px components in the same order. |
| 11 Interaction Rules & HubSpot Reuse Map | [40000828:2709](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000828-2709&m=dev) | Variant families, state contracts and implementation mapping. |
| HubSpot Reuse Gate | [40000838:2929](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000838-2929&m=dev) | Visual pre-coding checklist and source index. |

Approved source page frames remain `40000296:2359` (Desktop) and `40000329:2358`
(Mobile). The component chapters are the reuse source; the page frames are composition
references.

## Numbered component and request-alias map

Resolve ordinary request language here before treating a section as new. A match is
**reuse required**: inspect, render, clone and adapt the registered pair.

| # | Section and request aliases | Desktop source | Mobile source | HubSpot implementation |
| --- | --- | --- | --- | --- |
| 01 | **Hero** — hero, landing hero, page hero, first fold | [40000833:8980](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000833-8980&m=dev) | [40000836:2972](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000836-2972&m=dev) | Global theme navigation plus approved page hero. |
| 02 | **Revenue Workflows** — the problem, THE PROBLEM, problem section, pain/friction, where revenue leaks, before/after | [40000833:9074](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000833-9074&m=dev) | [40000836:3045](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000836-3045&m=dev) | `sections/02-workflows.html`, `.rv-workflows`. |
| 03 | **Case Studies** — case studies, customer stories, proof, client proof, examples, work/results | [40000833:9134](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000833-9134&m=dev) | [40000836:3082](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000836-3082&m=dev) | `sections/03-cases.html`, `.rv-cases`, `revops-refresh-2025.js`. |
| 04 | **Fix Banner** — fix banner, statement banner, transition statement, bridge banner | [40000833:9151](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000833-9151&m=dev) | [40000836:3098](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000836-3098&m=dev) | `sections/04-fixbanner.html`, `.rv-fixbanner`. |
| 05 | **Onboarding** — onboarding, how we start, kickoff, first four weeks, implementation start | [40000833:9279](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000833-9279&m=dev) | [40000836:3188](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000836-3188&m=dev) | `sections/05-onboarding.html`, `.rv-onboarding`. |
| 06 | **Roadmap** — roadmap, phases, implementation roadmap, delivery phases, progression | [40000833:9341](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000833-9341&m=dev) | [40000836:3236](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000836-3236&m=dev) | `sections/06-roadmap.html`, `.rv-roadmap`. |
| 07 | **Playbooks** — playbooks, capabilities, category tabs, master-detail, services by function | [set 40000832:29581](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000832-29581&m=dev) | [40000836:3319](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000836-3319&m=dev) | `sections/07-playbooks.html`, `.rv-playbooks`, `revops-refresh-2025.js`. |
| 08 | **Principles** — principles, how we work, operating principles, approach principles | [40000835:3025](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000835-3025&m=dev) | [40000837:2938](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000837-2938&m=dev) | `sections/08-principles.html`, `.rv-principles`. |
| 09 | **Leadership** — leadership, founders, founder section, experts, executive team | [40000835:3055](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000835-3055&m=dev) | [40000837:2963](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000837-2963&m=dev) | `sections/08z-leadership.html`, `.rv-leadership`. |
| 10 | **Team** — team, meet the team, people, specialists, delivery team | [40000835:3130](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000835-3130&m=dev) | [40000837:2992](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000837-2992&m=dev) | `sections/09-team.html`, `.rv-team`, `revops-refresh-2025.js`. |
| 11 | **Credentials** — credentials, accreditations, badges, certifications, HubSpot partner proof | [40000835:3315](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000835-3315&m=dev) | [40000837:3177](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000837-3177&m=dev) | `sections/10-credentials.html`, `.rv-credentials`. |
| 12 | **Strategy-call Form** — strategy call, contact form, book a call, consultation form, HubSpot form | [40000835:30048](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000835-30048&m=dev) | [40000837:3277](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000837-3277&m=dev) | `sections/11-form.html` and the existing HubSpot form embed. |
| 13 | **FAQ** — FAQ, FAQs, questions, common questions, objections, Q&A | [40000835:30110](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000835-30110&m=dev) | [40000837:3318](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000837-3318&m=dev) | `sections/12-faq.html` and accessible disclosure behavior. |
| 14 | **Footer** — footer, global footer, landing-page footer | [40000835:30229](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000835-30229&m=dev) | [40000837:3434](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000837-3434&m=dev) | Active global theme footer. |
| 15 | **Quote-to-Cash Outcome Tabs** — quote-to-cash, QTC outcomes, outcome tabs, pricing/approvals/contracts/billing/visibility | [default Pricing source 40000820:2358](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000820-2358&m=dev) · [family 40000832:30153](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000832-30153&m=dev) | **No approved mobile node** | Code status `[future]`; verify before implementation. |

The correct **Case Studies — Mobile** node is `40000836:3082`.
`40000836:3188` is **Onboarding — Mobile**, not Case Studies.

The canonical HubSpot source checkout is maintained by the `man-digital-cms-pages` skill
under `references/source/pages/revops-service/`. Treat the mapped HTML, CSS and JavaScript
as existing implementation, not inspiration to rebuild.

## Navigation and footer source components

These chapter-05 sources are the reusable global structures. The numbered page-section
nodes above show them in landing-page context.

| Component | Figma source |
| --- | --- |
| Desktop navigation with mega menu | [40000559:29021](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-29021&m=dev) |
| Mobile navigation | [40000559:29212](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-29212&m=dev) |
| Mobile navigation — open state | [40000559:29678](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-29678&m=dev) |
| Desktop footer — live structure | [40000559:30147](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-30147&m=dev) |
| Mobile footer — live structure | [40000559:30262](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-30262&m=dev) |

## Atomic component shelves

### Desktop

| Component | Figma source |
| --- | --- |
| Leak card — dark negative state | [40000559:30725](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-30725&m=dev) |
| Win card — Primary Blue positive state | [40000559:30760](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-30760&m=dev) |
| Playbooks master-detail | [40000559:30795](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-30795&m=dev) |
| Credentials cards | [40000559:30845](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-30845&m=dev) |
| Leadership cards | [40000559:31012](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-31012&m=dev) |
| Founder CTA chip | [40000563:2724](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000563-2724&m=dev) |

### Mobile

| Component | Figma source |
| --- | --- |
| Founder CTA chip | [40000555:2498](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000555-2498&m=dev) |
| Case-study card | [40000555:2505](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000555-2505&m=dev) |
| Onboarding step | [40000559:3114](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-3114&m=dev) |
| Roadmap phase | [40000559:3131](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-3131&m=dev) |
| Principle card | [40000559:3146](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-3146&m=dev) |
| Dark quote card | [40000559:3151](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-3151&m=dev) |
| Credential row | [40000559:3158](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000559-3158&m=dev) |
| FAQ item | [40000563:2727](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000563-2727&m=dev) |
| Statement banner | [40000563:2734](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000563-2734&m=dev) |

## Decorative component registry

`✨ Decorative Elements` is the only page allowed to contain decoration masters. Page
sections and `🎨 Design System` components use instances; they never own detached vectors,
duplicates or local decoration masters.

| Component | Sole master source | Consumer contract |
| --- | --- | --- |
| Connective arcs — blue section | [component 40000864:2416](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000864-2416&m=dev) on [✨ Decorative Elements 40000579:2358](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000579-2358&m=dev) | Use an instance at most once per Primary Blue section, behind content and clear of text. The Quote-to-Cash source and all five Design System states resolve to this master. |

## Interaction families

### Pagination — `40000829:2707`

| Variant | Figma source | Use |
| --- | --- | --- |
| `Breakpoint=Desktop, Mode=Counter` | [40000828:29367](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000828-29367&m=dev) | Desktop Case Studies and Team. |
| `Breakpoint=Mobile, Mode=Counter` | [40000828:29376](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000828-29376&m=dev) | Mobile Case Studies. |
| `Breakpoint=Mobile, Mode=Dots` | [40000828:29391](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000828-29391&m=dev) | Mobile Team and dot-paginated carousels. |

The `Counter` property is editable. Desktop Case Studies uses the Counter variant for
three cards per page. Mobile Case Studies uses the Mobile Counter for one card per view.
Desktop and Mobile Team use the appropriate reusable pagination treatment. Controls stay
keyboard-operable, retain accessible labels, and use the coded state management in
`revops-refresh-2025.js`.

### Playbooks — `40000832:29581`

Variants: [Sales `40000832:2769`](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000832-2769&m=dev),
[Marketing `40000832:2829`](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000832-2829&m=dev),
[Customer Success `40000832:2889`](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000832-2889&m=dev) and
[Data `40000832:2949`](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000832-2949&m=dev).
Each category has six playbooks.
All 24 detail panels remain in the DOM. Tabs and list items toggle classes; detail panels
transition with transform/opacity. No hover-only content, accordions or links out.

### Quote-to-Cash outcome tabs — `40000832:30153`

Default page source: [Pricing `40000820:2358`](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000820-2358&m=dev).
Canonical Design System default instance: [Pricing `40000835:30235`](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000835-30235&m=dev).

Variants: [Pricing `40000832:29698`](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000832-29698&m=dev),
[Approvals `40000832:29810`](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000832-29810&m=dev),
[Contracts `40000832:29924`](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000832-29924&m=dev),
[Billing `40000832:30040`](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000832-30040&m=dev) and
[Visibility `40000832:30152`](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40000832-30152&m=dev).
Every state owns its
before statement, source artefacts, broken handoff, disconnected object, governed rule
and named revenue objects. Grouped design rules remain at `40000823:2422`.
Every state uses the connective-arcs instance from `40000864:2416`; update that master
only on `✨ Decorative Elements`, never inside this component family.

There is no approved mobile layout. Do not auto-stack, compress or invent one. Add mobile
to the family only after a reviewed source exists.

## Colour and logo roles

- Primary Blue `#000FC4`: normal hero, section, active and governed states.
- Dark Navy `#161654`: approved mobile quote cards only.
- CTA Orange `#F26620`: conversion actions only.
- Critical failure: `#FDEBEC` surface with `#9E1C21` text/line/icon treatment.
- Dark, navy, blue or other brand-colour surfaces require approved white/reversed SVG
  logos. Light surfaces use approved dark or full-colour variants. Never mix treatments
  in one row.

## Required coding verification

Before implementation:

1. Find the canonical component and inspect both Desktop and Mobile chapters.
2. Run `get_design_context` on the component or approved instance.
3. Open the mapped HubSpot section and search its HTML classes, data hooks, CSS and JS.
4. Reuse the existing component and behavior; extend it only for a documented new state.
5. Reuse Pagination, Playbooks, forms, global navigation and footer exactly where mapped.
6. Check colour roles, white-logo usage, keyboard behavior, touch targets and responsive
   states.
7. Record any intentional design/code divergence before shipping.

If the design and live implementation disagree, use the approved component for visual
intent and the live code for existing behavior, then surface the conflict. Do not silently
create a third implementation.
