---
name: man-digital-revenue-leaders-interviews
description: Create, update, and validate MAN Digital Revenue Leaders Interview blog posts in HubSpot from YouTube videos, Granola calls, Markdown transcripts, or reviewed copy. Use for this interview series; do not use for ordinary MAN Digital blog posts or the interview landing-page theme.
---

# MAN Digital Revenue Leaders Interviews

Build each interview as a HubSpot blog post, not as a new theme. Preserve the existing blog chrome and keep all interview-specific markup and CSS scoped to `.rli-intro` and `.rli-article`.

## Route the work

- Read [references/figma-and-design-contract.md](references/figma-and-design-contract.md) before changing layout, typography, responsive behavior, questions, callouts, or guest treatments.
- Read [references/source-ingestion-and-drafting.md](references/source-ingestion-and-drafting.md) when the post starts from a YouTube URL, Granola call/export, Markdown file, or transcript pasted in the prompt.
- Read [references/editorial-seo-and-hubspot.md](references/editorial-seo-and-hubspot.md) before writing answers, changing metadata, creating tags/campaigns, or touching HubSpot.
- Use `assets/carol-chen/` as the tested implementation example. It is a draft demonstration, not publishable interview copy.
- Pair with `$man-digital-design-system` for brand decisions and `$man-digital-cms-pages` for source validation or CMS uploads.

## Required outcome

1. Normalize the supplied source. Run `python3 scripts/ingest_interview_source.py <source> --output <working-directory>` for public YouTube or local Markdown. Use `--source-type granola` for a copied Granola transcript or Markdown export. Resolve every `PROMPT_REQUIRED` field with the user; never fabricate missing guest assets or profile details.
2. Inspect the approved Figma desktop and mobile frames and the current HubSpot blog template before editing.
3. Create an internal evidence map from every approved question to source timestamps or source passages. Draft the full post only from that evidence; a source-derived draft remains visibly unapproved until reviewed.
4. Reuse the Carol structure: intro, lead image, optional privacy-enhanced YouTube embed, the notice required by the current editorial state, context blocks, one Q/A section per approved question, pull quote, takeaways, guest card, and LinkedIn action. Record the approved Figma source and exact ordered questions in metadata so the validator can reject wording or order drift.
5. Put post-specific CSS in the individual post Head HTML when shared theme CSS is not proven to load on the blog template. Scope it and wrap it with stable start/end markers so it can be replaced safely.
6. Generate the SEO title and meta description from the completed draft. Match Open Graph title/description to them; use the user-provided approved image or the YouTube thumbnail as a clearly identified draft candidate. Configure the exact series tag and campaign. Campaign attachment is an automatic mandatory step for every interview run, not an optional handoff suggestion.
7. Run `python3 scripts/validate_interview.py <interview-asset-directory>` and the CMS source validator when source files changed. When ingestion or validation changes, also run `python3 scripts/test_ingest_interview_source.py` and `python3 scripts/test_validate_interview.py`.
8. Manually check the actual HubSpot preview at desktop, tablet, and mobile widths, using native Chrome when it is available. Verify question count/order, video embed when enabled, LinkedIn icon/link, image loading, typography, table of contents, no overflow, rendered Open Graph fields, persisted tag/campaign values, and draft status.

## Hard gates

- Never present illustrative answers, automatic captions, Granola notes, or an unreviewed transcript as approved guest words. A machine-created first pass uses `draft-source-derived` with `source-derived` answers/quotes and a visible source notice. Sample copy uses `draft-sample-answers`; human-checked transcript copy awaiting approval uses `draft-transcript-reviewed`. Only guest-approved copy may use `approved`.
- Keep raw YouTube/Granola/Markdown source files and the evidence map out of the published article. Treat private Granola content as private input; do not send it to an unrelated external service or expose its share URL.
- Do not invent guest biography, company facts, employment history, metrics, LinkedIn URLs, or quotes. Leave a labeled draft placeholder when a fact is unverified.
- Keep the approved Figma question wording and order. Do not paraphrase questions for style.
- Use a real LinkedIn SVG or accessible inline SVG; no text glyph or missing icon. External links use `target="_blank"`, `rel="noopener noreferrer"`, and an accessible label.
- Keep the exact tag and campaign name `Revenue Leaders Interviews`. Search before creating either to avoid duplicates.
- For every Revenue Leaders Interview draft, automatically associate the canonical `Revenue Leaders Interviews` campaign before handoff and treat the run as incomplete until the saved association has been reopened and verified. If the canonical campaign ID is missing or no longer resolves, stop and request explicit authorization before creating a replacement; then update the canonical ID in the skill instead of silently accepting a new ID or name variant.
- Draft save, campaign association, scheduling, and publishing are separate states. Never publish or schedule without explicit authorization for that action.
- Report these statuses separately: source ingestion/completeness, editorial state, local validation, HubSpot draft save, SEO/Open Graph save, tag/campaign association, responsive preview QA, and publication state.

## Carol example

The bundled Carol assets document the known-good structure and draft-safety pattern:

- `assets/carol-chen/interview-intro.html`
- `assets/carol-chen/interview-body.html`
- `assets/carol-chen/interview-post.css`
- `assets/carol-chen/metadata.example.json`
- `assets/carol-chen/linkedin-icon.svg`

Copy the structure, replace guest-specific content and assets, preserve the safeguards, and validate the new directory before applying it to HubSpot.
