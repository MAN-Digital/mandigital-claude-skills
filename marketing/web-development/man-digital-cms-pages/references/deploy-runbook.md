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

Fields: `id` (deploy.sh selector), `portalId`, `hsAccount` (`hs` account name, PAK-based, onboarded via `hs account auth`), `theme` (destination theme folder), `staging` (exactly one `true`), `blogId` (HubSpot blog id or null to provision), `domain`, `forms` (module-name → HubSpot form GUID map), `tokenEnv` (optional: name of the env var holding THIS portal's private-app token — e.g. `HS_TOKEN_EXTEK`; absent = shared `HS_TOKEN`/prompt, old behavior), `formsProvision` (optional: `{enabled, spec, prefix}` — form auto-provisioning, see "Form provisioning" below; absent = manual forms, old behavior). The private-app token is NEVER in this file — the entry only names its env var.

Token precedence per run: `--token` flag → `tokenEnv` var → `HS_TOKEN` → hidden prompt (live) / placeholder (dry-run). When switching portals, give each entry its own `tokenEnv` var (`HS_TOKEN_EXTEK`, `HS_TOKEN_ACME`, …) and export each secret in your shell (`export HS_TOKEN_EXTEK='pat-…'` — add to `~/.zshrc` to persist). Fail-closed: a configured-but-unset `tokenEnv` stops the run instead of silently using another portal's token.

## 2. Guided deploy (default)

```bash
scripts/deploy.sh --portal prod --zip dist/my-theme-20260926-abc1234.zip --config portals.yaml --token "$HS_TOKEN"
```

Without `--portal`, deploy.sh lists entries and prompts. Without `--token` and no configured token source (`tokenEnv` var or `HS_TOKEN`), it prompts (input hidden) and never echoes; an empty `--token` is treated as unset and falls through the same chain. `--dry-run` prints every action without executing. `--yes` is required for real execution; without it the script stops after the plan summary. Exit codes: 0 ok, 1 failed check, 2 usage/config, 3 authorization required.

## 3. What deploy executes, in order

1. Verify `<theme>/QA-EVIDENCE.json`: all local gates `pass`, evidence newer than every theme file.
2. Upload images: each `assets.json` entry → File Manager destination (`folderPath` folders are auto-created by the upload call).
2b. Provision forms — ONLY when the portal entry sets `formsProvision.enabled: true`: run `scripts/create-forms.sh --portal <id> --config portals.yaml --token <resolved-token>` (spec + prefix come from the portal entry; deploy.sh passes its own resolved token so parent and child always use the same credential), which creates each form-spec form via `POST /marketing/v3/forms`, skipping names that already exist. The fail-closed unmapped-module check counts spec-covered modules as satisfied. Without the flag this step does not exist and step 7 stays fully manual. Trade-off: the resolved token travels via the child's argv (transiently `ps`-visible to other local users) so the child cannot re-resolve a different portal's token — correctness over argv secrecy; API calls themselves still use 0600 header files.
3. Upload theme: `hs cms upload <unzipped-theme> <theme> --account=<hsAccount>`.

**Steps 4–7 are MANUAL in v1** (deploy.sh plans them in dry-run but does not execute them; its `[LIVE] done` message says so explicitly). Run each by hand with the private-app token (`Authorization: Bearer $HS_TOKEN`, base `https://api.hubapi.com`), using the verified paths from `references/api-playbook.md` §1:

4. Create/update pages per `deploy.json`. Inventory first: `GET /cms/v3/pages/site-pages`; then per page: `POST /cms/v3/pages/site-pages` (new) or `PATCH /cms/v3/pages/site-pages/{objectId}` (existing, sparse update). Match `deploy.json` `templatePath`/`slug` to the page's template and slug fields.
5. Create/update menus per menu order. Gap: the playbook §1 row is UNVERIFIED — no public menus REST API exists in the reference, so there is no curl step; build the menu order by hand in HubSpot (Settings → Website → Navigation, or the menu editor) following the `deploy.json` `menuOrder` values.
6. Provision blog if `blogId` null, assign listing/post templates. First run `scripts/verify-blog.sh <theme-dir> [--portal <id> --config portals.yaml]` — it proves both templates exist locally with the right `templateType`, confirms they are uploaded, and reports the blog's current assignment. Gap: the playbook §1 provision row is UNVERIFIED — no create-blog endpoint in the reference, so provision the blog by hand in HubSpot when `blogId` is null. Assignment is UI-only too (blog-settings PUT/PATCH return 405, verified 2026-09-28): Marketing → Website → Blog → `<blog>` → Settings → Templates → set "Blog listing pages" to `<theme>/templates/blog_listing.html` and "Blog posts" to `<theme>/templates/blog_post.html`; record the `blogId` in `portals.yaml` and re-run verify-blog to confirm `ASSIGNED`.
7. Apply `forms` map to form modules; fail closed on unmapped form modules. Inventory: `GET /marketing/v3/forms`; verify each mapped GUID: `GET /marketing/v3/forms/{formId}`. Any form module without a `portals.yaml` `forms` entry stops the deploy — add the mapping, never skip.
8. Print per-item results. Any failure stops the run with a redacted error; fix the cause and re-run (theme upload + image upload both overwrite safely).

## Renaming a live theme folder

When the Design Manager path itself is wrong (wrong brand, past-agency watermark — extek went `transjt_projects/tj-extek` → `extek-theme` 2026-09-28):

1. Upload the QA-passed theme to the NEW path: `hs cms upload <theme-dir> <new-theme> --account=<hsAccount>`.
2. Prove parity: `hs cms list <old>/templates` vs `hs cms list <new>/templates` must diff empty (same for `modules/` on big renames). Delete anything the raw upload carried that deploy.sh staging would have stripped (e.g. `QA-EVIDENCE.json`).
3. Re-inventory pages: `GET /cms/v3/pages/site-pages`. Never trust cached page IDs — the list is the truth (see playbook §1).
4. Per page: `PATCH /cms/v3/pages/site-pages/{id}` `{"templatePath": "<new>/templates/<tpl>"}`. The PATCH applies immediately — live pages stay `PUBLISHED`; a following push-live 404s with nothing staged, which is success, not an error.
5. Curl every live URL: 200 + content renders. Confirm form embeds (GUIDs) survived.
6. Delete the old folder (`hs cms delete <old> --account=...`) plus any emptied watermarked parents. Leave DRAFT pages pointing at the old path for the user to delete or rewire — never delete user content unasked.
7. Update the portal entry's `theme:` in `portals.yaml`; re-run `verify-blog.sh --portal` (blog assignment paths changed → re-assign both templates in UI per step 6).

## Form provisioning

When the theme has form modules and the portal entry enables `formsProvision`, forms are created by API instead of by hand. Standalone use (same flags deploy.sh uses, plus overrides):

```bash
scripts/create-forms.sh --portal staging --config portals.yaml --token "$HS_TOKEN" \
  [--spec forms/staging.json] [--prefix "[staging] "] [--update] [--dry-run] [--out guids.json]
```

`--spec`/`--prefix` default to the portal entry's `formsProvision` values. Idempotent by HubSpot form name (prefix + spec name): lookup via `GET /marketing/v3/forms` first, `SKIP` existing names, `CREATED`/`UPDATED` (`--update` replaces via `PUT /marketing/v3/forms/{formId}`) otherwise. Every form prints a `FORM_GUID <module>=<guid>` line — paste those lines into the portal entry's `forms:` map so later deploys (and the fail-closed check) resolve without the spec. `--dry-run` validates the spec locally and prints the plan; it never touches the network. `--out` writes the module→GUID map as JSON for theme wiring.

### Form-spec format

JSON, `{"forms": [...]}`. One entry per form module:

```json
{
  "forms": [
    {
      "module": "contact_form",
      "name": "Contact",
      "fields": [
        {"name": "firstname", "label": "First name", "type": "text", "required": true},
        {"name": "email", "label": "Business email", "type": "email", "required": true,
         "blockFreeEmail": true},
        {"name": "phone", "label": "Phone", "type": "phone", "required": false},
        {"name": "message", "label": "Message", "type": "textarea", "required": true},
        {"name": "company_size", "label": "Company size", "type": "select",
         "options": [{"label": "1-10", "value": "1-10"}]},
        {"name": "newsletter_opt_in", "label": "Email me news", "type": "consent",
         "subscriptionTypeId": 12345}
      ],
      "consent": {"mode": "implicit", "privacyText": "We process your data per our privacy policy."},
      "submitText": "Send",
      "redirectUrl": "/thank-you",
      "recaptcha": true,
      "language": "en"
    }
  ]
}
```

Rules: `module` (theme module dir minus `.module`) and `name` (HubSpot display name, idempotency key after prefix) are required. Field `name` is the contact-property internal name (`firstname`, `email`, `phone`, …), `label` the visible label, `type` one of `text`/`email`/`phone`/`textarea`/`select`/`checkbox`/`consent`. `select` requires `options` (`[{label, value}]`, HubSpot option values); `consent` requires `subscriptionTypeId` (the portal's subscription-type id — look it up in the portal, it differs per portal) and a form-level `consent` object with API-required `privacyText`. Consent `mode`: `none` (default without consent fields), `implicit`, or `explicit` (GDPR variants; both need `privacyText`, explicit additionally accepts `consentToProcessText`/`consentToProcessCheckboxLabel`/`consentToProcessFooterText`). Only one of `redirectUrl`/`thankYouText`. Script display defaults (button color, theme, phone digit bounds) are cosmetic fallbacks — adjust in the form editor when the design demands it.

### Mapping from design fields

Translate each Figma/design input row in order: single-line inputs → `text` (use the matching contact property: `firstname`, `lastname`, `company`, `jobtitle`); email inputs → `email` (+ `blockFreeEmail` when the design says business-email-only); phone/tel inputs → `phone`; multi-line/message inputs → `textarea`; dropdowns/radios → `select` with the design's option list verbatim as `{label, value}` pairs; standalone tick boxes (non-legal, e.g. "book a callback") → `checkbox`; legal/GDPR tick boxes → `consent` (+ `subscriptionTypeId`, + form-level `consent` object). The design's submit-button copy → `submitText`; the post-submit destination → `redirectUrl` (or `thankYouText` for an inline message). Anything the API cannot express (custom inline error copy, per BUILD-NOTES precedent) stays a form-editor pass — never invent API fields for it.

### Manual fallback (when API create fails)

If `create-forms.sh` fails (auth, validation, or HubSpot-side error), the deploy stops before the theme upload — but forms created before the failure persist in the portal. Either re-run (creation is idempotent by name: existing forms `SKIP`, only missing ones are created) or fall back by hand: create each remaining form in HubSpot (Marketing → Forms) from the same spec values, copy each new form's GUID into the portal entry's `forms:` map (`<module>: "<guid>"`), then re-run deploy.sh. The fail-closed check passes on the pasted GUIDs with provisioning disabled or enabled; leaving provisioning enabled re-invokes the API (harmless — existing names skip).

## 4. Gate-5 staging verification

```bash
hs cms upload <theme-dir> <staging-theme> --account=<staging-hsAccount>
hs cms theme marketplace-validate <staging-theme-path> --account=<staging-hsAccount>
hs cms theme preview --src=<theme-dir> --account=<staging-hsAccount>
```

`<staging-theme-path>` is the path to the theme within the Design Manager (positional, per `hs cms theme marketplace-validate --help`); it must point at the just-uploaded staging theme.

Open the preview URL, confirm every module renders and edits without code, then proceed to package + prod deploy. Staging upload needs the same explicit authorization as prod.

Local gate-3 lint needs the same kind of account: an hs account with source-code-read or content-editor-access. Set `HS_ACCOUNT=<hsAccount>` (staging, never prod for routine runs) and `validate-theme.sh` passes it as `--account` to `hs cms lint`.

## 5. Smoke test (recommended for new portals)

Fetch `/`, one section page, blog listing, one post, contact page. Confirm 200, nav renders, one form submits to a test endpoint. Record results next to the QA evidence.

## File Manager verification

Local gate-4 proves every image default is manifested and every manifest file exists locally — it cannot prove the files exist in the portal's File Manager (a theme can pass g1–g4 with 10/10 images 404, as the 2026-09-27 portal audit found). Close that gap after upload, before go-live:

```bash
scripts/verify-fm.sh <theme-dir> --portal <id> --config portals.yaml
```

Read-only: fetch-probes each `assets.json` `dest` via `hs filemanager fetch <dest> <tmpfile> --account=<hsAccount>`, prints per-file `OK`/`MISSING`, exits 0 iff all exist. Record the run with the gate-5 evidence; any `MISSING` line blocks go-live — re-run the deploy.sh image-upload step, never ship broken images.

## Multilingual guidance

Per-locale page values must be **text/richtext/choice** fields — the only `module_attribute`-overridable kinds used here. (`textarea` is not a valid HubSpot *module* field type — S11 rejects it, use `richtext`; the form-*spec* `textarea` in the provisioning section above is a separate namespace mapping to the Forms API `multi_line_text` and is unaffected.) Grouped, link, and image content stays single-locale default plus an editor pass (this shapes field design: crumbs, language links, and CTAs use text hrefs rather than link/image pickers). Validated on the 2026-09-26 dry-run (see `docs/superpowers/evidence/cms-pages-full-site/2026-09-26-dryrun.md`, SB-9).

## Forms per locale (limitation)

v1 maps ONE form GUID per module (`portals.yaml` `forms:` is module-name → GUID). Bilingual themes reuse one form across locales or re-map per deployment — there is no per-locale dimension in the schema. A locale dimension is a tracked follow-up, not implemented here (see dry-run evidence, SB-4).
