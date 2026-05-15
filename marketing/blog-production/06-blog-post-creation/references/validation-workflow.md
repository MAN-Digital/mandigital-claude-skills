# Validation Workflow: Using the Scripts

## Purpose

This guide explains **when and how** to use each validation script in the blog post creation workflow.

---

## The Four Validation Scripts

| Script | Purpose | When to Run | Pass/Fail Gate |
|--------|---------|-------------|----------------|
| `formatting-validator.py` | Paragraph variety, bullets, visuals, tables | After drafting | ✅ Must pass |
| `readability-scorer.py` | Flesch-Kincaid, sentence length, complexity | After drafting | ✅ Must pass |
| `paragraph-analyzer.py` | Deep paragraph structure analysis | After drafting | ✅ Must pass |
| `seo-validation-helper.py` | Keywords, headings, meta elements | After drafting + After editing | ✅ Must pass |
| `style-enforcer.py` | Runs ALL above scripts | Final check before delivery | ✅ MUST PASS |

---

## Workflow Integration Points

### Checkpoint 1: After Drafting (Phase 2.8)

**Status:** Draft complete, before editing starts

**Run:**
```bash
python scripts/formatting-validator.py draft.md
```

**What it checks:**
- Paragraph variety (1, 2, 3 sentence distribution)
- Fat paragraphs (4+ sentences - auto-reject)
- Bullet sections (need 8-12 minimum)
- Visual placeholders (need 2-4 minimum)
- Tables (recommend 1-2)
- Bold headers (need 8-12 minimum)
- Sub-bullets (need 3-5 instances)

**If FAIL:**
- Fix issues immediately
- Don't proceed to editing
- Re-run until PASS

**Common fixes:**
- Break up fat paragraphs (4+ sentences)
- Add more 1-sentence paragraphs (need 10-15)
- Add more bullet sections (need 8-12)
- Insert visual placeholders ([Screenshot: ...])
- Add bold headers for hierarchy

---

### Checkpoint 2: Readability Check (Phase 2.8)

**Status:** Draft complete, checking accessibility

**Run:**
```bash
python scripts/readability-scorer.py draft.md
```

**What it checks:**
- Flesch Reading Ease (target: 60-70)
- Flesch-Kincaid Grade Level (target: 8-10)
- Average sentence length (target: 15-20 words)
- Complex words (target: <15%)
- Passive voice (target: <10%)
- Long sentences (target: <20% over 25 words)

**If FAIL:**
- Simplify vocabulary
- Break up long sentences
- Convert passive to active voice
- Use shorter words
- Re-run until PASS

**Common fixes:**
- Replace complex words: "utilize" → "use"
- Split sentences >25 words
- Change passive to active voice
- Use simple sentence structures

---

### Checkpoint 3: SEO Validation (Phase 3)

**Status:** After drafting, before editing

**Run:**
```bash
python scripts/seo-validation-helper.py draft.md "target keyword"
```

**What it checks:**
- H1 heading (one only, includes keyword)
- H2 headings (5-8 count, keyword variations)
- H3 headings (10+ for depth)
- Keyword placement (H1, first 100 words, conclusion)
- Keyword density (1.5-2.5%)
- Meta title (50-60 chars, has keyword)
- Meta description (150-160 chars, has keyword + CTA)
- Word count (1,200-1,600 range)
- Links (2+ internal, 3 max external)

**If FAIL:**
- Fix SEO issues before editing
- Don't let editing break SEO later
- Re-run until PASS

---

### Checkpoint 4: After Editing (Phase 4.11.5)

**Status:** All editing complete, final check

**Run:**
```bash
python scripts/style-enforcer.py final-draft.md "target keyword"
```

**What it does:**
- Runs ALL four validation scripts
- Produces comprehensive PASS/FAIL report
- Final gate before delivery

**Scripts run in sequence:**
1. Formatting validation
2. Readability scoring
3. Paragraph analysis
4. SEO validation

**ALL must PASS.**

**If ANY FAIL:**
- Review detailed report for each failure
- Fix issues
- Re-run style-enforcer.py
- Repeat until ALL PASS

---

## Interpreting Results

### Formatting Validator Output

```
🎯 OVERALL VARIETY SCORE
Score: 85/100 - Grade: B (Good)

Breakdown:
  • Paragraph variety: 30 points
  • Bullets: 15 points
  • Visuals: 10 points
  • Tables: 10 points
  • Bold headers: 15 points
  • Sub bullets: 7 points

🚨 FAT PARAGRAPHS CHECK (CRITICAL)
✅ No fat paragraphs (all 3 sentences or less)

📝 PARAGRAPH VARIETY
Distribution (total: 42 paragraphs):
  • One sentence: 12 (28.6%)
  • Two sentence: 23 (54.8%)
  • Three sentence: 7 (16.7%)
  • Four plus: 0 (0.0%)

🔸 BULLET SECTIONS
✅ 10 bullet sections (excellent!)
```

**How to read:**
- ✅ = Pass
- ⚠️ = Warning (acceptable but could improve)
- ❌ = Fail (must fix)

**Action required if:**
- Variety score <70
- Any fat paragraphs (4+ sentences)
- Bullet sections <8
- Visual placeholders <2

---

### Readability Scorer Output

```
🎯 OVERALL ASSESSMENT
✅ Overall: Excellent (5/6 passed)
Non-Native Friendly: ✅ YES

📖 FLESCH READING EASE
✅ Flesch Reading Ease: 67.3 (Easy - 9th-10th grade)
  Score: 67.3/100 (target: 60-70)

🎓 FLESCH-KINCAID GRADE LEVEL
✅ Grade Level: 9.2 (target: 8-10)

📏 SENTENCE LENGTH
✅ Average sentence length: 17.4 words (target: 15-20)
  Distribution:
    • Short (1-10 words): 15
    • Medium (11-20 words): 28
    • Long (21-30 words): 8
    • Very Long (30+ words): 2

📚 WORD COMPLEXITY
✅ Complex words: 12.3% (target: <15%)

🗣️  PASSIVE VOICE
✅ Passive voice: 7.1% (target: <10%)
```

**How to read:**
- Target ranges shown for each metric
- Pass = within target
- Fail = outside target

**Action required if:**
- Flesch Reading Ease <60
- Grade Level >10
- Complex words >15%
- Passive voice >10%
- Long sentences >20%

---

### Style Enforcer Output

```
🎨 Running Formatting Validation...
[Full formatting validation output]

📖 Running Readability Scorer...
[Full readability output]

📝 Running Paragraph Analyzer...
[Full paragraph analysis output]

🔍 Running SEO Validator...
[Full SEO validation output]

================================================================================
FINAL COMPREHENSIVE REPORT
================================================================================

📋 VALIDATION CHECK RESULTS
✅ Formatting Validation: PASSED
✅ Readability Score: PASSED
✅ Paragraph Analysis: PASSED
✅ SEO Validation: PASSED

================================================================================
OVERALL STATUS
================================================================================
Checks Passed: 4/4

🎉 SUCCESS: ALL VALIDATIONS PASSED

✅ Blog post is ready for delivery!
```

**If ALL PASS:**
- ✅ Proceed to delivery
- Article is publication-ready

**If ANY FAIL:**
- ❌ DO NOT deliver
- Review each failed check's detailed report
- Fix issues
- Re-run until all pass

---

## Common Failure Patterns & Fixes

### Failure: Fat Paragraphs

**Output:**
```
❌ CRITICAL: 5 paragraphs have 4+ sentences (auto-reject)

Fat paragraphs that need breaking up:
  📍 Line 23: 5 sentences
     Preview: Organizations implementing AI-powered customer service...
     Suggestion: Break into 3 paragraphs
```

**Fix:**
1. Go to line 23
2. Identify the 5 sentences
3. Break into 2-3 shorter paragraphs
4. Use bullets if listing items
5. Re-run validator

---

### Failure: Low Bullet Count

**Output:**
```
❌ Only 4 bullet sections (need minimum 8)
```

**Fix:**
1. Find 4-5 places where you're listing things in prose
2. Convert to bullet sections
3. Add bold headers before bullets
4. Example: "Key benefits:" followed by bullets
5. Re-run validator

---

### Failure: Poor Readability

**Output:**
```
❌ Flesch Reading Ease: 48.2 (Difficult - College)
❌ Average sentence length: 28.7 words (target: 15-20)
```

**Fix:**
1. Find all sentences >25 words
2. Break each into 2-3 shorter sentences
3. Replace complex words with simple ones
4. Convert passive to active voice
5. Re-run validator

---

### Failure: Missing SEO Elements

**Output:**
```
❌ Keyword density 0.8% (low). Consider adding more mentions.
⚠️ Keyword not in conclusion
```

**Fix:**
1. Add keyword mentions throughout article
2. Ensure keyword appears in:
   - H1 heading
   - First 100 words
   - 2-3 H2 headings
   - Conclusion paragraph
3. Re-run validator

---

## Iteration Workflow

### Standard Iteration Loop

```
1. Draft → Run formatting-validator.py
   └─ FAIL → Fix issues → Repeat step 1
   └─ PASS → Continue to step 2

2. Draft → Run readability-scorer.py
   └─ FAIL → Simplify → Repeat step 2
   └─ PASS → Continue to step 3

3. Draft → Run seo-validation-helper.py
   └─ FAIL → Fix SEO → Repeat step 3
   └─ PASS → Continue to step 4

4. Begin editing (all 11 frameworks)

5. Final draft → Run style-enforcer.py
   └─ FAIL → Review reports → Fix → Repeat step 5
   └─ PASS → READY FOR DELIVERY
```

---

## Time Estimates

| Script | Typical Runtime | Interpretation Time |
|--------|----------------|---------------------|
| formatting-validator.py | 2-3 seconds | 2-5 minutes |
| readability-scorer.py | 2-3 seconds | 3-5 minutes |
| paragraph-analyzer.py | 2-3 seconds | 3-5 minutes |
| seo-validation-helper.py | 2-3 seconds | 2-3 minutes |
| style-enforcer.py | 10-15 seconds | 10-15 minutes |

**Total validation time:** ~30 minutes including fixes

---

## Command Reference

### Individual Scripts

```bash
# Formatting validation
python scripts/formatting-validator.py draft.md

# Readability scoring
python scripts/readability-scorer.py draft.md

# Paragraph analysis
python scripts/paragraph-analyzer.py draft.md

# SEO validation
python scripts/seo-validation-helper.py draft.md "target keyword"
```

### Master Script

```bash
# Run ALL validations (use before delivery)
python scripts/style-enforcer.py final-draft.md "target keyword"
```

### Quick Check (Formatting Only)

```bash
# Fast check during drafting
python scripts/formatting-validator.py draft.md
```

---

## Best Practices

### 1. Run Early and Often

Don't wait until the end. Run formatting-validator.py during drafting to catch issues early.

### 2. Fix Issues Immediately

Don't accumulate failures. Fix each issue as you find it.

### 3. Use Sequential Validation

Run formatting → readability → SEO in that order. Don't skip ahead.

### 4. Document Patterns

Note which failures you encounter repeatedly. Create checklist to avoid them.

### 5. Trust the Scripts

If a script says FAIL, don't ignore it. The output users complained about happened because scripts weren't being run.

---

## Troubleshooting

### Script Not Found

```bash
python scripts/formatting-validator.py draft.md
# Error: No such file or directory
```

**Fix:** Ensure you're in the blog-post-creation skill directory.

### File Not Found

```bash
python scripts/formatting-validator.py draft.md
# Error: File 'draft.md' not found
```

**Fix:** Check file path. Use absolute path if needed:
```bash
python scripts/formatting-validator.py /full/path/to/draft.md
```

### Python Not Found

```bash
python scripts/formatting-validator.py draft.md
# Command not found: python
```

**Fix:** Try `python3` instead:
```bash
python3 scripts/formatting-validator.py draft.md
```

---

## Key Takeaways

1. **Run scripts at checkpoints** - After drafting, after editing
2. **ALL must pass** - One failure = not ready
3. **Fix immediately** - Don't accumulate issues
4. **Style enforcer is final gate** - Must pass before delivery
5. **Trust the tools** - They catch what instructions miss

**Remember:** The user's complaints happened because scripts weren't being run. Use them religiously.
