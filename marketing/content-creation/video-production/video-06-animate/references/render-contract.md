# The render contract

Frame-stepped capture works because rendering is decoupled from wall-clock time. The browser is
told "show me the state at t = 3.24s", it renders, we screenshot, we move on. If a screenshot takes
900ms at 4K, nothing drifts — the output is identical to a render that took 9ms per frame.

Screen recording cannot do this. At 4K it will drop frames and the drops land wherever the machine
happened to stutter, which is different every run.

For that to work, the page must expose time as an input. Two ways.

---

## Mode A — WAAPI scrubbing (preferred when the animation also ships on the web)

`document.getAnimations()` returns every `Animation` object on the page — **CSS animations, CSS
transitions, and `Element.animate()` calls alike**. Each can be paused and driven directly:

```js
document.getAnimations().forEach(a => {
  a.pause();
  a.currentTime = tSeconds * 1000;
});
```

This is the useful property: the CSS you ship to production *is* the render source. No second
implementation, no drift between what the site does and what the video shows.

### Requirements

Author the animation so a single global time value determines every element's state:

- Give every animation an explicit `animation-duration` and `animation-delay` measured from a
  common t=0. Stagger with `animation-delay`, not with `setTimeout`.
- Set `animation-fill-mode: both` so elements hold their start state before their delay elapses
  and their end state after. Without this, scrubbing to t=0 shows elements in their un-animated
  CSS state, which is usually wrong.
- Set `animation-play-state: paused` in CSS if you want the page to sit still until driven.

```css
.bar {
  animation: grow 800ms var(--ease-out-quint) both;
  animation-delay: calc(var(--i) * 120ms);
}
@keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
```

That renders correctly in a browser *and* scrubs frame-perfectly.

### Limitations — read these before choosing Mode A

- **Late-mounting elements.** An element that appears partway through the timeline only registers
  its `Animation` object once it exists. `render_frames.py` re-scans every frame, which handles
  most cases, but an element whose *appearance* is driven by a JS timer will never appear, because
  timers don't advance. If mounting is time-driven, use Mode B.
- **Transitions need a trigger.** A CSS transition only creates an `Animation` when the property
  actually changes. Scrubbing can't cause a hover. Simulate the state change by toggling a class
  from `__renderAt`, or convert the transition to a keyframe animation.
- **Motion/React** manages its own time internally and does not cleanly expose to WAAPI scrubbing.
  Do not attempt Mode A on a Motion component tree — use Mode B, or render the CSS version.

---

## Mode B — `window.__renderAt(t)` (the general fallback)

A pure function from time in seconds to visual state. It sets values directly and returns nothing.

```js
window.__renderAt = function (t) {
  // t is seconds from the start of the timeline
  const p = clamp01((t - 0.4) / 0.8);          // 400ms delay, 800ms duration
  const eased = easeOutQuint(p);

  bar.style.transform = `scaleX(${eased})`;
  counter.textContent = Math.round(eased * 1284).toLocaleString();
  label.style.opacity = clamp01((t - 1.0) / 0.3);
};
```

**Same `t` in, identical pixels out, always.** That's the whole contract.

Use Mode B when:

- Values are data-driven — counters, bar widths, chart paths, anything numeric.
- Text content changes over time.
- Elements need to mount or unmount on a schedule.
- You're driving a canvas.
- You're rendering a Motion/React tree.

### Rules for writing `__renderAt`

- **No accumulated state.** Never write `x += delta`. Every frame must be computable from `t`
  alone, in isolation, in any order.
- **No reads of wall-clock time.** No `Date.now()`, no `performance.now()`, no `requestAnimationFrame`
  deltas.
- **No `Math.random()`** unless seeded from `t` or from a fixed seed set once at load.
- **Idempotent.** Calling `__renderAt(2.0)` twice in a row produces the same result as once.
- **Must handle `t` beyond the end.** Clamp, don't wrap, or the last frames will loop back.

Declare the timeline length so the renderer doesn't have to guess:

```js
window.__duration = 6.0;   // seconds
```

`render_frames.py` reads this when `--duration` isn't passed.

---

## Third channel: `window.__segments`

Optional, but set it on anything destined for a timeline. It declares where each element's
animation starts and ends, and the renderer turns it into a manifest with frames and timecode.

```js
window.__segments = [
  { name: "rect1", startFrame: 0,  endFrame: 25, holdEndFrame: 29, targetFrame: 0   },
  { name: "rect2", startFrame: 29, endFrame: 54, holdEndFrame: 58, targetFrame: 500 },
];
```

`targetFrame` is where the segment belongs in the finished video, which differs from `startFrame`
when the render is compacted. The manifest reports both.

Set it via `tl.export()` rather than by hand — the `Timeline` helper in `assets/harness.js` derives
it from the slots you declared, so it can't drift out of sync with the animation.

This is what `--check-holds` validates against, and what `segments.csv` is built from. Without it
you're eyeballing segment boundaries in After Effects. See `references/timeline-and-layers.md`.

---

## Which mode to choose

| Situation | Mode |
|---|---|
| Pure CSS animation, also ships on the web | A |
| Animated counters, bars driven by real numbers | B |
| Text that changes mid-timeline | B |
| Motion / React component tree | B |
| Existing page you didn't write, CSS-based | A, with a test render to verify |
| Anything you're unsure about | B — it's strictly more capable |

Mixing is allowed. The renderer applies WAAPI scrubbing *and* calls `__renderAt` if both are
present, in that order, so a CSS-animated layout can carry a JS-driven counter.

---

## Converting an existing page

1. Pull the real source. For a Pencil `.pen` file: `batch_get` to read the node tree, then
   `export_html`. Don't reconstruct from a thumbnail — the labels, colours, and values will be
   wrong, and you won't notice until the render is done.
2. Slice out just the node you're animating into a standalone HTML file with inline `<style>` and
   `<script>`. One file, no external requests, no build step. This keeps capture fast and removes
   a class of loading race conditions.
3. Add the animation and the contract. `assets/harness.js` gives you the clamp/easing helpers and
   the `__renderAt` scaffold.
4. Verify in a browser by scrubbing manually before rendering anything:

```js
// paste in the console
let t = 0; setInterval(() => { window.__renderAt(t); t = (t + 0.04) % window.__duration; }, 40);
```

If that looks right at 40ms steps, it will render right at 25 fps — because that's the same thing.

---

## Determinism checklist

Before a full render, confirm all of these. Each one has silently corrupted a sequence before.

- [ ] `await document.fonts.ready` before frame 0, or the first frames use fallback fonts
- [ ] No `Date.now()` / `performance.now()` reads in the animation path
- [ ] `Math.random` seeded or unused
- [ ] No `setTimeout` / `setInterval` driving visual state
- [ ] No network requests after load — inline everything, including images as data URIs
- [ ] No `<video>`, GIFs, or CSS `steps()` animations tied to real time
- [ ] `animation-fill-mode: both` on every keyframe animation (Mode A)
- [ ] Rendering the same frame twice produces byte-identical PNGs

That last one is the actual test. `render_frames.py --verify` renders frame 0 twice and compares.
