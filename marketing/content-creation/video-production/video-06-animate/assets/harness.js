/**
 * Render contract harness.
 *
 * The contract: window.__renderAt(t) is a pure function of time in seconds.
 * Same t in, identical pixels out, always. No accumulated state, no Date.now(),
 * no timers.
 */

// ---------------------------------------------------------------- easing

const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);

const ease = {
  linear:     (t) => t,
  outQuint:   (t) => 1 - Math.pow(1 - t, 5),           // --ease-out-quint
  outCubic:   (t) => 1 - Math.pow(1 - t, 3),           // --ease-out-cubic
  inCubic:    (t) => t * t * t,
  inOutCubic: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  outBack:    (t) => 1 + 2.70158 * Math.pow(t - 1, 3) + 1.70158 * Math.pow(t - 1, 2),
};

/**
 * Progress of one animated segment at time t. Clamped at both ends, so it holds
 * its start value before `delay` and its end value after -- which is what makes
 * hold regions truly static.
 */
function at(t, delay, duration, fn = ease.outQuint) {
  return fn(clamp01((t - delay) / duration));
}

const lerp = (a, b, p) => a + (b - a) * p;
const frames = (n, fps = 25) => n / fps;

// ---------------------------------------------------------------- time parsing

/**
 * Accepts, and converts to frames:
 *   90            seconds (number)
 *   "90"          seconds
 *   "1:30"        m:ss
 *   "01:30:00"    h:mm:ss
 *   "00:01:30:00" h:mm:ss:ff  (timecode)
 *   "375f"        frames
 *   "2.5s"        seconds
 */
function parseTime(v, fps) {
  if (typeof v === "number") return Math.round(v * fps);
  const s = String(v).trim();

  if (/^\d+f$/i.test(s)) return parseInt(s, 10);
  if (/^[\d.]+s$/i.test(s)) return Math.round(parseFloat(s) * fps);
  if (/^[\d.]+$/.test(s)) return Math.round(parseFloat(s) * fps);

  const parts = s.split(":").map(Number);
  if (parts.some(isNaN)) throw new Error(`Timeline: cannot parse time "${v}"`);
  if (parts.length === 2) return Math.round((parts[0] * 60 + parts[1]) * fps);
  if (parts.length === 3) return Math.round((parts[0] * 3600 + parts[1] * 60 + parts[2]) * fps);
  if (parts.length === 4) {
    return (parts[0] * 3600 + parts[1] * 60 + parts[2]) * fps + parts[3];
  }
  throw new Error(`Timeline: cannot parse time "${v}"`);
}

function toTc(frame, fps) {
  const f = Math.round(frame);
  const pad = (n) => String(n).padStart(2, "0");
  return `${pad(Math.floor(f / (3600 * fps)))}:${pad(Math.floor(f / (60 * fps)) % 60)}:` +
         `${pad(Math.floor(f / fps) % 60)}:${pad(f % fps)}`;
}

// ---------------------------------------------------------------- timeline

/**
 * Allocates each element a non-overlapping window followed by a static hold, so
 * the edit can retime each one independently.
 *
 * Two things it is important not to confuse:
 *
 *   PACING  - when each element appears. Fully recoverable by time remapping,
 *             because remapping stretches a static hold losslessly. Render
 *             compactly and place segments in the edit.
 *
 *   SPEED   - how long one element takes to animate. NOT recoverable. Stretching
 *             20 rendered frames across 15 seconds means holding each frame ~19
 *             times (staccato) or optical-flow interpolating (mush, and any
 *             counter digits become nonsense). If a bar should take 15 seconds
 *             to fill, render 15 seconds of it.
 *
 * Pay render time for motion. Don't pay it for stillness.
 */
class Timeline {
  constructor({ fps = 25, ease: defaultEase = ease.outQuint } = {}) {
    this.fps = fps;
    this.defaultEase = defaultEase;
    this.segments = [];
    this._byName = {};
    this.compact = false;
  }

  slot(name, { at: atFrame, frames: len, hold = 0, target = null, ease: fn } = {}) {
    const seg = {
      name,
      startFrame: atFrame,
      endFrame: atFrame + len,
      holdEndFrame: atFrame + len + hold,
      targetFrame: target === null ? atFrame : target,
      start: atFrame / this.fps,
      duration: len / this.fps,
      ease: fn || this.defaultEase,
    };
    this.segments.push(seg);
    this._byName[name] = seg;
    return seg;
  }

  /**
   * Declare when each element should appear in the finished video, and how long
   * its animation takes. This is the recommended entry point when you know your
   * timestamps -- the cue list is the single source of truth, so the render
   * cannot drift from the spec.
   *
   *   Timeline.cues({
   *     fps: 25,
   *     compact: true,              // render short holds; remap in the edit
   *     cues: [
   *       { name: "rect1", at: "0:00", anim: "1s"  },
   *       { name: "rect2", at: "0:20", anim: "1s"  },
   *       { name: "rect3", at: "0:40", anim: "15s" },   // genuinely slow -> rendered slow
   *     ],
   *   });
   *
   * compact: false  -> renders the full declared timeline, holds and all. Drop it
   *                    on the timeline and it already has the right pacing.
   * compact: true   -> renders each animation at its real speed with a short hold
   *                    after. The manifest reports both where each segment sits in
   *                    the file AND where it should land in the edit, so remapping
   *                    is mechanical rather than eyeballed.
   *
   * Throws if two cues overlap -- an element still animating when the next one
   * starts breaks the hold, and therefore breaks time remapping.
   */
  static cues({ fps = 25, cues = [], compact = false, hold = 4, defaultAnim = "0.8s",
                ease: fn } = {}) {
    const tl = new Timeline({ fps, ease: fn });
    tl.compact = compact;

    const parsed = cues.map((c) => ({
      name: c.name,
      startFrame: parseTime(c.at, fps),
      animFrames: parseTime(c.anim === undefined ? defaultAnim : c.anim, fps),
      ease: c.ease,
    })).sort((a, b) => a.startFrame - b.startFrame);

    // Validate: an element still moving when the next begins has no hold between
    // them, so neither can be frozen cleanly.
    for (let i = 0; i < parsed.length - 1; i++) {
      const a = parsed[i], b = parsed[i + 1];
      const endsAt = a.startFrame + a.animFrames;
      if (endsAt > b.startFrame) {
        throw new Error(
          `Timeline.cues: "${a.name}" runs to ${toTc(endsAt, fps)} but "${b.name}" ` +
          `starts at ${toTc(b.startFrame, fps)}. Overlapping cues have no hold between ` +
          `them and cannot be time-remapped independently. Shorten "${a.name}" or move ` +
          `"${b.name}" later.`
        );
      }
    }

    let cursor = 0;
    for (let i = 0; i < parsed.length; i++) {
      const c = parsed[i];
      if (compact) {
        tl.slot(c.name, { at: cursor, frames: c.animFrames, hold, target: c.startFrame,
                          ease: c.ease });
        cursor += c.animFrames + hold;
      } else {
        const next = parsed[i + 1];
        const holdLen = next ? next.startFrame - (c.startFrame + c.animFrames) : hold;
        tl.slot(c.name, { at: c.startFrame, frames: c.animFrames, hold: holdLen,
                          target: c.startFrame, ease: c.ease });
      }
    }
    return tl;
  }

  /**
   * Even distribution when you don't have specific timestamps: each name gets
   * `frames` of animation then `hold` static frames.
   */
  static spread({ fps = 25, names = [], frames: len = 20, hold = 4, total = null, ease: fn } = {}) {
    const tl = new Timeline({ fps, ease: fn });
    let holdFrames = hold;
    if (total !== null && names.length) {
      const spare = Math.round(total * fps) - names.length * len;
      if (spare < 0) console.warn(`Timeline.spread: ${names.length}x${len}f exceeds ${total}s`);
      else holdFrames = Math.floor(spare / names.length);
    }
    let cursor = 0;
    for (const name of names) {
      tl.slot(name, { at: cursor, frames: len, hold: holdFrames });
      cursor += len + holdFrames;
    }
    return tl;
  }

  /** Eased progress 0..1 for a named slot at time t. 0 before, 1 after -- the hold. */
  p(name, t) {
    const s = this._byName[name];
    if (!s) { console.warn(`Timeline: no slot "${name}"`); return 0; }
    return at(t, s.start, s.duration, s.ease);
  }

  get duration() {
    return this.segments.length
      ? Math.max(...this.segments.map((s) => s.holdEndFrame)) / this.fps
      : 0;
  }

  /** Print the plan before rendering. Check this against your cue sheet. */
  table() {
    const rows = this.segments.map((s) => ({
      slot: s.name,
      "renders at": toTc(s.startFrame, this.fps),
      "place at": toTc(s.targetFrame, this.fps),
      anim: `${s.endFrame - s.startFrame}f`,
      hold: `${s.holdEndFrame - s.endFrame}f`,
    }));
    console.table(rows);
    console.log(`total ${this.duration.toFixed(2)}s (${Math.round(this.duration * this.fps)} frames)` +
                (this.compact ? " -- compact; use 'place at' when remapping" : ""));
    return this;
  }

  export() {
    window.__duration = this.duration;
    window.__fps = this.fps;
    window.__compact = this.compact;
    window.__segments = this.segments.map((s) => ({
      name: s.name,
      startFrame: s.startFrame,
      endFrame: s.endFrame,
      holdEndFrame: s.holdEndFrame,
      targetFrame: s.targetFrame,
    }));
    return this;
  }
}

// ---------------------------------------------------------------- contract

window.__duration = 6.0;

window.__renderAt = function (t) {
  // your animation here -- every visual value derived from `t` alone
};

// ---------------------------------------------------------------- preview

window.__preview = function (fps = 25, loop = true) {
  window.__preview.stop();
  let frame = 0;
  const total = Math.round(window.__duration * fps);
  window.__preview._id = setInterval(() => {
    window.__renderAt(frame / fps);
    frame++;
    if (frame > total) { if (loop) frame = 0; else window.__preview.stop(); }
  }, 1000 / fps);
};
window.__preview.stop = function () {
  if (window.__preview._id) clearInterval(window.__preview._id);
  window.__preview._id = null;
};
