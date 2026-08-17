#!/usr/bin/env python3
"""
Paragraph Analyzer Script for Editing Checklist

Detects fat paragraphs (4+ sentences) and analyzes paragraph variety.
Use after editing to ensure content is scannable and reader-friendly.

Usage:
    python paragraph-analyzer.py <text_file>

Example:
    python scripts/paragraph-analyzer.py edited-content.md
    python scripts/paragraph-analyzer.py edited-content.txt
"""

import re
import sys
from typing import Dict, List
from collections import Counter


class ParagraphAnalyzer:
    """Analyzes paragraph structure for readability and scannability."""

    def __init__(self, content: str):
        self.content = content
        self.lines = content.split('\n')
        self.paragraphs = self._extract_paragraphs_with_context()

    def _extract_paragraphs_with_context(self) -> List[Dict]:
        """Extract paragraphs with line numbers and context."""
        paragraphs = []
        current_para = []
        start_line = 0

        for i, line in enumerate(self.lines, 1):
            # Skip headings, bullets, tables, code blocks
            if (line.startswith('#') or
                line.strip().startswith(('*', '-', '|', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '```')) or
                line.strip().startswith('[') and line.strip().endswith(']') or
                line.strip() == ''):

                # Save accumulated paragraph
                if current_para:
                    para_text = ' '.join(current_para)
                    paragraphs.append({
                        'text': para_text,
                        'start_line': start_line,
                        'end_line': i - 1,
                        'length': len(current_para)
                    })
                    current_para = []
                    start_line = 0
                continue

            if not current_para:
                start_line = i
            current_para.append(line.strip())

        # Add last paragraph
        if current_para:
            para_text = ' '.join(current_para)
            paragraphs.append({
                'text': para_text,
                'start_line': start_line,
                'end_line': len(self.lines),
                'length': len(current_para)
            })

        return paragraphs

    def validate_all(self) -> Dict[str, any]:
        """Run all paragraph analysis checks."""
        return {
            'paragraph_distribution': self.analyze_distribution(),
            'fat_paragraphs': self.detect_fat_paragraphs(),
            'variety_check': self.check_variety(),
            'wall_of_text_detection': self.detect_walls_of_text(),
            'improvement_suggestions': self.suggest_improvements(),
            'visual_breakdown': self.create_visual_breakdown()
        }

    def analyze_distribution(self) -> Dict[str, any]:
        """Analyze paragraph length distribution."""
        sentence_counts = []

        for para in self.paragraphs:
            # Count sentences
            sentences = re.split(r'[.!?]+', para['text'])
            sentences = [s.strip() for s in sentences if s.strip()]
            sentence_count = len(sentences)
            sentence_counts.append({
                'count': sentence_count,
                'start_line': para['start_line'],
                'preview': para['text'][:80] + '...' if len(para['text']) > 80 else para['text']
            })

        # Group by sentence count
        distribution = {
            '1_sentence': [],
            '2_sentence': [],
            '3_sentence': [],
            '4_5_sentence': [],
            '6_7_sentence': [],
            '8_plus': []
        }

        for item in sentence_counts:
            count = item['count']
            if count == 1:
                distribution['1_sentence'].append(item)
            elif count == 2:
                distribution['2_sentence'].append(item)
            elif count == 3:
                distribution['3_sentence'].append(item)
            elif count in [4, 5]:
                distribution['4_5_sentence'].append(item)
            elif count in [6, 7]:
                distribution['6_7_sentence'].append(item)
            else:
                distribution['8_plus'].append(item)

        total = len(sentence_counts)
        percentages = {
            '1_sentence': len(distribution['1_sentence']) / total * 100 if total > 0 else 0,
            '2_sentence': len(distribution['2_sentence']) / total * 100 if total > 0 else 0,
            '3_sentence': len(distribution['3_sentence']) / total * 100 if total > 0 else 0,
            '4_5_sentence': len(distribution['4_5_sentence']) / total * 100 if total > 0 else 0,
            '6_7_sentence': len(distribution['6_7_sentence']) / total * 100 if total > 0 else 0,
            '8_plus': len(distribution['8_plus']) / total * 100 if total > 0 else 0
        }

        return {
            'total_paragraphs': total,
            'distribution': distribution,
            'percentages': percentages,
            'counts': {
                '1_sentence': len(distribution['1_sentence']),
                '2_sentence': len(distribution['2_sentence']),
                '3_sentence': len(distribution['3_sentence']),
                '4_5_sentence': len(distribution['4_5_sentence']),
                '6_7_sentence': len(distribution['6_7_sentence']),
                '8_plus': len(distribution['8_plus'])
            }
        }

    def detect_fat_paragraphs(self) -> Dict[str, any]:
        """Detect paragraphs with 4+ sentences (editing checklist considers these problematic)."""
        fat_paragraphs = []
        critical_fat = []  # 8+ sentences

        for para in self.paragraphs:
            sentences = re.split(r'[.!?]+', para['text'])
            sentences = [s.strip() for s in sentences if s.strip()]
            sentence_count = len(sentences)

            if sentence_count >= 4:
                para_info = {
                    'line': para['start_line'],
                    'sentence_count': sentence_count,
                    'preview': para['text'][:120] + '...' if len(para['text']) > 120 else para['text'],
                    'severity': 'critical' if sentence_count >= 8 else 'warning',
                    'word_count': len(para['text'].split())
                }

                fat_paragraphs.append(para_info)

                if sentence_count >= 8:
                    critical_fat.append(para_info)

        return {
            'count': len(fat_paragraphs),
            'critical_count': len(critical_fat),
            'fat_paragraphs': fat_paragraphs,
            'status': 'pass' if len(fat_paragraphs) == 0 else 'fail',
            'message': "✅ No fat paragraphs detected" if len(fat_paragraphs) == 0 else f"❌ {len(fat_paragraphs)} fat paragraphs found ({len(critical_fat)} critical)"
        }

    def detect_walls_of_text(self) -> Dict[str, any]:
        """Detect walls of text (paragraphs exceeding 150 words)."""
        walls = []

        for para in self.paragraphs:
            word_count = len(para['text'].split())

            if word_count > 150:
                sentences = re.split(r'[.!?]+', para['text'])
                sentences = [s.strip() for s in sentences if s.strip()]

                walls.append({
                    'line': para['start_line'],
                    'word_count': word_count,
                    'sentence_count': len(sentences),
                    'preview': para['text'][:120] + '...' if len(para['text']) > 120 else para['text'],
                    'severity': 'critical' if word_count > 200 else 'warning'
                })

        return {
            'count': len(walls),
            'walls': walls,
            'status': 'pass' if len(walls) == 0 else 'warning',
            'message': "✅ No walls of text detected" if len(walls) == 0 else f"⚠️ {len(walls)} dense paragraphs found (150+ words)"
        }

    def check_variety(self) -> Dict[str, any]:
        """Check for paragraph variety to avoid monotony."""
        dist = self.analyze_distribution()
        counts = dist['counts']
        total = dist['total_paragraphs']

        issues = []

        # Check if all paragraphs are the same length (monotonous)
        if total > 0:
            max_same_length = max(counts.values())
            if max_same_length > (total * 0.7):
                issues.append({
                    'severity': 'warning',
                    'issue': 'Monotonous paragraph length',
                    'description': f"{max_same_length}/{total} paragraphs are the same length—lacks variety"
                })

        # Check for good distribution (business writing context)
        # Optimal for business/editing: Mix of 1-3 sentence paragraphs, minimal 4+
        if counts['8_plus'] > 0:
            issues.append({
                'severity': 'critical',
                'issue': 'Extremely long paragraphs',
                'description': f"{counts['8_plus']} paragraphs have 8+ sentences (cognitive overload)"
            })

        if counts['6_7_sentence'] > (total * 0.2):
            issues.append({
                'severity': 'warning',
                'issue': 'Too many 6-7 sentence paragraphs',
                'description': f"{counts['6_7_sentence']} paragraphs are 6-7 sentences (approaching max)"
            })

        return {
            'issues': issues,
            'has_variety': len(issues) == 0,
            'status': 'pass' if len(issues) == 0 else 'warning',
            'message': "✅ Good paragraph variety" if len(issues) == 0 else f"⚠️ {len(issues)} variety issue(s) detected"
        }

    def suggest_improvements(self) -> Dict[str, any]:
        """Suggest specific improvements for fat paragraphs."""
        fat = self.detect_fat_paragraphs()
        walls = self.detect_walls_of_text()
        variety = self.check_variety()

        suggestions = []

        # Critical fat paragraphs (8+)
        if fat['critical_count'] > 0:
            critical_paras = [fp for fp in fat['fat_paragraphs'] if fp['severity'] == 'critical']
            suggestions.append({
                'priority': 'critical',
                'action': 'Break up extremely long paragraphs (8+ sentences)',
                'details': f"{fat['critical_count']} paragraphs exceed cognitive load limits",
                'locations': [f"Line {fp['line']} ({fp['sentence_count']} sentences)" for fp in critical_paras[:5]],
                'tip': "Split into 2-3 shorter paragraphs. One idea per paragraph."
            })

        # Warning fat paragraphs (4-7)
        warning_count = fat['count'] - fat['critical_count']
        if warning_count > 0:
            warning_paras = [fp for fp in fat['fat_paragraphs'] if fp['severity'] == 'warning']
            suggestions.append({
                'priority': 'high',
                'action': 'Reduce paragraph length (4-7 sentences)',
                'details': f"{warning_count} paragraphs are longer than optimal (3-5 sentences)",
                'locations': [f"Line {fp['line']} ({fp['sentence_count']} sentences)" for fp in warning_paras[:5]],
                'tip': "Target 3-5 sentences. Break at natural transition points."
            })

        # Walls of text
        if walls['count'] > 0:
            suggestions.append({
                'priority': 'high',
                'action': 'Break up dense text blocks (150+ words)',
                'details': f"{walls['count']} paragraphs create visual intimidation",
                'locations': [f"Line {w['line']} ({w['word_count']} words)" for w in walls['walls'][:5]],
                'tip': "Add white space and headings. Use chunking to improve scannability."
            })

        # Variety issues
        if variety['issues']:
            for issue in variety['issues']:
                if issue['severity'] == 'critical':
                    suggestions.append({
                        'priority': 'critical',
                        'action': issue['issue'],
                        'details': issue['description'],
                        'tip': "Vary paragraph lengths for better readability"
                    })

        return {
            'total_suggestions': len(suggestions),
            'suggestions': suggestions,
            'critical_actions': len([s for s in suggestions if s['priority'] == 'critical']),
            'high_priority_actions': len([s for s in suggestions if s['priority'] == 'high'])
        }

    def create_visual_breakdown(self) -> Dict[str, any]:
        """Create a visual representation of paragraph structure."""
        visual = []

        for i, para in enumerate(self.paragraphs[:30], 1):  # First 30 paragraphs
            sentences = re.split(r'[.!?]+', para['text'])
            sentences = [s.strip() for s in sentences if s.strip()]
            count = len(sentences)
            word_count = len(para['text'].split())

            # Create visual bar and status
            if count <= 3:
                status = "✅"
                bar = "█" * count
            elif count <= 5:
                status = "⚠️"
                bar = "█" * 3 + "▓" * (count - 3)
            elif count <= 7:
                status = "⚠️"
                bar = "█" * 3 + "▓" * 2 + "░" * (count - 5)
            else:
                status = "❌"
                bar = "████████+"

            visual.append({
                'para_num': i,
                'sentence_count': count,
                'word_count': word_count,
                'bar': bar,
                'status': status,
                'line': para['start_line']
            })

        return {
            'visual_map': visual,
            'legend': "█ = optimal (1-3), ▓ = acceptable (4-5), ░ = max (6-7), ❌ = reject (8+)"
        }


def print_report(validation_results: Dict[str, any]) -> None:
    """Print formatted paragraph analysis report."""
    print("\n" + "="*80)
    print("PARAGRAPH STRUCTURE ANALYSIS - Editing Checklist")
    print("="*80 + "\n")

    # Distribution
    print("📊 PARAGRAPH DISTRIBUTION")
    print("-" * 80)
    dist = validation_results['paragraph_distribution']
    print(f"Total paragraphs analyzed: {dist['total_paragraphs']}\n")
    print("Distribution by sentence count:")
    for key, count in dist['counts'].items():
        pct = dist['percentages'][key]
        label = key.replace('_', ' ')
        status = ""
        if '8_plus' in key:
            status = " ❌ CRITICAL"
        elif '6_7' in key:
            status = " ⚠️ APPROACHING MAX"
        elif '4_5' in key:
            status = " ⚠️ FAT"
        print(f"  • {label:15s}: {count:3d} ({pct:5.1f}%){status}")
    print()

    # Fat Paragraphs (4+ sentences)
    print("🚫 FAT PARAGRAPH DETECTION (4+ SENTENCES)")
    print("-" * 80)
    fat = validation_results['fat_paragraphs']
    print(fat['message'])
    if fat['fat_paragraphs']:
        print(f"\n{'Critical (8+):':<20} {fat['critical_count']} paragraphs")
        print(f"{'Warning (4-7):':<20} {fat['count'] - fat['critical_count']} paragraphs\n")

        print("Fat paragraphs that need breaking up:")
        for fp in fat['fat_paragraphs'][:10]:
            icon = "🚨" if fp['severity'] == 'critical' else "⚠️"
            print(f"\n  {icon} Line {fp['line']}: {fp['sentence_count']} sentences, {fp['word_count']} words")
            print(f"     Preview: {fp['preview']}")
    print()

    # Walls of Text
    print("📄 WALL OF TEXT DETECTION (150+ WORDS)")
    print("-" * 80)
    walls = validation_results['wall_of_text_detection']
    print(walls['message'])
    if walls['walls']:
        print("\nDense paragraphs:")
        for wall in walls['walls'][:5]:
            icon = "🚨" if wall['severity'] == 'critical' else "⚠️"
            print(f"  {icon} Line {wall['line']}: {wall['word_count']} words, {wall['sentence_count']} sentences")
    print()

    # Variety Check
    print("🎨 VARIETY & MONOTONY ANALYSIS")
    print("-" * 80)
    variety = validation_results['variety_check']
    print(variety['message'])
    if variety['issues']:
        print("\nIssues found:")
        for issue in variety['issues']:
            severity_icon = "🚨" if issue['severity'] == 'critical' else "⚠️"
            print(f"  {severity_icon} {issue['issue']}: {issue['description']}")
    print()

    # Visual Breakdown
    print("📍 VISUAL PARAGRAPH MAP (First 30)")
    print("-" * 80)
    visual = validation_results['visual_breakdown']
    print(f"Legend: {visual['legend']}\n")
    for v in visual['visual_map'][:30]:
        print(f"  Para {v['para_num']:2d} (line {v['line']:3d}): {v['bar']:<15s} {v['status']} ({v['sentence_count']} sentences, {v['word_count']} words)")
    print()

    # Improvement Suggestions
    print("💡 IMPROVEMENT SUGGESTIONS")
    print("-" * 80)
    suggestions = validation_results['improvement_suggestions']
    print(f"Total suggestions: {suggestions['total_suggestions']}")
    print(f"Critical actions: {suggestions['critical_actions']}")
    print(f"High-priority actions: {suggestions['high_priority_actions']}\n")

    if suggestions['suggestions']:
        for i, sug in enumerate(suggestions['suggestions'], 1):
            priority_icon = {
                'critical': '🚨',
                'high': '⚠️',
                'medium': 'ℹ️',
                'low': '💬'
            }.get(sug['priority'], 'ℹ️')

            print(f"{i}. {priority_icon} [{sug['priority'].upper()}] {sug['action']}")
            print(f"   {sug['details']}")
            if 'locations' in sug:
                print(f"   Locations: {', '.join(sug['locations'][:5])}")
                if len(sug['locations']) > 5:
                    print(f"   ... and {len(sug['locations']) - 5} more")
            if 'tip' in sug:
                print(f"   💡 Tip: {sug['tip']}")
            print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)

    fat = validation_results['fat_paragraphs']
    walls = validation_results['wall_of_text_detection']
    variety = validation_results['variety_check']

    if fat['critical_count'] > 0:
        print(f"❌ CRITICAL: {fat['critical_count']} paragraphs have 8+ sentences (cognitive overload)")
    elif fat['count'] > 0:
        print(f"⚠️ WARNING: {fat['count']} fat paragraphs (4+ sentences) detected")
    elif walls['count'] > 0:
        print(f"⚠️ WARNING: {walls['count']} dense paragraphs (150+ words) detected")
    elif not variety['has_variety']:
        print("⚠️ WARNING: Paragraph length lacks variety (monotonous)")
    else:
        print("✅ EXCELLENT: Paragraphs are well-structured and scannable")
        print("   All paragraphs within optimal length (3-5 sentences)")

    print("\n" + "="*80)
    print("Editing Checklist Step 4: Readability - Paragraph Structure")
    print("Target: 3-5 sentences per paragraph, maximum 7-8 before cognitive overload")
    print("="*80 + "\n")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python paragraph-analyzer.py <text_file>")
        print("Example: python scripts/paragraph-analyzer.py edited-content.md")
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

    # Run analysis
    analyzer = ParagraphAnalyzer(content)
    results = analyzer.validate_all()

    # Print report
    print_report(results)

    # Exit with error code if critical issues found
    fat = results['fat_paragraphs']
    if fat['critical_count'] > 0:
        sys.exit(1)  # Critical fat paragraphs (8+)
    elif fat['count'] > 0:
        sys.exit(2)  # Warning fat paragraphs (4-7)


if __name__ == "__main__":
    main()
