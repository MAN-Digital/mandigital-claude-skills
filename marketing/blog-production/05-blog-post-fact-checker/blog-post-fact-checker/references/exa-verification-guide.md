# Exa.ai Verification Guide

## Overview

This guide provides comprehensive instructions for using `mcp__MCP_DOCKER__web_search_exa` to verify factual claims in blog posts.

---

## Tool Basics

### Tool Name
```
mcp__MCP_DOCKER__web_search_exa
```

### Parameters
- **query** (string, required): Search query
- **numResults** (number, optional): Number of results to return (default: 5, recommended: 3-5)

### Returns
- Array of search results with URLs, titles, content snippets, and metadata
- Results ranked by relevance to query
- Full text content for verification

---

## Query Construction Strategies

### For Statistics (STAT)

**Goal:** Find original research data with specific numbers

**Query Pattern:**
```
"[topic] statistics [year]"
"[topic] adoption rate report [year]"
"[specific metric] data [year] Gartner Forrester"
```

**Examples:**
```
Query: "AI marketing adoption statistics 2024 2025"
Query: "martech spending report 2024 Gartner"
Query: "email open rates statistics 2024"
```

**Tips:**
- Include year (2024/2025) for current data
- Add authority names (Gartner, Forrester) to filter results
- Use "statistics", "data", "report" keywords
- Be specific with metric (adoption, spending, usage)

### For Product Features (PRODUCT)

**Goal:** Find official documentation confirming capabilities

**Query Pattern:**
```
"[product name] [feature] documentation official"
"[product name] [feature] capabilities"
"[product name] [integration/feature] support"
```

**Examples:**
```
Query: "HubSpot AI agents documentation official"
Query: "Salesforce Einstein features capabilities"
Query: "Slack Salesforce integration support"
```

**Tips:**
- Use product AND feature name
- Include "official" or "documentation"
- Add "capabilities" or "features"
- For integrations, name both platforms

### For Industry Trends (TREND)

**Goal:** Find research reports validating trends

**Query Pattern:**
```
"[trend topic] report 2024 Gartner Forrester"
"[trend] market analysis 2024"
"[trend] industry survey 2024"
```

**Examples:**
```
Query: "AI automation trends report 2024 Gartner"
Query: "marketing technology consolidation 2024"
Query: "remote work adoption survey 2024"
```

**Tips:**
- Include "report", "survey", "analysis"
- Add year + research firm names
- Focus on market/industry level
- Use present tense for current trends

### For Technical Accuracy (TECHNICAL)

**Goal:** Find authoritative technical documentation

**Query Pattern:**
```
"[technical concept] how it works documentation"
"[technology] architecture specification"
"[protocol/standard] official documentation"
```

**Examples:**
```
Query: "OAuth 2.0 how it works documentation"
Query: "GraphQL architecture specification"
Query: "REST API principles documentation"
```

**Tips:**
- Use "how it works" or "architecture"
- Include "documentation" or "specification"
- Look for .org or official sites
- Tech vendors or standards bodies

### For Comparative Claims (COMPARATIVE)

**Goal:** Find objective comparisons or rankings

**Query Pattern:**
```
"[topic] comparison 2024"
"[category] best tools review 2024"
"[product A] vs [product B] comparison"
```

**Examples:**
```
Query: "CRM platforms comparison 2024"
Query: "email marketing tools review 2024"
Query: "HubSpot vs Salesforce comparison"
```

**Tips:**
- Include "comparison", "review", or "vs"
- Add year for current data
- Look for independent review sites
- Check for methodology transparency

### For Temporal Claims (TEMPORAL)

**Goal:** Verify dates, timelines, and historical facts

**Query Pattern:**
```
"[event] [specific year]"
"[product] launch date"
"[company] founded when"
```

**Examples:**
```
Query: "ChatGPT launch date 2022"
Query: "HubSpot founded when"
Query: "GDPR effective date 2018"
```

**Tips:**
- Be very specific with years
- Use "when", "date", "year"
- Look for press releases or announcements
- Verify with multiple sources

### For Attribution Claims (ATTRIBUTION)

**Goal:** Verify quotes and attributed statements

**Query Pattern:**
```
"[person name] [topic] quote"
"[source name] [topic] report 2024"
"[expert] said [topic]"
```

**Examples:**
```
Query: "Marc Benioff AI salesforce quote"
Query: "Gartner marketing technology report 2024"
Query: "Forrester customer experience research"
```

**Tips:**
- Include person/organization name
- Add topic context
- Look for original sources
- Verify quote accuracy

---

## Interpreting Search Results

### What Exa Returns

For each result, you'll receive:
- **URL**: Web address of the source
- **Title**: Page title
- **Text**: Content snippet or full text
- **publishedDate**: When content was published
- **Author**: Content author (if available)
- **Image**: Featured image (if available)

### Evaluation Checklist

For EACH result returned:

#### 1. Check Domain Authority
```
Extract domain from URL
→ Is it Tier 1, 2, or 3?
→ See source-authority-hierarchy.md
```

#### 2. Verify Content Match
```
Read the text snippet
→ Does it actually confirm the claim?
→ Or just mentions related topics?
→ Is this the ORIGINAL source or citing another?
```

#### 3. Check Publication Date
```
Review publishedDate
→ Is it current (2024-2025)?
→ Is it appropriate for the claim?
→ Flag if outdated
```

#### 4. Assess Original vs. Secondary
```
Read for citations
→ Does text say "According to [X]..."?
→ If yes, this is SECONDARY source
→ Need to find original [X]
```

#### 5. Extract Supporting Evidence
```
Find relevant quote
→ Copy exact supporting text
→ Note context around quote
→ Verify numbers/facts match
```

### Example Result Evaluation

**Claim:** "85% of marketers use AI tools"

**Exa Result:**
```json
{
  "url": "https://www.hubspot.com/state-of-marketing-2024",
  "title": "State of Marketing Report 2024",
  "text": "Our survey of 1,200 marketers found that 82% now regularly use AI-powered tools in their workflows...",
  "publishedDate": "2024-03-15",
  "author": "HubSpot Research Team"
}
```

**Evaluation:**
1. **Domain Authority:** hubspot.com → Tier 1 ✅
2. **Content Match:** Confirms AI adoption (82% vs claimed 85%) → Close match ✅
3. **Publication Date:** March 2024 → Current ✅
4. **Original Source:** "Our survey" → This IS original research ✅
5. **Supporting Evidence:** "82% now regularly use AI-powered tools"

**Assessment:** ✅ VERIFIED (with minor discrepancy: 82% vs 85%)
**Recommendation:** Update claim to cite exact stat: "According to HubSpot's 2024 State of Marketing report, 82% of marketers..."

---

## Cross-Referencing Multiple Sources

### Why Cross-Reference?

- Confirms accuracy across authorities
- Identifies conflicts or variations
- Strengthens verification confidence
- Catches misattributed data

### Process

1. **Execute Initial Query**
   ```
   results = mcp__MCP_DOCKER__web_search_exa(
       query="AI marketing adoption 2024",
       numResults=5
   )
   ```

2. **Evaluate Each Result**
   - Check authority tier
   - Verify content match
   - Note specific data points

3. **Compare Findings**
   ```
   Source 1 (Tier 1): 82%
   Source 2 (Tier 1): 87%
   Source 3 (Tier 2): 85%
   Source 4 (Tier 3): 90%
   ```

4. **Analyze Patterns**
   - **Consensus:** Tier 1/2 sources agree (82-87%)
   - **Outlier:** Tier 3 source claims higher (90%)
   - **Trustworthy:** Average of Tier 1 sources ≈ 84.5%

5. **Make Decision**
   - ✅ VERIFIED: Claim falls within Tier 1 range
   - 📝 UPDATE: Use specific Tier 1 source citation
   - ❌ DISCARD: Outlier from unreliable source

### Handling Conflicts

**Scenario:** Sources disagree on numbers

**Example:**
- Source A (Tier 1): "65% of companies..."
- Source B (Tier 1): "78% of companies..."

**Resolution Strategy:**
1. Check if measuring same thing (different definitions?)
2. Check dates (one more recent?)
3. Check sample size/methodology (one more rigorous?)
4. Note the range: "Research shows between 65-78%..."
5. Cite most recent/authoritative

**When Sources Contradict:**
- ❌ Don't average them
- ✅ Choose most authoritative + recent
- ✅ Note the variation
- ✅ Or rephrase to acknowledge range

---

## Special Cases

### Case 1: No Results Found

**Query:** "obscure product feature statistics 2024"
**Results:** 0 relevant matches

**Actions:**
1. Try broader query
2. Remove year filter
3. Search for product directly
4. Search company documentation
5. If still nothing → ❌ UNSUPPORTED

### Case 2: Only Tier 3 Sources

**Query:** "specific claim statistics"
**Results:** All from unknown blogs

**Actions:**
1. Check if blogs cite original sources
2. If yes, trace to original
3. Run new query for original source
4. If no originals found → ❌ UNSUPPORTED

### Case 3: Outdated Data

**Query:** "AI adoption 2024"
**Results:** All from 2019-2021

**Actions:**
1. Try different query terms
2. Add "latest" or "recent"
3. Check if more recent data exists
4. If only old data → ⚠️ PARTIALLY VERIFIED (outdated)

### Case 4: Contradictory Results

**Scenario:** Sources strongly disagree

**Actions:**
1. Check publication dates
2. Compare methodologies
3. Assess sample sizes
4. Prioritize Tier 1 over Tier 2/3
5. Note conflict in report
6. Recommend rephrasing to acknowledge uncertainty

---

## Query Optimization Tips

### Too Many Results?
- Add specificity: "marketing automation" → "B2B marketing automation SMB"
- Add year filter: "statistics" → "statistics 2024"
- Add authority filter: "report" → "report Gartner Forrester"
- Add "official" or "documentation"

### Too Few Results?
- Broaden terms: "HubSpot sequence feature" → "HubSpot automation"
- Remove year: "2024" → remove it
- Remove qualifiers: "official documentation" → "documentation"
- Try synonyms: "adoption" → "usage" or "penetration"

### Wrong Results?
- Check spelling
- Rephrase query
- Break into smaller parts
- Try different angle

### Best Practices

✅ **DO:**
- Use specific, targeted queries
- Include year for current data
- Name specific research firms
- Use "official" for product claims
- Try 3-5 results for balance

❌ **DON'T:**
- Use vague general queries
- Include unnecessary words
- Trust first result blindly
- Skip authority evaluation
- Stop at one source

---

## Example Verification Workflow

### Claim to Verify
"85% of B2B marketers say AI has improved their productivity"

### Step 1: Construct Query
```
Query: "B2B marketing AI productivity statistics 2024"
NumResults: 5
```

### Step 2: Execute Search
```python
results = mcp__MCP_DOCKER__web_search_exa(
    query="B2B marketing AI productivity statistics 2024",
    numResults=5
)
```

### Step 3: Evaluate Results

**Result 1:**
- URL: forrester.com/report/b2b-ai-productivity-2024
- Authority: Tier 1 ✅
- Date: 2024-02-10 ✅
- Content: "Survey of 500 B2B marketers shows 82% report improved productivity"
- Match: Close (82% vs 85%)
- Original: Yes ✅

**Result 2:**
- URL: marketingprofs.com/article/b2b-ai-stats
- Authority: Tier 2 ✅
- Date: 2024-01-15 ✅
- Content: "According to recent studies, around 85% of B2B marketers..."
- Match: Exact BUT...
- Original: No - cites unnamed "studies"
- Action: Need to trace original

**Result 3:**
- URL: unknownblog.com/ai-marketing
- Authority: Tier 3 ❌
- Skip or use only to find originals

### Step 4: Cross-Reference
- Tier 1 source: 82%
- Claim states: 85%
- Difference: 3% (acceptable range)

### Step 5: Make Decision
✅ **VERIFIED** (with update)

Recommendation: Update to:
"According to Forrester's 2024 B2B Marketing Survey, 82% of B2B marketers report that AI has improved their productivity"

---

## Quick Reference

| Claim Type | Query Pattern | NumResults | Authority Focus |
|------------|---------------|------------|-----------------|
| Statistics | "[topic] statistics 2024" | 5 | Tier 1 required |
| Product | "[product] [feature] official" | 3 | Official docs |
| Trends | "[trend] report 2024 Gartner" | 5 | Research firms |
| Technical | "[concept] how it works docs" | 3 | Tech specs |
| Comparative | "[topic] comparison 2024" | 4 | Independent reviews |
| Temporal | "[event] [year]" | 2 | Press releases |
| Attribution | "[source] [topic] 2024" | 3 | Original source |

---

## Remember

1. **Be Specific:** Targeted queries get better results
2. **Check Authority:** Not all results are equal
3. **Verify Dates:** Current claims need current sources
4. **Trace Origins:** Secondary sources → find originals
5. **Cross-Reference:** Multiple sources strengthen verification
6. **Document Everything:** Query, results, evaluation, decision

**When in doubt:** Run additional searches with different query variations.
