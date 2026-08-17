---
name: seo-content-brief-v4
description: Creates focused SEO content briefs with deep entity understanding and competition analysis. Emphasizes understanding relationships between entities BEFORE creating structure. Includes statistics deduplication across content clusters, word targets per section, statistic-to-heading assignment, and internal article differentiation. Outputs lightweight but well-researched briefs with 8-12 headings, clear focus areas, and copywriting guidance. Designed for MAN Digital's RevOps content (1500-2000 words typical). Uses MCP_DOCKER tools for research, produces CSV and JSON outputs with identical core structures.
---

# SEO Content Brief Creation (v4)

## Purpose

Creates **lightweight, well-researched** SEO content briefs that:
- Deeply understand entities and relationships FIRST
- Analyze real competition (not generic templates)
- **Deduplicate statistics across content clusters**
- **Assign statistics to specific headings**
- **Define word targets per section**
- **Differentiate from existing internal articles**
- Output focused structure (8-12 headings max)
- Provide clear guidance without overwhelming detail
- Target 1500-2000 word blog posts (unless specified otherwise)

**Key Difference from v3:** This version adds statistics deduplication, per-heading statistic assignment, word targets, and internal article differentiation.

## Required Inputs

### Must Have:
1. **Topic/Subject** - What are we writing about?
2. **Target Audience** - Who is this for? (e.g., RevOps leaders, Marketing managers)
3. **Primary Keyword(s)** - 1-3 target keywords

### Optional but Helpful:
- Competitor URLs to analyze
- Specific angle or differentiator
- Word count if not standard (1500-2000)
- **Content cluster URLs** (existing internal articles to avoid duplicating)

**⚠️ IF INPUTS MISSING:** 
Ask: "I need: 1) Topic, 2) Target audience, 3) Primary keyword(s). Optional: competitor URLs, internal cluster articles, or specific angle."

---

## Phase 0: Content Cluster Analysis (NEW IN V4)

> **Critical for statistics deduplication and content differentiation**

### Step 0.1: Identify Content Cluster

Before any research, identify related internal articles:

```python
# Example cluster identification
cluster_articles = [
    "https://man.digital/blog/hubspot-buyer-intent",
    "https://man.digital/blog/account-based-marketing-setup",
    "https://man.digital/blog/lead-scoring-hubspot"
]
```

### Step 0.2: Scrape Internal Articles

**Use available tools to extract content:**

```python
for url in cluster_articles:
    if firecrawl_available:
        content = firecrawl_scrape(url, formats=["markdown"])
    # Extract:
    # - All statistics used
    # - Key topics covered
    # - Unique angles taken
```

### Step 0.3: Build Statistics Exclusion Registry

**MANDATORY before selecting any statistics for the brief:**

```markdown
## STATISTICS EXCLUSION REGISTRY

### Already Used in Cluster:
| Statistic | Source | Used In |
|-----------|--------|---------|
| "75% of RevOps see 10-20% growth" | Gartner | buyer-intent-guide |
| "70% B2B journey before sales" | Forrester | abm-setup |
| "36% better retention" | Forrester | lead-scoring |

### FORBIDDEN STATISTICS (overused across site):
- Gartner 75% RevOps stat
- BCG 70% transformation fail
- McKinsey 87% skills gap
- Forrester 36% retention
```

### Step 0.4: Internal Article Differentiation

Document what existing articles cover and what this article must NOT repeat:

```markdown
## INTERNAL ARTICLE DIFFERENTIATION

### Existing Article 1: HubSpot Buyer Intent Guide
- **URL:** /blog/hubspot-buyer-intent
- **Covers:** Visitor intent, research intent basics, workflow setup
- **DO NOT REPEAT:** Basic intent definitions, 3-component overview
- **THIS ARTICLE ADDS:** Advanced configuration, credit optimization, ROI calculation

### Existing Article 2: ABM Setup in HubSpot
- **URL:** /blog/abm-setup-hubspot
- **Covers:** Target account lists, ICP definition, account scoring
- **DO NOT REPEAT:** Basic ABM concepts, account list creation
- **THIS ARTICLE ADDS:** Intent-driven prioritization for existing ABM
```

---

## Phase 1: Entity & Relationship Understanding (CRITICAL)

> **This is the MOST IMPORTANT phase. Poor understanding = poor brief.**

### Step 1.1: Initial Topic Research

**Use available tools to understand the landscape:**

```python
# Priority order for research tools:
# 1. MCP_DOCKER tools (firecrawl, exa, perplexity)
# 2. DataForSEO if available
# 3. Web search as fallback

if firecrawl_available:
    results = firecrawl_search(
        query=f"{keyword} guide 2025",
        limit=5
    )
elif exa_available:
    results = web_search_exa(
        query=f"{keyword} explained",
        numResults=5
    )
```

### Step 1.2: Entity Mapping (MANDATORY)

**Identify ALL entities involved in your topic:**

Ask yourself:
- **WHO/WHAT** are the main players? (tools, companies, people, concepts)
- **HOW** do they relate to each other?
- **WHERE** do boundaries exist between entities?
- **WHAT** gets commonly confused or conflated?

> See `references/entity-understanding.md` for detailed patterns and examples.

### Step 1.3: Create Entity Architecture

Document the architecture BEFORE creating any headings:

```markdown
ENTITY ARCHITECTURE for [TOPIC]:

Primary Entity: [Main subject]
├── Component A: [What it includes]
├── Component B: [What it includes]
└── Component C: [What it includes]

Related Entities:
- Entity X: [How it relates to primary]
- Entity Y: [How it connects]

Boundaries:
- [Primary Entity] INCLUDES: [list]
- [Primary Entity] DOES NOT INCLUDE: [list]
- Common conflations to avoid: [list]
```

---

## Phase 2: Competition & Market Analysis

### Step 2.1: Find ACTUAL Competitors

**Don't guess - find who's actually ranking:**

```python
if firecrawl_available:
    search_results = firecrawl_search(
        query=keyword,
        limit=10,
        sources=["web"]
    )
    competitor_urls = [r['url'] for r in search_results[:5]]
```

### Step 2.2: Analyze Competitor Content

**For each competitor, understand:**
- What angle are they taking?
- What entities do they cover?
- What do they miss or get wrong?
- What's their typical structure?

### Step 2.3: Identify Opportunities

Based on competitor analysis:
- **Universal topics** (everyone covers these - must include)
- **Gaps** (no one covers these well - opportunities)
- **Misconceptions** (everyone gets this wrong - we can correct)
- **MAN Digital angle** (process-first, not tool-first)

---

## Phase 3: Fresh Statistics Research (NEW IN V4)

### Step 3.1: Research Sources Priority

**Tier-1 Sources by Topic Area:**

| Topic Area | Priority Sources |
|------------|-----------------|
| CRM/Implementation | CRM.org, SuperOffice, Nucleus Research |
| European B2B | ECXO, IDC Europe reports |
| Tech Adoption | IDC Future Enterprise, Gartner |
| Consulting Benchmarks | McKinsey, BCG, Bain (check if already used!) |
| Industry Research | Forrester, HubSpot Research |

### Step 3.2: Search Patterns for Fresh Statistics

```python
# Search query patterns
search_queries = [
    f'"{topic}" statistics 2024 2025 site:crmorg',
    f'"{topic}" research report PDF 2025',
    f'"{topic}" benchmark data B2B',
    f'"{topic}" survey results 2025'
]
```

### Step 3.3: Statistics Selection Rules

**BEFORE including any statistic:**
1. Check against exclusion registry
2. Verify it's from 2023+ (preferably 2024-2025)
3. Confirm source is credible
4. **Assign to specific heading immediately**

---

## Phase 4: Brief Structure Creation (DETAILED WITH V4 ENHANCEMENTS)

### Step 4.1: Define Focus

**One clear macro context (NO deviation):**
```
MACRO CONTEXT: [Single, clear focus that every section contributes to]
Example: "How HubSpot's buyer intent system identifies and prioritizes high-intent accounts through visitor tracking, research signals, and automated workflows"
```

### Step 4.2: Create Heading Structure with Word Targets

**Target: 8-12 total headings**
- 1 H1 (includes primary keyword with search volume)
- 5-8 H2s (major sections with detailed guidance)
- 2-4 H3s (subsections with specific focus)

**For each heading, develop ALL columns including WORD_TARGET:**

#### Column Specifications (8-Column CSV Format v4):

| Column | Description | Required |
|--------|-------------|----------|
| HEADINGS | The heading text | Yes |
| HX | Level (h1, h2, h3) | Yes |
| CONTEXT | 75-150 word directive guidance | Yes |
| VECTOR | Thematic connection to article | Yes |
| KEYWORDS | Primary keywords (H1 only) | H1 only |
| N-GRAMS | Semantic phrases (pipe-separated) | H1, H2 |
| WORD_TARGET | Target word count for section | Yes (NEW) |
| COMMENTS | Tips, links, statistic assignments | Yes |

### Step 4.3: CONTEXT Column (Use Directive Language!)

> See `references/context-vector-patterns.md` for complete patterns.

Write using action verbs:
- **Start with** => "Start with a clear definition of..."
- **Explain** => "Explain how X transforms Y..."
- **Discuss** => "Discuss the three main pillars..."
- **Include** => "Include the statistic that [STAT_ID]..."

### Step 4.4: WORD_TARGET Column (NEW IN V4)

**Standard word targets by heading level:**

| Level | Word Target Range | Notes |
|-------|------------------|-------|
| H1 (intro) | 200-250 | Hook + overview + stat |
| H2 (framework/overview) | 150-200 | Conceptual sections |
| H2 (implementation) | 250-350 | Detailed how-to |
| H2 (examples/cases) | 200-300 | Case studies, examples |
| H3 (configuration) | 150-200 | Specific steps |
| H3 (subsection) | 100-150 | Supporting detail |
| Conclusion | 100-150 | Summary + CTA |

### Step 4.5: Statistics Assignment in COMMENTS Column (NEW IN V4)

**Every statistic must be assigned to a specific heading:**

```
COMMENTS: "Use STAT_01 (47% conversion, Forrester) in opening paragraph. Screenshot opportunity: Dashboard view. Link to pricing guide."
```

**Statistics Reference Format:**
```
STAT_01: "47% better conversion rates" - Forrester, use_in: H1
STAT_02: "70% B2B journey before sales" - Forrester, use_in: H2-1
STAT_03: "2.3x more likely to convert" - Aberdeen, use_in: H2-3
```

---

## Phase 5: Interlinking with Avoidance Notes (NEW IN V4)

### Step 5.1: Internal Link Strategy

**For each internal link, document:**

```markdown
## INTERLINKING STRATEGY

### Link 1: ABM Strategy Guide
- **URL:** /blog/abm-strategy-hubspot
- **Anchor Text:** "account-based marketing strategy"
- **Place In:** H2 about target account configuration
- **DO NOT REPEAT FROM LINKED ARTICLE:**
  - Basic ABM definition
  - ICP framework explanation
  - Account tier structure

### Link 2: Lead Scoring Setup
- **URL:** /blog/lead-scoring-hubspot
- **Anchor Text:** "behavioral scoring model"
- **Place In:** H3 about scoring configuration
- **DO NOT REPEAT FROM LINKED ARTICLE:**
  - Score property creation steps
  - Point value recommendations
  - Threshold definitions
```

---

## Phase 6: Output Files

### Primary Output: 8-Column CSV Brief (v4 Format)

`[topic]_brief.csv` with columns:
```csv
HEADINGS,HX,CONTEXT,VECTOR,KEYWORDS,N-GRAMS,WORD_TARGET,COMMENTS
```

**Critical Requirements:**
- CONTEXT: 75-150 words of detailed directive guidance
- VECTOR: Thematic flow and connections
- WORD_TARGET: Specific word count for section (NEW)
- COMMENTS: Tips, statistic assignments (with STAT_ID), links

### Secondary Outputs:

**`[topic]_brief.json`** - JSON version with IDENTICAL heading structure:
```json
{
  "meta": { ... },
  "macro_context": "...",
  "heading_structure": [
    {
      "level": "h1",
      "text": "...",
      "context": "...",
      "vector": "...",
      "keywords": [],
      "ngrams": [],
      "word_target": 200,
      "comments": "..."
    }
  ],
  "statistics": [
    {
      "id": "STAT_01",
      "stat": "47% better conversion",
      "source": "Forrester",
      "use_in": "H1 - intro paragraph"
    }
  ],
  "interlinking": [ ... ],
  "exclusion_registry": [ ... ],
  "internal_differentiation": [ ... ]
}
```

**`[topic]_research.md`** - Research documentation including:
- Entity architecture
- Competitor analysis
- Statistics inventory (with exclusion status)
- Content gaps
- Internal article differentiation

---

## Phase 7: Validation (NEW IN V4)

**Run validator script before finalizing brief:**

```bash
python scripts/validator.py [topic]_brief.csv [topic]_research.md
```

### Validation Checklist (Automated):

- [ ] All headings have CONTEXT (75-150 words)
- [ ] All headings have VECTOR
- [ ] All headings have WORD_TARGET
- [ ] Statistics are fresh (not in exclusion list)
- [ ] Each statistic assigned to specific heading (STAT_ID in COMMENTS)
- [ ] Internal links have avoidance notes
- [ ] JSON and CSV columns match
- [ ] Differentiation section defines unique angle
- [ ] 8-12 total headings for 1500-2000 words
- [ ] Exactly 1 H1 with keywords

---

## Quick Reference: v4 Improvements Summary

| Feature | v3 | v4 |
|---------|----|----|
| Statistics Deduplication | ❌ | ✅ Exclusion registry |
| Statistics Assignment | Generic list | Assigned to headings with STAT_ID |
| Word Targets | Overall only | Per-section targets |
| Internal Differentiation | ❌ | ✅ Explicit boundaries |
| Output Consistency | Different structures | Identical CSV/JSON columns |
| Interlinking | Basic | With avoidance notes |
| Validation | Manual | Automated script |

---

## Tool Fallback Strategy

1. **Primary**: MCP_DOCKER tools (Firecrawl, Exa.ai, Perplexity)
2. **Secondary**: DataForSEO if available
3. **Tertiary**: Web search tools
4. **Last Resort**: Knowledge-based recommendations

Always use actual research when possible. Never create briefs from templates alone.

---

## References

- `references/entity-understanding.md` - Entity analysis patterns
- `references/context-vector-patterns.md` - CONTEXT and VECTOR writing guide
- `references/ngrams-keywords-guide.md` - N-grams and keywords reference
- `references/copywriter-instructions.md` - Writer guidance
- `references/statistics-sources.md` - Tier-1 source list by topic (NEW)
