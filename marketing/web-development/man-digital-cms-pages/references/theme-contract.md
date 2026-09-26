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
- `blog_listing` + `blog_post` read post data from `content`/`group`; only chrome (breadcrumb, labels) is editable.
- Every module ships `meta.json` with `host_template_types` + `content_types` covering its placements.
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
- `get_asset_url` images allowed only for CSS/structural decoration.
- `.hsignore` supported for local-only files (never uploaded).
