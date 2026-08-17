---
name: auditing-web-vitals
description: Use when auditing or trying to raise PageSpeed/Lighthouse scores, Core Web Vitals, accessibility, SEO or agentic-browsing scores on a live site, or when a page "feels slow", a client reports slowness, a score regressed after a change, or when making page content legible to LLM/AI content extractors (AEO) - semantic tags, heading structure, hidden or duplicated content
---

# Auditing Web Vitals

## Overview

Scores are a **throttled projection**, not what visitors experience, and they are **noisy**. Most wasted effort in this work comes from optimising something that was never on the critical path, or from believing a single measurement.

**Core principle: find the gate before you optimise bytes.** A page has one thing that blocks first paint. Until you know what it is, every byte you remove is a guess.

Use the bundled dependency-free CLI at `scripts/psi`. The examples below invoke that
path so the skill works immediately after being copied from this repository.

## The Iron Rules

1. **Never draw a conclusion from one run.** PSI varies up to ~13 points on the same URL. `scripts/psi score` medians 3 runs by default. If two numbers differ by less than ~13, you have measured nothing.
2. **Never trust local Lighthouse on a busy machine.** Measured on a loaded laptop: TBT 3,200–5,070 ms. PSI, same commit: 530–780 ms. A 6x error that inverted a decision.
3. **Never extrapolate from blocking a resource.** Blocking a stylesheet makes the page unstyled, which lays out trivially fast. That is not a model of loading it async. This mistake predicted a large win and delivered exactly zero.
4. **Simulated ≠ observed.** `scripts/psi diagnose` prints both. `observedFirstContentfulPaint` 2.4 s vs simulated 9.5 s means the score is a Slow-4G + 4x-CPU projection. Optimise the metric you are graded on, but never tell a client their site takes 9 s when it takes 2.4 s.

## Workflow

```
scripts/psi score <url> -s both -m # where am I, mobile AND desktop
scripts/psi diagnose <url>         # what gates first paint
scripts/psi audit <url>            # every failing a11y/SEO/best-practice/agentic item
# ...fix one thing...
scripts/psi score <url> -s both -n 5 # did it actually move
```

Always measure **both form factors**. Desktop and mobile diverge hugely — one real site scored 96 desktop / 73 mobile on the same URL. A "bad" site is often a bad _mobile_ site.

## What Is Actually Achievable

| Category         | 90–100 realistic?             | Why                                              |
| ---------------- | ----------------------------- | ------------------------------------------------ |
| Accessibility    | **Yes**                       | Deterministic markup fixes                       |
| Best practices   | **Yes**, minus platform items | Console errors, third-party cookies              |
| SEO              | **Yes**                       | Crawlable links, descriptive text, meta          |
| Agentic browsing | **Yes**                       | Driven by the same markup as a11y                |
| Performance      | **Yes, per page**             | But it is a _page_ property, not a site property |

**Find the platform floor empirically before promising or refusing anything.** The fastest
way: score your _lightest_ page — a documentation or policy page on the same theme, with
the same vendor scripts and almost no content.

On the site this was built against that page scored **97 mobile / 99 desktop**, while the
homepage scored 64 and a blog post scored 36. Same theme, same platform JS, same CMS. That
one measurement proved the platform was never the ceiling — page content was.

The inverse is just as useful: if your lightest page _also_ scores badly, the theme or
platform **is** the constraint and no amount of per-page work will fix it. Either way you
now have a number instead of an opinion.

Corollary: **desktop and mobile are different problems.** In that sweep desktop ranged
56–99 while mobile ranged 36–97 on identical URLs. "Fix the site" almost always means fix
mobile.

## Find the Gate First

Before touching bytes, answer: _what is preventing paint?_

- Is `body` hidden until JS runs? Look for `opacity:0` / `visibility:hidden` revealed by a JS-added class. If that class is added on `window.load`, the page is blank until **every** image, iframe and third-party script finishes. This single anti-pattern caused an 8.4 s white screen and made FCP unmeasurable (`null`). A gate at document-ready is still the LCP on every page (~7 s simulated). And the gate MASKS instability: fonts swap and late css re-style while nothing is painted, so CLS reads 0.000. Removing it makes CLS honest (0.3+ appeared) — the culprits were above-the-fold rules living only in the ASYNC stylesheet, including one-line spacing utilities (`.pt60`) whose late arrival dropped a hero strip 95 px. Mirror those rules (byte-identical, exact @media contexts) into the critical path; hunt culprits via the raw API `layout-shifts` audit on BAD runs only — clean runs show nothing.
- Is the LCP element a CSS `background-image`? It cannot be discovered until CSS parses. `scripts/psi diagnose` names the element.
- Is a heavy third-party script loaded eagerly for content below the fold? Forms are the usual culprit — they drag in captcha bundles.

**Optimising CSS or images while a JS gate holds the paint changes nothing.** Verified the hard way.

## Traps

| Trap                                     | Reality                                                                                                                  |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| "The image is 12 MB"                     | Measure with `Accept: image/webp`. Plain `curl` reported 12.9 MB for a file browsers get as 434 KB — a 30x error.        |
| "This SVG is fine, it's vector"          | SVGs get no CDN image conversion. One was an 11.4 MB wrapper around a 4096×2732 PNG shown at 667×384.                    |
| "Local Lighthouse says…"                 | Only if the machine is idle. Prefer PSI with a key.                                                                      |
| "Blocking it proved the win"             | It proved nothing. Ship it behind a flag and measure.                                                                    |
| "Minifying will fix Style & Layout"      | Style cost tracks **rule count** against the DOM, not bytes. 81→58 KB moved FCP by 0.2 s.                                |
| "Lazy-load everything below the fold"    | Not if it is within ~1.5 viewports, and not without reserving its height. Both mistakes cost real CLS (0.306).           |
| "TBT got worse, revert"                  | If you just stopped hiding the page, TBT got _honest_. Hiding content suppresses TBT by leaving no window to measure in. |
| "Score didn't move, so nothing happened" | Check the metric you targeted, not the score. And check run-to-run spread first.                                         |
| "Four API calls agree exactly — stable!" | The PSI API caches analyses; rapid repeats return ONE measurement. Byte-identical values are the tell. Space runs (`scripts/psi score -n 5`). |
| "Measured right after deploying" | CDN propagation windows produce phantom CLS and 30-point spreads. Wait 10+ min, then n=5 medians. Three false alarms in one day. |
| "Inlining the small css must help" | Lantern scores a small render-blocking LINK better than the same bytes inline (simulated LCP 4.1→7.4 s, reality unchanged). When the PSI score is the KPI, the simulator's preference IS the requirement — revert what it punishes, keep the link. |
| "Preload + crossorigin is only for CDN fonts" | Font fetches are always CORS-mode; a same-origin font preload without `crossorigin` mismatches and downloads twice. |
| "I pinned the font-size, it looks the same" | Only at the width you checked. Re-tagging `h3`→`h4` and hardcoding `36px` dropped the theme's `@media (max-width:991px)` downscale to 27px — phones rendered 36px headings in a 300px column. Carry the media queries across too. |
| "Put the content in the main flow" | If you _add_ it beneath the existing UI you now have it twice; on a 24-item section that doubled every description. Move the content or retire the original — do not clone it. |

## Before Changing a Shared Stylesheet or Layout

- **Record the stylesheet order.** If N module stylesheets load _after_ the main one, they override it. Moving the main one changes precedence site-wide. Verify order after deploying, not just before.
- **Check what a template block is used for.** Content placed inside an overridable block gets dropped by any child template that redefines it.
- **Never delete a rule you have not traced.** Four `@font-face` blocks looked dead (`src: url()`); the source was fine and the _asset path_ was broken. Deleting them would have hidden a real bug.

## Before Changing Anything That Captures Leads

Forms are revenue. Deferring or rewriting a form embed can break submission silently.

- Check how the redirect is stored. A page-ID redirect resolves server-side; a hand-rolled embed that only passes `redirect_url` will **submit successfully and never redirect**.
- Keep a **fail-safe branch**: if the config cannot be reproduced client-side, render the platform's original embed. Correctness beats speed.
- Test an actual render and submit path, not just the markup.

See references/fix-playbook.md for the concrete fixes behind each category, references/measurement-traps.md for the full list, and references/platform-hubspot.md for HubSpot CMS specifics.

## Fixing Accessibility Can Break Accessibility

Two regressions introduced _by the fixes themselves_, both caught only by re-auditing:

- Replacing a dead `<a>` with a `<span>` dropped the link colour, and the inherited body
  colour was near-black on a near-black footer — a **new contrast failure**. When you
  demote a link to text, carry its visual treatment across. Read the surrounding elements'
  computed colours rather than guessing.
- Adding `aria-label="Change language"` to a button that _also_ had visible text ("en")
  created a **new** failure: "elements with visible text labels do not have matching
  accessible names" (WCAG 2.5.3). An accessible name must **contain** the visible text.
  Use `aria-label="Change language: EN"`, or drop the label and mark the icon
  `aria-hidden="true"` so the visible text becomes the name.

- Promoting a heading for `heading-order` orphaned a `.card:nth-child(2) .quote h5
{ color:#fff }` rule on a **dark** card, dropping the text to roughly **1.6:1**. Changing
  a tag silently unhooks every CSS rule keyed to the old one. Sweep for them first and
  extend the selector; see references/fix-playbook.md.
- The same change inherited a different `letter-spacing` from the new heading level and
  produced visibly cramped text. Carry **every** computed property across, not just
  family/size/weight/line-height.

**Always re-audit after fixing, on more than the page you were looking at.** The button
looked fine on the homepage, where its text rendered empty.

## Extraction Is a Third Axis, and It Fights Accessibility

Scores are not the only consumer of your markup. The content cleaners in LLM ingestion
pipelines — trafilatura, readability and their derivatives — read the same DOM, and the
shape that satisfies a screen reader is not automatically the shape that survives
extraction. Verified on a live disclosure widget: 24 cards, each opening a panel of
service descriptions.

| Shape | Extraction | Assistive tech |
| ----- | ---------- | -------------- |
| `<a href="#panel">` wrapping heading + panel | **Broken** — headings and lists collapse into one run of anchor text | Panel content is one enormous link |
| `<div role="button">` wrapping heading + panel | Fine | **Broken** — ARIA presentational children strips descendants' roles, so the `h3`/`h4`/`ul` stop being a heading and a list |
| `<h3><button>Name</button></h3>`, the W3C disclosure pattern | **Broken** — a heading whose only child is a button is not emitted as a heading | Fine |
| Plain `<h3 id>` + a separate empty `<button aria-labelledby>` overlaid, panel a sibling | Fine | Fine |

Only the last satisfies both. The overlay button keeps the whole card clickable —
`position:absolute; inset:0` inside a positioned parent — without nesting anything inside
it. Across the three attempts, key names resolving as their own heading went
2/6 → 6/6 → **2/6 again** → 6/6. That middle regression was invisible on screen _and_ in
the accessibility audit; only re-running the extractor caught it.

**A `keydown` shim on a container swallows keys from its descendants.** While the panel
lived inside the `div role="button"`, the Enter/Space handler bound to that div also fired
for events bubbling out of the panel: Enter on a link inside did nothing, and Space stopped
scrolling. A real `<button>` for the trigger removes the shim, and the bug, entirely.

### Measure extraction the way you measure scores

Run the real library, before and after, with JavaScript not executed:

```bash
trafilatura --markdown -u "$URL"    # or the Python API with output_format='markdown'
```

Record three numbers beside the score: extracted characters, heading count, and how many of
your key entity names resolve as `### Name` rather than plain text. Heading count rising
while character count stays flat is the outcome you want — structure fixed, nothing
duplicated. Character count rising in step with heading count usually means you cloned the
content instead of restructuring it.

## A 100 Is Not A Clean Page

Accessibility hit **100 on four pages, both form factors** — and a human found unreadable
text on one of them within minutes. axe skips elements it considers hidden, so anything in
an **inactive carousel slide, tab panel or collapsed accordion is never sampled**. Two real
contrast failures were living there (2.67:1 and ~1.6:1).

On any page with rotating or toggled content, walk the variants manually and compute
contrast yourself. Report the score and the manual check as two separate claims — "scores
100" and "no contrast defects" are not the same statement, and conflating them is how you
tell a client something false with a screenshot to back it up.

## Red Flags — Stop

- About to report a score from one run
- About to compare local Lighthouse against a PSI baseline
- About to optimise bytes without knowing what gates paint
- About to delete CSS/markup you have not traced to its source
- About to defer a form, carousel or above-fold element without reserving its space
- About to claim a fix worked without re-measuring the specific metric it targeted
- About to add `aria-label` to something that already has visible text
- About to replace a link with plain text without carrying its styling across
- About to change a heading level without grepping for CSS rules keyed to the old tag
- About to report "accessibility is 100" as "there are no contrast defects"
- About to nest a heading, a list or a panel inside a `<button>` or `role="button"`
- About to bind a keyboard shim to a container that also holds the content it toggles
- About to claim an extraction fix worked without re-running the extractor
- About to satisfy "put it in the main flow" by copying the block rather than moving it
- About to append JS to an existing file without a leading `;`
- About to assert a CSS brace balance equals `0` rather than its original value
- About to fix a colour token without checking for a near-identical second one
