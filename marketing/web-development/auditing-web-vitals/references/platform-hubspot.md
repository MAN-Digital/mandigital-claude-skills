# HubSpot CMS specifics

Written against portal `1969772` / `www.man.digital`, but the mechanics apply to any
HubSpot CMS Hub site. Most of it generalises to other hosted CMSs — the shape of the
problem is the same even when the API is not.

## Working through the app session

The Design Manager and CMS APIs are reachable from an authenticated `app.hubspot.com`
page by echoing the `hubspotapi-csrf` cookie in an `X-HubSpot-CSRF-hubspotapi` header.

| Endpoint                                         | Use                                                                                              |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `/api/designmanager/v1/templates/<id>?portalId=` | GET/PUT theme files (CSS, JS, layouts). `PUT {source}`                                           |
| `/api/designmanager/v1/templates?portalId=`      | POST to create a file (`path`, `folder`, `source`, `categoryId:0`, `templateType:24`)            |
| `/api/designmanager/v1/modules/<id>?portalId=`   | GET/PUT module templates. Template lives in `source`                                             |
| `/api/cms/v3/pages/site-pages?slug__icontains=`  | Find pages                                                                                       |
| `/api/cms/v3/pages/site-pages/<id>`              | `PATCH {layoutSections}` — rich-text lives at `layoutSections.dnd_area.rows.<r>.<c>.params.html` |
| `/api/forms/v2/forms/<guid>`                     | Form config incl. `captchaEnabled` (per-form boolean)                                            |
| `/api/files/v3/files?portalId=`                  | POST multipart to upload; `options:{overwrite:true}` replaces in place                           |

`cms/v3/url-redirects` returns **401** through this path — redirects must go through the UI.

## The CLI, and what the access key can actually do

`hs cms list|fetch|upload <src> <dest> --account=<portalId>` is the fastest path for theme
work — no browser session needed. Note the subcommand is `hs cms list`, not `hs list`.
Always pass `--account`; the configured default is often a sandbox.

**A personal access key is read/write for theme source code but read-only for page
content.** Do not describe it as simply "read-only" — every theme change ships through it.
A typical key carries `cms.source_code.read` **and `cms.source_code.write`** (so
`hs cms upload` works), plus `cms.pages.site_pages.read`, but **not** `content`. So
`GET /cms/v3/pages/site-pages/<id>` succeeds while `PATCH` returns
`403 MISSING_SCOPES` requiring `content`. Consequence: you can ship template changes but
cannot PATCH a page to force a re-render — you wait for the platform. List the real scopes
with:

```bash
curl -s -X POST https://api.hubapi.com/localdevauth/v1/auth/refresh \
  -H 'Content-Type: application/json' \
  -d '{"encodedOAuthRefreshToken":"<PAK>","portalId":<id>}'
```

**Snapshot before you upload.** `hs cms fetch` the folder to a `ROLLBACK/` directory first,
then `diff -rq` your working copy against it. That gives you the exact changed-file list to
upload and doubles as proof you did not modify anything you did not intend to.

## Formatters will corrupt HubL

If your editor or a commit hook runs Prettier over the theme, it treats `.html` as HTML and
will happily line-wrap a HubL tag **inside a quoted string**:

```
{% module "x" path="/My Theme
2023/templates/partials/footer-v2", label="footer-v2" %}
```

That newline is inside the path literal, so the module silently fails to resolve. It also
reflows `{#- ... -#}` comments and mangles them when they contain literal `<tag>` markup.
Write HubL files with a shell heredoc rather than an editor tool, and re-read any HubL file
a formatter reports touching.

## Rendering and caching

- Pages are **pre-rendered**. Editing a page re-renders within ~30 s. A **theme module**
  upload re-renders the pages using it in ~60 s, a template upload in ~2 min, and blog
  posts trail the page templates by a further minute or two. Check the `x-hs-prerendered`
  response header before concluding a change failed — and note the 10 h `s-maxage` on the
  CDN does *not* delay page edits the way it delays `sitemap.xml`.
- `sitemap.xml` carries `s-maxage=36000` (10 h) and does **not** refresh on the same
  schedule as pages.
- **Replacing a File Manager file in place does not purge the CDN edge.** Rename it
  (new path = no cache entry) and repoint whatever references it.

## Assets and images

- `get_asset_url()` returns the **fs1 CDN host inside a JS string** but the **primary
  domain inside an HTML attribute**. Read URLs from an attribute when you need same-origin.
- `require_css()` emits one collected block, not inline at the call site. Raw `<link>`
  tags written in `<head>` render _before_ it. External URLs passed to `require_css()`
  are bucketed ahead of local assets.
- `/hs-fs/` paths get automatic resize + WebP conversion. `/hubfs/` raw paths do **not**.
- Store the plain `https://<portal>.fs1.hubspotusercontent-na1.net/hubfs/<portal>/...`
  URL with `width`/`height`/`loading` attributes and let HubSpot generate `srcset`.
  Hardcoding an `hs-fs` URL bypasses that pipeline.
- Watch for `width="0"`, `width="Infinity"`, `height="NaN"` in stored rich-text `<img>`
  tags — an editor bug, widespread, and it defeats aspect-ratio reservation.
- File Manager serves `.txt` as `text/plain` with **no charset**, so consumers fall back
  to windows-1252 and any UTF-8 byte becomes mojibake. Keep hosted `.txt` pure ASCII.

## Forms

- `captchaEnabled` is **per form**. Check it before assuming reCAPTCHA is site-wide policy.
- reCAPTCHA does **not** appear in the page HTML — `forms/v2.js` fetches it _during form
  creation_. Defer `hbspt.forms.create()` and it never loads.
- The `{% form %}` HubL tag server-renders a target div and emits an inline
  `hbspt.forms.create(options)`. `forms/v2.js` is a **synchronous** tag emitted _after_
  the module's markup, so you cannot inject between the two from inside a module.
- Redirects may be stored as `redirect_id` (a page ID) with `redirect_url` null. There is
  no reliable HubL function to resolve a site-page ID to a URL — resolve it via the API
  and write `redirect_url` into the instance, or fail safe to the eager embed.

## Render-blocking is mostly architectural

A typical page showed **19 render-blocking requests**. Ten of them were **one stylesheet
per module**, emitted automatically by HubSpot for every module on the page. You cannot
defer those without abandoning module-scoped CSS, so `render-blocking-insight` has a floor
well above zero on any content-rich HubSpot page. Fix what you own — third-party CDN CSS,
font URLs, your own theme file — then say plainly that the remainder is platform shape.

`theme-overrides.css` can be moved off the critical path (preload + `media="print"` swap,
inserted immediately after the critical file to preserve cascade order), and it does drop
out of the blocking list. Check the list rather than assuming: on this site the async
loader coexisted with a plain `<link rel="stylesheet">` further down the layout, and only
reading the audit's actual URL list showed which one was winning.

## Module JS is wrapped in a comma expression

HubSpot wraps a module's JS as `var module_<id> = ( <your code> );`. Appending a top-level
IIFE without a leading `;` lets the minifier glue it onto the previous expression as an
**argument**, so it silently never runs — no error, and the code is visibly present in the
deployed `.min.js`. Always append as `;(function(){...})();` and verify against the
minified artifact (correct output looks like `}),void function(){...}`).

## Headings usually live in content, not the module

`heading-order` fixes almost never belong in the module template — the `<h4>` is inside an
editor-entered rich-text field. Check `(source.match(/<h4/g)||[]).length` on the module
first; if it is zero, the tag is in page content.

- **One page** → `PATCH /api/cms/v3/pages/site-pages/<id>` with a walked-and-rewritten
  `layoutSections`. Assert tag counts before and after; the change is live in ~30 s with no
  publish step. This preserves inline editing.
- **Many pages via a module field** → filter at the template:
  `{{ item.title|replace('<h4','<h3')|replace('</h4>','</h3>') }}`

`{% inline_rich_text %}` cannot take a filter cleanly — converting it to a plain `{{ }}`
expression to apply one costs the editor inline editing, so prefer the content fix there.

## Things that are not yours to fix

`HubspotToolsMenu`, `cos-i18n`, `content-cwv-embed`, `hs-analytics`, `hs-banner`,
`hsadspixel` and the script loader are injected by the platform. `hs-analytics` in
particular is both slow (~900 ms) and erratic — it was the single largest source of
score variance observed. Budget performance targets with these in the floor.

jQuery 1.7.1 ships with older themes and costs ~200–550 ms. Replacing it is a project,
not a fix.

## Additions from the man.digital theme-perf project (Aug 2026)

- **Re-render mechanics:** pages re-render ~2–3 min after `hs cms upload`; identical uploads
  are DEDUPED (no re-render), and changes to `{% include %}`'d css never re-render including
  pages — force with a real byte change (render-bump comment) in the template.
- **Relative url() in theme css breaks** both as generated min css (served from
  hub_generated/<id>/<ts>/) and when inlined. Use `/hubfs/raw_assets/public/<Theme%20Name>/...`.
- **Empty module.css ⇒ HubSpot emits no stylesheet link** — the mechanism for removing
  per-module render-blocking css. Move the styles to a separate theme css file FIRST; an
  {% include %} of the module's own (now empty) css silently unstyles it.
- **HubSpot's minifier re-sorts selector lists** — verify live css by grepping fragments.
- For the full page-building workflow and trap list, load `$man-digital-cms-pages`.
