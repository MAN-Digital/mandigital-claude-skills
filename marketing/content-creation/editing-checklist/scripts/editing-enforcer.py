#!/usr/bin/env python3
"""
Editing Checklist Enforcer

This script ENFORCES systematic application of the 8-step editing process.
The AI cannot claim editing is complete without running this validation.

Usage:
    python scripts/editing-enforcer.py --original <original.txt> --edited <edited.txt> --changes <changes.json>

The changes.json file must document specific edits made for each of the 8 steps.

Purpose: Prevent surface-level editing by requiring documented proof of
systematic review for each step.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter
import difflib


class EditingEnforcer:
    """Enforces the 8-step editing checklist with validation."""

    # Step 1: Grammar patterns
    GRAMMAR_PATTERNS = {
        'comma_splice': r'\b\w+\b,\s+\b\w+\b(?:\s+\w+){3,}\.',  # Simple heuristic
        'brand_names': ['HubSpot', 'RevOps', 'SaaS', 'API'],
        'contractions': ["don't", "it's", "they're", "you're", "won't", "can't"]
    }

    # Step 2: Brevity - words that should be removed
    FILLER_WORDS = [
        'really', 'very', 'quite', 'extremely', 'absolutely', 'totally',
        'completely', 'utterly', 'truly', 'definitely', 'certainly',
        'literally', 'actually', 'basically', 'essentially', 'particularly',
        'especially', 'incredibly', 'remarkably', 'somewhat', 'rather',
        'fairly', 'pretty', 'kind of', 'sort of', 'just', 'simply', 'merely'
    ]

    WORDY_PHRASES = {
        'in order to': 'to',
        'due to the fact that': 'because',
        'at this point in time': 'now',
        'in the event that': 'if',
        'for the purpose of': 'to'
    }

    # Step 3: Clichés
    CLICHES = [
        'competitive edge', 'pain points', 'high-value', 'best-in-class',
        'game-changer', 'cutting-edge', 'bleeding-edge', 'world-class',
        'leverage', 'synergy', 'robust', 'seamless', 'streamline',
        'optimize', 'delve', 'comprehensive', 'paramount', 'landscape',
        'elevate', 'revolutionize', 'disrupt', 'touch base', 'circle back',
        'low-hanging fruit', 'move the needle', 'think outside the box'
    ]

    # Step 6: Hedging words
    HEDGING_WORDS = [
        'probably', 'possibly', 'potentially', 'might', 'could', 'may',
        'perhaps', 'maybe', 'seemingly', 'appears to be', 'tends to',
        'I think', 'I believe', 'it seems', 'in my opinion'
    ]

    # Step 7: Defensive phrases
    DEFENSIVE_PHRASES = [
        'It should be noted that', 'It is important to note that',
        'Important distinction:', 'Critical clarification:', 'Important note:',
        'Obviously', 'Clearly', 'As you can see', 'It goes without saying'
    ]

    def __init__(self, original_path: str, edited_path: str, changes_path: str):
        self.original_path = Path(original_path)
        self.edited_path = Path(edited_path)
        self.changes_path = Path(changes_path)

        # Load files
        self.original_text = self._load_file(self.original_path)
        self.edited_text = self._load_file(self.edited_path)
        self.changes = self._load_changes(self.changes_path)

        # Analysis results
        self.validation_results = {}

    def _load_file(self, path: Path) -> str:
        """Load text file."""
        try:
            return path.read_text(encoding='utf-8')
        except FileNotFoundError:
            print(f"❌ Error: File '{path}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            sys.exit(1)

    def _load_changes(self, path: Path) -> Dict:
        """Load changes documentation JSON."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: Changes file '{path}' not found.")
            print("\nThe changes.json file must document specific edits for each step.")
            print("See examples/changes-template.json for the required format.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in changes file: {e}")
            sys.exit(1)

    def validate_changes_documentation(self) -> bool:
        """Validate that changes.json documents all 8 steps."""
        required_steps = [
            'step1_grammar',
            'step2_brevity',
            'step3_cliches',
            'step4_readability',
            'step5_passive_voice',
            'step6_confidence',
            'step7_defensive_writing',
            'step8_repetition'
        ]

        missing_steps = []
        empty_steps = []

        for step in required_steps:
            if step not in self.changes:
                missing_steps.append(step)
            elif not self.changes[step].get('changes', []):
                empty_steps.append(step)

        if missing_steps:
            print(f"❌ Missing documentation for steps: {', '.join(missing_steps)}")
            return False

        if empty_steps:
            print(f"⚠️  Warning: No changes documented for: {', '.join(empty_steps)}")
            print("   If no changes were needed, explicitly state 'No changes required'")

        return True

    def step1_validate_grammar(self) -> Dict:
        """Step 1: Validate grammar improvements."""
        issues_found = []

        # Check for common grammar issues in edited text
        if re.search(r'\bHubspot\b', self.edited_text):
            issues_found.append("Brand name error: 'Hubspot' should be 'HubSpot'")

        if re.search(r'\bits\s', self.edited_text, re.IGNORECASE):
            # Check if "its" is used correctly (this is a simplified check)
            issues_found.append("Possible its/it's confusion detected")

        changes_made = len(self.changes.get('step1_grammar', {}).get('changes', []))

        return {
            'step': 'Step 1: Grammar',
            'issues_remaining': len(issues_found),
            'issues': issues_found,
            'changes_documented': changes_made,
            'status': 'pass' if len(issues_found) == 0 else 'warning'
        }

    def step2_validate_brevity(self) -> Dict:
        """Step 2: Validate brevity improvements."""
        issues_found = []

        # Count filler words in edited text
        text_lower = self.edited_text.lower()
        filler_count = sum(text_lower.count(word) for word in self.FILLER_WORDS)

        # Check for wordy phrases
        wordy_found = []
        for phrase in self.WORDY_PHRASES.keys():
            if phrase in text_lower:
                wordy_found.append(phrase)

        if filler_count > 0:
            issues_found.append(f"Found {filler_count} filler words (really, very, quite, etc.)")

        if wordy_found:
            issues_found.append(f"Wordy phrases remain: {', '.join(wordy_found[:5])}")

        # Word count reduction
        original_words = len(self.original_text.split())
        edited_words = len(self.edited_text.split())
        reduction_pct = ((original_words - edited_words) / original_words * 100) if original_words > 0 else 0

        changes_made = len(self.changes.get('step2_brevity', {}).get('changes', []))

        # Target: 20-40% reduction
        brevity_status = 'pass' if 20 <= reduction_pct <= 50 else 'warning'
        if reduction_pct < 10:
            brevity_status = 'fail'
            issues_found.append(f"Only {reduction_pct:.1f}% word reduction (target: 20-40%)")

        return {
            'step': 'Step 2: Brevity',
            'original_words': original_words,
            'edited_words': edited_words,
            'reduction_pct': reduction_pct,
            'issues_remaining': len(issues_found),
            'issues': issues_found,
            'changes_documented': changes_made,
            'status': brevity_status
        }

    def step3_validate_cliches(self) -> Dict:
        """Step 3: Validate cliché removal."""
        issues_found = []
        text_lower = self.edited_text.lower()

        cliches_remaining = []
        for cliche in self.CLICHES:
            if cliche.lower() in text_lower:
                cliches_remaining.append(cliche)

        if cliches_remaining:
            issues_found.append(f"Clichés remaining: {', '.join(cliches_remaining[:10])}")

        changes_made = len(self.changes.get('step3_cliches', {}).get('changes', []))

        return {
            'step': 'Step 3: Clichés',
            'cliches_remaining': len(cliches_remaining),
            'issues_remaining': len(issues_found),
            'issues': issues_found,
            'changes_documented': changes_made,
            'status': 'pass' if len(cliches_remaining) == 0 else 'warning'
        }

    def step4_validate_readability(self) -> Dict:
        """Step 4: Validate readability improvements."""
        issues_found = []

        # Count sentences over 25 words
        sentences = re.split(r'[.!?]+', self.edited_text)
        long_sentences = [s for s in sentences if len(s.split()) > 25]

        # Count paragraphs (simple heuristic: double newline)
        paragraphs = [p.strip() for p in self.edited_text.split('\n\n') if p.strip()]
        fat_paragraphs = []

        for para in paragraphs:
            para_sentences = re.split(r'[.!?]+', para)
            para_sentences = [s.strip() for s in para_sentences if s.strip()]
            if len(para_sentences) > 7:
                fat_paragraphs.append(len(para_sentences))

        if long_sentences:
            issues_found.append(f"{len(long_sentences)} sentences exceed 25 words")

        if fat_paragraphs:
            issues_found.append(f"{len(fat_paragraphs)} paragraphs exceed 7 sentences")

        changes_made = len(self.changes.get('step4_readability', {}).get('changes', []))

        return {
            'step': 'Step 4: Readability',
            'long_sentences': len(long_sentences),
            'fat_paragraphs': len(fat_paragraphs),
            'issues_remaining': len(issues_found),
            'issues': issues_found,
            'changes_documented': changes_made,
            'status': 'pass' if len(issues_found) == 0 else 'fail'
        }

    def step5_validate_passive_voice(self) -> Dict:
        """Step 5: Validate passive voice reduction."""
        issues_found = []

        # Simple passive voice detection
        passive_patterns = [
            r'\bis\s+\w+ed\b',
            r'\bare\s+\w+ed\b',
            r'\bwas\s+\w+ed\b',
            r'\bwere\s+\w+ed\b',
            r'\bbeen\s+\w+ed\b'
        ]

        passive_count = 0
        for pattern in passive_patterns:
            passive_count += len(re.findall(pattern, self.edited_text, re.IGNORECASE))

        if passive_count > 5:
            issues_found.append(f"~{passive_count} instances of passive voice detected")

        changes_made = len(self.changes.get('step5_passive_voice', {}).get('changes', []))

        return {
            'step': 'Step 5: Passive Voice',
            'passive_instances': passive_count,
            'issues_remaining': len(issues_found),
            'issues': issues_found,
            'changes_documented': changes_made,
            'status': 'pass' if passive_count <= 5 else 'warning'
        }

    def step6_validate_confidence(self) -> Dict:
        """Step 6: Validate hedging removal."""
        issues_found = []
        text_lower = self.edited_text.lower()

        hedging_remaining = []
        for hedge in self.HEDGING_WORDS:
            if hedge.lower() in text_lower:
                hedging_remaining.append(hedge)

        if hedging_remaining:
            issues_found.append(f"Hedging words remain: {', '.join(hedging_remaining[:10])}")

        changes_made = len(self.changes.get('step6_confidence', {}).get('changes', []))

        return {
            'step': 'Step 6: Confidence',
            'hedging_words_remaining': len(hedging_remaining),
            'issues_remaining': len(issues_found),
            'issues': issues_found,
            'changes_documented': changes_made,
            'status': 'pass' if len(hedging_remaining) == 0 else 'warning'
        }

    def step7_validate_defensive_writing(self) -> Dict:
        """Step 7: Validate defensive writing removal."""
        issues_found = []

        defensive_remaining = []
        for phrase in self.DEFENSIVE_PHRASES:
            if phrase.lower() in self.edited_text.lower():
                defensive_remaining.append(phrase)

        if defensive_remaining:
            issues_found.append(f"Defensive phrases remain: {', '.join(defensive_remaining)}")

        changes_made = len(self.changes.get('step7_defensive_writing', {}).get('changes', []))

        return {
            'step': 'Step 7: Defensive Writing',
            'defensive_phrases_remaining': len(defensive_remaining),
            'issues_remaining': len(issues_found),
            'issues': issues_found,
            'changes_documented': changes_made,
            'status': 'pass' if len(defensive_remaining) == 0 else 'warning'
        }

    def step8_validate_repetition(self) -> Dict:
        """Step 8: Validate repetition removal."""
        issues_found = []

        # Find most common words (excluding common words)
        words = re.findall(r'\b\w+\b', self.edited_text.lower())
        word_freq = Counter(words)

        # Remove very common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                     'can', 'could', 'may', 'might', 'must', 'this', 'that', 'these', 'those'}

        overused_words = []
        for word, count in word_freq.most_common(20):
            if word not in stop_words and len(word) > 3 and count > 10:
                overused_words.append(f"{word} ({count}x)")

        if overused_words:
            issues_found.append(f"Potentially overused words: {', '.join(overused_words[:5])}")

        changes_made = len(self.changes.get('step8_repetition', {}).get('changes', []))

        return {
            'step': 'Step 8: Repetition',
            'overused_words': len(overused_words),
            'issues_remaining': len(issues_found),
            'issues': issues_found,
            'changes_documented': changes_made,
            'status': 'pass' if len(overused_words) == 0 else 'warning'
        }

    def run_full_validation(self) -> Dict:
        """Run validation for all 8 steps."""
        print("\n" + "="*80)
        print("EDITING CHECKLIST ENFORCEMENT - VALIDATION REPORT")
        print("="*80 + "\n")

        # Step 0: Validate changes documentation
        print("📋 VALIDATING CHANGES DOCUMENTATION")
        print("-" * 80)
        if not self.validate_changes_documentation():
            print("\n❌ VALIDATION FAILED: Changes not properly documented")
            print("   You must document specific changes for each of the 8 steps.")
            sys.exit(1)
        print("✅ Changes documentation complete\n")

        # Run all step validations
        results = {
            'step1': self.step1_validate_grammar(),
            'step2': self.step2_validate_brevity(),
            'step3': self.step3_validate_cliches(),
            'step4': self.step4_validate_readability(),
            'step5': self.step5_validate_passive_voice(),
            'step6': self.step6_validate_confidence(),
            'step7': self.step7_validate_defensive_writing(),
            'step8': self.step8_validate_repetition()
        }

        # Print results
        for step_key, result in results.items():
            print(f"\n{result['step']}")
            print("-" * 80)
            print(f"Status: {result['status'].upper()}")
            print(f"Changes documented: {result['changes_documented']}")
            print(f"Issues remaining: {result['issues_remaining']}")

            if result['issues']:
                print("\nIssues:")
                for issue in result['issues']:
                    print(f"  ⚠️  {issue}")
            else:
                print("  ✅ No issues detected")

        # Overall summary
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)

        total_issues = sum(r['issues_remaining'] for r in results.values())
        total_changes = sum(r['changes_documented'] for r in results.values())

        failed_steps = [r['step'] for r in results.values() if r['status'] == 'fail']
        warning_steps = [r['step'] for r in results.values() if r['status'] == 'warning']

        print(f"\nTotal changes documented: {total_changes}")
        print(f"Total issues remaining: {total_issues}")
        print(f"Failed steps: {len(failed_steps)}")
        print(f"Warning steps: {len(warning_steps)}")

        if failed_steps:
            print(f"\n❌ CRITICAL FAILURES:")
            for step in failed_steps:
                print(f"   • {step}")

        if warning_steps:
            print(f"\n⚠️  WARNINGS:")
            for step in warning_steps:
                print(f"   • {step}")

        if not failed_steps and not warning_steps:
            print("\n✅ EXCELLENT: All validation checks passed!")
            print("   Systematic editing process completed successfully.")

        print("\n" + "="*80 + "\n")

        # Return overall status
        return {
            'overall_status': 'fail' if failed_steps else ('warning' if warning_steps else 'pass'),
            'total_changes': total_changes,
            'total_issues': total_issues,
            'failed_steps': failed_steps,
            'warning_steps': warning_steps,
            'results': results
        }


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Enforce systematic application of the 8-step editing checklist'
    )
    parser.add_argument('--original', required=True, help='Original text file')
    parser.add_argument('--edited', required=True, help='Edited text file')
    parser.add_argument('--changes', required=True, help='Changes documentation JSON file')

    args = parser.parse_args()

    # Run enforcement
    enforcer = EditingEnforcer(args.original, args.edited, args.changes)
    validation_results = enforcer.run_full_validation()

    # Exit with appropriate code
    if validation_results['overall_status'] == 'fail':
        print("❌ VALIDATION FAILED - Critical issues must be addressed")
        sys.exit(1)
    elif validation_results['overall_status'] == 'warning':
        print("⚠️  VALIDATION PASSED WITH WARNINGS - Review recommended")
        sys.exit(2)
    else:
        print("✅ VALIDATION PASSED - Systematic editing complete")
        sys.exit(0)


if __name__ == "__main__":
    main()
