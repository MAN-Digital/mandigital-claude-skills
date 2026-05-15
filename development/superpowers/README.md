# superpowers

External skill package by Jesse Vincent (obra). The skill framework that underlies how Claude reads, activates, and uses skills.

**Source:** https://github.com/obra/superpowers

## What It Is

`superpowers` defines the **skill activation protocol** Claude follows:

- How `SKILL.md` files are structured (YAML frontmatter + body)
- When skills should activate (description-based matching)
- How skills compose (chaining, dependencies, references)
- The "Iron Law" that skills are non-negotiable when they apply

If you write skills for MAN Digital, you're writing them in the superpowers format.

## Why We Use It

- It's the **standard format** for Claude Code skills — using it means our skills are portable
- It establishes a discipline: invoke the skill _before_ responding, not after
- Includes meta-skills for common engineering disciplines: brainstorming, TDD, debugging, plan execution, code review, parallel agent dispatch

## Key Meta-Skills

| Skill                            | When to use                                |
| -------------------------------- | ------------------------------------------ |
| `brainstorming`                  | Before any creative or scope-defining work |
| `systematic-debugging`           | When you hit a bug or test failure         |
| `test-driven-development`        | Before writing implementation code         |
| `verification-before-completion` | Before claiming work is done               |
| `requesting-code-review`         | Before merging                             |
| `writing-plans`                  | Multi-step task — write the plan first     |
| `executing-plans`                | When following a written plan              |
| `using-git-worktrees`            | Feature work that needs isolation          |
| `dispatching-parallel-agents`    | When you have 2+ independent tasks         |
| `writing-skills`                 | When building new skills                   |

## Install

See https://github.com/obra/superpowers for current install instructions.

## How It Fits With Our Setup

Every SKILL.md in this repo follows the superpowers format. Examples:

```markdown
---
name: editing-checklist
description: Use when editing or reviewing any written content for quality...
---

# Skill body here
```

When building a new skill for MAN Digital, **read the superpowers `writing-skills` meta-skill first**. It tells you exactly how to structure the YAML frontmatter and body for maximum activation reliability.

## Related

- [`../claudefast-v5.3/`](../claudefast-v5.3/) — uses superpowers as its skill substrate
- [Contributing guide](../../CONTRIBUTING.md) — MAN Digital's skill-writing conventions on top of superpowers
