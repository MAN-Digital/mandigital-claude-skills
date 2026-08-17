---
name: blog-post-fact-checker
description: Performs comprehensive fact-checking of blog post content using Exa.ai web search. Validates claims, statistics, sources, and assertions against authoritative web sources. Identifies unsupported claims, outdated information, and potential inaccuracies. Runs AFTER blog-post-creation and BEFORE editing-checklist. Outputs detailed fact-check report in Markdown format as both a saved file and artifact for easy review and potential return to blog-post-creation for corrections.
---

# Blog Post Fact Checker

## Purpose

This skill performs **pure fact-checking only** - verifying claims, statistics, and assertions in blog post content against authoritative web sources using Exa.ai MCP.

**What This Skill Does:**
✅ Extracts all factual claims from blog post content
✅ Verifies each claim using `mcp__MCP_DOCKER__web_search_exa`
✅ Evaluates source authority (Tier 1/2/3 classification)
✅ Generates comprehensive Markdown fact-check report
✅ Saves report to disk AND displays as artifact
✅ Provides clear PASS/FAIL decision for next steps

**What This Skill Does NOT Do:**
❌ No editing (that's editing-checklist)
❌ No SEO analysis (that's blog-post-seo-research)
❌ No content research (that's blog-post-content-research)
❌ No style improvements (that's editing-checklist)

**ONE JOB:** Verify factual accuracy using authoritative web sources

---

## Workflow Position

**CRITICAL PLACEMENT:**

```
1. blog-post-seo-research (DataForSEO keyword/SERP research)
2. blog-post-content-research (Content/competitor research)
3. blog-post-creation (Drafting)
4. → blog-post-fact-checker (THIS SKILL) ←
5. editing-checklist (Style/readability/optimization)
```

**Why This Order:**
- Must fact-check BEFORE editing to avoid wasting time editing incorrect content
- Results may require returning to blog-post-creation for corrections
- Fact-checking must PASS before proceeding to editing

---

## Required Inputs

### Input #1: Blog Post Content (MANDATORY)
- Full blog post in Markdown format
- Must include all body content (intro, sections, conclusion)
- Should include any existing source citations

**⚠️ IF MISSING:**
Ask user: "I need the complete blog post content in Markdown format to perform fact-checking. Please provide the draft."

**Optional Context:**
- Target keyword (helps with relevant search queries)
- Blog post title (helps with reporting)

---

## Fact-Checking Workflow (5 Phases)

### Phase 1: Content Parsing & Claim Extraction

**Step 1.1: Read and Parse Content**
- Read the complete blog post Markdown content
- Note the structure (intro, body sections, conclusion)
- Identify the main topic and angle

**Step 1.2: Extract All Factual Claims**

Identify all verifiable claims:

**Statistics:**
- Percentages (e.g., "85% of marketers...")
- Numbers with context (e.g., "$4.5 billion market size")
- Growth rates (e.g., "30% year-over-year increase")
- Adoption rates (e.g., "1 in 3 companies use...")
- ROI claims (e.g., "200% return on investment")

**Product Features/Capabilities:**
- "Tool X includes feature Y"
- "Platform supports integration with Z"
- "Native capability to do ABC"
- "Built-in functionality for..."

**Industry Trends:**
- "AI adoption is accelerating"
- "Market is shifting toward..."
- "Companies are increasingly..."

**Technical Accuracy:**
- How systems work
- Architecture descriptions
- Technical specifications
- Process flows

**Comparative Claims:**
- "X is better than Y"
- "Top 5 tools for..."
- "Leading solution for..."

**Temporal Claims:**
- Dates and timelines
- "In 2024..."
- "Since last year..."
- Historical events

**Attribution:**
- "According to [Source]..."
- "Expert X said..."
- Quoted statements

**Step 1.3: Extract Context**

For each claim, capture:
- The exact claim text
- 1-2 sentences before and after (context)
- Any existing source citation
- Location in document (intro/body/conclusion)

**Step 1.4: Initial Count**

Document:
- Total claims found: [X]
- By category breakdown
- Claims with existing citations vs uncited claims

---

### Phase 2: Claim Prioritization & Categorization

**Step 2.1: Assign Priority Levels**

**CRITICAL Priority:**
- Statistics about market size, revenue, growth
- ROI and business impact numbers
- Product pricing or performance claims
- Safety/security/compliance claims

**HIGH Priority:**
- Product capabilities and feature claims
- Integration availability
- Technical specifications
- Industry adoption statistics
- Competitive comparisons

**MEDIUM Priority:**
- General industry trends
- Market direction statements
- Predictions and forecasts
- Common best practices

**LOW Priority:**
- Subjective opinions (if attributed correctly)
- Common knowledge statements
- Obvious truths

**Step 2.2: Categorize by Type**

Label each claim:
- `[STAT]` - Statistic
- `[PRODUCT]` - Product Feature/Capability
- `[TREND]` - Industry Trend
- `[TECHNICAL]` - Technical Accuracy
- `[COMPARATIVE]` - Comparison
- `[TEMPORAL]` - Date/Timeline
- `[ATTRIBUTION]` - Quoted/Attributed

**Step 2.3: Create Verification Queue**

Order claims for verification:
1. All CRITICAL priority (regardless of type)
2. All HIGH priority
3. All MEDIUM priority
4. LOW priority (if time permits)

---

### Phase 3: Verification with Exa.ai (CORE TASK)

> **This is the most important phase - verify EVERY high-value claim**

For EACH claim in priority order:

**Step 3.1: Construct Targeted Exa Query**

Use `mcp__MCP_DOCKER__web_search_exa` with strategic queries:

**For Statistics:**
```
Query: "[statistic topic] statistics 2024 2025"
Example: "AI adoption marketing statistics 2024 2025"
numResults: 5
```

**For Product Features:**
```
Query: "[product name] [feature] documentation official"
Example: "HubSpot AI agents documentation official"
numResults: 3
```

**For Industry Trends:**
```
Query: "[trend topic] report 2024 Gartner Forrester"
Example: "martech consolidation report 2024 Gartner Forrester"
numResults: 5
```

**For Technical Accuracy:**
```
Query: "[technical concept] how it works documentation"
Example: "OAuth 2.0 how it works documentation"
numResults: 3
```

**Query Best Practices:**
- Include year ("2024" or "2025") for current data
- Add authority sources ("Gartner", "Forrester", "McKinsey") for statistics
- Use "official" or "documentation" for product claims
- Use "research" or "study" for academic topics

**Step 3.2: Execute Search and Review Results**

```python
results = mcp__MCP_DOCKER__web_search_exa(
    query="[constructed query]",
    numResults=3-5  # Balance thoroughness vs speed
)
```

For EACH result returned:

1. **Check Domain Authority**
   - Is this Tier 1, 2, or 3? (see `references/source-authority-hierarchy.md`)
   - Tier 1: Gartner, Forrester, HubSpot Research, HBR, WSJ, Forbes
   - Tier 2: Industry publications, known SaaS blogs (in their domain)
   - Tier 3: Unknown blogs, content farms (AVOID)

2. **Read Content for Verification**
   - Does the content support the claim?
   - Is it the ORIGINAL source or citing someone else?
   - What's the publication date?

3. **Note Key Information**
   - Supporting quote/excerpt
   - URL and domain
   - Authority tier
   - Publication date
   - Whether it's original or secondary source

**Step 3.3: Cross-Reference Multiple Sources**

For each claim, evaluate:
- How many authoritative sources (Tier 1/2) confirm this?
- Do sources agree or contradict?
- Is there a clear original/primary source?
- Are sources current (2024-2025)?

**Verification Thresholds:**
- ✅ **VERIFIED**: 2+ Tier 1/2 sources confirm, current data (2024-2025)
- ⚠️ **PARTIALLY VERIFIED**: 1 Tier 1/2 source confirms OR data is dated (2023 or earlier)
- ❌ **UNSUPPORTED**: No Tier 1/2 sources found OR contradicted by authoritative sources
- 🔍 **NEEDS ORIGINAL SOURCE**: Found in secondary/Tier 3 source, need to trace to primary

**Step 3.4: Trace to Original Sources**

If claim appears in secondary source:
```
Found in: unknownblog.com
Article says: "According to Gartner Research..."
→ Run new Exa query: "Gartner [specific claim topic] 2024"
→ Find and cite the ORIGINAL Gartner source
```

**Always prefer original sources:**
- Research firm reports (not blog posts about them)
- Company announcements (not news articles about them)
- Academic papers (not articles citing them)

**Step 3.5: Document Verification**

For each claim, document:
- Exa query used
- Results found (URLs, domains, authority tiers)
- Supporting quotes/excerpts
- Verification status (✅ ⚠️ ❌ 🔍)
- Publication dates
- Any conflicts or issues
- Recommendation (keep/update/correct/remove)

---

### Phase 4: Analysis & Confidence Scoring

**Step 4.1: Score Each Verified Claim**

**Confidence Level:**

**HIGH Confidence:**
- 3+ Tier 1 sources confirm
- Original sources cited
- Data from 2024-2025
- No conflicts found

**MEDIUM Confidence:**
- 1-2 Tier 1/2 sources confirm
- Data from 2023-2024
- Minor discrepancies between sources

**LOW Confidence:**
- Only Tier 2/3 sources found
- Data from pre-2023
- Significant conflicts
- Unable to verify independently

**Step 4.2: Identify Patterns**

Look for:
- Multiple claims from same unverified source
- Repeated use of outdated statistics
- Product claims unsupported by official docs
- Industry trends without research backing

**Step 4.3: Prioritize Issues**

Categorize problems:

**MUST FIX (Critical):**
- Unsupported statistics (❌ CRITICAL priority claims)
- Incorrect product capabilities
- Factual errors contradicted by sources
- Dated statistics presented as current

**SHOULD FIX (High Priority):**
- Partially verified claims needing better sources
- Claims needing original source attribution
- Outdated statistics that should be updated

**CONSIDER FIXING (Medium Priority):**
- Low confidence claims with weak sources
- Unverified trend statements
- Missing source citations

---

### Phase 5: Report Generation (MANDATORY OUTPUTS)

> **Critical: Create BOTH outputs**

**Step 5.1: Generate Markdown Report**

Use the template from `guidelines/output-format-template.md`:

**Report Structure:**
1. **Header**: Title, date, summary statistics
2. **Executive Summary**: 2-3 sentences on overall results
3. **Decision**: PASS / MINOR ISSUES / FAIL
4. **Critical Issues**: List any must-fix items
5. **Detailed Verification Results**: Every claim with full verification
6. **Summary Statistics**: Counts and percentages
7. **Source Authority Breakdown**: Tier 1/2/3 usage
8. **Recommendations**: Must fix / Should fix / Consider fixing
9. **Next Steps**: Clear direction on what to do next
10. **Methodology**: Tools and approach used

**Step 5.2: Save to Disk**

```python
filename = f"fact-check-report-{keyword.replace(' ', '-')}-{date}.md"
# Save to working directory
```

Example: `fact-check-report-hubspot-ai-agents-2025-01-26.md`

**Step 5.3: Display as Artifact**

**CRITICAL: Use artifact feature to display the report**

The report must be presented as an artifact in the conversation so:
- User can review without conversation clutter
- Report is easy to download/save
- User can reference while deciding next steps

**Step 5.4: Provide Clear Decision**

End with explicit decision:

```markdown
## DECISION

✅ **PASS** - Ready to proceed to editing-checklist
- All critical and high-priority claims verified
- Minor issues can be addressed during editing
- No factual accuracy concerns

⚠️ **MINOR ISSUES** - Review before proceeding
- [X] medium-priority claims need attention
- Decision: Fix now OR address during editing
- No critical factual errors found

❌ **FAIL** - Return to blog-post-creation
- [X] critical claims unsupported or incorrect
- [Y] high-priority issues require correction
- Must fix before editing can begin
```

**Step 5.5: Hand Off**

If PASS: "This fact-check report shows all critical facts are verified. You can now proceed to the editing-checklist skill."

If MINOR ISSUES: "This fact-check report identifies [X] issues. You can either address them now or proceed to editing. What would you like to do?"

If FAIL: "This fact-check report identifies critical factual issues. The content should be returned to blog-post-creation for corrections. Here's the report detailing what needs to be fixed."

---

## Quality Checklist

Before marking fact-checking complete:

**Claim Extraction:**
- [ ] All statistics extracted and verified
- [ ] All product claims identified
- [ ] All industry trends captured
- [ ] All technical statements checked
- [ ] All comparative claims evaluated

**Verification Completeness:**
- [ ] ALL CRITICAL priority claims verified
- [ ] ALL HIGH priority claims verified
- [ ] MEDIUM priority claims checked (if time permits)
- [ ] Each claim has Exa query documented
- [ ] Each claim has sources listed
- [ ] Source authority tier assigned (1/2/3)

**Source Quality:**
- [ ] Tier 1 sources preferred for critical claims
- [ ] Secondary sources traced to originals
- [ ] Publication dates noted (2024-2025 preferred)
- [ ] No Tier 3 sources used without disclaimer
- [ ] Original authoritative sources cited

**Report Outputs:**
- [ ] Markdown report generated with all sections
- [ ] Report saved to disk with proper filename
- [ ] Report displayed as artifact in conversation
- [ ] Clear PASS/FAIL/MINOR ISSUES decision provided
- [ ] Actionable recommendations included
- [ ] Next steps clearly stated

**Decision Quality:**
- [ ] Decision aligns with verification results
- [ ] Critical issues correctly identified
- [ ] User has clear path forward
- [ ] Report is ready to send to blog-post-creation (if FAIL)

---

## Common Mistakes to Avoid

### Research Phase Mistakes:
1. **Incomplete extraction** - Missing claims embedded in prose
2. **Skipping context** - Not capturing surrounding sentences
3. **Ignoring product claims** - Only checking statistics
4. **Not categorizing** - Treating all claims the same priority

### Verification Mistakes:
5. **Insufficient searches** - Only 1 Exa query per claim
6. **Accepting Tier 3 sources** - Using unknown blogs as evidence
7. **Not cross-referencing** - Trusting single source
8. **Skipping date checks** - Using outdated statistics as current
9. **Not tracing origins** - Citing secondary sources instead of originals

### Exa.ai Usage Mistakes:
10. **Vague queries** - Not specific enough to find verification
11. **Too few results** - Setting numResults=1 or 2
12. **Wrong query type** - Using product query for statistics
13. **No year filter** - Not including "2024" or "2025" in queries

### Source Evaluation Mistakes:
14. **Authority confusion** - Treating Tier 2/3 as Tier 1
15. **Missing conflicts** - Not noting contradictory information
16. **Secondary citation** - Citing "Blog X says Gartner said..." instead of Gartner
17. **Date blindness** - Not checking when source was published

### Report Mistakes:
18. **Missing sections** - Incomplete report template
19. **No artifact** - Only saving file, not displaying as artifact
20. **Unclear decision** - Ambiguous PASS/FAIL determination
21. **No filename** - Not saving report with proper naming
22. **Missing recommendations** - Verification without correction guidance

### Workflow Mistakes:
23. **Editing while fact-checking** - This skill does NOT edit
24. **SEO analysis** - This skill does NOT check SEO
25. **Premature pass** - Moving to editing with critical issues
26. **Not returning to creator** - Proceeding despite FAIL status

---

## Resources

This skill includes comprehensive supporting materials:

### Scripts

**`scripts/fact_check_analyzer.py`**
Python script for automated claim analysis:
- Parses markdown content
- Extracts factual claims by category
- Generates Exa queries
- Evaluates source authority
- Scores verification confidence
- Formats Markdown reports

**Usage:**
```bash
python3 scripts/fact_check_analyzer.py draft.md "target keyword"
```

**`scripts/claim_extractor.py`**
Utility functions for claim identification:
- Identifies statistics, product claims, trends
- Extracts context around claims
- Categorizes by type and priority
- Flags existing citations for validation

**Usage:**
```python
from scripts.claim_extractor import extract_claims, categorize_claim
claims = extract_claims(markdown_content)
```

### References

**`references/fact-checking-framework.md`**
Comprehensive verification methodology:
- Claim verification hierarchy
- Statistical validation rules
- Product claim verification process
- Industry trend validation
- Technical accuracy checking
- Date/recency requirements

**`references/exa-verification-guide.md`**
Exa.ai-specific instructions:
- Query construction strategies
- Interpreting search results
- Source evaluation from URLs
- Cross-referencing techniques
- Handling conflicting information

**`references/claim-categories-reference.md`**
Detailed claim type guide:
- Statistics (with examples)
- Product Features (with examples)
- Industry Trends (with examples)
- Technical Accuracy (with examples)
- Comparative Claims (with examples)
- Temporal Claims (with examples)
- How to verify each type

**`references/source-authority-hierarchy.md`**
Authority ranking system:
- Tier 1 sources (ALWAYS ACCEPTABLE)
- Tier 2 sources (ACCEPTABLE)
- Tier 3 sources (AVOID)
- How to trace to original sources
- Domain authority indicators

### Examples

**`examples/complete-fact-check-example.md`**
Full end-to-end walkthrough:
- Sample blog post (500 words, 12 claims)
- Complete claim extraction
- Exa.ai queries for each claim
- Source evaluation process
- Verification decisions with reasoning
- Final Markdown report output
- Decision: PASS/FAIL determination

**`examples/claim-type-examples.md`**
Specific verification examples:
- Statistical claim with Exa queries
- Product feature verification
- Industry trend validation
- Technical accuracy check
- Handling conflicting sources
- Outdated information handling

### Guidelines

**`guidelines/output-format-template.md`**
Exact Markdown format specification:
- Complete report template
- Section-by-section requirements
- Verification status indicators
- Source citation format
- Decision recommendation format

---

## Quick Start

**First time using this skill?**

1. Read `references/fact-checking-framework.md` for methodology
2. Review `references/source-authority-hierarchy.md` for Tier 1/2/3 sources
3. Check `examples/complete-fact-check-example.md` for full workflow
4. Reference `guidelines/output-format-template.md` for report format
5. Start fact-checking with CRITICAL priority claims first

**For experienced users:**

1. Extract all claims from blog post
2. Prioritize: CRITICAL → HIGH → MEDIUM → LOW
3. For each claim, run `mcp__MCP_DOCKER__web_search_exa`
4. Evaluate sources (Tier 1/2/3), prefer Tier 1
5. Document verification status (✅ ⚠️ ❌ 🔍)
6. Generate report (save file + display as artifact)
7. Make decision: PASS / MINOR ISSUES / FAIL

---

## Output Deliverable

**File:** `fact-check-report-[keyword]-[date].md`

**Artifact:** Same content displayed in conversation

**Contains:**
- Executive summary with decision
- Critical issues (if any)
- Detailed verification for every claim
- Exa queries used
- Sources found with authority tiers
- Verification status and confidence
- Recommendations for corrections
- Summary statistics
- Next steps

**To Be Used:**
- By USER to review fact-check results
- By blog-post-creation skill (if FAIL - needs corrections)
- By editing-checklist skill (if PASS - reference for context)

**Decision Point:**
- ✅ PASS → Proceed to editing-checklist
- ⚠️ MINOR ISSUES → User decides: fix now or during editing
- ❌ FAIL → Return to blog-post-creation with report
