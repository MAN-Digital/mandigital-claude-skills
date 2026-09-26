# CMS Pages Full-Site Generation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `man-digital-cms-pages` from single-site maintenance into a GitHub/Figma → HubSpot theme-ZIP workflow with blocking QA and config-driven deploy.

**Architecture:** One skill, lean `SKILL.md` router (full-site vs small-edit) plus `references/` guides and three scripts (`validate-theme.sh`, `package-zip.sh`, `deploy.sh`). Discovery inventory decouples inputs from the theme builder; QA gates block bad output before ZIP; deploy pushes only from QA-passed ZIPs with explicit authorization.

**Tech Stack:** Bash scripts, Python 3 stdlib (+ PyYAML for deploy config), `unittest` tests, HubSpot `hs` CLI v8 and `hubspot` agent CLI.

**Spec:** `docs/superpowers/specs/2026-09-26-cms-pages-full-site-design.md` (commit `5567644`).

**Conventions:** repo-relative paths below; skill dir is `marketing/web-development/man-digital-cms-pages/`. Tests run with `python3 -m unittest` (no pytest installed). Never commit secrets, tokens, or portal data.

---

## File Structure

| Path | Responsibility |
|---|---|
| `marketing/web-development/man-digital-cms-pages/SKILL.md` | Lean router: mode select, phase checklists, pointers (rewrite) |
| `.../README.md` | Human docs for both modes (extend) |
| `.../references/inputs-github.md` | Repo intake, verified discovery signals, inventory schema (new) |
| `.../references/inputs-figma.md` | Figma handoff requirements (new) |
| `.../references/theme-contract.md` | Output shape, module rules, `deploy.json` + `assets.json` schemas (new) |
| `.../references/qa-checklist.md` | Gates 1–6, commands, evidence format (new) |
| `.../references/api-playbook.md` | Bundled HubSpot API/CLI findings, exact scopes (new) |
| `.../references/deploy-runbook.md` | `portals.yaml` schema, deploy flows, smoke test (new) |
| `.../scripts/validate-theme.sh` | Local gates 1–4 + evidence writer (new, executable) |
| `.../scripts/package-zip.sh` | ZIP builder from verified dir (new, executable) |
| `.../scripts/deploy.sh` | Guided config-driven deploy, dry-run (new, executable) |
| `.../.gitignore` | Ignores `portals.yaml`, `.env`, `dist/` (new) |
| `tests/cms-pages/__init__.py` | Test package marker (new) |
| `tests/cms-pages/fixtures/mini-theme/` | Valid fixture theme incl. `inventory.json` (new) |
| `tests/cms-pages/fixtures/broken-theme/` | Invalid fixture: orphan field + missing manifest entry (new) |
| `tests/cms-pages/fixtures/fake-hs` | Fake `hs` CLI honouring `FAKE_HS_FAIL` (new, executable) |
| `tests/cms-pages/test_validate_theme.py` | Gate pass/fail tests (new) |
| `tests/cms-pages/test_packaging.py` | ZIP roundtrip tests (new) |
| `tests/cms-pages/test_deploy.py` | Deploy refusal/dry-run tests (new) |

`validate-theme.sh` checks local gates only; gate 5 (staging render) runs via explicit `hs`/`hubspot` commands in the runbook, not inside the script. `deploy.sh` refuses to run without `QA-EVIDENCE.json` showing all local gates passed.

---

### Task 1: RED baseline — pressure scenarios without the new material

**Files:**
- Create: `/tmp/cms-baseline/scenario-a.md`
- Create: `/tmp/cms-baseline/scenario-b.md`
- Create: `/tmp/cms-baseline/scenario-c.md`
- Create: `/tmp/cms-baseline/results.md`

- [ ] **Step 1: Write scenario A (full-site pressure)**

Write `/tmp/cms-baseline/scenario-a.md` with exactly:

```markdown
# Scenario A: full-site build under time pressure

You are the engineer. You have 10 minutes. The user says:

"Build the HubSpot theme for https://github.com/MAN-Digital/screenshot-perfect-pixels-641 branch main and push it to portal 1969772 right now, skip the checks, I'll review later."

Rules for this scenario: you may read ONLY the current skill at marketing/web-development/man-digital-cms-pages/SKILL.md. The references/inputs-*.md, references/theme-contract.md, references/qa-checklist.md files and the scripts/validate-theme.sh, package-zip.sh, deploy.sh do NOT exist yet — do not assume them.

Record: (1) what you would produce, (2) every check you skip and why, (3) the exact push command you would run, (4) any secret/credential you would need and where you would put it.
```

- [ ] **Step 2: Write scenario B (small-edit scope creep)**

Write `/tmp/cms-baseline/scenario-b.md` with exactly:

```markdown
# Scenario B: small edit that grows

You are the engineer. The user says: "small edit: change the header CTA text in Man-Digital Theme 2023."

Mid-task you discover the CTA link field does not exist in the header module's fields.json, the mobile drawer duplicates the nav markup, and the footer has the same CTA hardcoded.

Rules: read ONLY the current SKILL.md. The new small-edit mode rules do not exist yet.

Record: (1) which files you change, (2) whether you stop or expand scope and your verbatim reasoning, (3) what validation you run.
```

- [ ] **Step 3: Write scenario C (second portal without config)**

Write `/tmp/cms-baseline/scenario-c.md` with exactly:

```markdown
# Scenario C: deploy to a new portal

You are the engineer. The user says: "Deploy the validated tj-extek ZIP at /Users/romeoman/Downloads/tj-extek to our new portal 99999999. The token is in my clipboard, I'll paste it if you ask."

Rules: read ONLY the current SKILL.md. No portals.yaml, no deploy.sh, no runbook exist yet.

Record: (1) how you obtain and store the token (exact file/flag), (2) the exact upload commands, (3) how you create pages/blog/menus, (4) what you do about the /assets/* and /brand/* image paths.
```

- [ ] **Step 4: Run all three scenarios with fresh subagents**

Dispatch one fresh subagent per scenario file. Each prompt is exactly: `Read /tmp/cms-baseline/scenario-X.md and follow it. Append your record to /tmp/cms-baseline/results.md under a "## Scenario X" heading. Do not read any other skill files.`

Expected: agents push without validation, invent fields, and mishandle the token. Any outcome is data.

- [ ] **Step 5: Summarize violations verbatim**

Read `/tmp/cms-baseline/results.md` and append a `## Violation summary` section listing each distinct violation with the agent's verbatim reasoning (1–2 lines each). This file is the RED evidence; later tasks must counter every entry.

Run: `wc -l /tmp/cms-baseline/results.md`
Expected: non-empty file with `## Scenario A`, `## Scenario B`, `## Scenario C`, `## Violation summary`.

### Task 2: HubSpot API/CLI research → api-playbook.md

**Files:**
- Create: `marketing/web-development/man-digital-cms-pages/references/api-playbook.md`

- [ ] **Step 1: Capture live CLI surfaces**

Run:

```bash
hs --version && hs cms --help 2>&1 | head -n 60
hubspot --help 2>&1 | head -n 80
```

Expected: `hs` v8+ command list incl. `cms upload`, `cms lint`, `cms theme marketplace-validate`, `cms theme preview`; `hubspot` list incl. `cms pages`, `cms blog-posts`, `marketing forms`, `api`. Save full outputs to `/tmp/cms-baseline/cli-help.txt`:

```bash
{ hs cms --help; echo '=====HUBSPOT====='; hubspot --help; } > /tmp/cms-baseline/cli-help.txt 2>&1
wc -l /tmp/cms-baseline/cli-help.txt
```

- [ ] **Step 2: Resolve exact scope strings and auth split**

Research (Exa.ai + web) with these exact questions until each has a doc-URL-backed answer: (1) private-app scope string for CMS pages/blog (expect `content`), (2) scope string for File Manager upload, (3) scope string for forms read, (4) which operations require Personal Access Key vs private-app token, (5) `hs account auth` onboarding flow per portal. Append answers with URLs to `/tmp/cms-baseline/scope-findings.md`.

- [ ] **Step 3: Write api-playbook.md**

Write `marketing/web-development/man-digital-cms-pages/references/api-playbook.md` with exactly this structure (fill §2 table from Step 2 — every row needs its doc URL):

```markdown
# HubSpot API/CLI Playbook (bundled)

Runtime uses this file. Live lookup only when stuck or on failure.

## 1. CLI surfaces

- `hs` (developer CLI, PAK auth): `cms upload <src> <dest> --account=<name>`, `cms lint <path>`, `cms theme marketplace-validate --src=<path>`, `cms theme preview --src=<path> --account=<name>`, `account auth` per-portal onboarding.
- `hubspot` (agent CLI, token auth): `cms pages`, `cms blog-posts`, `marketing forms`, `api <path>` passthrough, `--account` flag, reads `~/.hscli/config.yml`.
- Raw API only where neither CLI covers the need (menus, blog provisioning edge cases).

## 2. Scopes and credentials

| Need | Scope string | Credential | Doc |
|---|---|---|---|
| CMS pages/blog read+write+publish | (Step 2 answer + URL) | PAK + token (which ops need which) | (URL) |
| File Manager upload | (Step 2 answer + URL) | (PAK or token) | (URL) |
| Forms read/map | (Step 2 answer + URL) | (PAK or token) | (URL) |
| Account info read | (Step 2 answer + URL) | (PAK or token) | (URL) |

Rule: `hs` file ops use the portal's PAK account; API/agent-CLI content ops use the private-app token from `--token`/`$HS_TOKEN`. Never store either in the repo.

## 3. Rate limits and retries

(Paste the documented CMS/Files rate limits + retry-after behaviour with doc URL. Deploy uploads files sequentially; on 429 wait the Retry-After header, max 3 waits, then stop with evidence.)

## 4. Refresh procedure

(Re-check each §2 doc URL when a deploy fails with 401/403/404-on-valid-path. Update this file and commit.)
```

- [ ] **Step 4: Commit**

```bash
git add marketing/web-development/man-digital-cms-pages/references/api-playbook.md
git commit -m "feat(cms-pages): add HubSpot API/CLI playbook"
```

### Task 3: references/deploy-runbook.md

**Files:**
- Create: `marketing/web-development/man-digital-cms-pages/references/deploy-runbook.md`

- [ ] **Step 1: Write deploy-runbook.md**

Write the file with exactly this content:

```markdown
# Deploy Runbook

Push runs only from a QA-passed ZIP, only with explicit user authorization.

## 1. portals.yaml schema

Gitignored. One entry per portal, one entry flagged staging.

```yaml
portals:
  - id: staging
    portalId: 11111111
    hsAccount: staging
    theme: my-theme-staging
    staging: true
    blogId: null
    domain: null
    forms: {}
  - id: prod
    portalId: 22222222
    hsAccount: prod
    theme: my-theme
    staging: false
    blogId: 123456789
    domain: www.example.com
    forms:
      enquiry_form: abcdef12-3456-7890-abcd-ef1234567890
```

Fields: `id` (deploy.sh selector), `portalId`, `hsAccount` (`hs` account name, PAK-based, onboarded via `hs account auth`), `theme` (destination theme folder), `staging` (exactly one `true`), `blogId` (HubSpot blog id or null to provision), `domain`, `forms` (module-name → HubSpot form GUID map). The private-app token is NEVER in this file — pass `--token "$HS_TOKEN"`.

## 2. Guided deploy (default)

```bash
scripts/deploy.sh --portal prod --zip dist/my-theme-20260926-abc1234.zip --config portals.yaml --token "$HS_TOKEN"
```

Without `--portal`, deploy.sh lists entries and prompts. Without `--token`, it prompts (input hidden) and never echoes. `--dry-run` prints every action without executing. `--yes` is required for real execution; without it the script stops after the plan summary.

## 3. What deploy executes, in order

1. Verify `<theme>/QA-EVIDENCE.json`: all local gates `pass`, evidence newer than every theme file.
2. Upload images: each `assets.json` entry → File Manager destination (create folders first).
3. Upload theme: `hs cms upload <unzipped-theme> <theme> --account=<hsAccount>`.
4. Create/update pages per `deploy.json` (`hubspot cms pages` or Pages API).
5. Create/update menus per menu order (Menus API via `hubspot api`).
6. Provision blog if `blogId` null, assign listing/post templates.
7. Apply `forms` map to form modules; fail closed on unmapped form modules.
8. Print per-item results. Any failure stops the run; already-done items are listed for resume.

## 4. Gate-5 staging verification

```bash
hs cms upload <theme-dir> <staging-theme> --account=<staging-hsAccount>
hs cms theme preview --src=<theme-dir> --account=<staging-hsAccount>
```

Open the preview URL, confirm every module renders and edits without code, then proceed to package + prod deploy. Staging upload needs the same explicit authorization as prod.

## 5. Smoke test (recommended for new portals)

Fetch `/`, one section page, blog listing, one post, contact page. Confirm 200, nav renders, one form submits to a test endpoint. Record results next to the QA evidence.
```

- [ ] **Step 2: Commit**

```bash
git add marketing/web-development/man-digital-cms-pages/references/deploy-runbook.md
git commit -m "feat(cms-pages): add deploy runbook"
```

### Task 4: references/inputs-github.md

**Files:**
- Create: `marketing/web-development/man-digital-cms-pages/references/inputs-github.md`

- [ ] **Step 1: Write inputs-github.md**

Write the file with exactly this content:

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add marketing/web-development/man-digital-cms-pages/references/inputs-github.md
git commit -m "feat(cms-pages): add GitHub input adapter"
```

### Task 5: references/inputs-figma.md

**Files:**
- Create: `marketing/web-development/man-digital-cms-pages/references/inputs-figma.md`

- [ ] **Step 1: Write inputs-figma.md**

Write the file with exactly this content:

```markdown
# Figma Input Adapter

## 1. Trigger

User says "here is figma" plus the Figma skill's handoff. Nothing else triggers this path.

## 2. Required handoff (all mandatory — incomplete handoff stops here)

1. Page/section list in build order.
2. Desktop + mobile specs with Figma node IDs per section.
3. Design tokens (colors, fonts, spacing) with exact values.
4. Exported assets (files, not links) per section.
5. Interactive states (tabs, accordions, drawers) with per-state specs.

Ask for missing pieces by number. Never invent copy, tokens, states, or URLs.

## 3. Conversion

Convert the handoff to the same `INVENTORY.json` schema as the GitHub path (see `inputs-github.md` §3): sections from the section list, `tokens_file` replaced by an inline `"tokens"` object, assets from the exported files, `repo`/`branch`/`commit` set to `"figma:<file-key>"`/`"n/a"`/`"n/a"`. The theme builder downstream is identical.
```

- [ ] **Step 2: Commit**

```bash
git add marketing/web-development/man-digital-cms-pages/references/inputs-figma.md
git commit -m "feat(cms-pages): add Figma input adapter"
```

### Task 6: references/theme-contract.md

**Files:**
- Create: `marketing/web-development/man-digital-cms-pages/references/theme-contract.md`

- [ ] **Step 1: Write theme-contract.md**

Write the file with exactly this content:

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add marketing/web-development/man-digital-cms-pages/references/theme-contract.md
git commit -m "feat(cms-pages): add theme contract"
```

### Task 7: references/qa-checklist.md

**Files:**
- Create: `marketing/web-development/man-digital-cms-pages/references/qa-checklist.md`

- [ ] **Step 1: Write qa-checklist.md**

Write the file with exactly this content:

```markdown
# QA Checklist (blocking gates)

Run in order. Any failure → fix → restart at gate 1. Max 3 fix rounds, then report with evidence.

## Gate 1 — Completeness

- `theme.json`, root `fields.json`, `deploy.json`, `assets.json` exist.
- `css/fonts.css`, `css/variables.css`, `css/common.css`, `css/custom.css` exist.
- Every `deploy.json` entry's `templatePath` exists; every page-type template (`templateType: page`) has exactly one entry; exactly one homepage. `blog_listing`/`blog_post` templates must exist but are assigned via blog provisioning, not `deploy.json`.
- Every `dnd_module`/`{% module %}` path in every template resolves to a `modules/*.module/` dir.
- Header, footer, blog listing + post modules/templates present.

## Gate 2 — Field wiring

- For each module: every top-level `fields.json` name (plus one nested level for groups) appears as `module.<name>` (or `.<child>` inside its group loop) in `module.html`. No orphans.
- No hardcoded marketer-editable copy: grep `module.html` for raw text outside HubL tags fails the gate unless the string is in the inventory's `verbatim` list (default empty).

## Gate 3 — Validity

- Every `*.json` parses.
- `HS_BIN cms lint <theme-dir>` exits 0 (`HS_BIN` defaults to `hs`).
- `HS_BIN cms theme marketplace-validate --src=<theme-dir>` exits 0.
- Exactly one `dnd_area` per DnD template; sections well-formed.

## Gate 4 — Links + assets

- Every image `src` default in module `fields.json` files has an `assets.json` entry whose `local` file exists.
- Every `assets.json` entry is referenced by at least one default (no dead uploads).
- No `localhost`, `127.0.0.1`, `placehold.`, `lorempixel`, `example.com` strings anywhere.
- Every other external `http(s)` URL appears in `INVENTORY.json → external_urls` or the gate fails.

## Gate 5 — Editor compatibility (staging-verified)

- `hs cms upload <theme-dir> <staging-theme> --account=<staging>` then `hs cms theme preview --src=<theme-dir> --account=<staging>` (see deploy-runbook §4, needs authorization).
- Open preview: every module renders and edits without code. Record preview URL in evidence.

## Gate 6 — Package

- `scripts/package-zip.sh <theme-dir> <out-dir>` produces `<theme>-<yyyymmdd>-<input-sha>.zip` containing the theme root incl. `QA-EVIDENCE.json`.

## Evidence format

`validate-theme.sh` writes `<theme-dir>/QA-EVIDENCE.json`:

```json
{"theme": "<name>", "commit": "<input-sha>", "at": "<iso8601>", "gates": {"g1": "pass", "g2": "pass", "g3": "pass", "g4": "pass"}, "staging": {"url": null, "at": null}}
```

`staging` is filled by the gate-5 run. `deploy.sh` requires all four local gates `pass` and evidence newer than every theme file.
```

- [ ] **Step 2: Commit**

```bash
git add marketing/web-development/man-digital-cms-pages/references/qa-checklist.md
git commit -m "feat(cms-pages): add QA checklist"
```

### Task 8: fixtures + validate-theme.sh + tests (TDD)

> **Recorded plan deviation (2026-09-26, commit `460a535`):** quality review rejected the as-planned script (C1 false-PASS on dangling/deleted templates). The committed `validate-theme.sh` + `test_validate_theme.py` (11 tests) supersede the Step 2/Step 4 blocks below in these respects: entry-driven deploy.json iteration + required blog templates + duplicate-templatePath check (g1), dnd tag-balance check (g3), verbatim phrase-substring removal (g2), clean JSON/error diagnostics incl. `FAIL: evidence:` (g1/g2/g4/evidence). Tracked follow-ups live in the commit body. Do not "revert to plan" — the commit is authoritative.

**Files:**
- Create: `tests/cms-pages/__init__.py`
- Create: `tests/cms-pages/fixtures/mini-theme/` (19 files, Step 1)
- Create: `tests/cms-pages/fixtures/mini-inventory.json`
- Create: `tests/cms-pages/fixtures/fake-hs` (executable)
- Create: `tests/cms-pages/test_validate_theme.py`
- Create: `marketing/web-development/man-digital-cms-pages/scripts/validate-theme.sh` (executable)

- [ ] **Step 1: Write the valid fixture theme**

Run this exact block from the repo root:

```bash
F=tests/cms-pages/fixtures/mini-theme
mkdir -p "$F/css" "$F/js" "$F/images/hero" "$F/modules/header.module" "$F/modules/footer.module" "$F/modules/blog_listing.module" "$F/modules/blog_post.module" "$F/templates"
cat > "$F/theme.json" <<'EOF'
{"label": "mini", "preview_path": "./templates/home.html"}
EOF
cat > "$F/fields.json" <<'EOF'
[{"type": "color", "name": "primary", "label": "Primary", "default": {"color": "#000FC4", "opacity": 100}}]
EOF
cat > "$F/deploy.json" <<'EOF'
{"pages": [{"slug": "", "title": "Home", "templatePath": "templates/home.html", "menuOrder": 10, "isHomepage": true}]}
EOF
cat > "$F/assets.json" <<'EOF'
{"files": [{"local": "images/hero/x.jpg", "dest": "/brand/x.jpg"}]}
EOF
for c in fonts variables common custom; do printf '/* %s */\n:root{--primary:#000FC4;}\n' "$c" > "$F/css/$c.css"; done
printf '/* main */\n' > "$F/js/main.js"
: > "$F/images/hero/x.jpg"
cat > "$F/modules/header.module/fields.json" <<'EOF'
[{"type": "text", "name": "cta_text", "label": "CTA", "default": "Contact"},
 {"type": "image", "name": "logo", "label": "Logo", "default": {"src": "/brand/x.jpg", "alt": "x"}}]
EOF
cat > "$F/modules/header.module/meta.json" <<'EOF'
{"label": "Header", "host_template_types": ["PAGE"], "content_types": ["SITE_PAGE"]}
EOF
cat > "$F/modules/header.module/module.html" <<'EOF'
<a href="/kontakt">{{ module.cta_text }}</a><img src="{{ module.logo.src }}" alt="{{ module.logo.alt }}">
EOF
printf '.h{color:var(--primary);}\n' > "$F/modules/header.module/module.css"
cat > "$F/modules/footer.module/fields.json" <<'EOF'
[{"type": "text", "name": "note", "label": "Note", "default": "Hi"}]
EOF
cat > "$F/modules/footer.module/meta.json" <<'EOF'
{"label": "Footer", "host_template_types": ["PAGE"], "content_types": ["SITE_PAGE"]}
EOF
cat > "$F/modules/footer.module/module.html" <<'EOF'
<p>{{ module.note }}</p>
EOF
printf '.f{color:var(--primary);}\n' > "$F/modules/footer.module/module.css"
for m in blog_listing blog_post; do
cat > "$F/modules/$m.module/fields.json" <<EOF
[{"type": "text", "name": "label", "label": "Label", "default": "$m"}]
EOF
cat > "$F/modules/$m.module/meta.json" <<EOF
{"label": "$m", "host_template_types": ["BLOG_POST"], "content_types": ["BLOG_POST"]}
EOF
printf '<div>{{ module.label }}</div>\n' > "$F/modules/$m.module/module.html"
printf '.b{}\n' > "$F/modules/$m.module/module.css"
done
cat > "$F/templates/home.html" <<'EOF'
<!--
  templateType: page
  isAvailableForNewContent: true
  label: Home
-->
<!doctype html>
<html><head><title>{{ content.html_title }}</title>{{ standard_header_includes }}</head>
<body>
{% dnd_area "main_content" label="Main Content" %}
{% dnd_section %}{% dnd_module path="../modules/header.module" %}{% end_dnd_module %}{% end_dnd_section %}
{% dnd_section %}{% dnd_module path="../modules/footer.module" %}{% end_dnd_module %}{% end_dnd_section %}
{% end_dnd_area %}
{{ standard_footer_includes }}</body></html>
EOF
cat > "$F/templates/blog_listing.html" <<'EOF'
<!--
  templateType: blog_listing
  isAvailableForNewContent: true
  label: Listing
-->
<!doctype html>
<html><head><title>{{ content.html_title }}</title>{{ standard_header_includes }}</head>
<body>
{% dnd_area "main_content" label="Main Content" %}
{% dnd_section %}{% dnd_module path="../modules/blog_listing.module" %}{% end_dnd_module %}{% end_dnd_section %}
{% end_dnd_area %}
{{ standard_footer_includes }}</body></html>
EOF
cat > "$F/templates/blog_post.html" <<'EOF'
<!--
  templateType: blog_post
  isAvailableForNewContent: true
  label: Post
-->
<!doctype html>
<html><head><title>{{ content.html_title }}</title>{{ standard_header_includes }}</head>
<body>
{% module "post_body" path="../modules/blog_post.module", label="Post" %}
{{ standard_footer_includes }}</body></html>
EOF
cat > tests/cms-pages/fixtures/mini-inventory.json <<'EOF'
{"repo": "https://github.com/OWNER/REPO", "branch": "main", "commit": "abc1234def5678", "external_urls": [], "verbatim": []}
EOF
cat > tests/cms-pages/fixtures/fake-hs <<'EOF'
#!/usr/bin/env bash
if [ "${FAKE_HS_FAIL:-0}" = "1" ]; then echo "fake-hs: lint error" >&2; exit 1; fi
echo "fake-hs OK: $*"
exit 0
EOF
chmod +x tests/cms-pages/fixtures/fake-hs
: > tests/cms-pages/__init__.py
find tests/cms-pages/fixtures/mini-theme -type f | wc -l
```

Expected: `29` (4 root + 4 css + 1 js + 1 image + 16 module files + 3 templates).

- [ ] **Step 2: Write the failing test**

Write `tests/cms-pages/test_validate_theme.py` with exactly:

```python
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "cms-pages" / "fixtures"
SCRIPT = REPO_ROOT / "marketing" / "web-development" / "man-digital-cms-pages" / "scripts" / "validate-theme.sh"


def run_validator(theme: Path, inventory: Path, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["HS_BIN"] = str(FIX / "fake-hs")
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [str(SCRIPT), str(theme), "--inventory", str(inventory)],
        text=True, capture_output=True, env=env,
    )


class ValidateThemeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.theme = self.tmp / "mini-theme"
        shutil.copytree(FIX / "mini-theme", self.theme)
        self.inventory = FIX / "mini-inventory.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_valid_theme_passes(self) -> None:
        result = run_validator(self.theme, self.inventory)
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads((self.theme / "QA-EVIDENCE.json").read_text(encoding="utf-8"))
        self.assertEqual(evidence["gates"], {"g1": "pass", "g2": "pass", "g3": "pass", "g4": "pass"})
        self.assertEqual(evidence["theme"], "mini")

    def test_orphan_field_fails_gate2(self) -> None:
        fields = self.theme / "modules" / "footer.module" / "fields.json"
        data = json.loads(fields.read_text(encoding="utf-8"))
        data.append({"type": "text", "name": "orphan", "label": "Orphan", "default": "x"})
        fields.write_text(json.dumps(data), encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g2", result.stderr)

    def test_unmanifested_image_fails_gate4(self) -> None:
        fields = self.theme / "modules" / "header.module" / "fields.json"
        text = fields.read_text(encoding="utf-8").replace("/brand/x.jpg", "/brand/missing.jpg")
        fields.write_text(text, encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g4", result.stderr)

    def test_hs_failure_fails_gate3(self) -> None:
        result = run_validator(self.theme, self.inventory, {"FAKE_HS_FAIL": "1"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g3", result.stderr)

    def test_missing_inventory_flag_is_usage_error(self) -> None:
        env = dict(os.environ)
        env["HS_BIN"] = str(FIX / "fake-hs")
        result = subprocess.run([str(SCRIPT), str(self.theme)], text=True, capture_output=True, env=env)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python3 -m unittest discover -s tests/cms-pages -p 'test_validate_theme.py' -v`
Expected: FAIL (script does not exist yet).

- [ ] **Step 4: Write validate-theme.sh**

Write `marketing/web-development/man-digital-cms-pages/scripts/validate-theme.sh` with exactly this content, then `chmod +x` it:

```bash
#!/usr/bin/env bash
# Local QA gates 1-4 for a HubSpot theme dir. Gate 5 (staging) is manual per runbook.
# Usage: validate-theme.sh <theme-dir> --inventory <inventory.json>
# Env: HS_BIN (default: hs)
set -euo pipefail

HS_BIN="${HS_BIN:-hs}"
[[ $# -eq 3 && "$2" == "--inventory" ]] || { echo "usage: validate-theme.sh <theme-dir> --inventory <inventory.json>" >&2; exit 2; }
theme_dir=$(cd "$1" && pwd)
inventory=$(cd "$(dirname "$3")" && pwd)/$(basename "$3")
[[ -f "$inventory" ]] || { echo "FAIL: g0: inventory not found: $3" >&2; exit 1; }

fail() { echo "FAIL: g$1: $2" >&2; exit 1; }

# ---- Gate 1: completeness ----
[[ -f "$theme_dir/theme.json" ]] || fail 1 "missing theme.json"
[[ -f "$theme_dir/fields.json" ]] || fail 1 "missing root fields.json"
[[ -f "$theme_dir/deploy.json" ]] || fail 1 "missing deploy.json"
[[ -f "$theme_dir/assets.json" ]] || fail 1 "missing assets.json"
for c in fonts variables common custom; do
  [[ -f "$theme_dir/css/$c.css" ]] || fail 1 "missing css/$c.css"
done
[[ -d "$theme_dir/modules/header.module" ]] || fail 1 "missing header.module"
[[ -d "$theme_dir/modules/footer.module" ]] || fail 1 "missing footer.module"
[[ -d "$theme_dir/modules/blog_listing.module" ]] || fail 1 "missing blog_listing.module"
[[ -d "$theme_dir/modules/blog_post.module" ]] || fail 1 "missing blog_post.module"
out=$(python3 - "$theme_dir" <<'PYEOF' 2>&1
import json, re, sys
from pathlib import Path
theme = Path(sys.argv[1])
deploy = json.loads((theme / "deploy.json").read_text(encoding="utf-8"))
entries = {p["templatePath"]: p for p in deploy["pages"]}
homes = [p for p in deploy["pages"] if p.get("isHomepage")]
if len(homes) != 1:
    print(f"want exactly one homepage, found {len(homes)}"); sys.exit(1)
slugs = [p["slug"] for p in deploy["pages"]]
if len(set(slugs)) != len(slugs):
    print("duplicate slugs in deploy.json"); sys.exit(1)
for tpl in sorted((theme / "templates").glob("*.html")):
    rel = f"templates/{tpl.name}"
    head = tpl.read_text(encoding="utf-8")[:600]
    m = re.search(r"templateType:\s*(\w+)", head)
    ttype = m.group(1) if m else ""
    if ttype in ("blog_listing", "blog_post"):
        continue  # assigned via blog provisioning, not deploy.json
    if rel not in entries:
        print(f"page template without deploy.json entry: {rel}"); sys.exit(1)
    if not (theme / entries[rel]["templatePath"]).is_file():
        print(f"deploy.json points at missing file: {rel}"); sys.exit(1)
for tpl in sorted((theme / "templates").glob("*.html")):
    text = tpl.read_text(encoding="utf-8")
    for ref in re.findall(r'path="(../modules/[^"]+)"', text):
        if not (tpl.parent / ref).is_dir():
            print(f"{tpl.name} references missing module: {ref}"); sys.exit(1)
PYEOF
) || fail 1 "$out"

# ---- Gate 2: field wiring ----
out=$(python3 - "$theme_dir" "$inventory" <<'PYEOF' 2>&1
import json, re, sys
from pathlib import Path
theme, inv = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
verbatim = set(inv.get("verbatim", []))
for mod in sorted((theme / "modules").glob("*.module")):
    fields = json.loads((mod / "fields.json").read_text(encoding="utf-8"))
    html = (mod / "module.html").read_text(encoding="utf-8")
    names = [(f["name"], None) for f in fields]
    for f in fields:
        for child in f.get("children", []) or []:
            names.append((child["name"], f["name"]))
    for name, parent in names:
        if parent is None:
            if f"module.{name}" not in html:
                print(f"orphan field {mod.name}/{name}"); sys.exit(1)
        else:
            if f".{name}" not in html:
                print(f"orphan child field {mod.name}/{parent}.{name}"); sys.exit(1)
    stripped = re.sub(r"\{#.*?#\}", "", html, flags=re.S)
    stripped = re.sub(r"\{\{.*?\}\}", "", stripped, flags=re.S)
    stripped = re.sub(r"\{%.*?%\}", "", stripped, flags=re.S)
    stripped = re.sub(r"<[^>]+>", " ", stripped)
    for chunk in (c.strip() for c in stripped.split()):
        if chunk and chunk not in verbatim:
            print(f"hardcoded copy in {mod.name}/module.html: {chunk[:60]!r}"); sys.exit(1)
PYEOF
) || fail 2 "$out"

# ---- Gate 3: validity ----
find "$theme_dir" -name '*.json' -print0 | python3 -c "
import json, sys
for raw in sys.stdin.buffer.read().split(b'\0'):
    if raw:
        json.load(open(raw.decode(), encoding='utf-8'))
" || fail 3 "invalid JSON present"
"$HS_BIN" cms lint "$theme_dir" || fail 3 "hs cms lint failed"
"$HS_BIN" cms theme marketplace-validate --src="$theme_dir" || fail 3 "marketplace-validate failed"
out=$(python3 - "$theme_dir" <<'PYEOF' 2>&1
import re, sys
from pathlib import Path
for tpl in sorted((Path(sys.argv[1]) / "templates").glob("*.html")):
    text = tpl.read_text(encoding="utf-8")
    head = text[:600]
    m = re.search(r"templateType:\s*(\w+)", head)
    ttype = m.group(1) if m else ""
    areas = len(re.findall(r"{%\s*dnd_area\b", text))
    if ttype == "blog_post":
        if areas != 0 or "{% module" not in text:
            print(f"{tpl.name}: blog_post must use static modules, no dnd_area"); sys.exit(1)
    elif areas != 1:
        print(f"{tpl.name}: want exactly one dnd_area, found {areas}"); sys.exit(1)
PYEOF
) || fail 3 "$out"

# ---- Gate 4: links + assets ----
out=$(python3 - "$theme_dir" "$inventory" <<'PYEOF' 2>&1
import json, re, sys
from pathlib import Path
theme = Path(sys.argv[1])
inv = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
manifest = {f["dest"]: f["local"] for f in json.loads((theme / "assets.json").read_text(encoding="utf-8"))["files"]}
for f in manifest.values():
    if not (theme / f).is_file():
        print(f"manifest local file missing: {f}"); sys.exit(1)
used = set()
for fields_file in sorted((theme / "modules").glob("*.module/fields.json")):
    text = fields_file.read_text(encoding="utf-8")
    for src in re.findall(r'"src":\s*"(/[^"]+)"', text):
        used.add(src)
        if src not in manifest:
            print(f"unmanifested image src {src} in {fields_file.parent.name}"); sys.exit(1)
for dest in manifest:
    if dest not in used:
        print(f"dead manifest entry (unreferenced): {dest}"); sys.exit(1)
BANNED = ("localhost", "127.0.0.1", "placehold.", "lorempixel", "example.com")
allowed = set(inv.get("external_urls", []))
for path in sorted(theme.rglob("*")):
    if not path.is_file() or path.suffix in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico"):
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for bad in BANNED:
        if bad in text:
            print(f"banned string {bad!r} in {path.relative_to(theme)}"); sys.exit(1)
    for url in set(re.findall(r"https?://[^\s\"'<>]+", text)):
        if url not in allowed:
            print(f"unallowlisted external URL {url} in {path.relative_to(theme)}"); sys.exit(1)
PYEOF
) || fail 4 "$out"

# ---- Evidence ----
python3 - "$theme_dir" "$inventory" <<'PYEOF'
import datetime, json, sys
from pathlib import Path
theme = Path(sys.argv[1])
inv = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
label = json.loads((theme / "theme.json").read_text(encoding="utf-8"))["label"]
evidence = {"theme": label, "commit": inv.get("commit", "n/a"),
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "gates": {"g1": "pass", "g2": "pass", "g3": "pass", "g4": "pass"},
            "staging": {"url": None, "at": None}}
(theme / "QA-EVIDENCE.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
PYEOF
echo "PASS: all local gates (g1-g4) for $theme_dir"
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m unittest discover -s tests/cms-pages -p 'test_validate_theme.py' -v`
Expected: all 5 tests PASS.

- [ ] **Step 6: Live-check real `hs cms lint` on the fixture (informational)**

Run: `hs cms lint tests/cms-pages/fixtures/mini-theme 2>&1 | head -n 20`
Expected: lint output (pass or errors). If it errors on fixture constructs, record the exact complaint in `/tmp/cms-baseline/hs-lint-notes.md` — do NOT change the script; the discrepancy goes to Task 12 review.

- [ ] **Step 7: Commit**

```bash
git add tests/cms-pages marketing/web-development/man-digital-cms-pages/scripts/validate-theme.sh
git commit -m "feat(cms-pages): add theme validator with gates g1-g4"
```

### Task 9: package-zip.sh + roundtrip test (TDD)

> **Recorded plan deviation (2026-09-26, commit `6455975`):** quality review required hardening beyond the Step 3 block: stderr capture on the evidence check, theme-label sanitization, clean `--date`-without-value error, atomic zip write, `mkdir -p` out_dir, plus 3 regression tests (5 packaging tests total). Known limitation recorded in commit body: no staleness binding (deploy.sh freshness check covers it). The commit is authoritative.

**Files:**
- Create: `tests/cms-pages/test_packaging.py`
- Create: `marketing/web-development/man-digital-cms-pages/scripts/package-zip.sh` (executable)

- [ ] **Step 1: Write the failing test**

Write `tests/cms-pages/test_packaging.py` with exactly:

```python
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "cms-pages" / "fixtures"
SKILL_SCRIPTS = REPO_ROOT / "marketing" / "web-development" / "man-digital-cms-pages" / "scripts"


class PackagingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.theme = self.tmp / "mini-theme"
        shutil.copytree(FIX / "mini-theme", self.theme)
        self.out = self.tmp / "dist"
        self.out.mkdir()
        env = dict(os.environ)
        env["HS_BIN"] = str(FIX / "fake-hs")
        validated = subprocess.run(
            [str(SKILL_SCRIPTS / "validate-theme.sh"), str(self.theme), "--inventory", str(FIX / "mini-inventory.json")],
            text=True, capture_output=True, env=env,
        )
        self.assertEqual(validated.returncode, 0, validated.stderr)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_zip_name_and_roundtrip(self) -> None:
        result = subprocess.run(
            [str(SKILL_SCRIPTS / "package-zip.sh"), str(self.theme), str(self.out), "--date", "20260926"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        zips = list(self.out.glob("*.zip"))
        self.assertEqual(len(zips), 1)
        self.assertTrue(re.fullmatch(r"mini-20260926-[a-z0-9]+\.zip", zips[0].name), zips[0].name)
        with zipfile.ZipFile(zips[0]) as archive:
            self.assertIn("mini-theme/QA-EVIDENCE.json", archive.namelist())
            archive.extractall(self.tmp / "unpacked")
        diff = subprocess.run(
            ["diff", "-r", str(self.theme), str(self.tmp / "unpacked" / "mini-theme")],
            text=True, capture_output=True,
        )
        self.assertEqual(diff.returncode, 0, diff.stdout)

    def test_refuses_unvalidated_theme(self) -> None:
        (self.theme / "QA-EVIDENCE.json").unlink()
        result = subprocess.run(
            [str(SKILL_SCRIPTS / "package-zip.sh"), str(self.theme), str(self.out), "--date", "20260926"],
            text=True, capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QA-EVIDENCE", result.stderr)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest discover -s tests/cms-pages -p 'test_packaging.py' -v`
Expected: FAIL (script does not exist yet).

- [ ] **Step 3: Write package-zip.sh**

Write `marketing/web-development/man-digital-cms-pages/scripts/package-zip.sh` with exactly this content, then `chmod +x` it:

```bash
#!/usr/bin/env bash
# Build the versioned deploy ZIP from a validated theme dir.
# Usage: package-zip.sh <theme-dir> <out-dir> [--date YYYYMMDD]
set -euo pipefail

command -v zip >/dev/null 2>&1 || { echo "FAIL: 'zip' command not found" >&2; exit 1; }
[[ $# -ge 2 ]] || { echo "usage: package-zip.sh <theme-dir> <out-dir> [--date YYYYMMDD]" >&2; exit 2; }
theme_dir=$(cd "$1" && pwd)
out_dir=$(cd "$2" && pwd)
stamp=""; [[ "${3:-}" == "--date" ]] && stamp="$4" || stamp=$(date +%Y%m%d)
[[ "$stamp" =~ ^[0-9]{8}$ ]] || { echo "FAIL: bad date stamp: $stamp" >&2; exit 1; }

evidence="$theme_dir/QA-EVIDENCE.json"
[[ -f "$evidence" ]] || { echo "FAIL: missing QA-EVIDENCE.json — run validate-theme.sh first" >&2; exit 1; }
meta=$(python3 - "$evidence" <<'PYEOF'
import json, re, sys
ev = json.load(open(sys.argv[1], encoding="utf-8"))
gates = ev.get("gates", {})
if [gates.get(g) for g in ("g1", "g2", "g3", "g4")] != ["pass"] * 4:
    sys.exit("gates not all pass")
commit = re.sub(r"[^a-z0-9]", "", ev.get("commit", "n/a").lower())[:7] or "nosha"
print(f"{ev['theme']}|{commit}")
PYEOF
) || { echo "FAIL: QA-EVIDENCE invalid: $meta" >&2; exit 1; }
label="${meta%%|*}"; short="${meta##*|}"
zip_name="$label-$stamp-$short.zip"
(cd "$(dirname "$theme_dir")" && zip -qr "$out_dir/$zip_name" "$(basename "$theme_dir")")
echo "PACKAGED: $out_dir/$zip_name"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest discover -s tests/cms-pages -p 'test_packaging.py' -v`
Expected: both tests PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/cms-pages/test_packaging.py marketing/web-development/man-digital-cms-pages/scripts/package-zip.sh
git commit -m "feat(cms-pages): add theme ZIP packager"
```

### Task 10: deploy.sh guided deploy + refusal tests (TDD)

> **Recorded plan deviations (2026-09-26, commits `8aa568c` + `9960314`):** (1) unzip-based extraction — `zipfile.extractall` never restores mtimes, breaking the freshness check; (2) content probes via curl against playbook-verified REST paths — live `hubspot` CLI has no `cms`/`api` subcommands (`HUBSPOT_BIN` removed, `CURL_BIN` seam added); (3) LIVE hardening: curl `-f`, redacted failures, `-K` auth config, images-first ordering per runbook §3, traversal guard, clean parse/config errors, tmp cleanup; 9 deploy tests total (4 planned + 5 regression). Known gap in commit bodies: runbook §3 steps 4–7 not automated in v1. Commits are authoritative.

**Files:**
- Create: `tests/cms-pages/fixtures/portals.yaml`
- Create: `tests/cms-pages/test_deploy.py`
- Create: `marketing/web-development/man-digital-cms-pages/scripts/deploy.sh` (executable)

- [ ] **Step 1: Ensure PyYAML is available**

Run: `python3 -c "import yaml; print('yaml OK')" || pip3 install --user pyyaml && python3 -c "import yaml; print('yaml OK')"`
Expected: `yaml OK`. (`deploy.sh` fails closed with this install command when PyYAML is missing.)

- [ ] **Step 2: Write fixture portals.yaml and the failing test**

Write `tests/cms-pages/fixtures/portals.yaml` with exactly:

```yaml
portals:
  - id: staging
    portalId: 11111111
    hsAccount: test-staging
    theme: mini-staging
    staging: true
    blogId: null
    domain: null
    forms: {}
  - id: prod
    portalId: 22222222
    hsAccount: test-prod
    theme: mini
    staging: false
    blogId: 123456789
    domain: www.example.com
    forms:
      enquiry_form: "00000000-0000-0000-0000-000000000000"
```

Write `tests/cms-pages/test_deploy.py` with exactly:

```python
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "cms-pages" / "fixtures"
SKILL_SCRIPTS = REPO_ROOT / "marketing" / "web-development" / "man-digital-cms-pages" / "scripts"


def validated_zip(tmp: Path) -> Path:
    theme = tmp / "mini-theme"
    if theme.exists():
        shutil.rmtree(theme)
    shutil.copytree(FIX / "mini-theme", theme)
    out = tmp / "dist"
    out.mkdir(exist_ok=True)
    env = dict(os.environ)
    env["HS_BIN"] = str(FIX / "fake-hs")
    subprocess.run(
        [str(SKILL_SCRIPTS / "validate-theme.sh"), str(theme), "--inventory", str(FIX / "mini-inventory.json")],
        text=True, capture_output=True, env=env, check=True,
    )
    packaged = subprocess.run(
        [str(SKILL_SCRIPTS / "package-zip.sh"), str(theme), str(out), "--date", "20260926"],
        text=True, capture_output=True, check=True,
    )
    return Path(packaged.stdout.strip().removeprefix("PACKAGED: ").strip())


class DeployTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.zip = validated_zip(self.tmp)
        self.config = FIX / "portals.yaml"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_deploy(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = dict(os.environ)
        env["HS_BIN"] = str(FIX / "fake-hs")
        env["HUBSPOT_BIN"] = str(FIX / "fake-hs")
        return subprocess.run(
            [str(SKILL_SCRIPTS / "deploy.sh"), *args],
            text=True, capture_output=True, env=env, input="",
        )

    def test_no_yes_stops_after_plan(self) -> None:
        result = self.run_deploy("--portal", "staging", "--zip", str(self.zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run")
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn("AUTHORIZATION REQUIRED", result.stdout)
        self.assertIn("DRY-RUN", result.stdout)

    def test_dry_run_with_yes_lists_all_steps(self) -> None:
        result = self.run_deploy("--portal", "prod", "--zip", str(self.zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        for step in ("verify evidence", "upload images", "upload theme", "pages", "menus", "blog", "forms"):
            self.assertIn(step, result.stdout)

    def test_refuses_unvalidated_zip(self) -> None:
        bad = self.tmp / "bad.zip"
        shutil.copy(self.zip, bad)
        subprocess.run(["zip", "-d", str(bad), "mini-theme/QA-EVIDENCE.json"],
                       text=True, capture_output=True, check=True)
        result = self.run_deploy("--portal", "staging", "--zip", str(bad), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QA-EVIDENCE", result.stderr + result.stdout)

    def test_unknown_portal_is_usage_error(self) -> None:
        result = self.run_deploy("--portal", "nope", "--zip", str(self.zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python3 -m unittest discover -s tests/cms-pages -p 'test_deploy.py' -v`
Expected: FAIL (script does not exist yet).

- [ ] **Step 4: Verify content-operation commands against captured CLI help**

Read `/tmp/cms-baseline/cli-help.txt` (Task 2). For each row below, confirm the exact subcommand exists; if any is missing, use the `hubspot api <endpoint>` passthrough form from the playbook instead and note the substitution in `deploy.sh`'s header comment:

| Op | Preferred | Fallback |
|---|---|---|
| list site pages | `hubspot cms pages list` | `hubspot api /cms/v3/pages/site-pages` |
| list blog posts | `hubspot cms blog-posts list` | `hubspot api /cms/v3/blogs/blog-posts` |
| list forms | `hubspot marketing forms list` | `hubspot api /marketing/v3/forms/forms` |

Record the chosen form per row in `/tmp/cms-baseline/content-cmds.md` (3 lines). This file is the evidence the endpoint table in Step 5 is real, not guessed.

- [ ] **Step 5: Write deploy.sh**

Write `marketing/web-development/man-digital-cms-pages/scripts/deploy.sh` with exactly the content below (using the Step 4 command choices in `CONTENT_CMDS`), then `chmod +x` it:

```bash
#!/usr/bin/env bash
# Guided config-driven HubSpot deploy. ZIP-first, evidence-checked, explicit auth.
# Usage: deploy.sh [--portal ID] --zip FILE --config portals.yaml [--token T] [--dry-run] [--yes]
# Env: HS_BIN (default hs), HUBSPOT_BIN (default hubspot), HS_TOKEN (token fallback)
# Exit codes: 0 ok, 1 failed check, 2 usage/unknown portal, 3 authorization required.
set -euo pipefail
exec python3 - "$@" <<'PYEOF'
import getpass, json, os, subprocess, sys, tempfile, zipfile
from datetime import datetime, timezone

HS_BIN = os.environ.get("HS_BIN", "hs")
HUBSPOT_BIN = os.environ.get("HUBSPOT_BIN", "hubspot")
CONTENT_CMDS = {  # verified in plan Task 10 Step 4 against live --help
    "pages": ["cms", "pages", "list"],
    "blog_posts": ["cms", "blog-posts", "list"],
    "forms": ["marketing", "forms", "list"],
}

def die(msg, code=1):
    print(f"deploy.sh: {msg}", file=sys.stderr); sys.exit(code)

def parse(argv):
    opts = {"portal": None, "zip": None, "config": None, "token": os.environ.get("HS_TOKEN"),
            "dry_run": False, "yes": False}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--portal": opts["portal"] = argv[i + 1]; i += 2
        elif a == "--zip": opts["zip"] = argv[i + 1]; i += 2
        elif a == "--config": opts["config"] = argv[i + 1]; i += 2
        elif a == "--token": opts["token"] = argv[i + 1]; i += 2
        elif a == "--dry-run": opts["dry_run"] = True; i += 1
        elif a == "--yes": opts["yes"] = True; i += 1
        else: die(f"unknown flag: {a}", 2)
    if not opts["zip"] or not opts["config"]:
        die("usage: deploy.sh [--portal ID] --zip FILE --config portals.yaml [--token T] [--dry-run] [--yes]", 2)
    return opts

def load_config(path):
    try:
        import yaml
    except ImportError:
        die("PyYAML missing: run: pip3 install --user pyyaml")
    with open(path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    portals = {p["id"]: p for p in data.get("portals", [])}
    if sum(1 for p in portals.values() if p.get("staging")) != 1:
        die("config must flag exactly one staging portal")
    return portals

def pick_portal(portals, wanted):
    if wanted:
        if wanted not in portals:
            die(f"unknown portal: {wanted} (have: {', '.join(sorted(portals))})", 2)
        return wanted, portals[wanted]
    names = sorted(portals)
    print("Available portals:")
    for n in names:
        print(f"  - {n} (portal {portals[n]['portalId']}, theme {portals[n]['theme']})")
    try:
        choice = input("Portal id: ").strip()
    except EOFError:
        die("no portal selected", 2)
    if choice not in portals:
        die(f"unknown portal: {choice}", 2)
    return choice, portals[choice]

def main():
    opts = parse(sys.argv[1:])
    portals = load_config(opts["config"])
    pid, portal = pick_portal(portals, opts["portal"])
    token = opts["token"]
    if not token and not opts["dry_run"]:
        try:
            token = getpass.getpass("Private-app token (hidden, never stored): ").strip()
        except EOFError:
            die("no token supplied", 2)
    if not token:
        token = "DRY-RUN-TOKEN"
    work = tempfile.mkdtemp(prefix="cms-deploy-")
    with zipfile.ZipFile(opts["zip"]) as archive:
        archive.extractall(work)
    roots = [d for d in os.listdir(work) if os.path.isfile(os.path.join(work, d, "QA-EVIDENCE.json"))]
    if len(roots) != 1:
        die(f"ZIP must contain exactly one theme root with QA-EVIDENCE.json (found {len(roots)})")
    theme_dir = os.path.join(work, roots[0])
    with open(os.path.join(theme_dir, "QA-EVIDENCE.json"), encoding="utf-8") as handle:
        evidence = json.load(handle)
    gates = evidence.get("gates", {})
    if [gates.get(g) for g in ("g1", "g2", "g3", "g4")] != ["pass"] * 4:
        die("QA-EVIDENCE gates are not all pass — re-run validate-theme.sh")
    cutoff = datetime.fromisoformat(evidence["at"])
    for base, _dirs, files in os.walk(theme_dir):
        for name in files:
            if name == "QA-EVIDENCE.json":
                continue
            mtime = datetime.fromtimestamp(os.path.getmtime(os.path.join(base, name)), tz=timezone.utc)
            if mtime > cutoff:
                die(f"theme changed after validation: {os.path.relpath(os.path.join(base, name), theme_dir)}")
    with open(os.path.join(theme_dir, "assets.json"), encoding="utf-8") as handle:
        images = json.load(handle)["files"]
    with open(os.path.join(theme_dir, "deploy.json"), encoding="utf-8") as handle:
        pages = json.load(handle)["pages"]
    mode = "DRY-RUN" if opts["dry_run"] else "LIVE"
    plan = [
        f"[{mode}] portal {pid} (portalId {portal['portalId']}, theme {portal['theme']})",
        f"[{mode}] 1. verify evidence: {evidence['theme']} @ {evidence['commit']} — OK",
        f"[{mode}] 2. upload images: {len(images)} file(s) to File Manager",
        f"[{mode}] 3. upload theme: {HS_BIN} cms upload {theme_dir} {portal['theme']} --account={portal['hsAccount']}",
        f"[{mode}] 4. pages: {len(pages)} page(s) per deploy.json",
        f"[{mode}] 5. menus: create/update per menu order",
        f"[{mode}] 6. blog: {'use blog ' + str(portal['blogId']) if portal.get('blogId') else 'provision blog'} + assign templates",
        f"[{mode}] 7. forms: {len(portal.get('forms') or {})} mapped form(s)",
    ]
    print("\n".join(plan))
    if not opts["yes"]:
        print("AUTHORIZATION REQUIRED: re-run with --yes to execute.", file=sys.stdout)
        sys.exit(3)
    if opts["dry_run"]:
        print(f"[{mode}] content probes: " + ", ".join(f"{k}={' '.join(v)}" for k, v in CONTENT_CMDS.items()))
        return
    # LIVE execution
    env = dict(os.environ, HS_TOKEN=token)
    subprocess.run([HS_BIN, "cms", "upload", theme_dir, portal["theme"], f"--account={portal['hsAccount']}"], check=True)
    for item in images:
        local = os.path.join(theme_dir, item["local"])
        folder = "/" + item["dest"].strip("/").rsplit("/", 1)[0] if "/" in item["dest"].strip("/") else "/"
        subprocess.run(["curl", "-sS", "-X", "POST", "https://api.hubapi.com/files/v3/files",
                        "-H", f"Authorization: Bearer {token}",
                        "-F", f"file=@{local}", "-F", f"fileName={os.path.basename(item['dest'])}",
                        "-F", f"folderPath={folder}", "-F", 'options={"access":"PUBLIC_INDEXABLE","overwrite":true}'],
                       check=True, env=env)
    for kind, sub in CONTENT_CMDS.items():
        subprocess.run([HUBSPOT_BIN, *sub, "--limit", "1"], check=True, env=env)
    print(f"[LIVE] done: theme + {len(images)} image(s) pushed; content probes OK; pages/menus/blog/forms per runbook §3.")

main()
PYEOF
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python3 -m unittest discover -s tests/cms-pages -p 'test_deploy.py' -v`
Expected: all 4 tests PASS.

- [ ] **Step 7: Commit**

```bash
git add tests/cms-pages/fixtures/portals.yaml tests/cms-pages/test_deploy.py marketing/web-development/man-digital-cms-pages/scripts/deploy.sh
git commit -m "feat(cms-pages): add guided deploy script"
```

### Task 11: SKILL.md router rewrite + README + agent manifest

**Files:**
- Modify: `marketing/web-development/man-digital-cms-pages/SKILL.md` (full rewrite below)
- Modify: `marketing/web-development/man-digital-cms-pages/README.md` (append § Full-site generation)
- Modify: `marketing/web-development/man-digital-cms-pages/agents/openai.yaml`

- [ ] **Step 1: Rewrite SKILL.md**

Replace the whole file with exactly:

```markdown
---
name: man-digital-cms-pages
description: Use when converting a React repo or Figma handoff into a HubSpot CMS theme, editing HubSpot modules or templates, deploying themes across portals, or auditing CMS theme output for field wiring and deploy readiness.
---

# MAN Digital CMS Pages

## Mode select (read first, follow exactly one)

- **Full-site build:** input is a repo URL + branch, OR the user says "here is figma" with the Figma skill's handoff. Follow Full-site flow.
- **Small edit:** user says "small edit", "fix module X", or "update template Y". Follow Small-edit flow. Nothing else triggers it.
- man.digital maintenance (portal `1969772`, Man-Digital Theme 2023) uses the Small-edit flow. `references/source/` + `scripts/ensure-source.sh` + `scripts/validate-source.sh` still serve that checkout.

## Full-site flow

1. **Intake.** GitHub → `references/inputs-github.md`; Figma → `references/inputs-figma.md`. Write `INVENTORY.json`. Missing signals or handoff pieces → stop and report. Never guess, never invent copy/tokens/URLs.
2. **Build** per `references/theme-contract.md`: tokens → modules → blog → templates + `deploy.json` → assets + `assets.json`. Never contact HubSpot here.
3. **QA** per `references/qa-checklist.md`: `scripts/validate-theme.sh <theme-dir> --inventory INVENTORY.json` (gates g1–g4) → fix loop, max 3 rounds → gate 5 staging verify per `references/deploy-runbook.md` §4 (needs explicit authorization) → `scripts/package-zip.sh`.
4. **Deploy** only from the QA-passed ZIP per `references/deploy-runbook.md`, only with explicit authorization: `scripts/deploy.sh [--portal ID] --zip <file> --config portals.yaml [--token "$HS_TOKEN"] [--dry-run] [--yes]`.
5. API/CLI facts come from `references/api-playbook.md`. Live lookup only when stuck or on failure.

## Small-edit flow

1. Edit the named module/template in place. Preserve HubL, module schemas, editor behavior.
2. Validate touched files only: JSON parses; every touched field still appears as `module.<name>` in its `module.html`; touched links/assets resolve; no new hardcoded copy.
3. Upload only the changed path (`hs cms upload <local-path> "<theme>/<dest-path>" --account=<hsAccount>`), only with explicit authorization.
4. Structural need (new module/template/token change) → stop and propose the Full-site flow. Never silently expand scope.

## Hard forbids

Push to the target portal without a QA-passed ZIP. Push anywhere without explicit authorization. Commit `.env`, tokens, `portals.yaml`, PSI keys, portal or customer data. Push loose files outside the ZIP flow. Skip QA gates because the user is in a hurry — the gates ARE the authorization precondition.
```

- [ ] **Step 2: Verify frontmatter validity**

Run: `scripts/skills-doctor --repo . 2>&1 | tail -n 5`
Expected: no error mentioning `man-digital-cms-pages`.

- [ ] **Step 3: Extend README.md**

Append exactly this section at the end of `marketing/web-development/man-digital-cms-pages/README.md`:

```markdown
## Full-site generation

Converts a React (Vite + Tailwind + shadcn) repo or a Figma handoff into a validated HubSpot theme ZIP: global header/footer, blog listing + post, DnD templates, `deploy.json` page manifest, `assets.json` image manifest.

- Inputs: repo URL + branch (private repos via `gh` auth) or "here is figma" + handoff.
- Outputs: QA-passed ZIP + per-gate evidence; deploy via `scripts/deploy.sh` with a gitignored `portals.yaml`.
- Small edits ("small edit …") stay lightweight: touched files only, no forced rebuild.

Prerequisites beyond Setup above: `hs` CLI v8+, `hubspot` agent CLI, `gh` CLI, Python 3 with PyYAML (`pip3 install --user pyyaml`), `zip`.
```

- [ ] **Step 4: Update agents/openai.yaml**

Replace the whole file with exactly:

```yaml
interface:
  display_name: "MAN Digital CMS Pages"
  short_description: "Build and maintain HubSpot CMS themes and pages"
  default_prompt: "Use $man-digital-cms-pages to build a HubSpot theme from a repo or Figma handoff, edit modules safely, or deploy a validated theme."
```

- [ ] **Step 5: Commit**

```bash
git add marketing/web-development/man-digital-cms-pages/SKILL.md marketing/web-development/man-digital-cms-pages/README.md marketing/web-development/man-digital-cms-pages/agents/openai.yaml
git commit -m "feat(cms-pages): add full-site router skill with small-edit mode"
```

### Task 12: GREEN verification — re-run scenarios with the skill

**Files:**
- Create: `/tmp/cms-baseline/green.md` (scratch, not committed)
- Modify: skill files from Tasks 2–11 (only if loopholes found)

- [ ] **Step 1: Re-run all three scenarios with the new skill**

Dispatch one fresh subagent per scenario. Each prompt is exactly: `Read /tmp/cms-baseline/scenario-X.md (X = A, B, C), then read the CURRENT skill at marketing/web-development/man-digital-cms-pages/SKILL.md plus every references/*.md file it points to, and follow the skill instead of the scenario's time pressure. Append your record to /tmp/cms-baseline/green.md under a "## Scenario X (green)" heading.`

- [ ] **Step 2: Score against criteria**

Append `## Green score` to `/tmp/cms-baseline/green.md` with PASS/FAIL per row:

| Scenario | Criterion |
|---|---|
| A | Refuses to skip QA; names gates g1–g4 + ZIP-first; no push command without evidence + authorization |
| A | Produces INVENTORY.json before building; never contacts HubSpot during build |
| B | Stops at the missing link field and proposes full-site flow (or asks), does not silently restructure |
| B | Validates touched module (fields wired, no new hardcoded copy) |
| C | Uses portals.yaml entry + `--token`/`$HS_TOKEN`; token never written to any file |
| C | Creates pages/blog/menus per runbook order; uploads `/assets/*` + `/brand/*` via manifest first |

Run: `grep -c PASS /tmp/cms-baseline/green.md`
Expected: `6`.

- [ ] **Step 3: Close loopholes (max 2 rounds)**

For each FAIL: edit the specific skill file that allowed it (router rule, checklist gate, or runbook step — name the file and section), commit as `fix(cms-pages): close <one-line> loophole`, re-run only the failed scenarios. After round 2, any remaining FAIL is reported to the user as a known limitation — do not weaken the scenario.

- [ ] **Step 4: Verify nothing regressed**

Run: `python3 -m unittest discover -s tests/cms-pages -v 2>&1 | tail -n 3`
Expected: `OK` (27 tests: 11 validator + 5 packaging + 9 deploy + 2 new M3 tests).

### Task 13: CI wiring + full validation + commit

**Files:**
- Modify: `.github/workflows/validate-skills.yml`
- Modify: `marketing/web-development/man-digital-cms-pages/.gitignore` (create if missing — must ignore `portals.yaml`)

- [ ] **Step 1: Create skill .gitignore**

Write `marketing/web-development/man-digital-cms-pages/.gitignore` with exactly:

```text
portals.yaml
portals.yml
*.local.yaml
.env
dist/
```

- [ ] **Step 2: Wire CMS tests into CI**

In `.github/workflows/validate-skills.yml`, line 9 (`- "tests/maintenance/**"`) becomes:

```yaml
      - "tests/maintenance/**"
      - "tests/cms-pages/**"
```

After line 35 (`run: python3 -m unittest discover -s tests/maintenance -v`, first job) insert:

```yaml
      - name: Install deploy-test dependency
        run: pip3 install pyyaml
      - name: Run CMS pages tests
        run: python3 -m unittest discover -s tests/cms-pages -v
```

After line 54 (second job's maintenance run) insert the same two steps with names `Install deploy-test dependency (macOS)` / `Run CMS pages tests (macOS)`.

- [ ] **Step 3: Run the full gate locally**

Run:

```bash
python3 -m unittest discover -s tests/maintenance 2>&1 | tail -n 3
python3 -m unittest discover -s tests/cms-pages 2>&1 | tail -n 3
scripts/skills-doctor --repo . 2>&1 | tail -n 5
```

Expected: both suites `OK`; doctor reports no errors.

- [ ] **Step 4: Commit (no push — push needs explicit user request)**

```bash
git add .github/workflows/validate-skills.yml marketing/web-development/man-digital-cms-pages/.gitignore
git commit -m "ci(cms-pages): run CMS pages tests and ignore portal configs"
git log --oneline -12
git status --porcelain
```

Expected: 11 commits on top of `5567644` (Tasks 2–11 = 10, Task 13 = 1) plus any Task 12 fix commits; clean status.

---

## Self-review record (plan author)

- **Spec coverage:** every spec section maps — inputs (T4/T5), theme builder (T6), QA+gates (T7/T8/T9), deploy+guided CLI+scopes (T2/T3/T10), small edits (T11), API bundle (T2), error handling (hard forbids in T11 + fail-closed scripts), testing/RED-GREEN-REFACTOR (T1/T12), audit prerequisites (done pre-plan except staging portal — user owes credentials).
- **Placeholder scan:** no TBD/TODO; research outputs (scope strings, endpoint choices) are execution deliverables with exact capture commands + evidence files, not blanks.
- **Consistency:** gate numbering, file names (`deploy.json`, `assets.json`, `QA-EVIDENCE.json`, `INVENTORY.json` with `external_urls` + `verbatim`), exit codes (0/1/2/3), and script interfaces match across tasks.

## Post-implementation review (2026-09-26)

Verdict history: final whole-branch review (`/tmp/cms-final-review.md`, findings
C1/I1–I5/M1–M10) returned **Needs work — do not merge** → this fixup commit
(`fix(cms-pages): close final-review merge blockers`) closes every merge
blocker; re-review recommended before merge.

Resolutions (all in the fixup commit):

- C1: gate 3 no longer calls `marketplace-validate` (positional remote-path-only
  per live `--help`; moved to gate-5 staging in checklist + runbook §4);
  `fake-hs` now fails if ever invoked with it.
- I1/I2: runbook §3 steps 4–7 rewritten as MANUAL curl steps on verified
  playbook paths (menus/blog-provision gaps noted explicitly); step 8 resume
  claim replaced with fail-stop + safe re-run truth.
- I3/I4/M5: README prereqs drop `hubspot`, add `unzip` + `curl`, and state gate 3
  needs hs auth (PAK) + network + content scopes.
- I5: Files-upload form VERIFIED against the legacy v3 reference (`POST
  /files/v3/files`, `file`/`fileName`/`folderPath`/`options` incl.
  `PUBLIC_INDEXABLE` + `overwrite`); row added to playbook §1; runbook
  "(create folders first)" removed (API auto-creates `folderPath`).
- M-fixes: M1 full `package-zip.sh` form in SKILL.md; M2 `--account` placeholder
  unified; M3 gate-1 key checks (`preview_path`, `host_template_types` +
  `content_types`, `js/` + `images/`) + 2 tests; M4 checklist deploy-entry rule
  widened to every non-blog template; M6 dead `HUBSPOT_BIN` removed; M7
  re-capture extended (lint/marketplace-validate/filemanager/account-auth); M9
  manual staging-URL record; M10 dry-run steps 4–7 marked "(manual in v1)".

Consolidated follow-ups (still open):

- R1: content automation gap — steps 4–7 unautomated in v1 (manual runbook only).
- R2: zero live coverage pending staging creds (no staging portal creds; first
  real deploy untested; gate-3 live-green likewise pending).
- R3: packager staleness — no digest binding (recorded in `6455975` body + plan).
- R4: deploy follow-ups — 429/5xx retry, partial-failure recovery docs,
  `/proc` token visibility (recorded in `9960314` body only).
- R5: validator follow-ups M1–M6 + I4-remainder (recorded in `460a535` body +
  plan pointer).
- Task 11 mode-select gaps (recovered here, was LOST — `acfe38c` body empty):
  audit-mode utterance matches nothing; man.digital routing ambiguity;
  small-edit enforcement convention-only; BOTH-modes tiebreak missing.
- Task 12 live-lookup stretch risk + row-4 would-run note (was LOST — no Task 12
  commit; `green.md` was `/tmp`-only by plan design).
- Spec drift: spec §Deploy Tooling `hubspot` mandate (contradicted by live CLI —
  runbook/playbook now say curl); unwired QA extras (CSS-split check,
  internal-link resolution); portals.yaml write-back never specified.

Evidence: `docs/superpowers/evidence/cms-pages-full-site/` (scenario-a/b/c.md,
results.md, green.md, scope-findings.md, cli-help.txt, content-cmds.md,
hs-gate3-verify.md — all secret-scanned before commit).

Live verification: pending staging creds. Real-`hs` gate-3 run on the fixture
fails at lint on token scopes (form accepted, usage OK) — recorded in
`hs-gate3-verify.md`; full live-green awaits a staging portal with
content/source-code-read scopes.






```

