# Scope findings — Task 2, Step 2 (2026-09-26)

Live CLI versions probed: `hs` 8.9.1, `hubspot` 0.13.0 (build 1076).
Full `--help` capture: `/tmp/cms-baseline/cli-help.txt` (173 lines).

## Q1 — Private-app scope string for CMS pages/blog

**Answer: `content`.**
Official scopes table: "`content` | This includes sites, landing pages, email, blog,
and campaigns. | CMS API and Calendar, Email and Email Events endpoints |
CMS Hub Professional or Enterprise, or Marketing Hub Professional or Enterprise".
URL: https://developers.hubspot.com/docs/apps/legacy-apps/authentication/scopes

## Q2 — Scope string for File Manager upload

**Answer: `files`.**
Official scopes table: "`files` | This includes access to File Manager. |
Files (File Manager) and file mapper endpoints | Any account".
Files API guide "Required Scopes: `files`, `files.ui_hidden.read`".
URLs:
- https://developers.hubspot.com/docs/apps/legacy-apps/authentication/scopes
- https://developers.hubspot.com/docs/api-reference/latest/files/guide

## Q3 — Scope string for forms read

**Answer: `forms`.**
Official scopes table: "`forms` | This includes access to the Forms endpoints. |
Forms endpoints | Any account".
URL: https://developers.hubspot.com/docs/apps/legacy-apps/authentication/scopes

## Q4 — Which operations require PAK vs private-app token

- `hs` (developer CLI) authenticates with a **Personal Access Key** per account
  (`hs account auth` stores it in `~/.hscli/config.yml`). PAK scopes are chosen at
  key creation and capped by the user's HubSpot permissions.
  URL: https://developers.hubspot.com/docs/developer-tooling/local-development/hubspot-cli/personal-access-key
- **Private-app access token** is a Bearer token for direct API calls
  (`Authorization: Bearer [TOKEN]`); scopes configured on the app's Scopes tab;
  requires super admin to create. Token self-describes via
  `POST /oauth/v2/private-apps/get/access-token-info` (returns Hub ID + scopes).
  URL: https://developers.hubspot.com/docs/apps/legacy-apps/private-apps/overview
- Operational split for this project: all `hs` file/CMS ops use the portal's PAK
  account (`--account=<name>`); direct REST calls (pages publish, forms read, menus)
  use the private-app token passed at runtime via environment, never stored in repo.
- `hubspot` agent CLI v0.13.0 is CRM-only (no cms/marketing/api subcommands —
  verified live `--help` + guide "directly interact with CRM data"); auth is
  `hubspot auth login` (OAuth) or service key via `HUBSPOT_ACCESS_TOKEN`.
  URL: https://developers.hubspot.com/docs/developer-tooling/local-development/agent-cli/guide

## Q5 — `hs account auth` onboarding flow per portal

Run `hs account auth` → terminal prompts for the portal's PAK → key is saved to the
global config `~/.hscli/config.yml`. Obtain the PAK via the terminal prompts, the
direct link (app.hubspot.com/l/personal-access-key), or Development > Keys >
Personal Access Key. Per-directory override via `hs account link` / `.hsaccount`.
URL: https://developers.hubspot.com/docs/developer-tooling/local-development/hubspot-cli/personal-access-key

## Account-info read (playbook §2 row 4)

- Raw API: `GET /account-info/2026-09/details` requires scope **`oauth`**.
  URL: https://developers.hubspot.com/docs/api-reference/latest/account/account-information/guide
- Scopes table notes `oauth` is "added by default to all public apps"; the docs do
  not state private-app token coverage of `oauth`, so the operational paths are:
  `hs account info` (PAK, verified live) and the token-info endpoint above (token,
  no scope needed).

## Rate limits (playbook §3)

Private apps (burst per app, daily shared per account):
Free/Starter 100/10s + 250K/day; Pro 190/10s + 625K/day; Enterprise 190/10s + 1M/day.
429 body: `errorType: RATE_LIMIT`, `policyName` DAILY vs secondly
(TEN_SECONDLY_ROLLING); daily resets midnight account TZ; headers
`X-HubSpot-RateLimit-*`. `Retry-After` on 429 is documented per-API (e.g. webhooks
journal guide), not promised globally on the usage page.
URLs:
- https://developers.hubspot.com/docs/developer-tooling/platform/usage-guidelines
- https://developers.hubspot.com/docs/api-reference/latest/webhooks-journal/guide (Retry-After example)
