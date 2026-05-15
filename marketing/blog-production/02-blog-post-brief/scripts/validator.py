#!/usr/bin/env python3
"""
Brief Validator v4 - Enhanced quality checks for content briefs
Includes: statistics deduplication, word target validation, JSON/CSV consistency
"""

import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# v4 Column specification
REQUIRED_COLUMNS = [
    'HEADINGS', 'HX', 'CONTEXT', 'VECTOR', 
    'KEYWORDS', 'N-GRAMS', 'WORD_TARGET', 'COMMENTS'
]

# Alternate column names that are acceptable
COLUMN_ALIASES = {
    'COMMENTS / MISC. INFO': 'COMMENTS',
    'MISC. INFO': 'COMMENTS',
    'COMMENTS/MISC': 'COMMENTS'
}


def normalize_columns(columns: List[str]) -> List[str]:
    """Normalize column names to standard format"""
    normalized = []
    for col in columns:
        col_upper = col.upper().strip()
        if col_upper in COLUMN_ALIASES:
            normalized.append(COLUMN_ALIASES[col_upper])
        else:
            normalized.append(col_upper)
    return normalized


def validate_csv_brief(filepath: Path) -> Tuple[bool, List[str], List[str]]:
    """
    Validate a CSV brief file with v4 8-column format
    Returns (pass/fail, list of errors, list of warnings)
    """
    errors = []
    warnings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headings = list(reader)
    except Exception as e:
        return False, [f"Cannot read CSV: {e}"], []
    
    if not headings:
        return False, ["CSV file is empty"], []
    
    # Check for required columns
    actual_columns = normalize_columns(list(headings[0].keys()))
    missing = [col for col in REQUIRED_COLUMNS if col not in actual_columns]
    
    # Special handling for WORD_TARGET (new in v4)
    if 'WORD_TARGET' in missing:
        errors.append("Missing WORD_TARGET column (required in v4). Add word targets for each section.")
    
    other_missing = [col for col in missing if col != 'WORD_TARGET']
    if other_missing:
        errors.append(f"Missing required columns: {other_missing}")
    
    # Check total heading count
    total_headings = len(headings)
    if total_headings < 8:
        errors.append(f"Too few headings ({total_headings}). Target: 8-12")
    elif total_headings > 15:
        warnings.append(f"Many headings ({total_headings}). Target: 8-15 max")
    
    # Count heading levels
    h1_count = sum(1 for h in headings if h.get('HX', '').lower() == 'h1')
    h2_count = sum(1 for h in headings if h.get('HX', '').lower() == 'h2')
    h3_count = sum(1 for h in headings if h.get('HX', '').lower() == 'h3')
    
    # Validate H1
    if h1_count != 1:
        errors.append(f"Must have exactly 1 H1 (found {h1_count})")
    
    # Check H1 has keywords
    h1 = next((h for h in headings if h.get('HX', '').lower() == 'h1'), None)
    if h1 and not h1.get('KEYWORDS', '').strip():
        errors.append("H1 must include keywords with search volume")
    
    # Check H2 count
    if h2_count < 5:
        warnings.append(f"Few H2s ({h2_count}). Target: 5-8")
    elif h2_count > 10:
        warnings.append(f"Many H2s ({h2_count}). Target: 5-8")
    
    # Track statistics assignments (v4)
    stat_ids_found = []
    stat_ids_assigned = set()
    
    # Check all headings
    total_word_target = 0
    for i, heading in enumerate(headings, 1):
        level = heading.get('HX', '').lower()
        
        if not heading.get('HEADINGS', '').strip():
            errors.append(f"Row {i}: Missing heading text")
        if not level:
            errors.append(f"Row {i}: Missing level")
        
        # Check CONTEXT length (most important!)
        context = heading.get('CONTEXT', '')
        if context:
            word_count = len(context.split())
            if level == 'h1' and word_count < 50:
                errors.append(f"H1 context too short ({word_count} words). Target: 100-150 words")
            elif level == 'h2' and word_count < 40:
                warnings.append(f"Row {i} (H2) context short ({word_count} words). Target: 75-100 words")
            
            # Check for STAT_ID references (v4)
            stat_refs = re.findall(r'STAT_\d+', context)
            stat_ids_found.extend(stat_refs)
        else:
            errors.append(f"Row {i}: Missing CONTEXT (this is the most important column!)")
        
        # Check VECTOR
        if not heading.get('VECTOR', '').strip():
            warnings.append(f"Row {i}: Missing VECTOR (thematic connection)")
        
        # Check WORD_TARGET (v4)
        word_target = heading.get('WORD_TARGET', '').strip()
        if word_target:
            try:
                # Handle range format like "200-250"
                if '-' in word_target:
                    low, high = word_target.split('-')
                    target_val = (int(low) + int(high)) // 2
                else:
                    target_val = int(word_target)
                total_word_target += target_val
            except ValueError:
                warnings.append(f"Row {i}: Invalid WORD_TARGET format '{word_target}'")
        else:
            warnings.append(f"Row {i}: Missing WORD_TARGET")
        
        # Check N-GRAMS for H1/H2
        if level in ['h1', 'h2'] and not heading.get('N-GRAMS', '').strip():
            warnings.append(f"Row {i}: Consider adding N-GRAMS for SEO")
        
        # Check COMMENTS for stat assignments (v4)
        comments = heading.get('COMMENTS', '') or heading.get('COMMENTS / MISC. INFO', '')
        if comments:
            stat_refs_comments = re.findall(r'STAT_\d+', comments)
            for stat_id in stat_refs_comments:
                stat_ids_assigned.add(stat_id)
    
    # v4: Check total word target
    if total_word_target > 0:
        if total_word_target < 1400:
            warnings.append(f"Total word target ({total_word_target}) may be too low. Target: 1500-2000")
        elif total_word_target > 2200:
            warnings.append(f"Total word target ({total_word_target}) may be too high. Target: 1500-2000")
    
    # v4: Check statistics assignments
    if stat_ids_found:
        unassigned = set(stat_ids_found) - stat_ids_assigned
        if unassigned:
            warnings.append(f"Statistics referenced but not assigned in COMMENTS: {unassigned}")
    
    # Check for question-based headings
    question_headings = sum(1 for h in headings if '?' in h.get('HEADINGS', ''))
    if question_headings < 3:
        warnings.append(f"Few question-based headings ({question_headings}). Target: 3+")
    
    return len(errors) == 0, errors, warnings


def validate_json_brief(filepath: Path) -> Tuple[bool, List[str], List[str]]:
    """
    Validate a JSON brief file matches v4 specification
    Returns (pass/fail, list of errors, list of warnings)
    """
    errors = []
    warnings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return False, [f"Cannot read JSON: {e}"], []
    
    # Check required top-level keys
    required_keys = ['meta', 'macro_context', 'heading_structure']
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required key: {key}")
    
    # v4: Check for new keys
    v4_keys = ['statistics', 'interlinking', 'exclusion_registry', 'internal_differentiation']
    for key in v4_keys:
        if key not in data:
            warnings.append(f"Missing v4 key: {key}")
    
    # Validate heading structure
    if 'heading_structure' in data:
        headings = data['heading_structure']
        
        for i, h in enumerate(headings, 1):
            # Check required fields
            if 'word_target' not in h:
                warnings.append(f"Heading {i}: Missing word_target (v4 requirement)")
            
            if 'context' not in h or not h.get('context', '').strip():
                errors.append(f"Heading {i}: Missing context")
            
            if 'vector' not in h or not h.get('vector', '').strip():
                warnings.append(f"Heading {i}: Missing vector")
    
    # v4: Validate statistics have use_in field
    if 'statistics' in data:
        for i, stat in enumerate(data['statistics'], 1):
            if 'use_in' not in stat:
                errors.append(f"Statistic {i}: Missing 'use_in' field (v4 requirement)")
            if 'id' not in stat and 'stat_id' not in stat:
                warnings.append(f"Statistic {i}: Consider adding STAT_ID for reference")
    
    # v4: Validate interlinking has avoidance notes
    if 'interlinking' in data:
        for i, link in enumerate(data['interlinking'], 1):
            if 'do_not_repeat' not in link and 'avoidance' not in link:
                warnings.append(f"Internal link {i}: Missing avoidance notes (v4 requirement)")
    
    return len(errors) == 0, errors, warnings


def validate_research_doc(filepath: Path) -> Tuple[bool, List[str], List[str]]:
    """
    Validate research documentation (v4 enhanced)
    Returns (pass/fail, list of errors, list of warnings)
    """
    errors = []
    warnings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, [f"Cannot read research doc: {e}"], []
    
    # Check for required sections
    required_sections = [
        "## Entity Architecture",
        "## Competitor Analysis", 
        "## Statistics Inventory",
        "## Content Gaps"
    ]
    
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")
    
    # v4: Check for new sections
    v4_sections = [
        "## STATISTICS EXCLUSION REGISTRY",
        "## INTERNAL ARTICLE DIFFERENTIATION"
    ]
    
    for section in v4_sections:
        # Check for various formats
        section_found = (
            section in content or 
            section.replace("## ", "### ") in content or
            section.lower().replace("## ", "## ") in content.lower()
        )
        if not section_found:
            warnings.append(f"Missing v4 section: {section}")
    
    # Check for entity documentation
    if "**Relationships:**" not in content:
        warnings.append("No entity relationships documented")
    
    # Check for statistics with sources
    if "Source:" not in content:
        errors.append("No statistics with sources found")
    
    # v4: Check for STAT_ID assignments
    if "STAT_" not in content and "use_in:" not in content.lower():
        warnings.append("No STAT_ID assignments found (v4 requirement)")
    
    # Check for competitor URLs
    if "**URL:**" not in content:
        warnings.append("No competitor URLs documented")
    
    # v4: Check for DO NOT REPEAT sections
    if "DO NOT REPEAT" not in content and "do not repeat" not in content.lower():
        warnings.append("No content avoidance notes found (v4 requirement)")
    
    return len(errors) == 0, errors, warnings


def check_csv_json_consistency(csv_path: Path, json_path: Path) -> Tuple[bool, List[str]]:
    """
    v4: Check that CSV and JSON have consistent heading structure
    """
    issues = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            csv_headings = [row.get('HEADINGS', '') for row in reader]
    except Exception as e:
        return False, [f"Cannot read CSV: {e}"]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            json_headings = [h.get('text', '') for h in data.get('heading_structure', [])]
    except Exception as e:
        return False, [f"Cannot read JSON: {e}"]
    
    # Compare headings
    if len(csv_headings) != len(json_headings):
        issues.append(f"Heading count mismatch: CSV has {len(csv_headings)}, JSON has {len(json_headings)}")
    
    for i, (csv_h, json_h) in enumerate(zip(csv_headings, json_headings), 1):
        if csv_h.strip() != json_h.strip():
            issues.append(f"Heading {i} mismatch: CSV='{csv_h[:30]}...' vs JSON='{json_h[:30]}...'")
    
    return len(issues) == 0, issues


def calculate_brief_metrics(filepath: Path) -> Dict:
    """
    Calculate metrics for a brief (v4 enhanced)
    """
    metrics = {
        "total_headings": 0,
        "h1_count": 0,
        "h2_count": 0,
        "h3_count": 0,
        "question_headings": 0,
        "estimated_words": 0,
        "total_word_target": 0,
        "stat_references": 0
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headings = list(reader)
            
        metrics["total_headings"] = len(headings)
        
        for h in headings:
            level = h.get('HX', '').lower()
            if level == 'h1':
                metrics["h1_count"] += 1
            elif level == 'h2':
                metrics["h2_count"] += 1
            elif level == 'h3':
                metrics["h3_count"] += 1
            
            if '?' in h.get('HEADINGS', ''):
                metrics["question_headings"] += 1
            
            # Count stat references
            context = h.get('CONTEXT', '')
            comments = h.get('COMMENTS', '') or h.get('COMMENTS / MISC. INFO', '')
            metrics["stat_references"] += len(re.findall(r'STAT_\d+', context + comments))
            
            # Sum word targets
            word_target = h.get('WORD_TARGET', '').strip()
            if word_target:
                try:
                    if '-' in word_target:
                        low, high = word_target.split('-')
                        metrics["total_word_target"] += (int(low) + int(high)) // 2
                    else:
                        metrics["total_word_target"] += int(word_target)
                except ValueError:
                    pass
        
        # Estimate words if no word targets
        if metrics["total_word_target"] == 0:
            metrics["estimated_words"] = (
                metrics["h1_count"] * 225 +
                metrics["h2_count"] * 250 +
                metrics["h3_count"] * 150
            )
        else:
            metrics["estimated_words"] = metrics["total_word_target"]
        
    except Exception as e:
        print(f"Error calculating metrics: {e}")
    
    return metrics


def print_validation_report(
    brief_path: Path, 
    research_path: Optional[Path] = None,
    json_path: Optional[Path] = None
):
    """
    Print a comprehensive validation report (v4)
    """
    print("=" * 60)
    print("BRIEF VALIDATION REPORT (v4)")
    print("=" * 60)
    
    # Validate CSV brief
    if brief_path.exists():
        print(f"\n📄 Validating Brief: {brief_path.name}")
        print("-" * 50)
        
        # Calculate metrics
        metrics = calculate_brief_metrics(brief_path)
        print("\n📊 Brief Metrics:")
        print(f"  • Total Headings: {metrics['total_headings']}")
        print(f"  • H1/H2/H3: {metrics['h1_count']}/{metrics['h2_count']}/{metrics['h3_count']}")
        print(f"  • Question Headings: {metrics['question_headings']}")
        print(f"  • Word Target Sum: {metrics['total_word_target']}")
        print(f"  • Stat References: {metrics['stat_references']}")
        
        # Validate
        passed, errors, warnings = validate_csv_brief(brief_path)
        
        if passed:
            print("\n✅ CSV Validation: PASSED")
        else:
            print("\n❌ CSV Validation: FAILED")
        
        if errors:
            print("\n🔴 Errors (must fix):")
            for error in errors:
                print(f"  • {error}")
        
        if warnings:
            print("\n🟡 Warnings (consider fixing):")
            for warning in warnings:
                print(f"  • {warning}")
    else:
        print(f"\n❌ Brief file not found: {brief_path}")
    
    # Validate JSON if provided
    if json_path and json_path.exists():
        print(f"\n📄 Validating JSON: {json_path.name}")
        print("-" * 50)
        
        passed, errors, warnings = validate_json_brief(json_path)
        
        if passed:
            print("✅ JSON Validation: PASSED")
        else:
            print("❌ JSON Validation: FAILED")
        
        if errors:
            print("\n🔴 Errors:")
            for error in errors:
                print(f"  • {error}")
        
        if warnings:
            print("\n🟡 Warnings:")
            for warning in warnings:
                print(f"  • {warning}")
        
        # Check consistency with CSV
        if brief_path.exists():
            print("\n🔄 CSV/JSON Consistency Check:")
            consistent, issues = check_csv_json_consistency(brief_path, json_path)
            if consistent:
                print("  ✅ CSV and JSON are consistent")
            else:
                for issue in issues:
                    print(f"  • {issue}")
    
    # Validate research doc if provided
    if research_path and research_path.exists():
        print(f"\n📄 Validating Research: {research_path.name}")
        print("-" * 50)
        
        passed, errors, warnings = validate_research_doc(research_path)
        
        if passed:
            print("✅ Research Validation: PASSED")
        else:
            print("❌ Research Validation: FAILED")
        
        if errors:
            print("\n🔴 Errors:")
            for error in errors:
                print(f"  • {error}")
        
        if warnings:
            print("\n🟡 Warnings:")
            for warning in warnings:
                print(f"  • {warning}")
    
    print("\n" + "=" * 60)
    
    # Overall recommendations
    if metrics.get("total_word_target", 0) > 0:
        wt = metrics["total_word_target"]
        if wt < 1400:
            print("⚠️ Word target sum low - article may be too short")
        elif wt > 2200:
            print("⚠️ Word target sum high - article may be too long")
        else:
            print("✅ Word target sum looks good (1500-2000 range)")
    
    if metrics.get("stat_references", 0) == 0:
        print("⚠️ No STAT_ID references found - assign statistics to headings")
    
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python validator.py <brief.csv> [research.md] [brief.json]")
        print("\nv4 Validation includes:")
        print("  • WORD_TARGET column check")
        print("  • Statistics assignment validation (STAT_ID)")
        print("  • CSV/JSON consistency check")
        print("  • Internal differentiation sections")
        print("\nExample: python validator.py buyer-intent_brief.csv buyer-intent_research.md buyer-intent_brief.json")
        sys.exit(1)
    
    brief_file = Path(sys.argv[1])
    research_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    json_file = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    
    # Auto-detect JSON file if not provided
    if not json_file:
        potential_json = brief_file.with_suffix('.json')
        if potential_json.exists():
            json_file = potential_json
    
    print_validation_report(brief_file, research_file, json_file)
