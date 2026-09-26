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
