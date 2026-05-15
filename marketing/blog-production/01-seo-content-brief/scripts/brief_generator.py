#!/usr/bin/env python3
"""
Detailed CSV Brief Generator v4
Creates comprehensive content briefs with:
- Statistics deduplication and assignment
- Word targets per section
- Internal article differentiation
- Consistent CSV/JSON output formats
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class DetailedBriefGeneratorV4:
    """Generate detailed content briefs in v4 8-column CSV format"""
    
    def __init__(self, topic: str, keyword: str):
        self.topic = topic
        self.keyword = keyword
        self.timestamp = datetime.now().strftime("%Y%m%d")
        self.headings = []
        self.statistics = []  # v4: Enhanced statistics tracking
        self.research_data = {
            "entities": {},
            "competitors": [],
            "content_gaps": [],
            "macro_context": "",
            "target_audience": "",
            # v4 additions:
            "exclusion_registry": [],
            "internal_differentiation": [],
            "interlinking": []
        }
    
    def set_macro_context(self, context: str):
        """Set the overall article focus"""
        self.research_data["macro_context"] = context
    
    def set_target_audience(self, audience: str):
        """Set target audience"""
        self.research_data["target_audience"] = audience
    
    def add_heading(
        self, 
        text: str, 
        level: str, 
        context: str, 
        vector: str, 
        word_target: str,  # v4: Required
        keywords: str = "", 
        ngrams: str = "", 
        comments: str = ""
    ):
        """Add a heading with comprehensive details including word target"""
        self.headings.append({
            "HEADINGS": text,
            "HX": level,
            "CONTEXT": context,
            "VECTOR": vector,
            "KEYWORDS": keywords,
            "N-GRAMS": ngrams,
            "WORD_TARGET": word_target,  # v4
            "COMMENTS": comments
        })
    
    def add_statistic(
        self, 
        stat_id: str,
        stat: str, 
        source: str, 
        use_in: str,  # v4: Required - which heading
        year: str = "",
        context: str = ""
    ):
        """v4: Add a statistic with required heading assignment"""
        self.statistics.append({
            "id": stat_id,
            "stat": stat,
            "source": source,
            "year": year,
            "use_in": use_in,
            "context": context
        })
    
    def add_exclusion(self, stat: str, source: str, used_in: str):
        """v4: Add a statistic to the exclusion registry"""
        self.research_data["exclusion_registry"].append({
            "stat": stat,
            "source": source,
            "used_in": used_in
        })
    
    def add_internal_differentiation(
        self, 
        url: str, 
        title: str,
        covers: List[str], 
        do_not_repeat: List[str],
        this_article_adds: List[str]
    ):
        """v4: Document internal article differentiation"""
        self.research_data["internal_differentiation"].append({
            "url": url,
            "title": title,
            "covers": covers,
            "do_not_repeat": do_not_repeat,
            "this_article_adds": this_article_adds
        })
    
    def add_internal_link(
        self,
        url: str,
        anchor_text: str,
        place_in: str,
        do_not_repeat: List[str]
    ):
        """v4: Add internal link with avoidance notes"""
        self.research_data["interlinking"].append({
            "url": url,
            "anchor_text": anchor_text,
            "place_in": place_in,
            "do_not_repeat": do_not_repeat
        })
    
    def add_entity(self, name: str, description: str, relationships: list):
        """Document an entity and its relationships"""
        self.research_data["entities"][name] = {
            "description": description,
            "relationships": relationships
        }
    
    def add_competitor(self, url: str, angle: str, gaps: list):
        """Add competitor analysis"""
        self.research_data["competitors"].append({
            "url": url,
            "angle": angle,
            "gaps": gaps
        })
    
    def add_content_gap(self, gap: str, opportunity: str):
        """Add content gap"""
        self.research_data["content_gaps"].append({
            "gap": gap,
            "opportunity": opportunity
        })
    
    def generate_csv(self, output_dir: Path = Path(".")) -> Path:
        """Generate detailed CSV brief in v4 format"""
        filename = output_dir / f"{self.keyword.replace(' ', '-')}_brief.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f, 
                fieldnames=[
                    "HEADINGS", "HX", "CONTEXT", "VECTOR", 
                    "KEYWORDS", "N-GRAMS", "WORD_TARGET", "COMMENTS"
                ],
                quoting=csv.QUOTE_ALL
            )
            
            # Header row
            writer.writeheader()
            
            # Content rows
            for h in self.headings:
                writer.writerow(h)
        
        print(f"✅ CSV brief created: {filename}")
        return filename
    
    def generate_json(self, output_dir: Path = Path(".")) -> Path:
        """Generate JSON brief with v4 format (consistent with CSV)"""
        filename = output_dir / f"{self.keyword.replace(' ', '-')}_brief.json"
        
        # Build heading structure matching CSV columns
        heading_structure = []
        for h in self.headings:
            heading_structure.append({
                "level": h["HX"],
                "text": h["HEADINGS"],
                "context": h["CONTEXT"],
                "vector": h["VECTOR"],
                "keywords": [k.strip() for k in h["KEYWORDS"].split("\n") if k.strip()] if h["KEYWORDS"] else [],
                "ngrams": [n.strip() for n in h["N-GRAMS"].split("|") if n.strip()] if h["N-GRAMS"] else [],
                "word_target": h["WORD_TARGET"],
                "comments": h["COMMENTS"]
            })
        
        output = {
            "meta": {
                "topic": self.topic,
                "target_keywords": [self.keyword],
                "word_count": "1500-2000",
                "target_audience": self.research_data.get("target_audience", ""),
                "content_type": "guide",
                "created": self.timestamp,
                "version": "v4"
            },
            "macro_context": self.research_data["macro_context"],
            "heading_structure": heading_structure,
            # v4: Enhanced statistics with assignments
            "statistics": self.statistics,
            # v4: Exclusion registry
            "exclusion_registry": self.research_data["exclusion_registry"],
            # v4: Internal differentiation
            "internal_differentiation": self.research_data["internal_differentiation"],
            # v4: Interlinking with avoidance
            "interlinking": self.research_data["interlinking"],
            # Existing fields
            "content_gaps": self.research_data["content_gaps"],
            "entity_boundaries": self.research_data["entities"],
            "competitors": self.research_data["competitors"],
            "man_digital_angle": {
                "focus": "Process-first RevOps implementation",
                "differentiators": [
                    "Implementation reality over feature lists",
                    "Credit cost transparency",
                    "Efficiency optimization strategies",
                    "Practical threshold recommendations"
                ]
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON brief created: {filename}")
        return filename
    
    def generate_research_doc(self, output_dir: Path = Path(".")) -> Path:
        """Generate research documentation with v4 sections"""
        filename = output_dir / f"{self.keyword.replace(' ', '-')}_research.md"
        
        lines = [
            f"# Research Documentation: {self.topic}",
            f"\n**Keyword:** {self.keyword}",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
            f"**Version:** v4",
            "",
            "---",
            "",
            "## STATISTICS EXCLUSION REGISTRY",
            "",
            "### Already Used in Cluster:",
            "| Statistic | Source | Used In |",
            "|-----------|--------|---------|"
        ]
        
        for excl in self.research_data["exclusion_registry"]:
            lines.append(f"| \"{excl['stat']}\" | {excl['source']} | {excl['used_in']} |")
        
        if not self.research_data["exclusion_registry"]:
            lines.append("| (none documented) | - | - |")
        
        lines.extend([
            "",
            "### FORBIDDEN STATISTICS (Site-Wide):",
            "- Gartner 75% RevOps stat",
            "- BCG 70% transformation fail",
            "- McKinsey 87% skills gap",
            "- Forrester 36% retention",
            "",
            "---",
            "",
            "## INTERNAL ARTICLE DIFFERENTIATION",
            ""
        ])
        
        for i, diff in enumerate(self.research_data["internal_differentiation"], 1):
            lines.extend([
                f"### Existing Article {i}: {diff['title']}",
                f"- **URL:** {diff['url']}",
                f"- **Covers:** {', '.join(diff['covers'])}",
                f"- **DO NOT REPEAT:** {', '.join(diff['do_not_repeat'])}",
                f"- **THIS ARTICLE ADDS:** {', '.join(diff['this_article_adds'])}",
                ""
            ])
        
        if not self.research_data["internal_differentiation"]:
            lines.append("*(No internal articles documented)*\n")
        
        lines.extend([
            "---",
            "",
            "## Entity Architecture",
            ""
        ])
        
        for name, data in self.research_data["entities"].items():
            lines.extend([
                f"### {name}",
                data["description"],
                "",
                "**Relationships:**"
            ])
            for rel in data["relationships"]:
                lines.append(f"- {rel}")
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "## Competitor Analysis",
            ""
        ])
        
        for i, comp in enumerate(self.research_data["competitors"], 1):
            lines.extend([
                f"### Competitor {i}",
                f"**URL:** {comp['url']}",
                f"**Angle:** {comp['angle']}",
                "**Content Gaps:**"
            ])
            for gap in comp["gaps"]:
                lines.append(f"- {gap}")
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "## Statistics Inventory",
            ""
        ])
        
        for stat in self.statistics:
            lines.extend([
                f"### {stat['id']}",
                f"- **Statistic:** \"{stat['stat']}\"",
                f"- **Source:** {stat['source']}",
                f"- **Year:** {stat.get('year', 'N/A')}",
                f"- **Use In:** {stat['use_in']}",
                f"- **Context:** {stat.get('context', '')}",
                ""
            ])
        
        lines.extend([
            "---",
            "",
            "## Content Gaps",
            ""
        ])
        
        for gap in self.research_data["content_gaps"]:
            lines.append(f"1. **{gap['gap']}**")
            lines.append(f"   - Opportunity: {gap['opportunity']}")
        
        lines.extend([
            "",
            "---",
            "",
            "## Interlinking Strategy",
            ""
        ])
        
        for i, link in enumerate(self.research_data["interlinking"], 1):
            lines.extend([
                f"### Link {i}",
                f"- **URL:** {link['url']}",
                f"- **Anchor Text:** \"{link['anchor_text']}\"",
                f"- **Place In:** {link['place_in']}",
                f"- **DO NOT REPEAT FROM LINKED ARTICLE:**"
            ])
            for item in link["do_not_repeat"]:
                lines.append(f"  - {item}")
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "## MAN Digital Angle",
            "",
            "- **Process Focus:** Design the process first, then configure HubSpot",
            "- **Implementation Reality:** Acknowledge 2-3 month optimization period",
            "- **Practical Examples:** Use real scoring scenarios",
            "- **Eastern European Skepticism:** Don't oversell",
            "- **RevOps Efficiency:** Show hours saved, not vague benefits"
        ])
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Research doc created: {filename}")
        return filename
    
    def validate_brief(self) -> bool:
        """Validate the brief meets v4 requirements"""
        errors = []
        warnings = []
        
        # Check heading count
        total = len(self.headings)
        if total < 8:
            errors.append(f"Too few headings ({total}). Target: 8-12")
        elif total > 15:
            warnings.append(f"Many headings ({total}). Target: 8-15")
        
        # Check H1
        h1_count = sum(1 for h in self.headings if h["HX"].lower() == "h1")
        if h1_count != 1:
            errors.append(f"Must have exactly 1 H1 (found {h1_count})")
        
        # Check H1 has keywords
        h1 = next((h for h in self.headings if h["HX"].lower() == "h1"), None)
        if h1 and not h1["KEYWORDS"]:
            errors.append("H1 must include keywords")
        
        # v4: Check word targets
        total_word_target = 0
        for i, h in enumerate(self.headings, 1):
            if not h.get("WORD_TARGET"):
                warnings.append(f"Heading {i}: Missing WORD_TARGET")
            else:
                try:
                    wt = h["WORD_TARGET"]
                    if '-' in wt:
                        low, high = wt.split('-')
                        total_word_target += (int(low) + int(high)) // 2
                    else:
                        total_word_target += int(wt)
                except ValueError:
                    warnings.append(f"Heading {i}: Invalid WORD_TARGET format")
        
        if total_word_target < 1400:
            warnings.append(f"Total word target ({total_word_target}) may be too low")
        elif total_word_target > 2200:
            warnings.append(f"Total word target ({total_word_target}) may be too high")
        
        # v4: Check statistics have use_in
        for stat in self.statistics:
            if not stat.get("use_in"):
                errors.append(f"Statistic '{stat.get('id', 'unknown')}' missing 'use_in' field")
        
        # Check context length
        for i, h in enumerate(self.headings, 1):
            context_words = len(h["CONTEXT"].split())
            if h["HX"].lower() == "h1" and context_words < 50:
                warnings.append(f"H1 context short ({context_words} words). Target: 100-150")
            elif h["HX"].lower() == "h2" and context_words < 40:
                warnings.append(f"H2 #{i} context short ({context_words} words). Target: 75-100")
        
        # Check for vectors
        missing_vectors = [i for i, h in enumerate(self.headings, 1) 
                          if not h["VECTOR"].strip()]
        if missing_vectors:
            warnings.append(f"Missing vectors for headings: {missing_vectors}")
        
        # Check entity documentation
        if not self.research_data["entities"]:
            warnings.append("No entities documented")
        
        # v4: Check internal differentiation
        if not self.research_data["internal_differentiation"]:
            warnings.append("No internal article differentiation documented")
        
        if errors:
            print("❌ Validation FAILED:")
            for error in errors:
                print(f"  🔴 {error}")
        
        if warnings:
            print("⚠️ Warnings:")
            for warning in warnings:
                print(f"  🟡 {warning}")
        
        if not errors:
            print("✅ Brief validation passed")
            return True
        
        return False


# Example usage showing v4 format
if __name__ == "__main__":
    # Create a sample v4 brief
    brief = DetailedBriefGeneratorV4(
        topic="HubSpot Buyer Intent Implementation",
        keyword="HubSpot buyer intent"
    )
    
    # Set context
    brief.set_macro_context(
        "How HubSpot's buyer intent system identifies and prioritizes high-intent "
        "accounts through visitor tracking, research signals, and automated workflows"
    )
    brief.set_target_audience("RevOps leaders and Marketing Operations managers")
    
    # v4: Add exclusions
    brief.add_exclusion(
        stat="75% of RevOps see 10-20% growth",
        source="Gartner",
        used_in="revops-maturity-guide"
    )
    
    # v4: Add internal differentiation
    brief.add_internal_differentiation(
        url="/blog/buyer-intent-basics",
        title="Buyer Intent Basics Guide",
        covers=["Intent definition", "Three intent types", "Basic setup"],
        do_not_repeat=["Basic intent definitions", "Component overview"],
        this_article_adds=["Advanced configuration", "Credit optimization", "ROI calculation"]
    )
    
    # v4: Add statistics with assignments
    brief.add_statistic(
        stat_id="STAT_01",
        stat="47% better conversion rates for intent-driven campaigns",
        source="Forrester",
        year="2024",
        use_in="H1 - intro paragraph",
        context="Justifies importance of intent tracking"
    )
    
    brief.add_statistic(
        stat_id="STAT_02",
        stat="2.3x more qualified opportunities identified",
        source="Aberdeen",
        year="2024",
        use_in="H2-2 (tracking section)",
        context="Supports behavioral tracking value"
    )
    
    # v4: Add internal link with avoidance
    brief.add_internal_link(
        url="/blog/abm-strategy-hubspot",
        anchor_text="account-based marketing strategy",
        place_in="H2 about target accounts",
        do_not_repeat=["Basic ABM definition", "ICP framework", "Account tiers"]
    )
    
    # Add H1 with word target
    brief.add_heading(
        text="HubSpot Buyer Intent: Turn Anonymous Visitors into Pipeline Opportunities",
        level="h1",
        context=(
            "Open by establishing the transformation from blind outreach to data-driven ABM targeting. "
            "Include STAT_01 (47% better conversion, Forrester) in the opening paragraph. "
            "Define HubSpot Buyer Intent as a three-component system (Visitor Intent, Research Intent, "
            "Intent Signals) that identifies high-intent accounts at the company level, not individual leads. "
            "Emphasize this is about account-based intelligence, not lead scoring. "
            "Set expectations that this guide covers complete configuration from market setup to workflow automation, "
            "specifically for B2B RevOps teams implementing ABM strategies. "
            "NOTE: Do not repeat basic intent definitions from /blog/buyer-intent-basics."
        ),
        vector=(
            "Core of the context vector: establishing the foundation for all subsections. Sets up the "
            "three-pillar structure that the rest of the article follows while differentiating from "
            "basic feature overviews."
        ),
        word_target="200-250",
        keywords="HubSpot buyer intent - 150\nbuyer intent data - 90\nintent signals - 200",
        ngrams="HubSpot buyer intent | anonymous visitor tracking | pipeline opportunities | ABM targeting | intent data configuration",
        comments="Use STAT_01. Include diagram of three components. Link to HubSpot pricing docs. Featured snippet: first sentence answers 'What is HubSpot buyer intent?'"
    )
    
    # Add H2 with word target
    brief.add_heading(
        text="What Are the Three Types of HubSpot Buyer Intent Data?",
        level="h2",
        context=(
            "Explain the three distinct components in detail. Start with Visitor Intent and how it uses "
            "reverse-IP tracking to identify companies (not individuals) visiting your website. Then discuss "
            "Research Intent and how it aggregates third-party data. Include STAT_02 (2.3x more opportunities, Aberdeen) "
            "here. Finally, detail Intent Signals that track company-level events. "
            "Clarify that these work independently but can be layered. Address the misconception "
            "that this tracks individuals - it's strictly company-level data."
        ),
        vector=(
            "KEY PARAGRAPH: Central anchor for the context vector, linking directly to the three subtopics "
            "of intent types. Establishes foundational understanding before diving into configuration details."
        ),
        word_target="250-300",
        keywords="",
        ngrams="visitor intent tracking | research intent data | intent signals | reverse-IP identification | third-party data | company-level tracking",
        comments="Use STAT_02. Use comparison table for the three types. Visual opportunity: diagram showing data sources."
    )
    
    # Add entity
    brief.add_entity(
        name="Visitor Intent",
        description="First-party tracking of company website visits via reverse-IP",
        relationships=[
            "Part of HubSpot's native tracking",
            "Requires tracking code installation",
            "Company-level, not individual tracking",
            "90-day maximum lookback period"
        ]
    )
    
    # Add competitor
    brief.add_competitor(
        url="https://blog.hubspot.com/marketing/buyer-intent-data-guide",
        angle="Feature-focused explanation",
        gaps=["No scoring examples", "Missing ROI calculation", "No credit cost info"]
    )
    
    # Add content gap
    brief.add_content_gap(
        gap="Credit cost optimization strategies",
        opportunity="Unique angle competitors don't cover"
    )
    
    # Validate and generate
    print("\n" + "="*50)
    print("GENERATING V4 BRIEF")
    print("="*50 + "\n")
    
    if brief.validate_brief():
        brief.generate_csv()
        brief.generate_json()
        brief.generate_research_doc()
