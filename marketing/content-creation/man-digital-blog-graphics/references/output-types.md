# Output Types

Use this file before choosing a template family. MAN Digital graphics are not only blog graphics.

## Routing

| Request type | Route | Notes |
| --- | --- | --- |
| LinkedIn carousel or social carousel | Use the Gemini/Codex `carousel` skill first | It already maps the carousel slide system, content planning, builder/auditor flow, and mobile text rules. Use this skill for brand and Pencil library support. |
| Single LinkedIn/social image | Use this skill | Default to 1080 x 1350 unless the user asks for square or 16:9. |
| Blog graphic / article graphic | Use this skill | Default to a website/article asset, not a slide. Use 1200 x 630 unless the prompt says inline explainer, wide hero, or a specific CMS size. |
| Blog hero / featured image | Use this skill | Default to 1200 x 630 for CMS/OG-safe article visuals. Use 1600 x 900 or 1920 x 1080 only for explicit wide website hero placement. |
| Blog inline graphic | Use this skill | Prefer 1190 x 1684 explainers or contained article-module crops when the visual explains a process, model, matrix, or workflow. |
| Open Graph image | Use this skill | Default to 1200 x 630. No slide footer, page number, proof badge, or deck chrome. |
| A4 paper / one-page PDF | Use this skill | Use vertical hierarchy, print-safe margins, restrained decoration, and larger body text than dense web diagrams. |
| Infographic / flowchart | Use this skill | Prefer architecture, process, matrix, lifecycle, and operating-model templates. |
| Slide deck graphic | Use this skill unless the user asks for a full deck | Prefer 16:9 slide families and keep title/subtitle/footer logic. |
| Web page graphic | Use this skill | Use blog hero, inline explainer, or wide 16:9 components based on placement. |

## Format Defaults

- Carousel cover/content: 1080 x 1080, 1080 x 1350, or 1920 x 1080 depending on the carousel plan.
- Blog graphic / article graphic: 1200 x 630 unless the user asks for another CMS placement.
- Blog hero / featured image: 1200 x 630 by default; 1600 x 900 or 1920 x 1080 only for explicit wide hero placements.
- Blog inline/explainer: 1190 x 1684 source frames or adapted responsive blog module dimensions; remove slide/page-number grammar.
- Open Graph: 1200 x 630.
- Slide: 1920 x 1080.
- LinkedIn single image: 1080 x 1350.
- A4 page: use print-safe margins and avoid tiny diagram labels.

## Static Image Rule

All outputs here are static images unless the user explicitly asks for an implemented responsive module. Design for the smallest real display width, not just the source canvas. A 1536 px image shown at 375 px wide scales all text, icons, and connectors down together.

For mobile-sensitive blog graphics:

- choose fewer, larger labels;
- use icons and shape hierarchy to carry secondary meaning;
- prefer a taller inline explainer when the concept needs many readable details;
- simplify one-image prompts rather than shrinking type.

## Anatomy By Type

| Type | Should include | Should avoid |
| --- | --- | --- |
| Blog graphic / article image | Topic label, article headline, one strong explanatory visual, optional MAN Digital mark, CMS-safe margins | Page numbers, "slide 01" labels, proof pills, deck footer bars, carousel progress indicators |
| Blog inline explainer | Compact title, diagram/process/matrix, short labels, user-requested/source-required caption only | Presentation footer, oversized slide headline, dense paragraph blocks |
| Open Graph | Short headline, brand mark, high-contrast visual hook, safe crop area | Small labels that fail at social preview size, slide numbers |
| Slide graphic | Slide title/subtitle, footer/page number, deck-safe hierarchy | Blog/CMS crop assumptions |

## Decision Rules

1. Match channel and ratio before narrative pattern.
2. Match narrative pattern before decoration.
3. For carousels, respect carousel-specific mobile readability and slide sequencing rules.
4. For blog graphics and A4 pages, prioritize article scan clarity over carousel-style impact.
5. For blog graphics, remove slide/deck grammar even when adapting a 16:9 source component.
6. For slide decks, preserve footer/page-number grammar unless building a standalone hero slide.
7. For blog graphics, do not add visible article-context notes, prompt rationale, section rationale, placeholder labels, or internal explanation footers. A HubSpot placeholder graphic is replacement art inserted into the article, not a self-contained slide. The article surrounding the image already provides context unless the user explicitly asks for a caption/source note or a real source citation is required.
