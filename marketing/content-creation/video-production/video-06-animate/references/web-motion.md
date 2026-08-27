# Web motion — CSS and Motion/React

Library note: **Motion**, formerly Framer Motion. Package `motion`, import from `motion/react`.
The old `framer-motion` package still resolves, which is why stale code survives silently — don't
write it into anything new.

```bash
pnpm add motion
```
```tsx
import { motion, AnimatePresence } from "motion/react";
```

**Next.js App Router:** any file using `motion.*` needs `"use client"`. Motion components carry
event handlers and state and cannot be server components. This is the most common Next.js motion
bug and it surfaces as a build-time error about event handlers in server components.

---

## CSS patterns

Reach for CSS first. It has no bundle cost, runs on the compositor, and survives hydration.

### Hover lift
```css
.card {
  transition: transform 200ms var(--ease-out-quint),
              box-shadow 200ms var(--ease-out-quint);
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgb(0 0 0 / 0.15);
}
```
`box-shadow` does trigger paint. It's acceptable on a single hovered card; it is not acceptable on
40 cards animating at once. For a grid, animate the shadow on a pseudo-element's `opacity` instead.

### Press
```css
.button { transition: transform 100ms ease-out; }
.button:active { transform: scale(0.97); }
```
Below `scale(0.95)` it reads as a glitch rather than a press.

### Reveal on mount
```css
@keyframes rise {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.reveal {
  animation: rise 280ms var(--ease-out-quint) both;
  animation-delay: calc(var(--i, 0) * 60ms);
}
```
`both` matters twice over: on the web it holds the start state before the delay elapses, and in the
render track it's what makes the animation scrubbable to t=0 correctly.

### Height without animating height
`height` is not animatable without layout. Use a grid row instead — this animates on the
compositor and needs no measurement:

```css
.collapse { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 260ms var(--ease-out-quint); }
.collapse[data-open="true"] { grid-template-rows: 1fr; }
.collapse > * { overflow: hidden; }
```

### Reduced motion
Ship with every animation:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
This kills motion but keeps end states, which is what the preference asks for — not "no
animation" but "no vestibular trigger". Opacity fades are generally fine to keep; movement,
parallax, and scale are what to remove.

---

## Motion / React patterns

### Enter and exit
```tsx
<AnimatePresence>
  {isOpen && (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.2, ease: [0.23, 1, 0.32, 1] }}
    />
  )}
</AnimatePresence>
```
`AnimatePresence` is the only way to animate an unmount — React removes the node immediately
otherwise. The child must have a stable `key` if there's more than one.

### Shared element
```tsx
{active === tab && (
  <motion.div
    layoutId="tab-indicator"
    className="absolute inset-0 rounded bg-blue-500 -z-10"
    transition={{ type: "spring", stiffness: 400, damping: 30 }}
  />
)}
```
One `layoutId` per shared element per tree. Duplicates cause the indicator to tear between two
positions.

### Stagger
```tsx
const container = { hidden: {}, visible: { transition: { staggerChildren: 0.06 } } };
const item = {
  hidden:  { opacity: 0, y: 16 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.28, ease: [0.23, 1, 0.32, 1] } },
};

<motion.ul variants={container} initial="hidden" animate="visible">
  {items.map((i) => <motion.li key={i.id} variants={item}>{i.label}</motion.li>)}
</motion.ul>
```
Variants propagate by name, so children need no props beyond `variants`.

### Layout changes
```tsx
<motion.div layout transition={{ duration: 0.3, ease: [0.23, 1, 0.32, 1] }} />
```
`layout` animates position and size changes caused by anything — a sibling appearing, text
changing, a flex reflow. It uses FLIP, so it's transform-based and cheap. The one artifact to know:
children get squashed by the parent's scale unless they also carry `layout`.

### Reduced motion in Motion
```tsx
import { useReducedMotion } from "motion/react";
const reduce = useReducedMotion();
<motion.div animate={{ opacity: 1, y: reduce ? 0 : 0 }} initial={{ opacity: 0, y: reduce ? 0 : 20 }} />
```
Or wrap the app in `<MotionConfig reducedMotion="user">` and let Motion strip transforms globally.
That's usually the better default.

---

## Performance

The rule is: **`transform` and `opacity` only.** They're handled by the compositor and skip layout
and paint entirely.

| Property | Cost |
|---|---|
| `transform`, `opacity` | composite only — free |
| `filter`, `backdrop-filter` | GPU, but expensive at large sizes |
| `box-shadow`, `border-radius`, `background` | paint every frame |
| `width`, `height`, `top`, `left`, `margin`, `padding` | **layout** every frame — avoid |

`will-change: transform` promotes an element to its own layer. Use it on the handful of things
actually animating, and remove it afterwards — every promoted layer costs GPU memory, and applying
it broadly makes things slower, not faster.

To verify: DevTools → Rendering → Paint flashing. If green rectangles appear during the animation,
something is repainting.

**None of this applies in the render track.** You're not running in real time, so an expensive
frame costs render seconds, not dropped frames. Animate `filter`, `box-shadow`, `clip-path`, or
layout freely when the output is a video file.
