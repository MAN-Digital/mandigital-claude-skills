---
name: man-digital-revenue-leaders-interviews
description: Create, update, and validate MAN Digital Revenue Leaders Interview blog posts in HubSpot from approved Figma designs and reviewed interview copy. Use for this interview series; do not use for ordinary MAN Digital blog posts or the interview landing-page theme.
---

# MAN Digital Revenue Leaders Interviews

Build each interview as a HubSpot blog post, not as a new theme. Preserve the existing blog chrome and keep all interview-specific markup and CSS scoped to `.rli-intro` and `.rli-article`.

## Route the work

- Read [references/figma-and-design-contract.md](references/figma-and-design-contract.md) before changing layout, typography, responsive behavior, questions, callouts, or guest treatments.
- Read [references/editorial-seo-and-hubspot.md](references/editorial-seo-and-hubspot.md) before writing answers, changing metadata, creating tags/campaigns, or touching HubSpot.
- Use `assets/carol-chen/` as the tested implementation example. It is a draft demonstration, not publishable interview copy.
- Pair with `$man-digital-design-system` for brand decisions and `$man-digital-cms-pages` for source validation or CMS uploads.

## Required outcome

1. Inspect the approved Figma desktop and mobile frames and the current HubSpot blog template before editing.
2. Reuse the Carol structure: intro, lead image, the notice required by the current editorial state, context blocks, one Q/A section per approved question, pull quote, takeaways, guest card, and LinkedIn action. Record the approved Figma source and exact ordered questions in metadata so the validator can reject wording or order drift.
3. Put post-specific CSS in the individual post Head HTML when shared theme CSS is not proven to load on the blog template. Scope it and wrap it with stable start/end markers so it can be replaced safely.
4. Configure the metadata contract: SEO title, meta description, matching Open Graph title/description, approved Open Graph image, exact series tag, and exact series campaign. Campaign attachment is an automatic mandatory step for every interview run, not an optional handoff suggestion.
5. Run `python3 scripts/validate_interview.py <interview-asset-directory>` and the CMS source validator when source files changed. When the validator or editorial contract changes, also run `python3 scripts/test_validate_interview.py`.
6. Manually check the actual HubSpot preview at desktop, tablet, and mobile widths, using native Chrome when it is available. Verify question count/order, LinkedIn icon/link, image loading, typography, table of contents, no overflow, persisted metadata/campaign values, and draft status.

## Hard gates

- Never present illustrative answers, automatic captions, or an unreviewed transcript as the guest's words. Sample copy uses `draft-sample-answers` plus the visible sample notice. Transcript-reviewed copy still awaiting approval uses `draft-transcript-reviewed` plus a visible pending-approval notice. Only guest-approved copy may use the `approved` state, and every answer and pull quote must use the matching state.
- Do not invent guest biography, company facts, employment history, metrics, LinkedIn URLs, or quotes. Leave a labeled draft placeholder when a fact is unverified.
- Keep the approved Figma question wording and order. Do not paraphrase questions for style.
- Use a real LinkedIn SVG or accessible inline SVG; no text glyph or missing icon. External links use `target="_blank"`, `rel="noopener noreferrer"`, and an accessible label.
- Keep the exact tag and campaign name `Revenue Leaders Interviews`. Search before creating either to avoid duplicates.
- For every Revenue Leaders Interview draft, automatically associate the canonical `Revenue Leaders Interviews` campaign before handoff and treat the run as incomplete until the saved association has been reopened and verified. If the canonical campaign ID is missing or no longer resolves, stop and request explicit authorization before creating a replacement; then update the canonical ID in the skill instead of silently accepting a new ID or name variant.
- Draft save, campaign association, scheduling, and publishing are separate states. Never publish or schedule without explicit authorization for that action.
- Report these statuses separately: local validation, HubSpot draft save, SEO/Open Graph save, tag/campaign association, responsive preview QA, and publication state.

## Carol example

The bundled Carol assets document the known-good structure and draft-safety pattern:

- `assets/carol-chen/interview-intro.html`
- `assets/carol-chen/interview-body.html`
- `assets/carol-chen/interview-post.css`
- `assets/carol-chen/metadata.example.json`
- `assets/carol-chen/linkedin-icon.svg`

Copy the structure, replace guest-specific content and assets, preserve the safeguards, and validate the new directory before applying it to HubSpot.
