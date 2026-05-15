# Formatting Guide: Visual Examples

## Purpose

This guide shows **visual examples** of good vs bad formatting. Use this to understand what "variety" and "scannability" actually look like in practice.

---

## The Core Problem

**User's complaint:** "Too long paragraphs, not linear, no table, very few bullet points. Hard to understand."

**Root cause:** Instructions alone don't work. You need to **SEE** what good formatting looks like.

---

## ❌ BAD Example: What User is Getting (Current Output)

```markdown
Ninety-five percent of customer interactions will be AI-powered by 2025 (Source: Tidio), yet 53% of executives cite concerns about negative customer experiences as their primary barrier to adoption (Source: Ada CX). HubSpot Customer Agent resolves this tension—organizations using it resolve 50%+ of support tickets autonomously while maintaining quality standards (Source: HubSpot).

Manual ticket queues grow faster than headcount. Response times stretch from minutes to hours. Customers expect instant answers while sensitive issues demand human judgment. The challenge isn't whether to adopt AI support—it's how to implement it without destroying customer trust.

Customer Agent automates volume so your team focuses on complexity. This guide covers process-first implementation, performance benchmarks, and the ongoing governance that prevents AI investments from becoming expensive experiments.
```

**Problems:**
- 3 paragraphs, all multi-sentence blocks
- NO bullets
- NO visual variety
- Dense, hard to scan
- Looks intimidating
- Non-native speakers struggle

---

## ✅ GOOD Example: What User Should Get

```markdown
HubSpot Customer Agent resolves 50%+ of support tickets autonomously while maintaining quality standards.

Ninety-five percent of customer interactions will be AI-powered by 2025 (Source: Tidio). Yet 53% of executives cite concerns about negative customer experiences as their primary barrier to adoption (Source: Ada CX).

Manual ticket queues grow faster than headcount. Response times stretch from minutes to hours. The challenge isn't whether to adopt AI support—it's how to implement it without destroying customer trust.

**The tension:**

- Customers expect instant answers
- Sensitive issues demand human judgment
- Volume exceeds team capacity
- Quality must stay high

Customer Agent resolves this by automating volume so your team focuses on complexity.

**What you'll learn:**

- Process-first implementation
- Performance benchmarks
- Ongoing governance that prevents expensive experiments

[Diagram: AI Agent workflow showing automated vs human-escalated paths]
```

**Why this is better:**
- ✅ Paragraph variety (1, 2, 3 sentences mixed)
- ✅ Bullet sections (2 shown, many more throughout)
- ✅ Bold headers for structure
- ✅ Visual placeholder included
- ✅ Scannable, easy to skim
- ✅ White space makes it breathable
- ✅ Non-native speakers can follow

---

## Visual Pattern Comparison

### ❌ BAD: Uniform Blocks

```
████████████████
████████████████
████████████████
████████████████
████████████████
████████████████
```

All paragraphs same length = **monotonous, hard to scan**

### ✅ GOOD: Varied Pattern

```
██           (1 sentence - punch)
████████     (2 sentences - explain)
█            (1 sentence - transition)
████████████ (3 sentences - depth)
██████       (Bullets section)
█            (1 sentence - conclusion)
```

Variety = **scannable, engaging, accessible**

---

## Detailed Side-by-Side Examples

### Example 1: Opening Section

#### ❌ BAD (Fat Paragraph)

```markdown
The revenue operations (RevOps) framework helps your company be more efficient by aligning processes, people, technology, and data across your go-to-market teams. It breaks down silos between marketing, sales, and customer success, creating a unified approach to revenue generation. Organizations implementing RevOps see 10-20% increase in revenue growth, 15-25% improvement in forecast accuracy, and 30-40% reduction in revenue cycle time. This framework transforms disconnected operations into a coordinated engine that scales revenue predictably while maintaining efficiency across all customer touchpoints.
```

**Problems:**
- 4 sentences = FAT PARAGRAPH (auto-reject)
- Dense block
- Hard to scan
- Statistics buried
- No visual hierarchy

#### ✅ GOOD (Variety + Bullets)

```markdown
The revenue operations (RevOps) framework aligns processes, people, technology, and data across your go-to-market teams.

It breaks down silos between marketing, sales, and customer success.

**The impact:**

- Revenue growth: +10-20%
- Forecast accuracy: +15-25%
- Revenue cycle time: -30-40%

This framework transforms disconnected operations into a coordinated engine that scales revenue predictably.
```

**Why better:**
- ✅ 1, 2, and 3 sentence variety
- ✅ Bullets make data scannable
- ✅ Bold header creates structure
- ✅ Easy for non-native speakers
- ✅ Statistics clear and prominent

---

### Example 2: Process Explanation

#### ❌ BAD (Wall of Text)

```markdown
To implement customer health scoring, start by identifying the key signals that matter for your business model. These typically include product usage metrics like login frequency and feature adoption, customer feedback through NPS and CSAT scores, account health indicators such as billing status and renewal dates, and engagement metrics like email responses and webinar attendance. Once you've identified these signals, assign weights that total 100 points based on which factors are most predictive of retention and expansion in your specific context. Then set clear thresholds for green, yellow, and red status that trigger appropriate workflows and team actions.
```

**Problems:**
- 3 long sentences = hard to follow
- No visual breaks
- Complex lists buried in prose
- Non-native speakers lost
- Nothing to skim

#### ✅ GOOD (Lists + Structure)

```markdown
To implement customer health scoring, identify the key signals that matter for your business:

**Product usage:**
- Login frequency
- Feature adoption
- Depth of use

**Customer feedback:**
- NPS scores
- CSAT scores
- Support interactions

**Account health:**
- Billing status
- Renewal dates
- Contract utilization

**Engagement:**
- Email responses
- Webinar attendance
- Community activity

Assign weights that total 100 points based on what predicts retention and expansion. Set clear thresholds (green/yellow/red) that trigger appropriate workflows.
```

**Why better:**
- ✅ Extensive bullets (4 sections shown)
- ✅ Bold headers create hierarchy
- ✅ Easy to scan
- ✅ Non-native speakers see structure
- ✅ Can skip to relevant section

---

### Example 3: Benefits Section

#### ❌ BAD (Minimal Bullets)

```markdown
Customer health scores provide several key benefits for your organization. They help you spot risk and growth opportunities sooner, prioritize the right accounts, and know your next move. You can rescue at-risk accounts, nurture those with potential, and grow strong relationships strategically.
```

**Problems:**
- Only descriptive text
- No bullet structure
- Vague language
- Not scannable
- Weak impact

#### ✅ GOOD (Extensive Bullets + Bold)

```markdown
Customer health scores transform scattered signals into clear actions.

**Prioritize by health:**

- **Red accounts:** 48-hour save plan, exec touch, clear next steps
- **Yellow accounts:** Targeted adoption help, resolve blockers, schedule check-in
- **Green accounts:** Expansion track, intro to advanced features, request referral

**Business impact:**

- Protect revenue: Catch churn early
- Focus the team: Know exactly where to act
- Grow smart: Flag expansion candidates
- Move faster: Automate alerts and playbooks
- Make it obvious: One signal leaders read in 2 minutes

**Outcome:** Fewer churn surprises, stronger renewals, clearer growth path.

[Table: Health Score Thresholds and Actions]

| Score | Status | Action |
|-------|--------|--------|
| 80-100 | Green | Expansion outreach |
| 50-79 | Yellow | Check-in + support |
| 0-49 | Red | Save plan |
```

**Why better:**
- ✅ 3 bullet sections (extensive)
- ✅ Bold headers create hierarchy
- ✅ Table for data comparison
- ✅ Visual placeholder
- ✅ Mix of 1, 2, 3 sentence paragraphs
- ✅ Extremely scannable

---

## The Scroll Test

**CRITICAL:** Before declaring a blog post complete, perform the SCROLL TEST.

1. Open `examples/example-1-health-score.md`
2. Open your draft
3. Scroll through BOTH side-by-side
4. Ask: **Do they LOOK similar?**

### Must Match:
- ✅ Bullet density (many sections throughout)
- ✅ White space (breathing room)
- ✅ Paragraph variety (1, 2, 3 sentence mix)
- ✅ Visual placeholders (2-4 minimum)
- ✅ Tables (1-2 for comparisons)
- ✅ Bold headers (8-12 minimum)
- ✅ Scannability (can skim in 30 seconds)

### If It Doesn't Match:
- ❌ REJECT and revise
- Add more bullets
- Break up fat paragraphs
- Add bold headers
- Insert visual placeholders
- Create tables for data

---

## Formatting Checklist (Visual Verification)

**After drafting, verify visually:**

- [ ] **Paragraph variety:** Mix of short (1), medium (2), and detailed (3) sentence paragraphs
- [ ] **NO fat paragraphs:** Zero paragraphs with 4+ sentences
- [ ] **Bullet density:** 8-12 bullet sections minimum throughout article
- [ ] **Sub-bullets:** 3-5 instances of nested lists
- [ ] **Bold headers:** 8-12 bold phrases for visual hierarchy
- [ ] **Visual placeholders:** 2-4 minimum ([Screenshot], [Diagram], etc.)
- [ ] **Tables:** 1-2 for data comparisons
- [ ] **White space:** Line breaks between all paragraphs
- [ ] **Scannability:** Can identify all major points in 30-second skim

---

## Key Takeaways

1. **Instructions don't work** - You must SEE good examples
2. **Variety is king** - Mix 1, 2, 3 sentence paragraphs
3. **Bullets everywhere** - 8-12 sections minimum
4. **Visual hierarchy** - Bold headers, visual placeholders, tables
5. **Scannable above all** - Non-native speakers must be able to skim
6. **Use the scroll test** - Compare to examples before declaring done

---

## Quick Reference

**When in doubt:**
- Add more bullets
- Break up long paragraphs
- Add bold headers
- Insert visual placeholders
- Look at example-1-health-score.md

**Remember:** Reading is not as effective as SEEING. Always compare visually to examples.
