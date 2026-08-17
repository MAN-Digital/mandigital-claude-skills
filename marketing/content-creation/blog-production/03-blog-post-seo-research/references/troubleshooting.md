# Troubleshooting Guide

Common issues when running DataForSEO pre-research and how to fix them.

---

## Issue 1: Tool Execution Fails

### Symptom
```
Error: Failed to execute mcp__dataforseo__labs_search_intent
Connection refused / Timeout
```

### Possible Causes
1. MCP connection not active
2. DataForSEO API key not configured
3. API rate limit exceeded
4. Network connectivity issue

### Solutions

**Check 1: Verify MCP Connection**
```
Is the MCP_DOCKER server running?
Check: MCP server status in Claude Code
```

**Check 2: Verify API Key**
```
Is DATAFORSEO_API_KEY configured in MCP environment?
Location: MCP configuration file
```

**Check 3: Rate Limiting**
```
Wait 1 minute and retry
DataForSEO has rate limits per minute
```

**Check 4: Retry with Correct Parameters**
```json
// Ensure proper format:
{
  "keyword": "your keyword",  // NOT "keywords": [...]
  "location_name": "United States",
  "language_code": "en"
}
```

---

## Issue 2: No Results Returned

### Symptom
```
Tool executed successfully but returned empty results
items: []
```

### Possible Causes
1. Keyword has no search volume
2. Wrong location/language combination
3. Typo in keyword
4. Keyword too specific/niche

### Solutions

**Solution 1: Verify Keyword Has Volume**
```
Try a broader keyword variation:
- Instead of: "hubspot prospecting agent 2025 tutorial"
- Try: "hubspot prospecting agent"
```

**Solution 2: Check Location/Language**
```
Ensure language is supported in that location:
- ✅ "en" + "United States" → Works
- ❌ "ja" + "United States" → Might fail
- ✅ "ja" + "Japan" → Works
```

**Solution 3: Test with Known Keyword**
```
Test with high-volume keyword to verify connection:
"crm software" → Should return results
```

**Solution 4: Use Keyword Ideas Tool First**
```
If no volume, generate alternatives:
mcp__dataforseo__labs_google_keyword_ideas
```

---

## Issue 3: SERP Results Different from Brief

### Symptom
```
Pre-research SERP URLs don't match competitor URLs in brief
```

### This is EXPECTED and CORRECT

### Why This Happens
- Rankings change daily
- Brief URLs may be from days/weeks ago
- New content has entered SERP
- Algorithm updates shifted rankings

### What to Do
✅ **USE THE FRESH SERP URLS** from pre-research
❌ **DO NOT use brief URLs** if they differ

**Reasoning:**
- Pre-research shows WHO ACTUALLY RANKS TODAY
- Brief URLs are historical data
- Fresh SERP = accurate competitor landscape

---

## Issue 4: Informational Intent Too Low

### Symptom
```
Search intent results:
- Informational: 35%
- Transactional: 55%
- Blog post format appropriate: NO
```

### This Means
The keyword is transactional (purchase intent), not informational (learning intent)

### Solutions

**Option 1: Adjust Keyword**
```
Instead of: "buy crm software"
Try: "what is crm software"
Or: "crm software guide"
Or: "how to choose crm"
```

**Option 2: Change Content Format**
```
If keyword is truly transactional:
- Don't write blog post
- Write product comparison page instead
- Write case study with strong CTA
```

**Option 3: Confirm with User**
```
"The keyword has 55% transactional intent. This suggests
a product page or comparison would perform better than
a blog post. Should we adjust the keyword or content format?"
```

---

## Issue 5: Keyword Difficulty Too High

### Symptom
```
Keyword difficulty: 85
Competitor domain ranks: 50, 75, 120 (very high authority)
```

### This Means
Very difficult to rank - dominated by high-authority sites

### Solutions

**Solution 1: Find Long-Tail Variation**
```
Instead of: "crm software" (difficulty: 85)
Try: "crm software for small business" (difficulty: 45)
Or: "best crm for startups" (difficulty: 40)
```

**Solution 2: Focus on Differentiation**
```
Can't beat on authority → Beat on content quality:
- More comprehensive coverage
- Better examples/case studies
- Implementation guides (not just theory)
- RevOps/consultancy angle
```

**Solution 3: Target Featured Snippet**
```
Even if can't rank #1-3, can capture position 0:
- Answer questions directly
- Use structured data
- Clear, concise format
```

---

## Issue 6: Related Keywords Too Generic

### Symptom
```
Related keywords are too broad:
- "software"
- "business"
- "tools"
```

### Possible Causes
1. Seed keyword too broad
2. Depth parameter too low
3. Not enough context

### Solutions

**Solution 1: Use More Specific Seed**
```
Instead of: "agent"
Use: "hubspot prospecting agent"
```

**Solution 2: Increase Depth**
```json
{
  "keyword": "hubspot prospecting agent",
  "depth": 50  // Get more keywords
}
```

**Solution 3: Filter Results**
```
Manually filter related keywords:
- Keep only those relevant to topic
- Discard generic terms
- Focus on keywords containing core terms
```

---

## Issue 7: Tool Parameters Rejected

### Symptom
```
Error: Invalid parameter 'keywords'
```

### Cause
Wrong parameter name for the tool

### Solution
Check tool-specific parameter names:

**search_intent:**
```json
{"keyword": "...", ...}  // Singular
```

**keyword_overview:**
```json
{"keywords": ["..."], ...}  // Plural, array
```

**serp_organic_live_advanced:**
```json
{"keyword": "...", ...}  // Singular
```

**domain_rank_overview:**
```json
{"target": "domain.com", ...}  // 'target' not 'domain'
```

**related_keywords:**
```json
{"keyword": "...", ...}  // Singular
```

---

## Issue 8: Output Format Inconsistent

### Symptom
```
Each run produces slightly different output format
```

### Solution
Use the **format_output.py** script in `/scripts`:

```bash
python3 scripts/format_output.py
```

This ensures consistent, structured output every time.

---

## Issue 9: Domain Authority Shows 0

### Symptom
```
Domain rank: 0
Organic keywords: 0
```

### Possible Causes
1. New domain (not yet indexed)
2. Domain doesn't exist
3. Typo in domain name
4. Very low authority (below tracking threshold)

### Solutions

**Solution 1: Verify Domain Exists**
```
Check domain in browser:
https://www.example.com
```

**Solution 2: Try Without www**
```
Instead of: "www.example.com"
Try: "example.com"
```

**Solution 3: Check for Typos**
```
Ensure exact domain from SERP results:
- hubspot.com ✅
- hubbspot.com ❌
```

---

## Issue 10: Results Cached (Outdated)

### Symptom
```
Running pre-research twice gives same results,
even though we know rankings changed
```

### Cause
DataForSEO may cache some results for performance

### Solution

**For Fresh Data:**
```
Wait 24 hours between runs for same keyword
OR
Use different parameter variations to bypass cache:
- Add device: "desktop" vs "mobile"
- Slightly different keyword phrasing
```

**Best Practice:**
```
Only run pre-research once per keyword per project
Re-run only if > 30 days old
```

---

## Issue 11: Too Many Errors in Sequence

### Symptom
```
Tool 1: Success
Tool 2: Error
Tool 3: Error
Tool 4: Error
Tool 5: Error
```

### Likely Cause
API key issue or connectivity problem after first tool

### Solution

**Stop and Diagnose:**
```
Don't continue forcing through errors
Pause and check:
1. API key still valid?
2. Network connection stable?
3. Rate limit hit?
```

**Then Retry:**
```
Wait 2-3 minutes
Retry ALL 5 tools from beginning
Don't patch together partial results
```

---

## Quick Troubleshooting Checklist

Before running pre-research, verify:

- [ ] MCP_DOCKER server is running
- [ ] DataForSEO API key configured
- [ ] Keyword has search volume (test with Google)
- [ ] Location/language combination valid
- [ ] Correct tool parameter names used
- [ ] Not hitting rate limits (wait if retry needed)

If errors occur:

- [ ] Check error message for specific issue
- [ ] Verify parameters match tool requirements
- [ ] Test with known working keyword
- [ ] Wait and retry (rate limiting)
- [ ] Check API key hasn't expired

---

## Getting Help

If issues persist after troubleshooting:

1. **Check DataForSEO Status:**
   - https://status.dataforseo.com/

2. **Review API Docs:**
   - https://docs.dataforseo.com/v3/

3. **Test with cURL:**
   ```bash
   curl -X POST https://api.dataforseo.com/v3/dataforseo_labs/google/search_intent/live \
   -H "Content-Type: application/json" \
   -d '{...}'
   ```

4. **Contact Support:**
   - If API key issues: DataForSEO support
   - If MCP issues: Check MCP_DOCKER documentation
