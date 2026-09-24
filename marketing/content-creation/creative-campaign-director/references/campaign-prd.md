# Campaign Development PRD

The campaign config is the executable control plane. The campaign PRD is the human-readable agreement about what the system should accomplish and how decisions will be made. Keep both synchronized.

Use `../assets/campaign-prd.template.md` as the starting document.

## PRD purpose

The PRD should allow a creative director, art director, researcher, producer, or future agent to understand:

- the business and audience problem;
- the verified facts and open questions;
- the standard of creative ambition;
- how research becomes a campaign platform;
- who makes each decision;
- which artifacts and gates are required;
- how originality, brand fit, and production quality are assessed;
- what the finished campaign must contain;
- how evidence and learning will improve the next campaign.

It should not prescribe the final idea before discovery. A PRD defines the problem, operating system, constraints, and success criteria; creative territories remain an output of the process.

## Relationship to the config

| PRD | Config |
|---|---|
| explains intent and rationale | controls workflow behavior |
| describes roles and conversation | records stages and gates |
| captures unknowns and decision context | stores current approved values |
| defines qualitative success | supplies validation-ready constraints |
| readable by stakeholders | readable by agents and scripts |

When they conflict, stop and resolve the difference. Do not silently treat prose as approval or overwrite an approved config value based on an older document.

## Functional requirements

The campaign-development system must:

1. ingest a structured brief and brand source of truth;
2. lock facts before turning them into creative claims;
3. research audience language, lived behavior, category conventions, culture, and strong reference work;
4. preserve source links and separate observation from inference;
5. synthesize tensions rather than simply summarize sources;
6. generate three to five campaign territories with meaningful execution range;
7. expose reference influence and complete an imitation check;
8. support human creative-director selection;
9. optionally pressure-test shortlisted territories with clearly labeled synthetic audiences;
10. define an approved campaign bible with invariants and variables;
11. prototype a small number of master executions before scaling;
12. preserve character, brand, copy, and visual invariants through production;
13. recompose rather than merely crop channel variants;
14. perform strategy, craft, rights, and technical QA;
15. require explicit approval before external publishing;
16. record real performance evidence for future learning.

## Roles and decision rights

These are responsibilities, not a requirement to create separate agents.

- **Human creative director:** owns territory selection, ambition, major tradeoffs, and production approval.
- **Creative strategist:** turns business context and research into tensions and propositions.
- **Research lead:** builds the evidence base and reference map.
- **Creative lead:** develops distinct territories and the campaign platform.
- **Art director:** defines the visual world, character system, composition, typography, and scene range.
- **Audience researcher:** designs tests and labels synthetic feedback as directional.
- **Producer:** converts the campaign bible into controlled assets and manifests.
- **Brand and rights reviewer:** protects brand correctness, truth, permissions, and originality.

One agent may perform several roles, but it must still preserve the decision boundaries.

## Conversation journey

The default conversation should follow this pattern:

```text
Agent: confirms facts, unknowns, ambition, constraints, and decision owner
Human: corrects the brief and approves the fact lock
Agent: presents evidence, tensions, reference principles, and exclusions
Human: challenges the interpretation where needed
Agent: presents 3–5 territories with examples, scores, risks, and a recommendation
Human creative director: selects, combines, rejects, or redirects territories
Agent: records the decision and develops the campaign bible
Human: approves the world and prototype scope
Agent: produces a small master set and performs a system-level critique
Human: approves, requests targeted repairs, or reopens the platform
Agent: scales approved assets, runs QA, and prepares the manifest
Human: authorizes or withholds external publishing
Agent: records real-world learning after launch
```

Questions should be concentrated at material decision points. Do not repeatedly ask about choices already established in the config.

## Success criteria

Evaluate the campaign on:

- **truth:** target practitioners recognize the tension;
- **clarity:** the idea is understood quickly without a long caption;
- **originality:** it transforms reference principles rather than copying executions;
- **brand ownership:** the brand has a credible and necessary role;
- **range:** the platform sustains multiple situations and channels;
- **coherence:** executions share recognizable invariants;
- **craft:** copy, imagery, typography, and composition hold up at real size;
- **action:** the desired next step is clear;
- **operability:** future agents can extend the system using the bible and config;
- **integrity:** claims, rights, approvals, and evidence are traceable.

Do not use “award-winning” as an acceptance criterion. It is an ambition for originality and craft, not a controllable or guaranteed result.

## Acceptance checklist

A campaign is production-ready only when:

- fact lock is approved;
- required research workstreams are complete;
- sources and inference are distinguishable;
- at least three developed territories were considered unless the config records an approved exception;
- the approved territory and version are recorded;
- the campaign bible defines invariants and variables;
- the character or casting strategy is explicit;
- the scene matrix proves execution range;
- prototypes pass strategic and craft review;
- identity, logo, and brand assets have valid sources;
- channel variants pass readability and composition QA;
- the production manifest is complete;
- external publication remains blocked until explicitly authorized.

## Learning loop

After launch, replace assumptions with evidence:

- record channel, audience, spend, reach, response, and conversion context;
- capture qualitative reactions and sales or registration feedback;
- distinguish creative signal from targeting, placement, and delivery effects;
- update the tension map only when evidence supports the change;
- preserve failed territories and why they failed;
- convert reusable principles into future memory without cloning the execution.

