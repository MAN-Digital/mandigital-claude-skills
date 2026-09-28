# Theme Contract (mandated output shape)

Every full-site run produces this layout. No partial outputs.

## 1. Tree

```text
<theme>/
├── theme.json            # {"label": "<name>", "preview_path": "./templates/home.html"}
├── fields.json           # global colors + fonts (theme settings)
├── deploy.json           # SKILL-CUSTOM page manifest (HubSpot does not read it; deploy.sh does)
├── assets.json           # SKILL-CUSTOM asset manifest (local path → File Manager dest)
├── QA-EVIDENCE.json      # written by validate-theme.sh, never by hand
├── css/                  # fonts.css, variables.css, common.css, custom.css
├── js/                   # vanilla JS only, one concern per file
├── images/<section>/     # per-section subfolders mirroring assets.json
├── modules/<name>.module/# fields.json, meta.json, module.html, module.css, [module.js]
└── templates/*.html      # DnD page templates + blog_listing + blog_post
```

## 2. Build order

Tokens (`fields.json` + `css/` + `theme.json`) → modules → blog modules → templates + `deploy.json` → assets + `assets.json`. No hardcoded brand values in modules.

## 3. Module rules

- One folder per section. Every text, image, link, list a marketer might change is a field — zero code-only content.
- Mandatory modules: global header (nav, language, CTA, mobile drawer) and footer.
- `blog_listing` + `blog_post` read post data from `content`/`group`; only chrome (breadcrumb, labels) is editable. Listing cards MUST use the `post_list_summary_featured_image or featured_image` chain — summary-only renders imageless cards when the summary image is unset.
- Listing data source: `contents` (auto-provided post sequence on listing templates — simplest, no editor step) vs `blog_recent_posts(blog_selection)` (editor picks the blog via a `blog`-type field; MUST ship manual fallback cards for the unconnected state). Prefer `contents`; use `blog_recent_posts` only when the listing must show a non-default blog.
- Post tags: render `content.tag_list` — `content.topic_list` is a legacy alias for older implementations ([HubL variables](https://developers.hubspot.com/docs/cms/reference/hubl/variables), "Blog variables" note).
- Header/footer SHOULD use `menu()` for nav with designed hardcoded fallback links when no menu is selected (marketers get the menu editor; visitors never see an empty nav).
- Every module ships `meta.json` with `host_template_types` + `content_types` covering its placements.
- Form-module marker: a module is a form module iff its `fields.json` contains a field with `"type": "form"`; `deploy.sh` refuses to run when any form module lacks a `portals.yaml` `forms:` entry. A form module MUST render via a native `{% form %}` tag; custom-JS submit is allowed only with an explicit `data-hsforms-ignore` declaration (validator warns).
- Blog-post templates use static `{% module %}` tags, not `dnd_area`. Page/blog-listing templates use `dnd_area`.

## 4. deploy.json schema (skill-custom)

```json
{"pages": [{"slug": "", "title": "Home", "templatePath": "templates/home.html", "menuOrder": 10, "isHomepage": true}]}
```

Every template has exactly one entry; exactly one `isHomepage: true`; slugs unique.

## 5. assets.json schema (skill-custom)

```json
{"files": [{"local": "images/hero/x.jpg", "dest": "/brand/x.jpg"}]}
```

Every image default `src` in every module `fields.json` has exactly one entry; every entry's `local` file exists; `dest` paths are absolute File Manager paths.

## 6. Asset rules

- Marketer-swappable images → File Manager via manifest, referenced by absolute `dest` path.
- Downloadable binaries (PDFs) ride the same manifest → File Manager flow (`dest` e.g. `/files/guide.pdf`); link them by absolute hubfs URL and cover every link in linkcheck (same 404 rules as images).
- `get_asset_url` images allowed only for CSS/structural decoration.
- `.hsignore` supported for local-only files (never uploaded).
