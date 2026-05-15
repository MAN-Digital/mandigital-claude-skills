#!/usr/bin/env python3
"""
Formatting Validator Script (v1.1 - Fixed Sentence Counting)

Validates blog post formatting requirements for scannability and readability.
Ensures content matches the variety and structure requirements.

Version 1.1 Changes:
- Fixed sentence counting to avoid false positives from:
  * Decimal numbers (3.5x, v2.0)
  * Abbreviations (U.S., Dr., Inc.)
  * URLs/domains (example.com)
  * Statistics with decimals (45.7%)

Usage:
    python formatting-validator-fixed.py <markdown_file>

Example:
    python formatting-validator-fixed.py draft.md
"""

import re
import sys
from typing import Dict, List, Tuple
from collections import Counter


class FormattingValidator:
    """Validates formatting requirements for blog posts."""

    def __init__(self, content: str):
        self.content = content
        self.lines = content.split('\n')
        self.paragraphs = self._extract_paragraphs()

    def _count_sentences_smart(self, text: str) -> int:
        """
        Count sentences intelligently, avoiding false splits.

        Protects against:
        - Decimal numbers: 3.5, 2.0, v1.2
        - Abbreviations: U.S., Dr., Inc., Corp., Ltd.
        - URLs/domains: example.com, site.org
        - Percentages with decimals: 45.7%
        """
        # Work on a copy to protect original
        protected = text

        # Protect decimal numbers: 3.5, 2.0, v1.2, etc.
        protected = re.sub(r'\b\d+\.\d+', lambda m: m.group().replace('.', '<!NUM!>'), protected)

        # Protect version numbers: v2.0, version 1.5
        protected = re.sub(r'\bv\d+\.\d+', lambda m: m.group().replace('.', '<!VER!>'), protected, flags=re.I)

        # Protect abbreviations with multiple periods: U.S., A.I.
        protected = re.sub(r'\b([A-Z]\.)+', lambda m: m.group().replace('.', '<!ABB!>'), protected)

        # Protect common title abbreviations: Dr., Mr., Mrs., Ms., Prof.
        protected = re.sub(
            r'\b(Dr|Mr|Mrs|Ms|Prof|Inc|Corp|Ltd|Co|Sr|Jr)\.\s',
            lambda m: m.group().replace('.', '<!TITLE!>'),
            protected
        )

        # Protect URLs/domains: example.com, site.org, etc.
        protected = re.sub(
            r'\b\w+\.(com|org|net|edu|gov|io|co|ai|uk|us)\b',
            lambda m: m.group().replace('.', '<!URL!>'),
            protected,
            flags=re.I
        )

        # Protect percentages with decimals: 45.7%
        protected = re.sub(r'\d+\.\d+%', lambda m: m.group().replace('.', '<!PCT!>'), protected)

        # Now split on actual sentence boundaries:
        # - Period, exclamation, or question mark
        # - Followed by space and capital letter, OR end of string
        # This avoids splitting on periods in the middle of words
        sentences = re.split(r'[.!?]+(?=\s+[A-Z]|$)', protected)
        sentences = [s.strip() for s in sentences if s.strip()]

        return len(sentences)

    def _extract_paragraphs(self) -> List[str]:
        """Extract paragraphs from content (non-heading, non-empty lines)."""
        paragraphs = []
        current_para = []

        for line in self.lines:
            # Skip headings, bullets, tables, visual placeholders
            if (line.startswith('#') or
                line.strip().startswith(('*', '-', '|', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or
                line.strip().startswith('[') and line.strip().endswith(']') or
                line.strip() == ''):

                # Save accumulated paragraph
                if current_para:
                    paragraphs.append(' '.join(current_para))
                    current_para = []
                continue

            current_para.append(line.strip())

        # Add last paragraph
        if current_para:
            paragraphs.append(' '.join(current_para))

        return paragraphs

    def validate_all(self) -> Dict[str, any]:
        """Run all validation checks."""
        return {
            'paragraph_variety': self.validate_paragraph_variety(),
            'bullet_sections': self.validate_bullet_sections(),
            'visual_placeholders': self.validate_visual_placeholders(),
            'tables': self.validate_tables(),
            'bold_headers': self.validate_bold_headers(),
            'sub_bullets': self.validate_sub_bullets(),
            'fat_paragraphs': self.detect_fat_paragraphs(),
            'variety_score': self.calculate_variety_score()
        }

    def validate_paragraph_variety(self) -> Dict[str, any]:
        """Validate paragraph length variety (1, 2, 3 sentences)."""
        sentence_counts = []

        for para in self.paragraphs:
            # Use smart sentence counting (FIXED)
            count = self._count_sentences_smart(para)
            sentence_counts.append(count)

        # Count distribution
        one_sent = sentence_counts.count(1)
        two_sent = sentence_counts.count(2)
        three_sent = sentence_counts.count(3)
        four_plus = sum(1 for count in sentence_counts if count >= 4)

        total_paragraphs = len(sentence_counts)

        # Calculate percentages
        one_pct = (one_sent / total_paragraphs * 100) if total_paragraphs > 0 else 0
        two_pct = (two_sent / total_paragraphs * 100) if total_paragraphs > 0 else 0
        three_pct = (three_sent / total_paragraphs * 100) if total_paragraphs > 0 else 0
        four_plus_pct = (four_plus / total_paragraphs * 100) if total_paragraphs > 0 else 0

        # Targets: 10-15 one-sent, 20-25 two-sent, 5-10 three-sent, 0 four+
        targets = {
            'one_sentence': (10, 15),
            'two_sentence': (20, 25),
            'three_sentence': (5, 10),
            'four_plus': (0, 0)
        }

        # Check if distribution is good
        variety_good = (
            10 <= one_sent <= 20 and  # More flexible
            15 <= two_sent <= 30 and
            3 <= three_sent <= 15 and
            four_plus == 0
        )

        status = 'pass' if variety_good and four_plus == 0 else 'fail'

        issues = []
        if four_plus > 0:
            issues.append(f"❌ CRITICAL: {four_plus} paragraphs have 4+ sentences (auto-reject)")
        if not (10 <= one_sent <= 20):
            issues.append(f"⚠️ One-sentence paragraphs: {one_sent} (need 10-15 for variety)")
        if not (15 <= two_sent <= 30):
            issues.append(f"⚠️ Two-sentence paragraphs: {two_sent} (need 20-25 for balance)")
        if not (3 <= three_sent <= 15):
            issues.append(f"⚠️ Three-sentence paragraphs: {three_sent} (need 5-10 maximum)")

        return {
            'total_paragraphs': total_paragraphs,
            'distribution': {
                'one_sentence': {'count': one_sent, 'percentage': round(one_pct, 1)},
                'two_sentence': {'count': two_sent, 'percentage': round(two_pct, 1)},
                'three_sentence': {'count': three_sent, 'percentage': round(three_pct, 1)},
                'four_plus': {'count': four_plus, 'percentage': round(four_plus_pct, 1)}
            },
            'status': status,
            'issues': issues,
            'message': "✅ Paragraph variety is excellent!" if variety_good and four_plus == 0 else "❌ Paragraph variety needs improvement"
        }

    def validate_bullet_sections(self) -> Dict[str, any]:
        """Validate bullet section count (minimum 8-12)."""
        # Count bullet sections (groups of consecutive bullet lines)
        bullet_sections = 0
        in_bullet_section = False

        for line in self.lines:
            is_bullet = bool(re.match(r'^[\s]*[-*][\s]', line)) or bool(re.match(r'^[\s]*\d+\.[\s]', line))

            if is_bullet and not in_bullet_section:
                bullet_sections += 1
                in_bullet_section = True
            elif not is_bullet:
                in_bullet_section = False

        status = 'pass' if bullet_sections >= 8 else 'fail'

        return {
            'count': bullet_sections,
            'minimum': 8,
            'optimal': 12,
            'status': status,
            'message': f"✅ {bullet_sections} bullet sections (excellent!)" if bullet_sections >= 8 else f"❌ Only {bullet_sections} bullet sections (need minimum 8)"
        }

    def validate_visual_placeholders(self) -> Dict[str, any]:
        """Validate visual placeholder count (minimum 2-4)."""
        # Find placeholders like [Screenshot: ...], [Diagram: ...], etc.
        visual_pattern = r'\[(Screenshot|Diagram|Chart|Infographic|Image|Visual|Figure|Table|Graphic)[:\s]'
        visuals = re.findall(visual_pattern, self.content, re.I)
        count = len(visuals)

        status = 'pass' if 2 <= count <= 6 else 'fail'

        return {
            'count': count,
            'minimum': 2,
            'optimal': 4,
            'types': Counter(visuals),
            'status': status,
            'message': f"✅ {count} visual placeholders (good!)" if count >= 2 else f"❌ Only {count} visual placeholders (need minimum 2-4)"
        }

    def validate_tables(self) -> Dict[str, any]:
        """Validate table count (recommended 1-2)."""
        # Count markdown tables (lines with pipes)
        table_lines = [line for line in self.lines if '|' in line and line.strip().startswith('|')]

        # Estimate table count (every table has at least 3 lines: header + separator + data)
        table_count = len(table_lines) // 3

        status = 'pass' if table_count >= 1 else 'warning'

        return {
            'count': table_count,
            'recommended': '1-2',
            'status': status,
            'message': f"✅ {table_count} table(s) found" if table_count >= 1 else "⚠️ No tables found (recommended: 1-2 for data comparisons)"
        }

    def validate_bold_headers(self) -> Dict[str, any]:
        """Validate bold header count (minimum 8-12)."""
        # Find bold text that looks like headers (short, standalone)
        bold_pattern = r'\*\*([^*]+)\*\*'
        bold_matches = re.findall(bold_pattern, self.content)

        # Filter for header-like bold (short phrases, often at line start)
        bold_headers = [b for b in bold_matches if len(b) < 80 and not b.strip().endswith('.')]
        count = len(bold_headers)

        status = 'pass' if count >= 8 else 'fail'

        return {
            'count': count,
            'minimum': 8,
            'optimal': 12,
            'headers': bold_headers[:10],  # Show first 10
            'status': status,
            'message': f"✅ {count} bold headers (great!)" if count >= 8 else f"❌ Only {count} bold headers (need minimum 8-12)"
        }

    def validate_sub_bullets(self) -> Dict[str, any]:
        """Validate sub-bullet usage (minimum 3-5 instances)."""
        # Look for indented bullets (nested lists)
        sub_bullet_pattern = r'^[\s]{2,}[-*][\s]'
        sub_bullets = [line for line in self.lines if re.match(sub_bullet_pattern, line)]

        # Count sections with sub-bullets
        sections_with_sub = 0
        has_sub_bullet = False

        for line in self.lines:
            is_sub = bool(re.match(sub_bullet_pattern, line))
            is_main = bool(re.match(r'^[-*][\s]', line.strip()))

            if is_sub and not has_sub_bullet:
                sections_with_sub += 1
                has_sub_bullet = True
            elif is_main and not is_sub:
                has_sub_bullet = False

        status = 'pass' if sections_with_sub >= 3 else 'fail'

        return {
            'count': sections_with_sub,
            'minimum': 3,
            'optimal': 5,
            'total_sub_bullets': len(sub_bullets),
            'status': status,
            'message': f"✅ {sections_with_sub} sections with sub-bullets" if sections_with_sub >= 3 else f"❌ Only {sections_with_sub} sections with sub-bullets (need 3-5)"
        }

    def detect_fat_paragraphs(self) -> Dict[str, any]:
        """Detect paragraphs with 4+ sentences (auto-reject)."""
        fat_paragraphs = []

        for i, para in enumerate(self.paragraphs, 1):
            # Use smart sentence counting (FIXED)
            count = self._count_sentences_smart(para)

            if count >= 4:
                preview = para[:100] + '...' if len(para) > 100 else para
                fat_paragraphs.append({
                    'paragraph_num': i,
                    'sentence_count': count,
                    'preview': preview,
                    'full_text': para  # Include full text for debugging
                })

        status = 'pass' if len(fat_paragraphs) == 0 else 'fail'

        return {
            'count': len(fat_paragraphs),
            'fat_paragraphs': fat_paragraphs,
            'status': status,
            'message': "✅ No fat paragraphs (all 3 sentences or less)" if status == 'pass' else f"❌ CRITICAL: {len(fat_paragraphs)} paragraphs have 4+ sentences (MUST break up)"
        }

    def calculate_variety_score(self) -> Dict[str, any]:
        """Calculate overall variety score (0-100)."""
        scores = {
            'paragraph_variety': 0,
            'bullets': 0,
            'visuals': 0,
            'tables': 0,
            'bold_headers': 0,
            'sub_bullets': 0,
            'no_fat_paragraphs': 0
        }

        # Paragraph variety (30 points)
        variety = self.validate_paragraph_variety()
        if variety['status'] == 'pass':
            scores['paragraph_variety'] = 30
        elif variety['distribution']['four_plus']['count'] == 0:
            scores['paragraph_variety'] = 15  # Partial credit if no fat paragraphs

        # Bullets (20 points)
        bullets = self.validate_bullet_sections()
        if bullets['count'] >= 12:
            scores['bullets'] = 20
        elif bullets['count'] >= 8:
            scores['bullets'] = 15
        elif bullets['count'] >= 5:
            scores['bullets'] = 10

        # Visuals (15 points)
        visuals = self.validate_visual_placeholders()
        if visuals['count'] >= 4:
            scores['visuals'] = 15
        elif visuals['count'] >= 2:
            scores['visuals'] = 10

        # Tables (10 points)
        tables = self.validate_tables()
        if tables['count'] >= 1:
            scores['tables'] = 10

        # Bold headers (15 points)
        bold = self.validate_bold_headers()
        if bold['count'] >= 12:
            scores['bold_headers'] = 15
        elif bold['count'] >= 8:
            scores['bold_headers'] = 10

        # Sub-bullets (10 points)
        subs = self.validate_sub_bullets()
        if subs['count'] >= 5:
            scores['sub_bullets'] = 10
        elif subs['count'] >= 3:
            scores['sub_bullets'] = 7

        # No fat paragraphs (CRITICAL - eliminates all points if failed)
        fat = self.detect_fat_paragraphs()
        if fat['count'] == 0:
            scores['no_fat_paragraphs'] = 0  # This is a pass/fail gate, not scored

        total_score = sum(scores.values())

        # If fat paragraphs exist, score is automatically 0
        if fat['count'] > 0:
            total_score = 0
            grade = 'F (AUTO-REJECT)'
        elif total_score >= 90:
            grade = 'A (Excellent)'
        elif total_score >= 80:
            grade = 'B (Good)'
        elif total_score >= 70:
            grade = 'C (Acceptable)'
        elif total_score >= 60:
            grade = 'D (Needs Work)'
        else:
            grade = 'F (Reject)'

        return {
            'total_score': total_score,
            'max_score': 100,
            'grade': grade,
            'breakdown': scores,
            'status': 'pass' if total_score >= 70 and fat['count'] == 0 else 'fail'
        }


def print_report(validation_results: Dict[str, any]) -> None:
    """Print formatted validation report."""
    print("\n" + "="*80)
    print("FORMATTING VALIDATION REPORT (v1.1 - Fixed Sentence Counting)")
    print("="*80 + "\n")

    # Overall Variety Score
    print("🎯 OVERALL VARIETY SCORE")
    print("-" * 80)
    variety_score = validation_results['variety_score']
    print(f"Score: {variety_score['total_score']}/100 - Grade: {variety_score['grade']}")
    print("\nBreakdown:")
    for category, points in variety_score['breakdown'].items():
        print(f"  • {category.replace('_', ' ').title()}: {points} points")
    print()

    # Fat Paragraphs (CRITICAL)
    print("🚨 FAT PARAGRAPHS CHECK (CRITICAL)")
    print("-" * 80)
    fat = validation_results['fat_paragraphs']
    print(fat['message'])
    if fat['fat_paragraphs']:
        print("\nFat paragraphs found (4+ sentences each):")
        for fp in fat['fat_paragraphs'][:5]:  # Show first 5
            print(f"  • Paragraph #{fp['paragraph_num']}: {fp['sentence_count']} sentences")
            print(f"    Preview: {fp['preview']}")
            print(f"    Full text: {fp['full_text']}")
            print()
    print()

    # Paragraph Variety
    print("📝 PARAGRAPH VARIETY")
    print("-" * 80)
    para = validation_results['paragraph_variety']
    print(para['message'])
    print(f"\nDistribution (total: {para['total_paragraphs']} paragraphs):")
    for length, data in para['distribution'].items():
        print(f"  • {length.replace('_', ' ').title()}: {data['count']} ({data['percentage']}%)")
    if para['issues']:
        print("\nIssues:")
        for issue in para['issues']:
            print(f"  {issue}")
    print()

    # Bullet Sections
    print("🔸 BULLET SECTIONS")
    print("-" * 80)
    bullets = validation_results['bullet_sections']
    print(bullets['message'])
    print(f"  Count: {bullets['count']} (minimum: {bullets['minimum']}, optimal: {bullets['optimal']})")
    print()

    # Visual Placeholders
    print("🖼️  VISUAL PLACEHOLDERS")
    print("-" * 80)
    visuals = validation_results['visual_placeholders']
    print(visuals['message'])
    if visuals['types']:
        print("  Types found:")
        for vtype, count in visuals['types'].items():
            print(f"    • {vtype}: {count}")
    print()

    # Tables
    print("📊 TABLES")
    print("-" * 80)
    tables = validation_results['tables']
    print(tables['message'])
    print()

    # Bold Headers
    print("💪 BOLD HEADERS")
    print("-" * 80)
    bold = validation_results['bold_headers']
    print(bold['message'])
    if bold['headers']:
        print("  Examples:")
        for header in bold['headers'][:5]:
            print(f"    • {header}")
    print()

    # Sub-Bullets
    print("  🔹 SUB-BULLETS (NESTED LISTS)")
    print("-" * 80)
    subs = validation_results['sub_bullets']
    print(subs['message'])
    print(f"  Total sub-bullet lines: {subs['total_sub_bullets']}")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)

    all_checks = [
        validation_results['fat_paragraphs']['status'],
        validation_results['paragraph_variety']['status'],
        validation_results['bullet_sections']['status'],
        validation_results['visual_placeholders']['status'],
        validation_results['bold_headers']['status'],
        validation_results['sub_bullets']['status']
    ]

    passes = all_checks.count('pass')
    fails = all_checks.count('fail')
    warnings = all_checks.count('warning')

    print(f"✅ Passed: {passes}/6 checks")
    print(f"❌ Failed: {fails}/6 checks")
    if warnings > 0:
        print(f"⚠️  Warnings: {warnings}/6 checks")

    print()

    if validation_results['fat_paragraphs']['count'] > 0:
        print("🚨 AUTO-REJECT: Fat paragraphs (4+ sentences) detected. MUST break up before proceeding.")
    elif variety_score['total_score'] < 70:
        print("❌ REJECT: Variety score below 70. Improve formatting before proceeding.")
    elif fails > 0:
        print("⚠️ ACTION REQUIRED: Fix failed checks before delivery.")
    else:
        print("🎉 EXCELLENT! All formatting checks passed.")

    print("="*80 + "\n")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python formatting-validator-fixed.py <markdown_file>")
        print("Example: python formatting-validator-fixed.py draft.md")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    # Run validation
    validator = FormattingValidator(content)
    results = validator.validate_all()

    # Print report
    print_report(results)

    # Exit with error code if validation fails
    if results['variety_score']['status'] == 'fail' or results['fat_paragraphs']['count'] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
