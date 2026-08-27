# animate

Animation for React, CSS, and HubSpot modules, plus deterministic frame-by-frame
export of any HTML animation to video at 25/50 fps.

Forked from `delphi-ai/animate-skill` (Emil Kowalski course notes). Changes:
Framer Motion -> Motion (`motion/react`), reduced-motion promoted inline,
anti-patterns added, Next.js gaps filled, and a render track added.

```
SKILL.md                          two-track router, golden rules, easing
references/
  canvas-fit.md                   fitting a blog-shaped design into the 4K 16:9 frame
  timing-and-easing.md            frame conversion, curves, springs
  web-motion.md                   CSS + Motion/React recipes
  render-contract.md              the two deterministic modes
  timeline-and-layers.md          slot allocation, time remapping, layered alpha
  video-export.md                 Playwright capture, ffmpeg profiles, alpha, blur
  hubspot-modules.md              no-build-step animation
scripts/
  render_frames.py                HTML -> PNG sequence
  encode.py                       PNG sequence -> ProRes / H.264 / VP9
assets/harness.js                 drop-in render contract
examples/bar-reveal.html          worked example, both modes
```

## Install

Drop the `animate/` folder into either location and restart Claude Code:

```
.claude/skills/animate/          # this project only
~/.claude/skills/animate/        # every project
```

SKILL.md must sit directly inside `animate/`, not in a nested folder.

## Render track quick start

```bash
pip install playwright && playwright install chromium   # ffmpeg also required

python scripts/render_frames.py --file examples/bar-reveal.html --check-fit --out fit/
python scripts/render_frames.py --file examples/bar-reveal.html --verify
python scripts/render_frames.py --file examples/bar-reveal.html --check-holds
python scripts/render_frames.py --file examples/bar-reveal.html --fps 25 --out frames/
python scripts/encode.py --frames frames/ --fps 25 --profile edit --out bars.mov
```

Defaults: 1920x1080 CSS px at `--scale 2` -> 3840x2160 output, 25 fps, ProRes 422 HQ.
`--profile web` for H.264 previews, `--profile edit-alpha` for transparent overlays.

`--width`/`--height` are the design's own coordinate space and `--scale` multiplies them into
real pixels; author against 1920x1080. A 4K-native design renders as `--width 3840 --height 2160
--scale 1` instead -- same output, different coordinate space. Combining the two is 7680x4320 and
is refused unless you pass `--allow-oversize`.

`--check-fit` comes first and needs no render contract, so it runs on the raw design
before any motion exists: it fails on anything crossing the frame edge or under the
27px legibility floor (54 real px at 2x), and writes a still to show the user. Pencil
exports arrive at 1536x1024 and blog graphics are portrait or square; both have to be
reflowed into 16:9 before they are animated, never cropped into it. See
`references/canvas-fit.md`.

Output goes beside the design, not here: for a real job, point `--out` at an absolute
path inside the source design's folder (`<design-dir>/<design>-animation/frames`). The
relative paths above are for the bundled example only. See *Where output goes* in
`SKILL.md`.

Declare timestamps with `Timeline.cues()` when you know them; the manifest written
alongside the frames tells you where each segment belongs in the edit.
