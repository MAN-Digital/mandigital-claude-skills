# Creative Campaign Director

Research, develop, art-direct, and produce an original campaign platform from a config-driven brief. Use this skill for coherent multi-execution campaigns, not routine template ads or isolated asset resizing.

## Inputs

- A campaign brief with the offer, audience, objective, and desired action.
- A `campaign.toml`, or the included [example config](./assets/campaign.example.toml) populated with verified facts.
- Approved brand references, product claims, assets, and human decisions at each approval gate.

## Workflow and Outputs

The workflow moves through discovery, territory review, audience testing when enabled, campaign-world development, prototypes, production, and learning. Human approval is required before advancing through the relevant gates.

Outputs include the campaign PRD, fact sheet, research evidence, tension map, creative territories, decision log, campaign bible, prototype review, production manifest, and approved assets. See [SKILL.md](./SKILL.md) for the full operating instructions.

## Prerequisites

- Python 3.11 or newer for the TOML validator; no third-party Python dependencies.
- A connected Exa app and its search skill when the config requires Exa research.
- Appropriate image-generation or design tools for the chosen production stage.

Validate a config from this skill directory:

```bash
python3 scripts/validate_campaign_config.py assets/campaign.example.toml
```

## Install

From the repository root, copy the complete folder into your local skills directory:

```bash
cp -R marketing/content-creation/creative-campaign-director ~/.codex/skills/
```

The [Revenue Context example](./references/revenue-context-example.md) includes a config, production manifest, logo, and eight visual examples. These demonstrate a campaign system; they are not templates to copy into unrelated campaigns. Synthetic audience feedback is directional, and the skill does not guarantee awards or performance or authorize external publishing.
