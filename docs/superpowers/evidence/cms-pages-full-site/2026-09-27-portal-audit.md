# Portal-audit fix round 2 — evidence (2026-09-27)

Source audit: `/tmp/portal-extek/AUDIT.md` (portal 50344783, reads via `--account=extek`; read-only throughout).
Branch: `fix/cms-portal-audit` (from `main`, post-dryfix). Commit: `fix(cms-pages): close portal-audit gaps S1-S8` (single commit, not pushed).
Skill dir: `marketing/web-development/man-digital-cms-pages/`.

## Per-item verdicts (from AUDIT.md)

- Images: VERIFIED broken — installed theme 0/10 uploaded, 10/10 default srcs 404; `/assets`, `/brand`, `/extek` all 404; FM root holds only 2 unrelated PNGs. Our dry-run dests equally absent pre-deploy (expected — deploy upload is load-bearing).
- Blog: VERIFIED genuine — installed listing is DnD with `blog_selection` + manual fallback cards; post is static with `group` guard, crumbs, topic pills. Ours: `contents`-based listing, unguarded post.
- Forms: VERIFIED broken-by-default — installed has `type: form` fields but NO `{% form %}` tag anywhere; custom `tj-forms.js` submit with null `form_id` default refuses to submit. Ours renders natively.
- Featured image: VERIFIED — installed covers more cases (`or` chain in listing/news cards, guarded post image). Ours listing is summary-only (adopted, see S5 + theme patch 1).
- Header/nav: PARTIAL — installed `menu()`+fallback is real but editor-dependent (field unset); ours is manual-only. Neither is live today; installed shape is the better long-term pattern (approved, see S3).
- Module quality: VERIFIED good wiring, weak packaging — 17/17 installed modules zero orphans; expected g1 fail (non-skill theme); shimmed g1/g2 pass; `hs cms lint` 0 issues; real g4 verdict FAIL (no assets at all); ships `[...]` placeholders; `tj-forms.js` render-blocking in `<head>`.
- File Manager: VERIFIED — no referenced dir exists. Nothing uploaded for either theme.

## S1–S8 resolutions

- S1 [HIGH, fixed] `scripts/validate-theme.sh` gate-4 src regex is now `"src"\s*:\s*"(/[^\"]+)"` (was strict `"src":`, which missed HubSpot-emitted `"src" : "`). Tests: spaced src + manifest entry → PASS; spaced src unmanifested → FAIL g4 naming it.
- S2 [HIGH, fixed] NEW executable `scripts/verify-fm.sh <theme-dir> --portal <id> --config portals.yaml [--token T]`: reads `assets.json` dests, read-only probes each via `hs filemanager fetch <dest> <tmpfile> --account=<hsAccount>` (`HS_BIN` seam), prints per-file `OK`/`MISSING`, exit 0 iff all exist. `--token` accepted for deploy.sh CLI symmetry but unused (hs CLI uses account auth). Runbook gained `## File Manager verification` (when: after upload, before go-live; part of gate-5 evidence). CLI semantics verified against the live portal read-only: missing path → rc=1 "no such file or folder"; present file → rc=0. Tests: `tests/cms-pages/test_verify_fm.py` (3 tests; fake-hs extended with `FAKE_FM_MISSING`).
- S3 [MED, fixed] `qa-checklist.md` gate-2: standard verbatim starter set (Hjem, Våre, kurs, Nyheter, Kontakt, Tilgjengelighetserklæring, ·, |, (, ), : — extend per project) + `menu()`-with-designed-fallback approval (link target: new `theme-contract.md` §3 SHOULD bullet).
- S4 [MED, fixed] Chosen home: **gate-2** (module wiring). A module with a form-type field MUST contain `{% form …%}`; `data-hsforms-ignore` passes with stderr `WARN: <module> uses custom form submit (not native {% form %})` instead of failing. Contract §3 form-module bullet extended with the mandate. Tests: native tag → PASS; neither → FAIL g2 naming module + "form field without {% form %} tag"; escape hatch → PASS + WARN. (`test_deploy.py` form-module helper updated to build a valid `{% form %}` module.)
- S5 [LOW, fixed] `theme-contract.md` §3 blog bullets: `post_list_summary_featured_image or featured_image` chain mandated in listing cards; `contents` (auto) vs `blog_recent_posts(blog_selection)` (editor-picked + mandatory fallback cards) trade-off documented; topic_list vs tag_list RESOLVED: **`content.tag_list` is current, `content.topic_list` is a legacy alias for older implementations** ([HubL variables](https://developers.hubspot.com/docs/cms/reference/hubl/variables), "Blog variables" note). Ours was already correct; installed uses the still-functional legacy alias.
- S6 [LOW, fixed] Gate-4 addition: parsed-JSON walk over every `fields.json` `default` (top-level + group children), testing only string VALUES against `\[[^\[\]]{1,60}\]` (structural brackets never match). Hit → FAIL g4 naming file + value truncated to 80 chars. Tests: `"PDF, [size]"` → FAIL g4; clean default → PASS.
- S7 [LOW, confirm only] No change. Recorded: gate-3 lint genuinely needs a source-code-read account, and lint-clean ≠ working (installed theme lints 0 issues with 10/10 images 404 and broken forms).
- S8 [LOW, fixed] Gate-2 addition, documented in code as a LINE-BASED HEURISTIC: each `<img>` whose src attribute contains `{{` must have `{% if` in the 5 preceding lines or earlier on the same line (same-line inclusion is a deliberate pragmatic choice — minified modules guard inline as `{% if x %}<img …>`, which preceding-only would falsely fail). Else FAIL g2 naming module + line number. Tests: guarded → PASS; `<img src="{{ x.src }}">` unguarded → FAIL g2.

## Theme patches (`/tmp/cms-dryrun/theme` ONLY — not repo, NOT repackaged)

1. `blog_listing.module/module.html` L3: summary-image test AND src now use `content.post_list_summary_featured_image or content.featured_image` (mirrors installed L17). Judgment call: the brief said "test" only, but test-without-src would render `<img src="">` exactly when the fallback triggers — wet-test quality required both.
2. `blog_post.module/module.html`: post reads (L5 h1, L6 meta, L7 featured image, L8 body, L9 tags) wrapped in `{% if group %}` … `{% endif %}`; chrome (back link) untouched; render identical when `group` present; `{% if %}`/`{% endif %}` balanced 4/4.

## Gate re-runs (patched theme, pristine `/tmp/cms-dryrun/INVENTORY.json`)

- OLD validator (`main`, `/tmp/validate-old.sh`) + fake-hs: **PASS g1–g4** — both patches gate-neutral; SB-1 dryfix confirmed (pristine inventory green).
- NEW validator + fake-hs: **FAIL g2** `unguarded img with dynamic src in footer.module/module.html:4` — first of exactly 3 pre-existing S8 hits (`footer.module:4`, `header.module:5`, `hero.module:3` logo/hero imgs; none from the patches).
- NEW validator on guarded scratch copy (`/tmp/cms-patched-copy`, diagnosis only): g1–g3 pass, **FAIL g4** S6 `placeholder '[...]' in default '[CompEx Ex01–Ex04]' (calendar_band.module/fields.json)`; 44 S6 hits total in 9 modules (calendar_band 17, course_cards 9, course_detail 9, news_section 3, prose_section 2, calendar_simple/footer/hero/testimonial 1 each) — all pre-existing content debt, must be cleared before wet-test go-live.
- Real `hs cms lint /tmp/cms-dryrun/theme --account=extek`: **0 issues found** (rc=0).

## Validation counts

- `tests/cms-pages`: 46 tests OK (12 new: 9 validator S1/S4/S6/S8 + 3 `test_verify_fm.py`).
- `tests/maintenance`: 19 tests OK (`shell_count` 9→10 for the new `verify-fm.sh`).
- `scripts/skills-doctor` (full): PASS — 41 skills, 44 Python files, 10 shell files, 48 links, 3 managed skills.
