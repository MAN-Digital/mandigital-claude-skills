# Development Skills & Tools

Skills and external repos for engineering, code review, and AI development workflows.

## What's Here

### Our Own Skills

| Folder                                   | What it is                                                                                                                                                                                             |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`claudefast-v5.3/`](./claudefast-v5.3/) | **ClaudeFast** — AI Development Management System with efficient sub-agents. The orchestration layer we use for `/team-plan`, `/build`, `/team-build`. Includes CLAUDE.md, justfile, and 3 PDF guides. |

### External Repos We Adopt

Three skill packages from the broader community. Each has its own README in this folder explaining what it does, when to use it, and how to install.

| Folder                                                 | Repo                                                                                  | One-liner                                                              |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [`gstack/`](./gstack/)                                 | [garrytan/gstack](https://github.com/garrytan/gstack)                                 | Brainstorming + dev workflow toolkit. `/office-hours`, `/qa`, `/ship`. |
| [`superpowers/`](./superpowers/)                       | [obra/superpowers](https://github.com/obra/superpowers)                               | The skill framework itself. How SKILL.md works.                        |
| [`claude-memory-compiler/`](./claude-memory-compiler/) | [coleam00/claude-memory-compiler](https://github.com/coleam00/claude-memory-compiler) | One-time setup for persistent Claude memory across sessions.           |

---

## When to Use What

| You want to...                                  | Use                                                   |
| ----------------------------------------------- | ----------------------------------------------------- |
| Set up persistent memory across Claude sessions | `claude-memory-compiler/` (one-time install)          |
| Brainstorm a product idea or feature            | `gstack/` — `/office-hours`                           |
| Run a code review before merging                | `gstack/` — `/review` or `/codex`                     |
| QA-test a web app with screenshots              | `gstack/` — `/qa`                                     |
| Ship code (test → bump → PR → deploy)           | `gstack/` — `/ship` + `/land-and-deploy`              |
| Orchestrate a multi-agent build                 | `claudefast-v5.3/` — `/team-plan` → `/team-build`     |
| Build a new skill                               | Read `superpowers/` first to understand the framework |
| Audit security on a codebase                    | `gstack/` — `/cso`                                    |

---

## Setup Order for a New Team Member

1. **Install Claude Code** (CLI)
2. **Install [claude-memory-compiler](./claude-memory-compiler/)** — one-time persistent memory setup
3. **Install [gstack](./gstack/)** — adds 25+ workflow slash commands
4. **Read [superpowers](./superpowers/)** — understand how the skill system works
5. **Adopt [claudefast-v5.3](./claudefast-v5.3/)** — for complex multi-agent builds

After these four, you're aligned with the rest of MAN Digital's Claude setup.
