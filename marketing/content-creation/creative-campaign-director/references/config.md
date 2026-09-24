# Campaign configuration

Read this reference when creating or changing campaign.toml.

## Why the config exists

The config holds campaign decisions and gates outside prompts. Prompts may evolve; the approved facts, territory, constraints, outputs, and production rules remain inspectable.

The config is not the creative brief itself. It is a control plane for the workflow.

## Required sections

### campaign

Defines the assignment and output location.

Required non-empty fields:

- id
- name
- objective
- offer
- audience
- desired_action
- output_directory

Use status for overall project state, not individual gate approval.

### workflow

Valid stages:

- discovery
- territory-review
- audience-test
- campaign-world
- prototype
- production
- learning

Valid gate values:

- pending
- approved
- rejected
- reopened
- skipped

Set skipped only when the human explicitly removes a gate from scope. Do not infer approval from silence or from an agent recommendation.

If territory_approval is approved, approved_territory and approved_territory_version must be present.

### research

Valid depth values:

- quick
- standard
- advanced
- exhaustive

Advanced is the default for a new campaign platform. Quick is suitable only for a narrow extension of an already approved platform.

If provider is exa and allow_provider_fallback is false, do not silently use another provider.

Workstreams must describe different search territories, not synonym variations.

### creative

The ambition field controls the evaluation standard, not a promised result.

Each territory must have enough execution examples to prove it can become a campaign. Three is the default minimum.

The reference policy must preserve the distinction between principles and protected executions.

### audience_testing

Synthetic testing is optional. When method is synthetic:

- directional_only must remain true;
- results must name the simulated segment;
- the human interprets the evidence;
- the simulation cannot approve a campaign.

Real interviews, survey results, or performance data should be tagged separately.

### brand

source_of_truth may be a local directory, design-system URL, Figma file, or brand document.

logo_paths should point to approved assets. Do not ask an image model to invent the logo when an asset exists.

Separate mandatory and prohibited elements.

### character

Common strategies:

- none
- recurring-character
- rotating-cast
- object-as-character
- decide-after-territory

When using recurring-character, identity_reference and identity_invariants are required before production.

### production

Prototype-first means:

1. produce a few master executions;
2. critique the platform;
3. obtain prototype approval;
4. scale formats.

Do not treat aspect-ratio adaptation as resizing. A variant may require recomposition while preserving strategic and visual invariants.

### deliverables

Boolean fields control which artifacts are required. A false field narrows output; it does not remove the reasoning or approval needed to work safely.

### guardrails

Keep these explicit so campaign work cannot drift toward fabricated claims, imitation, or unauthorized publishing.

## Config lifecycle

1. Create config from supported facts.
2. Run the validator.
3. Resolve errors before advancing.
4. Update stage and gates only after the corresponding decision.
5. Record meaningful changes in decision-log.md.
6. Re-run validation before prototype and production.

## Project-specific extension

Additional sections are allowed, including channels, markets, languages, legal, media, performance, or rights. The validator ignores unknown sections while still validating the core workflow.
