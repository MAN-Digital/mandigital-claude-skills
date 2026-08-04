# Source Paths

## Per-machine roots — read this first

The brand source lives on each team member's own disk. Absolute paths in the rest of this
document are written from **Diogo's machine**; on any other machine, translate the root
using this table and keep the relative structure:

| Machine | Design root | Notes |
|---|---|---|
| Diogo | `/Users/diogosa/Documents/!MAN DIGITAL/Design` | Local disk since 2026-07-10 (moved off Google Drive for Desktop — treat any old `GoogleDrive-…/Brand_Identity/Design/` reference as stale). |
| Romeo | `/Users/romeoman/Documents/Marketing/Design` | Pencil MCP resolves this path for opened `.pen` documents. Shell/Finder operations (`ls`, `cp`, `mv`, `open`) may need the iCloud-backed path instead: `/Users/romeoman/Library/Mobile Documents/com~apple~CloudDocs/Documents/Marketing/Design` — check it if the Documents path appears empty. |
| Anyone else | your copy of the `Design` folder | Locate it once, then substitute it as the root everywhere below. |

The subtree under the root is the same everywhere: `Assets/`, `MAN Digital Design System/`,
`Pencil/` (with `Playground.pen` and `Marketing Assets/`).

## Campaign & Brand Assets (logos, launch kits, decorations)

Shared asset library for real campaign work — logos, partner/product launch kits,
decorative elements, badges, client logos, and reference examples:

`/Users/diogosa/Documents/!MAN DIGITAL/Design/Assets`

Notable subfolders:

- `Logo/`, `MAN Digital White Logo.svg`, `Logo blue full.png` — MAN Digital marks.
- `Revenue Hub Launch Kit - Dropping June 16/` — HubSpot **Revenue Hub** product lockups
  (Icon / One-Line / Stacked) in Color / Cream / Orange, as PNG **and** SVG. Brand hex:
  orange `#ff4800`, cream `#f8f5ee`, near-black `#141414`; pair on a deep Revenue-Hub green
  (~`#123026`). Use the **Cream** lockup on dark backgrounds, **Color/Orange** on light.
- `Badges/`, `Client Logos/`, `Decorrative Elements/`, `Examples for AI/` — supporting assets.

**Co-brand rule:** when a request supplies a partner/product launch kit (e.g. Revenue Hub) and
asks for that look, the kit's palette and lockups **override the default MAN Digital blue** for
that asset. Co-brand by placing the MAN Digital logo as the host mark. Always honor the user's
explicit visual direction over the default brand.

**Pencil image-fill gotcha:** image-fill URLs resolve relative to the `.pen` file's folder, and
relative paths up into sibling asset folders are unreliable. For real assets, **copy the needed
PNG(s) into the same folder as the output `.pen` — whichever destination folder the user chose —
and reference them with a simple `./name.png`.** Prefer PNG over SVG for image fills (SVG fills render inconsistently).

## MAN Digital Design System

Primary brand source of truth:

`/Users/diogosa/Documents/!MAN DIGITAL/Design/MAN Digital Design System`

This folder now lives on local disk (moved off the old Google Drive for Desktop shortcut on
2026-07-10). Shell commands (`ls`, `cp`, `mv`, `open`) and Pencil MCP resolve this path
directly with no sync delay.

Read these first for meaningful design decisions:

- `README.md`
- `BRAND-GUIDELINES.md`
- `DESIGN.md`
- `colors_and_type.css`
- `ui_kits/website/README.md`

Relevant asset folders:

- `assets/` - logos, badges, client logos, HubSpot assets, decor SVGs.
- `fonts/` - Montserrat font files.
- `preview/` - rendered reference previews.
- `slides/` - slide design references.
- `ui_kits/website/` - website kit and UI primitives.
- `uploads/` - source imagery and campaign assets.

## Pencil Files

Pencil root (all Pencil files/folders live here):

`/Users/diogosa/Documents/!MAN DIGITAL/Design/Pencil`

Primary Pencil library file:

`/Users/diogosa/Documents/!MAN DIGITAL/Design/Pencil/Playground.pen`

Bundled repository reference copy:

`assets/playground/Playground.pen`

Use `Playground.pen` as the read-only component/template source by default. New prompt outputs must not be built inside this file.

When running inside this GitHub package on a machine without the local MAN Digital Pencil folder, use the bundled `assets/playground/Playground.pen` as a portable Pencil.dev reference. Prefer the live local `Playground.pen` when available because it is the newest editable library; treat the bundled file as a snapshot for component inspection and fallback context.

## Output folder — ASK, don't assume

**The destination folder is a question you put to the user at the start of every job**, not a
default you apply. Assets belong with the project they were made for; dumping everything into one
shared folder disconnects them from their project. See *Step 0* in `SKILL.md`.

Ask up front (once per session/set), propose the project folder the request implies, and let the
user confirm or type another path. Create it if it doesn't exist.

Shared fallback — **only** when the user declines to choose, and say out loud that's where it went:

`/Users/diogosa/Documents/!MAN DIGITAL/Design/Pencil/Marketing Assets/`

Every marketing asset gets its own `.pen` file in the chosen folder, with its exports and any
copied image assets beside it. Name the `.pen` and its top-level frame for the asset,
e.g. `MAN Digital - LinkedIn Event Cover - {Topic}` or `MAN Digital - YouTube Thumbnail - {Topic}`.
Do not build assets inside `Playground.pen`, and do not reuse a previous asset's file.

Video-specific overlays/graphics group under a dated subfolder of the chosen destination, e.g.
`{destination}/Video Overlays/{YYYY-MM}/`. Check for an existing dated folder for the video
project in question before creating a new one, and keep same-video assets grouped together there.

(The blog-graphics skill uses a separate `Skill Tests/` folder; keep marketing assets out of it.)

Observed note from 2026-05-22: `Playground.lib.pen` (same Pencil root) exists but did not expose the useful reusable component library. The important components were found in `Playground.pen`.

Current audit note from 2026-05-22: `Playground.pen` had 269 top-level nodes. Pencil marked only 12 nodes as formal `reusable: true`, but the canvas also contains many non-reusable template frames that should be treated as library components for blog/social work. See `component-index.md` and `current-playground-audit.md`.

Older Gemini carousel references may mention:

`/Users/romeoman/Documents/Design/Pencil/Playground.pen`

Treat that as stale unless the user confirms it. Prefer the Marketing path above.

## Gemini Carousel Skill

Existing skill and reference registry (path unverified on this machine — carried over from
an earlier author's setup; confirm with the user before relying on it):

`/Users/romeoman/.agents/skills/carousel`

Useful files:

- `SKILL.md`
- `component-registry.md`
- `brand-rules.md`
- `builder-instructions.md`
- `cover-variations.md`
- `content-architect-instructions.md`
- `auditor-instructions.md`

Use this as component memory and Pencil build discipline, but let the MAN Digital design system govern final brand decisions.

## Gemini Pencil / Carousel System

Additional Gemini-side sources discovered on 2026-05-23 (also unverified on this machine):

- `/Users/romeoman/.gemini/GEMINI.md`
- `/Users/romeoman/.gemini/commands/carousel.toml`
- `/Users/romeoman/.gemini/agents/man-digital-designer.md`
- `/Users/romeoman/.gemini/skills/man-digital-carousel/SKILL.md`
- `/Users/romeoman/.gemini/skills/man-digital-brand/SKILL.md`
- `/Users/romeoman/.gemini/skills/md-component-scanner/SKILL.md`
- `/Users/romeoman/.gemini/skills/md-carousel-architect/SKILL.md`
- `/Users/romeoman/.gemini/skills/md-visual-auditor/SKILL.md`
- `/Users/romeoman/.gemini/tasks/man-digital-carousel-skill-plan.md`
- `/Users/romeoman/.gemini/tasks/enhance-carousel-skill-plan.md`
- `/Users/romeoman/.gemini/tasks/advanced-carousel-agent-plan.md`

Read `gemini-pencil-learnings.md` for distilled lessons before creating carousel-derived or social graphics.
