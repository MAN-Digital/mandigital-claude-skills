# ClaudeFast v5.3 — AI Development Management System

A skill system that turns Claude Code into a coordinated development team with `/team-plan`, `/build`, `/team-build`, and efficient sub-agent orchestration.

## What's in This Folder

| File                                                | Purpose                                                                                  |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `CLAUDE.md`                                         | The system prompt that defines ClaudeFast's workflow, agents, and skill activation rules |
| `justfile`                                          | Task runner commands                                                                     |
| `pdfs/ClaudeFast Code Kit v5.3 - Product Guide.pdf` | Full product documentation                                                               |
| `pdfs/ClaudeFast v5.3 - Quick Start Guide.pdf`      | Get going in 10 minutes                                                                  |
| `pdfs/What's New in ClaudeFast v5.3.pdf`            | Changes from prior version                                                               |

## Core Concepts

1. **Skills-First Workflow** — every request starts by loading relevant skills before executing
2. **Context Management** — Central AI delegates exploration to sub-agents to preserve its own context
3. **`/team-plan` → `/build` (or `/team-build`)** — the standard operating procedure for non-trivial work
4. **Routing by complexity:**
   - Trivial → execute directly
   - Moderate → direct sub-agent
   - Complex → `/team-plan` → approval → `/build`
   - Collaborative → `/team-plan` → approval → `/team-build`

## When to Use

- Multi-phase implementation work (5+ files, architectural decisions)
- Cross-domain features (frontend + backend + database)
- Anything where you'd want a planning step before coding

## When NOT to Use

- Single-file fixes
- Quick research questions
- Anything you can do in one Edit call

## Install

Copy `CLAUDE.md` into your project root (or merge with your existing CLAUDE.md). The skill activation hooks will trigger automatically when you invoke `/team-plan`, `/build`, etc.

Read the **Quick Start Guide PDF** first — 10 minutes and you're productive.

## Related

- [`../superpowers/`](../superpowers/) — the skill framework ClaudeFast builds on
- [`../gstack/`](../gstack/) — complementary workflow commands (QA, ship, review)
