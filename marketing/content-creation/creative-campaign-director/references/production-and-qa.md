# Production and Quality Assurance

Use this reference after an approved campaign platform exists. Production should preserve the creative system while adapting each execution to its channel.

## Prototype first

Create the smallest set that can prove the platform:

- one execution with the clearest recognition moment;
- one with a materially different location and camera angle;
- one that tests the edge of the copy system;
- one that proves the brand can resolve the tension without over-explaining it.

Review these as a set. Do not scale a weak prototype into every format.

## Production packet

For every scene, specify:

- approved territory and version;
- audience truth and scene purpose;
- headline, supporting copy, event facts, and CTA;
- location and environmental storytelling;
- subject identity reference and invariants;
- action, expression, wardrobe, and props;
- camera position, lens feel, crop, lighting, and finish;
- protected negative-space zones for copy and logo;
- brand assets to place exactly;
- prohibited content and known generation risks;
- master size and intended variants.

Generate one scene per call when using an image model. This improves control and prevents the model from blending unrelated scenes.

## Image-generation prompt scaffold

```text
CAMPAIGN INVARIANTS
[approved platform, visual grammar, character identity, brand constraints]

THIS SCENE
[location, action, emotional beat, problem evidence, composition]

CAMERA AND LIGHT
[viewpoint, crop, lens character, flash or light behavior, finish]

COPY-SAFE AREAS
[where visual detail should be quiet]

MUST INCLUDE
[only scene-critical objects]

MUST AVOID
[reference copying, unapproved marks, accidental text, visual clichés]

OUTPUT
[dimensions, aspect ratio, intended channel]
```

Prefer generating the photographic or illustrated base without long typeset copy. Place final typography and exact logos with a design tool when practical.

## Targeted repair

When the platform and composition work but one detail fails, edit the specific defect:

- remove unintended text, posters, marks, or extra limbs;
- correct logo placement;
- restore the approved character identity;
- simplify distracting props;
- improve copy-safe negative space;
- correct a chart or product artifact without changing the whole scene.

Do not regenerate an otherwise approved image unless the defect cannot be isolated. Record material changes in the decision log.

## Format adaptation

Treat a new aspect ratio as recomposition, not cropping.

1. Start from the approved master.
2. Preserve subject identity, scene logic, lighting, and emotional beat.
3. Rebalance the subject, headline, logo, and negative space for the new frame.
4. Preserve hierarchy at actual display size.
5. Inspect hands, faces, props, edges, and background artifacts again.

Common risks:

- a square crop destroys the environmental story;
- portrait copy becomes too small because the same text block is scaled down;
- logos move into visually noisy zones;
- different variants accidentally change the character or core scene.

## QA gates

### Strategy

- The execution expresses the approved tension and platform.
- The product or offer has a credible role.
- No unsupported claim or fabricated fact appears.

### Campaign coherence

- Invariants match the campaign bible.
- Variables create a genuinely new execution.
- The series reads as one world without becoming repetitive.

### Character and scene

- Identity, age presentation, hair, and wardrobe follow the character bible.
- Pose, anatomy, gaze, and expression are plausible.
- Props and environmental details support the message.
- No accidental text, logos, or unexplained objects remain.

### Composition and typography

- One visual focal point dominates.
- Headline, event facts, CTA, and logo have a deliberate hierarchy.
- Copy is readable at realistic screen or feed size.
- Margins, alignment, padding, and optical balance are consistent.
- Crops do not cut faces, hands, or important evidence awkwardly.

### Brand and rights

- Exact approved logo assets are used.
- Brand colors and typography follow the source of truth.
- Reference images are used for analysis, not copied into the work without rights.
- Required credits, releases, or usage restrictions are recorded.

### Output

- Dimensions and aspect ratios match the config.
- Filenames match the naming pattern.
- Master and variants are clearly related.
- Files open correctly and resolution is adequate.
- A production manifest maps each asset to its source scene and approval status.

## Prototype review record

For each prototype, record:

```markdown
- Asset:
- What works:
- Strategic or visual failure:
- Repair type: copy / targeted edit / recomposition / regenerate / reject
- Decision:
- Approver and date:
```

Production approval applies only to the reviewed version. Reopen the gate if a change alters the platform, claim, character, or visual grammar.

## Packaging

The production manifest should include:

- stable asset ID;
- filename and absolute or project-relative path;
- campaign and territory version;
- scene name;
- aspect ratio and pixel dimensions;
- copy version;
- source and derivative relationship;
- logo and identity reference used;
- QA status;
- approval status;
- rights or usage notes.

External publishing, ad activation, or handoff that changes external state requires explicit authorization and an approved production gate.

