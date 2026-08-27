# Fix playbook

Concrete fixes per failing audit, ordered by how often they matter.
Run `scripts/psi audit <url> -e 5` first — it prints the offending elements and selectors.

---

## Accessibility → 90+

**Verified: 88 → 95 mobile, 84 → 92 desktop** by fixing only `link-name` and
`button-name`. Almost always the same four audits.

**`link-name` — Links do not have a discernible name**
An `<a>` whose only child is an image or icon with no text.

For **logos**, the accessible name is the company name. If the CMS exposes it, use it
rather than hardcoding — `aria-label="{{ site_settings.company_name|default('Home', true) }}"`
resolved correctly on a live HubSpot site.

For **social icons**, do not add a "label" field every editor then has to fill in. Derive
the name from the destination:

```
{% set social_href = (item.social_media_link.url.href|default('', true))|lower %}
{% if 'linkedin' in social_href %}{% set social_name = 'LinkedIn' %}
{% elif 'facebook' in social_href %}{% set social_name = 'Facebook' %}
{% elif 'youtube'  in social_href %}{% set social_name = 'YouTube' %}
{% else %}{% set social_name = 'Social media' %}{% endif %}
```

Self-maintaining, and correct the moment someone adds a new network.

**`button-name` — Buttons do not have an accessible name**
Icon-only buttons (language switchers, dropdown toggles, hamburgers). Add `aria-label`. Do not add visually-hidden text if `aria-label` will do.

**`heading-order` — Headings not sequentially descending**
Card and accordion components picking heading levels for _size_ rather than structure. Fix by choosing the correct level and styling with a class. Do not "fix" by demoting a real heading.

This audit is the single most regression-prone fix in this playbook. Three things bite:

**1. Fix the whole chain, not the flagged element.** Only the skip gets reported. On one
page the report named three elements; correcting just those created _new_ skips, because
the outline was `h1 → h3 → h4 → h2 → h4`. Print the full outline first and mark every
transition, then choose levels for the sequence as a whole:

```js
const seq = [...document.querySelectorAll("h1,h2,h3,h4,h5,h6")].map(
  (h) => +h.tagName[1],
);
seq.forEach(
  (l, i) =>
    i && l > seq[i - 1] + 1 && console.log(`SKIP h${seq[i - 1]}->h${l}`),
);
```

**2. Changing the tag orphans every CSS rule keyed to the old one.** This is where the
real damage happens. A rule like

```css
.card:nth-child(2) .quote h5 {
  color: #fff;
} /* white text on a dark card */
```

silently stops applying when the quote becomes an `h3`, and the text falls back to the
body colour — in one case dark grey on a blue card, about **1.6:1**. The accessibility
score stayed 100 because the element was in an inactive slide (see measurement-traps #11).

Before shipping a level change, sweep every stylesheet for rules that mention the old tag
inside the affected container, and **extend the selector rather than writing a new rule**:

```css
.card .quote h5,
.card .quote h3 { ... }      /* keep both while content is mid-migration */
```

**3. Pin _all_ inherited typography, not the obvious four.** Copying `font-family`,
`font-size`, `font-weight` and `line-height` is not enough — `letter-spacing` differs
between heading levels in most themes and produced visibly cramped text twice in one
session. Measure the element _before_ the change and carry every property across:

```js
const s = getComputedStyle(el);
[
  "fontFamily",
  "fontSize",
  "fontWeight",
  "lineHeight",
  "letterSpacing",
  "color",
  "margin",
  "textTransform",
].forEach((p) => console.log(p, s[p]));
```

**Where the heading actually lives matters.** On a hosted CMS the tag is usually _not_ in
the module template — it is editor-entered rich text. Two different fixes:

- Content-authored, one page → PATCH the page's stored content. Preserves inline editing.
- Rendered through a module field, many pages → filter at the template:
  `{{ item.title|replace('<h4','<h3')|replace('</h4>','</h3>') }}`

Prefer demoting non-headings out of the outline entirely — stat values, tab labels and
testimonial quotes are not headings — but only after checking rule 2, because a `<p>`
orphans the same rules a level change does.

**`color-contrast`**
Check whether the element belongs to you. Cookie-consent banners are frequently vendor-rendered (HubSpot, iubenda, Cookiebot) and you can only change them in the vendor's UI. Report those separately rather than counting them as your defect.

---

## SEO → 90+

**`crawlable-anchors` — Links are not crawlable** _(the big one)_
**Verified: 23 → 0, taking SEO 85 → 92.**

`<a href="javascript:void(0);">` used as a click target. Crawlers cannot follow it, and it
is usually broken for humans too.

**Check whether a link field already exists before assuming the element is decorative.**
On the site this came from, the repeater already had a `box_link` field that the template
ignored in favour of a hardcoded dead href — so eleven main-navigation entries
("Implementation", "Migration", "Revenue Operations"…) did nothing when clicked. Wiring the
existing field fixed an SEO audit _and_ a live navigation bug nobody had reported.

Make the template fail safe rather than trusting the data:

```
{% if item.box_link.url.href %}
  <a href="{{ item.box_link.url.href }}">{{ item.title }}</a>
{% else %}
  {{ item.title }}          {# plain heading, never a dead anchor #}
{% endif %}
```

Same shape wherever a human may have typed a void href into a URL field — a copyright line
had `javascript:void(0)` entered as its link:
`{% if href and 'javascript:' not in href %}` … `{% else %}<span>…</span>{% endif %}`

- If it navigates → give it a real `href`.
- If it only toggles UI → it is a `<button type="button">`, not an anchor.

**`link-text` — Links do not have descriptive text**
"Learn more", "Read more", "Click here". Replace with the destination's actual subject. This also fixes the same links in `link-name`.

**Other common ones:** missing `meta description`, non-self-referencing or absent `canonical`, `robots` blocking, missing structured data. All deterministic.

---

## Agentic browsing → 90+

**Verified: 67 → 100** with no work targeted at it — purely as a side effect of fixing
`link-name`, `button-name` and `crawlable-anchors`.

**It is noisy.** The category currently hangs off a single pass/fail audit, so it flips
between 67 and 100 between runs and even between form factors on the same URL. Take a
median like any other score, and do not chase a single 67.

It is driven by **`Accessibility tree is not well-formed`**, which shares root causes with
those three. Treat it as a downstream symptom, never as a separate workstream. If it is
failing and accessibility is clean, look for elements that are interactive to a mouse but
invisible to the tree (div-with-onclick, anchors with no name, custom widgets missing
roles).

---

## Best practices → 90+ (minus platform)

**`errors-in-console`** — real JS errors. Fix them; they often also break behaviour.
A single failed request is enough to cap the category. Look for third-party tags that are
**already broken**: one visitor-identification script was served as `.js.gz` from S3 and
blocked outright by Chrome (`ERR_BLOCKED_BY_ORB`) — costing the score while delivering
nothing. Check `requestfailed` and any response >= 400, not just thrown exceptions.
**`third-party-cookies`** — set by analytics/consent vendors. On a hosted CMS you usually cannot remove these without disabling the product. Report as platform-bound.
**Deprecations / DevTools Issues** — read the actual item; often a vendor bundle.

---

## Semantic containers → machine-readable pages

Content cleaners identify boilerplate by semantic tag first and fall back to heuristics
(link density, class names, position) when the tags are absent. A page with 1,300 `<div>`s
and zero `<nav>`/`<footer>`/`<article>` gives them nothing to work with, and the menu gets
read as body content.

**Grep for element-qualified selectors before you swap any tag.** This is what makes the
change free:

```bash
grep -rnE '(^|[,{}]|\s)(main|article|nav|footer)\s*[.,{#:>\[]' --include='*.css' .
```

On one theme the only hit was `footer.footer { background-color:#0A0A0A }` — so
`div`→`nav`, `div`→`article` and the `<main>` dedupe were all pure tag changes with zero
visual risk. Keep the class list identical and only the tag name moves.

Two template-estate patterns worth checking for explicitly, both of which hide in plain
sight because each individual template looks correct:

- **Duplicate `<main>`.** The base layout opens `<main id="main-content">`, and every page
  template _also_ opens its own inside the body block. 53 templates did this — two `<main>`
  elements and a duplicated `id` on every page. Fix by demoting the inner one to a `<div>`
  with the same class; the layout keeps the single `<main>` and the skip-link target.
- **Missing `<footer>`.** The tag lived only in the global partial, so every template that
  overrode the footer block and called the footer module directly rendered no `<footer>` at
  all — 29 of them. Fix once by moving the wrapper into the layout _around_ the block, and
  stripping it from the partials so nothing nests.

Verify across page types, not one URL. A sweep of 22 URLs (services, case studies,
localised paths, landing pages, blog listing, blog post, 404) asserting `nav=1, main=1,
footer=1` caught what per-template review did not.

### Hidden content and the two discard signals

Cleaners drop a block when it is `display:none` **and** carries class names that read as
interface (`modal`, `popup`, `overlay`). Fixing one and not the other leaves the block
matching the remaining criterion, so do both:

- Move hiding out of inline styles into a CSS class. jQuery `.hide()`/`.slideToggle()` write
  `style="display:none"` onto every element they touch; a class leaves the markup clean.
  Check with `document.querySelectorAll('.thing[style]').length`.
- Rename the classes. Then confirm nothing was orphaned — on one module `.modal-close` had
  its only rule in a **different** module's stylesheet, so renaming it locally would have
  left the button unstyled. Copy the rule across before renaming, and grep the whole theme
  for each old name.

## Performance

Do these **in order**. Stop when the score stops moving and re-diagnose.

### 1. Remove the paint gate

If `body` is hidden until a JS class is added, that is the ceiling on FCP. Moving it from `window.load` to DOM-ready took real FCP from "never paints until load (1.4–8.4 s)" to **500–900 ms**.

Better still, remove the gate entirely and scope the hiding to what actually needs it:

```css
/* instead of hiding the whole page until the carousel initialises */
.slick-slider:not(.slick-initialized) > *:not(:first-child) {
  display: none;
}
```

Expect TBT to _rise_ when you do this. It is not a regression — you stopped suppressing the measurement window.

### 2. Defer heavy third-party pulled in by below-fold content

Forms are the usual offender: an embed script plus a captcha bundle, eagerly loaded for a form many screens down. Measured cost: **1,032–1,621 ms** of main-thread time, 3–5x the next script.

Requirements for doing this safely:

- Build immediately if the element is within ~1.5 viewports of the top (above-fold forms must not be deferred — it cost CLS 0.306).
- Reserve the height the element will occupy, measured, not guessed.
- Keep a fail-safe branch that renders the vendor's original embed when the config cannot be reproduced client-side.

### 3. Fix genuinely oversized images

Measure with a browser `Accept` header first (see measurement-traps.md). Then look for:

- SVGs that are really a wrapper around a full-resolution raster
- Images with no `width`/`height` (CLS) or no `loading="lazy"` below the fold
- Raw CDN paths that bypass the host's resize/WebP pipeline

### 4. Then, and only then, CSS

Splitting a large stylesheet into an above-the-fold critical file plus an async remainder is **architecturally right but frequently score-neutral** — because once you fix the paint gate, FCP is often bound by JS, not CSS. Measure before and after; do not assume.

If you do it: preserve cascade order. Insert the async link immediately after the critical one, not appended to `<head>`, or later stylesheets that were meant to override it will lose.
