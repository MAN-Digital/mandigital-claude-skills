# Source Paths

## MAN Digital Design System

Primary brand source of truth:

`/Users/romeoman/Documents/Marketing/Design/MAN Digital Design System`

Observed Codex desktop path note: on this machine, shell/Finder operations may need the
iCloud-backed filesystem path:

`/Users/romeoman/Library/Mobile Documents/com~apple~CloudDocs/Documents/Marketing/Design/MAN Digital Design System`

Pencil MCP can still resolve the Finder-style `/Users/romeoman/Documents/...` path for
opened `.pen` documents. Shell commands such as `ls`, `cp`, `mv`, and `open` may not.
When creating or opening files from shell, check the iCloud path if the Finder-style
path appears empty.

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

Primary Pencil library file:

`/Users/romeoman/Documents/Marketing/Design/Pencil/Playground.pen`

Shell/open fallback:

`/Users/romeoman/Library/Mobile Documents/com~apple~CloudDocs/Documents/Marketing/Design/Pencil/Playground.pen`

Bundled repository reference copy:

`assets/playground/Playground.pen`

Use `Playground.pen` as the read-only component/template source by default. New prompt outputs must not be built inside this file.

When running inside this GitHub package on a machine without the local MAN Digital Pencil folder, use the bundled `assets/playground/Playground.pen` as a portable Pencil.dev reference. Prefer the live local `Playground.pen` when available because it is the newest editable library; treat the bundled file as a snapshot for component inspection and fallback context.

Per-prompt output folder:

`/Users/romeoman/Documents/Marketing/Design/Pencil/Skill Tests/`

Shell/open fallback:

`/Users/romeoman/Library/Mobile Documents/com~apple~CloudDocs/Documents/Marketing/Design/Pencil/Skill Tests/`

Every prompt/run/graphic should have its own `.pen` file in that folder unless the user explicitly provides a different new output file.

Observed note from 2026-05-22: `/Users/romeoman/Documents/Marketing/Design/Pencil/Playground.lib.pen` exists but did not expose the useful reusable component library. The important components were found in `Playground.pen`.

Current audit note from 2026-05-22: `Playground.pen` had 269 top-level nodes. Pencil marked only 12 nodes as formal `reusable: true`, but the canvas also contains many non-reusable template frames that should be treated as library components for blog/social work. See `component-index.md` and `current-playground-audit.md`.

Older Gemini carousel references may mention:

`/Users/romeoman/Documents/Design/Pencil/Playground.pen`

Treat that as stale unless the user confirms it. Prefer the Marketing path above.

## Gemini Carousel Skill

Existing skill and reference registry:

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

Additional Gemini-side sources discovered on 2026-05-23:

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
