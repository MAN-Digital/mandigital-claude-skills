# Contributing to MAN Digital Claude Skills

## Adding a New Skill

1. **Decide where it goes.** Two folders, no exceptions:
   - `marketing/` — content, SEO, copy, social, ads
   - `development/` — engineering, code review, devops, AI tooling

2. **Folder structure.** Every skill needs at minimum:

   ```
   your-skill-name/
   ├── SKILL.md          ← Required. The Claude-readable skill spec.
   ├── README.md         ← Required. Human-readable explanation.
   ├── references/       ← Optional. Supporting docs.
   ├── scripts/          ← Optional. Python/JS helpers.
   └── examples/         ← Optional. Sample inputs/outputs.
   ```

3. **Naming.**
   - Use `kebab-case` for folder names (`blog-post-creation`, not `BlogPostCreation`)
   - If it's part of a sequential pipeline, prefix with a number (`01-`, `02-`, etc.)

4. **SKILL.md format.** Follow the [superpowers](https://github.com/obra/superpowers) convention:

   ```markdown
   ---
   name: skill-name
   description: One sentence on when this skill activates.
   ---

   # Skill content here
   ```

5. **README.md should answer:**
   - What does this skill do?
   - When should I use it?
   - What inputs does it need?
   - What does it produce?
   - Any prerequisites (API keys, MCP tools, other skills)?

## Updating an Existing Skill

- Bump the version in the SKILL.md frontmatter if you change behavior
- Note breaking changes at the top of the README
- Update the parent folder's README if you change the skill's scope

## Adding a New External Repo Reference

If you find another skill repo worth adopting at MAN Digital:

1. Add a folder under `development/` (or `marketing/` if applicable) with the repo name in kebab-case
2. Inside, a single `README.md` explaining: what it is, when to use, install steps, link to source
3. Update the top-level `README.md`'s "External Repos We Use" table

## What Not to Do

- Don't create new top-level folders. Two is the rule.
- Don't commit zip files. Always extract first.
- Don't commit secrets, API keys, or `.env` files.
- Don't add a skill without a README — others on the team need to know when to use it.
