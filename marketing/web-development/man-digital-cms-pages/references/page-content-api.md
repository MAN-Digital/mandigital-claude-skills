# Page-content API workflow

Use this flow for cloning pages and editing draft content, layout module fields,
SEO, or page-specific CSS. A theme upload is unnecessary when only page fields change.

## Credentials

Resolve the intended portal from `portals.yaml`. Never infer it from the CLI default.
Use the selected entry's explicit `tokenFile` or `tokenEnv`; do not silently switch
credentials on failure. The optional `tokenFile` is for this flow only. Existing
deploy/form scripts retain their documented environment credential resolution.

For file-based credentials:

```bash
python3 scripts/cms-token.py setup --portal-id <selected-portalId>
python3 scripts/cms-token.py check --portal-id <selected-portalId>
```

`setup` requires a real terminal, hides input, validates the account and scope, and
writes `~/.config/man-digital/hubspot/<portalId>.json` with mode 600. No token goes
in argv, shell history, repository files, or tool output. See the README for obtaining
and rotating the token. The helper supports `setup` and `check`; it does not edit pages.

For a local Python API script, import the helper using `importlib.util` and use
`load_token(selected_portal_id)`, `verify(token, selected_portal_id)`, and
`request(token, path, method, body)`. These functions keep credentials in memory;
never print their token arguments or the credential file. The helper only accepts
API paths on `https://api.hubapi.com`, rejects redirects, and redacts error bodies.
For an explicitly selected environment credential, read it in-process with
`os.environ[configured_token_env]` and call the same `verify` function before writes.

The private-app verification request is
`POST /oauth/v2/private-apps/get/access-token-info`, JSON `{"tokenKey": token}`.
Check `hubId` equals the selected portal and `scopes` includes `content`.
A 401/403 is an authentication/scope problem, not a reason to repeat writes or use
UI editing. Prepare the payload while the user supplies a suitable credential.

## Draft mutations

1. Read the inventory (`GET /cms/v3/pages/site-pages`) and resolve page IDs. Reuse an
   existing task draft. Read `/site-pages/{id}/draft` and `/site-pages/{id}` into local
   snapshots outside the skill repository. Record `updatedAt` and relevant fields.
2. Clone only when needed: `POST /cms/v3/pages/site-pages/clone` with `id` and
   `cloneName`. Confirm the returned page remains unpublished. Avoid duplicate clones.
3. Build a sparse payload from the fresh draft. Module groups may be nested in
   dictionaries and lists; preserve all unrelated nodes, IDs, rich-text HTML, CTA
   URLs, and listing cards. Do not send response-only metadata or publication fields.
4. Immediately re-read the draft. If its `updatedAt` or edited fields changed,
   reconcile the new state before proceeding. This is a conflict check, not an
   atomic compare-and-swap guarantee; minimize the interval before the write.
5. Send **`PATCH /cms/v3/pages/site-pages/{id}/draft`**. Do not use the ordinary
   page PATCH, `/push-live`, `/schedule`, or publication-state mutations for draft work.
6. Read back and compare each intended field. Compare published content fields with
   the live snapshot. A successful HTTP response alone does not prove the intended
   copy or layout was saved. For a timeout, read back before retrying the mutation.
7. If a rollback is necessary, restore only the fields changed by this task through
   the draft endpoint after checking for newer edits. Never overwrite a newer draft
   blindly with a complete old snapshot.

## Content and design checks

- Client transcripts lead the narrative. Spreadsheet implementation details support
  the story. Quote verbatim; do not invent financial savings or turn a deadline
  constraint into a measured delivery duration. Label future work as future work.
- Preserve the established template and editor module fields. Do not replace the
  whole page with raw HTML unless specifically requested. Remove stale cloned
  client names from visible and hidden fields relevant to the new story.
- Put the video close to the introduction on desktop and mobile. Use a poster,
  `preload="none"`, `playsinline`, controls, and a fixed aspect ratio; no autoplay.
- Scope CSS to actual module wrapper IDs/classes observed in rendered output or
  module source. Check text against its background, including rich-text children;
  mobile metrics need readable labels, sensible wrapping, and no horizontal overflow.
- Match visible FAQs with FAQPage answers. Inspect the theme's existing JSON-LD:
  link to existing Article/WebPage/Organization IDs instead of duplicating them.
  Include accurate VideoObject metadata and OG image. Do not promise rich results.
- Verify desktop and narrow mobile previews, links, media playback, and page settings.
  Use performance measurements if available; report quota/preview limitations rather
  than claiming an unmeasured PSI score.
- Save draft/editor links and QA evidence. Publishing needs explicit user instruction.
