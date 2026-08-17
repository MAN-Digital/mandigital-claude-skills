#!/usr/bin/env python3
"""Check that required Playground/carousel template nodes have component refs."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / "references" / "components"
TEMPLATE_COVERAGE = ROOT / "references" / "template-coverage.md"


def main() -> int:
    text = TEMPLATE_COVERAGE.read_text(encoding="utf-8", errors="replace")
    node_ids = sorted(set(re.findall(r"`([A-Za-z0-9]{5,6})`", text)))
    missing = [node for node in node_ids if not (COMPONENTS / f"{node}.md").exists()]

    print(f"Required template nodes checked: {len(node_ids)}")

    if missing:
        print("Missing component refs:")
        for node in missing:
            print(f"- {node}")
        return 1

    print("Required node coverage passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
