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
