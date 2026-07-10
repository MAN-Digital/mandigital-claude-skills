#!/usr/bin/env python3
"""Validate the MAN Digital Blog Graphics component registry."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
COMPONENTS = REFERENCES / "components"

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/source-paths.md",
    "references/brand-rules.md",
    "references/pencil-workflow.md",
    "references/selection-guide.md",
    "references/component-index.md",
    "references/figma-patterns.md",
    "references/output-types.md",
    "references/template-coverage.md",
    "references/image-placeholders.md",
    "references/hubspot-post-fetch.md",
    "references/hubspot-placeholder-publish.md",
    "references/playground-candidate-roster.md",
    "references/preview-manifest.md",
    "references/current-playground-audit.md",
    "references/deep-dives.md",
    "references/gemini-pencil-learnings.md",
    "references/qa-checklist.md",
]

REQUIRED_SKILL_REFERENCES = [
    "references/source-paths.md",
    "references/brand-rules.md",
    "references/pencil-workflow.md",
    "references/selection-guide.md",
    "references/component-index.md",
    "references/figma-patterns.md",
    "references/output-types.md",
    "references/template-coverage.md",
    "references/image-placeholders.md",
    "references/hubspot-post-fetch.md",
    "references/hubspot-placeholder-publish.md",
    "references/playground-candidate-roster.md",
    "references/preview-manifest.md",
    "references/current-playground-audit.md",
    "references/deep-dives.md",
    "references/gemini-pencil-learnings.md",
    "references/qa-checklist.md",
    "scripts/check_required_nodes.py",
    "scripts/check_registry.py",
]

REQUIRED_TEXT_GATES = {
    "SKILL.md": [
        "search_all_unique_properties",
        "batch_get",
        "batch_design",
        "issues detected",
        "full-frame section-fit audit",
        "cV3XM",
        "dashboard",
        "l9vKx",
    ],
    "references/pencil-workflow.md": [
        "active editor path",
        "batch_design(filePath=...)",
        "issues detected",
        "unsupported icon names",
    ],
    "references/figma-patterns.md": [
        "Canonical Playground Reference",
        "LZkoW",
        "outcome band",
        "large dead gap",
    ],
    "references/audit-loop.md": [
        "batch_design",
        "issues detected",
        "full-frame section-fit",
        "large dead gap",
    ],
    "references/qa-checklist.md": [
        "issues detected",
        "unsupported icon names",
        "full-frame section fit",
        "batch_get",
        "cV3XM",
        "exported WebP",
        "l9vKx",
    ],
    "references/hubspot-placeholder-publish.md": [
        "data-man-graphic-number",
        "existing blog graphic figures",
        "replace only the figures",
        "l9vKx",
    ],
    "references/skill-optimization-protocol.md": [
        "Unresolved Pencil write warnings",
        "Playground `LZkoW` reference",
        "cV3XM",
        "dashboard",
        "l9vKx",
    ],
    "references/container-spacing-and-topic-coding.md": [
        "cV3XM",
        "one-word",
        "short step/card labels",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def component_links(markdown: str) -> list[str]:
    pattern = re.compile(r"`(components/[^`]+?\.md)`|\((components/[^)]+?\.md)\)")
    return [match.group(1) or match.group(2) for match in pattern.finditer(markdown)]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    for rel, required_terms in REQUIRED_TEXT_GATES.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing required text-gate file: {rel}")
            continue
        text = read_text(path)
        text_lower = text.lower()
        for term in required_terms:
            if term.lower() not in text_lower:
                errors.append(f"{rel} missing required learned gate text: {term}")

    skill = read_text(ROOT / "SKILL.md") if (ROOT / "SKILL.md").exists() else ""
    for rel in REQUIRED_SKILL_REFERENCES:
        if rel not in skill:
            errors.append(f"SKILL.md does not mention required reference: {rel}")

    if not COMPONENTS.exists():
        errors.append("missing references/components directory")
        component_files: list[Path] = []
    else:
        component_files = sorted(COMPONENTS.glob("*.md"))

    linked_components: list[tuple[Path, str]] = []
    for path in ROOT.rglob("*.md"):
        text = read_text(path)
        linked_components.extend((path, link) for link in component_links(text))

    for source, link in linked_components:
        target = REFERENCES / link
        if not target.exists():
            errors.append(f"broken component link in {source.relative_to(ROOT)}: {link}")

    for path in component_files:
        text = read_text(path)
        rel = path.relative_to(ROOT)
        words = len(text.split())

        if not re.search(r"^#\s+", text, flags=re.MULTILINE):
            errors.append(f"component missing H1 heading: {rel}")
        if not re.search(r"\bSource\b", text):
            errors.append(f"component missing Source line: {rel}")
        if words < 25:
            warnings.append(f"short component note ({words} words): {rel}")

    print(f"Registry files checked: {len(component_files)} component refs")
    print(f"Component links checked: {len(linked_components)}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        return 1

    print("Registry check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
