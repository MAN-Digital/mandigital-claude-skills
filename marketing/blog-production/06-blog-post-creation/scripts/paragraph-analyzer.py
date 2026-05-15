#!/usr/bin/env python3
"""
Paragraph Analyzer Script

Deep analysis of paragraph structure and variety.
Detects monotonous patterns and suggests improvements.

Usage:
    python paragraph-analyzer.py <markdown_file>

Example:
    python paragraph-analyzer.py draft.md
"""

import re
import sys
from typing import Dict, List, Tuple
from collections import Counter


class ParagraphAnalyzer:
    """Analyzes paragraph structure for variety and scannability."""

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
            # Skip headings, bullets, tables, visual placeholders
            if (line.startswith('#') or
                line.strip().startswith(('*', '-', '|', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or
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
            'variety_patterns': self.detect_variety_patterns(),
            'fat_paragraphs': self.detect_fat_paragraphs(),
            'monotony_detection': self.detect_monotony(),
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
            '4_plus': []
        }

        for item in sentence_counts:
            count = item['count']
            if count == 1:
                distribution['1_sentence'].append(item)
            elif count == 2:
                distribution['2_sentence'].append(item)
            elif count == 3:
                distribution['3_sentence'].append(item)
            else:
                distribution['4_plus'].append(item)

        total = len(sentence_counts)
        percentages = {
            '1_sentence': len(distribution['1_sentence']) / total * 100 if total > 0 else 0,
            '2_sentence': len(distribution['2_sentence']) / total * 100 if total > 0 else 0,
            '3_sentence': len(distribution['3_sentence']) / total * 100 if total > 0 else 0,
            '4_plus': len(distribution['4_plus']) / total * 100 if total > 0 else 0
        }

        return {
            'total_paragraphs': total,
            'distribution': distribution,
            'percentages': percentages,
            'counts': {
                '1_sentence': len(distribution['1_sentence']),
                '2_sentence': len(distribution['2_sentence']),
                '3_sentence': len(distribution['3_sentence']),
                '4_plus': len(distribution['4_plus'])
            }
        }

    def detect_variety_patterns(self) -> Dict[str, any]:
        """Detect paragraph variety patterns."""
        dist = self.analyze_distribution()
        counts = dist['counts']
        percentages = dist['percentages']

        # Check for monotonous patterns
        issues = []

        # All same length (very bad)
        if counts['2_sentence'] > (dist['total_paragraphs'] * 0.8):
            issues.append({
                'severity': 'critical',
                'issue': 'Monotonous 2-sentence pattern',
                'description': f"{counts['2_sentence']}/{dist['total_paragraphs']} paragraphs are exactly 2 sentences (monotonous)"
            })

        # Missing variety
        if counts['1_sentence'] < 5:
            issues.append({
                'severity': 'warning',
                'issue': 'Too few 1-sentence paragraphs',
                'description': f"Only {counts['1_sentence']} single-sentence paragraphs (need 10-15 for punch)"
            })

        if counts['3_sentence'] < 3:
            issues.append({
                'severity': 'warning',
                'issue': 'Too few 3-sentence paragraphs',
                'description': f"Only {counts['3_sentence']} three-sentence paragraphs (need 5-10 for depth)"
            })

        # Too many fat paragraphs
        if counts['4_plus'] > 0:
            issues.append({
                'severity': 'critical',
                'issue': 'Fat paragraphs present',
                'description': f"{counts['4_plus']} paragraphs have 4+ sentences (auto-reject)"
            })

        # Calculate variety score (0-100)
        variety_score = 100

        # Penalty for fat paragraphs (auto-fail)
        if counts['4_plus'] > 0:
            variety_score = 0
        else:
            # Penalty for poor distribution
            ideal_1_sent = 12
            ideal_2_sent = 22
            ideal_3_sent = 7

            deviation_1 = abs(counts['1_sentence'] - ideal_1_sent)
            deviation_2 = abs(counts['2_sentence'] - ideal_2_sent)
            deviation_3 = abs(counts['3_sentence'] - ideal_3_sent)

            total_deviation = deviation_1 + deviation_2 + deviation_3
            variety_score = max(0, 100 - (total_deviation * 2))

        if variety_score >= 80:
            status = 'excellent'
            icon = "✅"
        elif variety_score >= 60:
            status = 'good'
            icon = "⚠️"
        else:
            status = 'poor'
            icon = "❌"

        return {
            'variety_score': round(variety_score, 1),
            'status': status,
            'icon': icon,
            'issues': issues,
            'message': f"{icon} Variety Score: {round(variety_score, 1)}/100 ({status.upper()})"
        }

    def detect_fat_paragraphs(self) -> Dict[str, any]:
        """Detect paragraphs with 4+ sentences."""
        fat_paragraphs = []

        for para in self.paragraphs:
            sentences = re.split(r'[.!?]+', para['text'])
            sentences = [s.strip() for s in sentences if s.strip()]

            if len(sentences) >= 4:
                fat_paragraphs.append({
                    'line': para['start_line'],
                    'sentence_count': len(sentences),
                    'preview': para['text'][:100] + '...' if len(para['text']) > 100 else para['text'],
                    'suggestion': f"Break into {len(sentences) // 2} paragraphs"
                })

        return {
            'count': len(fat_paragraphs),
            'fat_paragraphs': fat_paragraphs,
            'status': 'pass' if len(fat_paragraphs) == 0 else 'fail',
            'message': "✅ No fat paragraphs" if len(fat_paragraphs) == 0 else f"❌ {len(fat_paragraphs)} paragraphs need breaking up"
        }

    def detect_monotony(self) -> Dict[str, any]:
        """Detect monotonous paragraph patterns."""
        # Check for consecutive paragraphs of same length
        consecutive_same = []
        last_length = None
        streak = 0
        streak_start = 0

        for i, para in enumerate(self.paragraphs):
            sentences = re.split(r'[.!?]+', para['text'])
            sentences = [s.strip() for s in sentences if s.strip()]
            current_length = len(sentences)

            if current_length == last_length:
                streak += 1
            else:
                if streak >= 4:  # 5+ consecutive same length
                    consecutive_same.append({
                        'length': last_length,
                        'streak': streak + 1,
                        'start_para': streak_start + 1,
                        'end_para': i
                    })
                streak = 0
                streak_start = i

            last_length = current_length

        # Check last streak
        if streak >= 4:
            consecutive_same.append({
                'length': last_length,
                'streak': streak + 1,
                'start_para': streak_start + 1,
                'end_para': len(self.paragraphs)
            })

        monotony_detected = len(consecutive_same) > 0

        return {
            'monotony_detected': monotony_detected,
            'monotonous_sequences': consecutive_same,
            'count': len(consecutive_same),
            'status': 'fail' if monotony_detected else 'pass',
            'message': "✅ Good variety, no monotonous patterns" if not monotony_detected else f"❌ {len(consecutive_same)} monotonous sequence(s) detected"
        }

    def suggest_improvements(self) -> Dict[str, any]:
        """Suggest specific improvements."""
        dist = self.analyze_distribution()
        fat = self.detect_fat_paragraphs()
        monotony = self.detect_monotony()

        suggestions = []

        # Fat paragraphs
        if fat['count'] > 0:
            suggestions.append({
                'priority': 'critical',
                'action': 'Break up fat paragraphs',
                'details': f"Split {fat['count']} paragraphs (4+ sentences each) into smaller chunks",
                'locations': [f"Line {fp['line']}" for fp in fat['fat_paragraphs'][:5]]
            })

        # Need more 1-sentence paragraphs
        if dist['counts']['1_sentence'] < 10:
            suggestions.append({
                'priority': 'high',
                'action': 'Add more 1-sentence paragraphs',
                'details': f"Current: {dist['counts']['1_sentence']}. Add {10 - dist['counts']['1_sentence']} more for punch and variety",
                'tip': "Use for powerful statements, transitions, or emphasis"
            })

        # Too many 2-sentence paragraphs
        if dist['counts']['2_sentence'] > 30:
            suggestions.append({
                'priority': 'medium',
                'action': 'Reduce 2-sentence paragraphs',
                'details': f"Current: {dist['counts']['2_sentence']}. Convert some to 1-sentence or 3-sentence for variety",
                'tip': "Look for opportunities to split explanations or combine simple statements"
            })

        # Need more 3-sentence paragraphs
        if dist['counts']['3_sentence'] < 5:
            suggestions.append({
                'priority': 'medium',
                'action': 'Add more 3-sentence paragraphs',
                'details': f"Current: {dist['counts']['3_sentence']}. Add {5 - dist['counts']['3_sentence']} more for depth",
                'tip': "Use for complex ideas that need explanation"
            })

        # Monotony
        if monotony['monotony_detected']:
            for seq in monotony['monotonous_sequences']:
                suggestions.append({
                    'priority': 'high',
                    'action': 'Break monotonous pattern',
                    'details': f"Paragraphs {seq['start_para']}-{seq['end_para']}: {seq['streak']} consecutive {seq['length']}-sentence paragraphs",
                    'tip': "Vary the length by splitting or combining"
                })

        return {
            'total_suggestions': len(suggestions),
            'suggestions': suggestions,
            'actionable': len([s for s in suggestions if s['priority'] in ['critical', 'high']])
        }

    def create_visual_breakdown(self) -> Dict[str, any]:
        """Create a visual representation of paragraph structure."""
        visual = []

        for i, para in enumerate(self.paragraphs[:30], 1):  # First 30 paragraphs
            sentences = re.split(r'[.!?]+', para['text'])
            sentences = [s.strip() for s in sentences if s.strip()]
            count = len(sentences)

            # Create visual bar
            if count == 1:
                bar = "█"
                label = "1"
            elif count == 2:
                bar = "██"
                label = "2"
            elif count == 3:
                bar = "███"
                label = "3"
            else:
                bar = "████+"
                label = f"{count}❌"

            visual.append({
                'para_num': i,
                'sentence_count': count,
                'bar': bar,
                'label': label,
                'line': para['start_line']
            })

        return {
            'visual_map': visual,
            'pattern': ''.join([v['bar'] + ' ' for v in visual])
        }


def print_report(validation_results: Dict[str, any]) -> None:
    """Print formatted paragraph analysis report."""
    print("\n" + "="*80)
    print("PARAGRAPH STRUCTURE ANALYSIS")
    print("="*80 + "\n")

    # Distribution
    print("📊 PARAGRAPH DISTRIBUTION")
    print("-" * 80)
    dist = validation_results['paragraph_distribution']
    print(f"Total paragraphs: {dist['total_paragraphs']}\n")
    print("Distribution:")
    for key, count in dist['counts'].items():
        pct = dist['percentages'][key]
        label = key.replace('_', '-')
        print(f"  • {label}: {count} ({pct:.1f}%)")
    print()

    # Variety Patterns
    print("🎨 VARIETY ANALYSIS")
    print("-" * 80)
    variety = validation_results['variety_patterns']
    print(variety['message'])
    if variety['issues']:
        print("\nIssues found:")
        for issue in variety['issues']:
            severity_icon = "🚨" if issue['severity'] == 'critical' else "⚠️"
            print(f"  {severity_icon} {issue['issue']}: {issue['description']}")
    print()

    # Fat Paragraphs
    print("🚫 FAT PARAGRAPHS (4+ SENTENCES)")
    print("-" * 80)
    fat = validation_results['fat_paragraphs']
    print(fat['message'])
    if fat['fat_paragraphs']:
        print("\nFat paragraphs that need breaking up:")
        for fp in fat['fat_paragraphs'][:5]:
            print(f"\n  📍 Line {fp['line']}: {fp['sentence_count']} sentences")
            print(f"     Preview: {fp['preview']}")
            print(f"     Suggestion: {fp['suggestion']}")
    print()

    # Monotony Detection
    print("🔁 MONOTONY DETECTION")
    print("-" * 80)
    monotony = validation_results['monotony_detection']
    print(monotony['message'])
    if monotony['monotonous_sequences']:
        print("\nMonotonous sequences found:")
        for seq in monotony['monotonous_sequences']:
            print(f"  • Paragraphs {seq['start_para']}-{seq['end_para']}: {seq['streak']} consecutive {seq['length']}-sentence paragraphs")
    print()

    # Visual Breakdown
    print("📍 VISUAL PARAGRAPH MAP (First 30)")
    print("-" * 80)
    visual = validation_results['visual_breakdown']
    print("Legend: █ = 1 sentence, ██ = 2 sentences, ███ = 3 sentences, ████+ = 4+ (reject)\n")
    for v in visual['visual_map'][:30]:
        icon = "❌" if v['sentence_count'] >= 4 else ""
        print(f"  Para {v['para_num']:2d} (line {v['line']:3d}): {v['bar']} {icon}")
    print()

    # Improvement Suggestions
    print("💡 IMPROVEMENT SUGGESTIONS")
    print("-" * 80)
    suggestions = validation_results['improvement_suggestions']
    print(f"Total suggestions: {suggestions['total_suggestions']}")
    print(f"High-priority actions: {suggestions['actionable']}\n")

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
            if 'tip' in sug:
                print(f"   💡 Tip: {sug['tip']}")
            print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)

    variety = validation_results['variety_patterns']
    fat = validation_results['fat_paragraphs']

    if fat['count'] > 0:
        print("❌ REJECT: Fat paragraphs (4+ sentences) must be broken up")
    elif variety['variety_score'] < 60:
        print(f"❌ POOR VARIETY: Score {variety['variety_score']}/100")
        print("   Action Required: Improve paragraph length distribution")
    elif variety['variety_score'] < 80:
        print(f"⚠️ ACCEPTABLE VARIETY: Score {variety['variety_score']}/100")
        print("   Consider minor improvements for better scannability")
    else:
        print(f"✅ EXCELLENT VARIETY: Score {variety['variety_score']}/100")
        print("   Paragraph structure is well-balanced and scannable")

    print("="*80 + "\n")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python paragraph-analyzer.py <markdown_file>")
        print("Example: python paragraph-analyzer.py draft.md")
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
    if (results['fat_paragraphs']['count'] > 0 or
        results['variety_patterns']['variety_score'] < 60):
        sys.exit(1)


if __name__ == "__main__":
    main()
