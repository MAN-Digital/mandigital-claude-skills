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

The free ingestion cascade is deterministic:

1. `youtube-transcript-api` retrieves the selected caption track.
2. `yt-dlp` retrieves metadata and provides a caption fallback.
3. Only when `--whisper-fallback` is explicitly supplied, `faster-whisper` downloads the audio and transcribes it locally on CPU with INT8 compute.

Installed CLIs are reused. Otherwise the first two tools run ephemerally through `uvx`, so the skill does not modify the caller's Python environment. The script writes `source-content.md` and `source.json`, including the provider and fallback history, generated-caption flag, video ID, privacy-enhanced embed URL, thumbnail/Open Graph image candidate, caption kind, source hash, and missing prompt inputs.

If a video has neither manual nor automatic captions, opt into the local fallback:

```bash
python3 scripts/ingest_interview_source.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --output work/guest-name \
  --whisper-fallback \
  --whisper-model small
```

Local Whisper downloads the audio and a model, and may take substantial CPU time. If it also fails, stop and ask for a transcript or Markdown export. Do not infer the interview from the title or description alone.

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
- `linkedinProfile`: candidate guest profile URL. Verify it with the LinkedIn identity workflow before treating the input as resolved or rendering it;
- `openGraphImage`: approved 16:9 article/OG image URL for Markdown, Granola, or another non-video source. This is the user-provided lead image when no video is embedded.

For YouTube, always use the highest-quality available YouTube thumbnail as the Open Graph candidate and record `openGraphImageSource: "youtube-thumbnail"`; do not ask for or substitute a separate title card. The thumbnail may be copied to HubSpot Files, but it must not also be rendered above the embedded player. Markdown and Granola sources have no automatic image candidate, so the user must provide the image in the prompt before handoff.

## Build the evidence map before writing

Create `evidence-map.json` in the working asset directory. It is an internal QA artifact and must not be pasted into the blog post. Use this structure:

```json
{
  "sourceSha256": "...",
  "questions": [
    {
      "question": "Source-adapted question supported by this interview",
      "sourceRefs": ["00:12:31-00:14:08"],
      "evidence": ["Short source passage or faithful note"],
      "coverage": "direct"
    }
  ]
}
```

Select 7 or 8 questions from the source's strongest answerable themes. Every selected question needs `direct` or `partial` coverage, evidence, and source references. Adapt question wording for clarity without changing the speaker's subject or intent. Never select a question with missing coverage and never render a placeholder; if fewer than 7 complete answers are supportable, request more source material.

## Drafting rules

- Use `draft-source-derived` for the first generated post. Every Q/A uses `data-answer-state="source-derived"` and every pull quote uses `data-editorial-state="source-derived"`. Track the source and review status in metadata and the evidence map; do not add a reader-facing automatic-caption or generation disclaimer.
- Preserve the guest's meaning. Remove verbal filler and repetition, but do not add claims, causal explanations, metrics, or certainty not supported by the evidence map.
- Direct quotation marks require exact source wording. Otherwise use an unquoted draft answer or clearly labelled paraphrase.
- Generate the intro, authority section, company section, learning callout, answers, takeaways, and SEO/social copy from supported evidence plus verified prompt details.
- Advance to `draft-transcript-reviewed` only after a human checks the draft against the transcript. Advance to `approved` only after guest/editorial approval.

## YouTube embed

When `embedVideo` is true, place one responsive `.rli-video` block as the first media in the article body and before the opening body paragraph. Omit `.rli-article__lead` entirely so the YouTube thumbnail is not duplicated above the player:

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

Do not autoplay. When there is no embedded video, omit the block, record `embedVideo: false`, and render exactly one `.rli-article__lead` using the approved image supplied by the user. Markdown and Granola modes never fabricate a video embed or a lead image.

The wrapper must span `100%` of the available blog-body width, use a transparent background, and preserve `aspect-ratio: 16 / 9`. The iframe must fill the wrapper with no border or extra padding. HubSpot's editor may wrap an iframe in `.mce-preview-object`; expand that wrapper to `100%` width and height as part of the scoped video CSS. Do not add a black background behind the player.

## Metadata assembly

- Generate the SEO title and meta description from the completed article, then use the same reviewed values for Open Graph title and description.
- Add a complete `linkedinVerification` record only after Apollo.io or Exa cross-source verification. The normalized profile URL must exactly match `source.json.provided.linkedinProfile` and every rendered LinkedIn action.
- Set `sourceType` to `youtube`, `markdown`, or `granola` and `embedVideo` to the actual rendered choice.
- For YouTube, transfer the YouTube thumbnail to HubSpot Files when required by the CMS workflow; verify the final public HTTPS `og:image` in preview and confirm that the same image is absent from the article body.
- For Markdown/Granola, stop before HubSpot handoff if the user-provided lead/Open Graph image or guest assets remain unresolved.

Official behavior references: [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api), [yt-dlp metadata and subtitle options](https://github.com/yt-dlp/yt-dlp/blob/master/README.md), [faster-whisper](https://github.com/SYSTRAN/faster-whisper), [Granola transcript copying](https://docs.granola.ai/help-center/taking-notes/transcription), and [Granola note sharing/export behavior](https://docs.granola.ai/help-center/sharing/sharing-notes).
