# Editing Checklist Enforcement Workflow

## Why This System Exists

**Problem:** AI takes shortcuts by doing surface-level edits instead of systematically applying the 8-step checklist line-by-line.

**Solution:** Enforcement scripts that validate systematic application and require documented proof of changes for each step.

---

## The Systematic Editing Process

### Step 1: Start with Original Content

User provides content that needs editing. Save this as the original file.

```bash
# User provides: original-content.md
```

### Step 2: Apply the 8-Step Checklist Systematically

**CRITICAL:** You MUST go through each step methodically, line-by-line. No shortcuts.

**For each step:**
1. Read the step instructions in SKILL.md
2. Go through EVERY LINE of the content
3. Apply that specific step's rules
4. Document EVERY change you make in changes.json

**The 8 Steps:**
1. Grammar, Spelling & Punctuation
2. Brevity (Omit Needless Words)
3. Clichés & Corporate Jargon
4. Readability (Simplify Convoluted Sentences)
5. Passive Voice → Active Voice
6. Confidence (Remove Hedging Words)
7. Defensive Writing & Content Deletion
8. Repetition Removal

### Step 3: Document Every Change

As you edit, populate a `changes.json` file following the template in `examples/changes-template.json`.

**Required for each change:**
- Line number or paragraph reference
- Before text (what it was)
- After text (what it became)
- Reason (why you made this change)

**Example:**
```json
{
  "step2_brevity": {
    "description": "Step 2: Brevity (Omit Needless Words)",
    "changes": [
      {
        "line": 12,
        "before": "In order to facilitate the implementation",
        "after": "To implement",
        "reason": "Replaced wordy phrase 'in order to' → 'to', replaced 'facilitate the implementation' with strong verb 'implement'"
      }
    ],
    "summary": "Reduced word count by 32%..."
  }
}
```

### Step 4: Save Edited Content

Save your edited content as a separate file.

```bash
# You create: edited-content.md
```

### Step 5: Run the Enforcement Script

**MANDATORY:** Before claiming editing is complete, run the enforcement script:

```bash
python scripts/editing-enforcer.py \
  --original original-content.md \
  --edited edited-content.md \
  --changes changes.json
```

**The script will:**
- ✅ Validate you documented changes for all 8 steps
- ✅ Check edited content for remaining issues
- ✅ Compare word counts, sentence lengths, etc.
- ✅ Flag any problems requiring attention
- ❌ FAIL if documentation is incomplete
- ❌ FAIL if critical issues remain

### Step 6: Run Paragraph Analysis (Step 4 Validation)

Additionally, run the paragraph analyzer to validate Step 4 (readability):

```bash
python scripts/paragraph-analyzer.py edited-content.md
```

This detects:
- Fat paragraphs (4+ sentences)
- Walls of text (150+ words)
- Lack of variety
- Cognitive overload issues

### Step 7: Present Results to User

**Only after validation passes**, present:

1. **Original Text** (for reference)
2. **Edited Text** (your final version)
3. **Key Changes Summary** (from changes.json)
4. **Validation Report** (from enforcement script)
5. **Paragraph Analysis** (from paragraph-analyzer script)

---

## Workflow Example

```bash
# Step 1: User provides content
original-content.md

# Step 2-3: You edit systematically and document changes
# (Manual work: go through 8 steps line-by-line)
edited-content.md
changes.json

# Step 4: Validate your work
python scripts/editing-enforcer.py \
  --original original-content.md \
  --edited edited-content.md \
  --changes changes.json

# Step 5: Validate paragraphs
python scripts/paragraph-analyzer.py edited-content.md

# Step 6: Present results
# Only if both validations pass!
```

---

## What Gets Validated

### Documentation Validation
- ✅ All 8 steps documented
- ✅ Specific changes listed for each step
- ✅ Line numbers and reasons provided
- ✅ Before/after examples given

### Content Validation
- ✅ Grammar issues resolved
- ✅ 20-40% word count reduction achieved
- ✅ Clichés removed
- ✅ Sentences under 25 words
- ✅ Paragraphs under 7 sentences
- ✅ Passive voice minimized
- ✅ Hedging words removed
- ✅ Defensive phrases deleted
- ✅ Repetition eliminated

---

## Exit Codes

**editing-enforcer.py:**
- `0` = Validation passed, systematic editing complete
- `1` = Validation FAILED, critical issues remain
- `2` = Validation passed with warnings

**paragraph-analyzer.py:**
- `0` = All paragraphs optimal (3-5 sentences)
- `1` = Critical issues (8+ sentence paragraphs)
- `2` = Warning issues (4-7 sentence paragraphs)

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Surface-Level Editing
**Problem:** Quick pass without systematic review
**Solution:** Go through EVERY LINE for EACH of the 8 steps

### ❌ Mistake 2: Incomplete Documentation
**Problem:** "I made some changes" without specifics
**Solution:** Document EVERY change with line numbers and reasons

### ❌ Mistake 3: Skipping Validation
**Problem:** Claiming editing is complete without running scripts
**Solution:** ALWAYS run both enforcement and paragraph scripts

### ❌ Mistake 4: Batch Completion
**Problem:** Marking all 8 steps complete at once
**Solution:** Work through steps sequentially, document as you go

### ❌ Mistake 5: Assuming No Changes Needed
**Problem:** "Text was already good, no changes"
**Solution:** EVERY text has improvement opportunities. Find them.

---

## Why This Prevents Shortcuts

**Before (Surface-Level):**
- AI scans text quickly
- Makes obvious fixes
- Claims "I applied all 8 steps"
- No proof of systematic review
- User receives incomplete edit

**After (Enforced Systematic):**
- AI MUST document specific changes
- Script validates changes for each step
- No completion without validation passing
- Proof of line-by-line review required
- User receives comprehensive edit

---

## Questions?

**Q: What if a step genuinely needs no changes?**
A: Explicitly document "No changes required" and explain why in the changes.json file.

**Q: Can I batch multiple steps together?**
A: No. Each step focuses on different aspects. Work sequentially.

**Q: What if the enforcement script flags false positives?**
A: Review the flagged items. If they're intentional (e.g., passive voice for emphasis), document in changes.json explaining the decision.

**Q: How long should this take?**
A: For a 1000-word article, expect 15-30 minutes for thorough systematic editing. Speed comes from practice, not shortcuts.

---

## Enforcement Philosophy

> "If you can't document it, you didn't do it systematically."

The enforcement scripts exist because:
1. Humans (and AI) naturally take shortcuts
2. Surface-level edits LOOK complete but miss issues
3. Systematic processes catch what casual review misses
4. Documentation proves the work was done thoroughly

**Trust but verify.** The scripts verify.
