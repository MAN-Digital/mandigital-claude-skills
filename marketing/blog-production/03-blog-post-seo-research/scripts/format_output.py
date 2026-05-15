#!/usr/bin/env python3
"""
Format DataForSEO pre-research results into structured output.

This script helps format raw DataForSEO tool results into the structured
format expected by the blog-post-creation skill.

Usage:
    python3 format_output.py

The script will prompt for input and generate formatted output.
"""

import json
from datetime import datetime
from typing import Dict, List, Any


def format_search_intent(data: Dict[str, Any]) -> str:
    """Format search intent data."""
    intent_types = data.get('intent_types', {})
    informational = intent_types.get('informational', 0)
    transactional = intent_types.get('transactional', 0)

    suitable = "YES" if informational > 60 else "NO"

    return f"""SEARCH INTENT:
- Informational: {informational}%
- Transactional: {transactional}%
- ✅ Blog post format appropriate: {suitable}"""


def format_keyword_metrics(data: Dict[str, Any]) -> str:
    """Format keyword overview data."""
    volume = data.get('search_volume', 0)
    competition = data.get('competition', 'unknown')
    difficulty = data.get('keyword_difficulty', 0)

    # Determine trend from monthly data
    monthly = data.get('monthly_searches', [])
    trend = "stable"
    if len(monthly) >= 2:
        recent = monthly[0].get('search_volume', 0)
        older = monthly[-1].get('search_volume', 0)
        if recent > older * 1.1:
            trend = "rising"
        elif recent < older * 0.9:
            trend = "declining"

    return f"""KEYWORD METRICS:
- Search volume: {volume:,}/month
- Competition: {competition}
- Keyword difficulty: {difficulty}
- Trend: {trend}"""


def format_serp_urls(items: List[Dict[str, Any]]) -> str:
    """Format SERP results."""
    urls = []
    for i, item in enumerate(items[:10], 1):
        url = item.get('url', '')
        urls.append(f"{i}. {url}")

    return "TOP 10 SERP COMPETITORS (USE THESE URLS FOR ANALYSIS):\n" + "\n".join(urls)


def format_competitor_authority(domains: List[Dict[str, Any]]) -> str:
    """Format domain authority data."""
    authority = []
    for i, domain in enumerate(domains[:3], 1):
        name = domain.get('target', 'unknown')
        rank = domain.get('domain_rank', 0)
        keywords = domain.get('keywords_count', 0)
        traffic = domain.get('traffic', 0)

        authority.append(
            f"{i}. {name} - Rank: {rank} - Organic Keywords: {keywords:,} - Traffic: {traffic:,}/mo"
        )

    return "TOP 3 COMPETITOR AUTHORITY:\n" + "\n".join(authority)


def categorize_keywords(keywords: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Categorize keywords by search volume."""
    high = []  # 300+
    medium = []  # 100-299
    lsi = []  # <100

    for kw in keywords:
        keyword = kw.get('keyword', '')
        volume = kw.get('search_volume', 0)

        if volume >= 300:
            high.append(f"- {keyword} - Vol: {volume}")
        elif volume >= 100:
            medium.append(f"- {keyword} - Vol: {volume}")
        elif volume > 0:
            lsi.append(keyword)

    return {
        'h2': high[:6],  # Top 6 for H2
        'h3': medium[:8],  # Top 8 for H3
        'lsi': lsi[:10]  # Top 10 for LSI
    }


def format_related_keywords(categorized: Dict[str, List[str]]) -> str:
    """Format related keywords by category."""
    h2_section = "H2 Opportunities (high-volume):\n" + "\n".join(categorized['h2'])
    h3_section = "H3 Opportunities (medium-volume):\n" + "\n".join(categorized['h3'])
    lsi_section = "LSI Keywords (natural integration):\n- " + ", ".join(categorized['lsi'])

    return f"""RELATED KEYWORDS FOR STRUCTURE:
{h2_section}

{h3_section}

{lsi_section}"""


def generate_full_output(
    keyword: str,
    intent_data: Dict[str, Any],
    metrics_data: Dict[str, Any],
    serp_items: List[Dict[str, Any]],
    authority_data: List[Dict[str, Any]],
    related_keywords: List[Dict[str, Any]]
) -> str:
    """Generate complete formatted output."""

    date = datetime.now().strftime('%Y-%m-%d')

    intent_section = format_search_intent(intent_data)
    metrics_section = format_keyword_metrics(metrics_data)
    serp_section = format_serp_urls(serp_items)
    authority_section = format_competitor_authority(authority_data)

    categorized = categorize_keywords(related_keywords)
    keywords_section = format_related_keywords(categorized)

    return f"""=== DATAFORSEO SEO RESEARCH RESULTS ===
Date: {date}
Primary Keyword: {keyword}

{intent_section}

{metrics_section}

{serp_section}

{authority_section}

{keywords_section}

=== END DATAFORSEO SEO RESEARCH ==="""


def validate_output(output: str) -> List[str]:
    """Validate the output has all required sections."""
    required_sections = [
        "SEARCH INTENT:",
        "KEYWORD METRICS:",
        "TOP 10 SERP COMPETITORS",
        "TOP 3 COMPETITOR AUTHORITY:",
        "RELATED KEYWORDS FOR STRUCTURE:",
        "H2 Opportunities",
        "H3 Opportunities",
        "LSI Keywords"
    ]

    missing = []
    for section in required_sections:
        if section not in output:
            missing.append(section)

    return missing


def main():
    """Interactive mode for formatting output."""
    print("DataForSEO Output Formatter")
    print("=" * 50)
    print("\nThis script helps format raw DataForSEO results.")
    print("\nYou'll be prompted to paste JSON data from each tool.")
    print("\n" + "=" * 50 + "\n")

    # Get keyword
    keyword = input("Enter primary keyword: ").strip()

    # Get search intent data
    print("\n1. Paste search_intent JSON (or press Enter to skip):")
    intent_json = input().strip()
    intent_data = json.loads(intent_json) if intent_json else {}

    # Get keyword metrics
    print("\n2. Paste keyword_overview JSON (or press Enter to skip):")
    metrics_json = input().strip()
    metrics_data = json.loads(metrics_json) if metrics_json else {}

    # Get SERP data
    print("\n3. Paste serp_organic_live_advanced JSON (or press Enter to skip):")
    serp_json = input().strip()
    serp_data = json.loads(serp_json) if serp_json else {}
    serp_items = serp_data.get('items', [])

    # Get authority data
    print("\n4. Paste domain_rank_overview JSON for top 3 domains (or press Enter to skip):")
    authority_json = input().strip()
    authority_data = json.loads(authority_json) if authority_json else []

    # Get related keywords
    print("\n5. Paste related_keywords JSON (or press Enter to skip):")
    related_json = input().strip()
    related_data = json.loads(related_json) if related_json else {}
    related_items = related_data.get('items', [])

    # Generate output
    output = generate_full_output(
        keyword,
        intent_data,
        metrics_data,
        serp_items,
        authority_data,
        related_items
    )

    # Validate
    missing = validate_output(output)

    print("\n" + "=" * 50)
    print("FORMATTED OUTPUT:")
    print("=" * 50 + "\n")
    print(output)

    if missing:
        print("\n" + "=" * 50)
        print("⚠️  WARNING: Missing sections:")
        for section in missing:
            print(f"  - {section}")
        print("=" * 50)
    else:
        print("\n✅ Output is complete and ready to use!")

    # Save to file
    save = input("\nSave to file? (y/n): ").strip().lower()
    if save == 'y':
        filename = f"seo-research-{keyword.replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}.txt"
        with open(filename, 'w') as f:
            f.write(output)
        print(f"✅ Saved to: {filename}")


if __name__ == "__main__":
    main()
