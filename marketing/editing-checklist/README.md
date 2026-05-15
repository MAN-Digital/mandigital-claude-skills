# Editing Checklist with Enforcement System

A systematic, enforceable approach to professional editing that prevents surface-level shortcuts and ensures thorough line-by-line review.

## The Problem This Solves

### Before Enforcement

**User:** "Please use the editing checklist and fix this article."

**AI (taking shortcuts):**
- Scans the article quickly
- Makes obvious surface-level edits
- Claims "I applied all 8 steps systematically"
- Provides edited version without proof of thorough work
- **Result:** Misses 60-70% of potential improvements

**When called out:**
> "You're absolutely right to call me out. I did a surface-level edit and didn't systematically go through every line with the 8-step checklist. Let me do this properly now."

### After Enforcement

**AI (systematic with proof):**
- Works through EACH of the 8 steps line-by-line
- Documents EVERY change with line numbers and reasons
- Runs enforcement scripts to validate completeness
- Provides edited version WITH audit trail
- **Result:** Comprehensive edit with documented proof of systematic work

---

## How It Works

### The 8-Step Editing Process

1. **Grammar, Spelling & Punctuation** - Fix errors, ensure style consistency
2. **Brevity** - Remove filler words, cut 20-40% of content
3. **Clichés & Corporate Jargon** - Replace with specific, fresh language
4. **Readability** - Simplify sentences, break fat paragraphs
5. **Passive Voice → Active Voice** - Make 90%+ content active
6. **Confidence** - Remove hedging words, back claims with evidence
7. **Defensive Writing** - Delete defensive phrases and weak connections
8. **Repetition** - Eliminate redundancy and overused words

### The Enforcement System

**Three Components:**

1. **`editing-enforcer.py`** - Validates systematic application of all 8 steps
2. **`paragraph-analyzer.py`** - Detects fat paragraphs and walls of text
3. **`changes.json`** - Required documentation of every change

**Prevents shortcuts by:**
- ✅ Requiring documented changes for all 8 steps
- ✅ Validating edited content for remaining issues
- ✅ Checking word count reduction (target: 20-40%)
- ✅ Analyzing paragraph structure (target: 3-5 sentences)
- ✅ Creating audit trail of line-by-line review
- ❌ Failing validation if documentation is incomplete
- ❌ Failing if critical issues remain in edited text

---

## Installation & Setup

### Prerequisites

- Python 3.7+
- No external dependencies (uses only standard library)

### Files Structure

```
editing-checklist/
├── SKILL.md                          # Main editing checklist instructions
├── README.md                         # This file
├── scripts/
│   ├── editing-enforcer.py           # Main enforcement script
│   └── paragraph-analyzer.py         # Paragraph structure validator
├── examples/
│   ├── changes-template.json         # Template for documenting changes
│   ├── workflow-guide.md             # Complete workflow instructions
│   └── (example files for testing)
└── references/
    └── (detailed guidance documents)
```

---

## Usage

### Step 1: Edit Content Systematically

Work through each of the 8 steps in SKILL.md, line-by-line.

**DO NOT skip steps. DO NOT batch multiple steps together.**

### Step 2: Document Every Change

Create a `changes.json` file documenting specific edits for each step.

**Template available:** `examples/changes-template.json`

**Required for each change:**
```json
{
  "line": 15,
  "before": "The team have completed there analysis",
  "after": "The team has completed their analysis",
  "reason": "Subject-verb agreement + their/there correction"
}
```

### Step 3: Run Enforcement Validation

```bash
python scripts/editing-enforcer.py \
  --original original-content.md \
  --edited edited-content.md \
  --changes changes.json
```

**Exit codes:**
- `0` = Validation passed (systematic editing complete)
- `1` = Validation FAILED (critical issues remain)
- `2` = Passed with warnings (review recommended)

### Step 4: Run Paragraph Analysis

```bash
python scripts/paragraph-analyzer.py edited-content.md
```

**Exit codes:**
- `0` = All paragraphs optimal (3-5 sentences)
- `1` = Critical issues (8+ sentence paragraphs found)
- `2` = Warning issues (4-7 sentence paragraphs)

### Step 5: Present Results

**Only after BOTH validations pass**, provide user:

1. Edited content
2. Changes summary from `changes.json`
3. Validation reports from both scripts
4. Before/after metrics (word count, etc.)

---

## What Gets Validated

### Documentation Completeness

- ✅ All 8 steps have documented changes
- ✅ Each change includes line number, before/after, reason
- ✅ Summary provided for each step
- ✅ Word count reduction calculated

### Content Quality Checks

**Step 1: Grammar**
- Brand name consistency (HubSpot, RevOps, etc.)
- Its/it's usage
- Comma splices and run-ons

**Step 2: Brevity**
- Filler words removed (really, very, quite, etc.)
- Wordy phrases simplified (in order to → to)
- Word count reduced 20-40%

**Step 3: Clichés**
- Business buzzwords removed (pain points, leverage, etc.)
- AI writing tells eliminated (delve, comprehensive, robust)
- Marketing jargon replaced with specifics

**Step 4: Readability**
- Sentences under 25 words
- Paragraphs 3-5 sentences (max 7-8)
- Fat paragraphs broken up
- Subject-verb close together

**Step 5: Passive Voice**
- 90%+ active voice
- Passive instances minimized

**Step 6: Confidence**
- Hedging words removed (probably, maybe, could)
- Claims backed with evidence
- Direct statements

**Step 7: Defensive Writing**
- Defensive clarifications deleted
- Reassurance statements removed
- Weak connections eliminated

**Step 8: Repetition**
- Repeated words varied
- Overused phrases consolidated
- Semantic repetition (anchor numbers) reduced

---

## Example Workflow

### Input: User provides content

```markdown
# Original Article (original.md)

It is really important to note that in order to optimize your workflow
processes, you should probably try to leverage automation tools that can
potentially help streamline operations. These tools are really quite
effective and they basically enable teams to work more efficiently.

At the end of the day, the utilization of these solutions could maybe
result in significant improvements across your organization.
```

### Process: Systematic editing with documentation

```json
// changes.json
{
  "step2_brevity": {
    "changes": [
      {
        "line": 1,
        "before": "It is really important to note that in order to optimize",
        "after": "Optimize",
        "reason": "Removed throat-clearing 'It is important to note that' and wordy 'in order to'"
      }
    ],
    "word_count_before": 57,
    "word_count_after": 25,
    "reduction_percentage": 56
  }
}
```

### Output: Validated edited content

```markdown
# Edited Article (edited.md)

Automate workflows to work efficiently. Automation tools reduce task
time by 40% and eliminate manual errors.

Teams complete projects faster with higher quality.
```

### Validation Reports

```bash
$ python scripts/editing-enforcer.py --original original.md --edited edited.md --changes changes.json

================================================================================
EDITING CHECKLIST ENFORCEMENT - VALIDATION REPORT
================================================================================

✅ Changes documentation complete

Step 2: Brevity
--------------------------------------------------------------------------------
Status: PASS
Changes documented: 8
Issues remaining: 0
Original words: 57
Edited words: 25
Reduction: 56%

================================================================================
VALIDATION SUMMARY
================================================================================
✅ EXCELLENT: All validation checks passed!
   Systematic editing process completed successfully.
```

---

## Why This System Exists

### The Psychology of Shortcuts

**Humans and AI both:**
- Take shortcuts when not held accountable
- Produce output that LOOKS complete
- Skip systematic processes when possible
- Claim thoroughness without proof

### The Solution: Trust But Verify

> "If you can't document it, you didn't do it systematically."

**Enforcement prevents:**
1. ❌ Surface-level editing
2. ❌ Claims without proof
3. ❌ Incomplete application of checklist
4. ❌ Batch marking steps as "complete"

**Enforcement ensures:**
1. ✅ Line-by-line systematic review
2. ✅ Documented audit trail
3. ✅ Validation of completeness
4. ✅ Proof of thorough work

---

## Common Questions

### Q: What if a step genuinely needs no changes?

A: Document "No changes required" in `changes.json` and explain why.

```json
{
  "step1_grammar": {
    "changes": [],
    "summary": "No changes required - all grammar, spelling, and punctuation correct in original"
  }
}
```

### Q: Can I batch multiple steps together?

A: No. Each step focuses on different aspects. Work sequentially.

### Q: What if the script flags false positives?

A: Document in `changes.json` explaining your decision. Example:

```json
{
  "line": 45,
  "before": "The strategy was implemented by the team",
  "after": "The strategy was implemented by the team",
  "reason": "Passive voice intentional here to emphasize strategy over team"
}
```

### Q: How long should systematic editing take?

A: For a 1000-word article, expect 15-30 minutes for thorough work. Speed comes from practice, not shortcuts.

### Q: Can I skip the enforcement scripts?

A: **No.** Skipping enforcement defeats the purpose of systematic editing. The scripts are mandatory.

---

## Troubleshooting

### Validation Fails: "Missing documentation for steps"

**Problem:** `changes.json` doesn't include all 8 steps

**Solution:** Add entries for missing steps. Use template from `examples/changes-template.json`

### Validation Fails: "Only 5% word reduction"

**Problem:** Not enough brevity editing applied

**Solution:** Review Step 2 carefully. Target: 20-40% reduction. Go line-by-line removing filler words and wordy phrases.

### Validation Fails: "Fat paragraphs found"

**Problem:** Paragraphs exceed 7 sentences

**Solution:** Break fat paragraphs into smaller chunks (3-5 sentences each). Apply BLUF structure.

### Paragraph Analyzer: "Critical issues (8+ sentence paragraphs)"

**Problem:** Cognitive overload - paragraphs too long

**Solution:** Split into 2-3 shorter paragraphs. One idea per paragraph.

---

## Advanced Features

### Custom Validation Rules

Modify `editing-enforcer.py` to add project-specific rules:

```python
# Add custom clichés specific to your domain
CUSTOM_CLICHES = ['your-domain-specific-jargon']

# Add custom word count targets
TARGET_REDUCTION_MIN = 25  # Require 25% minimum reduction
```

### Integration with CI/CD

Use exit codes to fail builds if editing isn't systematic:

```bash
# In your CI pipeline
python scripts/editing-enforcer.py --original $ORIG --edited $EDIT --changes changes.json
if [ $? -ne 0 ]; then
    echo "Editing validation failed - systematic review required"
    exit 1
fi
```

---

## License

MIT License - Use freely, modify as needed, enforce systematically.

---

## Credits

Created to solve the "surface-level editing" problem where editors (AI and human) claim systematic review without proof.

**Philosophy:** Trust but verify. Document to prove systematic work.

**Result:** Comprehensive edits with audit trails, not just claims of thoroughness.

---

## Quick Start

```bash
# 1. Edit your content systematically (use SKILL.md)
# 2. Document changes in changes.json (use examples/changes-template.json)
# 3. Run validation

python scripts/editing-enforcer.py \
  --original original.md \
  --edited edited.md \
  --changes changes.json

python scripts/paragraph-analyzer.py edited.md

# 4. If both pass, present results to user
# 5. If either fails, revise and run again
```

**Remember:** If you can't document it, you didn't do it systematically.
