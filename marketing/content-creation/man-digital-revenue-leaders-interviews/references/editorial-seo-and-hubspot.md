# Editorial, SEO, and HubSpot contract

## Editorial states

Use one explicit state throughout a draft:

- `draft-source-derived`: the first complete article was generated from automatic captions, an unreviewed transcript, Markdown, or Granola content. Every answer and pull quote is `source-derived`. Keep this state internal in metadata and evidence records; do not add a reader-facing generation disclaimer. It is never publishable.
- `draft-sample-answers`: layout demonstration only. Every answer and pull quote is `illustrative`; one visible `.rli-sample-notice` states that the copy is not the guest's words.
- `draft-transcript-reviewed`: copy was checked against a reliable recording/transcript but still awaits final editorial/guest approval. Every answer and pull quote is `transcript-reviewed`; one visible `.rli-approval-notice` states that publication approval is still pending.
- `approved`: questions, answers, pull quotes, bio, company facts, and links are approved. Every answer and pull quote is `approved`; no draft notice or draft placeholder may remain.

Automatic captions, Granola summaries, and first-person sample copy are not quote-safe. Direct quotation marks in a source-derived draft require exact source wording; otherwise treat the passage as an unapproved paraphrase. Do not advance the internal editorial state based only on automatic processing.

## Series metadata

Use the same series vocabulary everywhere:

- HubSpot tag: `Revenue Leaders Interviews`
- HubSpot campaign: `Revenue Leaders Interviews`
- Canonical MAN Digital portal campaign ID: `38b1a8b6-07c6-48e4-84de-16de94802392`
- Open Graph image: for YouTube sources, use the YouTube thumbnail (optionally copied to HubSpot Files) and do not render it in the article body above the player. For Markdown, Granola, and other non-video sources, require a user-provided image and use it as the article lead and Open Graph image unless a separate approved OG image is supplied.

Resolve the canonical campaign ID first and verify its exact name. Search by exact name only as a diagnostic fallback. Reuse the canonical record; never create punctuation, singular/plural, or capitalization variants. If the canonical ID no longer resolves, request explicit authorization before creating a replacement and update this reference plus the example metadata with the new ID.

## SEO fields

Write for search clarity, not keyword stuffing:

- SEO title target: about 30–60 characters. Pattern: `<topic/result> | <guest name>`.
- Meta description target: about 120–160 characters. State who the guest is and the useful decisions covered.
- Open Graph title and description normally match the approved SEO title and meta description. HubSpot may derive the rendered `og:title` and `og:description` from those two fields instead of exposing separate inputs; verify the rendered preview tags rather than inventing unavailable controls. Diverge only when a supported field exists and the user requests a reviewed social-specific message.
- Open Graph image must be HTTPS and publicly loadable. A YouTube source uses its own thumbnail and records `openGraphImageSource: "youtube-thumbnail"`. A non-video source records `openGraphImageSource: "user-provided-image"`. Never select a random inline image or invent an image.
- Keep the URL slug concise and stable. Do not change a live slug without explicit redirect/migration authorization.

Before saving, check title/description lengths, spelling of the guest/company, image URL, tag, and campaign. After saving, reopen settings or inspect the preview metadata so the save is evidenced rather than assumed.

## HubSpot workflow

1. Identify the portal, blog ID, and post ID. Confirm the post is a draft.
2. Apply scoped body/intro HTML and post Head HTML CSS. Preserve stable CSS markers for idempotent replacement.
3. Save the supported SEO/social fields and approved image, then verify the rendered `title`, meta description, `og:title`, `og:description`, and `og:image` in the actual preview.
4. Find the exact series tag and attach it to the post. If it is missing, obtain authorization before creating it.
5. Resolve the canonical campaign ID and automatically associate the blog post asset. A missing or unverified association means the draft is not ready for handoff. Creating a replacement campaign requires explicit authorization and a corresponding canonical-ID update.
6. Reopen the settings and campaign view to verify persisted values.
7. Preview desktop/tablet/mobile. Leave the post unpublished unless publication was separately authorized.

Connector or API writes must follow their own confirmation requirements. If connector permissions are missing, use the authenticated HubSpot UI only for the authorized in-scope change; do not treat missing connector access as permission to publish.

## Draft handoff checklist

Report exact values and evidence for:

- post ID and editor URL;
- editorial state and whether any sample/unapproved copy remains (report this in the handoff, not inside the reader-facing article);
- source type, source completeness, evidence-map coverage, and whether automatic captions or notes were used;
- SEO title and meta description;
- Open Graph title, description, and image;
- exact tag and campaign association;
- responsive preview result;
- publication state (`draft`, `scheduled`, or `published`).
