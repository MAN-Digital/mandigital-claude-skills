# MAN Digital — Claude Skills

This is MAN Digital's shared library of Claude skills. Everything we use to run marketing pipelines and accelerate development, in one place.

If you work at MAN Digital and use Claude (Code, Desktop, or the API), this is your starting point.

---

## How This Repo Is Organized

Two top-level folders. That's it.

```
mandigital-claude-skills/
├── marketing/      ← Skills for content, SEO, copy, social
└── development/    ← Skills and tools for engineering work
```

### marketing/

Everything related to producing content for MAN Digital.

| Folder                                                           | What it is                                                                                           |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| [`blog-production/`](./marketing/blog-production/)               | The full 7-step blog pipeline (brief → research → fact-check → write → graphics → publish)           |
| [`editing-checklist/`](./marketing/editing-checklist/)           | Standalone editorial quality framework — use on any piece of writing                                 |
| [`vibe-marketing-v2/`](./marketing/vibe-marketing-v2/)           | 11-skill marketing suite (brand voice, positioning, lead magnets, email, newsletter, creative, etc.) |
| [`linkedin-post-creation/`](./marketing/linkedin-post-creation/) | LinkedIn post writing skill                                                                          |

### development/

Skills and external tools for engineering and AI development workflows.

| Folder                                                             | What it is                                                              |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| [`claudefast-v5.3/`](./development/claudefast-v5.3/)               | ClaudeFast — AI development management system with efficient sub-agents |
| [`gstack/`](./development/gstack/)                                 | External: brainstorming, YC office hours, QA, ship workflow             |
| [`superpowers/`](./development/superpowers/)                       | External: the skill framework Claude uses (how SKILL.md works)          |
| [`claude-memory-compiler/`](./development/claude-memory-compiler/) | External: one-time setup for persistent Claude memory                   |

---

## External Repos We Use

Three skill packages we don't own but depend on. Each has a README inside `development/` that explains what it is, when to use it, and how to install.

| Repo                                                                                  | Purpose                                                                                                   |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [coleam00/claude-memory-compiler](https://github.com/coleam00/claude-memory-compiler) | Persistent memory across Claude sessions. **Set up once per project.**                                    |
| [garrytan/gstack](https://github.com/garrytan/gstack)                                 | Brainstorming + dev workflow toolkit. `/office-hours`, `/qa`, `/ship`, `/review`, `/design-consultation`. |
| [obra/superpowers](https://github.com/obra/superpowers)                               | The skill system itself — the framework that makes SKILL.md files work.                                   |

---

## Quick Start

1. **Pick your use case:**
   - Writing a blog post? → [`marketing/blog-production/`](./marketing/blog-production/)
   - Writing other content (LinkedIn, email, landing page)? → [`marketing/vibe-marketing-v2/`](./marketing/vibe-marketing-v2/)
   - Editing anything? → [`marketing/editing-checklist/`](./marketing/editing-checklist/)
   - Setting up your dev environment? → [`development/`](./development/)

2. **Install a skill** by copying its folder into your Claude Code skills directory (or symlinking it). Each skill folder contains a `SKILL.md` that Claude reads to activate it.

3. **Read the folder README** before using a skill — it explains scope, inputs, and outputs.

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Quick rules:

- New skills go into `marketing/` or `development/` only — no new top-level folders
- Every skill folder must have a `SKILL.md` (the Claude-readable spec) and a `README.md` (for humans)
- Use kebab-case for folder names
- If a skill belongs in a pipeline, prefix it with `NN-` (e.g. `01-`, `02-`)

---

Maintained by [@romeoman](https://github.com/romeoman) at [MAN Digital](https://www.man.digital).
