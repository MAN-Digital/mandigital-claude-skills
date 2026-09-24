# Campaign development workflow

Read this reference for stage transitions, required artifacts, approval gates, and collaboration behavior.

## Journey

~~~mermaid
flowchart TD
    A[Brief and fact lock] --> B[Audience and category research]
    B --> C[Creative reference research]
    C --> D[Evidence and tension synthesis]
    D --> E[Develop 3–5 creative territories]
    E --> F{Human creative director}
    F -->|Reject| B
    F -->|Refine| E
    F -->|Select| G[Audience pressure test]
    G --> H{Territory still strong?}
    H -->|No| E
    H -->|Yes| I[Build campaign world]
    I --> J[Create prototypes]
    J --> K{Art direction critique}
    K -->|Revise| I
    K -->|Approve| L[Produce masters]
    L --> M[Adapt formats]
    M --> N[Quality control]
    N --> O[Launch and learn]
~~~

## Roles

Roles describe responsibilities, not mandatory separate agents.

### Human creative director

- sets ambition and risk appetite;
- challenges category sameness;
- selects or combines territories;
- owns final taste decisions;
- approves the platform and production.

### Creative strategy

- translates business facts into an audience tension;
- plans research;
- synthesizes evidence;
- develops territories;
- maintains decision traceability.

### Research

- gathers audience language and category evidence;
- finds strong adjacent-category references;
- tags source quality;
- separates evidence from inference.

### Art direction

- builds the visual world;
- defines casting, character, location, camera, props, typography, and recurring motifs;
- establishes invariants and controlled variation.

### Audience testing

- tests recognition, clarity, credibility, and objections;
- never makes the final decision;
- labels simulated evidence as directional.

### Production

- executes approved scenes;
- preserves identity, brand, and copy;
- creates format-specific recompositions;
- packages outputs.

### Brand and quality control

- verifies claims, dates, spelling, logo fidelity, rights, originality, consistency, and output dimensions.

## Stage contracts

### Discovery

Inputs:

- campaign config;
- source brief;
- brand sources;
- known evidence.

Actions:

1. create campaign-facts.md;
2. resolve contradictions and stale sources;
3. pass fact_lock;
4. plan distinct research workstreams;
5. produce research-evidence.md and tension-map.md.

Exit condition:

- facts are stable enough to support creative decisions;
- evidence is linked and tagged;
- at least one non-obvious audience tension has emerged.

### Territory review

Actions:

1. develop the configured number of territories;
2. give each a proposition, leap, world, examples, brand connection, and risks;
3. run an imitation check;
4. recommend one;
5. present trade-offs to the human.

Exit condition:

- territory_approval is approved;
- approved_territory and version are recorded;
- decision-log.md explains why.

### Audience test

Actions:

1. define segments and questions;
2. test the strategic idea, not production polish;
3. identify confusion and disbelief;
4. distinguish signal from simulated speculation;
5. recommend keep, refine, combine, or reject.

Exit condition:

- human accepts the interpretation;
- meaningful refinements are recorded;
- territory version is updated if needed.

### Campaign world

Actions:

1. write the campaign platform;
2. define invariants and variables;
3. build character or casting logic;
4. define visual, copy, prop, and channel systems;
5. produce a scene matrix;
6. choose prototypes.

Exit condition:

- campaign-bible.md is coherent;
- the platform supports at least three materially different executions;
- prototype specifications are ready.

### Prototype

Actions:

1. produce a small master set;
2. critique strategy, originality, craft, and coherence;
3. repair isolated defects;
4. compare the set, not just individual images;
5. record decisions in prototype-review.md.

Exit condition:

- prototype_approval is approved;
- identity, brand, copy, and visual grammar are stable;
- production rules are explicit.

### Production

Actions:

1. generate or build approved masters;
2. adapt formats through recomposition;
3. validate dimensions and text;
4. create production-manifest.md;
5. save final files using the config naming pattern.

Exit condition:

- every requested deliverable exists;
- all required checks pass;
- production_approval is approved for any external release.

### Learning

Actions:

1. import real performance or qualitative evidence;
2. distinguish creative signal from media and targeting effects;
3. record supported learning;
4. update campaign memory without turning one result into a universal rule.

## Conversation flow

~~~mermaid
sequenceDiagram
    participant H as Human Creative Director
    participant C as Campaign Agent
    participant R as Research
    participant S as Audience Test
    participant A as Art Direction
    participant P as Production

    H->>C: Brief, ambition, constraints
    C->>H: Fact summary and material questions
    C->>R: Audience, category, and creative research
    R->>C: Evidence, tensions, references
    C->>H: Three to five territories and recommendation
    H->>C: Select, combine, redirect, or reject
    C->>S: Pressure-test shortlisted territory
    S->>C: Directional reactions and objections
    C->>H: Refined platform and decision
    H->>C: Territory approval
    C->>A: Campaign-world brief
    A->>H: Campaign bible and prototype plan
    H->>A: Art-direction approval
    A->>P: Scene specifications
    P->>A: Prototype assets
    A->>H: Critique and recommendation
    H->>P: Prototype approval
    P->>H: Final formats and manifest
~~~

## Decision log format

For every consequential decision, record:

- date;
- stage;
- decision owner;
- options considered;
- selected option;
- evidence;
- trade-offs;
- territory or config version affected;
- gate opened or closed.

The log preserves the creative journey so later agents understand why the campaign looks the way it does.

