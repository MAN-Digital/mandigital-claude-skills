# Structured data and singleton tag contract

Use this contract for every Revenue Leaders Interview HubSpot draft. It mirrors the
managed JSON-LD approach in OpenClaw's blog pipeline:

- `blog-pipeline/src/blog_runner/services/schema_graph.py`
- `blog-pipeline/src/blog_runner/services/hubspot_publish.py`

The interview skill adapts that implementation to a visible interview article and an
optional embedded YouTube video. Do not pass interview posts through OpenClaw's contextual
tag picker.

## Managed Head HTML region

Write one connected JSON-LD `@graph` to the HubSpot draft's `headHtml` field, bounded by:

```html
<!-- schema-graph:start -->
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[]}</script>
<!-- schema-graph:end -->
```

Before a PATCH, GET the current draft and preserve everything outside this region.

- No marker pair: append the new managed block.
- Exactly one complete pair: replace that region only.
- Exactly one legacy `openclaw-schema-graph` pair: replace it with the current marker pair
  during the same update.
- Multiple pairs, a missing mate, or an end marker before its start: abort. Never silently
  merge, deduplicate, or truncate operator-owned Head HTML.
- Escape a literal `</` inside the JSON body as `<\/` so content cannot terminate the script.

Use `scripts/build_interview_schema.py` to compose the block and to merge it into an
existing Head HTML file when needed.

## Interview graph

The graph uses stable page-fragment IDs and includes:

- blog author `Person`;
- guest/interviewee `Person`, with the verified LinkedIn profile in `sameAs`;
- `ImageObject` for the Open Graph/featured image;
- `WebPage`;
- `BreadcrumbList` (`Home` -> `Blog` -> article);
- `Article`, authored by the HubSpot blog author and linked to the guest through
  `contributor` and `about`;
- `VideoObject` only when the post visibly embeds YouTube.

The template owns the site-wide `Organization` and `WebSite` nodes. Reference their stable
IDs (`https://www.man.digital/#organization` and `https://www.man.digital/#website`) instead
of duplicating them per post.

Use the HubSpot draft's intended canonical page URL, never the editor or preview URL. The
schema headline, description, image, guest identity, video URL, and upload date must match
the saved post and normalized source. Add publication dates only when they are real ISO-8601
values; do not fabricate dates for an unpublished draft.

The interview's seven or eight editorial Q/A sections are not automatically an FAQ. Do not
emit `FAQPage` merely because their headings end in question marks. Add `FAQPage` only if the
article contains a separate, genuinely FAQ-style visible section and every schema answer
matches that visible text.

Google supports `Article`/`BlogPosting` and `VideoObject` structured data. Validate the
rendered page with the Rich Results Test before publication:

- https://developers.google.com/search/docs/appearance/structured-data/article
- https://developers.google.com/search/docs/appearance/structured-data/video

## Exactly one HubSpot tag

The only allowed tag is `Revenue Leaders Interviews`.

1. Resolve the exact existing tag to its canonical ID. Do not create a spelling or case
   variant without explicit authorization.
2. Set the draft payload's `tagIds` to a new singleton array: `[canonicalTagId]`.
3. Do not append to the current `tagIds`. Do not preserve a contextual, RevOps, Sales Ops,
   Marketing Ops, Customer Success, guest, company, or topic tag.
4. Do not invoke OpenClaw's contextual tag picker for interview posts.
5. Reopen `/cms/v3/blogs/posts/{postId}/draft`, require exactly one saved tag ID, resolve that
   ID through `/cms/v3/blogs/tags/{tagId}`, and require the exact name
   `Revenue Leaders Interviews`.

Zero tags, more than one tag, or one tag with the wrong resolved name is a blocking failure.
Campaign association is separate and must still resolve to the canonical
`Revenue Leaders Interviews` campaign.
