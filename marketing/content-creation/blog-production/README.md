# Blog Production Pipeline

The full 7-step pipeline for producing publish-ready MAN Digital blog posts with graphics.

## The Flow

```
┌─────────────────────┐
│ 01 SEO Content Brief│  Build the strategic brief: target keyword, intent, competitors, structure
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 02 Blog Post Brief  │  Convert SEO brief into a writing brief (angle, hook, key takeaways)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 03 SEO Research     │  DataForSEO: keyword clusters, SERP analysis, competitor gaps
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 04 Content Research │  Deep topic research, statistics, expert sources, citations
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 05 Fact Check       │  Python-driven claim extraction + Exa verification
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 06 Write            │  Draft the post following MAN Digital structure + paragraph patterns
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 07 Graphics         │  Generate TSX-based blog graphics matching MAN Digital brand
└──────────┬──────────┘
           ▼
       Publish
```

## The Steps

| #   | Skill                                                                            | What it produces                                                                             |
| --- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 01  | [`01-seo-content-brief/`](./01-seo-content-brief/)                               | Validated SEO brief with target keyword, intent, competitor SERP map, recommended structure  |
| 02  | [`02-blog-post-brief/`](./02-blog-post-brief/)                                   | Writer-facing brief: angle, hook, takeaways, tone, internal links                            |
| 03  | [`03-blog-post-seo-research/`](./03-blog-post-seo-research/)                     | DataForSEO output: keyword clusters, SERP intent, troubleshooting guide                      |
| 04  | [`04-blog-post-content-research/`](./04-blog-post-content-research/)             | Topic deep-dive: stats, expert quotes, planning framework, competitor gap analysis           |
| 05  | [`05-blog-post-fact-checker/`](./05-blog-post-fact-checker/)                     | Fact-check report: every claim extracted + verified via Exa, with source authority hierarchy |
| 06  | [`06-blog-post-creation/`](./06-blog-post-creation/)                             | Full draft following MAN Digital structure, paragraph patterns, readability targets          |
| 07  | [`07-blog-graphics-artifact-generator/`](./07-blog-graphics-artifact-generator/) | TSX graphics (timeline, infographic, maturity model) matching MAN Digital brand              |

## Quality Gate (Separate)

**Editing happens through [`../editing-checklist/`](../editing-checklist/)**, which lives outside this pipeline because it applies to _any_ piece of writing, not just blog posts. Run it after step 06 (Write) and before publishing.

## Run the Whole Pipeline

The full pipeline is automated via OpenProse — see the production setup in MAN Digital's internal infrastructure. Each step here is the standalone skill you can also invoke individually in Claude Code.

## Inputs and Outputs

- **Input to the pipeline**: a topic + target keyword
- **Output from the pipeline**: a markdown post + graphics, ready for HubSpot CMS

## Prerequisites

- Claude Code with skills loaded
- DataForSEO MCP (for step 03)
- Exa MCP (for step 05)
- HubSpot CMS access (for publishing — outside this repo's scope)
