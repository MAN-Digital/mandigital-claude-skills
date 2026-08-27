# Readability Guide: Writing for Non-Native English Speakers

## Purpose

This guide ensures content is accessible to non-native English speakers through simple language, clear structure, and readability best practices.

---

## Core Principle

**Write for clarity, not cleverness.**

Non-native speakers need:
- Short sentences (15-20 words average)
- Simple vocabulary
- Active voice
- Clear structure
- Logical flow

---

## Target Metrics

Use `readability-scorer.py` to validate these targets:

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Flesch Reading Ease | 60-70 | "Easy" for 9th-10th graders |
| Flesch-Kincaid Grade | 8-10 | Middle school reading level |
| Average Sentence Length | 15-20 words | Short enough to follow |
| Complex Words (<3 syllables) | <15% | Simple vocabulary |
| Passive Voice | <10% | Active is clearer |
| Long Sentences (>25 words) | <20% | Avoid run-ons |

---

## Simple Language Principles

### 1. Use Short Sentences (15-20 words average)

#### ❌ BAD (34 words)

```markdown
Organizations implementing AI-powered customer service achieve 3.5x–8x ROI with positive returns within 8–14 months, according to research from Zendesk, making the business case rest on operational efficiency, customer experience improvement, and cost reduction.
```

**Problems:**
- 34 words = too long
- Complex structure
- Multiple clauses
- Hard to parse

#### ✅ GOOD (Average 15 words)

```markdown
Organizations using AI customer service achieve 3.5x–8x ROI. Positive returns appear within 8–14 months (Source: Zendesk). The business case rests on three factors: operational efficiency, customer experience, and cost reduction.
```

**Why better:**
- 3 sentences: 8, 10, 15 words
- Simple structure
- Easy to follow
- Clear points

---

### 2. Choose Simple Words Over Complex Ones

#### ❌ BAD (Complex)

```markdown
Organizations must operationalize comprehensive methodologies to facilitate implementation and optimize utilization of automated conversational interfaces while simultaneously mitigating potential complications.
```

**Problems:**
- "operationalize" → use "use"
- "comprehensive methodologies" → use "complete methods"
- "facilitate implementation" → use "help implement"
- "optimize utilization" → use "get the most from"
- "mitigating potential complications" → use "avoiding problems"

#### ✅ GOOD (Simple)

```markdown
Organizations should use complete methods to implement chatbots and get the most value while avoiding problems.
```

**Simplification table:**

| Complex Word | Simple Alternative |
|--------------|-------------------|
| utilize | use |
| facilitate | help |
| implement | set up, start |
| optimize | improve |
| mitigate | reduce, avoid |
| comprehensive | complete, full |
| methodologies | methods, ways |
| operationalize | use, apply |
| leverage | use |
| synergy | teamwork |

---

### 3. Use Active Voice (Not Passive)

#### ❌ BAD (Passive)

```markdown
The tickets are handled by the AI agent. Responses are generated automatically. Escalations are routed by the system to human agents when confidence is dropped below the threshold.
```

**Problems:**
- Passive voice confuses who does what
- Wordy
- Unclear actors

#### ✅ GOOD (Active)

```markdown
The AI agent handles tickets. It generates responses automatically. The system routes escalations to human agents when confidence drops below the threshold.
```

**Active voice pattern:**
- Subject → Verb → Object
- "The agent does X" (not "X is done by the agent")
- Clear who does what

---

### 4. Break Complex Ideas Into Simple Steps

#### ❌ BAD (Complex)

```markdown
To implement customer health scoring, identify key signals across four pillars—product usage and behavior, engagement, customer feedback, and account health—then assign weights totaling 100 points based on predictive value for retention and expansion while setting clear green/yellow/red thresholds that trigger automated workflows and human interventions.
```

**Problems:**
- 45 words = way too long
- Multiple nested ideas
- Hard to follow
- Non-native speakers lost

#### ✅ GOOD (Step-by-Step)

```markdown
To implement customer health scoring:

**Step 1:** Identify key signals across four areas:
- Product usage
- Engagement
- Customer feedback
- Account health

**Step 2:** Assign weights that total 100 points. Base weights on what predicts retention and expansion.

**Step 3:** Set clear thresholds:
- Green = healthy
- Yellow = needs attention
- Red = at risk

**Step 4:** Create automated workflows for each status.
```

**Why better:**
- Numbered steps = easy to follow
- Bullets = scannable
- Short sentences
- Clear progression

---

### 5. Avoid Idioms and Cultural References

#### ❌ BAD (Idioms)

```markdown
This isn't rocket science, but you can't just wing it. Get your ducks in a row before diving in headfirst. Don't put the cart before the horse, and remember: Rome wasn't built in a day.
```

**Problems:**
- "rocket science" → confusing
- "wing it" → unclear
- "ducks in a row" → what?
- "cart before horse" → huh?
- Non-native speakers: lost

#### ✅ GOOD (Direct)

```markdown
This is straightforward, but you need a plan. Organize your approach before you start. Follow the correct order. Remember: good implementations take time.
```

**Idioms to avoid:**

| Avoid | Use Instead |
|-------|-------------|
| rocket science | difficult/complex |
| wing it | improvise/do without planning |
| ducks in a row | organized |
| cart before horse | wrong order |
| ballpark figure | rough estimate |
| low-hanging fruit | easy wins |
| move the needle | make progress |
| circle back | return to this |

---

## Sentence Structure Patterns

### Pattern 1: Simple (Subject + Verb + Object)

```markdown
The agent handles tickets.
Teams save time.
Customers receive instant responses.
```

**Best for:** Facts, quick points

### Pattern 2: Compound (Two simple sentences + connector)

```markdown
The agent handles routine tickets, and humans focus on complex issues.
Customers get instant answers, so satisfaction improves.
```

**Best for:** Showing relationships

### Pattern 3: Complex (Main idea + supporting detail)

```markdown
When confidence drops below 70%, the system routes tickets to human agents.
Organizations see 50% ticket reduction because AI handles routine questions.
```

**Best for:** Explanations (use sparingly)

**Rule:** Mix all three, but keep Pattern 3 under 20 words.

---

## Readability Before/After Examples

### Example 1: Product Description

#### ❌ BAD (Flesch-Kincaid: Grade 14, Score: 35)

```markdown
HubSpot's sophisticated conversational artificial intelligence paradigm facilitates autonomous resolution of multifaceted customer inquiries through contextualized natural language processing while simultaneously maintaining contextual continuity across disparate communication channels and implementing conditional escalation protocols predicated upon algorithmic confidence thresholds.
```

**Problems:**
- Grade 14 = college graduate level
- Score 35 = very difficult
- 40+ words
- Complex vocabulary

#### ✅ GOOD (Flesch-Kincaid: Grade 8, Score: 68)

```markdown
HubSpot's AI handles customer questions automatically. It understands natural language and keeps context when customers switch channels. When confidence drops below a threshold, it routes to humans.
```

**Why better:**
- Grade 8 = middle school level
- Score 68 = easy
- 3 short sentences
- Simple words

---

### Example 2: Process Explanation

#### ❌ BAD (Flesch-Kincaid: Grade 13, Score: 40)

```markdown
The implementation methodology necessitates comprehensive assessment of organizational readiness parameters, including but not limited to data infrastructure maturity, process documentation completeness, and stakeholder alignment across functional silos, prior to initiating technical configuration activities.
```

**Problems:**
- Grade 13 = college level
- Score 40 = difficult
- 35 words
- Jargon-heavy

#### ✅ GOOD (Flesch-Kincaid: Grade 9, Score: 65)

```markdown
Before you start setup, assess three things:

1. Data quality: Is your data clean and organized?
2. Process docs: Are your workflows documented?
3. Team alignment: Do all teams agree on the approach?

Complete these checks before technical setup.
```

**Why better:**
- Grade 9 = accessible
- Score 65 = easy
- Numbered list
- Questions help engagement
- Short, clear sentences

---

## Practical Tips

### Tip 1: Test Every Sentence

Ask: "Can a 15-year-old understand this?"

If NO → Simplify.

### Tip 2: Read Aloud

If you run out of breath mid-sentence → Too long, break it up.

### Tip 3: Use the Validator

Run `readability-scorer.py` on every draft:

```bash
python readability-scorer.py draft.md
```

Target scores:
- Flesch Reading Ease: 60-70
- Grade Level: 8-10

### Tip 4: Replace Complex Words

Keep a list of complex words and their simple alternatives:

```markdown
utilize → use
facilitate → help
implement → set up
optimize → improve
leverage → use
comprehensive → complete
methodology → method
```

### Tip 5: Break Up Long Sentences

Any sentence >25 words:
1. Find the main idea
2. Find supporting details
3. Split into 2-3 sentences

---

## Common Mistakes

### Mistake 1: Academic Writing Style

❌ **Academic:** "Organizations that implement AI-powered customer service solutions experience measurable improvements across multiple operational dimensions."

✅ **Business:** "Companies using AI customer service see clear improvements in operations."

### Mistake 2: Passive Voice Overuse

❌ **Passive:** "The tickets are processed by the agent, and responses are generated automatically."

✅ **Active:** "The agent processes tickets and generates responses automatically."

### Mistake 3: Jargon Without Definition

❌ **Jargon:** "Leverage synergistic paradigms to operationalize RevOps methodologies."

✅ **Clear:** "Use teamwork to implement RevOps methods."

### Mistake 4: Run-On Sentences

❌ **Run-on:** "The system analyzes customer queries using natural language processing algorithms that extract intent and entities from unstructured text inputs while maintaining contextual awareness across multi-turn conversational exchanges and applying confidence scoring mechanisms to determine optimal resolution pathways."

✅ **Short:** "The system analyzes customer queries using natural language processing. It extracts intent and entities from text. It maintains context across conversations. It uses confidence scores to find the best resolution path."

---

## Readability Checklist

Before declaring content complete:

- [ ] Average sentence length: 15-20 words
- [ ] Flesch Reading Ease: 60-70
- [ ] Flesch-Kincaid Grade: 8-10
- [ ] Complex words: <15%
- [ ] Passive voice: <10%
- [ ] No sentences >30 words
- [ ] No idioms or cultural references
- [ ] Active voice throughout
- [ ] Simple vocabulary
- [ ] Clear structure (bullets, steps, lists)

---

## Tools & Commands

**Validate readability:**
```bash
python scripts/readability-scorer.py draft.md
```

**Check full compliance:**
```bash
python scripts/style-enforcer.py final-draft.md "target keyword"
```

---

## Key Takeaways

1. **Short sentences win** - 15-20 words average
2. **Simple words work** - Don't use "utilize" when "use" works
3. **Active voice is clearer** - Subject does action
4. **Structure helps** - Bullets, steps, lists
5. **Test with tools** - Run readability-scorer.py
6. **Non-native speakers first** - If they understand, everyone does

**Remember:** Clarity beats cleverness every time.
