#!/usr/bin/env python3
"""
Content Analysis Script for Figma Graphics Generator

Analyzes content (markdown, text, or HTML) to identify opportunities
for visual graphics and recommends appropriate graphic types.

Usage:
    python analyze_content.py <content-file>
    python analyze_content.py <content-file> --output-format json
"""

import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter


class ContentAnalyzer:
    """Analyzes content to recommend graphic types and placements."""
    
    # Patterns for identifying different content types
    PATTERNS = {
        'statistics': [
            r'\b\d+%',  # Percentages
            r'\b\d+x\b',  # Multipliers
            r'\b\d+,\d+',  # Numbers with commas
            r'\bstatistic(s)?\b',
            r'\bdata\b',
            r'\bsurvey\b',
            r'\bresearch\b',
            r'\bmetric(s)?\b',
        ],
        'process': [
            r'\bstep\s+\d+',  # Step 1, Step 2
            r'\bfirst\b.*\bthen\b.*\bfinally\b',
            r'\bworkflow\b',
            r'\bprocess\b',
            r'\bprocedure\b',
            r'\bhow\s+to\b',
            r'\bguide\b',
        ],
        'comparison': [
            r'\bvs\.?\b',  # versus
            r'\bversus\b',
            r'\bcompare(d)?\b',
            r'\bcomparison\b',
            r'\balternative(s)?\b',
            r'\bbefore\b.*\bafter\b',
            r'\bpros\b.*\bcons\b',
            r'\badvantage(s)?\b.*\bdisadvantage(s)?\b',
        ],
        'timeline': [
            r'\b\d{4}\b',  # Years
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b',
            r'\btimeline\b',
            r'\broadmap\b',
            r'\bmilestone(s)?\b',
            r'\bevolution\b',
            r'\bhistory\b',
        ],
        'list': [
            r'^\s*[-*]\s+',  # Markdown list items
            r'^\s*\d+\.\s+',  # Numbered list items
            r'\btop\s+\d+\b',  # Top 10, Top 5, etc.
            r'\bkey\s+\w+\b',  # Key features, key points, etc.
        ],
        'concept': [
            r'\bframework\b',
            r'\bmodel\b',
            r'\btheory\b',
            r'\bconcept\b',
            r'\bapproach\b',
            r'\bmethodology\b',
            r'\bstrategy\b',
        ]
    }
    
    def __init__(self, content: str):
        """Initialize analyzer with content."""
        self.content = content
        self.lines = content.split('\n')
        self.sections = self._identify_sections()
    
    def _identify_sections(self) -> List[Dict]:
        """Identify content sections based on headers."""
        sections = []
        current_section = None
        
        for i, line in enumerate(self.lines):
            # Detect markdown headers
            if line.startswith('#'):
                if current_section:
                    sections.append(current_section)
                
                header_level = len(line.split()[0])
                header_text = line.strip('#').strip()
                current_section = {
                    'header': header_text,
                    'level': header_level,
                    'start_line': i,
                    'content': []
                }
            elif current_section:
                current_section['content'].append(line)
        
        if current_section:
            sections.append(current_section)
        
        return sections
    
    def _count_pattern_matches(self, text: str, patterns: List[str]) -> int:
        """Count how many patterns match in text."""
        count = 0
        text_lower = text.lower()
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.MULTILINE)
            count += len(matches)
        return count
    
    def analyze_content_type(self, text: str) -> Dict[str, int]:
        """Analyze text to determine content type scores."""
        scores = {}
        for content_type, patterns in self.PATTERNS.items():
            scores[content_type] = self._count_pattern_matches(text, patterns)
        return scores
    
    def recommend_graphics(self) -> List[Dict]:
        """Analyze content and recommend graphics."""
        recommendations = []
        
        for section in self.sections:
            section_text = '\n'.join(section['content'])
            if len(section_text) < 50:  # Skip very short sections
                continue
            
            scores = self.analyze_content_type(section_text)
            
            # Determine primary content type
            primary_type = max(scores, key=scores.get) if max(scores.values()) > 0 else None
            
            if not primary_type or scores[primary_type] < 2:
                continue  # Not enough signal
            
            # Map content type to graphic type
            graphic_mapping = {
                'statistics': {
                    'type': 'Statistical Infographic',
                    'description': 'Data visualization with charts, graphs, and key metrics',
                    'dimensions': '800px × 1800-2400px (vertical)',
                    'template': 'Statistical Infographic',
                    'footer': True
                },
                'process': {
                    'type': 'Process Flow Diagram',
                    'description': 'Step-by-step visual workflow',
                    'dimensions': '800px × 1600px (vertical) or 1920px × 1080px (horizontal)',
                    'template': 'Process Flow',
                    'footer': False  # Context-dependent
                },
                'comparison': {
                    'type': 'Comparison Table/Graphic',
                    'description': 'Side-by-side comparison visualization',
                    'dimensions': '1080px × 1080px (social) or 800px × 1200px (blog)',
                    'template': 'Comparison Table',
                    'footer': False  # Not for social, yes for blog
                },
                'timeline': {
                    'type': 'Timeline Graphic',
                    'description': 'Chronological visualization of events/milestones',
                    'dimensions': '1600px × 600px (horizontal) or 800px × 1800px (vertical)',
                    'template': 'Timeline',
                    'footer': False  # Context-dependent
                },
                'list': {
                    'type': 'Icon-Based List Infographic',
                    'description': 'Visual list with icons for each item',
                    'dimensions': '1080px × 1080px (social) or 800px × 1400px (blog)',
                    'template': 'List Infographic',
                    'footer': False  # Not for social
                },
                'concept': {
                    'type': 'Concept Diagram',
                    'description': 'Visual representation of framework or model',
                    'dimensions': '1200px × 800px (horizontal) or 800px × 1200px (vertical)',
                    'template': 'Concept Diagram',
                    'footer': False  # Context-dependent
                }
            }
            
            recommendation = {
                'section_header': section['header'],
                'section_line': section['start_line'],
                'content_type': primary_type,
                'confidence_score': scores[primary_type],
                'graphic_type': graphic_mapping[primary_type]['type'],
                'description': graphic_mapping[primary_type]['description'],
                'recommended_dimensions': graphic_mapping[primary_type]['dimensions'],
                'template': graphic_mapping[primary_type]['template'],
                'footer_recommended': graphic_mapping[primary_type]['footer'],
                'context_snippet': section_text[:200] + '...' if len(section_text) > 200 else section_text,
                'placement_before': self._get_context_snippet(section['start_line'] + len(section['content']) + 1),
                'placement_after': self._get_context_snippet(section['start_line'] - 1)
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _get_context_snippet(self, line_num: int, context_lines: int = 2) -> str:
        """Get context snippet around a line number."""
        start = max(0, line_num - context_lines)
        end = min(len(self.lines), line_num + context_lines)
        return ' '.join(self.lines[start:end])
    
    def generate_summary(self) -> Dict:
        """Generate analysis summary."""
        recommendations = self.recommend_graphics()
        
        # Count graphic types
        graphic_types = Counter([r['graphic_type'] for r in recommendations])
        
        # Calculate content statistics
        word_count = len(self.content.split())
        section_count = len(self.sections)
        
        return {
            'content_stats': {
                'word_count': word_count,
                'section_count': section_count,
                'recommendations_count': len(recommendations)
            },
            'graphic_types_summary': dict(graphic_types),
            'recommendations': recommendations
        }


def format_output_markdown(summary: Dict) -> str:
    """Format analysis output as markdown."""
    output = []
    
    output.append("# Content Analysis for Graphics Generation\n")
    output.append("## Summary\n")
    output.append(f"- **Word Count:** {summary['content_stats']['word_count']}")
    output.append(f"- **Sections:** {summary['content_stats']['section_count']}")
    output.append(f"- **Graphics Recommended:** {summary['content_stats']['recommendations_count']}\n")
    
    if summary['graphic_types_summary']:
        output.append("## Recommended Graphic Types\n")
        for graphic_type, count in summary['graphic_types_summary'].items():
            output.append(f"- **{graphic_type}:** {count} instance(s)")
        output.append("")
    
    output.append("## Detailed Recommendations\n")
    
    for i, rec in enumerate(summary['recommendations'], 1):
        output.append(f"### Recommendation {i}: {rec['section_header']}\n")
        output.append(f"**Graphic Type:** {rec['graphic_type']}")
        output.append(f"**Description:** {rec['description']}")
        output.append(f"**Recommended Dimensions:** {rec['recommended_dimensions']}")
        output.append(f"**Template to Use:** {rec['template']}")
        output.append(f"**Footer Recommended:** {'Yes' if rec['footer_recommended'] else 'Context-dependent'}")
        output.append(f"**Confidence Score:** {rec['confidence_score']} pattern matches\n")
        
        output.append("**Placement Context:**")
        output.append(f"- Insert after: \"{rec['placement_after'][:100]}...\"")
        output.append(f"- Insert before: \"{rec['placement_before'][:100]}...\"\n")
        
        output.append(f"**Content Preview:**")
        output.append(f"```")
        output.append(f"{rec['context_snippet']}")
        output.append(f"```\n")
        
        output.append("---\n")
    
    if not summary['recommendations']:
        output.append("No clear graphic opportunities identified in this content.")
        output.append("Consider manually reviewing sections for potential visualizations.\n")
    
    return '\n'.join(output)


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Usage: python analyze_content.py <content-file> [--output-format json]")
        sys.exit(1)
    
    content_file = Path(sys.argv[1])
    output_format = 'markdown'
    
    if len(sys.argv) > 2 and sys.argv[2] == '--output-format' and len(sys.argv) > 3:
        output_format = sys.argv[3]
    
    if not content_file.exists():
        print(f"Error: File '{content_file}' not found.")
        sys.exit(1)
    
    # Read content
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Analyze content
    analyzer = ContentAnalyzer(content)
    summary = analyzer.generate_summary()
    
    # Output results
    if output_format == 'json':
        print(json.dumps(summary, indent=2))
    else:
        print(format_output_markdown(summary))


if __name__ == '__main__':
    main()
