# MAN Digital Revenue Leaders Interviews

Creates and validates MAN Digital Revenue Leaders Interview posts as HubSpot blog drafts. The skill preserves the approved Figma question structure, uses scoped post-level styling, enforces editorial approval states, and verifies the required SEO, Open Graph, tag, and campaign metadata.

## When to use it

Use this skill when creating, updating, or QA-checking a post in the `Revenue Leaders Interviews` series. It is specific to interview blog posts; it does not create the interview landing-page theme or replace the general blog-production workflow.

## Inputs

- Approved desktop and mobile Figma frames
- Reviewed interview answers or a clearly identified draft editorial state
- Verified guest details, portrait, company information, and LinkedIn URL
- HubSpot access for saving and reviewing the draft
- The canonical `Revenue Leaders Interviews` campaign and tag

## Outputs

- Scoped intro, article HTML, and post-specific CSS
- A complete HubSpot draft with SEO and Open Graph metadata
- Automatic association with the canonical `Revenue Leaders Interviews` campaign
- Static validation results and responsive HubSpot preview QA

## Included example

`assets/carol-chen/` contains the tested Carol Chen draft example, including the intro, article body, CSS, LinkedIn SVG, and metadata contract. Its answers and unverified guest facts are visibly marked as draft placeholders and must not be published as quotations.

## Validation

From this skill directory, run:

```bash
python3 scripts/test_validate_interview.py
python3 scripts/validate_interview.py assets/carol-chen
```

## Prerequisites

- `man-digital-design-system` for brand decisions
- `man-digital-cms-pages` for HubSpot CMS source validation and uploads
- Native Chrome access for final live preview checks when available
- Explicit authorization before creating a replacement campaign, scheduling, or publishing

Read `SKILL.md` for the complete workflow and hard gates.
