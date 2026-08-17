# MAN Digital CMS Pages

Maintains and validates the HubSpot CMS source for `www.man.digital`, including the
Man-Digital Theme 2023 and the RevOps Service page.

## When to use it

Use `$man-digital-cms-pages` for HubL, Design Manager, theme, module, page, deployment,
render verification, or HubSpot-specific performance work on MAN Digital's website.

## Inputs and outputs

- Inputs: the requested CMS change or audit, portal `1969772`, and the canonical source
  repository.
- Outputs: validated source changes, scoped upload commands, verification evidence, and
  rollback-ready Git history.

## Setup

The skill definition lives here; website source remains canonical in
[`MAN-Digital/man-digital-cms-pages`](https://github.com/MAN-Digital/man-digital-cms-pages)
to avoid maintaining two copies.

From this skill directory, run:

```bash
scripts/ensure-source.sh
scripts/validate-source.sh
```

`ensure-source.sh` clones into `references/source/` when missing. Set
`MAN_DIGITAL_CMS_SOURCE=/absolute/path/to/checkout` to reuse another checkout.

Prerequisites: Git, Python 3, and ripgrep. HubSpot CLI access is needed only for an
explicitly authorized upload; local validation does not contact HubSpot.
