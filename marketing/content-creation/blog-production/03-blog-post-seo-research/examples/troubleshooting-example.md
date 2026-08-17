# Troubleshooting Example

Real-world example showing what to do when things go wrong during pre-research.

---

## Scenario

**Client Request:** "Write a blog post about buying AI sales tools"

**Initial Keyword from Brief:** "buy ai sales tools"

---

## Attempt 1: Initial Run

### Step 1: Extract Keyword
```
Primary Keyword: buy ai sales tools
```

### Step 2: Execute Tool 1 - Search Intent

**Tool Called:** `mcp__dataforseo__labs_search_intent`

**Results:**
```
Informational intent: 25%
Transactional intent: 65%
Navigational intent: 5%
Commercial intent: 5%
```

**❌ Verification:** Informational > 60%? → **NO** (only 25%)

---

## Problem Identified: Wrong Intent

**Analysis:**
- Keyword has transactional intent (65%)
- "buy" indicates purchase intent, not learning intent
- Blog post format NOT appropriate
- Need to adjust keyword

---

## Solution: Adjust Keyword

### Option A: Remove "buy" trigger
```
Old: "buy ai sales tools"
New: "ai sales tools"
```

### Option B: Make informational
```
Old: "buy ai sales tools"
New: "ai sales tools comparison"
```

### Option C: Educational angle
```
Old: "buy ai sales tools"
New: "choosing ai sales tools"
```

**Decision:** Try Option C - "choosing ai sales tools"

---

## Attempt 2: Corrected Keyword

### Step 1: New Keyword
```
Primary Keyword: choosing ai sales tools
```

### Step 2: Execute Tool 1 - Search Intent (Retry)

**Tool Called:** `mcp__dataforseo__labs_search_intent`

**Results:**
```
Informational intent: 72%
Transactional intent: 18%
Navigational intent: 6%
Commercial intent: 4%
```

**✅ Verification:** Informational > 60%? → **YES** (72%)

**Analysis:** Much better! Educational/comparison angle works.

---

### Step 3: Execute Tool 2 - Keyword Metrics

**Tool Called:** `mcp__dataforseo__labs_google_keyword_overview`

**Results:**
```
Search volume: 90/month
Competition: low
Keyword difficulty: 38
12-month trend: stable
```

**⚠️ Issue:** Volume only 90/month - quite low

---

## Problem Identified: Low Search Volume

**Analysis:**
- 90 searches/month is very low
- May not generate enough traffic
- Consider broader variation

---

## Solution: Find Higher Volume Variation

### Check Related Terms

Let's try a broader term: "ai sales tools"

### Step 3 (Retry): Execute Tool 2 with Broader Term

**Keyword:** "ai sales tools"

**Tool Called:** `mcp__dataforseo__labs_google_keyword_overview`

**Results:**
```
Search volume: 1,800/month
Competition: medium
Keyword difficulty: 45
12-month trend: rising (+25%)
```

**✅ Much better:** 1,800/month with rising trend

**But wait - check intent for this broader term:**

### Step 2 (Retry): Verify Intent for Broader Term

**Tool Called:** `mcp__dataforseo__labs_search_intent`

**Keyword:** "ai sales tools"

**Results:**
```
Informational intent: 68%
Transactional intent: 22%
Navigational intent: 6%
Commercial intent: 4%
```

**✅ Verification:** Still > 60% informational

---

## Decision: Use "ai sales tools"

**Final Keyword:** "ai sales tools"
- ✅ Informational intent: 68%
- ✅ Volume: 1,800/month
- ✅ Rising trend: +25%
- ✅ Difficulty: 45 (manageable)

---

## Continue with Corrected Keyword

### Step 4: Execute Tool 3 - SERP Analysis

**Tool Called:** `mcp__dataforseo__serp_organic_live_advanced`

**Parameters:**
```json
{
  "keyword": "ai sales tools",
  "location_name": "United States",
  "language_code": "en",
  "depth": 10
}
```

**Results:**
```
Position 1: https://www.gartner.com/reviews/market/sales-engagement-platforms
Position 2: https://www.forbes.com/advisor/business/software/best-ai-sales-tools/
Position 3: https://www.salesforce.com/blog/ai-sales-tools/
Position 4: https://www.hubspot.com/products/sales/ai-tools
Position 5: https://www.g2.com/categories/ai-sales-tools
Position 6: https://www.capterra.com/sales-software/ai-sales-tools/
Position 7: https://revops.com/blog/ai-sales-tools-guide
Position 8: https://www.techradar.com/pro/best-ai-sales-tools
Position 9: https://www.softwareadvice.com/sales/ai-comparison/
Position 10: https://martech.org/best-ai-sales-tools-2025/
```

**✅ Good mix:** Reviews, comparisons, guides

---

### Step 5: Execute Tool 4 - Competitor Authority

**Tool Called:** `mcp__dataforseo__labs_google_domain_rank_overview`

**Position 1: gartner.com**
```
Domain rank: 245
Organic keywords: 950,000
Organic traffic: 35,000,000/month
```

**Position 2: forbes.com**
```
Domain rank: 52
Organic keywords: 3,200,000
Organic traffic: 125,000,000/month
```

**Position 3: salesforce.com**
```
Domain rank: 87
Organic keywords: 2,100,000
Organic traffic: 62,000,000/month
```

**⚠️ Issue:** VERY high authority competitors

---

## Problem Identified: High Authority SERP

**Analysis:**
- Top 3 positions = major brands (Gartner, Forbes, Salesforce)
- Domain ranks all < 300 (extremely high authority)
- Cannot compete on authority alone

---

## Solution: Focus on Differentiation

**Strategy:**
1. **Target positions 5-10** (more realistic)
2. **RevOps consultancy angle** (unique perspective)
3. **Implementation focus** (not just lists/reviews)
4. **Real-world use cases** (hands-on expertise)
5. **HubSpot integration angle** (niche specialization)

**Content Angle:**
"AI Sales Tools for RevOps Teams: Implementation Guide"

---

### Step 6: Execute Tool 5 - Related Keywords

**Tool Called:** `mcp__dataforseo__labs_google_related_keywords`

**Parameters:**
```json
{
  "keyword": "ai sales tools",
  "location_name": "United States",
  "language_code": "en",
  "depth": 50
}
```

**Results Summary:**

**High-volume (300+) - H2 opportunities:**
1. best ai sales tools - Vol: 1,500
2. ai powered sales tools - Vol: 850
3. ai sales assistant tools - Vol: 620
4. ai for sales teams - Vol: 580
5. sales ai tools - Vol: 520
6. artificial intelligence sales tools - Vol: 450

**Medium-volume (100-299) - H3 opportunities:**
1. how to use ai sales tools - Vol: 280
2. ai sales tools comparison - Vol: 240
3. ai sales automation tools - Vol: 220
4. best ai tools for sales reps - Vol: 190
5. ai sales prospecting tools - Vol: 180
6. ai tools for b2b sales - Vol: 150

**LSI keywords (<100):**
ai sales enablement, predictive analytics sales, ai lead scoring, sales forecasting ai, ai email outreach, conversation intelligence, etc.

---

## Final Output (After Corrections)

```
=== DATAFORSEO SEO RESEARCH RESULTS ===
Date: 2025-01-25
Primary Keyword: ai sales tools

SEARCH INTENT:
- Informational: 68%
- Transactional: 22%
- ✅ Blog post format appropriate: YES

KEYWORD METRICS:
- Search volume: 1,800/month
- Competition: medium
- Keyword difficulty: 45
- Trend: rising (+25%)

TOP 10 SERP COMPETITORS:
1. https://www.gartner.com/reviews/market/sales-engagement-platforms
2. https://www.forbes.com/advisor/business/software/best-ai-sales-tools/
3. https://www.salesforce.com/blog/ai-sales-tools/
4. https://www.hubspot.com/products/sales/ai-tools
5. https://www.g2.com/categories/ai-sales-tools
6. https://www.capterra.com/sales-software/ai-sales-tools/
7. https://revops.com/blog/ai-sales-tools-guide
8. https://www.techradar.com/pro/best-ai-sales-tools
9. https://www.softwareadvice.com/sales/ai-comparison/
10. https://martech.org/best-ai-sales-tools-2025/

TOP 3 COMPETITOR AUTHORITY:
1. gartner.com - Rank: 245 - Organic Keywords: 950,000 - Traffic: 35M/mo
2. forbes.com - Rank: 52 - Organic Keywords: 3,200,000 - Traffic: 125M/mo
3. salesforce.com - Rank: 87 - Organic Keywords: 2,100,000 - Traffic: 62M/mo

RELATED KEYWORDS FOR STRUCTURE:
H2 Opportunities (high-volume):
- best ai sales tools - Vol: 1,500
- ai powered sales tools - Vol: 850
- ai sales assistant tools - Vol: 620
- ai for sales teams - Vol: 580
- sales ai tools - Vol: 520
- artificial intelligence sales tools - Vol: 450

H3 Opportunities (medium-volume):
- how to use ai sales tools - Vol: 280
- ai sales tools comparison - Vol: 240
- ai sales automation tools - Vol: 220
- best ai tools for sales reps - Vol: 190
- ai sales prospecting tools - Vol: 180
- ai tools for b2b sales - Vol: 150

LSI Keywords (natural integration):
- ai sales enablement, predictive analytics sales, ai lead scoring, sales forecasting ai, ai email outreach, conversation intelligence

=== END DATAFORSEO SEO RESEARCH ===
```

---

## Lessons Learned

### 1. Check Intent First
- Don't proceed if intent is wrong
- "Buy" keywords = transactional
- Adjust to informational angle

### 2. Balance Volume and Difficulty
- "choosing ai sales tools" = 90/month (too low)
- "ai sales tools" = 1,800/month (better)
- Always check volume before committing

### 3. High Authority SERP = Differentiation Strategy
- Can't beat Forbes/Gartner on authority
- Focus on unique angle (RevOps consultancy)
- Target positions 5-10, not 1-3

### 4. Keyword Iterations are Normal
- First attempt: "buy ai sales tools" (wrong intent)
- Second attempt: "choosing ai sales tools" (low volume)
- Third attempt: "ai sales tools" (perfect)
- This is expected - iterate until right

### 5. Communicate Changes to User
```
"The initial keyword 'buy ai sales tools' has transactional intent (65%),
not suitable for blog post format. I've adjusted to 'ai sales tools'
which has 68% informational intent and 1,800/month search volume.
This is a better target for the blog post. Proceed?"
```

---

## Summary

**What went wrong:**
1. Initial keyword had wrong intent (transactional, not informational)
2. First correction had too low volume (90/month)
3. Competitors have very high authority

**How it was fixed:**
1. Adjusted keyword to remove "buy" trigger
2. Tested broader variation with better volume
3. Validated new keyword has correct intent
4. Developed differentiation strategy for high-authority SERP

**Final result:**
- ✅ Correct keyword: "ai sales tools"
- ✅ Proper intent: 68% informational
- ✅ Good volume: 1,800/month
- ✅ Rising trend: +25%
- ✅ Realistic difficulty: 45
- ✅ Clear strategy: RevOps consultancy angle

**Key takeaway:** Expect iterations. First keyword is rarely perfect. Use the tools to guide adjustments, not just validate assumptions.
