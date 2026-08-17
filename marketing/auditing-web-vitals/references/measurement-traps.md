# Measurement traps

Every entry below is a mistake that actually happened during a real audit, with the
numbers it produced. They are here because each one _looked_ like a finding.

---

## 1. Single-run scores

PSI returned **39** and **52** for the same URL minutes apart, and **31 / 51 / 51** on
three spaced runs of another. Some pages are bimodal (`70 / 48 / 48`, FCP 2.9 s vs 8.3 s)
because PSI's own infrastructure varies.

**Rule:** median of 3+. If a difference is under ~13 points, it is not a difference.
`scripts/psi score` does this by default; `scripts/psi sweep` does not (it is one run per
URL for speed) — confirm anything surprising with `scripts/psi score -n 5`.

Parallel identical requests hit PSI's ~30 s cache and return the _same_ result — five
identical numbers are one sample, not five. `scripts/psi score` runs sequentially for this reason.

---

## 2. Local Lighthouse on a busy machine

|                                                           | TBT            |
| --------------------------------------------------------- | -------------- |
| Local Lighthouse, machine saturated with Chrome instances | 3,200–5,070 ms |
| PSI, same commit, same minute                             | 530–780 ms     |

A 6x error, and it pointed the wrong way on a keep/revert decision. Local Lighthouse is
fine for _relative_ A/B on an idle machine; it is not comparable to a PSI baseline.

**Rule:** compare like with like. If the baseline came from PSI, the after must too.

---

## 3. Blocking a resource to estimate its cost

`--blocked-url-patterns` on the main stylesheet suggested FCP would drop from 9.5 s to
2.1 s. The real async-loading change delivered **zero**.

Blocking CSS produces an _unstyled_ page, which lays out almost instantly. It models
deletion, not deferral. Same applies to blocking JS that other code depends on.

**Rule:** blocking experiments rank suspects. They do not size fixes.

---

## 4. Measuring images without a browser `Accept` header

Plain `curl` (`Accept: */*`): **12,892 KB**
`Accept: image/webp,image/avif`: **434 KB**

A 30x error, because the CDN converts on the fly. Every "enormous image" list built with
default curl is wrong.

```bash
curl -sSL -H 'Accept: image/avif,image/webp,image/*' \
     -A 'Mozilla/5.0 (Linux; Android 11) Mobile Safari/537.36' \
     -o /dev/null -w '%{size_download} %{content_type}\n' "$URL"
```

**Exception that matters:** SVG gets no such conversion. Once everything else is measured
honestly, SVGs often dominate. One was **11.4 MB** — a wrapper around a 4096×2732 PNG
displayed at 667×384, three viewports below the fold with no `loading="lazy"`.

---

## 5. Trusting a crawl that silently failed

`sed -E 's|</?loc>||g'` is fine; `sed 's|</\?loc>||g'` is **not** on BSD/macOS sed — `\?`
is not supported, the substitution silently does nothing, every URL keeps its XML tags,
every fetch fails, and the scan reports a clean result across 122 pages.

Likewise, fetching a sitemap through a summarising tool truncated 127 `<loc>` entries to
12 and then confidently reported URLs as absent.

**Rule:** sanity-check any scan that reports zero findings. Fetch one known-positive URL
through the same code path before believing a clean sweep.

---

## 6. Reading `cssRules` and concluding a stylesheet did not load

`SecurityError: Failed to read the 'cssRules' property` means the stylesheet is
**cross-origin**, not that it failed. The styles apply fine. It did, however, reveal a
real problem: the URL was being emitted for a different host, costing an extra DNS + TLS
handshake.

Related gotcha: a templating helper can return a CDN host inside a JS string but the
primary domain inside an HTML attribute. Read such URLs from an attribute.

---

## 7. Believing brace counting on JS or templated CSS

Brace/paren counting is meaningless where strings, regexes and template tags exist.
A template's `{% ... %}` tags and `{{ ... }}` expressions break naive CSS brace counts;
a regex literal breaks JS ones.

**Rule:** validate with a real parser. `new Function(src)` compiles JS without running it.
`postcss.parse()` validates CSS. For templated files, count the template's own constructs
separately and confirm they are unchanged.

Also: a CSS minifier refusing to run is a _signal_. One 400 KB stylesheet was served
unminified while every sibling was minified — because of a single missing semicolon
(`width: calc(100% + 32px)margin-left: -16px;`), which also silently dropped both
declarations in every browser. Fixing that one character let the platform minify the file
(81 KB → 58 KB gzipped) and restored the two lost rules.

---

## 8. Assuming a metric moved the right way

After removing a paint gate, TBT rose from ~250 ms to ~450 ms and the score fell. That
looked like a regression. It was not: while the page was hidden until fully loaded there
was no window in which blocking time could be measured. The jank had always been there.

**Rule:** when a metric worsens, ask whether you removed something that was suppressing
its measurement, before reverting.

---

## 9. Regex-replacing a template block and matching only some of them

A mega-menu rendered the same card markup twice, but the two blocks used **different loop
variables** (`item` and `item2`). A regex written against the first matched 1 of 2, and the
"fix" would have shipped half applied — with the counters still looking plausible.

**Rule:** capture the varying part rather than hardcoding it, and assert the match count
equals what you expect _before_ writing:

```js
const RE = /\{\{\s*(item2?)\.title\s*\}\}/g;
const found = [...src.matchAll(RE)].map((m) => m[1]); // ['item','item2']
if (found.length !== 2)
  throw new Error("expected 2 blocks, got " + found.length);
```

Related: exact-string matching fails on templates because your scrubbed/preview view
collapses whitespace that the source keeps as tabs and newlines. Match with `\s+`.

And when a check fails, confirm _why_ before loosening it. A guard expecting 4 new
occurrences saw 5 — because one already existed in the file. The guard was right to fire;
the expectation was wrong.

Same lesson, sharper version: **compare a CSS brace balance against the file's original
balance, not against zero.** Two modules in one theme had a pre-existing imbalance — one
a stray `}`, one an `@media` block that was never closed (silently swallowing every rule
after it). A guard hardcoded to `0` fires on both and tells you nothing; a guard that
asserts `balanceAfter === balanceBefore` catches your own damage _and_ surfaces theirs.

---

## 10. A minifier turning your appended IIFE into a function argument

Appending this to an existing module JS file looked completely safe:

```js
(function () {
  /* label the select */
})();
```

The file already ended in `})` with no trailing semicolon. The minifier joined them:

```js
...$(document).find(".privacyCheckboxOuter").show()})(function(){...})()
```

The IIFE became an **argument to the preceding call**. It never executed. No console
error, no failed request, no syntax error — the audit simply kept failing, twice, while
the deployed file visibly contained the code. Verified it was deployed by fetching the
minified URL and grepping for it, which made it _more_ confusing, not less.

**Rule:** always prefix appended top-level JS with `;`. Then check the _minified_ output,
not the source — the correct result reads `}),void function(){...}` or `};(function(){`.

Generalises: any time "the code is definitely deployed but definitely not running", read
the built artifact, not the source you wrote.

---

## 11. Lighthouse cannot see inside inactive carousel slides

Accessibility scored **100 on every page, both form factors** — and a human immediately
found unreadable text on one of those pages.

axe skips elements it considers hidden, which includes non-active slides in a carousel or
tab panel. Two real contrast failures were sitting there: role text at **2.67:1**, and a
quote at roughly **1.6:1** on a dark card. Both were plainly visible to a visitor the
moment the slide rotated in.

**Rule:** a 100 is evidence about what the tool sampled, not about the page. On any page
with carousels, tabs or accordions, walk the variants yourself and compute contrast on the
hidden ones. Report the score and the manual check as separate claims.

```js
// compute the effective background by walking ancestors — the failing element
// almost never sets its own
const eff = (el) => {
  let n = el;
  while (n && n !== document.documentElement) {
    const c = getComputedStyle(n).backgroundColor;
    if (c && !/rgba\(0, 0, 0, 0\)/.test(c)) return c;
    n = n.parentElement;
  }
  return "rgb(255,255,255)";
};
```

---

## 12. Fixing one colour token while a second one hides behind it

A CTA orange `#F26620` failed contrast and was corrected everywhere it paired with white
text — seven rules. The page still failed. There was a **second, near-identical token**,
`#F26419`, used by a different component. Visually indistinguishable, separately defined,
equally broken.

**Rule:** after fixing a colour, grep the stylesheet for _near-miss_ hex values, not just
the one you changed. Search by the failing computed `rgb()` value taken from the live
element rather than by the hex you assume is responsible.
