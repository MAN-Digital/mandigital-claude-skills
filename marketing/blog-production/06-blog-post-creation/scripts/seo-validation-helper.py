#!/usr/bin/env python3
"""
SEO Validation Helper Script

This script validates on-page SEO elements in markdown blog posts.
Use during Phase 3.5 (Post-Draft SEO Validation) and Phase 5 (Post-Editing SEO Verification).

Usage:
    python seo-validation-helper.py <markdown_file> <target_keyword>

Example:
    python seo-validation-helper.py draft.md "HubSpot AI agents"
"""

import re
import sys
from typing import Dict, List, Tuple
from collections import Counter


class SEOValidator:
    """Validates on-page SEO elements in markdown content."""

    def __init__(self, content: str, target_keyword: str):
        self.content = content
        self.target_keyword = target_keyword.lower()
        self.keyword_variations = self._generate_keyword_variations()
        self.lines = content.split('\n')

    def _generate_keyword_variations(self) -> List[str]:
        """Generate keyword variations for matching."""
        base = self.target_keyword
        words = base.split()

        variations = [
            base,  # exact match
            ' '.join(words[::-1]),  # reversed
        ]

        # Add partial matches (for multi-word keywords)
        if len(words) > 1:
            variations.extend(words)  # individual words

        return list(set(variations))

    def validate_all(self) -> Dict[str, any]:
        """Run all validation checks."""
        return {
            'h1': self.validate_h1(),
            'h2': self.validate_h2(),
            'h3': self.validate_h3(),
            'heading_hierarchy': self.validate_heading_hierarchy(),
            'keyword_placement': self.validate_keyword_placement(),
            'keyword_density': self.validate_keyword_density(),
            'meta_elements': self.validate_meta_elements(),
            'word_count': self.validate_word_count(),
            'links': self.validate_links(),
            'structure': self.validate_structure()
        }

    def validate_h1(self) -> Dict[str, any]:
        """Validate H1 heading."""
        h1_pattern = r'^# (.+)$'
        h1_matches = []

        for line in self.lines:
            match = re.match(h1_pattern, line)
            if match:
                h1_matches.append(match.group(1))

        h1_count = len(h1_matches)
        has_keyword = any(self.target_keyword in h1.lower() for h1 in h1_matches)

        return {
            'count': h1_count,
            'h1s': h1_matches,
            'status': 'pass' if h1_count == 1 else 'fail',
            'has_keyword': has_keyword,
            'keyword_status': 'pass' if has_keyword else 'fail',
            'message': self._get_h1_message(h1_count, has_keyword)
        }

    def _get_h1_message(self, count: int, has_keyword: bool) -> str:
        """Get H1 validation message."""
        if count == 0:
            return "❌ No H1 found. Add a single H1 with target keyword."
        elif count > 1:
            return f"❌ Multiple H1s found ({count}). Should have exactly 1."
        elif not has_keyword:
            return f"⚠️ H1 doesn't include target keyword '{self.target_keyword}'."
        else:
            return f"✅ H1 is valid with keyword '{self.target_keyword}'."

    def validate_h2(self) -> Dict[str, any]:
        """Validate H2 headings."""
        h2_pattern = r'^## (.+)$'
        h2_matches = []

        for line in self.lines:
            match = re.match(h2_pattern, line)
            if match:
                h2_matches.append(match.group(1))

        h2_count = len(h2_matches)
        h2_with_keyword = sum(1 for h2 in h2_matches if any(var in h2.lower() for var in self.keyword_variations))

        return {
            'count': h2_count,
            'h2s': h2_matches,
            'with_keyword': h2_with_keyword,
            'status': 'pass' if 5 <= h2_count <= 8 else 'warning',
            'message': self._get_h2_message(h2_count, h2_with_keyword)
        }

    def _get_h2_message(self, count: int, with_keyword: int) -> str:
        """Get H2 validation message."""
        if count < 5:
            return f"⚠️ Only {count} H2s. Recommend 5-8 for better structure."
        elif count > 8:
            return f"⚠️ {count} H2s found. Consider 5-8 for optimal structure."
        else:
            return f"✅ {count} H2s found (optimal range). {with_keyword} include keyword variations."

    def validate_h3(self) -> Dict[str, any]:
        """Validate H3 headings."""
        h3_pattern = r'^### (.+)$'
        h3_matches = []

        for line in self.lines:
            match = re.match(h3_pattern, line)
            if match:
                h3_matches.append(match.group(1))

        h3_count = len(h3_matches)

        return {
            'count': h3_count,
            'h3s': h3_matches,
            'status': 'pass' if h3_count >= 10 else 'warning',
            'message': f"✅ {h3_count} H3s found." if h3_count >= 10 else f"⚠️ Only {h3_count} H3s. Consider adding more for depth."
        }

    def validate_heading_hierarchy(self) -> Dict[str, any]:
        """Validate heading hierarchy (no H3 before H2, etc.)."""
        issues = []
        last_level = 0

        for i, line in enumerate(self.lines, 1):
            if line.startswith('### '):
                current_level = 3
            elif line.startswith('## '):
                current_level = 2
            elif line.startswith('# '):
                current_level = 1
            else:
                continue

            # Check for skipped levels
            if current_level > last_level + 1:
                issues.append(f"Line {i}: H{current_level} appears without H{current_level-1} before it")

            last_level = current_level

        return {
            'status': 'pass' if not issues else 'fail',
            'issues': issues,
            'message': "✅ Heading hierarchy is correct." if not issues else f"❌ {len(issues)} hierarchy issue(s) found."
        }

    def validate_keyword_placement(self) -> Dict[str, any]:
        """Validate keyword placement in critical locations."""
        content_lower = self.content.lower()

        # First 100 words
        first_100_words = ' '.join(content_lower.split()[:100])
        in_first_100 = self.target_keyword in first_100_words

        # Last 100 words (conclusion)
        last_100_words = ' '.join(content_lower.split()[-100:])
        in_conclusion = self.target_keyword in last_100_words

        # In H1 (checked separately, but include for completeness)
        in_h1 = self.validate_h1()['has_keyword']

        # In H2s
        h2_result = self.validate_h2()
        in_h2s = h2_result['with_keyword'] > 0

        placements = {
            'h1': in_h1,
            'first_100_words': in_first_100,
            'h2s': in_h2s,
            'conclusion': in_conclusion
        }

        passed = sum(placements.values())

        return {
            'placements': placements,
            'passed': passed,
            'total': 4,
            'status': 'pass' if passed >= 3 else 'warning',
            'message': f"{'✅' if passed >= 3 else '⚠️'} Keyword present in {passed}/4 critical locations."
        }

    def validate_keyword_density(self) -> Dict[str, any]:
        """Validate keyword density (should be 1.5-2.5%)."""
        words = self.content.lower().split()
        total_words = len(words)

        # Count exact keyword matches
        keyword_count = self.content.lower().count(self.target_keyword)

        # Calculate density
        density = (keyword_count / total_words * 100) if total_words > 0 else 0

        # Determine status
        if 1.5 <= density <= 2.5:
            status = 'pass'
            message = f"✅ Keyword density {density:.2f}% (optimal: 1.5-2.5%)"
        elif density < 1.5:
            status = 'warning'
            message = f"⚠️ Keyword density {density:.2f}% (low). Consider adding more mentions."
        else:
            status = 'fail'
            message = f"❌ Keyword density {density:.2f}% (too high). Risk of over-optimization."

        return {
            'density': round(density, 2),
            'keyword_count': keyword_count,
            'total_words': total_words,
            'status': status,
            'message': message
        }

    def validate_meta_elements(self) -> Dict[str, any]:
        """Validate meta title and description (look for them in markdown frontmatter or comments)."""
        meta_title = None
        meta_description = None

        # Look for meta elements (often in comments or frontmatter)
        for line in self.lines[:20]:  # Check first 20 lines
            if 'seo title' in line.lower() or 'meta title' in line.lower():
                # Extract title (might be in format: <!-- SEO Title: ... -->)
                match = re.search(r'(?:seo title|meta title)[:\s]+(.+?)(?:-->|$)', line, re.I)
                if match:
                    meta_title = match.group(1).strip()

            if 'seo description' in line.lower() or 'meta description' in line.lower():
                match = re.search(r'(?:seo description|meta description)[:\s]+(.+?)(?:-->|$)', line, re.I)
                if match:
                    meta_description = match.group(1).strip()

        results = {}

        # Validate title
        if meta_title:
            title_len = len(meta_title)
            title_has_keyword = self.target_keyword in meta_title.lower()
            title_status = 'pass' if (50 <= title_len <= 60 and title_has_keyword) else 'warning'
            results['title'] = {
                'content': meta_title,
                'length': title_len,
                'has_keyword': title_has_keyword,
                'status': title_status,
                'message': f"{'✅' if title_status == 'pass' else '⚠️'} Meta title: {title_len} chars (optimal: 50-60)"
            }
        else:
            results['title'] = {
                'content': None,
                'status': 'fail',
                'message': "❌ Meta title not found. Add in frontmatter or comment."
            }

        # Validate description
        if meta_description:
            desc_len = len(meta_description)
            desc_has_keyword = self.target_keyword in meta_description.lower()
            desc_status = 'pass' if (150 <= desc_len <= 160 and desc_has_keyword) else 'warning'
            results['description'] = {
                'content': meta_description,
                'length': desc_len,
                'has_keyword': desc_has_keyword,
                'status': desc_status,
                'message': f"{'✅' if desc_status == 'pass' else '⚠️'} Meta description: {desc_len} chars (optimal: 150-160)"
            }
        else:
            results['description'] = {
                'content': None,
                'status': 'fail',
                'message': "❌ Meta description not found. Add in frontmatter or comment."
            }

        return results

    def validate_word_count(self) -> Dict[str, any]:
        """Validate word count."""
        # Remove markdown syntax for accurate count
        clean_content = re.sub(r'#+ ', '', self.content)  # Remove heading markers
        clean_content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_content)  # Remove links, keep text
        clean_content = re.sub(r'[*_`]', '', clean_content)  # Remove formatting

        words = clean_content.split()
        word_count = len(words)

        if 1200 <= word_count <= 1600:
            status = 'pass'
            message = f"✅ Word count: {word_count} (optimal: 1,200-1,600)"
        elif word_count < 1200:
            status = 'warning'
            message = f"⚠️ Word count: {word_count} (below minimum 1,200)"
        elif word_count > 2500:
            status = 'warning'
            message = f"⚠️ Word count: {word_count} (above maximum 2,500)"
        else:
            status = 'pass'
            message = f"✅ Word count: {word_count} (acceptable range)"

        return {
            'count': word_count,
            'status': status,
            'message': message
        }

    def validate_links(self) -> Dict[str, any]:
        """Validate internal and external links."""
        # Find all markdown links
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = re.findall(link_pattern, self.content)

        internal_links = []
        external_links = []

        for text, url in links:
            # Simple heuristic: relative paths or same domain = internal
            if url.startswith('/') or url.startswith('#') or url.startswith('./'):
                internal_links.append((text, url))
            elif url.startswith('http'):
                external_links.append((text, url))

        internal_count = len(internal_links)
        external_count = len(external_links)

        internal_status = 'pass' if 3 <= internal_count <= 5 else 'warning'
        external_status = 'pass' if 3 <= external_count <= 5 else 'warning'

        return {
            'internal': {
                'count': internal_count,
                'links': internal_links,
                'status': internal_status,
                'message': f"{'✅' if internal_status == 'pass' else '⚠️'} {internal_count} internal links (optimal: 3-5)"
            },
            'external': {
                'count': external_count,
                'links': external_links,
                'status': external_status,
                'message': f"{'✅' if external_status == 'pass' else '⚠️'} {external_count} external links (optimal: 3-5)"
            }
        }

    def validate_structure(self) -> Dict[str, any]:
        """Validate content structure (bullets, visuals, etc.)."""
        # Count bullet sections (lines starting with -, *, or numbers)
        bullet_pattern = r'^[\s]*[-*\d]+\.?\s'
        bullet_lines = [line for line in self.lines if re.match(bullet_pattern, line)]
        bullet_sections = len(bullet_lines)  # Simplified; could group consecutive bullets

        # Count visual placeholders
        visual_pattern = r'\[(Screenshot|Diagram|Chart|Infographic|Image|Visual|Figure)[:\s]'
        visual_placeholders = len(re.findall(visual_pattern, self.content, re.I))

        # Count tables (markdown tables have pipes)
        table_pattern = r'\|.+\|'
        table_lines = [line for line in self.lines if re.match(table_pattern, line.strip())]
        table_count = len(table_lines) // 3  # Approximate: header + separator + data = 3 lines minimum

        # Count bold headers
        bold_header_pattern = r'\*\*[^*]+\*\*'
        bold_headers = len(re.findall(bold_header_pattern, self.content))

        return {
            'bullets': {
                'count': bullet_sections,
                'status': 'pass' if bullet_sections >= 8 else 'warning',
                'message': f"{'✅' if bullet_sections >= 8 else '⚠️'} {bullet_sections} bullet lines (minimum: 8 sections)"
            },
            'visuals': {
                'count': visual_placeholders,
                'status': 'pass' if visual_placeholders >= 2 else 'warning',
                'message': f"{'✅' if visual_placeholders >= 2 else '⚠️'} {visual_placeholders} visual placeholders (minimum: 2)"
            },
            'tables': {
                'count': table_count,
                'status': 'pass' if table_count >= 1 else 'info',
                'message': f"ℹ️ {table_count} table(s) found (optional: 1-2 for comparisons)"
            },
            'bold_headers': {
                'count': bold_headers,
                'status': 'pass' if bold_headers >= 8 else 'warning',
                'message': f"{'✅' if bold_headers >= 8 else '⚠️'} {bold_headers} bold headers (minimum: 8)"
            }
        }


def print_report(validation_results: Dict[str, any], keyword: str) -> None:
    """Print formatted SEO validation report."""
    print("\n" + "="*80)
    print(f"SEO VALIDATION REPORT - Target Keyword: '{keyword}'")
    print("="*80 + "\n")

    # H1 Validation
    print("📌 H1 HEADING")
    print("-" * 80)
    h1 = validation_results['h1']
    print(h1['message'])
    if h1['h1s']:
        print(f"   Found: {h1['h1s'][0]}")
    print()

    # H2 Validation
    print("📌 H2 HEADINGS")
    print("-" * 80)
    h2 = validation_results['h2']
    print(h2['message'])
    print()

    # H3 Validation
    print("📌 H3 HEADINGS")
    print("-" * 80)
    h3 = validation_results['h3']
    print(h3['message'])
    print()

    # Heading Hierarchy
    print("📌 HEADING HIERARCHY")
    print("-" * 80)
    hierarchy = validation_results['heading_hierarchy']
    print(hierarchy['message'])
    if hierarchy['issues']:
        for issue in hierarchy['issues']:
            print(f"   - {issue}")
    print()

    # Keyword Placement
    print("📌 KEYWORD PLACEMENT")
    print("-" * 80)
    placement = validation_results['keyword_placement']
    print(placement['message'])
    for location, present in placement['placements'].items():
        status = "✅" if present else "❌"
        print(f"   {status} {location.replace('_', ' ').title()}")
    print()

    # Keyword Density
    print("📌 KEYWORD DENSITY")
    print("-" * 80)
    density = validation_results['keyword_density']
    print(density['message'])
    print(f"   Keyword appears {density['keyword_count']} times in {density['total_words']} words")
    print()

    # Meta Elements
    print("📌 META ELEMENTS")
    print("-" * 80)
    meta = validation_results['meta_elements']
    print(meta['title']['message'])
    if meta['title']['content']:
        print(f"   Title: {meta['title']['content']}")
    print(meta['description']['message'])
    if meta['description']['content']:
        print(f"   Description: {meta['description']['content'][:80]}...")
    print()

    # Word Count
    print("📌 WORD COUNT")
    print("-" * 80)
    wc = validation_results['word_count']
    print(wc['message'])
    print()

    # Links
    print("📌 LINKS")
    print("-" * 80)
    links = validation_results['links']
    print(links['internal']['message'])
    print(links['external']['message'])
    print()

    # Structure
    print("📌 CONTENT STRUCTURE")
    print("-" * 80)
    structure = validation_results['structure']
    print(structure['bullets']['message'])
    print(structure['visuals']['message'])
    print(structure['tables']['message'])
    print(structure['bold_headers']['message'])
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)

    # Count passes and fails
    all_statuses = []
    for category in validation_results.values():
        if isinstance(category, dict):
            if 'status' in category:
                all_statuses.append(category['status'])
            # Handle nested results
            for subkey, subvalue in category.items():
                if isinstance(subvalue, dict) and 'status' in subvalue:
                    all_statuses.append(subvalue['status'])

    passes = all_statuses.count('pass')
    warnings = all_statuses.count('warning')
    fails = all_statuses.count('fail')
    total = len(all_statuses)

    print(f"✅ Passed: {passes}/{total}")
    print(f"⚠️  Warnings: {warnings}/{total}")
    print(f"❌ Failed: {fails}/{total}")

    if fails > 0:
        print("\n⚠️ ACTION REQUIRED: Fix failed items before proceeding.")
    elif warnings > 0:
        print("\n✅ Good! Address warnings for optimal SEO.")
    else:
        print("\n🎉 EXCELLENT! All SEO checks passed.")

    print("="*80 + "\n")


def main():
    """Main function."""
    if len(sys.argv) < 3:
        print("Usage: python seo-validation-helper.py <markdown_file> <target_keyword>")
        print('Example: python seo-validation-helper.py draft.md "HubSpot AI agents"')
        sys.exit(1)

    file_path = sys.argv[1]
    target_keyword = sys.argv[2]

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
    validator = SEOValidator(content, target_keyword)
    results = validator.validate_all()

    # Print report
    print_report(results, target_keyword)


if __name__ == "__main__":
    main()
