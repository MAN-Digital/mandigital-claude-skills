#!/usr/bin/env python3
"""
Claim Extractor Utility

This module provides functions for identifying and extracting factual claims
from blog post content for verification.

Usage:
    from scripts.claim_extractor import extract_claims, categorize_claim

    claims = extract_claims(markdown_content)
    for claim in claims:
        category = categorize_claim(claim)
        print(f"{claim['text']} - {category}")
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ClaimType(Enum):
    """Types of claims that can be extracted."""
    STATISTIC = "STAT"
    PRODUCT = "PRODUCT"
    TREND = "TREND"
    TECHNICAL = "TECHNICAL"
    COMPARATIVE = "COMPARATIVE"
    TEMPORAL = "TEMPORAL"
    ATTRIBUTION = "ATTRIBUTION"
    UNKNOWN = "UNKNOWN"


class Priority(Enum):
    """Priority levels for claim verification."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class Claim:
    """Represents a factual claim extracted from content."""
    text: str
    context_before: str
    context_after: str
    claim_type: ClaimType
    priority: Priority
    location: str  # intro, body, conclusion
    existing_citation: Optional[str] = None
    line_number: Optional[int] = None


def extract_statistics(text: str) -> List[Dict[str, str]]:
    """
    Extract statistical claims from text.

    Patterns:
    - Percentages: "85% of marketers"
    - Numbers with context: "$4.5 billion market"
    - Growth rates: "30% year-over-year"
    - Ratios: "1 in 3 companies"
    """
    statistics = []

    # Percentage patterns
    percentage_pattern = r'\b(\d+(?:\.\d+)?%)\s+(?:of\s+)?([^\.\n]{10,80})'
    for match in re.finditer(percentage_pattern, text):
        statistics.append({
            'value': match.group(1),
            'context': match.group(2).strip(),
            'full_text': match.group(0)
        })

    # Dollar amounts
    dollar_pattern = r'\$(\d+(?:\.\d+)?(?:\s?(?:million|billion|trillion|k|M|B|T))?)\s+([^\.\n]{10,80})'
    for match in re.finditer(dollar_pattern, text):
        statistics.append({
            'value': f"${match.group(1)}",
            'context': match.group(2).strip(),
            'full_text': match.group(0)
        })

    # Growth rates
    growth_pattern = r'(\d+(?:\.\d+)?%)\s+(?:increase|decrease|growth|decline|rise|drop)\s+([^\.\n]{10,80})'
    for match in re.finditer(growth_pattern, text):
        statistics.append({
            'value': match.group(1),
            'context': f"growth/change: {match.group(2).strip()}",
            'full_text': match.group(0)
        })

    # Ratios (1 in 3, 2 out of 5, etc.)
    ratio_pattern = r'(\d+\s+(?:in|out of)\s+\d+)\s+([^\.\n]{10,80})'
    for match in re.finditer(ratio_pattern, text):
        statistics.append({
            'value': match.group(1),
            'context': match.group(2).strip(),
            'full_text': match.group(0)
        })

    return statistics


def extract_product_claims(text: str) -> List[str]:
    """
    Extract product feature and capability claims.

    Patterns:
    - "Tool X includes/has/features Y"
    - "Platform supports/enables Z"
    - "Native capability to do ABC"
    """
    product_claims = []

    # Feature inclusion patterns
    inclusion_patterns = [
        r'(\w+\s+(?:includes?|has|features?|provides?|offers?)[\s\w,]+)',
        r'((?:platform|tool|system|software)\s+supports?[\s\w,]+)',
        r'(native\s+(?:capability|feature|integration|support)[\s\w,]+)',
        r'(built-in\s+[\s\w,]+)'
    ]

    for pattern in inclusion_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            claim_text = match.group(1).strip()
            if len(claim_text) > 15:  # Filter out very short matches
                product_claims.append(claim_text)

    return product_claims


def extract_temporal_claims(text: str) -> List[str]:
    """
    Extract date, timeline, and temporal claims.

    Patterns:
    - "In 2024..."
    - "Since last year..."
    - "By 2025..."
    """
    temporal_claims = []

    # Year references
    year_pattern = r'((?:in|since|by|during|before|after)\s+\d{4}[^\.\n]{0,80})'
    for match in re.finditer(year_pattern, text, re.IGNORECASE):
        temporal_claims.append(match.group(1).strip())

    # Relative time references
    relative_pattern = r'((?:last|this|next)\s+(?:year|month|quarter|decade)[^\.\n]{0,80})'
    for match in re.finditer(relative_pattern, text, re.IGNORECASE):
        temporal_claims.append(match.group(1).strip())

    return temporal_claims


def is_factual_claim(sentence: str) -> bool:
    """
    Determine if a sentence contains a factual claim that needs verification.

    Returns True if the sentence likely contains verifiable facts.
    """
    # Indicators of factual claims
    factual_indicators = [
        r'\d+%',  # Percentages
        r'\$\d+',  # Dollar amounts
        r'\d+\s+(?:million|billion|thousand)',  # Large numbers
        r'(?:according to|research shows|study found)',  # Attribution
        r'(?:includes?|features?|supports?|enables?)',  # Product claims
        r'(?:is|are)\s+(?:the\s+)?(?:best|top|leading|fastest)',  # Comparative claims
        r'\d{4}',  # Years
    ]

    for indicator in factual_indicators:
        if re.search(indicator, sentence, re.IGNORECASE):
            return True

    # Check for definitive statements (not opinions)
    definitive_patterns = [
        r'(?:can|will|does|has|have|provides?|offers?|supports?)',
    ]

    for pattern in definitive_patterns:
        if re.search(pattern, sentence, re.IGNORECASE):
            # Exclude opinions
            if not re.search(r'(?:believe|think|feel|opinion|might|may|could|should)', sentence, re.IGNORECASE):
                return True

    return False


def get_claim_context(claim_text: str, full_text: str, context_sentences: int = 2) -> Tuple[str, str]:
    """
    Extract context sentences before and after a claim.

    Args:
        claim_text: The claim to find context for
        full_text: The full document text
        context_sentences: Number of sentences to include before/after

    Returns:
        Tuple of (context_before, context_after)
    """
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', full_text)

    # Find the sentence containing the claim
    claim_index = -1
    for i, sentence in enumerate(sentences):
        if claim_text in sentence:
            claim_index = i
            break

    if claim_index == -1:
        return ("", "")

    # Get context before
    start_index = max(0, claim_index - context_sentences)
    context_before = ' '.join(sentences[start_index:claim_index])

    # Get context after
    end_index = min(len(sentences), claim_index + context_sentences + 1)
    context_after = ' '.join(sentences[claim_index + 1:end_index])

    return (context_before, context_after)


def categorize_claim(claim: Claim) -> ClaimType:
    """
    Categorize a claim by its type.

    Returns the ClaimType enum value.
    """
    text = claim.text.lower()

    # Check for statistics
    if re.search(r'\d+%|\$\d+|\d+\s+(?:million|billion)', text):
        return ClaimType.STATISTIC

    # Check for product claims
    if re.search(r'(?:includes?|features?|supports?|native|built-in)', text):
        return ClaimType.PRODUCT

    # Check for trends
    if re.search(r'(?:growing|increasing|declining|trend|shift|adoption)', text):
        return ClaimType.TREND

    # Check for technical claims
    if re.search(r'(?:architecture|algorithm|protocol|system|process|how.*works)', text):
        return ClaimType.TECHNICAL

    # Check for comparative claims
    if re.search(r'(?:better|best|top|leading|faster|superior|versus|vs\.)', text):
        return ClaimType.COMPARATIVE

    # Check for temporal claims
    if re.search(r'\d{4}|(?:last|this|next)\s+(?:year|month|quarter)', text):
        return ClaimType.TEMPORAL

    # Check for attribution
    if re.search(r'(?:according to|said|stated|reported|quoted)', text):
        return ClaimType.ATTRIBUTION

    return ClaimType.UNKNOWN


def assign_priority(claim: Claim) -> Priority:
    """
    Assign verification priority to a claim.

    Returns the Priority enum value.
    """
    text = claim.text.lower()

    # CRITICAL priority keywords
    critical_keywords = [
        r'market size',
        r'revenue',
        r'\$\d+\s+(?:million|billion)',
        r'roi',
        r'return on investment',
        r'security',
        r'compliance',
        r'pricing'
    ]

    for keyword in critical_keywords:
        if re.search(keyword, text):
            return Priority.CRITICAL

    # HIGH priority
    high_keywords = [
        r'(?:includes?|features?|supports?)\s+\w+',
        r'integration',
        r'capability',
        r'adoption rate',
        r'\d+%'
    ]

    for keyword in high_keywords:
        if re.search(keyword, text):
            return Priority.HIGH

    # MEDIUM priority
    medium_keywords = [
        r'trend',
        r'industry',
        r'companies',
        r'businesses',
        r'market'
    ]

    for keyword in medium_keywords:
        if re.search(keyword, text):
            return Priority.MEDIUM

    # Default to LOW
    return Priority.LOW


def extract_claims(markdown_content: str) -> List[Claim]:
    """
    Extract all factual claims from markdown content.

    Args:
        markdown_content: Full blog post content in Markdown format

    Returns:
        List of Claim objects
    """
    claims = []

    # Remove markdown formatting for cleaner text analysis
    clean_text = re.sub(r'#+ ', '', markdown_content)  # Remove heading markers
    clean_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_text)  # Remove links, keep text
    clean_text = re.sub(r'[*_`]', '', clean_text)  # Remove formatting

    # Determine document sections
    lines = markdown_content.split('\n')
    intro_end = 50  # First ~50 lines typically intro
    conclusion_start = len(lines) - 50  # Last ~50 lines typically conclusion

    # Extract by category
    statistics = extract_statistics(clean_text)
    product_claims_text = extract_product_claims(clean_text)
    temporal_claims_text = extract_temporal_claims(clean_text)

    # Process statistics
    for stat in statistics:
        context_before, context_after = get_claim_context(stat['full_text'], clean_text)

        claim = Claim(
            text=stat['full_text'],
            context_before=context_before,
            context_after=context_after,
            claim_type=ClaimType.STATISTIC,
            priority=Priority.CRITICAL,  # Statistics are always high priority
            location="body"  # Would need line analysis for precise location
        )
        claims.append(claim)

    # Process product claims
    for prod_claim in product_claims_text:
        context_before, context_after = get_claim_context(prod_claim, clean_text)

        claim = Claim(
            text=prod_claim,
            context_before=context_before,
            context_after=context_after,
            claim_type=ClaimType.PRODUCT,
            priority=Priority.HIGH,
            location="body"
        )
        claims.append(claim)

    # Process temporal claims
    for temp_claim in temporal_claims_text:
        context_before, context_after = get_claim_context(temp_claim, clean_text)

        claim = Claim(
            text=temp_claim,
            context_before=context_before,
            context_after=context_after,
            claim_type=ClaimType.TEMPORAL,
            priority=Priority.MEDIUM,
            location="body"
        )
        claims.append(claim)

    # Split into sentences and find additional factual claims
    sentences = re.split(r'(?<=[.!?])\s+', clean_text)
    for sentence in sentences:
        if len(sentence) > 20 and is_factual_claim(sentence):
            # Check if not already captured
            if not any(sentence in claim.text for claim in claims):
                context_before, context_after = get_claim_context(sentence, clean_text)

                claim = Claim(
                    text=sentence,
                    context_before=context_before,
                    context_after=context_after,
                    claim_type=ClaimType.UNKNOWN,
                    priority=Priority.MEDIUM,
                    location="body"
                )

                # Categorize and prioritize
                claim.claim_type = categorize_claim(claim)
                claim.priority = assign_priority(claim)

                claims.append(claim)

    return claims


def format_claims_for_report(claims: List[Claim]) -> str:
    """
    Format extracted claims for display in a report.

    Args:
        claims: List of Claim objects

    Returns:
        Formatted string ready for report
    """
    output = []
    output.append("="*80)
    output.append(f"EXTRACTED CLAIMS: {len(claims)} total")
    output.append("="*80)
    output.append("")

    # Group by priority
    for priority in [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
        priority_claims = [c for c in claims if c.priority == priority]
        if priority_claims:
            output.append(f"\n{priority.value} PRIORITY ({len(priority_claims)} claims):")
            output.append("-" * 80)

            for i, claim in enumerate(priority_claims, 1):
                output.append(f"\n{i}. [{claim.claim_type.value}] {claim.text}")
                if claim.context_before:
                    output.append(f"   Context: ...{claim.context_before[-50:]}")

    return '\n'.join(output)


if __name__ == "__main__":
    # Example usage
    sample_text = """
    Recent studies show that 85% of marketers are now using AI tools in their workflows.
    HubSpot includes native AI-powered prospecting agents that automate outreach.
    The market for marketing automation grew by 30% year-over-year in 2024.
    According to Gartner, companies are increasingly adopting integrated platforms.
    """

    claims = extract_claims(sample_text)
    print(format_claims_for_report(claims))
