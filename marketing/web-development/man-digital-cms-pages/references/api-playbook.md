# HubSpot API/CLI Playbook (bundled)

Runtime uses this file. Live lookup only when stuck or on failure.

## 1. CLI surfaces

Verified against live `--help` of `hs` 8.9.1 and `hubspot` 0.13.0. Re-capture
with this exact command:

```
{ hs cms --help; echo '=====HUBSPOT====='; hubspot --help; echo '=====UPLOAD====='; hs cms upload --help; echo '=====PREVIEW====='; hs cms theme preview --help; echo '=====LINT====='; hs cms lint --help; echo '=====MARKETPLACE-VALIDATE====='; hs cms theme marketplace-validate --help; echo '=====FILEMANAGER====='; hs filemanager --help; echo '=====ACCOUNT-AUTH====='; hs account auth --help; } > cli-help.txt 2>&1
```

- `hs` (developer CLI, PAK auth): `cms upload [src] [dest] --account=<name>`,
  `cms lint <path>`, `cms theme marketplace-validate <path>`,
  `cms theme preview --src=<path> --account=<name>`, `account auth` per-portal
  onboarding, `filemanager upload <src> <dest>`, `api <endpoint>` passthrough
  (`-X`, `--data`) for any PAK-supported REST endpoint. `cms upload` also takes
  `--cms-publish-mode <draft|publish>`.
- `hubspot` (agent CLI, OAuth/service-key auth): CRM-only — `objects`,
  `pipelines`, `properties`, `workflows`, `auth`, `whoami`, etc. It has NO
  `cms`, `marketing`, or `api` subcommands and NO `--account`/`--token` flags
  (auth is `hubspot auth login` or `HUBSPOT_ACCESS_TOKEN`). NOT used for CMS
  deploy; see the [Agent CLI guide](https://developers.hubspot.com/docs/developer-tooling/local-development/agent-cli/guide).
- Raw API (private-app token, `Authorization: Bearer <token>` from `$HS_TOKEN`)
  covers everything neither CLI does: pages/blog publish, menus, forms read,
  and blog provisioning edge cases.

### Content-operation endpoints

All paths verified against the method+path on the linked doc page.

| Op | Method + path | Purpose | Doc |
|---|---|---|---|
| List site pages | `GET /cms/v3/pages/site-pages` | Page inventory before deploy | https://developers.hubspot.com/docs/api-reference/legacy/cms/pages/website-pages/get-website-pages |
| Create site page | `POST /cms/v3/pages/site-pages` | Create page from templatePath | https://developers.hubspot.com/docs/api-reference/legacy/cms/pages/website-pages/create-website-page |
| Update site page | `PATCH /cms/v3/pages/site-pages/{objectId}` | Sparse-update page by ID | https://developers.hubspot.com/docs/api-reference/legacy/cms/pages/website-pages/update-website-page |
| List blog posts | `GET /cms/v3/blogs/posts` | Post inventory before deploy | https://developers.hubspot.com/docs/api-reference/legacy/cms/blogs/posts/get-posts |
| Create blog post | `POST /cms/v3/blogs/posts` | Create post with content body | https://developers.hubspot.com/docs/api-reference/legacy/cms/blogs/posts/create-post |
| List forms | `GET /marketing/v3/forms` | Form inventory for mapping | https://developers.hubspot.com/docs/api-reference/legacy/marketing/forms/get-forms |
| Read form | `GET /marketing/v3/forms/{formId}` | Get form definition by ID | https://developers.hubspot.com/docs/api-reference/legacy/marketing/forms/get-form |
| Create form | `POST /marketing/v3/forms` | Create form; 201 + `id` on success; scope `forms`; create-forms.sh sends the full `HubSpotFormDefinitionCreateRequest` (archived, configuration, createdAt/updatedAt, displayOptions, fieldGroups, formType `hubspot`, legalConsentOptions, name) | https://developers.hubspot.com/docs/api-reference/legacy/marketing/forms/create-form |
| Replace form | `PUT /marketing/v3/forms/{formId}` | Replace ALL fields of a form definition; scope `forms` (create-forms.sh `--update`) | https://developers.hubspot.com/docs/api-reference/legacy/marketing/forms/update-form |
| Get blog details | `GET /cms/v3/blog-settings/settings/{blogId}` | Retrieve blog by ID | https://developers.hubspot.com/docs/api-reference/legacy/cms/blogs/blog-settings/get-blog |
| Provision blog | UNVERIFIED — no create-blog endpoint in the reference | Create blog if missing | https://developers.hubspot.com/docs/api-reference/legacy/cms/blogs/blog-settings/guide |
| List/create menus | UNVERIFIED — no public menus REST API in the reference | Navigation menu wiring | https://developers.hubspot.com/docs/cms/start-building/building-blocks/modules/menus-and-navigation |
| Upload image | `POST /files/v3/files` | multipart `file` + `fileName` + `folderPath` (auto-created if missing) + `options={"access":"PUBLIC_INDEXABLE","overwrite":true}` | https://developers.hubspot.com/docs/api-reference/legacy/files/files/upload-file |

## 2. Scopes and credentials

| Need | Scope string | Credential | Doc |
|---|---|---|---|
| CMS pages/blog read+write+publish | `content` (sites, landing pages, email, blog, campaigns; needs CMS/Marketing Hub Pro/Enterprise) | PAK for `hs` file ops; private-app token for REST (pages/blog APIs) | https://developers.hubspot.com/docs/apps/legacy-apps/authentication/scopes |
| File Manager upload | `files` (`files.ui_hidden.read` also accepted) | PAK (`hs filemanager upload`) or token (Files API) | https://developers.hubspot.com/docs/api-reference/latest/files/guide |
| Forms read/create/map | `forms` | Private-app token (REST; `hs`/`hubspot` have no forms surface) | https://developers.hubspot.com/docs/apps/legacy-apps/authentication/scopes |
| Account info read | None for primary paths: `hs account info` (PAK, verified live) or `POST /oauth/v2/private-apps/get/access-token-info` (token self-describes, no scope needed); raw `GET /account-info/2026-09/details` needs `oauth` — docs only note `oauth` is "added by default to all public apps" and don't confirm private-app token coverage, so it may 403 | PAK + token | https://developers.hubspot.com/docs/api-reference/latest/account/account-information/guide |

Onboarding: obtain the PAK from `app.hubspot.com/l/personal-access-key` first,
then run `hs account auth` and paste the key when prompted; the key is stored
in `~/.hscli/config.yml`.
Per-directory override via `hs account link` / `.hsaccount`.
CLI config filename may be `~/.hscli/config.yml` or `hubspot.config.yml`
depending on version (per live `hs auth --help`).
([PAK doc](https://developers.hubspot.com/docs/developer-tooling/local-development/hubspot-cli/personal-access-key),
[private apps](https://developers.hubspot.com/docs/apps/legacy-apps/private-apps/overview))

Rule: `hs` file ops use the portal's PAK account (`--account=<name>`); direct API
content ops use the private-app token passed at runtime via environment (deploy
scripts must accept it from env, e.g. `$HS_TOKEN`). Never store either in the repo.

## 3. Rate limits and retries

Private-app limits (burst per app, daily shared per account):
Free/Starter 100 req/10s + 250,000/day; Professional 190/10s + 625,000/day;
Enterprise 190/10s + 1,000,000/day.
Over-limit calls get HTTP 429 with `errorType: RATE_LIMIT` and `policyName`
`DAILY` or secondly (`TEN_SECONDLY_ROLLING`); daily resets at midnight account TZ.
Every response carries `X-HubSpot-RateLimit-Max/-Remaining/-Interval-Milliseconds`
(+ `-Daily`/`-Daily-Remaining`) headers. `Retry-After` is sent on 429s per API
(e.g. webhooks journal guide) — honor it when present, else back off.
([usage guidelines](https://developers.hubspot.com/docs/developer-tooling/platform/usage-guidelines))

Deploy uploads files sequentially; on 429 wait the `Retry-After` header (or back
off when absent), max 3 waits, then stop with evidence.

## 4. Refresh procedure

Re-check each §2 doc URL when a deploy fails with 401/403/404-on-valid-path.
Re-run the §1 --help capture on any `hs`/`hubspot` minor upgrade; re-check
§2 URLs on 429-behavior change. Update this file and commit.
