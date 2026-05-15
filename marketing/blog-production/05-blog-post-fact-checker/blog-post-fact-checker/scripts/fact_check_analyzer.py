#!/usr/bin/env python3
"""
Fact Check Analyzer

Automated claim analysis and report generation for blog post fact-checking.

Usage:
    python3 scripts/fact_check_analyzer.py draft.md "target keyword"

This script:
1. Parses markdown content
2. Extracts factual claims by category
3. Generates structured output for Exa.ai verification
4. Formats results into Markdown reports

Note: This script extracts and organizes claims. The actual Exa.ai verification
should be performed using the MCP tool mcp__MCP_DOCKER__web_search_exa
"""

import sys
import re
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from pathlib import Path

# Import claim extraction utilities
try:
    from claim_extractor import (
        extract_claims,
        Claim,
        ClaimType,
        Priority,
        format_claims_for_report
    )
except ImportError:
    print("Error: claim_extractor.py not found in the same directory")
    print("Make sure both scripts are in the scripts/ directory")
    sys.exit(1)


class FactCheckAnalyzer:
    """Analyzes blog post content and generates fact-check reports."""

    def __init__(self, content: str, keyword: str = ""):
        self.content = content
        self.keyword = keyword
        self.claims = []
        self.verification_results = []

    def parse_content(self) -> Dict[str, any]:
        """
        Parse markdown content and extract metadata.

        Returns:
            Dict with content metadata
        """
        lines = self.content.split('\n')
        word_count = len(self.content.split())

        # Try to extract title (first H1)
        title = "Untitled"
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break

        # Count headings
        h2_count = len([l for l in lines if l.startswith('## ')])
        h3_count = len([l for l in lines if l.startswith('### ')])

        return {
            'title': title,
            'word_count': word_count,
            'h2_count': h2_count,
            'h3_count': h3_count,
            'line_count': len(lines)
        }

    def extract_all_claims(self) -> List[Claim]:
        """
        Extract all claims from content.

        Returns:
            List of Claim objects
        """
        self.claims = extract_claims(self.content)
        return self.claims

    def generate_exa_queries(self) -> List[Dict[str, any]]:
        """
        Generate Exa.ai search queries for each claim.

        Returns:
            List of query specifications
        """
        queries = []

        for claim in self.claims:
            query_spec = {
                'claim': claim.text,
                'claim_type': claim.claim_type.value,
                'priority': claim.priority.value,
                'query': self._construct_query(claim),
                'num_results': self._get_num_results(claim)
            }
            queries.append(query_spec)

        return queries

    def _construct_query(self, claim: Claim) -> str:
        """
        Construct appropriate Exa search query based on claim type.

        Args:
            claim: Claim object to create query for

        Returns:
            Search query string
        """
        text = claim.text.lower()

        # Extract key terms
        words = text.split()
        key_terms = [w for w in words if len(w) > 4 and w.isalpha()][:5]

        if claim.claim_type == ClaimType.STATISTIC:
            # For statistics, include year and authority sources
            topic = ' '.join(key_terms)
            return f"{topic} statistics 2024 2025"

        elif claim.claim_type == ClaimType.PRODUCT:
            # For product claims, search for official documentation
            # Try to extract product name
            product_match = re.search(r'(\w+)\s+(?:includes?|features?|supports?)', text)
            if product_match:
                product_name = product_match.group(1)
                feature = ' '.join(key_terms)
                return f"{product_name} {feature} documentation official"
            return f"{' '.join(key_terms)} documentation official"

        elif claim.claim_type == ClaimType.TREND:
            # For trends, search for research reports
            topic = ' '.join(key_terms)
            return f"{topic} report 2024 Gartner Forrester"

        elif claim.claim_type == ClaimType.TECHNICAL:
            # For technical claims, search for documentation
            topic = ' '.join(key_terms)
            return f"{topic} how it works documentation"

        elif claim.claim_type == ClaimType.COMPARATIVE:
            # For comparative claims, search for reviews and comparisons
            topic = ' '.join(key_terms)
            return f"{topic} comparison review 2024"

        elif claim.claim_type == ClaimType.TEMPORAL:
            # For temporal claims, include the year mentioned
            year_match = re.search(r'\d{4}', text)
            if year_match:
                year = year_match.group(0)
                topic = ' '.join(key_terms)
                return f"{topic} {year}"
            return ' '.join(key_terms)

        elif claim.claim_type == ClaimType.ATTRIBUTION:
            # For attributed claims, search for the original source
            source_match = re.search(r'according to (\w+)', text)
            if source_match:
                source = source_match.group(1)
                topic = ' '.join(key_terms)
                return f"{source} {topic} 2024"
            return ' '.join(key_terms)

        # Default query
        return ' '.join(key_terms)

    def _get_num_results(self, claim: Claim) -> int:
        """
        Determine appropriate number of search results based on claim priority.

        Args:
            claim: Claim object

        Returns:
            Number of results to request
        """
        if claim.priority == Priority.CRITICAL:
            return 5  # More results for critical claims
        elif claim.priority == Priority.HIGH:
            return 4
        elif claim.priority == Priority.MEDIUM:
            return 3
        else:
            return 2

    def evaluate_source_authority(self, url: str, domain: str) -> str:
        """
        Evaluate source authority tier from URL/domain.

        Args:
            url: Full URL of source
            domain: Domain name

        Returns:
            "Tier 1", "Tier 2", or "Tier 3"
        """
        domain_lower = domain.lower()

        # Tier 1 sources (Always acceptable)
        tier1_domains = [
            'gartner.com', 'forrester.com', 'mckinsey.com', 'deloitte.com',
            'hbr.org', 'harvard.edu', 'mit.edu', 'stanford.edu',
            'hubspot.com', 'salesforce.com', 'adobe.com',
            'forbes.com', 'wsj.com', 'bloomberg.com', 'reuters.com',
            'nytimes.com', 'techcrunch.com'
        ]

        for tier1 in tier1_domains:
            if tier1 in domain_lower:
                return "Tier 1"

        # Tier 2 sources (Acceptable)
        tier2_indicators = [
            'research', 'institute', 'university', '.edu', '.gov',
            'journal', 'publication', 'news'
        ]

        for indicator in tier2_indicators:
            if indicator in domain_lower:
                return "Tier 2"

        # Check if it's a known SaaS company blog (Tier 2 in their domain)
        known_saas = [
            'intercom', 'drift', 'zendesk', 'mailchimp', 'shopify',
            'stripe', 'twilio', 'slack', 'zoom', 'asana'
        ]

        for saas in known_saas:
            if saas in domain_lower:
                return "Tier 2"

        # Default to Tier 3 (Avoid)
        return "Tier 3"

    def generate_report_template(self) -> str:
        """
        Generate a complete fact-check report template with extracted claims.

        Returns:
            Markdown formatted report template
        """
        metadata = self.parse_content()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        date = datetime.now().strftime('%Y-%m-%d')

        # Count claims by priority
        critical = [c for c in self.claims if c.priority == Priority.CRITICAL]
        high = [c for c in self.claims if c.priority == Priority.HIGH]
        medium = [c for c in self.claims if c.priority == Priority.MEDIUM]
        low = [c for c in self.claims if c.priority == Priority.LOW]

        # Count claims by type
        stats = [c for c in self.claims if c.claim_type == ClaimType.STATISTIC]
        products = [c for c in self.claims if c.claim_type == ClaimType.PRODUCT]
        trends = [c for c in self.claims if c.claim_type == ClaimType.TREND]

        report = f"""# Fact-Check Report: {metadata['title']}

**Generated:** {timestamp}
**Target Keyword:** {self.keyword if self.keyword else 'Not specified'}
**Total Claims Analyzed:** {len(self.claims)}
**Verification Status:** [TO BE COMPLETED AFTER VERIFICATION]

---

## Executive Summary

[TO BE COMPLETED: 2-3 sentence overview of fact-check results]

**Total Claims Extracted:**
- {len(critical)} CRITICAL priority
- {len(high)} HIGH priority
- {len(medium)} MEDIUM priority
- {len(low)} LOW priority

**By Type:**
- {len(stats)} Statistics
- {len(products)} Product Features
- {len(trends)} Industry Trends
- {len(self.claims) - len(stats) - len(products) - len(trends)} Other types

**DECISION:** [TO BE COMPLETED: PASS / MINOR ISSUES / FAIL]

---

## Critical Issues

[TO BE COMPLETED: List any CRITICAL priority claims that failed verification]

---

## Detailed Verification Results

"""

        # Add each claim with verification template
        for i, claim in enumerate(self.claims, 1):
            query = self._construct_query(claim)
            num_results = self._get_num_results(claim)

            report += f"""### CLAIM #{i}: {claim.text[:80]}...

- **Category:** {claim.claim_type.value}
- **Priority:** {claim.priority.value}
- **Status:** [TO BE VERIFIED] ✅ VERIFIED / ⚠️ PARTIALLY VERIFIED / ❌ UNSUPPORTED / 🔍 NEEDS ORIGINAL SOURCE
- **Confidence:** [TO BE COMPLETED] High / Medium / Low

**Full Claim Text:**
```
{claim.text}
```

**Context:**
```
...{claim.context_before[-100:] if claim.context_before else 'No prior context'}
{claim.text}
{claim.context_after[:100] if claim.context_after else 'No following context'}...
```

**Verification Instructions:**

1. **Exa.ai Query:**
   ```
   mcp__MCP_DOCKER__web_search_exa(
       query="{query}",
       numResults={num_results}
   )
   ```

2. **For Each Result:**
   - Check domain authority (Tier 1/2/3)
   - Verify claim is supported
   - Note publication date
   - Identify if original or secondary source

3. **Document Findings:**
   - **Sources Found:**
     1. [URL] - [Domain] - Tier [X] - [Date]
        - Confirms: [What it confirms]
        - Quote: "[relevant excerpt]"
     2. [URL] - [Domain] - Tier [X] - [Date]
        - Confirms: [What it confirms]
        - Quote: "[relevant excerpt]"

   - **Assessment:** [Why verified/unverified/partial]
   - **Recommendation:** [Keep as-is / Update to "[corrected text]" / Remove / Find original source]

---

"""

        # Add summary section
        report += f"""## Summary Statistics

**[TO BE COMPLETED AFTER VERIFICATION]**

- Total Claims: {len(self.claims)}
- ✅ Verified: [X] ([X%])
- ⚠️ Partially Verified: [X] ([X%])
- ❌ Unsupported: [X] ([X%])
- 🔍 Needs Original Source: [X] ([X%])

### By Category:
- Statistics: [X verified / {len(stats)} total]
- Product Features: [X verified / {len(products)} total]
- Industry Trends: [X verified / {len(trends)} total]

### By Priority:
- Critical: [X verified / {len(critical)} total]
- High: [X verified / {len(high)} total]
- Medium: [X verified / {len(medium)} total]
- Low: [X verified / {len(low)} total]

---

## Source Authority Breakdown

**[TO BE COMPLETED AFTER VERIFICATION]**

- Tier 1 Sources Used: [X]
- Tier 2 Sources Used: [X]
- Tier 3 Sources Found: [X] (flagged for replacement)

---

## Recommendations

### Must Fix (Critical)
[TO BE COMPLETED]

### Should Fix (High Priority)
[TO BE COMPLETED]

### Consider Fixing (Medium Priority)
[TO BE COMPLETED]

---

## Next Steps

**[TO BE DETERMINED BASED ON VERIFICATION RESULTS]**

**If PASS:**
Proceed to editing-checklist skill for content editing and optimization.

**If MINOR ISSUES:**
Review recommendations and decide whether to:
- Make quick corrections now
- Proceed to editing and fix during that phase
- Return to blog-post-creation for more substantial changes

**If FAIL:**
Return content to blog-post-creation skill with this fact-check report. Address all critical and high-priority issues before proceeding.

---

## Verification Methodology

- **Tool Used:** mcp__MCP_DOCKER__web_search_exa
- **Date Preference:** 2024-2025 sources
- **Source Authority:** Tier 1/2 preferred, Tier 3 avoided
- **Cross-reference Threshold:** 2+ authoritative sources for verification
- **Total Exa Queries Planned:** {len(self.claims)}
- **Total Sources to Review:** [TO BE DETERMINED]

---

## Appendix: All Exa Queries

Below are all the Exa.ai queries to be executed for verification:

"""

        # Add all queries as reference
        queries = self.generate_exa_queries()
        for i, query_spec in enumerate(queries, 1):
            report += f"""{i}. **[{query_spec['priority']}]** {query_spec['claim'][:50]}...
   - Query: `"{query_spec['query']}"`
   - NumResults: {query_spec['num_results']}
   - Type: {query_spec['claim_type']}

"""

        return report


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python3 fact_check_analyzer.py <markdown_file> [keyword]")
        print('Example: python3 fact_check_analyzer.py draft.md "HubSpot AI agents"')
        sys.exit(1)

    file_path = sys.argv[1]
    keyword = sys.argv[2] if len(sys.argv) > 2 else ""

    # Read markdown file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    # Create analyzer
    print(f"📊 Analyzing: {file_path}")
    print(f"🎯 Keyword: {keyword if keyword else 'Not specified'}")
    print()

    analyzer = FactCheckAnalyzer(content, keyword)

    # Extract claims
    print("🔍 Extracting claims...")
    claims = analyzer.extract_all_claims()
    print(f"✅ Found {len(claims)} claims to verify")
    print()

    # Show claim summary
    print(format_claims_for_report(claims))
    print()

    # Generate report template
    print("📝 Generating fact-check report template...")
    report = analyzer.generate_report_template()

    # Save report
    timestamp = datetime.now().strftime('%Y-%m-%d')
    keyword_slug = keyword.replace(' ', '-').lower() if keyword else 'blog-post'
    output_file = f"fact-check-report-{keyword_slug}-{timestamp}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ Report template saved to: {output_file}")
    print()
    print("📋 Next Steps:")
    print("1. Open the report template")
    print("2. For each claim, execute the Exa.ai query specified")
    print("3. Document verification results in the template")
    print("4. Complete the summary statistics")
    print("5. Make final PASS/FAIL decision")
    print("6. Display completed report as artifact")


if __name__ == "__main__":
    main()
