# GitHub Input Adapter

## 1. Intake

Input is repo URL + branch. Private repos via `gh` CLI auth (verified: `gh auth status` shows `repo` scope). Clone:

```bash
workdir="${CMS_THEME_INPUT_SOURCE:-/tmp/cms-theme-input}"
rm -rf "$workdir" && gh repo clone <owner>/<repo> "$workdir" -- --branch <branch> --depth 1
```

Never accept a local path as a substitute input.

## 2. Discovery signals (verified on reference repo)

| Signal | Means |
|---|---|
| `vite.config.*` + `src/routes/` + generated route tree | File-based pages → one template each |
| `src/pages/*.tsx` | Template composition per page |
| `src/components/*.tsx` (+`layout/`) | One module per section; `layout/` → header/footer |
| `components.json` + `@radix-ui/*` deps | shadcn present |
| `@tailwindcss/*` dep | Tailwind present |
| `src/styles/tokens.json` + generator script | Token source of truth — read the JSON, never the generated CSS |
| `src/content/<lang>/` + content data files | Copy + blog/news model |
| `src/assets/*` | Bundled images → `/assets/...` manifest entries |
| `public/*` | Static files → File Manager root paths (`public/brand/` → `/brand/`) |
| Route prefixes (`en.*`) + content langs | Language list |
| Draft/editor/404 routes | Flag for exclusion, never templates |

Missing Vite/Tailwind/shadcn signals → stop with a report listing which signals were absent. Do not guess.

## 3. Inventory schema

Write `$workdir/INVENTORY.json` (builder consumes this, never the raw repo):

```json
{
  "repo": "https://github.com/OWNER/REPO",
  "branch": "main",
  "commit": "<full sha>",
  "pages": [{"route": "/", "template": "home", "title": "Home", "menuOrder": 10, "homepage": true}],
  "excluded_routes": [{"route": "/redaktor/*", "reason": "editor-only"}],
  "sections": [{"component": "src/components/Hero.tsx", "module": "hero", "fields_hint": ["heading", "image"]}],
  "tokens_file": "src/styles/tokens.json",
  "content": {"langs": ["nb", "en"], "copy_dir": "src/content", "blog_source": "src/content/news.ts"},
  "assets": {"bundled_dir": "src/assets", "public_dir": "public"},
  "forms": [{"component": "src/components/EnquiryForm.tsx", "module": "enquiry_form"}],
  "menus": [{"id": "site_root", "items_from": "routes"}],
  "external_urls": ["https://fonts.googleapis.com"],
  "verbatim": []
}
```

`external_urls` is the gate-4 allowlist: every external URL in the output must appear here or the gate fails. `verbatim` lists literal strings allowed to appear outside HubL tags (gate 2 hardcoded-copy check); default empty.
