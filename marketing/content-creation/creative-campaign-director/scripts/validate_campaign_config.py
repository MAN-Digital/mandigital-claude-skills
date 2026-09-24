#!/usr/bin/env python3
"""Validate the core contract of a creative-campaign-director TOML config."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path
from typing import Any


REQUIRED_SECTIONS = {
    "campaign",
    "workflow",
    "research",
    "creative",
    "audience_testing",
    "brand",
    "character",
    "production",
    "deliverables",
    "guardrails",
}

REQUIRED_CAMPAIGN_FIELDS = {
    "id",
    "name",
    "objective",
    "offer",
    "audience",
    "desired_action",
    "output_directory",
}

STAGES = {
    "discovery",
    "territory-review",
    "audience-test",
    "campaign-world",
    "prototype",
    "production",
    "learning",
}

GATE_VALUES = {"pending", "approved", "rejected", "reopened", "skipped"}
RESEARCH_DEPTHS = {"quick", "standard", "advanced", "exhaustive"}
CHARACTER_STRATEGIES = {
    "none",
    "recurring-character",
    "rotating-cast",
    "object-as-character",
    "decide-after-territory",
}


def is_blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing_sections = sorted(REQUIRED_SECTIONS - data.keys())
    if missing_sections:
        errors.append("Missing sections: " + ", ".join(missing_sections))
        return errors, warnings

    campaign = data["campaign"]
    for field in sorted(REQUIRED_CAMPAIGN_FIELDS):
        if is_blank(campaign.get(field)):
            errors.append(f"campaign.{field} must be non-empty")

    workflow = data["workflow"]
    stage = workflow.get("stage")
    if stage not in STAGES:
        errors.append(
            "workflow.stage must be one of: " + ", ".join(sorted(STAGES))
        )

    for gate in (
        "fact_lock",
        "territory_approval",
        "prototype_approval",
        "production_approval",
    ):
        if workflow.get(gate) not in GATE_VALUES:
            errors.append(
                f"workflow.{gate} must be one of: "
                + ", ".join(sorted(GATE_VALUES))
            )

    if workflow.get("territory_approval") == "approved":
        if is_blank(workflow.get("approved_territory")):
            errors.append(
                "workflow.approved_territory is required when territory_approval is approved"
            )
        if is_blank(workflow.get("approved_territory_version")):
            errors.append(
                "workflow.approved_territory_version is required when territory_approval is approved"
            )

    advanced_stages = {"campaign-world", "prototype", "production", "learning"}
    if stage in advanced_stages and workflow.get("territory_approval") != "approved":
        errors.append(
            f"workflow.territory_approval must be approved before stage {stage}"
        )

    if stage in {"production", "learning"} and workflow.get(
        "prototype_approval"
    ) != "approved":
        errors.append(
            f"workflow.prototype_approval must be approved before stage {stage}"
        )

    research = data["research"]
    if research.get("depth") not in RESEARCH_DEPTHS:
        errors.append(
            "research.depth must be one of: "
            + ", ".join(sorted(RESEARCH_DEPTHS))
        )
    workstreams = research.get("workstreams")
    if research.get("enabled") and (
        not isinstance(workstreams, list) or not workstreams
    ):
        errors.append("research.workstreams must contain at least one workstream")
    minimum = research.get("minimum_workstreams")
    if research.get("enabled") and isinstance(workstreams, list):
        if not isinstance(minimum, int) or minimum < 1:
            errors.append("research.minimum_workstreams must be a positive integer")
        elif len(workstreams) < minimum:
            errors.append(
                "research.workstreams contains fewer entries than minimum_workstreams"
            )

    creative = data["creative"]
    lower = creative.get("territories_min")
    upper = creative.get("territories_max")
    if not isinstance(lower, int) or lower < 1:
        errors.append("creative.territories_min must be a positive integer")
    if not isinstance(upper, int) or upper < 1:
        errors.append("creative.territories_max must be a positive integer")
    if isinstance(lower, int) and isinstance(upper, int) and lower > upper:
        errors.append("creative.territories_min cannot exceed territories_max")
    examples = creative.get("execution_examples_per_territory")
    if not isinstance(examples, int) or examples < 2:
        warnings.append(
            "creative.execution_examples_per_territory below 2 may not prove campaign range"
        )

    audience_testing = data["audience_testing"]
    if (
        audience_testing.get("enabled")
        and audience_testing.get("method") == "synthetic"
        and audience_testing.get("directional_only") is not True
    ):
        errors.append(
            "audience_testing.directional_only must be true for synthetic testing"
        )

    character = data["character"]
    strategy = character.get("strategy")
    if strategy not in CHARACTER_STRATEGIES:
        errors.append(
            "character.strategy must be one of: "
            + ", ".join(sorted(CHARACTER_STRATEGIES))
        )
    if strategy == "recurring-character" and stage in {
        "prototype",
        "production",
        "learning",
    }:
        if is_blank(character.get("identity_reference")):
            errors.append(
                "character.identity_reference is required for recurring-character production"
            )
        invariants = character.get("identity_invariants")
        if not isinstance(invariants, list) or not invariants:
            errors.append(
                "character.identity_invariants must be non-empty for recurring-character production"
            )

    production = data["production"]
    if is_blank(production.get("master_aspect_ratio")):
        errors.append("production.master_aspect_ratio must be non-empty")
    variants = production.get("variant_aspect_ratios")
    if not isinstance(variants, list):
        errors.append("production.variant_aspect_ratios must be a list")
    if "{aspect}" not in str(production.get("naming_pattern", "")):
        warnings.append(
            "production.naming_pattern should include {aspect} to keep format variants distinct"
        )
    if production.get("generate_one_scene_per_call") is not True:
        warnings.append(
            "generate_one_scene_per_call=false can reduce control over distinct campaign scenes"
        )

    guardrails = data["guardrails"]
    for field in (
        "no_unverified_claims",
        "no_award_guarantee",
        "no_reference_copying",
        "no_external_publish_without_authorization",
        "label_synthetic_feedback",
    ):
        if guardrails.get(field) is not True:
            errors.append(f"guardrails.{field} must be true")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a creative campaign TOML configuration."
    )
    parser.add_argument("config", type=Path, help="Path to campaign.toml")
    args = parser.parse_args()

    if not args.config.is_file():
        print(f"ERROR: config file not found: {args.config}", file=sys.stderr)
        return 2

    try:
        with args.config.open("rb") as handle:
            data = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        print(f"ERROR: invalid TOML: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate(data)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(
            f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)",
            file=sys.stderr,
        )
        return 1

    print(f"OK: {args.config}")
    print(f"Stage: {data['workflow']['stage']}")
    print(
        "Gates: "
        f"fact={data['workflow']['fact_lock']}, "
        f"territory={data['workflow']['territory_approval']}, "
        f"prototype={data['workflow']['prototype_approval']}, "
        f"production={data['workflow']['production_approval']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
