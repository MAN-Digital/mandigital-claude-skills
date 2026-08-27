# Timing and easing

## Easing: which curve, and why

Easing communicates physics. Getting it wrong is more noticeable than getting duration wrong.

| Curve | Use for | Reads as |
|---|---|---|
| `ease-out` | anything **entering** | arriving and settling |
| `ease-in` | anything **exiting** | being taken away |
| `ease-in-out` | anything **moving** while staying on screen | a considered move |
| `linear` | opacity-only, rotation, progress | mechanical, which is correct for these |
| `ease-out-back` | playful confirmations | overshoot; use sparingly |

**Never `ease-in` on an entrance.** It starts slow and ends fast, so the element slams into place.
This is the most common easing mistake and it's immediately visible once you know to look.

**`linear` for opacity is not laziness.** Perceived brightness change is close enough to linear
that easing a fade usually looks worse — it lingers at one end.

```css
:root {
  --ease-out-quint:    cubic-bezier(.23, 1, .32, 1);   /* strong settle, default entrance */
  --ease-out-cubic:    cubic-bezier(.33, 1, .68, 1);   /* gentler, for larger elements */
  --ease-in-out-cubic: cubic-bezier(.645, .045, .355, 1);
}
```

Larger elements need gentler curves and longer durations. A full-screen sheet with
`--ease-out-quint` at 200ms feels violent; the same curve on a 32px chip feels crisp.

---

## Values that arrive at a number: the settle curve

Anything that **counts to a figure or fills to a measured length** — counters, percentages,
currency, bar fills, gauges, progress rings, donut sweeps — is a different problem from an element
entering the frame, and it wants a different curve.

Use **`ease-out-expo`**, not `ease-out-cubic`.

```css
--ease-out-expo: cubic-bezier(.16, 1, .3, 1);
```
```js
outExpo: t => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t))
```

The behaviour, counting 0 → 45:

| Elapsed | Value | Reads as |
|---|---|---|
| first 25% | 0 → 30 | too fast to read; you register motion, not digits |
| next 35% | 30 → 42 | slowing, digits becoming legible |
| last 40% | 42 → 45 | visibly settling onto the number |

A wave running up wet sand. Fast up the beach, then it takes its time arriving at the line it
stops on. `ease-out-cubic` distributes the change too evenly — the number ticks up at a near-steady
rate and reads as a mechanical odometer. `ease-out-expo` gives you the arrival.

**The bar and its number must share one progress value.** This is the failure to watch for: if the
fill is eased on one curve and the counter on another — or worse, they have different delays or
durations — the digits stop describing the bar, and at some frames the number is simply wrong for
the length shown.

```js
// WRONG: two independent animations of the same quantity
const pBar = at(t, d, F(12), ease.outCubic);
bar.style.width = (pBar * frac * TRACK) + "px";
label.textContent = Math.round(at(t, d + F(1), F(14), ease.outCubic) * 45) + "%";

// RIGHT: one value, both consumers
const p = at(t, d, F(24), ease.outExpo);
bar.style.width = (p * frac * TRACK) + "px";
label.textContent = Math.round(p * 45) + "%";
```

**Budget more frames than feels necessary.** The tail is the whole point, and it's the first thing
lost to a short window — at 12 frames the settle is 5 frames long and invisible. 24–30 frames at
25fps is the useful range for a counter you want people to watch land.

---

## Web durations

| Motion | Duration |
|---|---|
| Hover, focus ring | 100–150ms |
| Press / active | 80–120ms |
| Small element enter | 200–250ms |
| Small element exit | 150–200ms |
| Modal, sheet, drawer enter | 250–350ms |
| Modal, sheet, drawer exit | 200–250ms |
| Page / route transition | 300–400ms |
| Stagger interval between siblings | 40–80ms |

Exits at roughly 75% of the matching entrance. Entering deserves attention; leaving is already
decided and lingering feels like lag.

**Stagger only works up to about 6 items.** Beyond that the last item's delay exceeds the point
where the user is still reading it as one gesture. For long lists, stagger the first 5 and bring
the rest in together, or animate the container instead.

---

## Render durations: use frames

At 25 fps one frame is 40ms. Milliseconds stop being a meaningful unit — you can only land on
multiples of 40. Author in frames and convert.

| Frames | @25 fps | @50 fps | Typical use |
|---|---|---|---|
| 2 | 80ms | 40ms | below the floor — reads as a cut |
| 3 | 120ms | 60ms | **minimum perceptible motion** |
| 4 | 160ms | 80ms | quick exit |
| 5 | 200ms | 100ms | standard exit |
| 6 | 240ms | 120ms | standard entrance |
| 8 | 320ms | 160ms | large element entrance |
| 10 | 400ms | 200ms | sheet, drawer |
| 12 | 480ms | 240ms | slow reveal |
| 20 | 800ms | 400ms | bar growth, counter |
| 25 | 1000ms | 500ms | full-second beat |

**Three frames is the floor at 25 fps.** Anything shorter is a pop. This means the web's 100ms
button press and 150ms hover simply don't exist as motion at 25 fps — if you're rendering a
simulated interaction, budget at least 4 frames for it.

**Stagger in frames too.** At 25 fps, 2 frames (80ms) between siblings is a comfortable stagger;
1 frame (40ms) reads as almost simultaneous. At 50 fps use 4 and 2 respectively.

Use `frames(n, fps)` from `assets/harness.js` so the numbers stay readable in code:

```js
const p = at(t, frames(5), frames(20), ease.outQuint);   // 5-frame delay, 20-frame growth
```

---

## Springs

Springs are the right default for **interruptible web motion** — a drag, a toggle, anything the
user can reverse mid-flight. They model momentum, so reversing feels physical rather than like a
rewind.

```tsx
transition={{ type: "spring", stiffness: 400, damping: 30 }}
```

| Feel | stiffness | damping |
|---|---|---|
| Snappy, minimal overshoot | 400 | 30 |
| Gentle | 200 | 25 |
| Bouncy | 300 | 15 |
| Heavy, deliberate | 150 | 30 |

Damping below about 15 gives visible oscillation. Above about 40 the spring is effectively a
tween and you should use one.

**Avoid springs in the render track.** A spring has no fixed duration — it settles asymptotically —
so you can't pin the end to a frame count, and the last few frames are spent on movement too small
to see. Use a tween with `ease-out-quint` or `ease-out-back`, which gets you the same settle with a
known end time.

---

## Duration scales with distance

A 4px hover lift and a 400px sheet slide should not share a duration. Rough guide, at 1080p:

| Distance | Web duration | Frames @25 |
|---|---|---|
| under 20px | 120–160ms | 3–4 |
| 20–100px | 180–240ms | 5–6 |
| 100–400px | 250–320ms | 6–8 |
| full screen | 350–450ms | 9–11 |

Not linear — perceived duration scales closer to the square root of distance. Doubling the travel
does not mean doubling the time.
