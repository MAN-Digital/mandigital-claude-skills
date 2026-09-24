---
name: creative-campaign-director
description: Research, develop, validate, art-direct, and produce original campaign platforms from a config-driven brief. Use when the user wants a distinctive multi-execution advertising campaign, creative territories, or award-caliber brand work rather than routine template ads or isolated asset resizing.
metadata:
  short-description: Direct original, research-led campaigns
---

# Creative Campaign Director

Build an original campaign platform before producing assets. Treat “award-winning” as an ambition for strategic truth, originality, craft, and coherence—not a guaranteed outcome.

This skill coordinates responsibilities that may be performed by one agent or several: creative strategy, research, creative direction, art direction, audience testing, production, and brand review. Do not create subagents unless the user or active environment explicitly authorizes delegation.

## Start with the campaign config

Use a user-provided TOML config when available. Otherwise look for campaign.toml in the working project. If neither exists, copy assets/campaign.example.toml into the project and fill only facts supported by the brief or source material.

Run:

~~~text
python3 scripts/validate_campaign_config.py /absolute/path/to/campaign.toml
~~~

Do not silently invent missing product claims, dates, rights, brand assets, audience evidence, or approval status. Ask only for missing choices that would materially change the campaign.

Read references/config.md when creating, interpreting, or revising a config.
Read references/campaign-prd.md when turning a brief into the human-readable PRD that accompanies the config.

## Choose the operating stage

Use the config's workflow.stage and approval fields.

- discovery: research the audience, category, culture, and creative references; then develop territories.
- territory-review: present three to five coherent territories and record the human creative director's decision.
- audience-test: pressure-test shortlisted work when enabled; treat synthetic findings as directional.
- campaign-world: define the selected platform, character/casting logic, visual grammar, copy system, scenes, and channel behavior.
- prototype: create a small set of master executions and critique the campaign as a system.
- production: produce approved formats, validate invariants, and package the work.
- learning: record real performance evidence and update reusable campaign memory.

Never skip directly from a raw brief to production unless the config explicitly marks a campaign platform as already approved.

For the full stage inputs, outputs, gates, and conversation flow, read references/workflow.md.

## Research before ideation

Research must improve the creative leap, not decorate a predetermined idea.

When research is required:

1. lock current campaign facts;
2. investigate how practitioners describe the problem;
3. identify recurring workarounds, contradictions, rituals, objects, and private language;
4. study strong work inside and outside the category;
5. extract transferable principles;
6. explicitly record what must not be copied;
7. synthesize tensions before proposing executions.

If research.provider is exa, use the Exa search skill and tools when available. If Exa is explicitly required but unavailable or disconnected, tell the user rather than silently substituting generic search.

Read references/research-and-originality.md for query workstreams, source records, evidence boards, and originality rules.

## Develop campaign territories

A territory is not a moodboard, headline, or single ad. Each territory needs:

- an audience truth;
- a strategic proposition;
- a creative leap;
- a campaign platform;
- a visual and copy world;
- at least three materially different execution examples;
- a credible brand connection;
- risks and imitation checks.

Recommend one territory, preserve meaningful alternatives, and request the human creative director's selection. Do not mark a territory approved because an audience simulation preferred it.

Read references/creative-direction.md when developing territories, campaign worlds, characters, visual grammar, copy systems, or scene matrices.

## Build the campaign world after approval

Once a territory is approved, create a campaign bible that separates invariants from variables.

Typical invariants:

- strategic tension and campaign platform;
- brand codes;
- character identity or casting logic;
- tone;
- copy architecture;
- recurring visual motif;
- truth and originality constraints.

Typical variables:

- locations;
- camera angles;
- poses;
- props;
- individual headlines;
- channel-specific composition;
- aspect ratios.

Change enough variables between executions to create a campaign rather than superficial layout variants.

## Prototype before scaling

Create only enough master executions to test whether the platform sustains variation. Critique:

- strategic recognition;
- specificity and credibility;
- originality;
- visual clarity before reading the caption;
- campaign coherence;
- brand ownership;
- production feasibility.

Repair isolated defects with targeted edits. Do not regenerate a successful concept merely because of one background artifact or text error.

Read references/production-and-qa.md before image production, aspect-ratio adaptation, packaging, or final review.

## Approval gates

Observe the config-driven gates:

- fact_lock must pass before research synthesis;
- territory_approval must pass before campaign-world production;
- prototype_approval must pass before format scaling;
- production_approval must pass before external publishing or handoff that changes external state.

An approval applies only to the named gate and version. Significant changes to the platform, claims, audience, or visual world reopen the relevant gate.

## Required deliverables

Unless the config narrows the scope, maintain:

- campaign-prd.md
- campaign-facts.md
- research-evidence.md
- tension-map.md
- creative-territories.md
- decision-log.md
- campaign-bible.md
- prototype-review.md
- production-manifest.md
- campaign.toml

Use the output directory and naming pattern from the config. Preserve source links and distinguish observed evidence, inference, synthetic feedback, and human decisions.

## Worked example

Read references/revenue-context-example.md when a concrete example would help, especially for recurring characters, raw photography, scene systems, research-to-idea traceability, or ratio adaptation.

The visual reference assets are in assets/examples/revenue-context/. Use them to understand the finished system. Do not reuse their character, copy, scene, or layout in an unrelated campaign unless the user explicitly asks to extend that exact campaign.

## Boundaries

- Do not promise awards or performance.
- Do not copy a reference campaign's protected execution.
- Do not treat synthetic-audience feedback as validated market evidence.
- Do not publish, launch ads, contact people, or mutate external systems without authorization.
- Do not let image generation replace research, strategy, or human creative direction.
- Do not create routine format variants before the master creative idea is approved.
