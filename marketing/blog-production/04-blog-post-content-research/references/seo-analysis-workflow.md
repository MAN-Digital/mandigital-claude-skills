# SEO Analysis Workflow with DataForSEO MCP

## Overview

This workflow integrates DataForSEO MCP tools into the blog post creation process for comprehensive SEO analysis. SEO analysis occurs at FOUR critical checkpoints throughout the content creation lifecycle, with a dedicated Phase 1.2 for SEO data gathering.

---

## Available DataForSEO MCP Tools

### 1. Keyword Overview (Volume & Metrics)
**Tool:** `dataforseo_labs_google_keyword_overview`

**Purpose:** Get comprehensive keyword metrics including search volume, competition, CPC, and difficulty

**Use When:**
- No keyword provided by user (need to discover keywords)
- Validating keyword potential before writing
- Comparing multiple keyword options
- Understanding keyword difficulty and opportunity

**Parameters:**
- `keywords` (array): List of keywords to analyze (up to 1000)
- `location_code` (number): Location code (e.g., 2840 for USA)
- `language_code` (string): Language code (e.g., "en")

**Returns:**
- Search volume (monthly average)
- Competition level (low/medium/high)
- CPC (cost-per-click) data
- Keyword difficulty score
- Trend data (12-month history)
- SERP features (snippets, videos, etc.)

**Example Usage:**
```javascript
dataforseo_labs_google_keyword_overview({
  keywords: ["HubSpot AI agents", "marketing automation AI", "AI social media tools"],
  location_code: 2840,
  language_code: "en"
})
```

**Analysis Output:**
- **High-value keywords**: Volume > 500, Competition: Low-Medium, Difficulty < 50
- **Long-tail opportunities**: Volume 100-500, Low competition
- **Avoid**: High difficulty (> 70) unless domain authority is strong

---

### 2. Search Intent Analysis
**Tool:** `dataforseo_labs_search_intent`

**Purpose:** Determine user intent behind keywords (informational, commercial, transactional, navigational)

**Use When:**
- After selecting target keyword
- Planning content angle and structure
- Understanding what type of content Google expects
- Validating keyword matches blog post format

**Parameters:**
- `keywords` (array): Keywords to analyze intent
- `location_code` (number): Location code
- `language_code` (string): Language code

**Returns:**
- Primary intent (informational/commercial/transactional/navigational)
- Intent probability scores
- SERP feature expectations
- Content format recommendations

**Example Usage:**
```javascript
dataforseo_labs_search_intent({
  keywords: ["HubSpot AI agents for marketing"],
  location_code: 2840,
  language_code: "en"
})
```

**Intent Types:**
- **Informational** (80-100%): Perfect for blog posts - guides, how-tos, explainers
- **Commercial** (60-80%): Comparison content - "best X for Y", reviews
- **Transactional** (< 40%): Avoid - users want to buy, not read
- **Navigational** (< 20%): Avoid - users seeking specific brands

**CRITICAL:** Only target keywords with primary informational intent (> 60%) for blog posts.

---

### 3. SERP Organic Results (Competitor Rankings)
**Tool:** `dataforseo_serp_organic_live_advanced`

**Purpose:** Get real-time organic Google search results showing who actually ranks for target keywords

**Use When:**
- After confirming target keyword
- BEFORE researching content (to identify actual ranking competitors)
- Understanding SERP landscape and features

**Parameters:**
- `keyword` (string): Target keyword
- `location_code` (number): Location code (e.g., 2840 for USA)
- `language_code` (string): Language code (e.g., "en")
- `device` (string): "desktop" or "mobile"
- `depth` (number): Number of results (default: 10, max: 100)

**Returns:**
- Ranking URLs (positions 1-10+)
- Page titles
- Meta descriptions
- Domain authority signals
- Rich snippet data (featured snippets, PAA, videos)
- SERP features present

**Example Usage:**
```javascript
dataforseo_serp_organic_live_advanced({
  keyword: "HubSpot AI agents for marketing",
  location_code: 2840,
  language_code: "en",
  device: "desktop",
  depth: 10
})
```

**CRITICAL RULES:**
- The URLs from this tool are the ONLY competitors you should analyze
- Don't search randomly with Exa.ai for "articles about X" - that gives irrelevant content
- SERP tells you WHO actually ranks = WHO to analyze
- Prioritize positions 1-5 for detailed analysis

---

### 4. Competitor Ranked Keywords
**Tool:** `dataforseo_labs_google_ranked_keywords`

**Purpose:** Discover what keywords a competitor domain ranks for

**Use When:**
- After SERP analysis identifies top competitors
- Understanding competitor's keyword strategy
- Finding keyword gaps and opportunities
- Analyzing competitor authority in topic space

**Parameters:**
- `target` (string): Competitor domain or URL from SERP
- `location_code` (number): Location code
- `language_code` (string): Language code
- `filters` (array): Filter by position, search volume, etc.

**Returns:**
- List of keywords competitor ranks for
- Ranking positions
- Search volumes
- Traffic estimates
- SERP feature wins

**Example Usage:**
```javascript
dataforseo_labs_google_ranked_keywords({
  target: "hubspot.com",
  location_code: 2840,
  language_code: "en",
  filters: [
    ["ranked_serp_element.serp_item.rank_group", "<=", 10],
    ["keyword_data.keyword_info.search_volume", ">=", 100]
  ]
})
```

**Analysis Focus:**
- Keywords they rank #1-3 for (their strengths)
- Keywords they rank #4-10 for (opportunities to outrank)
- Topic clusters (what themes they dominate)
- Gaps in their coverage (your opportunities)

---

### 5. Related Keywords Discovery
**Tool:** `dataforseo_labs_google_related_keywords`

**Purpose:** Find semantically related keywords and long-tail variations

**Use When:**
- After confirming target keyword
- Planning H2/H3 content sections
- Discovering LSI keywords for natural optimization
- Finding subtopics to cover comprehensively

**Parameters:**
- `keyword` (string): Seed keyword
- `location_code` (number): Location code
- `language_code` (string): Language code
- `depth` (number): Depth of related keyword discovery

**Returns:**
- Related keywords list
- Search volumes
- Relevance scores
- Keyword difficulty
- Long-tail variations

**Example Usage:**
```javascript
dataforseo_labs_google_related_keywords({
  keyword: "HubSpot AI agents",
  location_code: 2840,
  language_code: "en",
  depth: 2
})
```

**Use For:**
- **H2 Topics**: High-volume related keywords (300+ searches)
- **H3 Subtopics**: Medium-volume variations (100-300 searches)
- **LSI Keywords**: Low-volume semantically related terms (naturally integrate)
- **FAQ Section**: Question-format long-tail keywords

---

### 6. Keyword Ideas Generation
**Tool:** `dataforseo_labs_google_keyword_ideas`

**Purpose:** Expand keyword research with Google's autocomplete suggestions and related searches

**Use When:**
- Brainstorming keyword options (no keyword provided)
- Discovering trending variations
- Finding "People Also Ask" type questions
- Uncovering long-tail opportunities

**Parameters:**
- `keywords` (array): Seed keywords for expansion
- `location_code` (number): Location code
- `language_code` (string): Language code

**Returns:**
- Expanded keyword ideas
- Search volumes
- Competition levels
- Trend data
- Autocomplete suggestions

**Example Usage:**
```javascript
dataforseo_labs_google_keyword_ideas({
  keywords: ["AI agents", "marketing automation"],
  location_code: 2840,
  language_code: "en"
})
```

**Best Use Cases:**
- Initial keyword discovery (Phase 0)
- Finding content angles (variations on main keyword)
- FAQ section content (question-based keywords)
- Identifying trending topics

---

### 7. Domain Rank Overview (Authority Analysis)
**Tool:** `dataforseo_labs_google_domain_rank_overview`

**Purpose:** Analyze domain authority metrics and organic visibility

**Use When:**
- Evaluating competitor strength from SERP
- Understanding ranking difficulty
- Assessing if you can realistically outrank competitors
- Prioritizing which competitors to analyze deeply

**Parameters:**
- `target` (string): Competitor domain from SERP
- `location_code` (number): Location code
- `language_code` (string): Language code

**Returns:**
- Domain rank (authority score)
- Organic keywords count
- Organic traffic estimate
- Organic cost (traffic value)
- ETV (estimated traffic value)

**Example Usage:**
```javascript
dataforseo_labs_google_domain_rank_overview({
  target: "hubspot.com",
  location_code: 2840,
  language_code: "en"
})
```

**Interpretation:**
- **Organic Keywords > 100K**: Very high authority (difficult to outrank)
- **Organic Keywords 10K-100K**: High authority (need strong content + backlinks)
- **Organic Keywords 1K-10K**: Medium authority (outrank with superior content)
- **Organic Keywords < 1K**: Low authority (good opportunity)

**Strategy:**
- Target competitors with similar or lower authority
- Focus on content gaps even if competitor has high authority
- Use insights to set realistic ranking timeline expectations

---

## SEO Analysis Workflow: Four Critical Checkpoints

### CHECKPOINT 1: Pre-Research SEO Planning (Phase 0 - Strategic Planning)

**WHEN:** During strategic planning, BEFORE any content research

**OBJECTIVE:** Validate keyword strategy, determine search intent, identify actual ranking competitors

**WORKFLOW:**

1. **If NO keyword provided:**
   ```
   Step 1a: Generate Keyword Ideas
   → Use dataforseo_labs_google_keyword_ideas
   → Input: Broad topic/seed keywords
   → Get: 20-50 keyword variations

   Step 1b: Analyze Keyword Metrics
   → Use dataforseo_labs_google_keyword_overview
   → Input: Top 5-10 keywords from ideas
   → Compare: Volume, competition, difficulty, trends
   → Select: Best keyword (high volume + low competition + informational intent)

   Step 1c: Confirm Keyword with User
   → "I found 3 keyword options:
      1. [Keyword A]: 2,400 searches/mo, Medium competition, Difficulty 45
      2. [Keyword B]: 1,800 searches/mo, Low competition, Difficulty 30
      3. [Keyword C]: 3,100 searches/mo, High competition, Difficulty 65

      Recommend targeting [Keyword B] - best opportunity. Proceed?"
   ```

2. **If keyword provided OR confirmed:**
   ```
   Step 2a: Validate Search Intent (CRITICAL)
   → Use dataforseo_labs_search_intent
   → Input: Confirmed keyword
   → Verify: Informational intent > 60%
   → If transactional/navigational: STOP - Wrong content type

   Step 2b: Get Keyword Metrics
   → Use dataforseo_labs_google_keyword_overview (if not done in Step 1)
   → Confirm: Adequate search volume + manageable difficulty

   Step 2c: SERP Analysis (MOST CRITICAL)
   → Use dataforseo_serp_organic_live_advanced
   → Get: Top 10 ranking URLs for target keyword
   → THESE are your actual competitors (not random articles)
   → Note: SERP features (featured snippets, PAA, videos)

   Step 2d: Analyze Top Competitor Authority
   → Use dataforseo_labs_google_domain_rank_overview
   → Input: Domains from positions 1-3 in SERP
   → Assess: Can we realistically compete with these domains?
   → Strategy: If high authority, focus on content gaps

   Step 2e: Discover Related Keywords
   → Use dataforseo_labs_google_related_keywords
   → Input: Target keyword
   → Get: 20-30 related keywords for H2/H3 planning
   → Identify: Subtopics to cover comprehensively
   ```

**OUTPUT:**
- ✅ Confirmed target keyword with metrics
- ✅ Search intent validation (informational)
- ✅ List of 5-10 ranking competitor URLs (from SERP)
- ✅ Competitor authority assessment
- ✅ Related keywords for content structure
- ✅ SERP features to target (snippets, PAA)

**CRITICAL RULE:** The URLs from `dataforseo_serp_organic_live_advanced` are the ONLY competitors you should analyze. Don't search randomly with Exa.ai for "articles about X" - that gives you irrelevant content. SERP tells you WHO actually ranks.

---

### CHECKPOINT 2: SEO Data Gathering (Phase 1.2 - NEW PHASE)

**WHEN:** After Phase 0 SEO planning, AFTER initial research strategy, BEFORE deep content research

**OBJECTIVE:** Gather comprehensive SEO data to inform content structure and identify gaps

**WORKFLOW:**

```
Step 1: Deep Competitor Keyword Analysis
→ For each top 3-5 competitors from SERP:
  → Use dataforseo_labs_google_ranked_keywords
  → Discover: What else do they rank for in this topic space?
  → Identify: Their keyword strengths and weaknesses
  → Find: Topic clusters they dominate

Step 2: Expand Keyword Opportunities
→ Use dataforseo_labs_google_keyword_ideas
→ Input: Target keyword + top related keywords
→ Find: Long-tail variations and question-based keywords
→ Map: Keywords to potential H2/H3 sections

Step 3: Compile SEO Intelligence Report
→ Document:
  - Target keyword metrics (volume, difficulty, intent)
  - SERP competitor list (positions 1-10)
  - Competitor authority levels (high/medium/low)
  - Related keywords by search volume (high/medium/low)
  - Competitor keyword gaps (topics they miss)
  - SERP features to target

→ Set Content Targets:
  - Word count target (based on CHECKPOINT 3 analysis)
  - H2 sections to include (universal topics + gap topics)
  - H3 depth per section
  - Schema markup to implement
  - Internal linking targets
```

**OUTPUT:**
- ✅ Comprehensive SEO Intelligence Report
- ✅ Competitor keyword strategy breakdown
- ✅ Content structure informed by keyword data
- ✅ Gap opportunities identified
- ✅ Clear SEO targets for drafting phase

**INTEGRATION:**
- Phase 0: SEO strategy planning
- Phase 1: Research strategy planning
- **Phase 1.2: SEO Data Gathering** ← NEW
- Phase 2: Deep content research (Exa.ai, Perplexity, Firecrawl)

---

### CHECKPOINT 3: Competitor On-Page SEO Analysis (Phase 2 - Deep Research)

**WHEN:** After SEO data gathering, BEFORE drafting brief/content

**OBJECTIVE:** Understand competitor on-page SEO structure and identify content gaps

**WORKFLOW:**

```
Step 1: Select Top 3-5 Competitors from SERP
→ Use URLs from positions 1-5 in SERP results
→ Prioritize: High rankings + relevant content + recent publish dates
→ Consider authority (from domain_rank_overview analysis)

Step 2: Parse Each Competitor Page
→ Use MCP_DOCKER Firecrawl or web scraping tools
→ Extract (Manual analysis or automated parsing):
  - H1 (should be 1 only)
  - H2 hierarchy (how many? what topics?)
  - H3 usage (depth of coverage)
  - Word count
  - Meta title pattern
  - Meta description pattern
  - Internal links (how many? to where?)
  - External links (how many? to where?)
  - Schema markup (what types?)
  - Images/visuals count
  - Content structure (intro, body, conclusion patterns)

Step 3: Analyze Patterns Across Competitors
→ Document common patterns in seo-competitor-analysis-template.md:
  - Average word count: X-Y words
  - Common H2 topics: [Topic A], [Topic B], [Topic C]
  - Heading structure: H1 → 5-7 H2s → 2-3 H3s per H2
  - Meta title pattern: "[Keyword] - [Benefit] | [Brand]"
  - Schema types: Article, HowTo, FAQPage, etc.
  - Internal linking density: 3-5 contextual links
  - Visual elements: 2-4 images/diagrams

Step 4: Cross-Reference with Keyword Data
→ Compare competitor H2s with related keywords from Phase 1.2
→ Identify: Topics all competitors cover (must-include)
→ Identify: Topics NONE cover (your differentiation)
→ Identify: Keywords competitors rank for but don't optimize for (gaps)

Step 5: Identify SEO Gaps (Opportunities)
→ What are competitors missing?
  - Topics not covered?
  - Shallow H3 coverage?
  - Missing schema types?
  - Weak internal linking?
  - Outdated content (2+ years old)?
  - Missing visual elements?
  - No FAQ section (but PAA appears in SERP)?
```

**OUTPUT:**
- ✅ Competitor on-page SEO report (use seo-competitor-analysis-template.md)
- ✅ Universal H2 topics (must include)
- ✅ Gap topics (your differentiation)
- ✅ Average content depth benchmarks
- ✅ SEO optimization targets
- ✅ Schema markup requirements

**TOOLS USED:**
- `dataforseo_labs_google_ranked_keywords` - Cross-reference competitor keywords
- `dataforseo_labs_google_related_keywords` - Compare with related keywords
- MCP_DOCKER Firecrawl/web scraping - Parse competitor page structure
- Manual analysis - Pattern identification

**INTEGRATION WITH EXISTING WORKFLOW:**
- Do this AFTER Phase 1.2 SEO Data Gathering
- Do this BEFORE web_search_exa (now you know what gaps to fill)
- Do this BEFORE creating brief (if no brief provided)

---

### CHECKPOINT 4: Post-Draft On-Page SEO Validation (Phase 3.5)

**WHEN:** After drafting, BEFORE comprehensive editing

**OBJECTIVE:** Validate our article has strong on-page SEO BEFORE editing changes it

**WORKFLOW:**

```
Step 1: Self-Analysis (Manual Review)
→ Use scripts/seo-validation-helper.py for automated checks
→ Command: python scripts/seo-validation-helper.py draft.md "target keyword"

→ Validate:
  ☑ H1: Single, includes target keyword
  ☑ H2s: 5-8 sections, keyword variations
  ☑ H3s: 2-4 per H2 (depth)
  ☑ Word count: Matches or exceeds competitor average
  ☑ Meta title: 50-60 chars, includes keyword + brand
  ☑ Meta description: 150-160 chars, CTA included
  ☑ Internal links: 3-5 relevant links
  ☑ External links: 3-5 authoritative links
  ☑ Keyword placement: H1, first paragraph, H2s, conclusion
  ☑ Keyword density: 1.5-2.5% (natural usage)

Step 2: Competitor Comparison
→ Compare YOUR structure to competitor patterns from Phase 2:
  ☑ Do you cover all universal H2 topics?
  ☑ Do you include gap topics (differentiation)?
  ☑ Is your word count competitive (match or +10-15%)?
  ☑ Is your H2 count appropriate (5-8)?
  ☑ Is your H3 depth adequate (2-4 per H2)?
  ☑ Do you match or exceed competitor schema markup?

Step 3: Related Keywords Integration Check
→ Review related keywords from Phase 1.2
→ Verify:
  ☑ High-volume related keywords in H2s
  ☑ Medium-volume keywords in H3s
  ☑ LSI keywords naturally integrated in body
  ☑ Long-tail variations in FAQ or sections

Step 4: SEO Element Checklist
→ Manual verification:
  ☑ Target keyword in H1
  ☑ Keyword variations in H2s (not just exact match)
  ☑ Keyword in first 100 words
  ☑ Keyword in conclusion
  ☑ LSI keywords throughout (natural placement)
  ☑ Meta title optimized (50-60 chars)
  ☑ Meta description optimized (150-160 chars + CTA)
  ☑ Internal links present (3-5 contextual)
  ☑ External authoritative links present (3-5)
  ☑ Image alt text (if images present)
  ☑ Proper heading hierarchy (no H3 before H2)
  ☑ No keyword stuffing (density < 3%)
```

**OUTPUT:**
- ✅ SEO validation report
- ✅ List of SEO issues to fix
- ✅ Confirmation article meets SEO baseline BEFORE editing
- ✅ Comparison against competitor benchmarks

**TOOLS:**
- `scripts/seo-validation-helper.py` - Automated validation
- Manual review - Pattern verification
- Competitor analysis from Phase 2 - Benchmark comparison

**CRITICAL:** Fix any SEO issues NOW before editing. Editing can accidentally break SEO if not careful.

---

### CHECKPOINT 5: Post-Editing SEO Verification (Phase 5 - After Editing)

**WHEN:** After ALL 11 editing frameworks applied, BEFORE final polish

**OBJECTIVE:** Ensure editing didn't break on-page SEO

**WORKFLOW:**

```
Step 1: Re-run Automated Validation
→ Use scripts/seo-validation-helper.py again
→ Command: python scripts/seo-validation-helper.py edited_draft.md "target keyword"
→ Compare: Results to pre-editing validation (Phase 3.5)
→ Flag: Any elements that changed

Step 2: Quick SEO Elements Check
→ Verify critical elements unchanged:
  ☑ H1 still includes keyword (editing didn't change it)
  ☑ H2s still have keyword variations (not removed)
  ☑ H2 count unchanged (5-8)
  ☑ H3 depth maintained (2-4 per H2)
  ☑ Meta title unchanged (still 50-60 chars)
  ☑ Meta description unchanged (still 150-160 chars)
  ☑ Keyword still in first paragraph (editing didn't remove)
  ☑ Keyword still in conclusion (editing didn't cut it)
  ☑ Internal links still present (editing didn't delete)
  ☑ External links still present

Step 3: Heading Hierarchy Verification
→ Ensure editing didn't break structure:
  ☑ Still single H1
  ☑ H2s in logical order
  ☑ No H3 before H2
  ☑ No orphaned H3s
  ☑ Hierarchy flows logically

Step 4: Keyword Density Re-check
→ Verify keyword not over-optimized or under-optimized:
  ☑ 1.5-2.5% keyword density (natural usage)
  ☑ Keyword variations present (not just exact match)
  ☑ LSI keywords still present
  ☑ No accidental keyword stuffing from editing

Step 5: Final Comparison
→ Compare to competitor benchmarks (Phase 2):
  ☑ Still meet or exceed word count target
  ☑ Still cover all universal topics
  ☑ Still include differentiation (gap topics)
  ☑ Still maintain competitive SEO elements
```

**OUTPUT:**
- ✅ Final SEO verification confirmation
- ✅ Any issues flagged for immediate fix
- ✅ Confirmation editing preserved SEO optimization
- ✅ Ready for final validation (Phase 6)

**TOOLS:**
- `scripts/seo-validation-helper.py` - Automated re-validation
- Manual spot-checks - Critical element verification

---

## Complete SEO-Enhanced Workflow Integration

**BEFORE (Old Workflow):**
```
Phase 0: Planning → Phase 2: Research (web_search_exa) → Phase 3: Draft → Phase 5: Edit
```

**AFTER (Enhanced with DataForSEO MCP):**
```
Phase 0: Strategic Planning
  ↓ ADD: Keyword Research (keyword_ideas + keyword_overview)
  ↓ ADD: Search Intent Validation (search_intent)
  ↓ ADD: SERP Analysis (serp_organic_live_advanced)
  ↓ ADD: Domain Authority Check (domain_rank_overview)
  ↓ ADD: Related Keywords (related_keywords)
  ↓ OUTPUT: SEO Strategy Report

Phase 1: Research Strategy Planning
  ↓ (existing planning)

Phase 1.2: SEO Data Gathering (NEW PHASE)
  ↓ ADD: Competitor Keyword Analysis (ranked_keywords)
  ↓ ADD: Keyword Expansion (keyword_ideas)
  ↓ ADD: SEO Intelligence Report compilation
  ↓ OUTPUT: Content Structure Targets

Phase 2: Deep Content Research
  ↓ ADD: Competitor On-Page SEO Analysis (Firecrawl/scraping)
  ↓ ADD: Pattern Analysis (universal topics + gaps)
  ↓ THEN: web_search_exa (with context of gaps identified)
  ↓ THEN: perplexity_research (focused on gaps)
  ↓ OUTPUT: Competitor SEO Report

Phase 3: Drafting
  ↓ (existing draft process with SEO targets)

Phase 3.5: Post-Draft SEO Validation (NEW CHECKPOINT)
  ↓ CHECK: On-page SEO elements (seo-validation-helper.py)
  ↓ CHECK: Heading structure and hierarchy
  ↓ CHECK: Keyword placement and density
  ↓ CHECK: Competitor benchmark comparison
  ↓ FIX: Any SEO issues before editing
  ↓ OUTPUT: SEO Validation Report

Phase 5: Comprehensive Editing
  ↓ (apply all 11 frameworks)

Phase 5.5: Post-Editing SEO Verification (NEW CHECKPOINT)
  ↓ RE-CHECK: On-page SEO elements
  ↓ VERIFY: Editing didn't break SEO
  ↓ COMPARE: Pre-edit vs post-edit validation
  ↓ OUTPUT: Final SEO Confirmation

Phase 6: Final Validation
  ↓ (existing checks)
  ↓ ADD: Final SEO sign-off
```

---

## SEO Analysis Best Practices

### 1. SERP First, Content Research Second
- **NEVER** search randomly for "articles about [topic]" with Exa.ai
- **ALWAYS** use `dataforseo_serp_organic_live_advanced` first to identify WHO ranks
- **THEN** use `dataforseo_labs_google_ranked_keywords` to understand competitor keyword strategy
- **THEN** use Exa.ai/Perplexity/Firecrawl to analyze those specific URLs
- **FINALLY** fill gaps you identified

### 2. Validate Search Intent Early
- Always run `dataforseo_labs_search_intent` after selecting keyword
- Only target keywords with > 60% informational intent for blog posts
- If transactional (< 40% informational), STOP - wrong content type
- Commercial intent (40-60%) can work for comparison/review content

### 3. Analyze Top 3-5 Only
- Don't analyze all 10 SERP results (diminishing returns)
- Focus on positions 1-5 (highest authority + most relevant)
- Check domain authority with `dataforseo_labs_google_domain_rank_overview`
- Look for patterns across these top performers

### 4. Document Patterns, Not Individual Details
- Track: "Average word count: 2,000-2,500"
- Not: "Competitor A: 2,100 words, Competitor B: 2,300 words"
- Patterns reveal what Google rewards
- Individual outliers can mislead

### 5. Use Keyword Data to Inform Structure
- Map high-volume related keywords to H2 sections
- Use medium-volume variations for H3 subtopics
- Integrate LSI keywords naturally (don't force)
- Include long-tail question keywords in FAQ sections

### 6. Identify Gaps (The Opportunity)
- What topics do competitors NOT cover?
- What keywords do they rank for but not optimize for?
- Where is their H3 depth shallow?
- What schema are they missing?
- These gaps = your competitive advantage

### 7. Validate Early, Verify After
- SEO validation BEFORE editing = less rework
- SEO verification AFTER editing = ensure you didn't break it
- Use automated tools (seo-validation-helper.py) for consistency
- Manual spot-checks for quality assurance

### 8. Balance SEO with Quality
- Don't over-optimize (keyword stuffing)
- SEO serves the content, not the other way around
- User experience > search engines (but both matter)
- Natural language > forced keyword placement

### 9. Leverage DataForSEO Intelligence
- Use competitor ranked keywords to understand their strategy
- Use related keywords for comprehensive topic coverage
- Use domain rank to set realistic expectations
- Use SERP features data to target snippets/PAA

### 10. Automate Where Possible
- Use `seo-validation-helper.py` for on-page checks
- Batch keyword analysis with `keyword_overview`
- Compile reports programmatically (Phase 1.2)
- Focus manual effort on strategic analysis

---

## DataForSEO Tool Sequence by Phase

### Phase 0 (Strategic Planning)
**Total Tools: 5**
1. `dataforseo_labs_google_keyword_ideas` (if no keyword)
2. `dataforseo_labs_google_keyword_overview` (validate keyword)
3. `dataforseo_labs_search_intent` (confirm informational)
4. `dataforseo_serp_organic_live_advanced` (get competitors)
5. `dataforseo_labs_google_domain_rank_overview` (assess authority)
6. `dataforseo_labs_google_related_keywords` (plan structure)

**Estimated Time: 15-20 minutes**

### Phase 1.2 (SEO Data Gathering)
**Total Tools: 2-3**
1. `dataforseo_labs_google_ranked_keywords` (competitor strategy)
2. `dataforseo_labs_google_keyword_ideas` (expand opportunities)
3. Compile SEO Intelligence Report (manual)

**Estimated Time: 20-30 minutes**

### Phase 2 (Deep Research)
**Total Tools: 0 (DataForSEO)**
- Use Firecrawl/web scraping for on-page analysis
- Cross-reference with keyword data from Phase 1.2
- Manual pattern analysis

**Estimated Time: 30-45 minutes**

### Phase 3.5 (Post-Draft Validation)
**Total Tools: 1 (script)**
- `seo-validation-helper.py` (automated checks)
- Manual verification

**Estimated Time: 10-15 minutes**

### Phase 5.5 (Post-Editing Verification)
**Total Tools: 1 (script)**
- `seo-validation-helper.py` (re-run)
- Manual spot-checks

**Estimated Time: 5-10 minutes**

---

## Location Codes Reference

Common location codes for `location_code` parameter:

- **United States:** 2840
- **United Kingdom:** 2826
- **Canada:** 2124
- **Australia:** 2036
- **Germany:** 2276
- **France:** 2250
- **Spain:** 2724
- **Italy:** 2380
- **Netherlands:** 2528
- **India:** 2356

For full list, see DataForSEO documentation.

---

## Language Codes Reference

Common language codes for `language_code` parameter:

- **English:** "en"
- **Spanish:** "es"
- **French:** "fr"
- **German:** "de"
- **Portuguese:** "pt"
- **Italian:** "it"
- **Dutch:** "nl"
- **Russian:** "ru"
- **Japanese:** "ja"
- **Chinese:** "zh"

---

## Integration with MAN Digital Brand

**Remember:**
- SEO serves MAN Digital's positioning as RevOps consultancy
- Optimize for RevOps-related search terms
- Use `dataforseo_labs_google_keyword_overview` to validate RevOps keyword volume
- Competitor analysis should validate our unique angle (process-first, not feature-first)
- On-page SEO should reinforce brand differentiators

**SEO Title Pattern:**
```
[Topic] for RevOps: [Benefit] | MAN Digital
```

**Meta Description Pattern:**
```
Transform [challenge] with [solution]. Learn how RevOps teams use [topic] to [benefit]. [CTA].
```

Both patterns already support SEO while maintaining brand positioning.

**RevOps Keyword Strategy:**
- Target "RevOps + [technology]" combinations
- Use `dataforseo_labs_search_intent` to find informational RevOps keywords
- Leverage `dataforseo_labs_google_related_keywords` for RevOps topic expansion
- Analyze RevOps competitor domains with `dataforseo_labs_google_domain_rank_overview`
