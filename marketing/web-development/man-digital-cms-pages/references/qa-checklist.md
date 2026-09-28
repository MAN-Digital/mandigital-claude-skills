# QA Checklist (blocking gates)

Run in order. Any failure → fix → restart at gate 1. Max 3 fix rounds, then report with evidence.

## Gate 1 — Completeness

- `theme.json`, root `fields.json`, `deploy.json`, `assets.json` exist.
- `css/fonts.css`, `css/variables.css`, `css/common.css`, `css/custom.css` exist.
- Every `deploy.json` entry's `templatePath` exists; every non-blog template (anything except `templateType: blog_listing`/`blog_post`, including untyped ones) has exactly one entry; exactly one homepage. `blog_listing`/`blog_post` templates must exist but are assigned via blog provisioning, not `deploy.json`.
- Every `dnd_module`/`{% module %}` path in every template resolves to a `modules/*.module/` dir.
- Header, footer, blog listing + post modules/templates present.

## Gate 2 — Field wiring

- For each module: every top-level `fields.json` name (plus one nested level for groups) appears as `module.<name>` (or `.<child>` inside its group loop) in `module.html`. No orphans.
- No hardcoded marketer-editable copy: grep `module.html` for raw text outside HubL tags fails the gate unless the string is in the inventory's `verbatim` list (default empty).
- Standard verbatim starter set for menu-fallback/nav punctuation: Hjem, Våre, kurs, Nyheter, Kontakt, Tilgjengelighetserklæring, ·, |, (, ), : — extend per project.
- Header/footer may use `menu()` with designed hardcoded fallback links (approved pattern, see theme-contract §3); list the fallback strings in `verbatim`.
- A module whose `fields.json` has a form-type field MUST contain a native `{% form %}` tag; custom-JS submit declares `data-hsforms-ignore` (passes with WARN, not fail).
- Every `<img>` whose src carries a `{{ }}` expression must sit inside an `{% if %}` guard (line-based heuristic: guard within the 5 preceding lines or earlier on the same line).
- No HubSpot-reserved field name (S9): `body`, `label`, `type`, `name`, `id`, `class`, `style`, `children`, `default`, `parent`, `module` — top-level or group children alike (HubSpot rejects them at upload).
- Every group/repeater `default` row key matches a defined child field name (S10) — stale keys upload as null fields.
- Every field `type` is in the verified allowlist (S11): `text`, `richtext`, `number`, `boolean`, `choice`, `image`, `url`, `link`, `color`, `font`, `menu`, `form`, `group`, `blog`. Notably `textarea` is NOT valid — use `richtext` for body copy.

## Gate 3 — Validity

- Every `*.json` parses.
- `HS_BIN cms lint <theme-dir>` exits 0 with no reported issues (`HS_BIN` defaults to `hs`; the gate fails on error output even when the exit code is 0). Lint needs an hs account with source-code-read or content-editor-access; set `HS_ACCOUNT=<hsAccount>` (staging, never prod for routine runs).
- Exactly one `dnd_area` per DnD template; sections well-formed.

## Gate 4 — Links + assets

- Every image `src` default in module `fields.json` files has an `assets.json` entry whose `local` file exists. `src` matching tolerates HubSpot-emitted spacing (`"src" : "..."`).
- Live themes reference File Manager files by absolute `https://<portal>.fs1.hubspotusercontent-<region>.net/hubfs/<portal><dest>` URL (site-relative FM paths 404). The gate normalizes trusted-host hubfs URLs back to the manifest dest (S12); lookalike hosts earn no exemption.
- No `[...]`-bracket placeholder text in any `fields.json` default string value (parsed-value scan — structural JSON brackets never match).
- Every `assets.json` entry is referenced by at least one default (no dead uploads).
- No `localhost`, `127.0.0.1`, `placehold.`, `lorempixel`, `example.com` strings anywhere.
- Every other external `http(s)` URL appears in `INVENTORY.json → external_urls` or the gate fails. Manifested-file hubfs URLs are first-party and need no allowlisting.

## Gate 5 — Editor compatibility (staging-verified)

- `hs cms upload <theme-dir> <staging-theme> --account=<staging-hsAccount>` then `hs cms theme marketplace-validate <staging-theme-path> --account=<staging-hsAccount>` (`<staging-theme-path>` is the path to the theme within the Design Manager per `hs cms theme marketplace-validate --help` — see deploy-runbook §4, needs authorization).
- `hs cms theme preview --src=<theme-dir> --account=<staging-hsAccount>`; open preview: every module renders and edits without code. Record preview URL in evidence.

## Gate 6 — Package

- `scripts/package-zip.sh <theme-dir> <out-dir>` produces `<theme>-<yyyymmdd>-<input-sha>.zip` containing the theme root incl. `QA-EVIDENCE.json`.

## Evidence format

`validate-theme.sh` writes `<theme-dir>/QA-EVIDENCE.json`:

```json
{"theme": "<name>", "commit": "<input-sha>", "at": "<iso8601>", "gates": {"g1": "pass", "g2": "pass", "g3": "pass", "g4": "pass"}, "staging": {"url": null, "at": null}}
```

`staging` (`url` + `at`): record the staging URL + timestamp manually after the gate-5 run. `deploy.sh` requires all four local gates `pass` and evidence newer than every theme file.
