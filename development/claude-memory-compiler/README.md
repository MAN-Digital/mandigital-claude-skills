# claude-memory-compiler

External tool by coleam00. Compiles a persistent memory store from all your Claude work so context survives across sessions.

**Source:** https://github.com/coleam00/claude-memory-compiler

## What It Is

A one-time setup that creates a persistent memory layer for Claude Code. After installation, Claude can recall:

- Previous decisions and trade-offs you discussed
- Code patterns and conventions from past projects
- Bug fixes and their root causes
- Anything you've explicitly told it to remember

Without it, every new session starts cold. With it, Claude builds genuine continuity.

## Why We Use It

> "This GitHub repository is the Claude memory compiler. You only need to set it up once; it really helps when you work a lot with Claude by creating a memory of all your work." — Romeo

If you use Claude heavily (multiple sessions per week), the productivity gain is substantial. The cold-start tax disappears.

## When to Set It Up

**Once per machine**, ideally right after installing Claude Code. Before you accumulate any meaningful work history — otherwise you'll wish you'd done it sooner.

## Install (One Time)

1. Clone the upstream repo:

   ```bash
   git clone https://github.com/coleam00/claude-memory-compiler
   cd claude-memory-compiler
   ```

2. Follow the install instructions in the upstream README. The setup typically:
   - Configures hooks in your `~/.claude/settings.json`
   - Sets up a memory directory under `~/.claude/projects/`
   - Optionally connects to an external memory service

3. Verify by starting a new Claude Code session — it should mention loading memory context.

## After Install

Memory works automatically. Claude saves and recalls context without you doing anything. If you want to explicitly save something, just say:

> "Remember that we decided to use Bun instead of Node for this project because..."

To check what Claude remembers about a topic, ask:

> "What do you remember about our auth setup?"

## How It Fits With Our Setup

- **Foundational tool** — install before anything else in this repo
- Works alongside [ClaudeFast](../claudefast-v5.3/), [gstack](../gstack/), and [superpowers](../superpowers/)
- MAN Digital infrastructure also has a project-level memory layer (OpenClaw Mission Control) — claude-memory-compiler handles personal/local memory; Mission Control handles team-shared project memory

## Troubleshooting

If memory doesn't seem to be working:

1. Check `~/.claude/settings.json` for the memory hook configuration
2. Check `~/.claude/projects/` for memory files
3. See the upstream repo's issues page: https://github.com/coleam00/claude-memory-compiler/issues
