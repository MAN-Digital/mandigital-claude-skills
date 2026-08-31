# MAN Digital — Claude Skills

This is MAN Digital's shared library of Claude skills. Everything we use to run marketing pipelines and accelerate development lives here.

If you work at MAN Digital and use Claude Code, Claude Desktop, Codex, or the API, this is your starting point.

---

## How This Repo Is Organized

The repository keeps two top-level areas. Marketing skills are split by the kind of work they support.

```text
mandigital-claude-skills/
├── marketing/
│   ├── content-creation/   ← Writing, editing, social, video, and visual content
│   ├── outreach/           ← Outbound campaign coordination, cadences, copy, and QA
│   └── web-development/    ← Website design, CMS implementation, and performance
└── development/            ← Engineering and AI-development workflows
```

| Area                                                           | What belongs there                                                                                            |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| [`marketing/content-creation/`](./marketing/content-creation/) | Blog production, editing, LinkedIn, YouTube, diagrams, graphics, marketing assets, and campaign skills        |
| [`marketing/outreach/`](./marketing/outreach/)                 | Outbound campaign coordination: the outreach-strategist skill with its cadence, copywriting, and QA subskills |
| [`marketing/web-development/`](./marketing/web-development/)   | Figma website design, HubSpot CMS development, and PSI/Web Vitals auditing                                    |
| [`development/`](./development/)                               | Engineering, code review, agent workflows, and external development toolkits                                  |

See the [marketing index](./marketing/) for the complete skill inventory.

---

## External Repos We Use

Three skill packages we don't own but depend on. Each has a README inside `development/` that explains what it is, when to use it, and how to install it.

| Repo                                                                                  | Purpose                                                                                                   |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [coleam00/claude-memory-compiler](https://github.com/coleam00/claude-memory-compiler) | Persistent memory across Claude sessions. **Set up once per project.**                                    |
| [garrytan/gstack](https://github.com/garrytan/gstack)                                 | Brainstorming + dev workflow toolkit. `/office-hours`, `/qa`, `/ship`, `/review`, `/design-consultation`. |
| [obra/superpowers](https://github.com/obra/superpowers)                               | The skill system itself—the framework that makes `SKILL.md` files work.                                   |

---

## Quick Start

1. **Pick your use case:**
   - Writing a blog post? → [`marketing/content-creation/blog-production/`](./marketing/content-creation/blog-production/)
   - Writing other content? → [`marketing/content-creation/vibe-marketing-v2/`](./marketing/content-creation/vibe-marketing-v2/)
   - Editing anything? → [`marketing/content-creation/editing-checklist/`](./marketing/content-creation/editing-checklist/)
   - Producing or repurposing a video? → [`marketing/content-creation/video-production/`](./marketing/content-creation/video-production/)
   - Designing a website page in Figma? → [`marketing/web-development/man-digital-figma-website-design/`](./marketing/web-development/man-digital-figma-website-design/)
   - Maintaining the HubSpot website? → [`marketing/web-development/man-digital-cms-pages/`](./marketing/web-development/man-digital-cms-pages/)
   - Auditing PSI, Web Vitals, SEO, or AEO? → [`marketing/web-development/auditing-web-vitals/`](./marketing/web-development/auditing-web-vitals/)
   - Setting up a development workflow? → [`development/`](./development/)

2. **Install a skill** by copying its skill folder—not the category folder—into your Claude or Codex skills directory. The skill's folder name remains unchanged.

3. **Read the skill's `SKILL.md`** for its activation rules and workflow.

For shared installations across multiple computers, follow [Multi-machine maintenance](./MAINTENANCE.md).

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Quick rules:

- Put marketing skills in either `marketing/content-creation/` or `marketing/web-development/`.
- Put engineering and AI-development skills in `development/`.
- Every skill folder must contain a `SKILL.md`.
- Use kebab-case for folder names.
- If a skill belongs in a pipeline, prefix it with `NN-` (for example, `01-` or `02-`).

---

Maintained by [@romeoman](https://github.com/romeoman) at [MAN Digital](https://www.man.digital).
