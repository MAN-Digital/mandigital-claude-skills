---
name: man-digital-revenue-leaders-interviews
description: Create, update, and validate MAN Digital Revenue Leaders Interview blog posts in HubSpot from YouTube videos, Granola calls, Markdown transcripts, or reviewed copy. Use for this interview series; do not use for ordinary MAN Digital blog posts or the interview landing-page theme.
---

# MAN Digital Revenue Leaders Interviews

Build each interview as a HubSpot blog post, not as a new theme. Preserve the existing blog chrome and keep all interview-specific markup and CSS scoped to `.rli-intro` and `.rli-article`.

## Route the work

- Read [references/figma-and-design-contract.md](references/figma-and-design-contract.md) before changing layout, typography, responsive behavior, callouts, video, or guest treatments.
- Read [references/source-ingestion-and-drafting.md](references/source-ingestion-and-drafting.md) when the post starts from a YouTube URL, Granola call/export, Markdown file, or transcript pasted in the prompt.
- Read [references/linkedin-identity-verification.md](references/linkedin-identity-verification.md) before accepting, rendering, or changing a guest LinkedIn URL.
- Read [references/editorial-seo-and-hubspot.md](references/editorial-seo-and-hubspot.md) before writing answers, changing metadata, creating tags/campaigns, or touching HubSpot.
- Read [references/schema-and-tag-contract.md](references/schema-and-tag-contract.md) before generating Head HTML, structured data, or any HubSpot tag payload.
- Use `assets/carol-chen/` as the tested implementation example. It is a draft demonstration, not publishable interview copy.
- Pair with `$man-digital-design-system` for brand decisions and `$man-digital-cms-pages` for source validation or CMS uploads.

## Required outcome

1. Normalize the supplied source. Run `python3 scripts/ingest_interview_source.py <source> --output <working-directory>` for public YouTube or local Markdown. YouTube intake uses the free caption cascade documented in the source-ingestion reference; only add `--whisper-fallback` when local audio transcription is acceptable. Use `--source-type granola` for a copied Granola transcript or Markdown export. Resolve every `PROMPT_REQUIRED` field with the user; never fabricate missing guest assets or profile details.
2. Treat a supplied LinkedIn URL as a candidate, not as verified identity. Resolve the guest with Apollo.io's no-credit people search or Exa's `category:people` search, corroborate the match against at least two person-specific signals and two independent HTTPS evidence URLs, and record the result in `linkedinVerification`. Do not use Apollo's credit-based enrichment without the user's explicit approval. Stop before rendering or CMS save when the identity is ambiguous or contradictory.
3. Inspect the approved Figma desktop and mobile frames and the current HubSpot blog template before editing. Treat Figma as the layout and visual reference, not as a fixed interview-question script.
4. Map the strongest answerable themes in the supplied source, then select 7 or 8 source-adapted questions. Every selected question must have direct or partial evidence with timestamps or source passages. If the source cannot support at least 7 complete answers, stop and request more source material instead of inserting a placeholder.
5. Reuse the Carol structure: intro, one lead-media treatment, context blocks, 7–8 complete Q/A sections, pull quote, takeaways, guest card, and LinkedIn action. When a YouTube video is embedded, make the responsive privacy-enhanced player the only lead media in the article body and do not render a separate thumbnail or title-card image above it. Keep the YouTube thumbnail only as the Open Graph/featured image. When there is no embedded video, require an approved image from the user prompt and render that image as the article lead; never fabricate or infer it. Keep editorial state and evidence in internal metadata; do not add a reader-facing automatic-caption or generation disclaimer. Record the visual Figma reference and exact selected question order in metadata so the validator can reject drift.
6. Put post-specific CSS in the individual post Head HTML when shared theme CSS is not proven to load on the blog template. Scope it and wrap it with stable start/end markers so it can be replaced safely.
7. Generate the SEO title and meta description from the completed draft. Match Open Graph title/description to them; use the user-provided approved image or the YouTube thumbnail as a clearly identified draft candidate. Build one marker-bounded connected JSON-LD graph with `scripts/build_interview_schema.py`, using the intended canonical blog URL from the HubSpot draft. Preserve non-schema Head HTML and never emit an automatic `FAQPage` for the interview Q/A sections.
8. Create or update the HubSpot record through the CMS draft API, reusing the content-scoped OpenClaw credential and helpers. Fetch and back up the existing draft, write only through `/cms/v3/blogs/posts/{postId}/draft`, and set `tagIds` by replacement to the singleton canonical Revenue Leaders Interviews tag ID. Do not invoke contextual tag classification or append existing tags. Associate the canonical campaign, then reopen the draft and verify the saved fields, managed schema graph, exactly one resolved tag name, and campaign. Do not use Chrome to author or save the post.
9. Run `python3 scripts/validate_interview.py <interview-asset-directory>` and the CMS source validator when source files changed. When ingestion, schema, or validation changes, also run `python3 scripts/test_ingest_interview_source.py`, `python3 scripts/test_build_interview_schema.py`, and `python3 scripts/test_validate_interview.py`.
10. Manually check the actual HubSpot preview at desktop, tablet, and mobile widths, using native Chrome when it is available. Chrome is a read-only visual QA surface for this workflow. Verify question count/order, video embed when enabled, LinkedIn icon/link and destination, image loading, typography, table of contents, no overflow, rendered Open Graph fields, one valid managed schema graph, exactly one resolved `Revenue Leaders Interviews` tag, the campaign association, and draft status.

## Hard gates

- Never present illustrative answers, automatic captions, Granola notes, or an unreviewed transcript as approved guest words. A machine-created first pass uses internal `draft-source-derived` state with `source-derived` answers/quotes, but no reader-facing generation disclaimer. Sample copy uses `draft-sample-answers`; human-checked transcript copy awaiting approval uses `draft-transcript-reviewed`. Only guest-approved copy may use `approved`.
- Keep raw YouTube/Granola/Markdown source files and the evidence map out of the published article. Treat private Granola content as private input; do not send it to an unrelated external service or expose its share URL.
- Do not invent guest biography, company facts, employment history, metrics, LinkedIn URLs, or quotes. A plausible slug or same-name profile is not evidence. Exclude unsupported material and request missing required inputs; never render an unanswered question or draft placeholder.
- The normalized `linkedinVerification.profileUrl` must exactly match `source.json` and every rendered `.rli-linkedin` href. Validation must reject unverified status, fewer than two matched signals, fewer than two independent evidence URLs, mismatched URLs, query-string tracking, and non-profile LinkedIn URLs.
- Select 7 or 8 questions that fit the actual source. Adapt their wording for clarity while preserving the speaker's subject and intent, then keep that selected wording and order stable through validation and CMS save.
- Use a real LinkedIn SVG or accessible inline SVG; no text glyph or missing icon. External links use `target="_blank"`, `rel="noopener noreferrer"`, and an accessible label.
- Keep the exact tag and campaign name `Revenue Leaders Interviews`. Search before creating either to avoid duplicates. The saved `tagIds` array must contain exactly one ID and that ID must resolve to `Revenue Leaders Interviews`; zero tags, extra topic/context tags, and additive tag updates are blocking failures.
- For every Revenue Leaders Interview draft, automatically associate the canonical `Revenue Leaders Interviews` campaign before handoff and treat the run as incomplete until the saved association has been reopened and verified. If the canonical campaign ID is missing or no longer resolves, stop and request explicit authorization before creating a replacement; then update the canonical ID in the skill instead of silently accepting a new ID or name variant.
- Draft save, campaign association, scheduling, and publishing are separate states. Never publish or schedule without explicit authorization for that action.
- HubSpot writes are API-first. Never use browser form automation for draft creation, replacement, metadata updates, tags, or campaign attachment when the CMS API can perform the operation. Keep browser use to final read-only preview validation.
- Use one managed JSON-LD `@graph` in Head HTML between `<!-- schema-graph:start -->` and `<!-- schema-graph:end -->`. On update, replace only one complete marker pair and preserve everything outside it. Abort on missing mates or duplicate pairs. The graph must describe the article, blog author, verified guest, image, page, breadcrumb, and an embedded `VideoObject` when YouTube is visible; never invent schema fields or publish an automatic FAQ schema for ordinary interview questions.
- Lead media is mutually exclusive. An embedded YouTube player means zero `.rli-article__lead` images in the body and `openGraphImageSource: "youtube-thumbnail"`; a post without an embedded video requires one user-provided `.rli-article__lead` image and `openGraphImageSource: "user-provided-image"`.
- Report these statuses separately: source ingestion/completeness, editorial state, local validation, HubSpot draft save, SEO/Open Graph save, structured-data save/validation, singleton tag/campaign association, responsive preview QA, and publication state.

## Carol example

The bundled Carol assets document the known-good structure and draft-safety pattern:

- `assets/carol-chen/interview-intro.html`
- `assets/carol-chen/interview-body.html`
- `assets/carol-chen/interview-post.css`
- `assets/carol-chen/metadata.example.json` (singleton tag and managed-schema configuration)
- `assets/carol-chen/source.json`
- `assets/carol-chen/source-content.md`
- `assets/carol-chen/evidence-map.json`
- `assets/carol-chen/linkedin-icon.svg`

The Carol example is generated from the bundled YouTube transcript, remains `draft-source-derived`, and contains eight complete source-adapted Q/A sections with no reader-facing generation notice or unsupported placeholders. Copy the structure, replace guest-specific content and assets, preserve the evidence safeguards, and validate the new directory before applying it to HubSpot.
