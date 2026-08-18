# Canonical page sections and implementation reuse

This reference is the pre-design and pre-coding gate for MAN Digital website sections.
Use the reusable components on the `🎨 Design System` page before copying a page frame or
creating a new HubSpot module.

## Canonical chapters

| Chapter | Figma node | Purpose |
| --- | --- | --- |
| 09 Canonical Page Sections — Desktop | `40000828:2707` | Approved 1512px components in page order. |
| 10 Canonical Page Sections — Mobile | `40000828:2708` | Approved 360px components in the same order. |
| 11 Interaction Rules & HubSpot Reuse Map | `40000828:2709` | Variant families, content/state contracts, colour roles and code mapping. |
| HubSpot Reuse Gate | `40000838:2929` | The visual pre-coding checklist and source index. |

Approved source page frames remain `40000296:2359` (Desktop) and `40000329:2358`
(Mobile). The component chapters are the reuse source; the page frames are composition
references.

## Numbered component map

| # | Section | Desktop component | Mobile component | HubSpot implementation |
| --- | --- | --- | --- | --- |
| 01 | Hero | `40000833:8980` | `40000836:2972` | Global theme navigation plus approved page hero. |
| 02 | Revenue Workflows | `40000833:9074` | `40000836:3045` | `sections/02-workflows.html`, `.rv-workflows`. |
| 03 | Case Studies | `40000833:9134` | `40000836:3082` | `sections/03-cases.html`, `.rv-cases`, `revops-refresh-2025.js`. |
| 03b | Highlighted Case Study | `40000892:2954` | `40000894:2961` | Intercom-inspired single landing-page proof feature; no outbound case-study link. |
| 04 | Fix Banner | `40000833:9151` | `40000836:3098` | `sections/04-fixbanner.html`, `.rv-fixbanner`. |
| 05 | Onboarding | `40000833:9279` | `40000836:3188` | `sections/05-onboarding.html`, `.rv-onboarding`. |
| 06 | Roadmap | `40000833:9341` | `40000836:3236` | `sections/06-roadmap.html`, `.rv-roadmap`. |
| 07 | Playbooks | set `40000832:29581` | `40000836:3319` | `sections/07-playbooks.html`, `.rv-playbooks`, `revops-refresh-2025.js`. |
| 08 | Principles | `40000835:3025` | `40000837:2938` | `sections/08-principles.html`, `.rv-principles`. |
| 09 | Leadership | `40000835:3055` | `40000837:2963` | `sections/08z-leadership.html`, `.rv-leadership`. |
| 10 | Team | `40000835:3130` | `40000837:2992` | `sections/09-team.html`, `.rv-team`, `revops-refresh-2025.js`. |
| 11 | Credentials | `40000835:3315` | `40000837:3177` | `sections/10-credentials.html`, `.rv-credentials`. |
| 12 | Strategy-call Form | `40000835:30048` | `40000837:3277` | `sections/11-form.html` and the existing HubSpot form embed. |
| 13 | FAQ | `40000835:30110` | `40000837:3318` | `sections/12-faq.html` and accessible disclosure behavior. |
| 14 | Footer | `40000835:30229` | `40000837:3434` | Active global theme footer. |
| 15 | Quote-to-Cash Outcome Tabs | set `40000832:30153` | Pending approved source | Code status `[future]`; verify before implementation. |

### Highlighted Case Study — single-story proof contract

- Responsive Design System wrapper: `40000894:2949`.
- Desktop master: `40000892:2954`; mobile master: `40000894:2961`.
- Review examples: desktop `40000912:2962`; mobile `40000912:2995`.
- Approved composition is Intercom-inspired. Desktop is `1512×981`: wide white story and
  proof area, then a Blue 100 testimonial band with the quote left and a prominent centered
  `160×160` portrait identity right.
- Mobile is `360×1293`: story first, two stacked full-width result rows, then a Blue 100
  portrait-first testimonial band with a centered `144×144` client image and identity.
- Never restore the superseded narrow dark quote panel or squeeze the two mobile results
  into side-by-side cards.
- Use only when a landing page highlights one case study. For multiple stories, use the
  registered `03 Case Studies` carousel/card family instead.
- Include an approved company logo, approved 1:1 client image, separate centered client
  name/company/role lines, two verified results, and one attributable approved quote.
- Prefer numeric metrics only when verified. Otherwise use concise qualitative outcomes;
  never invent a number, result, project claim, testimonial, or attribution.
- The brief owns every headline, summary, metric/outcome and quote. Reference-frame copy is
  pattern context only and must never be copied into a new landing page.
- Do not add a "Read case study", "Learn more", or other outbound case-study link. The
  proof story is intentionally self-contained on the landing page.
- The current review examples use Truvio logo source `40000598:29561` and Kris Nagrabski's
  verified identity fields to demonstrate layout only; their bracketed proof remains
  placeholder copy and is not approved campaign content.

The canonical HubSpot source checkout is maintained by the `man-digital-cms-pages` skill
under `references/source/pages/revops-service/`. Treat the mapped HTML, CSS and JavaScript
as existing implementation, not inspiration to rebuild.

## Interaction families

### Pagination — `40000829:2707`

Variants:

- `Breakpoint=Desktop, Mode=Counter`
- `Breakpoint=Mobile, Mode=Counter`
- `Breakpoint=Mobile, Mode=Dots`

The `Counter` property is editable. Desktop Case Studies uses the Counter variant for
three cards per page. Mobile Case Studies uses the Mobile Counter for one card per view.
Desktop and Mobile Team use the appropriate reusable pagination treatment. Controls stay
keyboard-operable, retain accessible labels, and use the coded state management in
`revops-refresh-2025.js`.

### Playbooks — `40000832:29581`

Variants: Sales, Marketing, Customer Success and Data. Each category has six playbooks.
All 24 detail panels remain in the DOM. Tabs and list items toggle classes; detail panels
transition with transform/opacity. No hover-only content, accordions or links out.

### Quote-to-Cash outcome tabs — `40000832:30153`

Variants: Pricing, Approvals, Contracts, Billing and Visibility. Every state owns its
before statement, source artefacts, broken handoff, disconnected object, governed rule
and named revenue objects. Grouped design rules remain at `40000823:2422`.

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
