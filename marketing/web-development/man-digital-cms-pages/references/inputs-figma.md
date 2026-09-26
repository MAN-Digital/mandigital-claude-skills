# Figma Input Adapter

## 1. Trigger

User says "here is figma" plus the Figma skill's handoff. Nothing else triggers this path.

## 2. Required handoff (all mandatory — incomplete handoff stops here)

1. Page/section list in build order.
2. Desktop + mobile specs with Figma node IDs per section.
3. Design tokens (colors, fonts, spacing) with exact values.
4. Exported assets (files, not links) per section.
5. Interactive states (tabs, accordions, drawers) with per-state specs.

Ask for missing pieces by number. Never invent copy, tokens, states, or URLs.

## 3. Conversion

Convert the handoff to the same `INVENTORY.json` schema as the GitHub path (see `inputs-github.md` §3): sections from the section list, `tokens_file` replaced by an inline `"tokens"` object, assets from the exported files, `repo`/`branch`/`commit` set to `"figma:<file-key>"`/`"n/a"`/`"n/a"`. The theme builder downstream is identical.
