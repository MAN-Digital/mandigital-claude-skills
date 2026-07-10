# Gemini Pencil Learnings

These notes distill the Gemini-side MAN Digital Pencil/carousel system found on 2026-05-23. Use them when creating social graphics, carousel-derived blog visuals, or anything that should reuse the same `Playground.pen` design language.

## Sources

- `/Users/romeoman/.gemini/skills/man-digital-brand/SKILL.md`
- `/Users/romeoman/.gemini/skills/man-digital-carousel/SKILL.md`
- `/Users/romeoman/.gemini/skills/md-component-scanner/SKILL.md`
- `/Users/romeoman/.gemini/skills/md-carousel-architect/SKILL.md`
- `/Users/romeoman/.gemini/skills/md-visual-auditor/SKILL.md`
- `/Users/romeoman/.gemini/agents/man-digital-designer.md`
- `/Users/romeoman/.gemini/commands/carousel.toml`

## High-Value Rules To Preserve

- Branding was called "Religion": the design must follow exact MAN Digital color, typography, logo, spacing, and component rules.
- Cover slides use dark Medium Blue `#000FC4`, massive Montserrat title type, rich geometric decoration, and no slide number.
- Carousel covers should include two logos when the context is HubSpot-related: MAN Digital white logo plus HubSpot Elite.
- Content slides use Ghost White or white backgrounds, footer logo, and slide numbers.
- Footer component `ZadxP` is mandatory for slide 2+ in square carousel work.
- Sequential indicator `AkWtb` belongs near `y: 64`.
- Internal slide title zone is around `y: 153`.
- Footer zone is around `y: 940`.
- Use premium drop shadows and icon container boxes; do not create flat text-only slides.
- Use `get_screenshot` on finalized slides and fix alignment/brand problems before presenting.
- Avoid repeated visual components across slides in a single carousel.
- Do not use logo walls unless the slide is explicitly about clients, trust, or social proof.
- Do not use wide multi-column tables in 1:1 slides; reserve wide components for 16:9.

## Component Semantics From Gemini Brand Dictionary

| Need | Component IDs |
| --- | --- |
| Cover logo / white logo | `msD2q` |
| Slide 2+ footer | `ZadxP` |
| Sequential indicator | `AkWtb` |
| Cover trust badges | `vn2H9` |
| Premium checklist / task visual | `mPCEU`, `XHGgD`, `jjQBD` |
| Listing table | `AZsW5` |
| Icon-text grid | `Eu2yG` |
| Department hierarchy / iceberg | `nYjua`, `Lmgbx`, `Og4KA`, `TcPS3`, `hTevb`, `vtKoc`, `FJfLJ`, `KwHxx` |
| Bow-tie lifecycle | `6pVsU` |
| Funnel / conversion model | `YNSWP`, `WvQJY` |
| Metric tables / KPI boxes | `otjfC`, `1SOX3`, `iQPul` |
| Iterative delivery loop | `WllkZ`, `GK280` |
| Circular process / stakeholder flow | `urVgX`, `tsWno` |
| Social proof / testimonials | `bVLQb`, `EiUbM`, `5gAdO` |
| CTA | `n3dat`, `DyzVQ` |
| Decorative elements | `EK2xz`, `VsypW`, `wExgP`, `xOLUX`, `p4Dtt`, `GogdW` |

## What This Changes For Blog Graphics

- For blog hero graphics, keep the 16:9 cover system but import the richer Gemini cover rules when the visual is also used on LinkedIn.
- For social crops from blog posts, use Gemini safe zones and footer/indicator conventions.
- For dense blog explainers, do not force carousel font minimums; use the source frame scale. But if exporting as LinkedIn carousel, respect mobile-safe body size.
- If a graphic feels too plain, scan for Gemini decorative components and icon boxes before inventing new shapes.
- If the requested visual is a carousel, prefer the dedicated `man-digital-carousel` skill; use this blog-graphics skill when the source is a blog/article visual or when adapting a blog visual for social.
