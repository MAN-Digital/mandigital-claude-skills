# Animation in HubSpot custom modules

No build step, no npm, no React at runtime. Motion/React is unavailable — everything here is CSS
plus vanilla JS. The Golden Rules and the easing values from SKILL.md carry over unchanged; the
delivery mechanism is what differs.

---

## Scope everything

Module CSS is global. A bare `.card` rule will collide with the theme or another module on the same
page, usually on a page you aren't looking at.

Namespace with the module's own id:

```css
{% require_css %}
<style>
  #module-{{ module.id }} {
    --ease-out-quint: cubic-bezier(.23, 1, .32, 1);
  }
  #module-{{ module.id }} .mn-card {
    transition: transform 200ms var(--ease-out-quint);
  }
  #module-{{ module.id }} .mn-card:hover { transform: translateY(-4px); }
</style>
{% end_require_css %}
```

Define custom properties on the module root rather than `:root`. A `:root` declaration from one
module leaks into every other module on the page and the last one loaded wins.

---

## Reduced motion inside the module

Blogs and landing pages reach a wider, less predictable audience than an app. Include this in
every module that moves:

```css
@media (prefers-reduced-motion: reduce) {
  #module-{{ module.id }} * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Scroll reveals

`IntersectionObserver`, not a scroll listener. Scroll handlers fire on the main thread at scroll
frequency and are the usual cause of janky HubSpot pages.

```html
<div id="module-{{ module.id }}">
  <div class="mn-reveal" style="--i:0">…</div>
  <div class="mn-reveal" style="--i:1">…</div>
</div>

<style>
  #module-{{ module.id }} .mn-reveal {
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 320ms var(--ease-out-quint),
                transform 320ms var(--ease-out-quint);
    transition-delay: calc(var(--i) * 70ms);
  }
  #module-{{ module.id }} .mn-reveal.is-in { opacity: 1; transform: none; }
</style>

<script>
(function () {
  var root = document.getElementById('module-{{ module.id }}');
  if (!root) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -10% 0px' });
  root.querySelectorAll('.mn-reveal').forEach(function (el) { io.observe(el); });
})();
</script>
```

`unobserve` after firing — otherwise elements re-animate on every scroll back up, which reads as a
bug. The negative `rootMargin` delays the trigger until the element is properly in view rather than
one pixel past the fold.

**Never start elements at `opacity: 0` without a fallback.** If the script fails to load, the
content is invisible and unindexable. Either accept that risk consciously or gate the initial
hidden state behind a `js-enabled` class set by the script itself.

---

## Numeric counters

```js
function countTo(el, target, durationMs) {
  var start = null;
  function step(ts) {
    if (start === null) start = ts;
    var p = Math.min((ts - start) / durationMs, 1);
    var eased = 1 - Math.pow(1 - p, 5);            // outQuint
    el.textContent = Math.round(target * eased).toLocaleString();
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
```

Set the final value in the markup and let the script animate *from* zero, so the real number is in
the DOM for crawlers and for anyone with JS disabled.

---

## Constraints worth knowing

- **Email modules**: no JS, and animation support is effectively nil. Don't.
- **`position: fixed`** behaves unpredictably inside HubSpot page sections. Use `sticky` or absolute
  positioning within a relatively-positioned module root.
- **Custom properties in HubL**: `{{ module.id }}` interpolation inside a `<style>` block works, but
  the CSS is inlined per instance. Keep the block small.
- **Drag-and-drop areas** may reorder or duplicate the module; nothing may assume a single instance
  per page. Scoping by `module.id` handles this.

---

## Rendering a module to video

A HubSpot module can be rendered with the same pipeline as anything else — it's HTML and CSS.

1. Render the module in a browser and copy the resolved HTML (DevTools → Copy → Copy outerHTML),
   or build a standalone file from the module source with the HubL interpolated by hand.
2. Inline the CSS and any images as data URIs. No external requests.
3. Convert the `IntersectionObserver` trigger to a time-based one — scrolling doesn't happen in a
   frame-stepped render. Either add the `is-in` class from `__renderAt(t)` at the right moment, or
   convert the transitions to keyframe animations with explicit delays for WAAPI scrubbing.
4. Follow the render track workflow in SKILL.md.

Point 3 is the one that catches people: a scroll-triggered reveal renders as 150 frames of nothing
because the trigger never fires.
