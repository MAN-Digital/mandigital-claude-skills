# gstack

External skill package by Garry Tan. Brainstorming + dev workflow toolkit for Claude Code.

**Source:** https://github.com/garrytan/gstack

## Why We Use It

Two big reasons:

1. **`/office-hours`** — YC-style founder Q&A. The best skill we've found for stress-testing product ideas, MVP scope, and go-to-market plans. Six forcing questions that expose demand reality and narrowest wedge.

2. **Dev workflow commands** — `/qa`, `/ship`, `/review`, `/codex`, `/design-review`, `/cso` (security audit). Replaces ad-hoc workflows with structured, evidence-based ones.

## Key Commands

| Command               | What it does                                                                   |
| --------------------- | ------------------------------------------------------------------------------ |
| `/office-hours`       | Brainstorm an idea, MVP, or process map (YC office hours mode)                 |
| `/plan-ceo-review`    | Strategic review: think bigger, expand scope where it creates a better product |
| `/plan-eng-review`    | Engineering review: lock in architecture before coding                         |
| `/plan-design-review` | Designer's eye review of a plan                                                |
| `/autoplan`           | Run CEO + Design + Eng reviews automatically                                   |
| `/qa`                 | Test a web app with screenshots, then fix bugs                                 |
| `/qa-only`            | Test only, no fixes (report mode)                                              |
| `/design-review`      | Visual QA on a live site, find AI slop patterns, fix in source                 |
| `/review`             | Pre-landing PR review (SQL safety, LLM trust boundaries)                       |
| `/codex`              | Independent second opinion via OpenAI Codex CLI                                |
| `/cso`                | Chief Security Officer audit (OWASP, STRIDE, secrets, supply chain)            |
| `/ship`               | Full ship workflow: test → bump → PR → push                                    |
| `/land-and-deploy`    | Merge + deploy + canary verify                                                 |
| `/canary`             | Post-deploy monitoring (console errors, perf, screenshots)                     |
| `/benchmark`          | Performance regression detection                                               |
| `/browse`             | Fast headless browser (use instead of MCP browser tools)                       |
| `/investigate`        | Systematic root-cause debugging                                                |
| `/retro`              | Weekly engineering retrospective                                               |
| `/document-release`   | Post-ship docs update + CHANGELOG                                              |
| `/careful`            | Safety guardrails for destructive commands                                     |
| `/freeze`             | Lock edits to a single directory                                               |
| `/guard`              | `/careful` + `/freeze` combined                                                |

## Install

```bash
# Follow the install instructions in the upstream repo
git clone https://github.com/garrytan/gstack
cd gstack
# Then follow the README there
```

Or check the [upstream README](https://github.com/garrytan/gstack#installation) for the latest install steps.

## How It Fits With Our Setup

- Use `/office-hours` **before** any new product work
- Use `/plan-eng-review` **after** writing a plan, before coding
- Use `/qa` and `/design-review` **during** development
- Use `/review` and `/ship` **before** merging
- Use `/canary` **after** deploying

`gstack` and [ClaudeFast](../claudefast-v5.3/) are complementary — gstack covers QA + ship workflows, ClaudeFast covers multi-agent orchestration.

## Romeo's Note

> "G Stack: I use it a lot for brainstorming. I have ideas for marketing, an MVP, a process map, or whatever else, and it also offers strong development-oriented features. G Stack is also useful for development, and it includes office hours I really like from Y Combinator."
