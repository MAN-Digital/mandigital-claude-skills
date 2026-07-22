# Video-Grounded Storyboard (Gemini Video Understanding)

## When to use this

Only for brain-dump mode where the user hands you an actual **source video file, a public
YouTube URL, or a public Loom share URL** — not just a pasted transcript — of a
tutorial/screen-share, and the source has enough distinct on-screen frames that guessing the
sequence from prose would risk the Reader Script and Visual Cue Sheet drifting out of sync.
If all you have is text, skip this file and follow
[script-templates.md](script-templates.md)'s brain-dump mode as before.

## What it does

Runs [`scripts/analyze_source_video.py`](../scripts/analyze_source_video.py) against the
source video using Gemini's video-understanding API. Gemini returns a structured, timestamped
list of on-screen events — what screen is showing, what the presenter clicks or types, any
visible UI text — read directly from the video's pixels and audio, not inferred from a
transcript someone typed up.

## Setup (one-time)

1. Get a Gemini API key from Google AI Studio: `https://aistudio.google.com/apikey`.
2. Set it as an environment variable. **Never paste the key into a file in this repo** — this
   skill lives in a public repository.
   ```bash
   export GEMINI_API_KEY="..."
   ```
   (`GOOGLE_API_KEY` also works — the SDK checks both.)
3. Install the one dependency:
   ```bash
   pip install -r scripts/requirements.txt
   ```

## Running it

```bash
# Local video file — uploaded automatically via Gemini's File API, no public hosting needed
python scripts/analyze_source_video.py /path/to/video.mp4 --out video-events.json

# Public YouTube URL — referenced directly, no upload step
python scripts/analyze_source_video.py "https://www.youtube.com/watch?v=XXXXXXXXXXX" --out video-events.json

# Public Loom share URL — downloaded automatically, then uploaded like a local file
python scripts/analyze_source_video.py "https://www.loom.com/share/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" --out video-events.json
```

- **Local files work directly.** You do not need to host the video anywhere public — the
  script uploads it to Gemini's File API and references the returned file URI.
- **YouTube URLs work directly** for public videos (not private/unlisted).
- **Loom share URLs work directly too.** The script downloads the video first (via Loom's
  `transcoded-url` endpoint — see "Loom download caveats" below), then uploads it through the
  same local-file path as any other video.
- **Any other hosted link (Vimeo, a direct file URL) is not supported directly** — the Gemini
  API does not fetch arbitrary URLs. Download the file first, then run the script against the
  local path.
- Uploaded files are stored by Google for 48 hours, then deleted automatically. There's no
  storage cost — only the normal generation cost of the analysis call.
- No length limit — long videos just cost more (see "Cost and model notes" below).

### Loom download caveats

The Loom download step uses `https://www.loom.com/api/campaigns/sessions/{id}/transcoded-url`
— the same undocumented endpoint several independent open-source Loom downloaders rely on, not
an official Loom API. Two things follow from that:

- **It only works for public share links** where the video owner hasn't disabled downloads.
  Private, password-protected, or download-restricted Looms will fail with a clear error.
- **It could stop working if Loom changes that endpoint.** It's been stable enough for
  multiple independent tools to depend on it, but there's no guarantee. If it breaks, download
  the video manually from Loom's own UI and pass the local file path instead — that path is
  unaffected.

## What comes back

`video-events.json` — an ordered list of events, each with:

- `timestamp` (`MM:SS` in the **source** video)
- `screen_or_context` — what tool/screen/state is visible
- `action` — what the presenter does (click, type, toggle, scroll)
- `on_screen_text` — visible UI labels, field names, button text
- `notes` — anything unclear, worth flagging to Romeo before relying on it

This is raw material for the Blueprint and Cue Sheet — not a finished deliverable, and never
shown to the requester as-is.

## How to fold it into the Blueprint + Cue Sheet

1. Use the event list's **order and content** to plan Blueprint beats
   ([output-export-contract.md](output-export-contract.md) §3) — it tells you what actually
   happens on screen and in what sequence, so beats match a real walkthrough instead of an
   invented one.
2. **Do not copy the source video's own timestamps into the Cue Sheet.** The new recording
   will follow this script's own pacing, usually with new footage — the Cue Sheet's
   timecodes come from the wpm-based Blueprint budget, same as any other script. The source
   video's timestamps only establish sequence and rough relative duration per step.
3. Feed each event's `screen_or_context` / `action` / `on_screen_text` into the matching Cue
   Sheet entry's `Shows:` field. Mark the `Origin:` field as `Rebuild of source video's UI at
{{SOURCE_TIMESTAMP}}` so the editor can pull up the original frame if anything is
   ambiguous.
4. If `notes` flags something unclear in an event, do not guess — surface it in the Flags
   section (§6 of output-export-contract.md) instead of inventing what was on screen.

## Cost and model notes

Gemini bills video input by duration: roughly 300 tokens per second of video at default
resolution, or 100 tokens/sec at `low` resolution. A 10-minute source video costs about
180,000 input tokens for one analysis pass. `low` resolution is cheaper but often can't read
small on-screen text reliably — don't use it for HubSpot UI walkthroughs with small labels
and field names. The script defaults to `gemini-2.5-flash` for cost; pass `--model
gemini-2.5-pro` if `flash` misses details on a first pass.

## Known limits — read before relying on this

- **API auth confirmed working**: a real `GEMINI_API_KEY` was tested against a live text
  generation call and returned a correct response, so the credential wiring (`.env` loading,
  client construction) is verified.
- **Loom URL parsing confirmed working**: the ID regex was tested against share/embed URL
  formats with and without query strings.
- **Not yet tested**: an actual Loom download (no real Loom URL was available to try), and a
  full video-understanding call against real footage (structured JSON parsing, File API
  upload/poll on a real video). Run one short real clip through the full pipeline before
  trusting it for production work — SDK parameter names occasionally shift between
  `google-genai` versions, and that's the first thing to check if it errors.
- Arbitrary public URLs (Vimeo, a direct CDN link) still aren't supported — see above.
