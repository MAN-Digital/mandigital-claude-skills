---
name: man-digital-cms-pages
description: Use when converting a React repo or Figma handoff into a HubSpot CMS theme, creating or revising draft CMS pages through the API, configuring private-app credentials, editing HubSpot modules or templates, adding or updating portals.yaml entries, selecting a configured portal, deploying themes across portals, or auditing CMS theme output for field wiring and deploy readiness.
metadata:
  version: "1.1.0"
---

# MAN Digital CMS Pages

## Mode select (read first, follow exactly one)

- **Page content:** clone or edit a page, case study, listing, page-specific CSS, SEO, or structured data. Follow Page-content flow using the API; no theme upload is needed for page-field changes.

- **Portal configuration:** user asks to add/update a portal, change `portals.yaml`, or select an existing portal. Follow Portal-config flow. Configuration-only work does not trigger a site build or upload.

- **Full-site build:** input is a repo URL + branch, OR the user says "here is figma" with the Figma skill's handoff. Follow Full-site flow.
- **Small edit:** user says "small edit", "fix module X", or "update template Y". Follow Small-edit flow. Nothing else triggers it.
- man.digital module/template maintenance uses the Small-edit flow; page content uses Page-content flow. Its existing checkout is served by `references/source/`, `scripts/ensure-source.sh`, and `scripts/validate-source.sh`; this checkout is specific to man.digital and must not be used as another portal's source. Resolve the target portal and theme from the existing configuration below.

## Portal configuration (all modes)

- Use the existing gitignored `portals.yaml` (or the user's explicitly supplied `--config` path) as the source of truth for `portalId`, `hsAccount`, `theme`, `staging`, `blogId`, `domain`, `forms`, `tokenEnv`, optional `tokenFile` for page-content API credentials, and optional `formsProvision`. Preserve existing entries and values except those the user requests to change; never replace it with `portals.yaml.example` during a skill update.
- Keep the portal selected in the current task. Resolve `--portal <id>` against the config entry's `id`; do not infer a target from example values, the local source checkout, or the CLI's default account. If the task has no selected portal and the target is ambiguous, ask before any remote operation. A missing entry is a configuration gap, never permission to fall back to another portal.
- Derive every remote theme path and `--account=<hsAccount>` from that same selected entry. Gate 5 uses the entry marked `staging: true`; this does not change the task's selected deployment target. Select the lint account explicitly with `HS_ACCOUNT` as documented in the QA checklist.
- For Page-content flow, use only the selected entry’s explicit `tokenFile` (created by `cms-token.py`) or its configured `tokenEnv`; verify portal and scope before writes. Do not fall back to a different credential if the selected source fails. `tokenFile` is a path, never a token.
- For existing deployment/form scripts, preserve per-portal credential resolution: explicit `--token` → the entry's `tokenEnv` → `HS_TOKEN` → hidden prompt. A configured-but-unset `tokenEnv` fails closed instead of falling back. Never print or commit secrets.
- Config selection is not deployment authorization. Follow the applicable flow's QA and explicit authorization requirements.

## Portal-config flow

1. Read `references/portal-config-maintenance.md` and the existing config. Resolve the default `portals.yaml` relative to this skill's real directory, not the shell's working directory. Honor an explicit config path.
2. For “use portal `<id>`”, resolve the existing entry and retain that selection for the task; do not rewrite config or invent a persisted default. For additions/edits, apply only the requested changes. The user's request authorizes the local config edit; no extra confirmation is needed. Ask only for missing required values or an ambiguous target.
3. Validate the proposed YAML locally using the maintenance checklist before replacing the existing file. Preserve unrelated entries, settings, comments, and file permissions. Never store credentials in YAML.
4. Report the changed entry and field names, validation results, and any remaining gaps without dumping the config. A config edit does not authorize HubSpot writes, provisioning, theme migration, or deployment. No ZIP or theme QA is required for a config-only edit.

## Page-content flow

1. Read `references/page-content-api.md` and resolve the selected portal. Prefer direct API/CLI for structured page edits. Use the browser for visual review and UI-only features, not as a response to a missing API credential.
2. Preflight private-app portal identity and `content` scope. The CLI PAK may read pages without permission to edit them. If the credential is missing, provide the README hidden-input setup command; continue preparing copy and payloads locally while the user supplies it.
3. Inventory pages and snapshot the current draft and published response. Reuse the existing draft when one exists. Preserve the requested template, rich-text HTML wrappers, unrelated modules, and existing listing cards. For case studies, lead with the customer's transcript; use spreadsheet metrics as supporting evidence. Keep direct quotes exact and distinguish measured outcomes, qualitative benefits, and future plans.
4. Prepare sparse payloads. Edit existing pages only through `PATCH /cms/v3/pages/site-pages/{id}/draft`. Never use the ordinary page PATCH for draft work: it can change a live page immediately. Re-read before writing to catch concurrent edits. A draft request authorizes draft writes; it does not authorize publication.
5. Read back saved fields. Compare live content before/after. Check headline, title, description, canonical, OG image, assets, internal links, visible FAQ/schema parity, and existing theme-generated schema to avoid duplicates. Keep video `preload="none"`, a poster, and explicit aspect ratio; do not autoplay.
6. Review desktop and narrow mobile previews. Check video placement, contrast, metric cards, wrapping, overflow, and spacing. Scope page CSS to the relevant module wrapper. Report measured performance only when actually measured; draft preview access and third-party scripts can affect results.
7. Report draft editor/preview links and remaining verification limits. Do not publish, push-live, or change publication state unless the user explicitly requests it.

## Full-site flow

1. **Intake.** GitHub → `references/inputs-github.md`; Figma → `references/inputs-figma.md`. Write `INVENTORY.json`. Missing signals or handoff pieces → stop and report. Never guess, never invent copy/tokens/URLs.
2. **Build** per `references/theme-contract.md`: tokens → modules → blog → templates + `deploy.json` → assets + `assets.json`. Never contact HubSpot here.
3. **QA** per `references/qa-checklist.md`: `scripts/validate-theme.sh <theme-dir> --inventory INVENTORY.json` (gates g1–g4) → fix loop, max 3 rounds → `scripts/verify-blog.sh <theme-dir> [--portal ID --config portals.yaml]` for the blog templates (local + upload + assignment state) → gate 5 staging verify per `references/deploy-runbook.md` §4 (needs explicit authorization) → `scripts/package-zip.sh <theme-dir> <out-dir>`.
4. **Deploy** only from the QA-passed ZIP per `references/deploy-runbook.md`, only with explicit authorization: `scripts/deploy.sh [--portal ID] --zip <file> --config portals.yaml [--token "$HS_TOKEN"] [--dry-run] [--yes]`.
5. API/CLI facts come from `references/api-playbook.md`. Live lookup only when stuck or on failure.

## Small-edit flow

1. Resolve the selected portal entry and the matching source checkout, then edit the named module/template in place. Preserve HubL, module schemas, editor behavior.
2. Validate touched files only: JSON parses; every touched field still appears as `module.<name>` in its `module.html`; touched links/assets resolve; no new hardcoded copy.
3. Upload only the validated changed path (`hs cms upload <local-path> "<theme>/<dest-path>" --account=<hsAccount>`), using `theme` and `hsAccount` from the selected config entry, only with explicit authorization. This scoped Small-edit upload is the sole exception to the full-site ZIP requirement.
4. Structural need (new module/template/token change) → stop and propose the Full-site flow. Never silently expand scope.

## Hard forbids

Deploy a full site without a QA-passed ZIP. Push anywhere without explicit authorization. Commit `.env`, tokens, `portals.yaml`, PSI keys, portal or customer data. Push loose files except for validated, explicitly authorized Small-edit uploads. Reset existing portal configuration, silently switch portals, or rely on the CLI default account. Skip the applicable flow's QA requirements because the user is in a hurry — QA is an authorization precondition.
