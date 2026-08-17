# Auditing Web Vitals

Audits PageSpeed Insights and Lighthouse performance, accessibility, SEO, best practices,
agentic browsing, and AEO/content-extraction quality without relying on single noisy runs.

## When to use it

Use `$auditing-web-vitals` when a page feels slow, a score regresses, a client reports a
performance problem, or content needs to survive both accessibility tooling and LLM
extractors.

## Inputs and outputs

- Inputs: one or more public URLs and, preferably, a PageSpeed Insights API key.
- Outputs: repeat-measurement baselines, bottleneck diagnosis, failing audit evidence,
  verified fixes, and explicit platform constraints.

## Setup

The dependency-free Python CLI is bundled at `scripts/psi`:

```bash
scripts/psi --help
scripts/psi score https://example.com -s both -n 5 -m
```

Store the API key in `PSI_API_KEY`, `./.env`, or `~/.psi.env`. The CLI never prints the
key. Python 3 is the only runtime dependency. The original standalone package remains at
[`romeoman/psi-audit`](https://github.com/romeoman/psi-audit) and is licensed under MIT.
