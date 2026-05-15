#!/usr/bin/env python3
"""
Style Enforcer - Master Validation Orchestrator

Runs ALL validation scripts and produces comprehensive PASS/FAIL report.
This is the gate-keeper script that must pass before delivery.

Usage:
    python style-enforcer.py <markdown_file> <target_keyword>

Example:
    python style-enforcer.py final-draft.md "HubSpot AI agents"
"""

import subprocess
import sys
import os
from typing import Dict, List


class StyleEnforcer:
    """Master orchestrator for all validation checks."""

    def __init__(self, file_path: str, target_keyword: str):
        self.file_path = file_path
        self.target_keyword = target_keyword
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def run_all_validations(self) -> Dict[str, any]:
        """Run all validation scripts."""
        results = {
            'file': self.file_path,
            'keyword': self.target_keyword,
            'checks': {}
        }

        print("\n" + "="*80)
        print("STYLE ENFORCER - COMPREHENSIVE VALIDATION")
        print("="*80)
        print(f"\nFile: {self.file_path}")
        print(f"Target Keyword: {self.target_keyword}")
        print("\n" + "="*80 + "\n")

        # 1. Formatting Validation
        print("🎨 Running Formatting Validation...")
        print("-" * 80)
        formatting_result = self._run_script('formatting-validator.py', [self.file_path])
        results['checks']['formatting'] = {
            'passed': formatting_result['exit_code'] == 0,
            'exit_code': formatting_result['exit_code']
        }
        print()

        # 2. Readability Scoring
        print("\n📖 Running Readability Scorer...")
        print("-" * 80)
        readability_result = self._run_script('readability-scorer.py', [self.file_path])
        results['checks']['readability'] = {
            'passed': readability_result['exit_code'] == 0,
            'exit_code': readability_result['exit_code']
        }
        print()

        # 3. Paragraph Analysis
        print("\n📝 Running Paragraph Analyzer...")
        print("-" * 80)
        paragraph_result = self._run_script('paragraph-analyzer.py', [self.file_path])
        results['checks']['paragraph'] = {
            'passed': paragraph_result['exit_code'] == 0,
            'exit_code': paragraph_result['exit_code']
        }
        print()

        # 4. SEO Validation
        print("\n🔍 Running SEO Validator...")
        print("-" * 80)
        seo_result = self._run_script('seo-validation-helper.py', [self.file_path, self.target_keyword])
        results['checks']['seo'] = {
            'passed': seo_result['exit_code'] == 0,
            'exit_code': seo_result['exit_code']
        }
        print()

        # Calculate overall result
        all_passed = all(check['passed'] for check in results['checks'].values())
        results['overall_passed'] = all_passed

        return results

    def _run_script(self, script_name: str, args: List[str]) -> Dict[str, any]:
        """Run a validation script and capture results."""
        script_path = os.path.join(self.script_dir, script_name)

        if not os.path.exists(script_path):
            print(f"❌ Error: Script not found: {script_path}")
            return {'exit_code': 1, 'output': '', 'error': 'Script not found'}

        try:
            # Run the script
            cmd = ['python3', script_path] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            # Print output (the script's own report)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)

            return {
                'exit_code': result.returncode,
                'output': result.stdout,
                'error': result.stderr
            }

        except subprocess.TimeoutExpired:
            print(f"❌ Error: Script timed out: {script_name}")
            return {'exit_code': 1, 'output': '', 'error': 'Timeout'}
        except Exception as e:
            print(f"❌ Error running script {script_name}: {e}")
            return {'exit_code': 1, 'output': '', 'error': str(e)}

    def print_final_report(self, results: Dict[str, any]) -> None:
        """Print final comprehensive report."""
        print("\n" + "="*80)
        print("FINAL COMPREHENSIVE REPORT")
        print("="*80 + "\n")

        # Check Results
        print("📋 VALIDATION CHECK RESULTS")
        print("-" * 80)

        checks = results['checks']

        formatting_icon = "✅" if checks['formatting']['passed'] else "❌"
        readability_icon = "✅" if checks['readability']['passed'] else "❌"
        paragraph_icon = "✅" if checks['paragraph']['passed'] else "❌"
        seo_icon = "✅" if checks['seo']['passed'] else "❌"

        print(f"{formatting_icon} Formatting Validation: {'PASSED' if checks['formatting']['passed'] else 'FAILED'}")
        print(f"{readability_icon} Readability Score: {'PASSED' if checks['readability']['passed'] else 'FAILED'}")
        print(f"{paragraph_icon} Paragraph Analysis: {'PASSED' if checks['paragraph']['passed'] else 'FAILED'}")
        print(f"{seo_icon} SEO Validation: {'PASSED' if checks['seo']['passed'] else 'FAILED'}")

        print()

        # Overall Status
        passed_count = sum(1 for check in checks.values() if check['passed'])
        total_count = len(checks)

        print("="*80)
        print("OVERALL STATUS")
        print("="*80)
        print(f"Checks Passed: {passed_count}/{total_count}")
        print()

        if results['overall_passed']:
            print("🎉 SUCCESS: ALL VALIDATIONS PASSED")
            print()
            print("✅ Blog post is ready for delivery!")
            print("✅ Formatting: Excellent variety and scannability")
            print("✅ Readability: Accessible to non-native English speakers")
            print("✅ Paragraphs: Well-structured and varied")
            print("✅ SEO: Optimized for target keyword")
        else:
            print("❌ VALIDATION FAILED")
            print()
            print("🚫 Blog post is NOT ready for delivery.")
            print()
            print("Failed checks:")
            if not checks['formatting']['passed']:
                print("  ❌ Formatting - Review formatting validation report above")
            if not checks['readability']['passed']:
                print("  ❌ Readability - Review readability score report above")
            if not checks['paragraph']['passed']:
                print("  ❌ Paragraphs - Review paragraph analysis report above")
            if not checks['seo']['passed']:
                print("  ❌ SEO - Review SEO validation report above")
            print()
            print("📝 ACTION REQUIRED:")
            print("   1. Review each failed check's detailed report above")
            print("   2. Make the recommended fixes")
            print("   3. Re-run this validator: python style-enforcer.py <file> <keyword>")
            print("   4. Repeat until all checks pass")

        print("="*80 + "\n")


def main():
    """Main function."""
    if len(sys.argv) < 3:
        print("="*80)
        print("STYLE ENFORCER - Master Validation Orchestrator")
        print("="*80)
        print()
        print("Usage: python style-enforcer.py <markdown_file> <target_keyword>")
        print()
        print("Example:")
        print('  python style-enforcer.py final-draft.md "HubSpot AI agents"')
        print()
        print("This script runs ALL validation checks:")
        print("  • Formatting Validation (variety, bullets, visuals, tables)")
        print("  • Readability Score (Flesch-Kincaid, non-native speaker focus)")
        print("  • Paragraph Analysis (structure, variety, fat paragraphs)")
        print("  • SEO Validation (keywords, headings, meta elements)")
        print()
        print("ALL checks must PASS before blog post is ready for delivery.")
        print("="*80)
        sys.exit(1)

    file_path = sys.argv[1]
    target_keyword = sys.argv[2]

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found.")
        sys.exit(1)

    # Run all validations
    enforcer = StyleEnforcer(file_path, target_keyword)
    results = enforcer.run_all_validations()

    # Print final report
    enforcer.print_final_report(results)

    # Exit with error code if any validation failed
    if not results['overall_passed']:
        sys.exit(1)


if __name__ == "__main__":
    main()
