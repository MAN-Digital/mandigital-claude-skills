---
name: blog-post-creation
description: "Creates SEO-optimized blog posts for MAN Digital RevOps consultancy from research inputs. RECEIVES brief, SEO research, content research with Architecture, Workflow, ERD. DIGESTION PHASE - reviews architecture (relationship clarity), workflow (process understanding), ERD (entity mapping), brand positioning, guidelines before drafting. Uses architecture to prevent entity conflation, workflow for accurate processes, ERD to prevent stat mismatches. NO third-party case studies (not tool vendors' marketing). Follows brief structure exactly. Creates draft at target word count with variety (1-3 sentence paragraphs), extensive bullets (8-12 sections), visuals (2-4). Applies 11-step editing framework. Outputs publication-ready markdown with SEO title, meta description. Max 3 external links (Tier 1/2 sources), min 2 internal links, one domain once, statistics with bridges, specific hooks."
---

# MAN Digital Blog Post Creation Skill

## Purpose

This skill creates publication-ready blog posts for MAN Digital's RevOps consultancy based on provided research inputs. It does NOT perform research—it RECEIVES research and transforms it into a polished blog post.

**What This Skill Does:**
✅ Receives and digests all inputs (brief, SEO research, content research + architecture + workflow + ERD)
✅ Reviews brand positioning and guidelines
✅ Uses architecture documentation to represent relationships accurately
✅ Uses workflow diagrams to explain processes correctly
✅ Uses ERD to prevent entity/statistic mismatches
✅ Creates draft following brief structure exactly
✅ Applies 11-step editing framework
✅ Performs final word-by-word polish
✅ Outputs publication-ready markdown

**What This Skill Does NOT Do:**
❌ SEO pre-research (use `blog-post-seo-research` skill)
❌ Content research (use `blog-post-content-research` skill)
❌ Create briefs from scratch (brief must be provided)

---

## 🆕 Critical Success Requirements

1. **BRIEF IS SACRED** - The brief structure, headings, and requirements are non-negotiable. Everything revolves around the brief.

2. **DIGESTION PHASE MANDATORY** - Before drafting, MUST review and organize ALL inputs: brief, SEO research file, content research file with architecture + workflow + ERD, brand guidelines, positioning.

3. **ARCHITECTURE UNDERSTANDING** - Use architecture documentation to understand and accurately represent relationships between entities/concepts. Prevent conflation of "part of" vs "works with" vs "triggered by."

4. **WORKFLOW UNDERSTANDING** - Use workflow diagrams to understand and accurately explain processes, sequences, decision points, and triggers.

5. **ENTITY UNDERSTANDING FROM ERD** - Use the Entity Relationship Diagram from content research to prevent stat mismatches.

6. **STATISTICS MUST BRIDGE TO CONTEXT** - Never drop stats without transitions. Stats must match correct entity.

7. **NO THIRD-PARTY CASE STUDIES** - NEVER write about other companies' success stories. MAN Digital is NOT a tool vendor's marketing team. We don't say "Company X saved Y hours with Tool Z." Use industry statistics, research data, and general capabilities - NOT other companies' case studies.

8. **STRICT LINKING LIMITS**:
   - Maximum 3 outbound/external links (Tier 1/2 sources only)
   - Minimum 2 internal links to man.digital
   - One domain used once only
   - Trace to original authoritative source

9. **NATURAL FORMATTING** - Vary spacing, no uniform line breaks after every heading (AI detection avoidance)

10. **FLEXIBLE WORD COUNT** - Default 1,200-1,600 words, OR user-specified word count

11. **COMPREHENSIVE EDITING** - All 11 frameworks + final word-by-word polish (MANDATORY)

---

## Required Inputs (ALL MANDATORY)

### Input #1: The Brief
**Format:** Written document or brief-template.md filled out
**Contains:** Topic, angle, target keyword, audience, content structure, headings, requirements

**⚠️ BRIEF IS SACRED:** Guard it like your only child. The brief IS the law.

### Input #2: SEO Research File
**Format:** `seo-research-[keyword]-[date].md` (from blog-post-seo-research skill)
**Contains:** Primary keyword, search intent, SERP competitors, related keywords (H2/H3 opportunities), keyword metrics, SEO strategy

### Input #3: Content Research File with Architecture, Workflow & ERD
**Format:** `content-research-[keyword]-[date].md` (from blog-post-content-research skill)
**Contains:**
- Statistics with validated authoritative sources
- **Architecture Documentation** - Relationship mapping, boundary clarity, common misconceptions (CRITICAL for accurate representation)
- **Workflow Diagram (Mermaid)** - Process visualization, decision points, triggers, flows
- **Entity Relationship Diagram (Mermaid ERD)** - Entity mapping (CRITICAL for preventing entity mismatches)
- Entity-statistic mapping
- Competitor content analysis
- Content gaps and opportunities
- Universal topics to cover
- Recommendations

**⚠️ IF ANY INPUT IS MISSING:**
Ask user: "I need ALL three inputs to proceed:
1. The brief
2. SEO research file (from blog-post-seo-research skill)
3. Content research file with ERD (from blog-post-content-research skill)
Please provide all missing inputs."

---

## Phase 0: Input Reception & Validation

**Step 0.1: Confirm All Inputs Received**

Document what you have:
```
✅ Brief received: [brief name/topic]
✅ SEO Research file: seo-research-[keyword]-[date].md
   → Primary keyword: [keyword]
   → Search volume: [volume]
   → Related keywords: [H2/H3 counts]
✅ Content Research file: content-research-[keyword]-[date].md
   → Statistics count: [X statistics validated]
   → Architecture documentation: YES
   → Workflow diagram: YES
   → ERD present: YES
   → Entity mapping: [X entities mapped]
✅ Ready to proceed to Digestion Phase
```

**Step 0.2: Quick Input Validation**

- [ ] Brief contains topic, keyword, structure requirements
- [ ] SEO research file contains primary keyword, SERP URLs, related keywords
- [ ] Content research file contains statistics, architecture documentation, workflow diagram, ERD diagram, entity mapping
- [ ] All files are current (2024-2025 dates)

**If validation fails:** Request missing information before proceeding.

---

## Phase 1: DIGESTION & ORGANIZATION (MANDATORY - BEFORE DRAFTING)

**⚠️ CRITICAL: This phase is NON-NEGOTIABLE. You MUST digest and organize ALL inputs before creating any draft.**

**Purpose:** Review and organize all provided research, guidelines, and brand context to create a comprehensive mental model before writing a single word.

### Step 1.1: Brief Deep Dive

> **📋 Reference: `brief-template.md` for expected brief format**

**Read the entire brief thoroughly:**
- [ ] Topic and angle understood
- [ ] Target keyword identified
- [ ] Content structure documented (H2s, sections)
- [ ] Word count target noted (or use default 1,200-1,600)
- [ ] Special requirements noted
- [ ] Target audience confirmed

**Document Brief Summary:**
```
BRIEF SUMMARY:
Topic: [main topic]
Primary Keyword: [keyword from brief]
Target Audience: [who this is for]
Word Count Target: [X,XXX words or default 1,200-1,600]
Required H2 Sections: [list from brief]
Special Requirements: [any unique requirements]
Content Angle: [perspective/approach]
```

### Step 1.2: Brand Positioning Review

> **🏢 MANDATORY: Read `guidelines/MAN-DIGITAL-BRAND-CONTEXT.md` before proceeding**

**Review and confirm brand alignment:**

**Client Profile:**
- [ ] Does this topic speak to mid-to-large B2B firms with HubSpot?
- [ ] Which buyer persona: Marketing Leader, CRO, Sales Leader, CS Ops, CEO?

**Pain Points:**
- [ ] Which client pain points does this address? (disconnected systems, no trusted forecasts, value erosion, etc.)

**Service Connection:**
- [ ] Which MAN Digital service(s) does this relate to?
- [ ] How does this show our unique approach?

**Positioning:**
- [ ] Clearly positions us as RevOps consultancy (not HubSpot feature seller)?
- [ ] HubSpot positioned as enabler (not hero)?

**Document Brand Angle:**
```
BRAND POSITIONING:
Target Decision Maker: [persona]
Pain Point Addressed: [specific pain]
Service Connection: [MAN Digital service]
Differentiator: [our unique approach]
RevOps Angle: [how we position this]
Process-First Element: [how we show process before tools]
```

### Step 1.3: SEO Research Digestion

**Read the SEO research file thoroughly:**

**Extract Key SEO Data:**
```
SEO RESEARCH SUMMARY:
Primary Keyword: [keyword]
Search Volume: [volume/month]
Keyword Difficulty: [score]
Search Intent: [% informational]
Target Word Count: [from SEO strategy]
Target H2 Count: [from SEO strategy]
Target H3 Count: [from SEO strategy]

H2 Keyword Opportunities (High-Volume):
1. [keyword 1] - [volume]
2. [keyword 2] - [volume]
3. [keyword 3] - [volume]
[Continue for all H2 keywords]

H3 Keyword Opportunities (Medium-Volume):
1. [keyword 1] - [volume]
2. [keyword 2] - [volume]
[Continue for all H3 keywords]

LSI Keywords (Natural Integration):
- [keyword 1, keyword 2, keyword 3...]

Top SERP Competitors (for reference):
1. [URL 1] - Position 1
2. [URL 2] - Position 2
3. [URL 3] - Position 3

SEO Strategy Notes:
[Key findings from SEO research file]
```

### Step 1.4: Content Research Digestion

**Read the content research file thoroughly:**

**Extract Statistics Inventory:**
```
STATISTICS INVENTORY (Authority-Validated):

Statistic 1:
- Text: "[full statistic]"
- Source: [authoritative source]
- Authority: Tier 1 / Tier 2
- Date: [year]
- Entity: [which entity this describes]
- Usage Context: [when/how to use]

Statistic 2:
[Repeat for all statistics]

Domain Usage Tracking:
- domain1.com ✓ (used once)
- domain2.com ✓ (used once)
- domain3.com ✓ (used once)
```

**Extract Content Guidance:**
```
CONTENT STRATEGY:

Universal Topics (Must Include):
1. [topic A] - ALL competitors cover
2. [topic B] - ALL competitors cover
3. [topic C] - ALL competitors cover

Content Gaps (Differentiation):
1. [gap 1] - Opportunity to stand out
2. [gap 2] - Missing from all competitors
3. [gap 3] - Outdated across competitors

Key Insights:
- [insight 1 from content research]
- [insight 2 from content research]
- [insight 3 from content research]
```

### Step 1.5: Architecture Documentation Study (CRITICAL)

> **⚠️ CRITICAL: This prevents entity conflation and relationship misunderstandings**

**Review the Architecture Documentation from content research file:**

The architecture section clarifies **how entities relate to each other** and prevents common misconceptions like:
- Confusing "part of" with "works with" or "triggered by"
- Attributing characteristics to the wrong entity
- Conflating separate concepts that merely relate

**Document Architecture Understanding:**
```
ARCHITECTURE MAP:

Primary Entity/Concept: [Name]
- Essential Nature: [what this fundamentally IS]
- Intrinsic Characteristics: [what inherently belongs to it]

Connected Entities:
- [Entity A] → [relationship type] → [Entity B]
  Example: "Buying Intent Signal" → triggers → "Prospecting Agent"
- [Entity C] → [relationship type] → [Entity D]
  Example: "CRO" → oversees → "VP Sales, VP Marketing, VP CS"

Conditional Relationships:
- IF [condition], THEN [entity A] relates to [entity B] as: [description]
- WHEN [situation], [these entities] interact as: [description]

Directional Flows:
- [Entity] provides/delivers → [value/resource] → to [Entity]
- [Entity] receives/depends on ← [value/resource] ← from [Entity]

COMMON MISCONCEPTIONS (AVOID THESE):
❌ WRONG: [misconception identified in research]
✅ CORRECT: [accurate understanding]

❌ WRONG: [another misconception]
✅ CORRECT: [correction]
```

**How to use this when writing:**
- When mentioning entities, ensure you represent relationships accurately
- Don't say "X includes Y" if Y actually triggers X or works with X
- Check the misconceptions list before writing about relationships
- Ensure boundaries between entities are clear in your explanations

### Step 1.6: Workflow Diagram Study (CRITICAL)

> **⚠️ CRITICAL: This ensures you explain processes, sequences, and triggers correctly**

**Review the Workflow Diagram from content research file:**

The workflow diagram shows **how things happen over time** - sequences, decision points, triggers, and flows.

**Document Workflow Understanding:**
```
WORKFLOW MAP:

Workflow Name: [Name of process/workflow]

Purpose: [What this workflow accomplishes]

Entry Points (How it starts):
- [Trigger/start point 1]
- [Trigger/start point 2]
- [Trigger/start point 3]

Key Stages/Steps (In sequence):
1. [Stage 1] → [what happens]
2. [Stage 2] → [what happens]
3. [Stage 3] → [what happens]
4. [Stage 4] → [what happens]

Decision Points (Conditional logic):
- At [Stage X]: IF [condition] → Path A: [outcome]
                ELSE → Path B: [outcome]
- At [Stage Y]: IF [condition] → Path A: [outcome]
                ELSE → Path B: [outcome]

Integration Points (Where systems connect):
- At [Stage X]: Connects with [external system/entity]
- At [Stage Y]: Data exchange with [entity]

Outcomes (Possible endings):
- ✅ [Success outcome]
- ⚠️ [Alternative outcome]
- ❌ [Exception/error outcome]
```

**How to use this when writing:**
- When explaining processes, follow the actual sequence shown in the diagram
- Mention decision points where relevant (shows depth of understanding)
- Don't skip steps or oversimplify complex workflows
- Ensure you represent triggers and initiators accurately
- Show understanding of "what leads to what"

### Step 1.7: Entity Relationship Diagram Study (CRITICAL)

> **⚠️ This is the MOST IMPORTANT part of digestion - prevents entity mismatches**

**Review the Mermaid ERD from content research file:**

**Document Entity Understanding:**
```
ENTITY MAP:

Entity 1: [Name]
- Description: [what this entity is]
- Role: [what it does]
- Statistics that apply: [list statistics that describe THIS entity]
- Statistics that DON'T apply: [mismatches to avoid]

Entity 2: [Name]
- Description: [what this entity is]
- Role: [what it does]
- Statistics that apply: [list]
- Statistics that DON'T apply: [list]

[Continue for ALL entities in ERD]

ENTITY RELATIONSHIPS:
- [Entity A] creates [Entity B]
- [Entity C] uses [Entity D]
- [Entity E] affects [Entity F]

CRITICAL MISMATCH RISKS:
⚠️ RISK 1: [statistic X] describes [Entity A], NOT [Entity B] - don't confuse
⚠️ RISK 2: [statistic Y] describes [Entity C behavior], NOT [Entity D behavior]
[Continue for all identified risks]
```

**Visualize the ERD mentally:** Understand how all entities relate before writing.

### Step 1.8: Guidelines Review

> **📚 Review ALL guideline files before drafting**

**Read and internalize:**
- `guidelines/Writing_guidelines.md` - Writing style and voice
- `guidelines/SEO_guidelines.md` - SEO title and meta description patterns
- `guidelines/positioning_hubspot_revops.json` - Positioning data
- `guidelines/MAN-DIGITAL-BRAND-CONTEXT.md` - Brand context (already read in Step 1.2)

**Note key requirements:**
```
WRITING GUIDELINES CHECKLIST:
- [ ] Specific opening hooks (no "transforms" vagueness)
- [ ] No verbose transitions before stats
- [ ] Statistics must have bridges to context
- [ ] Relationships represented accurately (use architecture documentation)
- [ ] Processes explained correctly (use workflow diagram)
- [ ] Each statistic mapped to correct entity (use ERD)
- [ ] NO third-party company case studies (no "Company X saved Y with Tool Z")
- [ ] Max 3 external links (Tier 1/2 only)
- [ ] Min 2 internal links to man.digital
- [ ] One domain used once
- [ ] Vary paragraph lengths (1, 2, OR 3 sentences)
- [ ] 8-12 bullet sections minimum
- [ ] 2-4 visual placeholders
- [ ] No uniform spacing (AI detection avoidance)
```

**CRITICAL: No Third-Party Case Studies Rule**

> **⚠️ MAN Digital is a RevOps consultancy, NOT a tool vendor's marketing team**

**NEVER include third-party company case studies or success stories.**

**❌ FORBIDDEN - Do NOT write:**
- "Agicap saved 750 hours weekly across 150 sales reps with HubSpot Prospecting Agent"
- "Company X increased conversion by Y% using Tool Z"
- "Organization A reduced costs by $X with Platform B"
- "Startup C accelerated their sales cycle by Y weeks using Feature D"
- ANY mention of specific companies' results with specific tools

**Why this is forbidden:**
- Makes MAN Digital look like we're selling tools, not consulting
- Positions us as tool evangelists instead of strategic advisors
- Undermines our process-first, RevOps consultancy positioning
- We are NOT HubSpot's (or any vendor's) marketing department

**✅ ALLOWED - What you CAN use:**

**Industry Statistics & Research:**
- "AI-powered prospecting tools can reduce research time by up to 95% (Source: Industry Research Firm)"
- "Companies implementing automated personalization see 2x higher response rates on average (Source: HubSpot Research)"
- "Sales teams report saving 10-20 hours weekly with prospecting automation (Source: Gartner)"

**General Capabilities:**
- "Modern prospecting agents cut research from 15-20 minutes to under 1 minute"
- "AI personalization typically doubles response rates compared to manual approaches"
- "Automated prospecting can save 750+ hours weekly for a 150-person sales team"

**Our Own Work (MAN Digital case studies):**
- "Our client, a mid-market SaaS company, implemented RevOps framework and..."
- Reference OUR implementations, OUR results, OUR methodologies

**The Rule:**
If the content research includes third-party case studies (e.g., "Agicap saved..."), **extract only the general capability or industry statistic**, NOT the company-specific success story.

**Transformation Example:**

Research says: "Agicap saved 750 hours weekly across 150 sales reps with HubSpot (Source: HubSpot)"

❌ Don't write: "Agicap saved 750 hours weekly with HubSpot's Prospecting Agent"

✅ Do write: "Prospecting automation can save 750+ hours weekly for a 150-person sales team (Source: HubSpot Research)" OR "Teams of 150+ sales reps report saving 750 hours weekly with automation"

**Remove the company name, keep the capability/statistic.**

### Step 1.9: Example Structure Review

> **📊 Review example blog posts for structure patterns**

**Read at least 2 examples:**
- `examples/example-1-health-score.md`
- `examples/example-2-revops-framework.md`
- `examples/example-3-ai-agents.md`

**Note structural patterns:**
- Paragraph variety (mix of 1, 2, 3 sentences)
- Extensive bullet usage
- Visual placeholder placement
- Bold header usage
- Table usage for comparisons
- Opening hook patterns
- Statistics with bridges
- Section flow

### Step 1.10: Drafting Plan Creation

**NOW organize everything into a drafting plan:**

```
COMPREHENSIVE DRAFTING PLAN:

STRUCTURE (from Brief):
H1: [from brief or create]
H2 #1: [from brief] → Map H2 keyword: [keyword from SEO research]
H2 #2: [from brief] → Map H2 keyword: [keyword from SEO research]
H2 #3: [from brief] → Map H2 keyword: [keyword from SEO research]
[Continue for all H2s from brief]

STATISTICS PLACEMENT PLAN:
Section: [H2 title]
→ Use statistic: "[stat text]" - Source: [domain] - Bridge: "[how to connect]" - Entity: [which entity]

Section: [H2 title]
→ Use statistic: "[stat text]" - Source: [domain] - Bridge: "[how to connect]" - Entity: [which entity]

[Plan placement for all statistics - ensure entity matches section context]

CONTENT GAP FILLING:
- Brief covers: [topics from brief]
- Must add (universal topics): [any missing universal topics]
- Will add (differentiation): [content gaps we're filling]

WORD COUNT DISTRIBUTION:
Target: [X,XXX words total]
Opening: ~150 words
H2 #1: ~200 words
H2 #2: ~250 words
H2 #3: ~200 words
[Continue for all sections to reach target]

VISUAL PLACEMENT:
- Visual 1: [after H2 #2] - [type: screenshot/diagram]
- Visual 2: [after H2 #4] - [type: table/chart]
- Visual 3: [after H2 #6] - [type: diagram]

LINKING STRATEGY:
Internal Links (min 2):
1. Link to: man.digital/[service-page] in section [H2 #X]
2. Link to: man.digital/[resource-page] in section [H2 #Y]

External Citations (max 3):
1. [Domain 1] - [statistic] - Section [H2 #X]
2. [Domain 2] - [statistic] - Section [H2 #Y]
3. [Domain 3] - [statistic] - Section [H2 #Z]

SEO DELIVERABLES PLAN:
SEO Title (50-60 chars): [draft title following pattern from SEO_guidelines.md]
SEO Meta Description (150-160 chars): [draft description following pattern from SEO_guidelines.md]
```

### Step 1.9: Digestion Verification Checkpoint

**Before proceeding to drafting, verify:**

- [ ] Brief structure fully understood and documented
- [ ] Brand positioning angle determined
- [ ] SEO research data organized (keywords, targets, strategy)
- [ ] Content research statistics inventory created
- [ ] Entity Relationship Diagram studied and entity map created
- [ ] Entity-statistic mappings documented
- [ ] Entity mismatch risks identified
- [ ] Guidelines reviewed and requirements noted
- [ ] Examples reviewed for structural patterns
- [ ] Comprehensive drafting plan created with all sections mapped
- [ ] Statistics placement planned with entity verification
- [ ] Word count distribution planned
- [ ] Link strategy planned (2+ internal, 3 max external)
- [ ] SEO deliverables drafted (title + meta description)

**⚠️ IF ANY ITEM UNCHECKED:** Complete it before proceeding. Digestion phase is non-negotiable.

**Output Digestion Summary:**

```
✅ DIGESTION PHASE COMPLETE

Inputs Processed:
✅ Brief: [topic] - Structure with [X] H2s planned
✅ SEO Research: [keyword] - [X] H2 keywords, [Y] H3 keywords mapped
✅ Content Research: [X] statistics inventoried, ERD with [Y] entities mapped
✅ Brand Positioning: [decision maker] - [service connection] - [differentiator]
✅ Guidelines: Writing style, SEO requirements, brand context internalized
✅ Examples: Structural patterns identified

Drafting Plan Ready:
✅ [X,XXX] word target with section distribution planned
✅ Statistics mapped to correct entities with bridges planned
✅ Content gaps identified and will be filled
✅ Link strategy: [X] internal + [X] external citations planned
✅ SEO deliverables: Title (XX chars) + Meta (XXX chars) drafted

PROCEEDING TO PHASE 2: DRAFTING
```

---

## Phase 2: Drafting

> **📋 Reference: `references/STRUCTURE-QUICK-REF.md` for structure requirements**
> **📝 Reference: `examples/` for structural patterns**

**⚠️ DRAFT AT TARGET WORD COUNT:** Do NOT create oversized draft and trim later. Create draft at target size from the start.

### Step 2.1: Opening (MANDATORY STRUCTURE)

**Sentence 1: Hook with keyword**
- Contains primary keyword from SEO research
- Complete standalone sentence
- States **SPECIFIC** value (NOT "transforms" vagueness)
- ONE sentence only

**Sentences 2-3: Amplify with statistics**
- Use statistic from content research inventory
- Verify entity matches (check ERD)
- Add bridge phrase to connect
- Citation format: `(Source: Domain Name)`

**Example Good Opening:**
```
HubSpot social agent automates content generation, scheduling, and engagement—freeing marketers to focus on strategy.

That time burden is real: marketing teams spend 15-20 hours weekly on manual social scheduling (Source: HubSpot Research).

This automation shift transforms tactical bottlenecks into strategic capacity.
```

**Example BAD Opening:**
```
AI transforms social media management from burden to advantage. [❌ Vague "transforms"]

Digital marketers spend 2 hours and 24 minutes daily on social platforms. [❌ Wrong entity - this is USER consumption time, not MARKETER creation time]

The social agent automates these tasks. [❌ No bridge, disconnected]
```

### Step 2.2: Body Structure

**Requirements:**
- **Paragraph variety:** Mix of 1, 2, and 3 sentence paragraphs (NOT uniform)
- **Extensive bullets:** 8-12 bullet sections minimum
- **Sub-bullets:** 3-5 instances of nested bullets
- **Visual placeholders:** 2-4 minimum ([Screenshot], [Diagram], [Table])
- **Comparison tables:** 1-2 when comparing data
- **Bold headers:** 8-12 for visual hierarchy
- **One idea per paragraph**
- **Line breaks between paragraphs**

**Flow Pattern (adjust based on brief):**
1. Problem Context (3-4 paragraphs, 1-2 bullet sections)
2. What/Solution (3-4 paragraphs, 2-3 bullet sections)
3. Why It Matters (2-3 paragraphs, 1 bullet section)
4. How It Works (4-5 paragraphs, 2-3 bullet sections, 1 table, 1-2 visuals)
5. Implementation (4-5 paragraphs, 2-3 bullet sections, 1 visual)
6. Business Impact (3-4 paragraphs, 1-2 bullet sections, 1 table)
7. Next Steps (2-3 paragraphs, 1 bullet section)

### Step 2.3: Statistics Usage with Entity Verification

**For EVERY statistic used:**

1. **Check entity mapping** (from digestion phase)
   - Which entity does this stat describe?
   - Which entity am I discussing in this paragraph?
   - Do they match?

2. **Add bridge phrase**
   - Never drop statistic without transition
   - Use bridge patterns: "That reality shows...", "The data confirms...", "Consider the scale..."

3. **Track domain usage**
   - Each domain used ONCE only
   - Update domain tracking list

**Example with Entity Verification:**
```
Context: Discussing social agent tool for MARKETERS creating content

Statistics Available:
- "Teams spend 15-20 hours weekly on social scheduling" → Entity: MARKETER ✅
- "Users spend 2.5 hours daily on social platforms" → Entity: USER ❌ MISMATCH

Use: "Teams spend 15-20 hours weekly on social scheduling"
Bridge: "That time burden is real:"
Full: "That time burden is real: teams spend 15-20 hours weekly on social scheduling (Source: HubSpot Research)."
```

### Step 2.4: Following the Brief Structure

**CRITICAL: Brief IS the law:**

- Follow H2 structure from brief exactly
- Use H2 keywords from SEO research where they map to brief sections
- Cover all topics from brief
- Meet any specific requirements from brief
- If brief specifies order, follow that order

### Step 2.5: Word Count Monitoring

**As you draft, monitor word count:**
- Target: [from digestion plan]
- Current: [check periodically]
- Remaining sections: [X sections left]
- Words per remaining section: [calculate]

**Stay on target throughout drafting - do NOT overdraft and trim later.**

### Step 2.6: Link Integration

**Internal Links (min 2):**
- Natural contextual placement
- Link to MAN Digital services or resources
- Format: `[descriptive anchor text](https://man.digital/page)`
- Track: [X of 2+ minimum completed]

**External Citations (max 3):**
- Inline citation format: `(Source: Domain Name)`
- NO full URLs in text
- Only Tier 1/2 authoritative sources
- Track: [X of 3 maximum used]

### Step 2.7: Natural Formatting (AI Detection Avoidance)

**⚠️ VARY your spacing - no uniform patterns:**

- Some H2 sections start immediately after heading (no line break)
- Other H2 sections have line break after heading
- NO pattern - mix it up naturally
- Think: "Does this need breathing room or immediate flow?"

**Example Natural Variation:**
```markdown
## Benefits of Automation
Marketing teams gain three key advantages:

## Implementation Steps

1. Configure your settings
2. Define your workflows

## ROI Analysis

The investment delivers measurable returns...
```
✅ Varied spacing - some headings have breaks, some don't

### Step 2.8: Draft Completion Checklist

**Before moving to SEO validation:**

- [ ] Word count: [X,XXX words] (within target range)
- [ ] Paragraph variety: Mix of 1, 2, 3 sentences (counted)
- [ ] Bullet sections: [X of 8-12 minimum]
- [ ] Sub-bullets: [X of 3-5 instances]
- [ ] Visual placeholders: [X of 2-4 minimum]
- [ ] Tables: [X of 1-2 for comparisons]
- [ ] Bold headers: [X of 8-12 minimum]
- [ ] Internal links: [X of 2+ minimum]
- [ ] External citations: [X of 3 maximum]
- [ ] All H2s from brief included
- [ ] All universal topics covered
- [ ] Content gaps filled (differentiation)
- [ ] Primary keyword in H1, opening, conclusion
- [ ] H2 keywords mapped to sections
- [ ] All statistics have entity verification + bridges
- [ ] Domain tracking: each used once only
- [ ] Natural spacing (no uniform AI patterns)
- [ ] SEO Title (50-60 chars) included
- [ ] SEO Meta Description (150-160 chars) included

---

## Phase 3: Post-Draft SEO Validation (BEFORE EDITING)

> **🔧 Use: `scripts/seo-validation-helper.py` for automated validation**

**Purpose:** Validate SEO BEFORE editing to catch issues when they're easier to fix.

### Step 3.1: Primary Keyword Validation

From SEO research file:
- Primary keyword: [keyword]

Check draft:
- [ ] Keyword in H1? YES/NO
- [ ] Keyword in first 100 words? YES/NO
- [ ] Keyword in conclusion? YES/NO
- [ ] Keyword density: [calculate: (count/total_words)*100] → Target: 1.5-2.5%

**If ANY fails:** Fix before proceeding.

### Step 3.2: H2/H3 Keywords Validation

From SEO research file:
- H2 keywords (high-volume): [list]
- H3 keywords (medium-volume): [list]

Check draft:
- [ ] Total H2 count: [X] → Target from SEO research: [Y]
- [ ] H2s containing high-volume keywords: [X of Y]
- [ ] Total H3 count: [X] → Target from SEO research: [Y]
- [ ] H3s containing medium-volume keywords: [X of Y]

**List missing keywords and add if needed.**

### Step 3.3: Heading Structure Validation

- [ ] Single H1 only (not multiple)
- [ ] H1 includes target keyword
- [ ] Proper hierarchy (no H3 before H2, etc.)
- [ ] H2 count: 5-8 range
- [ ] H3 depth: 2-3 per H2 average

### Step 3.4: Meta Elements Validation

> **Reference: `guidelines/SEO_guidelines.md` for patterns**

**SEO Title:**
- Current: [title]
- Character count: [X]
- Target: 50-60 chars
- Pattern: `[Topic] for RevOps: [Benefit] | MAN Digital`
- Includes keyword? YES/NO

**SEO Meta Description:**
- Current: [description]
- Character count: [X]
- Target: 150-160 chars
- Pattern: `Transform [challenge] with [solution]. Learn how RevOps teams use [topic] to [benefit]. [CTA].`
- Includes keyword + CTA? YES/NO

### Step 3.5: Content Structure Validation

From SEO research file - compare to targets:
- Word count: Draft [X,XXX] vs Target [Y,YYY] → Pass/Fail
- H2 count: Draft [X] vs Target [5-8] → Pass/Fail
- H3 count: Draft [X] vs Target [10+] → Pass/Fail

### Step 3.6: Technical SEO Elements

- [ ] Internal links: [X of 2+ minimum] → Pass/Fail
- [ ] External citations: [X of 3 maximum] → Pass/Fail
- [ ] Citation format correct: `(Source: Domain)` → YES/NO
- [ ] All sources Tier 1/2 authority: YES/NO
- [ ] Each domain used once only: YES/NO

### Step 3.7: Universal Topics & Gaps Check

From content research file:
- Universal topics (must include): [list]
- Content gaps (differentiation): [list]

Check draft:
- [ ] All universal topics covered? YES/NO
- [ ] All content gaps filled? YES/NO

**List any missing and add before proceeding.**

### Step 3.8: SEO Validation Output

**Document results:**
```
POST-DRAFT SEO VALIDATION:

✅ PASSED:
- [list all passed checks]

⚠️ ISSUES FOUND & FIXED:
- [Issue 1]: [what was wrong] → [how fixed]
- [Issue 2]: [what was wrong] → [how fixed]

READY FOR EDITING: ✅ YES / ❌ NO
```

**⚠️ Fix ALL issues before proceeding to editing phase.**

---

## Phase 4: Editing (MANDATORY - ALL 11 FRAMEWORKS + FINAL POLISH)

> **📚 All editing checklists in: `editing-checklists/` directory**
> **📋 See: `references/editing-excellence-examples.md` for thorough vs rushed editing examples**

**⚠️⚠️⚠️ CRITICAL EDITING MINDSET WARNING ⚠️⚠️⚠️**

**THE #1 FAILURE MODE: RUSHING THROUGH EDITING**

**MANDATORY APPROACH:**
- ✋ **SLOW DOWN** - 15-20 minutes minimum for 1,500 words
- 🔍 **BE THOROUGH** - Aim for 20-30+ specific improvements
- 💭 **THINK DEEPLY** - Question every word choice
- ✅ **FIND EVERYTHING** - Read multiple times

**If you find yourself saying "looks good" after 5 minutes, you RUSHED. Go back.**

### Framework Application Order (MUST apply in sequence)

**1. COMPREHENSIVE EDIT CHECKLIST** (`editing-checklists/01_Editing_-_Edit_Checklist.md`) - **APPLY FIRST**
   - **⚠️ MOST IMPORTANT EDITING STEP ⚠️**
   - Time: 15-20 minutes minimum
   - Runs complete copy editing forensics
   - Checks: redundancy (especially openings), outcome-first headers, active voice, tenses, parallelism, sentence structure, specificity, stats with magnitude, style consistency, synthesis
   - **Ultra-thoroughness required**

**2. Redundancy Deep Dive** (`editing-checklists/02_Editing_-_Redudancy.md`)
   - Remove repeated words/ideas
   - Each sentence advances narrative
   - **Style Check:** Paragraph variety preserved?

**3. Active Voice** (`editing-checklists/03_Editing_-_Active_Voice.md`)
   - Convert passive to active
   - More direct, powerful writing
   - **Style Check:** Bullet sections maintained?

**4. Tenses** (`editing-checklists/05_Editing_-_Tenses.md`)
   - Favor simple present
   - Ensure consistency
   - **Style Check:** Visual placeholders present?

**5. Parallelism** (`editing-checklists/04_Editing_-_Parallelism.md`)
   - Match structures in lists
   - Consistent word choice/tenses
   - **Style Check:** Sub-bullets used?

**6. Sentence Variety** (`editing-checklists/06_Editing_-_Sentence_Structure.md`)
   - Mix sentence types and lengths
   - Create rhythm and flow
   - **Style Check:** Paragraph lengths varied?

**7. Specificity** (`editing-checklists/07_Editing_-_Specificity.md`)
   - Add quantifiable numbers
   - Make problems/outcomes specific
   - **Style Check:** Tables used for comparisons?

**8. Arguments** (`editing-checklists/08_Editing_-_Amplify_Your_Arguments.md`)
   - Structure: Claim → Support → Takeaway
   - Strengthen evidence
   - **Style Check:** Bold headers for hierarchy?

**9. Structure** (`editing-checklists/09_Editing_-_Structural_Strategy.md`)
   - Check overall flow
   - Ensure smooth transitions
   - **Style Check:** Overall structure matches examples?

**10. Takeaways** (`editing-checklists/10_Editing_-_Takeaway.md`)
   - Clear conclusions in each section
   - Actionable insights
   - **Style Check:** Required elements present?

**11. FINAL STRUCTURE AUDIT** - **CRITICAL**
   - **PERFORM SCROLL TEST:** Open `examples/example-1-health-score.md` and your article side-by-side
   - **Verify VARIETY:** Mix of 1, 2, 3 sentence paragraphs
   - **Count bullet sections:** Need 8-12 minimum
   - **Count visual placeholders:** Need 2-4 minimum
   - **Check sub-bullets:** Need 3-5 instances
   - **Verify tables:** 1-2 when comparing data
   - **Count bold headers:** Need 8-12 minimum
   - **Does it LOOK like the example?** If NO → REJECTED
   - **Flag ANY 4+ sentence paragraphs** and break up

**11.5. POST-EDITING SEO VERIFICATION** - **MANDATORY**

After all 11 frameworks, verify editing didn't break SEO:

```
POST-EDITING SEO CHECK:
☑ H1: Still correct with keyword? YES/NO
☑ H2 Count: Still 5-8? [X H2s]
☑ H2 Keywords: At least 2-3 still have keyword variations? YES/NO
☑ Meta Title: Unchanged? [XX chars]
☑ Meta Description: Unchanged? [XXX chars]
☑ Keyword Placement: Still in first 100 words, conclusion? YES/NO
☑ Heading Hierarchy: Still correct? YES/NO
☑ Internal Links: Still [X of 2+]? YES/NO
☑ External Links: Still [X of 3 max]? YES/NO
☑ Keyword Density: Still 1.5-2.5%? [X.X%]
☑ Word Count: Still in range? [X,XXX words]
```

**If ANY issues:** Fix immediately before final polish.

### Framework 12: FINAL WORD-BY-WORD POLISH (MANDATORY)

> **Reference: `editing-checklists/11_Editing_-_Final_Word_by_Word_Polish.md`**

**Purpose:** Comprehensive 9-step final pass after ALL frameworks.

**Time Requirement:** 15-20 minutes minimum for 1,500 words.

**The 9-Step Final Polish:**

1. **Wording & Sentence Structure**
   - Read each sentence aloud (mentally)
   - Fix awkward phrasings
   - Ensure sentence variety

2. **Grammar & Spelling**
   - Subject-verb agreement
   - Comma splices, run-ons
   - Spelling, punctuation
   - Capitalization (HubSpot, RevOps, X)

3. **Brevity (Omit Needless Words)**
   - Remove filler: "really", "very", "quite", "actually"
   - Cut redundancies
   - Eliminate throat-clearing

4. **Clichés & Corporate Jargon**
   - Remove: "synergy", "leverage", "paradigm shift"
   - Cut: "at the end of the day", "moving forward"
   - Replace vague with specific

5. **Readability (Simplify Convoluted)**
   - Break complex sentences
   - Simplify nested clauses
   - Use common words

6. **Passive to Active Voice**
   - Final check for remaining passive constructions
   - Convert to active

7. **Confidence (Remove Hedging)**
   - Remove: "probably", "I think", "might", "perhaps"
   - Make direct, confident statements

8. **Citation Verification**
   - All claims have evidence
   - All sources authoritative (Tier 1/2)
   - Format correct: `(Source: Domain)`
   - Each domain used once

9. **Repetition Removal**
   - Scan for repeated words/phrases
   - Vary language
   - Eliminate redundancy

**Final Polish Output:**
```
FINAL POLISH COMPLETE:

Changes Made: [X] specific improvements
- [Improvement 1]: [location] - [what changed]
- [Improvement 2]: [location] - [what changed]
[Continue for all improvements]

Final Quality Metrics:
✅ Word count: [X,XXX] (target: [Y,YYY])
✅ No passive voice remaining
✅ No corporate jargon/clichés
✅ No hedging language
✅ All citations verified
✅ No repetition
✅ Readability optimized
✅ Confidence maintained

READY FOR FINAL DELIVERABLES: ✅
```

---

## Phase 5: Final Deliverables

### Step 5.1: Format Final Markdown

**Ensure proper formatting:**
- H1 title at top
- SEO Title and Meta Description after H1 (in HTML comments or separate section)
- Proper heading hierarchy (H1 → H2 → H3)
- Line breaks between paragraphs
- Natural spacing (varied, not uniform)
- Bold headers for visual hierarchy
- Bullet lists formatted correctly
- Tables formatted correctly
- Visual placeholders noted: `[Screenshot: description]`, `[Diagram: description]`, `[Table: description]`

### Step 5.2: Create Publication Package

**Output files:**

1. **blog-post-[keyword]-[date].md** - Complete blog post markdown
2. **metadata-[keyword]-[date].txt** - SEO title, meta description, tags, etc.

**Metadata file format:**
```
SEO Title: [50-60 char title]
SEO Meta Description: [150-160 char description]
Primary Keyword: [keyword]
H2 Keywords Used: [list]
Word Count: [X,XXX]
Internal Links: [X] ([list URLs])
External Citations: [X] ([list domains])
Publication Date: [date or TBD]
Target Audience: [audience]
```

### Step 5.3: Final Quality Checklist

**Before delivery, verify ALL:**

**Content Quality:**
- [ ] Word count in target range
- [ ] Brief structure followed exactly
- [ ] All brief requirements met
- [ ] Brand positioning clear (RevOps consultancy, not HubSpot seller)
- [ ] MAN Digital differentiators shown
- [ ] All universal topics covered
- [ ] Content gaps filled (differentiation)

**Entity & Statistics:**
- [ ] All statistics from content research used appropriately
- [ ] Entity mapping followed (no mismatches)
- [ ] All statistics have bridge phrases
- [ ] All sources Tier 1/2 authoritative
- [ ] Each domain used once only

**SEO:**
- [ ] Primary keyword in H1, opening, conclusion
- [ ] Keyword density 1.5-2.5%
- [ ] H2 count: 5-8
- [ ] H2s use related keywords from SEO research
- [ ] H3 count: 10+
- [ ] H3s provide depth
- [ ] Heading hierarchy correct
- [ ] SEO title: 50-60 chars, follows pattern
- [ ] SEO meta description: 150-160 chars, includes CTA

**Structure & Style:**
- [ ] Paragraph variety: Mix of 1, 2, 3 sentences
- [ ] Bullet sections: 8-12 minimum
- [ ] Sub-bullets: 3-5 instances
- [ ] Visual placeholders: 2-4 minimum
- [ ] Tables: 1-2 for comparisons
- [ ] Bold headers: 8-12 minimum
- [ ] Natural spacing (no uniform AI patterns)
- [ ] Matches example structure (scroll test passed)
- [ ] No 4+ sentence paragraphs

**Links & Citations:**
- [ ] Internal links: 2+ minimum to man.digital
- [ ] External citations: 3 maximum
- [ ] Citation format: `(Source: Domain)` - no full URLs
- [ ] All sources authoritative
- [ ] Domain tracking: each used once

**Editing:**
- [ ] All 11 frameworks applied in order
- [ ] Final word-by-word polish completed
- [ ] Post-editing SEO verification passed
- [ ] No passive voice
- [ ] No corporate jargon/clichés
- [ ] No hedging language
- [ ] No redundancy
- [ ] Readability optimized
- [ ] All citations verified

**If ANY item fails:** Fix before delivery.

### Step 5.4: Delivery Summary

**Provide final summary to user:**

```
✅ BLOG POST CREATION COMPLETE

Publication-Ready Files:
✅ blog-post-[keyword]-[date].md ([X,XXX] words)
✅ metadata-[keyword]-[date].txt

Quality Metrics:
✅ Brief adherence: 100% (all requirements met)
✅ Brand positioning: RevOps consultancy angle maintained
✅ Entity mapping: All statistics entity-verified using ERD
✅ SEO optimization: All targets from SEO research met
✅ Word count: [X,XXX] (target: [Y,YYY])
✅ Paragraph variety: [X]% 1-sent, [Y]% 2-sent, [Z]% 3-sent
✅ Bullet sections: [X] (target: 8-12 min)
✅ Visual placeholders: [X] (target: 2-4 min)
✅ Internal links: [X] to man.digital (target: 2+ min)
✅ External citations: [X] authoritative sources (target: 3 max)
✅ Editing frameworks: All 11 applied + final polish
✅ SEO verification: Passed (pre-edit and post-edit)

Content Differentiation:
✅ Universal topics covered: [list]
✅ Content gaps filled: [list]
✅ Unique angle: [differentiation approach]

Statistics Used: [X] total
- All entity-verified against ERD
- All from Tier 1/2 authoritative sources
- All with context bridges
- All domains used once only

Ready for Publication: ✅ YES
```

---

## Common Mistakes to Avoid

### Input Phase Mistakes:
1. **Skipping input validation** - Not confirming all inputs received
2. **Missing inputs** - Proceeding without brief, SEO research, or content research
3. **Not checking dates** - Using outdated research files
4. **Ignoring ERD** - Skipping entity relationship diagram from content research

### Digestion Phase Mistakes:
5. **Skipping digestion entirely** - Going straight to drafting (FATAL ERROR)
6. **Rushed digestion** - Not thoroughly reading all inputs
7. **No brand review** - Skipping MAN-DIGITAL-BRAND-CONTEXT.md
8. **Ignoring ERD** - Not studying entity relationships before writing
9. **No entity mapping** - Not documenting which stats apply to which entities
10. **No drafting plan** - Starting to draft without organized plan
11. **Skipping examples** - Not reviewing example blog posts for structure

### Drafting Mistakes:
12. **Ignoring brief** - Not following brief structure exactly
13. **Wrong word count approach** - Creating oversized draft and trimming (wrong method)
14. **Entity mismatches** - Using stats about wrong entities (not checking ERD)
15. **No stat bridges** - Dropping statistics without transitions
16. **Vague opening hooks** - Using "transforms" instead of specific value
17. **Uniform structure** - All paragraphs same length (no variety)
18. **Too few bullets** - Less than 8 bullet sections
19. **No visual placeholders** - Forgetting to plan visuals
20. **Domain reuse** - Using same domain more than once
21. **Too many external links** - Exceeding 3 maximum
22. **Low-authority sources** - Citing Tier 3 blogs instead of Tier 1/2
23. **Uniform spacing** - Line break after every heading (AI detection pattern)

### SEO Validation Mistakes:
24. **Skipping pre-edit SEO validation** - Going straight to editing without SEO check
25. **Wrong keyword density** - Too low (<1.5%) or too high (>2.5%)
26. **Missing H2 keywords** - Not using related keywords from SEO research
27. **Shallow H3 depth** - Less than 2-3 H3s per H2
28. **Meta elements wrong length** - Title not 50-60 chars, description not 150-160 chars
29. **Missing universal topics** - Not covering topics all competitors cover
30. **Not filling content gaps** - Missing differentiation opportunities

### Editing Mistakes:
31. **RUSHING** - Finishing editing in <5 minutes for 1,500 words (FATAL)
32. **Skipping frameworks** - Not applying all 11 frameworks in order
33. **Breaking structure** - Editing destroys paragraph variety, bullets, visuals
34. **Removing SEO elements** - Editing accidentally removes keywords or links
35. **No post-edit SEO check** - Not verifying SEO after editing
36. **Skipping final polish** - Not doing final word-by-word pass
37. **Creating uniform blocks** - Edits remove variety, create monotony
38. **Missing scroll test** - Not comparing to examples before declaring done

### Final Deliverables Mistakes:
39. **Missing metadata file** - Only delivering markdown, not SEO metadata
40. **Wrong file naming** - Not using convention: blog-post-[keyword]-[date].md
41. **Incomplete quality check** - Skipping final verification checklist
42. **No delivery summary** - Not providing quality metrics to user

---

## References & Support Files

**Guidelines:**
- `guidelines/MAN-DIGITAL-BRAND-CONTEXT.md` - Brand positioning, services, client profile, differentiators
- `guidelines/Writing_guidelines.md` - Writing style and voice requirements
- `guidelines/SEO_guidelines.md` - SEO title and meta description patterns
- `guidelines/positioning_hubspot_revops.json` - Positioning data structure

**Editing Checklists (Apply in Order):**
- `editing-checklists/01_Editing_-_Edit_Checklist.md` - MASTER checklist (APPLY FIRST)
- `editing-checklists/02_Editing_-_Redudancy.md` - Redundancy removal
- `editing-checklists/03_Editing_-_Active_Voice.md` - Passive to active conversion
- `editing-checklists/04_Editing_-_Parallelism.md` - Structural consistency
- `editing-checklists/05_Editing_-_Tenses.md` - Tense consistency
- `editing-checklists/06_Editing_-_Sentence_Structure.md` - Sentence variety
- `editing-checklists/07_Editing_-_Specificity.md` - Quantifiable specificity
- `editing-checklists/08_Editing_-_Amplify_Your_Arguments.md` - Argument strengthening
- `editing-checklists/09_Editing_-_Structural_Strategy.md` - Flow and logic
- `editing-checklists/10_Editing_-_Takeaway.md` - Clear conclusions
- `editing-checklists/11_Editing_-_Final_Word_by_Word_Polish.md` - Final comprehensive pass

**Examples (Review for Structure):**
- `examples/example-1-health-score.md` - Customer health scoring example
- `examples/example-2-revops-framework.md` - RevOps framework example
- `examples/example-3-ai-agents.md` - AI agents example

**References:**
- `references/STRUCTURE-QUICK-REF.md` - Quick structure requirements reference
- `references/editing-excellence-examples.md` - Examples of thorough vs rushed editing
- `references/seo-competitor-analysis-template.md` - SEO analysis template (for reference)
- `references/seo-analysis-workflow.md` - SEO analysis workflow (for reference)
- `references/planning-framework.md` - Planning and source authority (for reference)

**Scripts:**
- `scripts/seo-validation-helper.py` - Automated SEO validation tool

**Templates:**
- `brief-template.md` - Brief format template (for reference)

---

## Success Criteria

A blog post created with this skill is successful when:

✅ **Brief Adherence:** Follows brief structure exactly, meets all requirements
✅ **Brand Positioning:** Clearly positions MAN Digital as RevOps consultancy (not HubSpot seller)
✅ **Entity Accuracy:** All statistics entity-verified using ERD, no mismatches
✅ **SEO Optimization:** Meets all SEO targets from research (keywords, structure, meta)
✅ **Content Quality:** Target word count, variety, extensive bullets, visuals
✅ **Source Authority:** Only Tier 1/2 sources, proper citations, domain tracking
✅ **Editing Excellence:** All 11 frameworks applied thoroughly + final polish
✅ **Structure Match:** Passes scroll test against examples
✅ **Differentiation:** Fills content gaps, covers universal topics
✅ **Publication Ready:** Requires zero additional editing before publication

**User Feedback Loop:** After publication, note what worked well and what could improve for future iterations of this skill.
