# Script 04: Parallelism Check

## Purpose
Ensure list structure consistency across bullet lists and comma-separated lists in sentences.

## When to Use
- After completing Script 01 (Master Edit Checklist)
- When article has multiple bullet lists or enumerated items
- Before final polish

## Time Expectation
4-6 minutes for a 1,500-word article

## Prerequisites
- Article with bullet lists or comma-separated lists
- Understanding of parallel structure principles

---

## Instructions

⚠️ **CRITICAL: SLOW DOWN. This is Framework 4 of 11 - Be THOROUGH** ⚠️

**MANDATORY APPROACH:**
- 🕐 **Time expectation:** 4-6 minutes for this framework on a 1,500-word article
- 🔍 **Check EVERY bullet list** for parallel structure
- 💭 **Check EVERY comma-separated list** in sentences
- 📍 **Expected findings:** 5-10 parallelism issues minimum
- ✅ **Focus areas:** Bullet sections (you have 8-12 of them!), lists in sentences, sub-bullets

**If you finish in under 2 minutes, you RUSHED. Go back and look harder.**

---

## Critical Patterns to Find

### In Bullet Lists
- All start with same part of speech (verbs, nouns, adjectives)
- All use same tense if verbs
- All have similar structure
- Example issue: "Maintains consistency, learns what resonates, transforms dates, applies strategies"
- Example fix: "Maintains consistency, learns patterns, transforms dates, applies strategies" (all verbs + objects)

### In Comma-Separated Lists
- Same grammatical structure throughout
- Example issue: "quick, efficient, and helps save time"
- Example fix: "quick, efficient, and time-saving" (all adjectives)

### Common Parallelism Breaks
- Mixing verb forms: "writing, to edit, and revise"
- Mixing parts of speech: "quickly, efficient, and with accuracy"
- Inconsistent article use: "a plan, strategy, and a timeline"
- Mixed structures in bullets: Some start with verbs, others with nouns

---

## Parallelism Framework

### What is Parallelism?

Parallelism maintains consistent grammatical form. Think of it as rhythm in music. When a song flows seamlessly, it's pleasing to the ear. The same applies to writing. When writing lacks rhythm, flow, emphasis, it's not just grammatically incorrect—it creates a poor reading experience.

"Give a person a fish and you feed them for a day; teach a person to fish and you feed them for a lifetime."

Do you feel the balance? It's an intentional pattern. Parallelism creates balance and emphasis on similar things.

---

## Five Common Ways to Use Parallelism

### 1. When elements are joined by coordinating conjunctions ("and", "but", "or", etc.)

✅ **Parallel:** I like running and listening to music.
❌ **Not parallel:** I like running and to listen to music.

"To listen" is the infinitive form, whereas "running" is the gerund. They must match in type.

---

### 2. Lists or series

✅ **Parallel:**
Make sure to answer:
- Why it matters
- What they can do
- How to use it

❌ **Not parallel:**
Make sure to answer:
- Why it matters
- How will they do it?

"How will they do it?" is interrogative form, whereas "Why it matters" is positive form. They must match.

---

### 3. Comparisons

✅ **Parallel:** Trying and failing is better than not trying at all.
❌ **Not parallel:** Trying and failing is better than not to try at all.

The second part must match the first part's structure.

---

### 4. Linking verbs

✅ **Parallel:** The secret is to build trust.
❌ **Not parallel:** To write well is building trust.

The infinitive is incorrectly followed by a gerund. Balance both sides of the linking verb.

---

### 5. Correlative conjunctions

✅ **Parallel:** The dog is either sleeping or snoring.
❌ **Not parallel:** The dog is either sleeping or she is snoring.

"She is" is unnecessary and breaks parallelism.

---

## Common Mistake: Bulleted Lists

**The most common mistake occurs with bulleted lists** because writers structure the list without checking if items are parallel.

**Example:**
Avoid these three mistakes:
- Reading the email but not responding
- Forgetting to share posts
- When you quote inaccurate sources

**Problem:** Third item ("When you quote...") breaks parallelism. It should match the gerund form of the first two items.

**Fixed:**
Avoid these three mistakes:
- Reading emails without responding
- Forgetting to share posts
- Quoting inaccurate sources

---

## Output Format

For each parallelism issue you detect, return it in the following format:

```
1 - [very short title or description of the issue]
Location: [line number or paragraph number]
Issue: [short description of what is there and what is missing or could be improved]
Suggestion: [concise one-line explanation of how to fix parallelism, written in the writer's own writeprint/voice/style]

2 - [very short title or description of the issue]
Location: [line number or paragraph number]
Issue: [short description]
Suggestion: [concise explanation]

[Continue same pattern...]
```

---

## Edit Constraints

- If there are no issues, say so.
- If there are multiple issues, say so.
- You may use **bolding** in the Issue section to highlight specific words
- "Location", "Issue" and "Suggestion" must be present for each finding
- Suggestions must match the user's writing style

---

## Success Criteria

- [ ] Checked ALL bullet lists
- [ ] Checked ALL comma-separated lists in sentences
- [ ] Found minimum 5-10 parallelism issues (for 1,500-word article with multiple lists)
- [ ] Output format matches specification
- [ ] Suggestions maintain writer's voice and style

---

**Remember:** Parallelism creates rhythm and flow. When elements are balanced grammatically, reading becomes effortless and engaging.
