# Complete Workflow Example

This example shows the complete blog-post-seo-research skill in action.

---

## Scenario

**Client Request:** "Write a blog post about HubSpot's prospecting agent"

**Brief Provided:** Yes (includes keyword: "hubspot prospecting agent")

---

## Step 1: Extract Primary Keyword

**Action:** Read the brief and identify the primary keyword

**Result:**
```
Primary Keyword: hubspot prospecting agent
```

---

## Step 2: Execute All 5 DataForSEO Tools

### Tool 1: Search Intent Validation

**Tool Called:** `mcp__dataforseo__labs_search_intent`

**Parameters:**
```json
{
  "keyword": "hubspot prospecting agent",
  "location_name": "United States",
  "language_code": "en"
}
```

**Results:**
```
Informational intent: 78%
Transactional intent: 12%
Navigational intent: 8%
Commercial intent: 2%
```

**✅ Verification:** Informational > 60%? → **YES** (78% informational)

**Analysis:** Strong informational intent - perfect for blog post format.

---

### Tool 2: Keyword Metrics

**Tool Called:** `mcp__dataforseo__labs_google_keyword_overview`

**Parameters:**
```json
{
  "keywords": ["hubspot prospecting agent"],
  "location_name": "United States",
  "language_code": "en"
}
```

**Results:**
```
Search volume: 1,200/month
Competition: low
Keyword difficulty: 35
12-month trend: rising (+15% from 1,050 to 1,200)
CPC: $4.50
```

**✅ Verification:** Adequate volume for blog post? → **YES** (1,200/month is solid)

**Analysis:**
- Good search volume for B2B SaaS topic
- Low competition = opportunity
- Rising trend = timely content
- Difficulty 35 = realistic to rank

---

### Tool 3: SERP Rankings

**Tool Called:** `mcp__dataforseo__serp_organic_live_advanced`

**Parameters:**
```json
{
  "keyword": "hubspot prospecting agent",
  "location_name": "United States",
  "language_code": "en",
  "depth": 10
}
```

**Results:**
```
Top 10 SERP URLs (Fresh data from 2025-01-25):

Position 1: https://www.hubspot.com/products/crm/prospecting-agent
Domain: hubspot.com
Title: HubSpot Prospecting Agent | AI-Powered Sales Tool

Position 2: https://blog.hubspot.com/sales/prospecting-agent-guide
Domain: hubspot.com
Title: How to Use HubSpot's Prospecting Agent: Complete Guide

Position 3: https://www.salesforce.com/resources/articles/hubspot-prospecting-tools/
Domain: salesforce.com
Title: Understanding HubSpot's AI Prospecting Agent

Position 4: https://www.gartner.com/reviews/market/sales-engagement-platforms/vendor/hubspot/product/hubspot-sales-hub
Domain: gartner.com
Title: HubSpot Sales Hub Reviews - Gartner Peer Insights

Position 5: https://www.revops.com/blog/hubspot-prospecting-agent-review
Domain: revops.com
Title: HubSpot Prospecting Agent Review: Is It Worth It?

Position 6: https://www.forbes.com/advisor/business/software/best-sales-prospecting-tools/
Domain: forbes.com
Title: Best Sales Prospecting Tools 2025

Position 7: https://www.techradar.com/pro/hubspot-breeze-ai-agents-review
Domain: techradar.com
Title: HubSpot Breeze AI Agents Review

Position 8: https://www.capterra.com/p/140788/HubSpot-CRM/
Domain: capterra.com
Title: HubSpot CRM Reviews, Ratings & Features 2025

Position 9: https://www.softwareadvice.com/crm/hubspot-profile/
Domain: softwareadvice.com
Title: HubSpot CRM Software - 2025 Reviews, Pricing & Demo

Position 10: https://martech.org/hubspot-launches-ai-prospecting-agent/
Domain: martech.org
Title: HubSpot Launches AI-Powered Prospecting Agent
```

**✅ These are the ONLY competitors the content skill should analyze**

**Analysis:**
- Positions 1-2: HubSpot owns (official docs + blog)
- Position 3: Competitor comparison
- Positions 4-9: Review/comparison sites
- Position 10: News/announcement

**Content Patterns:**
- Mix of official docs, guides, reviews, and comparisons
- Opportunity: Deep "how-to" guide from consultancy perspective

---

### Tool 4: Top Competitor Authority

**Tool Called:** `mcp__dataforseo__labs_google_domain_rank_overview`

**Executed for positions 1, 2, 3:**

**Position 1 Domain: hubspot.com**
```
Domain rank: 125
Organic keywords: 1,250,000
Organic traffic: 45,000,000/month
```

**Position 2 Domain: hubspot.com** (same as position 1)

**Position 3 Domain: salesforce.com**
```
Domain rank: 87
Organic keywords: 2,100,000
Organic traffic: 62,000,000/month
```

**✅ Competitive landscape authority:** **VERY HIGH**

**Analysis:**
- Top 2 positions owned by HubSpot (product page + guide)
- Position 3 is Salesforce (even higher authority)
- **Strategy:** Focus on differentiation - RevOps consultancy angle, implementation expertise, real-world use cases
- Cannot outrank on authority alone - need content gaps

---

### Tool 5: Related Keywords Discovery

**Tool Called:** `mcp__dataforseo__labs_google_related_keywords`

**Parameters:**
```json
{
  "keyword": "hubspot prospecting agent",
  "location_name": "United States",
  "language_code": "en",
  "depth": 50
}
```

**Results:**

**High-volume keywords (300+) - Use as H2 headings:**
1. prospecting agent hubspot - Volume: 850 - Difficulty: 32
2. hubspot ai prospecting - Volume: 650 - Difficulty: 28
3. hubspot breeze prospecting - Volume: 520 - Difficulty: 30
4. hubspot sales agent - Volume: 480 - Difficulty: 35
5. prospecting automation hubspot - Volume: 420 - Difficulty: 27
6. hubspot ai agents - Volume: 380 - Difficulty: 33

**Medium-volume keywords (100-299) - Use as H3 headings:**
1. how to use prospecting agent - Volume: 280 - Difficulty: 25
2. prospecting agent features - Volume: 240 - Difficulty: 22
3. hubspot prospecting tools - Volume: 220 - Difficulty: 26
4. prospecting agent setup - Volume: 190 - Difficulty: 20
5. hubspot prospecting vs salesforce - Volume: 180 - Difficulty: 28
6. prospecting agent pricing - Volume: 150 - Difficulty: 24
7. best hubspot prospecting practices - Volume: 130 - Difficulty: 21
8. hubspot prospecting integration - Volume: 120 - Difficulty: 23

**LSI keywords (<100) - Use naturally in content:**
1. ai-powered prospecting - Volume: 95
2. automated lead research - Volume: 85
3. sales automation hubspot - Volume: 75
4. prospecting workflow - Volume: 70
5. lead enrichment hubspot - Volume: 65
6. outbound prospecting - Volume: 60
7. prospecting sequences - Volume: 55
8. crm prospecting - Volume: 50

**✅ These keywords will guide H2/H3 structure and content optimization**

---

## Step 3: Final Output Summary

**📊 DATAFORSEO SEO RESEARCH RESULTS**

```
=== DATAFORSEO SEO RESEARCH RESULTS ===
Date: 2025-01-25
Primary Keyword: hubspot prospecting agent

SEARCH INTENT:
- Informational: 78%
- Transactional: 12%
- ✅ Blog post format appropriate: YES

KEYWORD METRICS:
- Search volume: 1,200/month
- Competition: low
- Keyword difficulty: 35
- Trend: rising (+15% over 12 months)

TOP 10 SERP COMPETITORS (USE THESE URLS FOR ANALYSIS):
1. https://www.hubspot.com/products/crm/prospecting-agent
2. https://blog.hubspot.com/sales/prospecting-agent-guide
3. https://www.salesforce.com/resources/articles/hubspot-prospecting-tools/
4. https://www.gartner.com/reviews/market/sales-engagement-platforms/vendor/hubspot
5. https://www.revops.com/blog/hubspot-prospecting-agent-review
6. https://www.forbes.com/advisor/business/software/best-sales-prospecting-tools/
7. https://www.techradar.com/pro/hubspot-breeze-ai-agents-review
8. https://www.capterra.com/p/140788/HubSpot-CRM/
9. https://www.softwareadvice.com/crm/hubspot-profile/
10. https://martech.org/hubspot-launches-ai-prospecting-agent/

TOP 3 COMPETITOR AUTHORITY:
1. hubspot.com - Rank: 125 - Organic Keywords: 1,250,000 - Traffic: 45M/mo
2. hubspot.com - Rank: 125 - Organic Keywords: 1,250,000 - Traffic: 45M/mo
3. salesforce.com - Rank: 87 - Organic Keywords: 2,100,000 - Traffic: 62M/mo

RELATED KEYWORDS FOR STRUCTURE:
H2 Opportunities (high-volume):
- prospecting agent hubspot - Vol: 850
- hubspot ai prospecting - Vol: 650
- hubspot breeze prospecting - Vol: 520
- hubspot sales agent - Vol: 480
- prospecting automation hubspot - Vol: 420
- hubspot ai agents - Vol: 380

H3 Opportunities (medium-volume):
- how to use prospecting agent - Vol: 280
- prospecting agent features - Vol: 240
- hubspot prospecting tools - Vol: 220
- prospecting agent setup - Vol: 190
- hubspot prospecting vs salesforce - Vol: 180
- prospecting agent pricing - Vol: 150
- best hubspot prospecting practices - Vol: 130
- hubspot prospecting integration - Vol: 120

LSI Keywords (natural integration):
- ai-powered prospecting, automated lead research, sales automation hubspot, prospecting workflow, lead enrichment hubspot, outbound prospecting, prospecting sequences, crm prospecting

=== END DATAFORSEO SEO RESEARCH ===
```

---

## Next Steps

**✅ Pre-research complete** - Hand this output to user

**User Action:** Provide this structured data along with the brief to the `blog-post-creation` skill

**Content Creation Will Use:**
- SERP URLs (not brief URLs) for competitor analysis
- Related keywords for H2/H3 structure planning
- Search intent validation (78% informational = perfect for blog)
- Keyword difficulty (35 = realistic target)
- Competitor authority (very high = focus on differentiation)

---

## Key Insights for Content Creation

1. **Competition Strategy:**
   - HubSpot owns positions 1-2 (official content)
   - Cannot beat on authority alone
   - **Angle:** RevOps consultancy implementation guide
   - **Differentiation:** Real-world use cases, setup guidance, integration with RevOps workflows

2. **Content Structure:**
   - H2: Use high-volume related keywords (prospecting agent hubspot, hubspot ai prospecting, etc.)
   - H3: Use medium-volume keywords (how to use, features, setup, pricing, etc.)
   - Natural: Integrate LSI keywords throughout

3. **SEO Targets:**
   - Target positions 5-10 (review/guide sites)
   - Aim for featured snippet with "how to use" section
   - Focus on comprehensive implementation guide

4. **Word Count Target:**
   - Positions 2-3 are 2,000-2,500 words
   - Target: 1,800-2,200 words (detailed but focused)
