# Source ingestion and transcript-derived drafting

## Choose the source mode

### Public YouTube URL

Run:

```bash
python3 scripts/ingest_interview_source.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --output work/guest-name \
  --guest-image "https://..." \
  --linkedin-url "https://www.linkedin.com/in/.../"
```

The script uses `yt-dlp` to capture video metadata and available manual or automatic captions without downloading the video. It writes `source-content.md` and `source.json`, including the video ID, privacy-enhanced embed URL, thumbnail/Open Graph image candidate, caption kind, source hash, and missing prompt inputs.

If the video has no downloadable captions, stop and ask for a transcript or Markdown export. Do not infer the interview from the title or description alone.

### Markdown or plain-text transcript

Run:

```bash
python3 scripts/ingest_interview_source.py interview.md \
  --output work/guest-name \
  --source-type markdown \
  --content-kind transcript \
  --guest-image "https://..." \
  --linkedin-url "https://www.linkedin.com/in/.../" \
  --og-image "https://..."
```

The input may also be transcript text supplied directly in the prompt; save it in the isolated working directory before running intake. Preserve the original wording and record the generated source hash.

### Granola call

A shared Granola web note exposes summarised notes, not the full transcript. Prefer one of these authorized inputs:

1. the full transcript copied from the Granola transcript panel;
2. a Markdown file containing the copied transcript;
3. Granola notes plus transcript obtained through the user's authorized Granola MCP/API access.

Run the local export through:

```bash
python3 scripts/ingest_interview_source.py granola-call.md \
  --output work/guest-name \
  --source-type granola \
  --content-kind notes-and-transcript \
  --source-url "https://notes.granola.ai/..."
```

Use `--content-kind notes` when only enhanced notes are available. Notes-only input may support a paraphrased draft and takeaways, but not attributed direct quotes or a claim that the answers were transcript-verified.

## Resolve the prompt inputs

Read `missingPromptInputs` from `source.json`. Ask for only the unresolved items:

- `guestImage`: approved HTTPS portrait or HubSpot Files URL;
- `linkedinProfile`: verified guest profile URL;
- `openGraphImage`: approved 16:9 title card or image URL.

For YouTube, the highest-quality available thumbnail is recorded as a draft Open Graph candidate. It may be used for a draft when the user has not supplied a title card, but it must be identified as a YouTube thumbnail and visually checked. Markdown and Granola sources have no automatic image candidate.

## Build the evidence map before writing

Create `evidence-map.json` in the working asset directory. It is an internal QA artifact and must not be pasted into the blog post. Use this structure:

```json
{
  "sourceSha256": "...",
  "questions": [
    {
      "question": "Exact approved Figma question",
      "sourceRefs": ["00:12:31-00:14:08"],
      "evidence": ["Short source passage or faithful note"],
      "coverage": "direct"
    }
  ]
}
```

Every approved question needs `direct`, `partial`, or `missing` coverage. Keep the exact Figma wording in the rendered question even when the interviewer phrased it differently. For `partial` or `missing`, write a transparent placeholder rather than filling the gap from general knowledge.

## Drafting rules

- Use `draft-source-derived` for the first generated post. Every Q/A uses `data-answer-state="source-derived"`, every pull quote uses `data-editorial-state="source-derived"`, and one visible `.rli-source-notice` states that the copy was generated from source material and awaits transcript/editorial review.
- Preserve the guest's meaning. Remove verbal filler and repetition, but do not add claims, causal explanations, metrics, or certainty not supported by the evidence map.
- Direct quotation marks require exact source wording. Otherwise use an unquoted draft answer or clearly labelled paraphrase.
- Generate the intro, authority section, company section, learning callout, answers, takeaways, and SEO/social copy from supported evidence plus verified prompt details.
- Advance to `draft-transcript-reviewed` only after a human checks the draft against the transcript. Advance to `approved` only after guest/editorial approval.

## YouTube embed

When `embedVideo` is true, place one responsive `.rli-video` block after the lead image and before the editorial notice:

```html
<div class="rli-video">
  <iframe
    src="https://www.youtube-nocookie.com/embed/VIDEO_ID"
    title="Interview with GUEST NAME"
    loading="lazy"
    referrerpolicy="strict-origin-when-cross-origin"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen></iframe>
</div>
```

Do not autoplay. When `--no-embed-video` is chosen, omit the block and record `embedVideo: false` in metadata. Markdown and Granola modes never fabricate a video embed.

## Metadata assembly

- Generate the SEO title and meta description from the completed article, then use the same reviewed values for Open Graph title and description.
- Set `sourceType` to `youtube`, `markdown`, or `granola` and `embedVideo` to the actual rendered choice.
- For YouTube, transfer the chosen thumbnail or user-supplied title card to HubSpot Files when required by the CMS workflow; verify the final public HTTPS `og:image` in preview.
- For Markdown/Granola, stop before HubSpot handoff if the requested Open Graph image or guest assets remain unresolved.

Official behavior references: [yt-dlp metadata and subtitle options](https://github.com/yt-dlp/yt-dlp/blob/master/README.md), [Granola transcript copying](https://docs.granola.ai/help-center/taking-notes/transcription), and [Granola note sharing/export behavior](https://docs.granola.ai/help-center/sharing/sharing-notes).
