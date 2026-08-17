---
name: man-digital-cms-pages
description: Maintain and validate MAN Digital's HubSpot CMS sources for www.man.digital, including the Man-Digital Theme 2023, custom modules, templates, and the RevOps Service page. Use when inspecting, changing, deploying, or verifying MAN Digital HubSpot CMS files, or when working on HubSpot page performance and PageSpeed findings tied to this theme.
---

# MAN Digital CMS Pages

Resolve the canonical source checkout with `scripts/ensure-source.sh`. It uses
`references/source/` by default and honors `MAN_DIGITAL_CMS_SOURCE` when a checkout
already exists elsewhere. Treat HubSpot Design Manager in portal `1969772` as the live
source of truth and the checkout as the versioned source, rollback record, and operational
knowledge base.

## Workflow

1. Run `source_dir=$(scripts/ensure-source.sh)`. The helper clones the canonical source when missing, fetches it when present, fast-forwards only a clean tracked branch, and preserves dirty worktrees.
2. Read `$source_dir/README.md` and the smallest relevant source files. For RevOps Service work, also read `$source_dir/pages/revops-service/BUILD-NOTES.md` and edit section sources rather than only the assembled page file.
3. Preserve existing HubL, module schemas, and editor behavior. Never commit `.env` files, personal access keys, PSI keys, portal data, or customer data.
4. Run `scripts/validate-source.sh "$source_dir"` before any upload or commit.
5. Upload only the explicitly changed path with `hs cms upload <local-path> "Man-Digital Theme 2023/<dest-path>" --account=1969772`. Do not upload or publish without explicit user authorization.
6. After an authorized upload, wait for a new prerender and verify the rendered page. Identical uploads and changes to included CSS may not trigger a rerender; use an intentional render bump only when necessary and authorized.

## Performance and PSI work

Read `$source_dir/docs/theme-perf-log.md` and the relevant `$source_dir/docs/psi-*.txt`
snapshots before changing the critical path. Also load `$auditing-web-vitals` for
measurement discipline and diagnosis.

- Measure mobile and desktop separately.
- Use five-run medians for release decisions.
- Wait at least ten minutes after deployment before settled PSI measurements.
- Do not treat rapid, byte-identical PSI responses as independent samples.
- Keep above-the-fold requirements in `$source_dir/theme/templates/layouts/base.html` inline blocks rather than only in asynchronously loaded overrides.
- Preserve cascade order and HubSpot rerender behavior when consolidating or inlining CSS.

## Local validation

Run from the skill directory:

```bash
source_dir=$(scripts/ensure-source.sh)
scripts/validate-source.sh "$source_dir"
```

The validator confirms the checkout is a Git worktree, verifies required theme and RevOps structures, parses every JSON configuration file, and detects unresolved merge markers. It does not contact HubSpot, deploy files, or claim that a live page is correct.
