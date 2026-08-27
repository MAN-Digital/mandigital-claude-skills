# Marketing Asset Specs (2026)

Authoritative canvas sizes, aspect ratios, safe zones, and export rules for every MAN
Digital marketing asset this skill builds. Verified across multiple 2025–2026 sources.
**Always confirm the asset type first, then build to the exact spec below.** When the user
names a size that conflicts with these, prefer the spec unless the user is explicit.

All assets are built as **editable Pencil sources** (see `editable-pencil-source.md`) and
exported at the end. Color space is always **sRGB** — never CMYK or Adobe RGB.

---

## Quick Spec Table

| Asset                               | Canvas (px)                      | Ratio     | Export                 | Hard limits      |
| ----------------------------------- | -------------------------------- | --------- | ---------------------- | ---------------- |
| LinkedIn post — square              | **1080 × 1080**                  | 1:1       | PNG/JPG                | ≤5 MB            |
| LinkedIn post — portrait (default)  | **1080 × 1350**                  | 4:5       | PNG/JPG                | ≤5 MB            |
| LinkedIn post — landscape           | 1200 × 627                       | 1.91:1    | PNG/JPG                | ≤5 MB            |
| LinkedIn carousel (PDF)             | **1080 × 1350** (or 1080 × 1080) | 4:5 / 1:1 | → route to `/carousel` | ≤100 MB PDF      |
| LinkedIn Event cover                | **1920 × 1080** (min width 480)  | 16:9      | PNG/JPG                | ≤8 MB            |
| LinkedIn personal banner            | **1584 × 396**                   | 4:1       | PNG/JPG                | ≤8 MB            |
| LinkedIn company cover              | **1128 × 191**                   | ~5.9:1    | PNG/JPG                | ≤3 MB            |
| Facebook ad — feed (portrait)       | **1080 × 1350**                  | 4:5       | PNG/JPG                | ≤30 MB           |
| Facebook ad — feed (square)         | 1080 × 1080                      | 1:1       | PNG/JPG                | ≤30 MB           |
| Facebook ad — Stories               | 1080 × 1920                      | 9:16      | PNG/JPG                | ≤30 MB           |
| Facebook ad — Reels                 | 1080 × 1920                      | 9:16      | PNG/JPG                | ≤30 MB           |
| Facebook ad — carousel card         | 1080 × 1080                      | 1:1 only  | PNG/JPG                | ≤30 MB/card      |
| Facebook post — portrait (default)  | **1080 × 1350**                  | 4:5       | PNG/JPG                | ≤30 MB           |
| Facebook post — square              | 1080 × 1080                      | 1:1       | PNG/JPG                | ≤30 MB           |
| Facebook link / OG preview          | **1200 × 630**                   | 1.91:1    | PNG/JPG                | min 600 × 315    |
| Instagram post — square             | 1080 × 1080                      | 1:1       | PNG/JPG                | ≤30 MB           |
| Instagram post — portrait (default) | **1080 × 1350**                  | 4:5       | PNG/JPG                | ≤30 MB           |
| Instagram Stories / Reels           | 1080 × 1920                      | 9:16      | PNG/JPG                | ≤30 MB img       |
| YouTube thumbnail                   | **1280 × 720**                   | 16:9      | **JPG ~85–90%**        | **≤2 MB (hard)** |
| Open Graph / share image            | **1200 × 630**                   | 1.91:1    | **JPG/PNG**            | <1 MB ideal      |
| Luma (lu.ma) event cover            | **1080 × 1080** (min 800 × 800)  | 1:1       | PNG/JPG                | no max; static   |

> Carousels are **not** built here — detect and route to the `/carousel` skill (see
> `SKILL.md` Routing). This file documents the carousel page size only so the assets skill
> can answer questions and hand off cleanly.

---

## Per-Asset Detail

### LinkedIn single feed post image

- **Square 1080 × 1080 (1:1)** — versatile, never cropped in feed.
- **Portrait 1080 × 1350 (4:5)** — **default for scroll-stopping**; takes the most mobile
  height. LinkedIn renders no taller than 4:5; anything taller is cropped.
- **Landscape 1200 × 627 (1.91:1)** — only when content genuinely needs width. On mobile,
  landscape may center-crop toward 1:1, so keep key content in the central 627 × 627 square.
- Min recommended width 1080 px (absolute floor 552 × 276). JPG/PNG/GIF, ≤5 MB.

### LinkedIn document / carousel (PDF)

- Page size **1080 × 1350 (4:5)** best performer, or **1080 × 1080 (1:1)**.
- **All pages must be identical dimensions.** Headline top / body middle / CTA low-center.
- 5–15 slides is the engagement sweet spot. **Route to `/carousel`** — do not build here.

### LinkedIn Event cover

- **1920 × 1080 (16:9).** LinkedIn's own event cover uploader (verified 2026-06) states
  **"Minimum width 480 pixels, 16:9 recommended."** Build 16:9 at 1920 × 1080. Do **not** reuse
  the old 4:1 (1776 × 444) banner or the 1584 × 396 personal banner.
- **Safe zone:** keep the event name, date, and logo central-ish. The cover renders full 16:9 on
  the event page but is cropped narrower in feed/share previews, so keep load-bearing content
  away from the extreme edges; an event icon/label can overlay the lower area.
- **Spec history:** earlier 2026 guidance listed a 4:1 (1776 × 444) banner; LinkedIn has since
  moved the event cover to **16:9 — use 1920 × 1080**.

### LinkedIn personal profile banner

- **1584 × 396 (4:1)**, same on desktop and mobile. JPG/PNG, ≤8 MB.
- **Critical overlap:** the user's avatar + name cover the **bottom-left ≈ 568 × 264 px**.
  Treat bottom-left as dead space — push logo, tagline, and key art to the **upper-right
  two-thirds**. Safe content box ≈ x 300–1300, y 20–300. Edges crop on mobile.

### LinkedIn company page cover

- **1128 × 191 (~5.9:1)** — brutally short. Logo/name render **below** the banner (no in-banner
  overlap), but the 191 px height forces heavy mobile crop.
- **Safe zone:** keep everything in the **center 50% × 50%** (≈ x 280–848, y 48–143), one line
  of large text max. To stay crisp, design large at 4200 × 700 (same 6:1) and let the center
  1128 × 191 strip survive. Company Life-tab main image is 1128 × 376.

### Facebook ad (feed + Stories/Reels)

- Feed: **1080 × 1350 (4:5)** Meta-recommended, or 1080 × 1080 (1:1). Stories/Reels 1080 × 1920 (9:16).
- **Carousel cards force-crop to 1:1 — never feed them 4:5 art.**
- **Stories/Reels safe zones:** keep text/logos clear of **top ~14% (≈250 px)** and **bottom
  ~20% (≈340 px) for Stories / ~35% (≈595 px) for Reels** (Reels also reserve ~6% each side).
- Optional quality buffer: upload at 1440-px-wide equivalents to resist Meta's compression;
  1080-base is the safe minimum. ≤30 MB image. Primary text ~125 chars, headline ~27–40.

### Facebook feed post + Open Graph link preview

- Photo post: **1080 × 1350 (4:5)** default, 1080 × 1080 (1:1), or 1200 × 630 (1.91:1) landscape.
- **Shared-link / OG preview: 1200 × 630 (1.91:1)** pulled from the page's `og:image` (min
  600 × 315). Treat the **bottom 20–25%** of a link image as a caution band (UI overlay).
- PNG for text, JPG for photos, sRGB. ≤30 MB; keep OG files small (<100 KB ideal).

### Instagram post + Stories/Reels

- Feed: 1080 × 1080 (1:1) or **1080 × 1350 (4:5) recommended**. Stories/Reels 1080 × 1920 (9:16).
- **Grid-crop trap (2026):** the profile grid now previews at **3:4 (1080 × 1440)**. A 4:5
  portrait is slightly trimmed on the grid — keep the subject inside the center 3:4 region.
- **Stories/Reels safe band ≈ 1080 × 1420**: keep content out of top ~250 px and bottom
  ~250–340 px (username bar, captions, reply/CTA UI). ≤30 MB image.

### YouTube thumbnail

- **1280 × 720 (16:9)** — 16:9 is mandatory; off-ratio gets black bars. Min width 640 px.
- **Hard 2 MB file cap** — files over are silently rejected. Export **JPG at ~85–90%**
  (~200–400 KB); do not shrink dimensions to fit, reduce quality instead. PNG often blows the cap.
- **Duration-badge safe zone:** YouTube paints the dark duration pill over the **bottom-right
  ~15–20%** of every thumbnail — never put text/faces/logos there.
- Keep critical content in the **central 80%** (≈ 1024 × 576). Avoid top corners (Live/New
  badges) and bottom edge (progress bar). Test legibility at ~168–320 px wide.

### Open Graph / social share image

- **1200 × 630 (1.91:1)**, min 600 × 315. JPG or PNG (PNG for text/logos) — **avoid WebP/AVIF**,
  not universally parsed by unfurlers in 2026. Aim <1 MB, ideally <300 KB.
- Keep the headline/logo/key visual in the **center 66%** (~1100 × 580).
- **X (Twitter)** prefers 16:9 (1200 × 675) and crops 1200 × 630 top/bottom; needs
  `twitter:card = summary_large_image`. **LinkedIn caches hard** — refresh via Post Inspector.
  iMessage/Slack mobile square-crop, so keep content centered. Always use absolute HTTPS URLs
  and declare `og:image:width`/`og:image:height`.

---

### Luma (lu.ma) event cover

- **Square 1:1** is required (per Luma's own help docs). Recommended **≥ 800 × 800**; no max and
  no GIF (use a static image). Build at **1080 × 1080** for crisp display across event pages,
  explore feeds, and social shares.
- **Rounded corners:** Luma rounds the image corners on display — **keep logos, text, and key
  elements out of the four corners** or they get clipped. Center the composition.
- **Leave edge breathing room** and **keep text minimal** — the Luma event page already shows the
  title, date, location, and Register button, so the cover can lean visual. A short hook + the
  brand orbit/visual reads better than a paragraph; it must work at both large and thumbnail size.
- Source verified 2026-06 via Luma help center (`help.luma.com/p/event-cover-images`).

## Universal Safe-Zone Cheat-Sheet

- **LinkedIn personal banner:** avatar + name cover **bottom-left ≈ 568 × 264** → push art upper-right.
- **LinkedIn company cover:** brutal 5.9:1, 191 px tall → center 50% × 50%, one line of text.
- **LinkedIn event cover:** **16:9 (1920 × 1080)**, min width 480; keep name/date/logo central, away from extreme edges (feed/share previews crop narrower); never reuse the personal banner.
- **LinkedIn feed landscape:** may center-crop to 1:1 on mobile → key content central square.
- **Meta carousel ads:** force 1:1 → never 4:5 art.
- **Stories vs Reels:** Reels reserve more bottom (~35% / ~595 px) than Stories (~20% / ~340 px).
- **Instagram grid:** previews 3:4 → keep subject in center 3:4 of a 4:5 post.
- **Stories/Reels safe band:** central ≈ 1080 × 1420; clear top ~250 / bottom ~250–340.
- **YouTube:** bottom-right ~15–20% owned by the duration badge; central 80% only; **≤2 MB JPG**.
- **OG image:** X crops to 16:9, mobile chat square-crops → center 66%; absolute HTTPS URL.
- **Luma event cover:** square 1:1, corners are rounded on display → keep logo/text/key art out of corners; minimal text, edge breathing room.
- **Format rule:** JPG for photos, PNG for text/logo-heavy, sRGB everywhere, compress ~85–90%.

---

## Feed-Post Type Minimums (mobile-first — MANDATORY)

Feed posts (LinkedIn / Facebook / Instagram single images, 1080×1080 or 1080×1350, and
Stories/Reels 1080×1920) are read on a phone. A 1080-wide image renders at **~390 px on a
phone (≈0.36×)**, so a 22 px source label shows at **~8 px on screen — invisible**. **Make text
big. When in doubt, go bigger** — but vary weight, don't bold everything. These are floors for a
1080-wide canvas — scale up for 1080×1920:

| Role                                          | Min size (1080-wide)             | Weight                                        |
| --------------------------------------------- | -------------------------------- | --------------------------------------------- |
| Headline / title                              | **≥ 56 px** (aim 64–110)         | 700–800 (bold) — this is the ONE bold element |
| Subhead / supporting line                     | **≥ 34 px** (aim 40–50)          | **500 (medium, NOT bold)**                    |
| Eyebrow / kicker / date                       | **≥ 22 px**                      | 600                                           |
| In-graphic labels (orbit/chip/callout/node)   | **≥ 30 px**                      | 600                                           |
| CTA                                           | **≥ 26 px**                      | 600–700                                       |
| **Logo — stacked mark+wordmark** (e.g. MAN)   | **≥ 44 px tall**                 | n/a (image asset)                             |
| **Logo — one-line lockup** (e.g. Revenue Hub) | **≥ 200 px wide** (≥ 30 px tall) | n/a                                           |

- **Logos count as type for mobile legibility.** A logo's embedded wordmark must survive the same
  ~0.36× phone downscale as text. Don't size logos as tokens — a 120 px-wide stacked logo or a
  200 px lockup on a 1920 cover becomes an unreadable smudge on a phone. Size co-brand logos like
  the table (scale up proportionally on larger canvases — e.g. ~70 px tall mark / ~280 px lockup on
  a 1920-wide cover), keep both co-brand marks at comparable visual weight, and zoom the header in
  the audit to confirm the wordmarks are readable.
- **Hard floor: no meaning-bearing text below 30 px** on a feed post. If text must be smaller to
  fit, the layout is wrong — cut words, shrink the visual, or split the content, don't shrink type.
- **Fix small/weak text by making it bigger, not by bolding it.** The real MAN Digital covers use
  a bold title with a **weight-500, ~50 px subtitle** — only the title is bold. Over-bolding every
  line looks cheap. Reserve weight 400 for genuinely secondary fine print (rare on feed posts).
- This **overrides** any smaller "common Pencil sizes" in inherited brand/readability references —
  those came from dense blog diagrams, not mobile feed posts.
- This **overrides** any smaller "common Pencil sizes" in inherited brand/readability references —
  those came from dense blog diagrams, not mobile feed posts.
- Wide event covers/banners (1776×444, 1584×396, 1128×191) are a different case — they are read
  larger on the profile/event page; follow each asset's safe-zone notes, not these post floors.

## Orientation Defaults When the User Doesn't Specify

| Channel                        | Default canvas                                       |
| ------------------------------ | ---------------------------------------------------- |
| LinkedIn single post           | 1080 × 1350 (4:5 portrait)                           |
| LinkedIn event cover           | 1920 × 1080 (16:9)                                   |
| LinkedIn personal banner       | 1584 × 396                                           |
| LinkedIn company cover         | 1128 × 191                                           |
| Facebook / Instagram post      | 1080 × 1350 (4:5 portrait)                           |
| Facebook ad                    | 1080 × 1350, plus 1080 × 1920 if Stories/Reels named |
| YouTube thumbnail              | 1280 × 720                                           |
| Open Graph / blog share image  | 1200 × 630                                           |
| Luma (lu.ma) event cover       | 1080 × 1080 (square, corner-safe)                    |
| Stories / Reels (any platform) | 1080 × 1920                                          |
