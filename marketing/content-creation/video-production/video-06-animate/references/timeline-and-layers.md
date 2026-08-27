# Timeline slots and layer separation

Two ways to keep element animations independently controllable in the edit. Pick one before
authoring — retrofitting either is more work than starting with it.

| | **Slotted timeline** | **Layered alpha** |
|---|---|---|
| Output | one file | one file per element |
| Retiming | time remapping | drag the layer |
| Reordering | **not possible** | free |
| Repositioning | not possible | free |
| Setup cost | low | medium |
| Render cost | full timeline once | sum of segment lengths |
| Use when | build-up sequence, order is fixed | elements are independent |

---

## Slotted timeline

Spread each element's animation across a long fixed timeline so no two overlap, then use time
remapping in After Effects or Premiere to place each one where the edit wants it.

```
0s                                                              60s
|--[card]------|--[title]-----|--[total]-----|--[bars]-----------|
   anim  hold     anim  hold     anim  hold     anim      hold
```

Each element animates at the head of its slot and **holds perfectly still** for the rest of it.
The hold regions are what time remapping freezes on.

### The hard constraint: holds must be absolutely static

Time remapping freezes a frame. If anything is still moving during a hold — a slow gradient
drift, a pulsing dot, a blinking cursor, an easing curve that hasn't fully settled — you cannot
freeze cleanly there, and the freeze will read as a stutter or a stuck frame.

This means:

- **No idle or ambient animation anywhere on the timeline.** Loops, pulses, and shimmer break the
  whole pattern. If you need them, they belong on a separate layer rendered independently.
- **Let easing fully settle before the hold begins.** `ease-out-quint` is asymptotic; the last 2%
  of movement can run several frames past where it looks finished. Budget 2–3 frames of settle
  inside the animation length, not at the start of the hold.
- **Clamp, don't wrap.** `at()` in the harness clamps at both ends, which is what produces a true
  hold. Never use a modulo or a looping progress function.

`render_frames.py --check-holds` renders the last frame of each hold region twice and compares —
if a hold isn't static, it fails there rather than after the full render.

**Scope: this rule is for renders that will be remapped.** A *final placed clip* — pacing already
true against the transcript, `compact: false` — may carry ambient motion (a drifting depth
ellipse, dot-grid shimmer: the house "soul" layer), and usually should. The trade is explicit and
you state it when delivering: an ambient clip can never be retimed by freezing holds, so when the
cut shifts, the clip is re-derived and re-rendered. Decide per clip which contract it's under:
**remappable** (sterile holds, retiming free) or **final** (ambient allowed, retiming = re-render).

### The limit: order of appearance is fixed

Time remapping changes *when*, never *what*. If the card appears at frame 100 and the title at
frame 300, then any frame after 300 shows both. You cannot produce title-without-card from this
render, in any order, at any speed.

That's usually fine — a build-up sequence is exactly what you want on a dashboard reveal. It is
not fine if the edit might want elements in a different order, or one element alone. That's the
layered case below.

### Pacing and speed are different things

This is the distinction that decides everything else, and conflating them is what makes a render
not match the spec.

**Pacing** — *when* each element appears. Fully recoverable by time remapping, because remapping
stretches a static hold losslessly. A 4-frame hold can be held for ten seconds in the edit.

**Speed** — *how long* one element takes to animate. **Not recoverable.** Stretching 20 rendered
frames across 15 seconds means either holding each frame ~19 times (staccato) or optical-flow
interpolating (mush on type, and any counter digits become nonsense). If a bar should take 15
seconds to fill, render 375 frames of it.

So: **pay render time for motion, never for stillness.**

That resolves the "long-form graphics need slower animation" problem correctly. A graphic on screen
for two minutes with everything animating in 2 seconds does feel abrupt — but the fix is longer
*animations*, not longer *holds*. Give the bar 15 seconds of real growth if that's the intent. The
40 seconds of nothing between elements is what compaction removes, and it costs you nothing.

### Cue sheets

When you know your timestamps, declare them. The cue list becomes the single source of truth, so
the render cannot drift from the spec:

```js
const tl = Timeline.cues({
  fps: 25,
  compact: true,
  cues: [
    { name: "rect1", at: "0:00", anim: "1s"  },
    { name: "rect2", at: "0:20", anim: "1s"  },
    { name: "rect3", at: "0:40", anim: "15s" },   // genuinely slow -> rendered slow
  ],
});
tl.table();    // print the plan, check it against your cue sheet
```

`at` accepts seconds (`20`), `m:ss` (`"0:20"`), `h:mm:ss`, timecode (`"00:00:20:00"`), or frames
(`"500f"`). `anim` accepts the same.

**Overlapping cues throw.** If one element is still animating when the next starts, there's no hold
between them and neither can be frozen independently — so the constructor refuses rather than
producing a render that silently can't be remapped:

```
Timeline.cues: "rect1" runs to 00:00:25:00 but "rect2" starts at 00:00:20:00.
Overlapping cues have no hold between them and cannot be time-remapped
independently. Shorten "rect1" or move "rect2" later.
```

### compact: true vs false

Same cue sheet, two renders:

| | `compact: false` | `compact: true` |
|---|---|---|
| Frames (example above) | 1379 | 437 |
| Length | 55s | 17.5s |
| In the edit | drop it in, pacing is already right | remap each segment to its **place at** timecode |
| Holds | as declared | 4 frames |
| Animation speed | as declared | **as declared** — unchanged |

Compaction only ever removes stillness. `rect3`'s 15-second growth survives at 375 frames in both.

Use `compact: false` when the pacing is final and you want to drop one clip on the timeline.
Use `compact: true` when the pacing might change, or when the holds are long enough that rendering
them is wasteful — which at 4K is most of the time.

### The manifest closes the loop

Compact rendering only works if you know where each segment belongs. `render_frames.py` writes
`segments.csv` / `.json` / `.md` with both timecodes:

| Slot | Renders at | Place at | Anim | Hold |
|---|---|---|---|---|
| rect1 | 00:00:00:00 | 00:00:00:00 | 25f | 4f |
| rect2 | 00:00:01:04 | 00:00:20:00 | 25f | 4f |
| rect3 | 00:00:02:08 | 00:00:40:00 | 375f | 4f |

Remapping becomes mechanical: keyframe at *renders at*, move to *place at*. No scrubbing, no
eyeballing, no drift between what you asked for and what landed.

Timecode is 25fps non-drop, so it's exact — frame 1500 is `00:01:00:00`.

---

## Chained multi-state assets — the continuity contract

One system too long or too heavy for one clip — persistent chrome (a progress rail, a shared
background) plus N states — is delivered as N butt-joined clips, each state cut to its own
transcript window. On the timeline they must read as one unbroken take. The contract:

1. **Frame counts are law.** Each state renders exactly its cue-sheet window. The chain is placed
   back-to-back with no transitions; the joins carry it.
2. **Last frame = next state's first frame.** Each state fades everything except background +
   persistent chrome over its final ~12 frames, and the next state opens from exactly that frame.
   Verify by extracting the boundary pair of every join and comparing the stills — claiming
   continuity is not checking it.
3. **Persistent chrome never re-animates.** The rail exists at full presence in every state; when
   the active segment changes, it *crossfades* (~12f) at the state start — which is
   transcript-aligned by construction, because each state starts on the word that opens it.
4. **Ambient elements run on asset-global time.** Give every state its offset from the group's
   first IN and drive phase as `f(offset + t)`, so the drifting ellipse at S1's frame 0 is exactly
   where it was at S0's last frame. Local time restarts per state; the ambience must not.
5. **Build all states from one generator.** Continuity enforced structurally survives revision
   rounds; continuity re-implemented per file breaks the first time one state is revised alone.
   A revised state keeps its exact frame count, offset, and boundary treatment — then re-verify
   **both** of its joins against the *approved* neighbours, not against its own previous version.

---

## Layered alpha

Render each element to its own transparent file. Composite in After Effects.

This is what an AE-native workflow would normally do, and it removes both limitations above:
layers can be reordered, repositioned, retimed, and used individually.

```bash
python scripts/render_frames.py --file dash.html --selector "#card"  --alpha --out layers/card/
python scripts/render_frames.py --file dash.html --selector "#title" --alpha --out layers/title/
python scripts/render_frames.py --file dash.html --layers --alpha --out layers/
```

`--layers` reads `window.__layers` — a list of selectors — and renders each one for the length of
its own slot only, not the whole timeline. Six elements at 20 frames each is 120 frames total
instead of 1500.

```js
window.__layers = ["#card", "#title", "#total", ".bar-1", ".bar-2", ".bar-3"];
```

Encode each with `--profile edit-alpha` (ProRes 4444).

### When this doesn't work

Layer separation needs elements to be visually independent. It breaks down when:

- **Shadows or glows cross element boundaries.** A card's drop shadow falls on the background, so
  capturing the card alone loses it. Fix: put the shadow on its own layer, or keep the shadowed
  group as one layer.
- **Elements overlap and share antialiasing.** Text over a gradient captured separately will have
  edge pixels matted against transparent rather than against the gradient, producing a faint halo.
  Fix: group overlapping elements into one layer.
- **`backdrop-filter` is in play.** It samples what's behind it, which doesn't exist in an isolated
  capture. Always group these with their background.

Rule of thumb: **one layer per independently-movable visual group**, not per DOM node.

---

## Working with the render in After Effects

**Interpret the footage explicitly.** File → Interpret Footage → Main, set the frame rate to what
you rendered. AE guesses from the file, and a ProRes tagged 25 landing in a 25 comp is only correct
if you set it. This is also the free slow-motion trick: render at 50, interpret at 25, and you get
half speed with every frame real.

**Time remapping.** Layer → Time → Enable Time Remapping. You get keyframes at the first and last
frame; add keyframes at the segment boundaries from `segments.csv` and drag them. Holding a value
between two keyframes freezes; the gaps compress or stretch as you move them.

**Frame blending.** If you slow a segment below 1×, turn on Frame Blending → Pixel Motion. It works
noticeably better when the source has motion blur, which is the argument for rendering with
`--subframes 4` on anything you plan to retime.

**Premiere.** Same idea via Rate Stretch or Time Remapping on the clip, but AE handles it more
precisely. If the composition is going to be retimed much, do it in AE and bring the comp across
via Dynamic Link.

---

## Choosing

Start with the slotted timeline. It's one file, one render, and time remapping covers most edits.

Move to layers when you hit either wall: you need elements in a different order than they were
authored, or you need to move one independently in space. Both are signals that the elements
aren't really one composition and shouldn't be baked into one file.
