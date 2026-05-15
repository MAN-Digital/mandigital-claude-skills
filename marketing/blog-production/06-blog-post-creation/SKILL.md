---
name: blog-post-creation
description: "Creates SEO-optimized blog posts for MAN Digital RevOps consultancy. RECEIVES brief, SEO research, content research. MANDATORY: Run validation scripts after drafting and editing - formatting-validator.py, readability-scorer.py MUST PASS. Creates drafts with extensive bullets (8-12 sections), paragraph variety (1, 2, 3 sentences mixed), high readability (Flesch-Kincaid 60-70) for non-native English speakers. Applies 11-step editing framework. Scripts enforce variety and scannability programmatically."
---

# MAN Digital Blog Post Creation Skill

## Purpose

Creates **publication-ready** blog posts for MAN Digital's RevOps consultancy based on provided research inputs.

**What This Skill Does:**
✅ Receives research inputs (brief, SEO research, content research)
✅ Creates drafts with enforced formatting (variety, bullets, visuals)
✅ Validates with scripts (formatting, readability, SEO - MANDATORY)
✅ Applies comprehensive editing (11 frameworks)
✅ Outputs publication-ready markdown

**What This Skill Does NOT Do:**
❌ SEO pre-research (use `blog-post-seo-research` skill)
❌ Content research (use `blog-post-content-research` skill)

---

## 🚨 CRITICAL: Formatting Requirements (ENFORCED BY SCRIPTS)

**The #1 Problem:** Previous outputs had fat paragraphs, few bullets, poor scannability.

**The Solution:** Validation scripts now **enforce** these requirements:

### Required Formatting (Validated Programmatically)

**Paragraph Variety (MANDATORY):**
- 10-15 single-sentence paragraphs (punch, emphasis)
- 20-25 two-sentence paragraphs (explanations)
- 5-10 three-sentence paragraphs (maximum depth)
- **ZERO** 4+ sentence paragraphs (auto-reject)

**Extensive Bullets (MANDATORY):**
- 8-12 bullet sections minimum
- 3-5 instances of sub-bullets (nested lists)

**Visual Elements (MANDATORY):**
- 2-4 visual placeholders: [Screenshot: ...], [Diagram: ...]
- 1-2 tables for data comparisons
- 8-12 bold headers for hierarchy

**Readability (MANDATORY - Non-Native English Speakers):**
- Flesch Reading Ease: 60-70 (Easy)
- Flesch-Kincaid Grade: 8-10 (Middle school)
- Average sentence length: 15-20 words
- Complex words: <15%
- Passive voice: <10%

> **📚 See:** `references/formatting-guide.md` for visual examples
> **📚 See:** `references/readability-guide.md` for simplification techniques
> **📚 See:** `references/paragraph-patterns.md` for variety patterns

---

## Required Inputs (ALL MANDATORY)

### Input #1: The Brief
**Contains:** Topic, target keyword, content structure, headings, word count, audience

**⚠️ BRIEF IS SACRED:** Follow structure exactly.

### Input #2: SEO Research File
**Format:** `seo-research-[keyword]-[date].md`
**Contains:** Primary keyword, search intent, SERP competitors, H2/H3 keywords, strategy

### Input #3: Content Research File
**Format:** `content-research-[keyword]-[date].md`
**Contains:** Statistics (with sources), architecture docs, workflow diagrams, ERD, competitor analysis

**⚠️ IF ANY INPUT MISSING:** Request all three before proceeding.

---

## Phase 0: Input Validation

**Confirm all inputs received:**
```
✅ Brief: [topic]
✅ SEO Research: [keyword] - [volume]
✅ Content Research: [X stats], architecture, workflow, ERD
✅ Ready to proceed
```

---

## Phase 1: Digestion & Planning (MANDATORY BEFORE DRAFTING)

**⚠️ CRITICAL:** Do NOT skip this phase. Review ALL inputs before writing.

### Step 1.1: Review Brief
- [ ] Topic, keyword, structure understood
- [ ] Word count target noted (or default 1,200-1,600)
- [ ] Required H2 sections documented

### Step 1.2: Review Brand Context
> **📚 Read:** `guidelines/MAN-DIGITAL-BRAND-CONTEXT.md`

- [ ] Target persona identified
- [ ] Pain point addressed
- [ ] RevOps consultancy angle (not HubSpot seller)

### Step 1.3: Extract SEO Data
From SEO research file:
- Primary keyword: [keyword]
- H2 keywords (high-volume): [list for mapping]
- H3 keywords (medium-volume): [list]
- Target H2 count: 5-8
- Target H3 count: 10+

### Step 1.4: Extract Statistics & Sources
From content research file:
- Create statistics inventory
- Map stats to entities (use ERD to prevent mismatches)
- Track domain usage (each domain ONCE only)
- Max 3 external citations

### Step 1.5: Review Guidelines
> **📚 Read:** `guidelines/Writing_guidelines.md`
> **📚 Read:** `guidelines/SEO_guidelines.md`

Note requirements:
- Hook sentence pattern
- Citation format: `(Source: Domain)`
- NO third-party case studies
- Max 3 external links, min 2 internal links

### Step 1.6: Review Examples
> **📚 Open:** `examples/example-1-health-score.md`

Note structural patterns:
- Paragraph variety (1, 2, 3 sentence mix)
- Extensive bullet usage
- Visual placeholders
- Bold headers
- Tables

### Step 1.7: Create Drafting Plan
Document:
- H2 structure (from brief + SEO keywords)
- Statistics placement (which sections)
- Visual placeholders (where to insert)
- Link strategy (2+ internal, 3 max external)
- Word count distribution per section

**Digestion Complete Checkpoint:**
- [ ] All inputs reviewed
- [ ] Brand angle determined
- [ ] SEO data organized
- [ ] Statistics inventoried
- [ ] Drafting plan created

---

## Phase 2: Drafting

**⚠️ DRAFT AT TARGET WORD COUNT** - Do NOT overdraft and trim later.

### Step 2.1: Opening (MANDATORY STRUCTURE)

**Sentence 1: Hook with keyword**
- Contains primary keyword
- Complete standalone sentence
- States SPECIFIC value (NOT "transforms" vagueness)

**Sentences 2-3: Amplify with statistics**
- Use statistic from content research
- Add bridge phrase to connect
- Citation format: `(Source: Domain Name)`

**Example:**
```markdown
HubSpot social agent automates content generation and scheduling—freeing marketers for strategy.

Teams spend 15-20 hours weekly on manual social scheduling (Source: HubSpot Research).

This automation shifts capacity from tactical execution to strategic growth.
```

### Step 2.2: Body Structure

Follow brief structure exactly. For each section:

**Use Paragraph Variety:**
- Mix 1, 2, and 3 sentence paragraphs
- NEVER use 4+ sentences in one paragraph

**Use Extensive Bullets:**
- 8-12 bullet sections throughout article
- Use for: features, benefits, steps, comparisons, lists
- Add sub-bullets (3-5 instances of nested lists)

**Add Visual Hierarchy:**
- Bold headers (8-12 minimum): **Why this matters**, **How it works**
- Visual placeholders (2-4): [Screenshot: description], [Diagram: ...]
- Tables (1-2): For data comparisons

**Write for Non-Native Speakers:**
- Short sentences (15-20 words average)
- Simple vocabulary
- Active voice
- Clear structure

> **📚 See:** `references/paragraph-patterns.md` for specific patterns
> **📚 See:** `references/readability-guide.md` for simplification techniques

### Step 2.6: Article Ending Structure (MANDATORY)

**⚠️ CRITICAL:** Articles MUST end with a Conclusion section, NOT "Getting Started" or "Next Steps" as the final section.

**CORRECT Final Structure:**
1. Body sections (implementation, benefits, how-to)
2. **Final section: "Conclusion"** with:
   - Key takeaways (3-5 bullet points)
   - Actionable summary
   - Brief next steps (optional, as sub-section)
   - Closing statement

**Example Conclusion Structure:**
```markdown
## Conclusion

Your path to [topic]:

• [Key point 1]
  - [Sub-detail]
  - [Sub-detail]

• [Key point 2]
  - [Sub-detail]

• [Key point 3]
  - [Sub-detail]

Remember: [Closing wisdom statement]
```

**❌ WRONG (Do NOT end with):**
- "Getting Started" section
- "How to Get Started" section
- Implementation steps as final section

**✅ CORRECT (Always end with):**
- "Conclusion" section
- Key takeaways
- Summary of learnings

> **📚 See:** `examples/example-1-health-score.md` (lines 383-405) for perfect conclusion
> **📚 See:** `examples/example-2-revops-framework.md` (lines 341-365) for conclusion with next steps

### Step 2.3: Statistics Usage

For EVERY statistic:
1. Check entity mapping (use ERD from content research)
2. Add bridge phrase ("That reality shows...", "The data confirms...")
3. Track domain usage (each used ONCE only)

**NO Third-Party Case Studies:**
❌ "Agicap saved 750 hours with HubSpot"
✅ "Teams of 150+ sales reps save 750 hours weekly with automation"

### Step 2.4: Link Integration

**Internal Links (min 2):**
- Link to MAN Digital services/resources
- Format: `[anchor text](https://man.digital/page)`

**External Citations (max 3):**
- Inline format: `(Source: Domain Name)`
- NO full URLs in text
- Tier 1/2 authoritative sources only

### Step 2.5: Natural Formatting (AI Detection Avoidance)

**Vary spacing** - NO uniform patterns:
- Some H2 sections start immediately after heading
- Other H2 sections have line break after heading
- Mix naturally, think "breathing room vs. immediate flow"

---

## 🚨 CHECKPOINT: Mandatory Validation After Drafting

**⚠️ CRITICAL:** Run these scripts BEFORE proceeding to editing.

### Validation 1: Formatting (MUST PASS)

```bash
python scripts/formatting-validator.py draft.md
```

**What it validates:**
- Paragraph variety (1, 2, 3 sentence distribution)
- NO fat paragraphs (4+ sentences = auto-reject)
- Bullet sections (need 8-12 minimum)
- Visual placeholders (need 2-4)
- Tables (recommend 1-2)
- Bold headers (need 8-12)
- Sub-bullets (need 3-5 instances)

**If FAIL:** Fix issues immediately. Re-run until PASS. DO NOT proceed to editing.

> **📚 See:** `references/validation-workflow.md` for interpretation guide

### Validation 2: Readability (MUST PASS)

```bash
python scripts/readability-scorer.py draft.md
```

**What it validates:**
- Flesch Reading Ease (target: 60-70)
- Grade Level (target: 8-10)
- Sentence length (target: 15-20 words avg)
- Complex words (target: <15%)
- Passive voice (target: <10%)

**If FAIL:** Simplify vocabulary, break long sentences, use active voice. Re-run until PASS.

### Validation 3: SEO (MUST PASS)

```bash
python scripts/seo-validation-helper.py draft.md "target keyword"
```

**What it validates:**
- H1 heading (one only, includes keyword)
- H2/H3 count and keyword usage
- Keyword placement (H1, first 100 words, conclusion)
- Keyword density (1.5-2.5%)
- Meta title/description

**If FAIL:** Fix SEO issues before editing. Re-run until PASS.

**✅ ALL THREE MUST PASS BEFORE EDITING.**

---

## Phase 3: Editing (ALL 11 FRAMEWORKS)

> **📚 See:** `editing-checklists/` directory for detailed checklists

**⚠️ SLOW DOWN:** 15-20 minutes minimum for 1,500 words. If you finish faster, you RUSHED.

### Framework 1: Comprehensive Edit Checklist (MOST IMPORTANT)
> **Apply:** `editing-checklists/01_Editing_-_Edit_Checklist.md`

- Opening redundancy (paragraphs 1-2 often repeat)
- Outcome-first headers
- Stats with timeframes and baselines
- Remove filler words
- Avoid UI-instruction tone
- Make CTAs specific
- Style consistency (en dashes, curly quotes, contractions)
- Tighten verbs

**Time:** 15-20 minutes minimum

### Frameworks 2-11: Apply in Order
> **See:** `editing-checklists/` for detailed instructions

2. Redundancy Deep Dive
3. Active Voice
4. Parallelism
5. Tenses (favor simple present)
6. Sentence Variety
7. Specificity (quantifiable numbers)
8. Arguments (Claim → Support → Takeaway)
9. Structure (flow and transitions)
10. Takeaways (clear conclusions)
11. Final Word-by-Word Polish

**For each framework:**
- Apply thoroughly
- Preserve formatting (variety, bullets, visuals)
- Maintain readability
- Don't break SEO

### Post-Editing SEO Verification

After all editing, verify SEO still intact:
- [ ] H1 still correct with keyword
- [ ] H2 count still 5-8
- [ ] Keyword still in first 100 words, conclusion
- [ ] Meta title/description unchanged
- [ ] Keyword density still 1.5-2.5%
- [ ] Links still present (2+ internal, 3 max external)

---

## 🚨 CHECKPOINT: Final Validation Before Delivery

**⚠️ CRITICAL:** This is the FINAL GATE. Must pass before delivery.

### Run Master Validator (ALL CHECKS)

```bash
python scripts/style-enforcer.py final-draft.md "target keyword"
```

**This runs ALL four validations:**
1. Formatting validation
2. Readability scoring
3. Paragraph analysis
4. SEO validation

**ALL MUST PASS.**

**If ANY FAIL:**
- Review detailed reports
- Fix issues
- Re-run until ALL PASS
- DO NOT deliver until 100% pass rate

> **📚 See:** `references/validation-workflow.md` for detailed workflow

---

## Phase 4: Final Deliverables

### Format Final Markdown

Ensure:
- H1 title at top
- SEO Title and Meta Description included
- Proper heading hierarchy
- Line breaks between paragraphs
- Natural spacing (varied, not uniform)
- Bold headers throughout
- Bullet lists formatted correctly
- Tables formatted correctly
- Visual placeholders noted

### Create Publication Package

**Output files:**
1. `blog-post-[keyword]-[date].md` - Complete blog post
2. `metadata-[keyword]-[date].txt` - SEO metadata

**Metadata format:**
```
SEO Title: [50-60 chars]
SEO Meta Description: [150-160 chars]
Primary Keyword: [keyword]
Word Count: [X,XXX]
Internal Links: [X] - [URLs]
External Citations: [X] - [domains]
Formatting Score: [X]/100
Readability Score: [Flesch-Kincaid]
Variety Score: [X]/100
Publication Date: [TBD]
```

### Final Quality Verification

**Before delivery, confirm:**

**Content Quality:**
- [ ] Brief structure followed exactly
- [ ] Brand positioning clear (RevOps consultancy)
- [ ] All universal topics covered
- [ ] Content gaps filled

**Formatting (Script-Validated):**
- [ ] Paragraph variety: 1, 2, 3 sentence mix
- [ ] NO fat paragraphs (0 with 4+ sentences)
- [ ] Bullet sections: 8-12 minimum
- [ ] Visual placeholders: 2-4 minimum
- [ ] Tables: 1-2 for comparisons
- [ ] Bold headers: 8-12 minimum
- [ ] Sub-bullets: 3-5 instances

**Readability (Script-Validated):**
- [ ] Flesch Reading Ease: 60-70
- [ ] Grade Level: 8-10
- [ ] Average sentence: 15-20 words
- [ ] Complex words: <15%
- [ ] Passive voice: <10%

**SEO (Script-Validated):**
- [ ] Keyword in H1, opening, conclusion
- [ ] Keyword density: 1.5-2.5%
- [ ] H2 count: 5-8
- [ ] H3 count: 10+
- [ ] Meta title: 50-60 chars
- [ ] Meta description: 150-160 chars

**Scripts (All PASSED):**
- [ ] formatting-validator.py: PASS
- [ ] readability-scorer.py: PASS
- [ ] paragraph-analyzer.py: PASS
- [ ] seo-validation-helper.py: PASS
- [ ] style-enforcer.py: PASS (master check)

**✅ If all checked: READY FOR DELIVERY**

---

## Success Criteria

A blog post is successful when:

✅ **All scripts pass** (formatting, readability, SEO)
✅ **Variety score ≥80/100** (programmatically validated)
✅ **Flesch Reading Ease 60-70** (non-native accessible)
✅ **Brief followed exactly** (structure, requirements met)
✅ **No fat paragraphs** (0 with 4+ sentences)
✅ **Extensive bullets** (8-12 sections minimum)
✅ **Visual hierarchy** (bold headers, placeholders, tables)
✅ **Publication-ready** (zero additional editing needed)

---

## Common Mistakes (Prevented by Scripts)

**Script NOW catches:**
1. ❌ Fat paragraphs (4+ sentences) → Auto-reject
2. ❌ Too few bullets (<8 sections) → Fail
3. ❌ Poor variety (all 2-sentence paragraphs) → Fail
4. ❌ Low readability (grade >10) → Fail
5. ❌ Missing visuals (<2 placeholders) → Fail
6. ❌ Complex language (>15% complex words) → Fail

**These issues can NO LONGER slip through.**

---

## Quick Reference

**Guidelines:**
- `guidelines/MAN-DIGITAL-BRAND-CONTEXT.md` - Brand positioning
- `guidelines/Writing_guidelines.md` - Style and voice
- `guidelines/SEO_guidelines.md` - SEO patterns

**References:**
- `references/formatting-guide.md` - Visual good vs bad examples
- `references/readability-guide.md` - Non-native speaker techniques
- `references/paragraph-patterns.md` - Variety pattern library
- `references/validation-workflow.md` - How to use scripts
- `references/STRUCTURE-QUICK-REF.md` - Structure requirements

**Editing Checklists:**
- `editing-checklists/01_Editing_-_Edit_Checklist.md` - Master checklist (APPLY FIRST)
- `editing-checklists/02-11_*.md` - Additional frameworks

**Examples:**
- `examples/example-1-health-score.md` - Health scoring example (USE FOR SCROLL TEST)
- `examples/example-2-revops-framework.md` - RevOps framework
- `examples/example-3-ai-agents.md` - AI agents

**Scripts (MANDATORY):**
- `scripts/formatting-validator.py` - Validate variety, bullets, visuals
- `scripts/readability-scorer.py` - Validate accessibility
- `scripts/paragraph-analyzer.py` - Deep structure analysis
- `scripts/seo-validation-helper.py` - Validate SEO elements
- `scripts/style-enforcer.py` - Run ALL validations (FINAL GATE)

**Templates:**
- `brief-template.md` - Brief format reference

---

## Workflow Summary (Condensed)

```
Phase 0: Input Validation
  └─ Confirm brief + SEO research + content research received

Phase 1: Digestion (MANDATORY)
  └─ Review ALL inputs, create drafting plan
  └─ Time: 20-30 minutes

Phase 2: Drafting
  └─ Draft at target word count (1,200-1,600)
  └─ Paragraph variety (1, 2, 3 sentences)
  └─ Extensive bullets (8-12 sections)
  └─ Visual hierarchy (bold, placeholders, tables)
  └─ Write for non-native speakers (simple, clear)
  └─ Time: 60-90 minutes

CHECKPOINT 1: Run Validation Scripts (MANDATORY)
  ├─ formatting-validator.py → MUST PASS
  ├─ readability-scorer.py → MUST PASS
  └─ seo-validation-helper.py → MUST PASS
  └─ Fix issues, re-run until ALL PASS
  └─ Time: 15-30 minutes (including fixes)

Phase 3: Editing
  └─ Apply all 11 editing frameworks in order
  └─ Time: 45-60 minutes (15-20 min on framework 1 alone)

CHECKPOINT 2: Final Validation (MANDATORY)
  └─ style-enforcer.py final-draft.md "keyword"
  └─ Runs ALL four validations
  └─ ALL MUST PASS before delivery
  └─ Time: 15-20 minutes (including fixes)

Phase 4: Delivery
  └─ Format markdown
  └─ Create metadata file
  └─ Final verification checklist
  └─ Time: 10-15 minutes

TOTAL TIME: 3-4 hours per blog post
```

---

**Key Insight:** Previous outputs failed because instructions alone don't work. Scripts **enforce** requirements programmatically. Use them religiously.
