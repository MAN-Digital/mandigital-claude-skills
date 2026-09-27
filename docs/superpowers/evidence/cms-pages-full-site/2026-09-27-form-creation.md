# Form-creation scope — evidence (2026-09-27)

Branch: `fix/cms-portal-audit`. Single commit, not pushed.
Skill dir: `marketing/web-development/man-digital-cms-pages/` (canonical — see Scope verification).

## Status

Implemented: `scripts/create-forms.sh` (new, executable) provisions HubSpot forms from a
form-spec JSON via Forms API v3, idempotent by name (lookup → SKIP, or `--update` to
replace); `scripts/deploy.sh` runs it as plan step 2b before the theme upload, gated by the
new per-portal `formsProvision` config block; runbook documents spec format, design-field
mapping, and manual fallback; api-playbook §1 gained Create/Replace form rows.

## Scope verification

- Canonical-tree check: `git ls-files | grep -i -E 'cms-pages|form|portal'` shows the skill
  ONLY under `marketing/web-development/man-digital-cms-pages/`; `ls skills/` → no such
  directory. All work went into the committed location; no `skills/man-digital-cms-pages/`
  path was created or touched.
- Shared-lib check: `deploy.sh` / `verify-fm.sh` are self-contained bash + embedded-python
  (`exec python3 -`) with NO shared lib file — so `create-forms.sh` follows that same
  convention. The two `forms_provision()` validators (deploy.sh, create-forms.sh) are
  intentionally mirrored, each carrying a keep-in-sync note.
- Forms API grounding: no `form-research-codex` file exists anywhere in the committed tree
  (verified via `git ls-files` + `find`), so payload shapes were taken from the public
  reference, fetched 2026-09-27: `POST /marketing/v3/forms` (scope `forms`, 201 + `id`),
  full `HubSpotFormDefinitionCreateRequest` required keys, per-field required keys
  (incl. `objectTypeId "0-1"` CONTACT, email `validation.useDefaultBlockList`, phone
  `useCountryCodeSelect` + digit bounds, dropdown `options` + `defaultValues`), consent
  oneOf variants (explicit/implicit both require `communicationsCheckboxes`,
  `privacyText`, `type`), `postSubmitAction` (`redirect_url`/`thank_you`), and replace via
  `PUT /marketing/v3/forms/{formId}` ("Update all fields", operationId `..._replace`).
  Display constants (theme `default`, style colors, phone 7–20 digits) are script defaults
  documented as cosmetic fallbacks in the runbook. No live portal calls were made (fakes only).

## Verification

Exact CLI outputs (2026-09-27):

```
$ python3 -m unittest discover -s tests/cms-pages
Ran 65 tests in 25.385s
OK
$ python3 -m unittest discover -s tests/maintenance
Ran 19 tests in 8.723s
OK
$ ./scripts/skills-doctor
PASS: 41 skills, 44 Python files, 11 shell files, 48 links, 3 managed skills
```

Claimed-vs-actual: 65 cms-pages tests (46 pre-existing + 14 `test_create_forms.py` + 5
deploy-provisioning integration) — actual 65 OK. 19 maintenance (incl. `shell_count`
10→11) — actual 19 OK. skills-doctor full PASS.

Coverage of the brief: spec validation errors (unknown type, select-without-options,
consent-without-subscriptionTypeId, consent-fields-without-consent-object — all exit 2
with zero network); idempotency skip path (GET hit → SKIP, no POST/PUT); GUID capture
(`FORM_GUID` lines + `--out` JSON); deploy.sh 2b dry-run/live/disabled/malformed/missing-spec
paths; portals schema accepts (absent block = old behavior, all pre-existing tests
unmodified-green) and rejects (non-mapping block, missing spec).

## Concerns

Pre-existing doc disagreements found (all recorded, none blocking — no STOP triggered):

1. `marketing/web-development/man-digital-cms-pages/references/source/pages/webinars/BUILD-NOTES.md:7`
   cites `form-spec-webinar-registration.md` ("Form spec: ...", also "spec §3" at :122),
   but that file does not exist in `references/source/pages/webinars/` (only `build.py`,
   `BUILD-NOTES.md`, `template-*.html`). Stale path — continued silently; the new
   form-spec JSON format is defined fresh in `references/deploy-runbook.md` ("Form
   provisioning"), informed by the BUILD-NOTES field evidence (:43–:50: 5 fields,
   `useDefaultBlockList`, GDPR consent, submit text, redirect, recaptcha).
2. The brief's `form-research-codex` doc is absent from `docs/` (only `docs/superpowers/`
   evidence/plans/specs exist). Absence, not contradiction — grounded on the live public
   API reference instead (URLs in api-playbook §1).
3. `docs/superpowers/evidence/cms-pages-full-site/content-cmds.md:3` lists a forms fallback
   path `/marketing/v3/forms/forms` (doubled `/forms`), disagreeing with the playbook's
   verified `GET /marketing/v3/forms`. Pre-existing, out of scope, left untouched;
   create-forms.sh uses the playbook path.
