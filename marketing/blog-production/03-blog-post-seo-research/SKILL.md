---
name: blog-post-seo-research
description: Execute DataForSEO MCP tools to gather SEO validation data BEFORE blog post creation. This skill should be used when starting a new blog post project to validate keywords, analyze SERP competitors, assess competitor authority, and discover related keywords. Run this skill first, then pass the structured results to the blog-post-creation skill.
---

# Blog Post SEO Research

## Overview

This skill executes all DataForSEO MCP tools to provide validated SEO data before content creation begins. It serves as a pre-requisite step that prevents AI from skipping DataForSEO execution during content creation.

**Input:** Brief (or primary keyword)
**Output:** Structured DataForSEO results ready for blog-post-creation workflow

## Purpose

The skill has ONE job: **Execute DataForSEO tools and provide structured results.**

- ❌ Does NOT do content research (that's the main skill's job)
- ❌ Does NOT analyze competitors deeply (that's the main skill's job)
- ❌ Does NOT draft content (that's the main skill's job)
- ✅ DOES execute all 5 DataForSEO tools
- ✅ DOES paste actual results in structured format
- ✅ DOES hand off results to the user

## Workflow

### Step 1: Extract Primary Keyword

**From brief:**
- Read the brief provided by the user
- Identify the primary keyword (usually in "Primary Keyword" field)
- If no brief, user will provide keyword directly

**Output:**
```
Primary Keyword: [keyword]
```

---

### Step 2: Execute All 5 DataForSEO Tools

**⚠️ EXECUTE ALL 5 TOOLS IN ORDER - NO SKIPPING**

#### Tool 1: Search Intent Validation
```
mcp__dataforseo__labs_search_intent
```

**Parameters:**
- keyword: [primary keyword from Step 1]
- location_name: "United States"
- language_code: "en"

**Paste actual results here:**
```
[PASTE TOOL OUTPUT]
```

**Extract and document:**
- Informational intent: [X%]
- Transactional intent: [X%]
- Navigational intent: [X%]
- Commercial intent: [X%]

✅ Verification: Informational > 60%? → YES/NO

---

#### Tool 2: Keyword Metrics
```
mcp__dataforseo__labs_google_keyword_overview
```

**Parameters:**
- keywords: [[primary keyword]]
- location_name: "United States"
- language_code: "en"

**Paste actual results here:**
```
[PASTE TOOL OUTPUT]
```

**Extract and document:**
- Search volume: [X,XXX/month]
- Competition: [high/medium/low]
- Keyword difficulty: [0-100 score]
- 12-month trend: [rising/stable/declining]
- CPC: $[X.XX]

✅ Verification: Adequate volume for blog post? → YES/NO

---

#### Tool 3: SERP Rankings (MOST CRITICAL)
```
mcp__dataforseo__serp_organic_live_advanced
```

**Parameters:**
- keyword: [primary keyword]
- location_name: "United States"
- language_code: "en"
- depth: 10 (get top 10 results)

**Paste actual results here:**
```
[PASTE TOOL OUTPUT]
```

**Extract and document top 10 URLs:**
1. Position 1: [URL] - Domain: [domain] - Title: [title]
2. Position 2: [URL] - Domain: [domain] - Title: [title]
3. Position 3: [URL] - Domain: [domain] - Title: [title]
4. Position 4: [URL] - Domain: [domain] - Title: [title]
5. Position 5: [URL] - Domain: [domain] - Title: [title]
6. Position 6: [URL] - Domain: [domain] - Title: [title]
7. Position 7: [URL] - Domain: [domain] - Title: [title]
8. Position 8: [URL] - Domain: [domain] - Title: [title]
9. Position 9: [URL] - Domain: [domain] - Title: [title]
10. Position 10: [URL] - Domain: [domain] - Title: [title]

✅ These are the ONLY competitors the content skill should analyze

---

#### Tool 4: Top Competitor Authority
```
mcp__dataforseo__labs_google_domain_rank_overview
```

**Parameters:**
- target: [domain of position 1 result]
- location_name: "United States"
- language_code: "en"

**Paste actual results here:**
```
[PASTE TOOL OUTPUT]
```

**Extract and document:**
- Domain rank: [X]
- Organic keywords count: [X,XXX]
- Organic traffic: [X,XXX/month]
- Domain authority indicator: [score if available]

**Repeat for positions 2 and 3:**

**Position 2 Domain:**
```
[PASTE TOOL OUTPUT]
```
- Domain rank: [X]
- Organic keywords: [X,XXX]
- Organic traffic: [X,XXX/month]

**Position 3 Domain:**
```
[PASTE TOOL OUTPUT]
```
- Domain rank: [X]
- Organic keywords: [X,XXX]
- Organic traffic: [X,XXX/month]

✅ This shows the competitive landscape authority

---

#### Tool 5: Related Keywords Discovery
```
mcp__dataforseo__labs_google_related_keywords
```

**Parameters:**
- keyword: [primary keyword]
- location_name: "United States"
- language_code: "en"
- depth: 50 (get 50 related keywords)

**Paste actual results here:**
```
[PASTE TOOL OUTPUT]
```

**Extract and document by volume tier:**

**High-volume keywords (300+ monthly searches) - Use as H2 headings:**
1. [keyword] - Volume: [X,XXX] - Difficulty: [X]
2. [keyword] - Volume: [X,XXX] - Difficulty: [X]
3. [keyword] - Volume: [X,XXX] - Difficulty: [X]

**Medium-volume keywords (100-299 monthly searches) - Use as H3 headings:**
1. [keyword] - Volume: [XXX] - Difficulty: [X]
2. [keyword] - Volume: [XXX] - Difficulty: [X]
3. [keyword] - Volume: [XXX] - Difficulty: [X]

**LSI keywords (<100 monthly searches) - Use naturally in content:**
1. [keyword] - Volume: [XX]
2. [keyword] - Volume: [XX]
3. [keyword] - Volume: [XX]

✅ These keywords will guide H2/H3 structure and content optimization

---

## Step 3: Save Output and Provide as Artifact

**📊 DATAFORSEO PRE-RESEARCH COMPLETE**

**CRITICAL: Save results to markdown file AND provide as artifact**

### Create the Output File

**File naming:** `seo-research-[keyword-slug]-[date].md`

Example: `seo-research-hubspot-prospecting-agent-2025-01-25.md`

**File contents:**

```markdown
# SEO Research: [Primary Keyword]

**Date:** [YYYY-MM-DD]
**Keyword:** [primary keyword]

---

## Search Intent Analysis

- **Informational:** [X%]
- **Transactional:** [X%]
- **Navigational:** [X%]
- **Commercial:** [X%]

**✅ Blog post format appropriate:** YES/NO

---

## Keyword Metrics

- **Search volume:** [X,XXX/month]
- **Competition:** [high/medium/low]
- **Keyword difficulty:** [0-100 score]
- **12-month trend:** [rising/stable/declining]
- **CPC:** $[X.XX]

---

## SERP Competitors (Top 10)

Use THESE URLs for competitor analysis (NOT brief URLs):

1. [URL] - [Domain] - [Title]
2. [URL] - [Domain] - [Title]
3. [URL] - [Domain] - [Title]
4. [URL] - [Domain] - [Title]
5. [URL] - [Domain] - [Title]
6. [URL] - [Domain] - [Title]
7. [URL] - [Domain] - [Title]
8. [URL] - [Domain] - [Title]
9. [URL] - [Domain] - [Title]
10. [URL] - [Domain] - [Title]

---

## Competitor Authority

### Top 3 Domain Analysis

**Position 1: [domain]**
- Domain rank: [X]
- Organic keywords: [X,XXX]
- Organic traffic: [X,XXX/month]

**Position 2: [domain]**
- Domain rank: [X]
- Organic keywords: [X,XXX]
- Organic traffic: [X,XXX/month]

**Position 3: [domain]**
- Domain rank: [X]
- Organic keywords: [X,XXX]
- Organic traffic: [X,XXX/month]

**Authority Assessment:** [High/Medium/Low]

**Strategy:** [Based on authority level, recommend approach]

---

## Related Keywords for Structure

### H2 Opportunities (High-volume: 300+)

1. [keyword] - Vol: [X,XXX] - Difficulty: [X]
2. [keyword] - Vol: [X,XXX] - Difficulty: [X]
3. [keyword] - Vol: [X,XXX] - Difficulty: [X]
4. [keyword] - Vol: [X,XXX] - Difficulty: [X]
5. [keyword] - Vol: [X,XXX] - Difficulty: [X]

### H3 Opportunities (Medium-volume: 100-299)

1. [keyword] - Vol: [XXX] - Difficulty: [X]
2. [keyword] - Vol: [XXX] - Difficulty: [X]
3. [keyword] - Vol: [XXX] - Difficulty: [X]
4. [keyword] - Vol: [XXX] - Difficulty: [X]
5. [keyword] - Vol: [XXX] - Difficulty: [X]

### LSI Keywords (Low-volume: <100)

[keyword 1], [keyword 2], [keyword 3], [keyword 4], [keyword 5], [keyword 6], [keyword 7], [keyword 8]

---

## SEO Strategy Summary

**Target Position:** [1-3 / 4-7 / 8-10]

**Differentiation Strategy:**
- [Key differentiator 1]
- [Key differentiator 2]
- [Key differentiator 3]

**Content Gaps to Fill:**
- [Gap 1]
- [Gap 2]
- [Gap 3]

**Word Count Target:** [Based on competitor analysis]

**H2 Count Target:** [Based on competitor analysis]

**H3 Count Target:** [Based on competitor analysis]

---

## Next Steps

1. Provide this file to blog-post-creation skill along with the brief
2. Blog-post-creation will use SERP URLs (not brief URLs) for analysis
3. H2/H3 structure will follow related keywords mapping
4. Draft will be validated against this research before editing
```

### Provide as Artifact

**After creating the file, provide it as an artifact in the conversation:**

Use the artifact feature to display the complete SEO research file so the user can:
1. Review the research without cluttering conversation
2. Easily save/download the file
3. Reference it while working with blog-post-creation skill

**✅ MISSION COMPLETE**

**User receives:**
1. ✅ Markdown file saved to disk: `seo-research-[keyword]-[date].md`
2. ✅ Artifact in conversation for easy reference
3. ✅ Ready to provide to blog-post-creation skill along with brief

---

## Common Issues & Fixes

**Issue 1:** Tool execution fails
- Check MCP connection is active
- Verify DataForSEO API key is configured
- Retry with correct parameters

**Issue 2:** No results returned
- Verify keyword has search volume
- Try broader keyword variation
- Check location/language settings

**Issue 3:** Want to skip a tool
- ❌ NOT ALLOWED - All 5 tools are mandatory
- Each tool serves a specific purpose
- Missing data = incomplete research

---

## Notes

- Run this skill BEFORE blog-post-creation
- Results are input for blog-post-creation skill
- Keep results for 30 days (SERP data can change)
- Re-run if creating content for same keyword after 30 days

---

## Resources

This skill includes comprehensive supporting materials:

### References

**`references/dataforseo-tools-reference.md`**
Complete reference for all 5 DataForSEO tools with:
- Tool purposes and use cases
- Parameter specifications
- Example responses
- How to interpret results
- Best practices

**`references/locations-languages.md`**
Location and language codes reference:
- Common locations (US, UK, Canada, Australia, etc.)
- Language codes (en, es, fr, de, etc.)
- Usage examples for different regions
- Multi-region content strategies

**`references/troubleshooting.md`**
Troubleshooting guide for common issues:
- Tool execution failures
- No results returned
- Wrong intent detection
- High difficulty keywords
- Parameter errors
- Rate limiting

### Examples

**`examples/complete-workflow-example.md`**
Full end-to-end example showing:
- Complete 5-tool execution
- Real keyword: "hubspot prospecting agent"
- Actual results and analysis
- How to use results in blog-post-creation
- Strategic insights for content

**`examples/troubleshooting-example.md`**
Real-world troubleshooting scenario:
- Initial keyword with wrong intent
- Keyword adjustment iterations
- Volume vs difficulty tradeoffs
- High authority competitor strategies
- Final successful outcome

### Scripts

**`scripts/format_output.py`**
Python helper script to format DataForSEO results:
- Converts raw JSON to structured output
- Ensures consistent formatting
- Validates all required sections
- Saves formatted results to file

**Usage:**
```bash
python3 scripts/format_output.py
```

The script prompts for input and generates properly formatted output ready for blog-post-creation skill.

---

## Quick Start

**First time using this skill?**

1. Read `references/dataforseo-tools-reference.md` for tool details
2. Review `examples/complete-workflow-example.md` for workflow understanding
3. Check `references/locations-languages.md` for your target region
4. Execute the 5 tools following the workflow in SKILL.md
5. If issues occur, consult `references/troubleshooting.md`

**For experienced users:**

1. Extract keyword from brief
2. Execute all 5 tools with consistent location/language
3. Paste actual results
4. Format output (optionally use `scripts/format_output.py`)
5. Hand off to blog-post-creation skill
