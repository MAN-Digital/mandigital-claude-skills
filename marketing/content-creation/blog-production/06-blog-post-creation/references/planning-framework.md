# Strategic Planning Framework for Blog Post Creation

## Overview

This document provides the detailed framework for Phase 0: Strategic Planning & Deep Thinking. Use this before ANY execution to ensure comprehensive planning and optimal outcomes.

## The 30-60 Second Ultra-Thinking Phase

Before touching ANY tools or writing ANY content, spend 30-60 seconds in focused strategic thinking:

### Question Framework

Ask yourself these questions IN ORDER:

1. **Uniqueness**: What makes this topic/angle unique in the current landscape?
2. **Gap Analysis**: What do existing articles miss that we can provide?
3. **Value Proposition**: What's the ONE thing readers will take away?
4. **Differentiation**: How will we stand out from top 10 Google results?
5. **Audience Needs**: What specific problem does this solve for GTM leaders?
6. **Evidence Required**: What statistics/data will make this credible?
7. **Tool Strategy**: Which MCP tools in what order will be most effective?
8. **Quality Measures**: What specific criteria define success for this piece?

## Phase 0 Components (Detailed)

### 1. Request Analysis

**Goal**: Fully understand what's being asked

**Process**:
- Extract primary topic and keywords
- Identify target audience (usually: GTM leaders, RevOps professionals)
- Determine content type (guide, analysis, how-to, thought leadership)
- Assess complexity level (introductory, intermediate, advanced)
- Define scope (breadth vs depth)

**Output Template**:
```
Topic: [Primary subject]
Primary Keyword: [Main SEO term]
Secondary Keywords: [Related terms]
Target Audience: [Specific personas]
Content Type: [Format/style]
Complexity: [Level]
Scope: [Boundaries]
```

**Example**:
```
Topic: HubSpot AI Agents for Marketing Teams
Primary Keyword: "HubSpot AI agents"
Secondary Keywords: "marketing automation AI", "HubSpot Breeze", "AI social media agent"
Target Audience: Marketing Directors, CMOs, RevOps Managers
Content Type: Implementation guide with strategic context
Complexity: Intermediate (assumes HubSpot knowledge)
Scope: Focus on marketing applications, not sales/service
```

### 2. Research Strategy Planning

**Goal**: Map exact research approach before execution

**Components**:

#### A. SEO Strategy & SERP Analysis (FIRST - BEFORE Content Research)

> **📋 For complete SEO workflow, see: `references/seo-analysis-workflow.md`**

**Goal**: Identify actual ranking competitors and SEO targets BEFORE content research

**Process**:

**STEP 1: Keyword Research (if no keyword provided)**

```
Tools:
- dataforseo_labs_google_keyword_ideas (generate options)
- dataforseo_labs_google_keyword_overview (analyze metrics)

Query Plan Phase 1a - Generate Ideas:
- Seed keywords: ["broad topic 1", "broad topic 2"]
- Location: United States (location_code: 2840)
- Language: English (language_code: "en")

Expected Output:
- 20-50 keyword variations
- Autocomplete suggestions
- Related searches

Query Plan Phase 1b - Analyze Metrics:
- Keywords: [top 5-10 options from ideas]
- Location: 2840
- Language: "en"

Expected Output:
- Search volume (monthly average)
- Competition level (low/medium/high)
- Keyword difficulty score
- Trend data (12-month history)
- SERP features

Decision Criteria:
- Balance: volume (>500) + low competition + difficulty (<50)
- Select keyword with best opportunity
- Confirm with user if needed
```

**Example**:
```
# Step 1a: Generate keyword ideas
dataforseo_labs_google_keyword_ideas({
  keywords: ["AI agents", "marketing automation"],
  location_code: 2840,
  language_code: "en"
})
→ Got 35 keyword variations

# Step 1b: Analyze top options
dataforseo_labs_google_keyword_overview({
  keywords: ["HubSpot AI agents", "marketing automation AI", "AI marketing tools"],
  location_code: 2840,
  language_code: "en"
})

→ Results:
  - "HubSpot AI agents": 8,100/mo, Medium comp, Difficulty 45, Rising trend
  - "marketing automation AI": 3,200/mo, High comp, Difficulty 62, Stable
  - "AI marketing tools": 12,500/mo, High comp, Difficulty 71, Rising

→ Selected: "HubSpot AI agents" (best balance of volume + difficulty + trend)
```

**STEP 2: Validate Search Intent (CRITICAL)**

```
Tool: dataforseo_labs_search_intent

Query Plan:
- Keyword: [confirmed keyword from Step 1]
- Location: 2840
- Language: "en"

Expected Output:
- Primary intent (informational/commercial/transactional/navigational)
- Intent probability scores
- SERP feature expectations
- Content format recommendations

Validation:
→ Informational intent > 60%? PROCEED
→ Transactional intent > 40%? STOP - Wrong content type
→ Commercial 40-60%? Consider (comparison/review content)
```

**Example**:
```
dataforseo_labs_search_intent({
  keywords: ["HubSpot AI agents"],
  location_code: 2840,
  language_code: "en"
})

→ Primary Intent: Informational (82%)
→ Commercial: 15%
→ Transactional: 3%
→ VERDICT: ✅ Perfect for blog post (high informational intent)
```

**STEP 3: SERP Analysis (MOST CRITICAL - Identify Ranking Competitors)**

```
Tool: dataforseo_serp_organic_live_advanced

Query Plan:
- Keyword: [confirmed keyword]
- Location: United States (2840)
- Language: English ("en")
- Device: Desktop
- Depth: 10 results (top 10 rankings)

Expected Output:
- URLs ranking in positions 1-10
- Page titles and meta descriptions
- Domain authority signals
- Rich snippet data (featured snippets, PAA, videos)
- SERP features present

Critical Rule:
→ These URLs from SERP are the ONLY competitors to analyze
→ DO NOT search randomly with Exa.ai for "articles about X"
→ SERP tells you WHO actually ranks = WHO to analyze
→ Prioritize positions 1-5 for detailed analysis
```

**Example**:
```
dataforseo_serp_organic_live_advanced({
  keyword: "HubSpot AI agents",
  location_code: 2840,
  language_code: "en",
  device: "desktop",
  depth: 10
})

→ Got top 10 URLs:
1. hubspot.com/blog/ai-agents → Position 1 (Official)
2. competitor1.com/hubspot-ai-guide → Position 2 (Comprehensive)
3. competitor2.com/ai-marketing-tools → Position 3 (Comparison)
4. blog.example.com/ai-agents → Position 4
5. revops-site.com/hubspot-automation → Position 5
[6-10 also captured]

→ SERP Features: Featured snippet (pos 0), People Also Ask (3 questions)
```

**STEP 4: Analyze Top Competitor Authority**

```
Tool: dataforseo_labs_google_domain_rank_overview

Query Plan:
- Target: Domains from positions 1-3 in SERP
- Location: 2840
- Language: "en"

Expected Output:
- Domain rank (authority score)
- Organic keywords count
- Organic traffic estimate
- Organic cost (traffic value)

Assessment:
→ Organic Keywords > 100K: Very high authority (difficult to outrank)
→ Organic Keywords 10K-100K: High authority (need strong content + backlinks)
→ Organic Keywords 1K-10K: Medium authority (outrank with superior content)
→ Organic Keywords < 1K: Low authority (good opportunity)

Strategy:
→ If high authority competitors: Focus on content gaps
→ If similar authority: Match quality + add unique value
→ Set realistic ranking timeline expectations
```

**Example**:
```
# Check top 3 competitor domains
dataforseo_labs_google_domain_rank_overview({
  target: "hubspot.com",
  location_code: 2840,
  language_code: "en"
})
→ Organic Keywords: 2.8M, Very high authority

dataforseo_labs_google_domain_rank_overview({
  target: "competitor1.com",
  location_code: 2840,
  language_code: "en"
})
→ Organic Keywords: 45K, High authority

→ ASSESSMENT: Strong competitors, need content gap strategy + exceptional quality
```

**STEP 5: Discover Related Keywords**

```
Tool: dataforseo_labs_google_related_keywords

Query Plan:
- Keyword: [target keyword]
- Location: 2840
- Language: "en"
- Depth: 2 (related keyword depth)

Expected Output:
- Related keywords list (20-30)
- Search volumes
- Relevance scores
- Keyword difficulty
- Long-tail variations

Use For:
→ H2 Topics: High-volume related keywords (300+ searches)
→ H3 Subtopics: Medium-volume variations (100-300 searches)
→ LSI Keywords: Low-volume semantic terms (naturally integrate)
→ FAQ Section: Question-format long-tail keywords
```

**Example**:
```
dataforseo_labs_google_related_keywords({
  keyword: "HubSpot AI agents",
  location_code: 2840,
  language_code: "en",
  depth: 2
})

→ Related Keywords (by volume):
  High (300+):
  - "HubSpot Breeze AI" (2,400/mo) → H2 topic
  - "AI social media agent" (890/mo) → H2 topic
  - "marketing automation AI" (3,200/mo) → H2 topic

  Medium (100-300):
  - "HubSpot AI features" (210/mo) → H3 subtopic
  - "AI content creation tools" (180/mo) → H3 subtopic

  Long-tail:
  - "how to set up AI agents in HubSpot" (40/mo) → FAQ question
  - "best HubSpot AI agent for email" (25/mo) → FAQ question
```

**STEP 6: Competitor On-Page SEO Analysis**

> **Note**: This step moved to Phase 1.2 SEO Data Gathering for more detailed analysis

```
Method: Use MCP_DOCKER Firecrawl or web scraping tools
Target: Top 3-5 URLs from SERP results (Step 3)

For Each Competitor URL:
□ Scrape page with Firecrawl
□ Extract H1, H2, H3 hierarchy
□ Count word count
□ Analyze meta title pattern
□ Analyze meta description pattern
□ Count internal/external links
□ Identify schema markup types (if visible)
□ Analyze content structure

Analysis Template: Use references/seo-competitor-analysis-template.md

Expected Output:
- Average word count: [X,XXX - Y,YYY]
- Common H2 count: [5-8]
- H3 depth: [2-3 per H2]
- Meta patterns identified
- Schema types used
- Universal topics (ALL competitors cover)
- SEO gaps (opportunities)
```

**Example**:
```
For each of top 3 SERP URLs:

firecrawl_scrape({
  url: "https://competitor1.com/hubspot-ai-guide",
  formats: ["markdown"]
})

→ Extract structure manually or with parsing
→ Competitor 1: 2,200 words, 7 H2s, 18 H3s, Article schema visible
→ Competitor 2: 1,800 words, 6 H2s, 14 H3s, Article + HowTo schema
→ Competitor 3: 2,500 words, 8 H2s, 22 H3s, Article schema

Pattern Analysis:
- Average word count: 2,167 words → Our target: 2,200 words (+10%)
- H2 range: 6-8 → Our target: 7 H2s
- H3 depth: 2.3 per H2 → Our target: 3 per H2 (deeper coverage)
- Universal topics: [Topic A], [Topic B], [Topic C] (must include)
- SEO gaps: None have FAQPage schema, shallow coverage on [Topic X]
```

**STEP 7: Set SEO Targets**

```
Based on competitor analysis, set targets:

Content Targets:
- Word count: [match or exceed competitor average by 10-15%]
- H2 count: [5-8 based on competitor range]
- H3 depth: [2-3 per H2 or deeper if gap]
- Universal topics: [list all must-include topics]
- Gap topics: [list differentiation opportunities]

Technical Targets:
- Meta title: [follow successful patterns, 50-60 chars]
- Meta description: [follow patterns, 150-160 chars]
- Schema: [Article + any gaps identified]
- Internal links: [3-5 contextual]
- External links: [3-5 authoritative]
- Keyword density: [1.5-2.5% natural]

Differentiation Strategy:
1. Fill gap topics competitors miss
2. Exceed average depth by X%
3. Implement missing schema types
4. Use stronger visual elements
```

**SEO Strategy Planning Output Template**:

```
=== SEO STRATEGY SUMMARY ===

Target Keyword: [confirmed keyword]
Search Volume: [X,XXX monthly searches]
Competition: [high/medium/low]
Trend: [rising/stable/declining]

SERP Competitors Identified:
1. Position 1: [URL] - [domain.com]
2. Position 2: [URL] - [domain.com]
3. Position 3: [URL] - [domain.com]
4. Position 4: [URL] - [domain.com]
5. Position 5: [URL] - [domain.com]

Competitor Baseline (from on-page analysis):
- Average word count: [X,XXX words]
- H2 range: [5-8]
- H3 depth: [2-3 per H2]
- Schema: Article (all), HowTo (1), FAQPage (0)

Universal Topics (MUST Include):
1. [Topic A] - All competitors cover
2. [Topic B] - All competitors cover
3. [Topic C] - All competitors cover

SEO Gaps (Differentiation Opportunities):
1. [Gap 1: Topic none cover]
2. [Gap 2: Shallow coverage area]
3. [Gap 3: Missing schema type]

Our SEO Targets:
- Word count: [2,200 words] (10% above average)
- H2 count: [7 H2s] (include gap topic)
- H3 depth: [3 per H2] (deeper coverage)
- Meta title: "[Keyword] for RevOps: [Benefit] | MAN Digital"
- Meta description: "Transform [challenge]... [CTA]" (158 chars)
- Schema: Article + FAQPage (competitor gap)
- Internal links: 4-5 (above average)
- Keyword density: 1.8% target

Content Angle Insights:
- Competitors focus on: [feature-first approach]
- We'll differentiate with: [process-first RevOps angle]
- Unique value: [specific gap we're filling]

=== READY FOR CONTENT RESEARCH ===
Now proceed to web_search_exa with context of gaps identified.
```

#### B. Search Query Planning (AFTER SEO Analysis)
List 4-6 specific web_search_exa queries:

```
PRIMARY QUERIES (Core topic):
1. web_search_exa("[primary keyword] 2025", numResults=5)
   Purpose: Current state, recent developments
   
2. web_search_exa("[primary keyword] guide", numResults=5)
   Purpose: Comprehensive coverage, identify gaps

SECONDARY QUERIES (Context & depth):
3. web_search_exa("[related concept] best practices", numResults=5)
   Purpose: Industry standards, proven approaches
   
4. web_search_exa("[product/platform] features update", numResults=5)
   Purpose: Latest capabilities, official sources

DATA QUERIES (Evidence):
5. web_search_exa("[industry] statistics 2025", numResults=5)
   Purpose: Fresh data, credible numbers
   
6. web_search_exa("[specific metric] research", numResults=5)
   Purpose: Specific data points for claims
```

#### B. Perplexity Research Planning

Identify complex topics requiring deep research:

```
Complex Topic 1: [Topic]
Query: "Comprehensive analysis of [topic] with authoritative sources and 2025 data"
Expected Output: Multi-source synthesis, citations, trends

Complex Topic 2: [Topic]
Query: "Statistical analysis of [metric] in [industry] 2025"
Expected Output: Data validation, source comparison
```

#### C. Fact-Checking Strategy

List specific claims that need verification:

```
Claim 1: [Specific statement to verify]
Verification: perplexity_reason query
Expected: Confirmation + sources OR correction + accurate data

Claim 2: [Product feature or capability]
Verification: perplexity_reason + web_fetch official docs
Expected: Accurate feature description, limitations
```

#### D. Competitor Analysis Plan

```
Target: Top 5-7 articles from web_search_exa results
Method: web_fetch for full content
Analysis Points:
- Publication date (prefer < 6 months old)
- Unique angles taken
- Statistics used (don't copy)
- Content gaps identified
- Citation quality
- Structural approach
```

### 3. Content Structure Planning

**Goal**: Blueprint entire article before writing

**Template**:

```
HOOK SECTION (1 paragraph, 2-3 sentences):
- Sentence 1: Transformation statement with primary keyword
- Sentences 2-3: Statistics + context
- Purpose: Immediate value, hook reader
- Statistics needed: [specific data point]
- Citation source: [from research query #X]

PROBLEM CONTEXT (3-4 paragraphs, 2-3 sentences each):
- Paragraph 1: [Current state problem]
  * Statistics needed: [specific data]
  * Source: [research query]
  
- Paragraph 2: [Impact/consequences]
  * Evidence needed: [what type]
  * Source: [which tool/search]
  
- Paragraph 3: [Why existing solutions fall short]
  * Data needed: [comparative stats]
  * Source: [research approach]
  
- Paragraph 4: [Transition to solution]
  * Evidence: [proof point]

SOLUTION OVERVIEW (3-4 paragraphs, 2-3 sentences each):
- Paragraph 1: [What is it]
  * Key features to highlight
  * Source: [product research]
  
- Paragraph 2: [How it differs]
  * Comparative advantage
  * Source: [competitor analysis]
  
[Continue for each major section...]

TAKEAWAY PLANNING:
- End of each section needs clear takeaway
- Final paragraph: actionable next steps
- No summary before content (no TL;DR)
```

**Example Planning**:
```
HOOK SECTION:
- Sentence 1: "HubSpot AI agents transform marketing teams from tactical executors to strategic advisors."
- Sentence 2-3: Statistics about time spent on manual tasks (need: % time, hours/week) + Source: web_search_exa("marketing team time statistics 2025")

PROBLEM CONTEXT:
Para 1: Marketing teams drowning in execution
- Need: % time on tactical vs strategic work
- Source: perplexity_research on marketing time allocation

Para 2: Cost of tactical focus
- Need: Impact on revenue, missed opportunities
- Source: web_search_exa("marketing productivity statistics")

Para 3: Why traditional automation fails
- Need: AI vs traditional automation comparison
- Source: web_search_exa("marketing automation AI difference")

[etc.]
```

### 4. Tool Selection & Sequence

**Goal**: Optimize research efficiency and quality

**Decision Framework**:

```
ALWAYS START:
1. web_search_exa (3-4+ queries)
   - Fast, comprehensive coverage
   - URL discovery
   - Recent content

THEN CHOOSE:
2. perplexity_research IF:
   - Topic is complex (requires synthesis)
   - Need authoritative sources
   - Comparing multiple perspectives
   - Deep market analysis required
   
   OR skip to web_fetch if topic is straightforward

3. web_fetch (top 3-5 URLs)
   - Get full article content
   - Analyze structure
   - Extract approach patterns
   - Identify unique angles

4. perplexity_reason IF:
   - Specific claims need verification
   - Statistics seem questionable
   - Technical accuracy critical
   - Product capabilities unclear
   
   OR skip if all info is clearly validated

5. Additional web_search_exa IF:
   - Gaps identified during analysis
   - Need more specific data
   - Statistics insufficient
```

**Sequence Template**:

```
PLANNED TOOL SEQUENCE:

Phase 1 - Initial Discovery:
□ web_search_exa("[keyword] 2025", numResults=5)
□ web_search_exa("[keyword] guide", numResults=5)
□ web_search_exa("[topic] best practices", numResults=5)

Phase 2 - Deep Research (if needed):
□ perplexity_research: [complex topic analysis]

Phase 3 - Content Analysis:
□ web_fetch: [URL from search 1]
□ web_fetch: [URL from search 2]
□ web_fetch: [URL from search 3]

Phase 4 - Data Gathering:
□ web_search_exa("[statistics] 2025", numResults=5)
□ web_search_exa("[specific data point]", numResults=5)

Phase 5 - Validation:
□ perplexity_reason: Verify [claim 1]
□ perplexity_reason: Verify [claim 2]

TOTAL TOOL CALLS PLANNED: [X]
ESTIMATED RESEARCH TIME: [Y minutes]
```

### 5. Quality Assurance Planning

**Goal**: Define success criteria before starting

**Quality Checkpoints Template**:

```
RESEARCH QUALITY:
□ Minimum 3 web_search_exa calls executed
□ Fresh sources only (published < 6 months)
□ Each claim has citation from MY research
□ Statistics verified with perplexity_reason
□ No copied content from examples/competitors

CONTENT QUALITY:
□ Primary keyword in hook sentence
□ Every paragraph 2-3 sentences (counted)
□ Line breaks between all paragraphs
□ Prose-focused, minimal bullets
□ 1,200-1,600 word count
□ No TL;DR before content

CITATION QUALITY:
□ Format: ([_Source Name_](URL))
□ All URLs from MY research
□ Links working and relevant
□ Authoritative sources prioritized
□ Publication dates recent

EDITING QUALITY:
□ All 10 frameworks applied in order
□ Active voice dominant
□ Specific numbers (no vague "many")
□ Sentence variety confirmed
□ Clear takeaways per section
□ Professional RevOps tone

TECHNICAL QUALITY:
□ Current platform names (X not Twitter)
□ Product features accurate (verified)
□ No outdated information
□ Statistics current for 2025
□ Claims defensible with sources
```

## Complete Planning Example

**Request**: "Create blog post about HubSpot's content agent for content marketers"

**PHASE 0 - STRATEGIC PLANNING OUTPUT**:

```
=== ULTRA-THINKING (30-60 seconds) ===

Uniqueness: Most articles focus on features; we'll focus on the strategic shift from content production to content strategy

Gap Analysis: Current content is feature-focused. Missing: how this changes the content marketer's role, strategic implications, team restructuring

Value Proposition: Content marketers learn how to evolve from producers to strategists using AI agents

Differentiation: 
- NOT a feature list
- Focus on role transformation
- Include change management aspect
- Real implementation challenges

Audience Needs: Content marketing leaders worried about AI replacing them need to see AI as role-enhancer, not replacer

Evidence Required:
- Time spent on content production (current)
- Strategic vs tactical time allocation
- Content quality impact data
- ROI of strategic content work
- AI adoption statistics in content marketing

Tool Strategy:
1. web_search_exa for current landscape (3-4 searches)
2. perplexity_research for content marketing time allocation data
3. web_fetch top 5 competitor articles
4. perplexity_reason to verify HubSpot content agent capabilities
5. web_search_exa for fresh statistics on content marketing

Quality Measures:
- Every claim backed by 2025 research
- Clear role transformation narrative
- Practical implementation steps
- Business impact quantified
- No feature list section

=== REQUEST ANALYSIS ===

Topic: HubSpot Content Agent for Content Marketers
Primary Keyword: "HubSpot content agent"
Secondary Keywords: "AI content marketing", "content automation", "HubSpot Breeze"
Target Audience: Content Marketing Directors, CMOs, Content Strategists
Content Type: Strategic guide with implementation framework
Complexity: Intermediate (assumes content marketing knowledge)
Scope: Focus on strategic transformation, not just features

=== SEO STRATEGY & SERP ANALYSIS (NEW - FIRST) ===

Step 1: Keyword Validation
□ dataforseo:ai_optimization_keyword_data_search_volume({
    keywords: ["HubSpot content agent", "AI content marketing", "content automation AI"],
    location_code: 2840,
    language_code: "en"
  })
  Result: "HubSpot content agent" - 3,200 monthly searches, medium competition, rising trend
  ✅ Confirmed as primary keyword

Step 2: SERP Analysis (Identify Ranking Competitors)
□ dataforseo:serp_organic_live_advanced({
    keyword: "HubSpot content agent",
    location_code: 2840,
    language_code: "en",
    device: "desktop",
    depth: 10
  })
  Results:
  1. hubspot.com/blog/content-agent → Position 1 (Official)
  2. martech.com/hubspot-content-ai → Position 2 (Industry news)
  3. contentmarketing.com/guide → Position 3 (Guide)
  4. competitor4.com/review → Position 4 (Review)
  5. competitor5.com/how-to → Position 5 (How-to)

  ✅ These are ACTUAL ranking competitors (not random articles)

Step 3: Keyword Trend Analysis
□ dataforseo:content_analysis_phrase_trends({
    keyword: "HubSpot content agent",
    location_code: 2840,
    language_code: "en"
  })
  Result: Rising trend, +45% mentions last 3 months
  ✅ Good keyword momentum

Step 4: Content Angle Analysis
□ dataforseo:content_analysis_summary({
    keyword: "HubSpot content agent",
    location_code: 2840,
    language_code: "en"
  })
  Result: Positive sentiment, focus on "automation", "efficiency", "strategy"
  Insight: Most content is feature-focused, opportunity for role-transformation angle

Step 5: Competitor On-Page SEO Analysis (Top 3 from SERP)
□ dataforseo:on_page_content_parsing for each:
  - hubspot.com/blog/content-agent
  - martech.com/hubspot-content-ai
  - contentmarketing.com/guide

Analysis Results:
Competitor 1 (hubspot.com):
- Word count: 1,800 words
- H2 count: 6 H2s
- H3 count: 12 H3s (2 per H2)
- Meta title: 58 chars
- Schema: Article
- Internal links: 5
- External links: 3

Competitor 2 (martech.com):
- Word count: 2,100 words
- H2 count: 7 H2s
- H3 count: 18 H3s (2.6 per H2)
- Meta title: 62 chars
- Schema: Article + NewsArticle
- Internal links: 4
- External links: 6

Competitor 3 (contentmarketing.com):
- Word count: 2,400 words
- H2 count: 8 H2s
- H3 count: 22 H3s (2.8 per H2)
- Meta title: 55 chars
- Schema: Article + HowTo
- Internal links: 6
- External links: 5

Pattern Analysis:
- Average word count: 2,100 words → Our target: 2,200 words (10% higher)
- H2 range: 6-8 → Our target: 7 H2s
- H3 depth: 2-2.8 per H2 → Our target: 3 per H2
- Schema: All have Article, 1 has HowTo → We'll add FAQPage (gap)
- Internal links: 4-6 average → Our target: 5-6
- External links: 3-6 average → Our target: 5-6

Universal Topics (ALL competitors cover):
1. "What is HubSpot content agent" (intro)
2. "Key features and capabilities"
3. "How to implement/get started"

Frequent Topics (2 of 3 cover):
1. "Comparison with traditional tools"
2. "Use cases and examples"

SEO Gaps Identified:
1. None deeply cover "change management" aspect
2. All are feature-focused, none cover "role transformation"
3. Missing: strategic planning implications
4. No one has FAQPage schema

Step 6: Set SEO Targets
Content Targets:
- Word count: 2,200 words (exceed average by 5%)
- H2 count: 7 H2s (include "Role Transformation" as gap topic)
- H3 depth: 3 per H2 (deeper than competitors)
- Universal topics: All 3 must-include topics
- Gap topics: Add "Strategic Planning Implications", "Change Management"

Technical Targets:
- Meta title: "HubSpot Content Agent for RevOps: Transform Marketing Strategy | MAN Digital" (58 chars)
- Meta description: "Transform content teams from tactical to strategic with HubSpot's content agent. Learn implementation, change management, and RevOps integration. [CTA]" (157 chars)
- Schema: Article + FAQPage (gap opportunity)
- Internal links: 5-6 contextual
- External links: 5-6 authoritative
- Keyword density: 1.8% target

Differentiation Strategy:
1. Fill gap: Role transformation angle (none cover)
2. Add change management section (gap)
3. Strategic planning implications (gap)
4. Implement FAQPage schema (gap)
5. Deeper H3 coverage (3 per H2 vs 2-2.8)

SEO Strategy Complete: ✅
Ready to proceed to content research with identified gaps.

=== RESEARCH STRATEGY (AFTER SEO) ===

Now that we know WHO ranks and WHAT gaps exist, plan content research:

Search Queries Planned:
1. web_search_exa("HubSpot content agent 2025", numResults=5)
   Purpose: Current capabilities, recent updates
   
2. web_search_exa("AI content marketing automation", numResults=5)
   Purpose: Broader context, competitive landscape
   
3. web_search_exa("content marketing productivity statistics", numResults=5)
   Purpose: Baseline data for impact claims
   
4. web_search_exa("HubSpot Breeze content features", numResults=5)
   Purpose: Official feature documentation

5. web_search_exa("content marketing strategy 2025", numResults=5)
   Purpose: Industry trends, strategic context

Perplexity Research Planned:
1. Topic: Content marketing time allocation
   Query: "How do content marketing teams allocate time between strategic and tactical work? Include 2025 statistics and authoritative sources."
   
2. Topic: AI impact on content roles
   Query: "Impact of AI tools on content marketing roles and responsibilities in 2025. Include research and data."

Web Fetch Targets:
- Top 3 URLs from search #1 (HubSpot content agent)
- Top 2 URLs from search #5 (strategy articles)

Verification Needed:
1. perplexity_reason: "Verify HubSpot content agent capabilities: can it research topics, optimize for SEO, and manage content calendar?"
2. perplexity_reason: "Verify claim: AI content tools reduce production time by 60-70%"

=== CONTENT STRUCTURE ===

HOOK (1 paragraph, 2-3 sentences):
- "HubSpot's content agent transforms content marketers from producers to strategists."
- Statistics: [% time on production vs strategy] + source
- Setup: The shift from tactical to strategic work

PROBLEM CONTEXT (3 paragraphs, 2-3 sentences each):
1. Content teams drowning in production
   - Need: % time on writing/editing vs strategy
   - Source: perplexity_research result
   
2. Strategic work gets deprioritized
   - Need: Impact on content performance/ROI
   - Source: web_search_exa results
   
3. Traditional tools don't solve this
   - Need: Comparison of tools vs AI agents
   - Source: Competitor analysis

SOLUTION (3 paragraphs):
1. What is HubSpot content agent
   - Features: Research, writing, optimization
   - Source: Official HubSpot docs + verification
   
2. How it differs from content tools
   - Agentic vs assistant
   - Source: Technology analysis
   
3. The strategic shift it enables
   - Time reallocation data
   - Source: Calculated from baseline stats

[Continue for Implementation, Impact, Next Steps sections...]

Paragraph Count Planned: ~25 paragraphs
Each: 2-3 sentences MAX
Total Word Count Target: 1,300-1,500

=== TOOL SEQUENCE (WITH SEO) ===

Phase 0 - SEO Strategy (6 tool calls):
□ dataforseo:ai_optimization_keyword_data_search_volume (keyword validation)
□ dataforseo:serp_organic_live_advanced (identify ranking competitors)
□ dataforseo:content_analysis_phrase_trends (keyword trends)
□ dataforseo:content_analysis_summary (content angle)
□ dataforseo:on_page_content_parsing (competitor 1 from SERP)
□ dataforseo:on_page_content_parsing (competitor 2 from SERP)
□ dataforseo:on_page_content_parsing (competitor 3 from SERP)
Subtotal: 7 tool calls

Phase 1 - Content Discovery (5 tool calls):
□ MCP_DOCKER:web_search_exa("HubSpot content agent 2025", numResults=5)
□ MCP_DOCKER:web_search_exa("AI content marketing automation", numResults=5)
□ MCP_DOCKER:web_search_exa("content marketing productivity statistics", numResults=5)
□ MCP_DOCKER:web_search_exa("HubSpot Breeze content features", numResults=5)
□ MCP_DOCKER:web_search_exa("content marketing strategy 2025", numResults=5)
Subtotal: 5 tool calls

Phase 2 - Deep Research (2 tool calls):
□ MCP_DOCKER:perplexity_research: Content marketing time allocation analysis
□ MCP_DOCKER:perplexity_research: AI impact on content roles
Subtotal: 2 tool calls

Phase 3 - Content Analysis (5 tool calls):
NOTE: May use SERP competitor URLs OR new URLs from web_search_exa
□ MCP_DOCKER:firecrawl_scrape OR web_fetch: [SERP competitor 1 - full content]
□ MCP_DOCKER:firecrawl_scrape OR web_fetch: [SERP competitor 2 - full content]
□ MCP_DOCKER:firecrawl_scrape OR web_fetch: [top URL from search]
□ web_fetch: [strategy article 1]
□ web_fetch: [strategy article 2]
Subtotal: 5 tool calls

Phase 4 - Verification (2 tool calls):
□ MCP_DOCKER:perplexity_reason: Verify content agent capabilities
□ MCP_DOCKER:perplexity_reason: Verify productivity claims
Subtotal: 2 tool calls

TOTAL: 21 planned tool calls (7 SEO + 14 content research)
ESTIMATED TIME:
- SEO Strategy: 4-5 minutes
- Content Research: 8-10 minutes
- Total: 12-15 minutes for complete research phase

=== QUALITY ASSURANCE PLAN ===

Research Checkpoints:
□ 5 web_search_exa calls minimum
□ All sources published in 2024-2025
□ HubSpot capabilities verified with perplexity_reason
□ Statistics cross-referenced across sources
□ No statistics from competitor articles copied

Content Checkpoints:
□ Hook sentence: keyword + transformation statement
□ Every paragraph: 2-3 sentences (will count during editing)
□ Line breaks: between ALL paragraphs
□ No bullets except for implementation steps
□ Word count: 1,200-1,600
□ No TL;DR or summary section

Citation Checkpoints:
□ Format: ([_Source Name_](URL))
□ Minimum 8-10 citations
□ All URLs from MY research
□ Publication dates in 2024-2025
□ Mix of sources (official, research, news)

Editing Checkpoints:
□ Framework 1: Redundancy
□ Framework 2: Active voice
□ Framework 3: Tenses
□ Framework 4: Parallelism
□ Framework 5: Sentence variety
□ Framework 6: Specificity
□ Framework 7: Arguments
□ Framework 8: Structure
□ Framework 9: Takeaways
□ Framework 10: Paragraph structure

Technical Checkpoints:
□ Platform names: X (not Twitter)
□ Product name: HubSpot content agent (correct capitalization)
□ Feature accuracy: verified with official sources
□ No outdated product info
□ Current for 2025 context

=== PLANNING COMPLETE ===

Total Planning Time: ~5 minutes (includes SEO strategy planning)
Estimated Research Time:
- SEO Strategy Phase: ~5 minutes (7 tool calls)
- Content Research Phase: ~10 minutes (14 tool calls)
- Total Research: ~15 minutes
Estimated Drafting Time: ~15 minutes
Estimated SEO Validation (Post-Draft): ~5 minutes
Estimated Editing Time: ~20 minutes
Estimated SEO Verification (Post-Edit): ~3 minutes
Total Estimated Time: ~63 minutes

Breakdown:
- Phase 0 (Planning): 5 min
- SEO Strategy (Phase 0): 5 min
- Content Research (Phase 2): 10 min
- Drafting (Phase 3): 15 min
- Post-Draft SEO Validation (Phase 3.5): 5 min
- Editing (Phase 4): 20 min
- Post-Edit SEO Verification (Phase 4.5): 3 min

Ready to proceed: YES
Plan comprehensiveness: VERY HIGH (includes SEO strategy)
Success probability: VERY HIGH (detailed plan, clear structure, validated approach, SEO targets set)
SEO Advantage: HIGH (gaps identified, targets set, competitors analyzed)

NOW BEGINNING EXECUTION WITH SEO-FIRST APPROACH...
```

## When to Revisit Planning

Return to planning phase if:
- Research reveals major gaps in original plan
- Topic is more complex than initially assessed
- Additional tool calls needed beyond original plan
- Content structure needs significant reorganization
- Quality checkpoints not being met

## Planning Phase Success Metrics

Planning phase is complete when you can answer YES to all:

1. ✅ I know EXACTLY what makes this piece unique
2. ✅ **I've completed SEO strategy (keyword, SERP, competitors, targets)**
3. ✅ **I know WHO ranks (actual SERP competitors identified)**
4. ✅ **I know WHAT gaps exist (competitor analysis complete)**
5. ✅ **I've set SEO targets (word count, H2/H3, technical elements)**
6. ✅ I have a complete list of tool calls to make (including SEO tools)
7. ✅ I know the full structure (all sections, paragraphs, must-include topics)
8. ✅ I've identified specific statistics needed
9. ✅ I have a clear quality validation approach
10. ✅ I can estimate time to completion (including SEO checkpoints)
11. ✅ I know success criteria for this piece
12. ✅ I've thought through potential challenges

**SEO-Specific Success Metrics (Must be YES):**

13. ✅ **Target keyword validated** (or researched if not provided)
14. ✅ **SERP competitors identified** (top 5-10 URLs from dataforseo:serp_organic_live_advanced)
15. ✅ **Competitor on-page SEO analyzed** (top 3-5 parsed with dataforseo:on_page_content_parsing)
16. ✅ **Universal topics documented** (topics ALL competitors cover)
17. ✅ **SEO gaps identified** (opportunities competitors miss)
18. ✅ **SEO targets set** (word count, H2/H3 structure, meta, schema, links, keyword density)
19. ✅ **Differentiation strategy clear** (how we'll exceed competitor baseline)

If ANY answer is NO, continue planning.
