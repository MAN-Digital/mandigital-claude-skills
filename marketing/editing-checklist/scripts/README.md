# Editing Checklist Scripts

## paragraph-analyzer.py

Automated fat paragraph detection and paragraph structure analysis for the editing checklist workflow.

### Purpose

Detects fat paragraphs (4+ sentences) that create cognitive overload and reduce readability. Helps ensure compliance with Step 4 of the editing checklist (Readability - Paragraph Structure).

### Usage

```bash
python scripts/paragraph-analyzer.py your-edited-file.md
python scripts/paragraph-analyzer.py your-edited-file.txt
```

### What It Checks

1. **Fat Paragraphs (4+ sentences)**
   - Warning: 4-7 sentences (longer than optimal)
   - Critical: 8+ sentences (cognitive overload)

2. **Walls of Text (150+ words)**
   - Identifies dense paragraphs that create visual intimidation

3. **Paragraph Variety**
   - Checks for monotonous paragraph lengths
   - Ensures mix of 1-3 sentence paragraphs

4. **Visual Breakdown**
   - Shows first 30 paragraphs with visual bars
   - Easy to spot problematic patterns at a glance

### Exit Codes

- `0` = All paragraphs optimal (3-5 sentences)
- `1` = Critical issues (8+ sentence paragraphs found)
- `2` = Warning issues (4-7 sentence paragraphs found)

### Example Output

```
================================================================================
PARAGRAPH STRUCTURE ANALYSIS - Editing Checklist
================================================================================

📊 PARAGRAPH DISTRIBUTION
Total paragraphs analyzed: 5

Distribution by sentence count:
  • 2 sentence     :   2 ( 40.0%)
  • 3 sentence     :   1 ( 20.0%)
  • 8 plus         :   2 ( 40.0%) ❌ CRITICAL

🚫 FAT PARAGRAPH DETECTION (4+ SENTENCES)
❌ 2 fat paragraphs found (2 critical)

Critical (8+):       2 paragraphs
Warning (4-7):       0 paragraphs

Fat paragraphs that need breaking up:
  🚨 Line 9: 8 sentences, 98 words
  🚨 Line 13: 9 sentences, 91 words

💡 IMPROVEMENT SUGGESTIONS
1. 🚨 [CRITICAL] Break up extremely long paragraphs (8+ sentences)
   Tip: Split into 2-3 shorter paragraphs. One idea per paragraph.
```

### Integration with Editing Workflow

Run this script as part of Step 4 (Readability) to verify paragraph structure before finalizing edits:

1. Complete editing steps 1-7
2. Run paragraph analyzer
3. Fix any fat paragraphs detected
4. Re-run to verify compliance
5. Proceed with final quality checks

### Optimal Paragraph Structure

Based on Editing Checklist Step 4 guidelines:

- **Optimal:** 3-5 sentences per paragraph
- **Maximum:** 7-8 sentences (cognitive load threshold)
- **Target:** 75-100 words per paragraph
- **Critical:** 8+ sentences = immediate action required

### Related Files

- `SKILL.md` - Step 4.8: Paragraph Structure and Density
- `references/paragraph-structure-guide.md` - Comprehensive theory and examples
- `references/readability-masterclass.md` - Sentence-level guidance
