# HubSpot API/CLI Playbook (bundled)

Runtime uses this file. Live lookup only when stuck or on failure.

## 1. CLI surfaces

Verified against live `--help` of `hs` 8.9.1 and `hubspot` 0.13.0 (capture:
`/tmp/cms-baseline/cli-help.txt`).

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
- Raw API (private-app Bearer token) covers everything neither CLI does: pages/blog
  publish, menus, forms read, and blog provisioning edge cases.

## 2. Scopes and credentials

| Need | Scope string | Credential | Doc |
|---|---|---|---|
| CMS pages/blog read+write+publish | `content` (sites, landing pages, email, blog, campaigns; needs CMS/Marketing Hub Pro/Enterprise) | PAK for `hs` file ops; private-app token for REST (pages/blog APIs) | https://developers.hubspot.com/docs/apps/legacy-apps/authentication/scopes |
| File Manager upload | `files` (`files.ui_hidden.read` also accepted) | PAK (`hs filemanager upload`) or token (Files API) | https://developers.hubspot.com/docs/api-reference/latest/files/guide |
| Forms read/map | `forms` | Private-app token (REST; `hs`/`hubspot` have no forms surface) | https://developers.hubspot.com/docs/apps/legacy-apps/authentication/scopes |
| Account info read | `oauth` (raw `GET /account-info/2026-09/details`); `hs account info` needs no API scope; token self-describes via `POST /oauth/v2/private-apps/get/access-token-info` | PAK + token | https://developers.hubspot.com/docs/api-reference/latest/account/account-information/guide |

Onboarding: run `hs account auth`, paste the portal's PAK when prompted (get it via
the terminal prompts, `app.hubspot.com/l/personal-access-key`, or Development >
Keys > Personal Access Key); the key is stored in `~/.hscli/config.yml`.
Per-directory override via `hs account link` / `.hsaccount`.
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
Update this file and commit.
