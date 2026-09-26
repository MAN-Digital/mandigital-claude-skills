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

## Gate 3 — Validity

- Every `*.json` parses.
- `HS_BIN cms lint <theme-dir>` exits 0 (`HS_BIN` defaults to `hs`).
- Exactly one `dnd_area` per DnD template; sections well-formed.

## Gate 4 — Links + assets

- Every image `src` default in module `fields.json` files has an `assets.json` entry whose `local` file exists.
- Every `assets.json` entry is referenced by at least one default (no dead uploads).
- No `localhost`, `127.0.0.1`, `placehold.`, `lorempixel`, `example.com` strings anywhere.
- Every other external `http(s)` URL appears in `INVENTORY.json → external_urls` or the gate fails.

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
