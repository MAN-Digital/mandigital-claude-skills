# Carousels (LinkedIn & Facebook)

How MAN Digital carousels are made, and the **CTA-link conventions** (the part this skill owns).

## Routing — who builds it

- The slide-by-slide **build** is owned by the **`carousel` skill** (it has the builder + auditor
  sub-agent flow, component registry, cover variations). When a user asks for a carousel, hand the
  topic + slide plan to `/carousel`. This `man-digital-marketing-assets` skill provides the brand
  system and the **channel + link conventions below**.
- Carousels build in their **own new `.pen` file** under
  `/Users/romeoman/Documents/Marketing/Design/Pencil/Carousels/` — **Playground.pen is read-only
  reference only, never the build canvas.** The file must contain ONLY the slides (no copied
  library); recreate component anatomy in the output file (cross-file copy is unsupported).

## Format

- **LinkedIn document carousel:** 4:5 (**1080×1350**), exported as **PDF**, **< 3 MB**, **8–10
  slides**, one idea per slide, hook-first, summary + CTA last. (Exa research, 2026: document/PDF
  posts are LinkedIn's top organic format — algorithm rewards swipe dwell-time.)
- **Facebook carousel:** image **cards only** (no PDF, no clickable links). Each card is an image
  (1080×1350 or 1080×1080).

## Export folder (deliverables)

Carousel exports go to **`/Users/romeoman/Documents/Marketing/Design/Assets/Carousels/`**, in a
**per-carousel subfolder** named for the topic:

```
…/Assets/Carousels/{Carousel Name}/
  {Carousel Name}.pdf      ← all slides, one PDF (LinkedIn document post)
  images/
    slide-01-….png … slide-NN-….png   ← per-slide PNGs (Facebook cards / fallback)
```

The editable `.pen` source lives separately in `…/Pencil/Carousels/` (build folder). Build folder
(`.pen`) ≠ export folder (flat PDF + PNGs).

## CTA link — ALWAYS add it

Every carousel ends on a CTA slide with a CTA pill (e.g. node **`I5IJUu`** "CTA Pill", label
"Read the full playbook →"). Always wire the link:

- **LinkedIn (PDF):** the link CANNOT be stored inside the `.pen` via the Pencil MCP. `href` is in
  the read schema for text, but `Update(textNode,{href})` is silently dropped (returns OK, re-read
  shows nothing — verified 2026-06-22). So add the link at **export time, on the PDF**: export each
  slide as PNG (sequential — parallel exports race), bundle with `img2pdf`, then add a clickable
  **`pypdf` Link annotation** over the CTA pill region on the last page → the post URL
  (e.g. `https://www.man.digital/blog/<slug>`). Pencil's own native multi-slide PDF export times
  out, so this PNG→img2pdf→pypdf path is the reliable one.
- **Facebook (images only):** no clickable links are possible, so put the URL as **visible text**
  on the final slide — `www.man.digital/blog` (or the specific post URL). Never rely on a
  clickable CTA for a Facebook image carousel.
- **Default blog URL:** `www.man.digital/blog`; use the specific post URL when known.

## Build / file gotchas (learned)

- Use **absolute asset paths** for logos (e.g. `/Users/romeoman/Documents/Marketing/Design/Pencil/image-7.png`
  or the design-system `assets/logo-*.png`). Relative filenames break when the `.pen` is in a
  subfolder, rendering the logo as a dotted placeholder.
- Slide frames: 1080×1350, `clip:true`, and **no outer drop-shadow on the slide frame itself**
  (shadow bleed inflates the PNG export past 1080×1350). Put shadows on inner cards only.
- Pencil builds live in memory and may not be flushed to disk immediately; a new build can only be
  reached as the active editor, and `open -a Pencil` on an already-open file re-focuses the
  in-memory tab instead of reloading from disk (use a fresh filename to force a clean load).
