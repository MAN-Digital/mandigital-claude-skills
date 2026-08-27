# Video export

Pipeline: HTML with a render contract → Playwright frame capture → PNG sequence → ffmpeg → video.

The PNG sequence is the master. Keep it until the edit is locked; every NLE imports a PNG sequence
directly and it's lossless.

**Paths in this file are relative for readability.** In real runs, frames and video go in the
design's own output folder — see *Where output goes* in `SKILL.md`. Pass `--out` an absolute path
every time; its `frames` default is relative to the working directory and is what scatters renders
away from the project.

---

## Frame rate

**25 fps is the default** — it matches the rest of the timeline, so no conform, no judder, no
frame blending on import.

**50 fps when slow motion is wanted.** Rendering at 50 and dropping it on a 25p timeline gives you
50% speed with every frame real, no optical-flow interpolation guessing. Costs double the render
time and double the disk. Worth it for a hero shot, wasteful for a lower third.

Do not render at 30 or 60 for a 25p timeline. The 6:5 cadence produces judder that no import
setting fixes cleanly.

### Duration in frames

| Frames | @25 fps | @50 fps |
|---|---|---|
| 1 | 40ms | 20ms |
| 3 | 120ms | 60ms |
| 5 | 200ms | 100ms |
| 6 | 240ms | 120ms |
| 8 | 320ms | 160ms |
| 12 | 480ms | 240ms |
| 25 | 1000ms | 500ms |

Author render-track durations in frames and convert. `6 frames` survives a frame-rate change;
`240ms` doesn't.

---

## Capture

```bash
python scripts/render_frames.py --file animation.html --fps 25 --duration 6 --out frames/
```

| Flag | Default | Notes |
|---|---|---|
| `--file` / `--url` | — | local path or URL; local is faster and avoids network races |
| `--fps` | 25 | 25 or 50 |
| `--duration` | reads `window.__duration` | seconds |
| `--width` / `--height` | 1920 / 1080 | **CSS pixels — the design size, not the output size** |
| `--scale` | 2 | device scale factor; 1920×1080 @2 = 3840×2160 output |
| `--allow-oversize` | off | permit output above 3840×2160; refused by default |
| `--alpha` | off | transparent background, for compositing |
| `--start` | 0 | start time in seconds, for re-rendering a section |
| `--verify` | off | render frame 0 twice and compare — run this once per new animation |

### Why `--scale` and not a bigger viewport

Setting `--width 3840` asks the CSS layout to fill 3840 *CSS* pixels — a different design, with
different breakpoints and relatively smaller text. Setting `--width 1920 --scale 2` renders the
1920 design at 2× pixel density, which is what "4K version of this design" actually means. Text
and borders come out crisp; layout is unchanged.

**The two are multiplied, not chosen between.** Output is `width × scale`. A 4K canvas left on the
default 2× scale is 7680×4320 — four times the pixels, four times the disk, four times the render
time, for no visible gain on a 4K timeline. The script refuses anything above 3840×2160 and tells
you the scale you actually wanted; `--allow-oversize` overrides it if you genuinely mean it.

Neither space is sharper than the other. Both put the same 3840×2160 pixels on disk, and text and
vectors rasterize at device resolution either way. The only thing that changes is which coordinate
system the HTML has to be written in — so pick the one that matches the design and stop there. The
one place the choice does bite is **raster images**: a photo placed at 800 CSS px needs a 1600px
source to stay sharp at 2×, the same demand as an 800-device-px image in a 4K-native design.

### Alpha

Transparency has to be requested at capture time. Playwright screenshots default to an opaque
white background and there's no fixing it afterwards.

```bash
python scripts/render_frames.py --file lower-third.html --alpha --fps 25 --duration 4 --out frames/
```

The page must also have no opaque background of its own — `body { background: transparent }`.

---

## Encoding

```bash
python scripts/encode.py --frames frames/ --fps 25 --profile edit --out animation.mov
```

| Profile | Codec | Pixel format | Container | Use |
|---|---|---|---|---|
| `edit` | ProRes 422 HQ | `yuv422p10le` | `.mov` | **default** — cutting into a timeline |
| `edit-alpha` | ProRes 4444 | `yuva444p10le` | `.mov` | overlays composited over footage |
| `web` | H.264 CRF 18 | `yuv420p` | `.mp4` | previews, YouTube, sharing |
| `web-alpha` | VP9 | `yuva420p` | `.webm` | transparency in a browser |

**Do not deliver H.264 into an editor.** Flat colour with hard edges — dashboards, charts, type —
is the worst case for 4:2:0 chroma subsampling, and every subsequent grade or scale compounds on
top of it. ProRes is bigger on disk and that is the entire point of an intermediate codec.

Raw equivalents, if running ffmpeg by hand:

```bash
# edit — ProRes 422 HQ
ffmpeg -framerate 25 -i frames/f-%06d.png \
  -c:v prores_ks -profile:v 3 -vendor apl0 -pix_fmt yuv422p10le \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  animation.mov

# edit-alpha — ProRes 4444 with alpha
ffmpeg -framerate 25 -i frames/f-%06d.png \
  -c:v prores_ks -profile:v 4444 -alpha_bits 16 -vendor apl0 -pix_fmt yuva444p10le \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  animation.mov

# web — H.264
ffmpeg -framerate 25 -i frames/f-%06d.png \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  animation.mp4
```

The `bt709` tags stop Resolve and Premiere from guessing and shifting the colour on import.

---

## Motion blur / shutter angle

Frame-stepped renders have a 0° shutter — every frame is infinitely sharp, with zero blur. Camera
footage at 25p has motion blur. Cut a rendered element next to real footage and fast movement will
strobe and read as cheap.

Two fixes, in order of preference:

**1. Move slower.** If an element travels more than roughly its own width in one frame, it will
strobe. At 25 fps that's a hard constraint — it's 40ms of screen time. Most of the time the right
answer is a slower, shorter move, which usually looks better anyway.

**2. Render subframes and blend down.** Render at 4× the target rate, then average groups of
frames to approximate a shutter:

```bash
python scripts/render_frames.py --file animation.html --fps 100 --duration 6 --out frames/
python scripts/encode.py --frames frames/ --fps 25 --subframes 4 --profile edit --out animation.mov
```

Under the hood that's `tmix` to average, `framestep` to decimate:

```bash
ffmpeg -framerate 100 -i frames/f-%06d.png \
  -vf "tmix=frames=2,framestep=4,fps=25" \
  -c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le animation.mov
```

`tmix=frames=2` out of 4 subframes ≈ a 180° shutter. Blending 4 of 4 gives 360° — heavier smear,
occasionally the right look for a fast whip. Costs 4× render time and 4× disk, so use it on shots
where the movement is fast enough to need it, not on everything.

---

## Gotchas

**Fonts.** Capture before `document.fonts.ready` resolves and the first frames render in a fallback
face. `render_frames.py` awaits it; if you write your own capture, don't skip it.

**Disk.** 4K PNGs run 5–15 MB each. 60 seconds at 25 fps is 1500 frames — 10–20 GB. At 50 fps with
4× subframes it's 12,000 frames. Confirm duration before starting a long render, and delete frame
directories once the encode is verified.

**ProRes 4444 alpha in Premiere.** Known interpretation mismatch that shows up as green/magenta
tearing. Fix on import — right-click → Modify → Interpret Footage → conform alpha
premultiplication. It's not a bad render; don't re-export.

**Odd dimensions.** H.264 with `yuv420p` needs even width and height. 1920×1080 and 3840×2160 are
fine; a clipped element region might not be. Add `-vf "pad=ceil(iw/2)*2:ceil(ih/2)*2"` if ffmpeg
complains.

**Frame numbering.** `%06d` supports 999,999 frames. Frames start at 0; if a sequence starts
elsewhere, pass `-start_number`.

**Headless rendering differences.** Headless Chromium can differ subtly from headed — most often
in font smoothing. If the render doesn't match the browser, try `--headed` before debugging the
animation.

---

## Handoff

State these when delivering, because the editor needs them and they aren't recoverable from the
file alone:

- frame rate and exact duration in frames
- resolution and whether it carries alpha
- whether it's a loop, and if so the loop point
- if 50 fps was rendered for slow motion, say so — otherwise it lands on a 25p timeline at double
  speed by default
