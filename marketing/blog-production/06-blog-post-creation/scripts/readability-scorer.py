#!/usr/bin/env python3
"""
Readability Scorer Script

Analyzes blog post readability with focus on non-native English speakers.
Calculates Flesch-Kincaid scores, sentence complexity, and accessibility metrics.

Usage:
    python readability-scorer.py <markdown_file>

Example:
    python readability-scorer.py draft.md
"""

import re
import sys
from typing import Dict, List, Tuple
from collections import Counter
import math


class ReadabilityScorer:
    """Analyzes readability and accessibility of blog content."""

    def __init__(self, content: str):
        self.content = content
        self.clean_content = self._clean_markdown(content)
        self.sentences = self._extract_sentences()
        self.words = self._extract_words()
        self.syllables = self._count_syllables()

    def _clean_markdown(self, text: str) -> str:
        """Remove markdown syntax for clean text analysis."""
        # Remove headings
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        # Remove links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Remove bold/italic markers
        text = re.sub(r'[*_`]+', '', text)
        # Remove visual placeholders
        text = re.sub(r'\[(Screenshot|Diagram|Chart)[^\]]*\]', '', text, flags=re.I)
        # Remove bullet markers
        text = re.sub(r'^[\s]*[-*\d]+\.?\s', '', text, flags=re.MULTILINE)
        # Remove table markers
        text = re.sub(r'\|', '', text)
        return text

    def _extract_sentences(self) -> List[str]:
        """Extract sentences from clean content."""
        # Split on period, exclamation, question mark
        sentences = re.split(r'[.!?]+', self.clean_content)
        # Filter empty and very short
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return sentences

    def _extract_words(self) -> List[str]:
        """Extract words from clean content."""
        # Split on whitespace and punctuation
        words = re.findall(r'\b[a-zA-Z]+\b', self.clean_content.lower())
        return words

    def _count_syllables(self) -> int:
        """Count total syllables in content (simplified algorithm)."""
        total = 0
        for word in self.words:
            total += self._count_syllables_in_word(word)
        return total

    def _count_syllables_in_word(self, word: str) -> int:
        """Count syllables in a single word (simplified)."""
        word = word.lower()
        # Remove non-alphabetic characters
        word = re.sub(r'[^a-z]', '', word)

        if len(word) == 0:
            return 0

        # Basic syllable counting
        count = 0
        vowels = 'aeiouy'
        previous_was_vowel = False

        for i, char in enumerate(word):
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent 'e'
        if word.endswith('e') and count > 1:
            count -= 1

        # Adjust for 'le' ending
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            count += 1

        # Minimum 1 syllable
        return max(1, count)

    def validate_all(self) -> Dict[str, any]:
        """Run all readability checks."""
        return {
            'flesch_kincaid_ease': self.flesch_reading_ease(),
            'flesch_kincaid_grade': self.flesch_kincaid_grade_level(),
            'sentence_stats': self.analyze_sentence_length(),
            'word_stats': self.analyze_word_complexity(),
            'passive_voice': self.detect_passive_voice(),
            'long_sentences': self.detect_long_sentences(),
            'complex_words': self.detect_complex_words(),
            'overall_assessment': self.get_overall_assessment()
        }

    def flesch_reading_ease(self) -> Dict[str, any]:
        """Calculate Flesch Reading Ease score (0-100, higher is easier)."""
        if not self.sentences or not self.words:
            return {'score': 0, 'status': 'fail', 'message': 'Not enough content to analyze'}

        total_sentences = len(self.sentences)
        total_words = len(self.words)
        total_syllables = self.syllables

        # Flesch Reading Ease = 206.835 - 1.015(words/sentences) - 84.6(syllables/words)
        avg_words_per_sentence = total_words / total_sentences
        avg_syllables_per_word = total_syllables / total_words

        score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        score = max(0, min(100, score))  # Clamp to 0-100

        # Interpretation
        if score >= 70:
            level = "Very Easy (8th grade)"
            status = 'pass'
            icon = "✅"
        elif score >= 60:
            level = "Easy (9th-10th grade)"
            status = 'pass'
            icon = "✅"
        elif score >= 50:
            level = "Fairly Easy (10th-12th grade)"
            status = 'warning'
            icon = "⚠️"
        elif score >= 30:
            level = "Difficult (College)"
            status = 'fail'
            icon = "❌"
        else:
            level = "Very Difficult (College Graduate)"
            status = 'fail'
            icon = "❌"

        return {
            'score': round(score, 1),
            'level': level,
            'status': status,
            'target': '60-70 (Easy)',
            'message': f"{icon} Flesch Reading Ease: {round(score, 1)} ({level})"
        }

    def flesch_kincaid_grade_level(self) -> Dict[str, any]:
        """Calculate Flesch-Kincaid Grade Level."""
        if not self.sentences or not self.words:
            return {'grade': 0, 'status': 'fail', 'message': 'Not enough content to analyze'}

        total_sentences = len(self.sentences)
        total_words = len(self.words)
        total_syllables = self.syllables

        # F-K Grade = 0.39(words/sentences) + 11.8(syllables/words) - 15.59
        avg_words_per_sentence = total_words / total_sentences
        avg_syllables_per_word = total_syllables / total_words

        grade = 0.39 * avg_words_per_sentence + 11.8 * avg_syllables_per_word - 15.59
        grade = max(0, grade)

        # Target: 8-10 grade level
        if grade <= 10:
            status = 'pass'
            icon = "✅"
        elif grade <= 12:
            status = 'warning'
            icon = "⚠️"
        else:
            status = 'fail'
            icon = "❌"

        return {
            'grade': round(grade, 1),
            'status': status,
            'target': '8-10 grade level',
            'message': f"{icon} Grade Level: {round(grade, 1)} (target: 8-10)"
        }

    def analyze_sentence_length(self) -> Dict[str, any]:
        """Analyze sentence length distribution."""
        sentence_lengths = [len(s.split()) for s in self.sentences]

        if not sentence_lengths:
            return {'status': 'fail', 'message': 'No sentences found'}

        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        max_length = max(sentence_lengths)
        min_length = min(sentence_lengths)

        # Count sentences by length category
        short = sum(1 for l in sentence_lengths if l <= 10)  # 1-10 words
        medium = sum(1 for l in sentence_lengths if 11 <= l <= 20)  # 11-20 words
        long = sum(1 for l in sentence_lengths if 21 <= l <= 30)  # 21-30 words
        very_long = sum(1 for l in sentence_lengths if l > 30)  # 30+ words

        # Target: 15-20 words average
        if 15 <= avg_length <= 20:
            status = 'pass'
            icon = "✅"
        elif 12 <= avg_length <= 23:
            status = 'warning'
            icon = "⚠️"
        else:
            status = 'fail'
            icon = "❌"

        return {
            'average': round(avg_length, 1),
            'max': max_length,
            'min': min_length,
            'distribution': {
                'short_1_10': short,
                'medium_11_20': medium,
                'long_21_30': long,
                'very_long_30_plus': very_long
            },
            'status': status,
            'target': '15-20 words average',
            'message': f"{icon} Average sentence length: {round(avg_length, 1)} words (target: 15-20)"
        }

    def analyze_word_complexity(self) -> Dict[str, any]:
        """Analyze word complexity."""
        if not self.words:
            return {'status': 'fail', 'message': 'No words found'}

        total_words = len(self.words)

        # Complex words: 3+ syllables
        complex_words = [w for w in self.words if self._count_syllables_in_word(w) >= 3]
        complex_pct = len(complex_words) / total_words * 100

        # Target: <15% complex words
        if complex_pct <= 15:
            status = 'pass'
            icon = "✅"
        elif complex_pct <= 20:
            status = 'warning'
            icon = "⚠️"
        else:
            status = 'fail'
            icon = "❌"

        # Average word length
        avg_word_length = sum(len(w) for w in self.words) / total_words

        return {
            'complex_word_count': len(complex_words),
            'complex_word_percentage': round(complex_pct, 1),
            'average_word_length': round(avg_word_length, 1),
            'status': status,
            'target': '<15% complex words',
            'message': f"{icon} Complex words: {round(complex_pct, 1)}% (target: <15%)"
        }

    def detect_passive_voice(self) -> Dict[str, any]:
        """Detect passive voice usage."""
        passive_indicators = [
            r'\bis\s+\w+ed\b',
            r'\bare\s+\w+ed\b',
            r'\bwas\s+\w+ed\b',
            r'\bwere\s+\w+ed\b',
            r'\bbeen\s+\w+ed\b',
            r'\bbe\s+\w+ed\b',
        ]

        passive_count = 0
        for pattern in passive_indicators:
            passive_count += len(re.findall(pattern, self.clean_content, re.I))

        total_sentences = len(self.sentences)
        passive_pct = (passive_count / total_sentences * 100) if total_sentences > 0 else 0

        # Target: <10% passive voice
        if passive_pct <= 10:
            status = 'pass'
            icon = "✅"
        elif passive_pct <= 15:
            status = 'warning'
            icon = "⚠️"
        else:
            status = 'fail'
            icon = "❌"

        return {
            'passive_count': passive_count,
            'passive_percentage': round(passive_pct, 1),
            'status': status,
            'target': '<10%',
            'message': f"{icon} Passive voice: {round(passive_pct, 1)}% (target: <10%)"
        }

    def detect_long_sentences(self) -> Dict[str, any]:
        """Detect sentences longer than 25 words."""
        long_sentences = []

        for sentence in self.sentences:
            words = sentence.split()
            if len(words) > 25:
                preview = ' '.join(words[:15]) + '...'
                long_sentences.append({
                    'word_count': len(words),
                    'preview': preview
                })

        long_pct = (len(long_sentences) / len(self.sentences) * 100) if self.sentences else 0

        # Target: <20% of sentences over 25 words
        if long_pct <= 20:
            status = 'pass'
            icon = "✅"
        elif long_pct <= 30:
            status = 'warning'
            icon = "⚠️"
        else:
            status = 'fail'
            icon = "❌"

        return {
            'count': len(long_sentences),
            'percentage': round(long_pct, 1),
            'long_sentences': long_sentences[:5],  # Show first 5
            'status': status,
            'target': '<20% over 25 words',
            'message': f"{icon} Long sentences (>25 words): {len(long_sentences)} ({round(long_pct, 1)}%)"
        }

    def detect_complex_words(self) -> Dict[str, any]:
        """Find most complex words."""
        word_syllables = {}
        for word in set(self.words):
            syllable_count = self._count_syllables_in_word(word)
            if syllable_count >= 4:  # Very complex
                word_syllables[word] = syllable_count

        # Sort by syllable count
        complex_words = sorted(word_syllables.items(), key=lambda x: x[1], reverse=True)[:20]

        return {
            'count': len(complex_words),
            'examples': complex_words[:10],  # Top 10
            'message': f"Found {len(complex_words)} words with 4+ syllables"
        }

    def get_overall_assessment(self) -> Dict[str, any]:
        """Get overall readability assessment."""
        ease = self.flesch_reading_ease()
        grade = self.flesch_kincaid_grade_level()
        sentences = self.analyze_sentence_length()
        words = self.analyze_word_complexity()
        passive = self.detect_passive_voice()
        long_sent = self.detect_long_sentences()

        # Count passes and fails
        checks = [ease, grade, sentences, words, passive, long_sent]
        passes = sum(1 for c in checks if c.get('status') == 'pass')
        warnings = sum(1 for c in checks if c.get('status') == 'warning')
        fails = sum(1 for c in checks if c.get('status') == 'fail')

        # Overall status
        if fails > 0:
            status = 'fail'
            grade_assessment = 'Not Ready'
            icon = "❌"
        elif warnings > 2:
            status = 'warning'
            grade_assessment = 'Needs Improvement'
            icon = "⚠️"
        else:
            status = 'pass'
            grade_assessment = 'Excellent'
            icon = "✅"

        return {
            'status': status,
            'grade': grade_assessment,
            'icon': icon,
            'checks_passed': passes,
            'checks_warned': warnings,
            'checks_failed': fails,
            'total_checks': len(checks),
            'non_native_friendly': passes >= 5 and fails == 0,
            'message': f"{icon} Overall: {grade_assessment} ({passes}/{len(checks)} passed)"
        }


def print_report(validation_results: Dict[str, any]) -> None:
    """Print formatted readability report."""
    print("\n" + "="*80)
    print("READABILITY SCORE REPORT")
    print("Focus: Non-Native English Speakers")
    print("="*80 + "\n")

    # Overall Assessment
    print("🎯 OVERALL ASSESSMENT")
    print("-" * 80)
    overall = validation_results['overall_assessment']
    print(overall['message'])
    print(f"Non-Native Friendly: {'✅ YES' if overall['non_native_friendly'] else '❌ NO'}")
    print(f"Checks: {overall['checks_passed']} passed, {overall['checks_warned']} warnings, {overall['checks_failed']} failed")
    print()

    # Flesch Reading Ease
    print("📖 FLESCH READING EASE")
    print("-" * 80)
    ease = validation_results['flesch_kincaid_ease']
    print(ease['message'])
    print(f"  Score: {ease['score']}/100 (target: {ease['target']})")
    print(f"  Level: {ease['level']}")
    print()

    # Grade Level
    print("🎓 FLESCH-KINCAID GRADE LEVEL")
    print("-" * 80)
    grade = validation_results['flesch_kincaid_grade']
    print(grade['message'])
    print()

    # Sentence Length
    print("📏 SENTENCE LENGTH")
    print("-" * 80)
    sentences = validation_results['sentence_stats']
    print(sentences['message'])
    print(f"  Average: {sentences['average']} words (target: {sentences['target']})")
    print(f"  Range: {sentences['min']} - {sentences['max']} words")
    print("\n  Distribution:")
    dist = sentences['distribution']
    print(f"    • Short (1-10 words): {dist['short_1_10']}")
    print(f"    • Medium (11-20 words): {dist['medium_11_20']}")
    print(f"    • Long (21-30 words): {dist['long_21_30']}")
    print(f"    • Very Long (30+ words): {dist['very_long_30_plus']}")
    print()

    # Word Complexity
    print("📚 WORD COMPLEXITY")
    print("-" * 80)
    words = validation_results['word_stats']
    print(words['message'])
    print(f"  Complex words (3+ syllables): {words['complex_word_count']} ({words['complex_word_percentage']}%)")
    print(f"  Average word length: {words['average_word_length']} characters")
    print()

    # Passive Voice
    print("🗣️  PASSIVE VOICE")
    print("-" * 80)
    passive = validation_results['passive_voice']
    print(passive['message'])
    print(f"  Instances: {passive['passive_count']}")
    print()

    # Long Sentences
    print("⚠️  LONG SENTENCES (>25 WORDS)")
    print("-" * 80)
    long_sent = validation_results['long_sentences']
    print(long_sent['message'])
    if long_sent['long_sentences']:
        print("\n  Examples:")
        for ls in long_sent['long_sentences'][:3]:
            print(f"    • {ls['word_count']} words: {ls['preview']}")
    print()

    # Complex Words
    print("🔤 MOST COMPLEX WORDS (4+ SYLLABLES)")
    print("-" * 80)
    complex = validation_results['complex_words']
    print(complex['message'])
    if complex['examples']:
        print("\n  Examples:")
        for word, syllables in complex['examples'][:10]:
            print(f"    • {word} ({syllables} syllables)")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)

    if overall['status'] == 'fail':
        print("❌ READABILITY: NOT READY for non-native English speakers")
        print("\nAction Required:")
        print("  1. Simplify sentence structure (aim for 15-20 words average)")
        print("  2. Replace complex words with simpler alternatives")
        print("  3. Convert passive voice to active voice")
        print("  4. Break up long sentences (>25 words)")
    elif overall['status'] == 'warning':
        print("⚠️ READABILITY: ACCEPTABLE but could be improved")
        print("\nSuggestions:")
        print("  • Review warnings above and make targeted improvements")
        print("  • Focus on simplifying the most complex sections")
    else:
        print("✅ READABILITY: EXCELLENT for non-native English speakers")
        print("\nThis content is accessible and easy to understand!")

    print("="*80 + "\n")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python readability-scorer.py <markdown_file>")
        print("Example: python readability-scorer.py draft.md")
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
    scorer = ReadabilityScorer(content)
    results = scorer.validate_all()

    # Print report
    print_report(results)

    # Exit with error code if validation fails
    if results['overall_assessment']['status'] == 'fail':
        sys.exit(1)


if __name__ == "__main__":
    main()
