# MAN Digital Marketing Assets — Skill

Builds branded MAN Digital **marketing/social assets** in Pencil from user-supplied copy,
using the same Playground.pen component library and MAN Digital design system as the
`man-digital-blog-graphics` and `carousel` skills.

## What it makes

LinkedIn post images, LinkedIn event covers, LinkedIn personal/company banners, Facebook
ads, Facebook/Instagram posts, Stories/Reels, YouTube thumbnails, and Open Graph / social
share images. The user provides the copy.

## What it does NOT do

- **Carousels** → routes to the `carousel` skill.
- **Blog in-body graphics / HubSpot placement** → use `man-digital-blog-graphics`.
- **No HubSpot fetch/publish** of any kind.

## How it differs from blog-graphics

|                  | blog-graphics                                | marketing-assets                                        |
| ---------------- | -------------------------------------------- | ------------------------------------------------------- |
| Output           | blog/article graphics, OG, HubSpot placement | standalone social/marketing assets                      |
| Sizing authority | blog/OG defaults                             | `references/asset-specs.md` (exact 2026 platform specs) |
| Output folder    | `Pencil/Skill Tests/`                        | `Pencil/Marketing Assets/`                              |
| Imagery          | screenshots/placeholders                     | photo/product placeholders + "add this here" briefs     |

## Key files

- `SKILL.md` — routing, source order, startup, workflow, non-negotiables.
- `references/asset-specs.md` — **the spec authority**: canvas size, ratio, safe zones, file caps per asset.
- `references/brand-rules.md`, `pencil-workflow.md`, `editable-pencil-source.md`,
  `image-placeholders.md`, `component-index.md`, `references/components/` — shared design-system doctrine.

## Build doctrine (inherited, unchanged)

Editable Pencil sources only (never flatten), Playground component lineage required,
Montserrat/Lato, Medium Blue `#000FC4` anchor + cyan `#2DE4E6`, approved logo assets, one
`.pen` per asset, full audit loop before export.

## Inherited-reference scope note

The `references/` folder carries shared design-system doctrine copied from blog-graphics.
**Ignore any HubSpot / blog-placement / `man-graphic-placeholder` / fetch-publish instructions**
in those files — they do not apply here. `asset-specs.md` overrides any blog/OG size defaults
in inherited files.
