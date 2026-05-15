---
name: editing-checklist
description: Comprehensive text editing that transforms any written content (blog posts, emails, social media, documents) into polished, professional writing through systematic review of grammar, brevity, clichés, readability, voice, confidence, defensive writing, and repetition. Eliminates weak statements, defensive phrases, and content that creates doubt. Use when the user needs editing, proofreading, polishing, or improving written content of any kind.
---

# Editing-Checklist

Transform any written content into polished, professional writing through systematic editing across eight critical dimensions.

## When to Use This Skill

Use this skill when the user provides text that needs editing, regardless of format:
- Blog posts and articles
- Social media posts
- Emails and business communications
- Reports and documents
- Marketing copy
- Academic writing
- Any written content requiring polish

## ENFORCEMENT REQUIREMENT ⚠️

**CRITICAL:** You MUST use the enforcement system to validate systematic application of the 8-step checklist. **DO NOT claim editing is complete without running validation scripts.**

### Why Enforcement Exists

Research shows AI (and humans) naturally take shortcuts:
- Surface-level editing that LOOKS complete but misses issues
- Claiming "I applied all 8 steps" without systematic line-by-line review
- Producing output without documented proof of thorough work

**The enforcement scripts prevent this by requiring:**
1. ✅ Documented changes for ALL 8 steps
2. ✅ Line-by-line review with specific before/after examples
3. ✅ Validation that checks for remaining issues
4. ✅ Proof of systematic application (not just claims)

### Required Workflow

**Step 1:** Edit content systematically using the 8-step process below
**Step 2:** Document EVERY change in a `changes.json` file (see `examples/changes-template.json`)
**Step 3:** Run enforcement validation:

```bash
python scripts/editing-enforcer.py \
  --original original.md \
  --edited edited.md \
  --changes changes.json
```

**Step 4:** Run paragraph analysis validation:

```bash
python scripts/paragraph-analyzer.py edited.md
```

**Step 5:** Only after BOTH validations pass, present results to user

### What Gets Validated

The enforcement scripts check:
- ✅ All 8 steps have documented changes
- ✅ Word count reduced by 20-40%
- ✅ Grammar issues resolved
- ✅ Clichés and jargon removed
- ✅ Sentences under 25 words
- ✅ Paragraphs under 7 sentences
- ✅ Passive voice minimized
- ✅ Hedging words removed
- ✅ Defensive phrases deleted
- ✅ Repetition eliminated

**If validation fails, you MUST revise and run again. No exceptions.**

See `examples/workflow-guide.md` for complete instructions.

---

## Core Editing Principle

**You are a world-class copy editor.** Your mission is to make every word count, every sentence clear, and every paragraph engaging. Edit with precision and care, respecting the writer's voice while elevating clarity and impact.

**You are ALSO a systematic editor.** You work methodically through each of the 8 steps, document your changes, and validate your work with enforcement scripts. Surface-level editing is unacceptable.

## The 8-Step Editing Process

Apply these eight steps systematically to every piece of content. Each step focuses on a specific aspect of writing quality.

---

### Step 1: Grammar, Spelling & Punctuation

**What to fix:**
- Subject-verb agreement errors
- Incorrect verb tenses
- Spelling mistakes
- Comma splices and run-on sentences
- Missing or incorrect punctuation
- Capitalization errors
- Apostrophe misuse

**Common errors to watch for:**
- **Brand names:** "HubSpot" not "Hubspot", "RevOps" not "Rev Ops"
- **Comma splices:** Two independent clauses joined with only a comma
- **Run-ons:** Multiple sentences without proper punctuation
- **Its vs. it's:** "Its" is possessive, "it's" means "it is"
- **Their/there/they're:** Use the correct form
- **Your/you're:** "Your" is possessive, "you're" means "you are"

**Examples:**
- ❌ Before: "The team have completed there analysis and its ready for review"
- ✅ After: "The team has completed their analysis, and it's ready for review"

- ❌ Before: "The report was finished yesterday it needs approval today"
- ✅ After: "The report was finished yesterday. It needs approval today."

**Style consistency:**
- Use **en dashes (–)** for ranges: "3–5 hours", "15–25 hours" (not hyphens)
- Use **curly quotes** and apostrophes: "don't", "it's" (not straight quotes)
- Use **contractions** for conversational tone when appropriate
- Fix spacing around dashes (consistent throughout)

---

### Step 2: Brevity (Omit Needless Words)

**Core Principle: Every word must earn its place.**

Apply these brevity techniques word-by-word. When editing, question EVERY word: Does this add meaning? Could I say this with fewer words? Would removing it change the meaning? If not, delete it.

#### 2.1: Delete Filler Words (Add Zero Value)

**Remove these immediately:**
- **Intensifiers:** really, very, quite, extremely, absolutely, totally, completely, utterly, truly, definitely, certainly, literally (when not literal), actually, basically, essentially, particularly, especially, incredibly, remarkably
- **Weak modifiers:** somewhat, rather, fairly, pretty (as in "pretty good"), kind of, sort of, just, simply, merely

**Why:** These words dilute your message. "Very important" is weaker than "critical."

**Examples with explanations:**
- ❌ "This is really very important"
- ✅ "This is critical"
- **Why:** "Really very" adds nothing. "Critical" conveys urgency better than "important."

- ❌ "The tool is quite effective and actually works really well"
- ✅ "The tool works"
- **Why:** "Quite," "actually," and "really well" add no information. If it works, say it works.

#### 2.2: Eliminate Redundancies

**Common redundant phrases:**
- "absolutely essential" → "essential" (essential IS absolute)
- "advance planning" → "planning" (all planning is advance)
- "past history" → "history" (history is always past)
- "end result" → "result" (results come at the end)
- "future plans" → "plans" (plans are for the future)
- "completely eliminate" → "eliminate" (eliminate means remove completely)
- "added bonus" → "bonus" (bonuses are additions)
- "unexpected surprise" → "surprise" (surprises are unexpected)

**Why:** Redundancies waste words without adding meaning.

**Example:**
- ❌ "We need to completely eliminate the past history of errors"
- ✅ "We need to eliminate error history"
- **Why:** "Completely" is redundant with "eliminate." "Past" is redundant with "history."

#### 2.3: Remove Throat-Clearing Phrases

**Delete these preambles:**
- "It should be noted that..."
- "It is important to note that..."
- "It is worth mentioning that..."
- "The fact of the matter is..."
- "What I mean to say is..."
- "The point I'm trying to make is..."
- "Allow me to explain..."
- "Let me start by saying..."
- "First of all,"
- "To begin with,"

**Why:** These phrases delay your point. Start with what matters.

**Example:**
- ❌ "It is important to note that the system saves time"
- ✅ "The system saves time"
- **Why:** The throat-clearing adds nothing. If you're writing it, it's already noted.

#### 2.4: Simplify Wordy Phrases (The 80/20 Rule)

These verbose phrases appear in 80% of wordy writing. Master these replacements:

**Replace multi-word phrases with single words:**
- "in order to" → "to"
- "due to the fact that" → "because"
- "despite the fact that" → "although"
- "in spite of the fact that" → "although"
- "at this point in time" → "now"
- "at the present time" → "now"
- "in the near future" → "soon"
- "in the event that" → "if"
- "for the purpose of" → "to"
- "with regard to" → "about"
- "in terms of" → "for" or "in"
- "has the ability to" → "can"
- "is able to" → "can"
- "during the course of" → "during"
- "until such time as" → "until"

**Examples with explanations:**
- ❌ "In order to facilitate the implementation"
- ✅ "To implement"
- **Why:** "In order to" is always replaceable with "to." "Facilitate the implementation" is verbose for "implement."

- ❌ "Due to the fact that the system failed"
- ✅ "Because the system failed"
- **Why:** "Due to the fact that" is always "because."

#### 2.5: Convert Weak Verb Phrases to Strong Verbs

**Replace verb phrases with single verbs:**
- "give consideration to" → "consider"
- "make a decision" → "decide"
- "make a determination" → "determine"
- "reach a conclusion" → "conclude"
- "conduct an analysis" → "analyze"
- "perform an assessment" → "assess"
- "provide assistance" → "assist" or "help"
- "make improvements" → "improve"
- "take action" → "act"
- "come to an agreement" → "agree"

**Why:** Verb phrases bury the action. Strong verbs clarify.

**Examples with explanations:**
- ❌ "We need to make a decision about this approach"
- ✅ "We need to decide on this approach"
- **Why:** "Make a decision" buries the verb. "Decide" is direct.

- ❌ "The team will conduct an analysis of the data"
- ✅ "The team will analyze the data"
- **Why:** "Conduct an analysis" is verbose. "Analyze" is the action.

#### 2.6: Tighten Verb Constructions

**Active, specific verbs beat generic verb phrases:**
- "cuts that time in half" → "halves that time"
- "is handled by" → "handles"
- "helps improve" → "improves"
- "works to enhance" → "enhances"
- "serves to demonstrate" → "demonstrates"
- "tends to increase" → "increases"
- "appears to be" → "is"

**Examples with explanations:**
- ❌ "This approach helps improve efficiency"
- ✅ "This approach improves efficiency"
- **Why:** "Helps improve" is weaker than "improves." Either it improves or it doesn't.

- ❌ "The tool is used to analyze data"
- ✅ "The tool analyzes data"
- **Why:** "Is used to" adds words without adding meaning.

#### 2.7: Remove Unnecessary Determiners and Articles

**Question every "the," "a," "an":**
Sometimes articles are needed. Often they're not.

**Examples:**
- ❌ "In the process of the implementation"
- ✅ "During implementation"
- **Why:** "The" before "process" and "implementation" adds nothing.

- ❌ "For the purpose of improving the efficiency"
- ✅ "To improve efficiency"
- **Why:** Both "the"s are unnecessary. Efficiency doesn't need an article here.

#### 2.8: Cut Empty Modifiers and Qualifiers

**These modifiers add no specificity:**
- "various" → Often delete or specify
- "different" → Often delete or specify
- "certain" → Usually delete
- "particular" → Usually delete
- "specific" → Usually delete (unless comparing to general)
- "individual" → Usually delete
- "given" → Usually delete

**Examples with explanations:**
- ❌ "Various different tools and systems"
- ✅ "Tools and systems" or "Five tools and three systems"
- **Why:** "Various" and "different" add no information. If you know the number, use it.

- ❌ "A certain approach to solving the problem"
- ✅ "An approach to solving the problem"
- **Why:** "Certain" adds no specificity. Delete it.

#### 2.9: Compress Multi-Clause Sentences

**Break or combine for brevity:**

**Example:**
- ❌ "HubSpot's Prospecting Agent cuts prospect research from 15–20 minutes to under 1 minute—up to 95% time savings—while doubling response rates through AI-powered personalization."
- ✅ "HubSpot's Prospecting Agent cuts prospect research from 15–20 minutes to under 1 minute—95% faster—and doubles response rates through AI personalization."
- **Why:** "Up to" is uncertain and adds words. "AI-powered" → "AI" (powered is redundant). "Doubling" → "doubles" (present tense is stronger).

#### 2.10: Remove "Currently," "Now," and Time References That Add Nothing

**When the present tense implies timing:**
- ❌ "We are currently in the process of conducting"
- ✅ "We're conducting"
- **Why:** "Currently," "in the process of" add no value. Present tense handles timing.

- ❌ "At this point in time, the team is working on"
- ✅ "The team is working on"
- **Why:** "At this point in time" is verbose for "now," which the present tense already conveys.

#### Brevity Checklist (Apply to Every Sentence)

When editing for brevity, ask:
- [ ] Can I delete "really," "very," "quite," "actually"? → Delete
- [ ] Is there a redundant pair? ("past history") → Delete modifier
- [ ] Is there throat-clearing? ("It should be noted") → Delete
- [ ] Can I replace a phrase with one word? ("in order to" → "to") → Replace
- [ ] Is there a verb phrase? ("make a decision" → "decide") → Simplify
- [ ] Can I tighten this verb? ("helps improve" → "improves") → Tighten
- [ ] Are there unnecessary articles? ("the implementation of the strategy") → Test removal
- [ ] Do I have empty modifiers? ("various," "certain") → Delete or specify
- [ ] Can I cut "currently" or "now"? → Check if present tense handles it
- [ ] Is this sentence longer than 25 words? → Break or compress

**Target: 20-40% word reduction while preserving meaning.**

**For detailed word-by-word examples:** See `references/brevity-masterclass.md` for granular editing demonstrations with explanations for every change.

---

### Step 3: Clichés & Corporate Jargon

**Core Principle: Replace vague, overused phrases with specific, fresh language.**

Clichés signal lazy thinking. They're shortcuts that make writing sound generic, unoriginal, and often insincere. Every cliché you remove is an opportunity to be more specific, more interesting, or more accurate.

#### 3.1: Common Business Buzzword Clichés

**Replace these overused business terms:**

**"Competitive edge" → "competitive advantage"**
- **Why it's a cliché:** "Edge" is overused in business contexts to sound sharp or cutting. It's a metaphor that's lost its impact.
- **Better:** "Competitive advantage" is clearer and more professional without being cliché.
- **Example:** ❌ "This gives us a competitive edge" → ✅ "This gives us a competitive advantage"

**"Pain points" → "challenges" or specific problems**
- **Why it's a cliché:** "Pain points" is business jargon that sounds overly dramatic. Every consultant and marketer uses it.
- **Better:** Use "challenges," "problems," or better yet, name the specific issue.
- **Example:** ❌ "Address customer pain points" → ✅ "Solve data fragmentation challenges"

**"High-value" → "key" or "important"**
- **Why it's a cliché:** "High-value" is vague business speak. What makes something high-value? Revenue? Strategic importance?
- **Better:** "Key accounts" or "important clients" or specify what makes them valuable.
- **Example:** ❌ "High-value accounts" → ✅ "Key accounts" or "accounts generating $500K+ annually"

**"Capacity" → "capability" (in context of work)**
- **Why it's a cliché:** "Work capacity" is corporate jargon that sounds mechanical.
- **Better:** "Capability" focuses on what can be done, not just volume.
- **Example:** ❌ "3–4 full-time employees' work capacity" → ✅ "3–4 full-time employees' work capability"

**"Best" → "ideal" or "optimal"**
- **Why it's a cliché:** "Best" is a superlative that's overused and often unsupported. It's also subjective.
- **Better:** "Ideal" suggests suitability without claiming absolute superiority.
- **Example:** ❌ "Best for proven templates" → ✅ "Ideal for proven templates"

#### 3.2: Vague Modifier Clichés

**"Matters" → "is important" or specific reason**
- **Why it's a cliché:** "Matters" is vague and overused, especially in headlines ("Why X Matters").
- **Better:** "Is important" is clearer, or better yet, explain why.
- **Example:** ❌ "Why It Matters" → ✅ "Why It Is Important" or "Why This Saves Time"

**"Elevated" → "increased" or "higher"**
- **Why it's a cliché:** "Elevated" tries to sound sophisticated but is pretentious. Just say what you mean.
- **Better:** "Increased" is direct and clear.
- **Example:** ❌ "Elevated engagement" → ✅ "Increased engagement"

**"Similar" → "comparable"**
- **Why it's a cliché:** "Similar" is vague and overused. "Comparable" is more precise.
- **Better:** "Comparable" suggests equivalence in relevant dimensions.
- **Example:** ❌ "Similar growth" → ✅ "Comparable growth"

**"Full" (in "full visibility") → "complete"**
- **Why it's a cliché:** "Full visibility" is a common business phrase that sounds like jargon.
- **Better:** "Complete visibility" says the same thing without the cliché ring.
- **Example:** ❌ "Full visibility" → ✅ "Complete visibility"

**"Precision" → "accuracy" (in business contexts)**
- **Why it's a cliché:** "Precision" is overused in business and tech writing to sound exacting.
- **Better:** "Accuracy" is clearer and less pretentious when discussing correctness.
- **Example:** ❌ "Messaging precision matters" → ✅ "Messaging accuracy matters"

**"Chosen" → "selected"**
- **Why it's a cliché:** "Chosen" can sound vague or mystical. "Selected" is more deliberate.
- **Better:** "Selected" implies active choice with criteria.
- **Example:** ❌ "Chosen mode" → ✅ "Selected mode"

#### 3.3: Marketing & Tech Jargon Clichés

**"24/7" → "constantly" or "continuously"**
- **Why it's a cliché:** "24/7" is informal shorthand that sounds like marketing copy.
- **Better:** "Constantly" or "continuously" is more professional.
- **Example:** ❌ "24/7 without manual intervention" → ✅ "Constantly without manual intervention"

**"2x" → "double" or "twice"**
- **Why it's a cliché:** "2x" is marketing jargon that looks lazy. Write it out.
- **Better:** "Double" is clearer and more professional.
- **Example:** ❌ "2x Response Rates" → ✅ "Double Response Rates"

**"200+" → "Over 200" or "more than 200"**
- **Why it's a cliché:** The plus sign is informal and looks like marketing shorthand.
- **Better:** "Over 200" is professional and clear.
- **Example:** ❌ "200+ Accounts" → ✅ "Over 200 Accounts"

**"Game-changer" / "game-changing" → Specific benefit**
- **Why it's a cliché:** "Game-changer" is the most overused marketing phrase. It's meaningless hype.
- **Better:** Describe the actual change or benefit.
- **Example:** ❌ "This game-changing solution" → ✅ "This approach cuts processing time 50%"

**"Cutting-edge" / "bleeding-edge" → "new" or specific capability**
- **Why it's a cliché:** These phrases are tech marketing staples that sound dated.
- **Better:** Describe what's actually new about it.
- **Example:** ❌ "Cutting-edge technology" → ✅ "AI-powered automation released in 2024"

#### 3.4: Pretentious/Academic Word Clichés

**"Cohort" → "group" (in non-statistical contexts)**
- **Why it's a cliché:** "Cohort" sounds academic or pretentious when "group" is clearer.
- **Better:** "Group" is understood by everyone.
- **Example:** ❌ "Small cohort" → ✅ "Small group"

**"Thresholds" → "limits" or "levels"**
- **Why it's a cliché:** "Thresholds" can sound overly formal or technical.
- **Better:** "Limits" is clearer in most business contexts.
- **Example:** ❌ "Time-on-site thresholds" → ✅ "Time-on-site limits"

**"Misconception" → "misunderstanding"**
- **Why it's a cliché:** "Misconception" can sound pretentious or preachy, implying the reader is wrong.
- **Better:** "Misunderstanding" is gentler and more collaborative.
- **Example:** ❌ "The common misconception" → ✅ "The misunderstanding"

**"Impossible" → "unfeasible" or "impractical"**
- **Why it's a cliché:** "Impossible" is absolute hyperbole. Very few things are truly impossible.
- **Better:** "Unfeasible" or "impractical" is more accurate.
- **Example:** ❌ "Manual monitoring at this scale is impossible" → ✅ "Manual monitoring at this scale is unfeasible"

#### 3.5: Time & Process Clichés

**"Over time" → "with experience" or "gradually"**
- **Why it's a cliché:** "Over time" is predictable filler. Be more specific about how time helps.
- **Better:** "With experience" shows what causes the improvement.
- **Example:** ❌ "Gets Better Over Time" → ✅ "Improves with Experience"

**"Fast" → "quickly" (in some contexts)**
- **Why it's a cliché:** "Fast" is overused in business, especially with "scale."
- **Better:** "Quickly" can sound less marketing-y in certain contexts.
- **Example:** ❌ "Scale Fast" → ✅ "Scale Quickly"

**"At the end of the day" → Delete or "ultimately"**
- **Why it's a cliché:** This phrase is filler that adds nothing. It's one of the most overused phrases in business.
- **Better:** Usually delete it entirely, or use "ultimately" if needed.
- **Example:** ❌ "At the end of the day, teams need..." → ✅ "Teams need..."

**"Moving forward" / "going forward" → Delete or "next" / "from now on"**
- **Why it's a cliché:** Corporate filler that rarely adds meaning. Time is already moving forward.
- **Better:** Often delete, or use "next" if timing matters.
- **Example:** ❌ "Moving forward, we'll implement..." → ✅ "We'll implement..." or "Next, we'll implement..."

#### 3.6: Integration & Tech Buzzwords to Remove

**"Unified" → Often delete or be specific**
- **Why it's a cliché:** "Unified" is integration buzzword that's overused in tech marketing.
- **Better:** Often you can delete it, or specify how things connect.
- **Example:** ❌ "Unified HubSpot billing" → ✅ "HubSpot billing"

**"Seamless" / "seamlessly" → Delete or "smooth" / "without friction"**
- **Why it's a cliché:** "Seamless" is the most overused word in tech marketing. Nothing is truly seamless.
- **Better:** Delete it, or describe what actually happens smoothly.
- **Example:** ❌ "Seamlessly integrate" → ✅ "Integrate with X, Y, Z in under 5 minutes"

**"Leverage" (as a verb) → "use" or specific action**
- **Why it's a cliché:** "Leverage" is corporate jargon for "use." It sounds pretentious.
- **Better:** Use "use," or be specific about the action.
- **Example:** ❌ "Leverage our synergies" → ✅ "Combine our resources"

**"Robust" → Specific quality**
- **Why it's a cliché:** "Robust" is tech jargon that means nothing specific. Robust how?
- **Better:** Specify what makes it strong: reliable, scalable, comprehensive, etc.
- **Example:** ❌ "Robust solution" → ✅ "Reliable solution with 99.9% uptime"

#### 3.7: Corporate Meeting & Communication Clichés

**"Touch base" → "discuss" or "meet"**
- **Why it's a cliché:** "Touch base" is corporate speak that tries to sound casual but is tired.
- **Better:** "Discuss" or "meet" is direct.
- **Example:** ❌ "Let's touch base next week" → ✅ "Let's discuss this next week"

**"Circle back" → "revisit" or "return to"**
- **Why it's a cliché:** "Circle back" is corporate jargon that tries to soften "get back to."
- **Better:** "Revisit" or "return to" is clearer.
- **Example:** ❌ "Circle back on this" → ✅ "Revisit this topic"

**"Think outside the box" → "find creative solutions" or specific approach**
- **Why it's a cliché:** This is perhaps the most tired creativity cliché. It's ironic to use a cliché about creativity.
- **Better:** Describe what kind of thinking you actually want.
- **Example:** ❌ "Think outside the box" → ✅ "Find unconventional approaches"

**"Low-hanging fruit" → "easy opportunities" or "quick wins"**
- **Why it's a cliché:** "Low-hanging fruit" is overused business metaphor.
- **Better:** Say what you mean: easy opportunities.
- **Example:** ❌ "Start with low-hanging fruit" → ✅ "Start with the easiest opportunities"

#### 3.8: Emphatic Clichés to Remove

**"NOT" (in all caps) → Remove emphasis or restructure**
- **Why it's a cliché:** ALL CAPS emphasis feels like shouting and is often overused.
- **Better:** Restructure the sentence to make the point clear without caps.
- **Example:** ❌ "Signal detection is NOT required" → ✅ "Signal detection is optional"

**"Example:" as introduction → Remove or integrate naturally**
- **Why it's a cliché:** "Example:" is unnecessary introduction. Just give the example.
- **Better:** Integrate the example naturally into the paragraph.
- **Example:** ❌ "Example: A SaaS company..." → ✅ "A SaaS company..."

**"(Not Sequential Steps)" → Remove clarifying phrases in parentheses**
- **Why it's a cliché:** Parenthetical clarifications are often unnecessary. The content should be clear without them.
- **Better:** Make the main text clear enough that parentheticals aren't needed.
- **Example:** ❌ "Four Pathways (Not Sequential Steps)" → ✅ "Four Distinct Pathways"

#### 3.9: AI-Specific Clichés (ChatGPT/GPT Era - 2023+)

*These are the most common AI writing "tells." Research shows "delve" increased 400% after ChatGPT's release.*

**The AI Top 5 Words to Always Replace:**

**"Delve" → "examine" or "explore"**
- **Why it's a cliché:** "Delve" is the #1 AI writing tell. ChatGPT and other AI tools overuse this word. Humans rarely say "delve."
- **Better:** "Examine," "explore," "analyze," "review" are all clearer.
- **Example:** ❌ "Let's delve into the strategies" → ✅ "Let's examine the strategies"

**"Comprehensive" → Delete or "thorough"**
- **Why it's a cliché:** "Comprehensive" is AI's favorite vague adjective. It adds no specific information.
- **Better:** Often delete it. If needed, use "thorough" or "complete."
- **Example:** ❌ "A comprehensive analysis" → ✅ "An analysis" or "A thorough analysis"

**"Robust" → "strong" or "effective"**
- **Why it's a cliché:** "Robust" is AI's way to sound technical, but it's vague.
- **Better:** Use specific qualities: "strong," "effective," "reliable," "comprehensive."
- **Example:** ❌ "A robust framework" → ✅ "An effective framework"

**"Paramount" → "essential" or "critical"**
- **Why it's a cliché:** "Paramount" is pretentious AI language. Humans rarely say "paramount."
- **Better:** "Essential," "critical," or "vital" are clearer and less pretentious.
- **Example:** ❌ "Of paramount importance" → ✅ "Essential" or "Critical"

**"Landscape" (as metaphor) → Specific domain**
- **Why it's a cliché:** "Landscape" is AI's favorite vague metaphor for "field" or "domain."
- **Better:** Name the specific domain: "market," "industry," "field," "sector."
- **Example:** ❌ "The business landscape" → ✅ "The market" or "The industry"

**AI Intensifier Overuse (also avoid):**
- "crucial," "vital," "pivotal," "meticulous" → Appear constantly in AI writing
- "harness," "unlock the potential," "tap into" → AI dramatic verbs
- "It's important to note that..." → AI throat-clearing (always delete)
- "In today's fast-paced world..." → AI temporal cliché (always delete)

#### 3.10: Copywriting & Marketing Transformation Verbs

*Research shows marketing jargon decreases trust by 17% and lowers deal closure rates by 23%.*

**"Elevate" → "improve" + specific metric**
- **Why it's a cliché:** "Elevate" appears on every SaaS landing page. It's vague marketing speak.
- **Better:** "Improve" or specify the improvement with metrics.
- **Example:** ❌ "Elevate your workflow" → ✅ "Improve your workflow by 40%"

**"Streamline" → "simplify" + specific metric**
- **Why it's a cliché:** "Streamline" is a top 5 marketing cliché. Every software "streamlines" something.
- **Better:** "Simplify," "speed up," or specify what improves.
- **Example:** ❌ "Streamline operations" → ✅ "Reduce approval time from 3 days to 4 hours"

**"Revolutionize" / "disrupt" → Specific change + proof**
- **Why it's a cliché:** These are hyperbolic marketing terms. Few things are truly revolutionary.
- **Better:** Describe the actual change with evidence.
- **Example:** ❌ "Revolutionize your business" → ✅ "Reduce processing time by 50%"

**"Optimize" / "maximize" → Specific improvement + metric**
- **Why it's a cliché:** Vague marketing promises that sound impressive but mean nothing.
- **Better:** State the specific improvement with measurable results.
- **Example:** ❌ "Optimize performance" → ✅ "Reduce load time from 5s to 1s"

**Empty Superlatives (always remove or prove):**
- "world-class," "industry-leading," "best-in-class" → Cite rankings or remove
- "cutting-edge," "groundbreaking," "innovative" → Specify what's new
- "next-level," "next-generation" → Use version numbers or specific improvements

#### 3.11: Sales Jargon & Culture Clichés

*Sales-specific language that undermines professionalism.*

**"Hungry" → "motivated" or "driven"**
- **Why it's a cliché:** "Hungry" is unprofessional sales jargon that sounds aggressive.
- **Better:** "Motivated," "driven," or "results-focused."
- **Example:** ❌ "Looking for hungry sales reps" → ✅ "Seeking motivated sales professionals"

**"Rockstar" / "ninja" → "professional" or "expert"**
- **Why it's a cliché:** Cringey startup jargon from the 2010s. Unprofessional.
- **Better:** "Professional," "expert," "specialist."
- **Example:** ❌ "Rockstar developer" → ✅ "Experienced developer"

**"Crush quota" → "exceed targets"**
- **Why it's a cliché:** Aggressive sales bro language that sounds unprofessional.
- **Better:** "Exceed," "surpass," "consistently achieve."
- **Example:** ❌ "Crush your quota" → ✅ "Exceed your targets"

**"We're a family" → Specific culture description**
- **Why it's a cliché:** Corporate HR cliché that often signals dysfunction. Companies aren't families.
- **Better:** Be specific about culture: "collaborative environment," "supportive team."
- **Example:** ❌ "We're a family here" → ✅ "We value collaboration and support"

**"Low-hanging fruit" → "easy opportunities" or "quick wins"**
- **Why it's a cliché:** Perhaps the most overused business metaphor after "pain points."
- **Better:** Use literal language: "easy opportunities," "quick wins."
- **Example:** ❌ "Focus on low-hanging fruit" → ✅ "Start with the easiest opportunities"

**"Move the needle" → "make progress" or "show results"**
- **Why it's a cliché:** Business jargon metaphor that's overused.
- **Better:** "Make progress," "show results," or specify the metric.
- **Example:** ❌ "We need to move the needle" → ✅ "We need to increase revenue"

#### Cliché Detection Checklist

When editing for clichés, ask:
- [ ] Is this phrase used in every business article? → Replace it
- [ ] Does this sound like marketing copy? → Make it specific
- [ ] Would I say this in real conversation? → If no, simplify
- [ ] Is this a vague metaphor? ("edge," "pain points") → Use literal language
- [ ] Is this an overused superlative? ("best," "game-changer") → Be specific
- [ ] Am I using jargon to sound smart? → Use plain language
- [ ] Can I replace this with a specific metric? → Do it
- [ ] Does this sound like AI wrote it? ("delve," "comprehensive," "robust") → Humanize it
- [ ] Is this a marketing transformation verb? ("elevate," "streamline") → Add metrics

**Quick AI Detection Test:** Count instances of: delve, comprehensive, crucial, robust, paramount, landscape, harness, unlock
- **0-1:** Likely human / **2-3:** Possibly AI / **4+:** Likely AI-generated

**For detailed word-by-word examples:** See `references/cliches-masterclass.md` for granular cliché editing with explanations for every replacement.

---

### Step 4: Readability (Simplify Convoluted Sentences)

**Core Principle: Place subjects and verbs close together. Separate complex ideas into distinct sentences. Move context to the beginning.**

**Research foundation:** Readers comprehend information 40% faster when subjects and verbs appear in the first seven words. Sentences over 25 words see a 45% drop in comprehension.

#### 4.1: Separate Complex Ideas into Multiple Sentences

**When one sentence contains two distinct ideas, break them apart:**

**Example 1: Two benefits in one sentence**
- ❌ Before: "HubSpot's Prospecting Agent cuts prospect research from 15–20 minutes to under 1 minute—up to 95% time savings—while doubling response rates through AI-powered personalization."
- ✅ After: "HubSpot's Prospecting Agent cuts prospect research from 15–20 minutes to under 1 minute—95% faster. It also doubles response rates through AI personalization."
- **Why:** Each sentence focuses on one complete idea, making both benefits easier to absorb. The connection between time savings and response rate improvement is clearer when separated.

**Example 2: Multiple points plus clarification**
- ❌ Before: "This guide explains the agent's role, enrollment methods, and its fit in your RevOps architecture—including the misunderstanding about signal detection being required."
- ✅ After: "This guide explains the agent's role, enrollment methods, and its fit in your RevOps architecture. It also addresses the misunderstanding about signal detection being required."
- **Why:** Separating the clarification from the main list makes both easier to process. The dash-introduced clause no longer feels tacked on.

#### 4.2: Place Subject and Verb Close Together (Within 5 Words)

**Keep subjects and verbs within 4-5 words of each other for optimal comprehension:**

**Example 1: Move interrupting clauses**
- ❌ Before: "The agent, knowing that her team depended on her, researched the prospect."
- ✅ After: "The agent researched the prospect, knowing that her team depended on her."
- **Why:** "Agent researched" delivers the main idea immediately. Readers don't have to hold "agent" in memory while processing the interruption.

**Example 2: Restructure long opening phrases**
- ❌ Before: "Using HubSpot's Buyer Intent features (under Marketing Hub), you can create workflows that enroll prospects based on intent signals."
- ✅ After: "You can create workflows that enroll prospects based on intent signals using HubSpot's Buyer Intent features (under Marketing Hub)."
- **Why:** "You can create" appears immediately. The method (Buyer Intent features) comes after the main action.

#### 4.3: Move Context and Conditions to the Beginning

**Place "without," "when," "if," and other conditions at the start of sentences:**

**Example 1: Context at the beginning**
- ❌ Before: "The agent uses this profile as its playbook for personalizing messages. Without this training documentation, the agent can't 'know' your brand."
- ✅ After: "Without this training documentation, the agent can't 'know' your brand. The agent uses this profile as its playbook for personalizing messages."
- **Why:** Condition comes before consequence. Readers understand the limitation before learning the solution. This follows natural cause-effect logic.

**Example 2: Add "should you" for clarity**
- ❌ Before: "When to prioritize outreach to accounts showing buying signals or increased engagement?"
- ✅ After: "When should you prioritize outreach to accounts showing buying signals or increased engagement?"
- **Why:** Adding "should you" creates a grammatically correct question. The subject and verb are properly positioned.

#### 4.4: Use "By [Verb]ing" for Methods

**Show how something is done with parallel gerund structures:**

**Example:**
- ❌ Before: "Researches the prospect: Queries Breeze Intelligence for firmographic data, analyzes company news, and reviews prior CRM interactions."
- ✅ After: "Researches the prospect by querying Breeze Intelligence for firmographic data, analyzing company news, and reviewing prior CRM interactions."
- **Why:** The gerund form (-ing) creates parallel structure: querying, analyzing, reviewing. "By" naturally connects the action to the methods.

#### 4.5: Lead with the Main Action

**Put the most important information at the beginning:**

**Example 1: Adding "automatically" at the start**
- ❌ Before: "Logs all activities to contact timelines."
- ✅ After: "Automatically logs all activities to contact timelines."
- **Why:** Starting with "Automatically" emphasizes the automation benefit immediately. The adverb is directly before the verb for natural flow.

**Example 2: Converting passive to active**
- ❌ Before: "Any trigger condition compatible with the workflow can be used to enroll prospects."
- ✅ After: "Use any workflow-compatible trigger condition to enroll prospects."
- **Why:** Imperative form ("Use") makes it an instruction. "Workflow-compatible" is more concise than "compatible with the workflow."

#### 4.6: Fix Comma Splices and Run-On Sentences

**Two independent clauses need proper punctuation:**

**Example 1: Comma splice**
- ❌ Before: "You define configurable visitor intent criteria (e.g., 'visited pricing page 3+ times in 7 days'), workflows automatically trigger outreach when prospects hit these thresholds."
- ✅ After: "You define configurable visitor intent criteria (e.g., 'visited pricing page 3+ times in 7 days'). Workflows automatically trigger outreach when prospects hit these thresholds."
- **Why:** Two independent clauses cannot be joined with just a comma. Separating them fixes the grammar and improves clarity.

**Example 2: And vs. comma**
- ❌ Before: "Semi-Autonomous Mode: Quality control at scale—rep reviews every draft, approves/edits/rejects, and the agent learns from changes."
- ✅ After: "Semi-Autonomous Mode: Quality control at scale. The rep reviews every draft, approves/edits/rejects, and the agent learns from changes."
- **Why:** Clarifies that "rep" does the first actions and "agent" does the learning. Subject clarity improves readability.

#### 4.7: Simplify Vocabulary

**Replace academic or unnecessarily complex words:**

**Example:**
- ❌ Before: "Notwithstanding the aforementioned considerations, it is imperative that stakeholders endeavor to ascertain the viability of the proposed initiative"
- ✅ After: "Despite these concerns, stakeholders must determine if this initiative will work"
- **Why:** Simpler words increase comprehension speed. "Notwithstanding" → "Despite", "ascertain" → "determine", "viability" → "will work"

#### 4.8: Paragraph Structure and Density

**Core Principle: One idea per paragraph, maximum 3-5 sentences.**

**Research foundation:** Paragraphs exceeding 7-8 sentences create cognitive overload. Readers scan rather than read continuously—dense "walls of text" cause readers to skip content entirely.

**Technical Terms:**
- **Wall of text:** Dense paragraphs with too many sentences and ideas bundled together
- **Chunking:** Breaking content into small, distinct units that readers can scan and understand
- **BLUF (Bottom Line Up Front):** Stating the main point first, then providing supporting details
- **Cognitive load:** Mental effort required to process information

**Paragraph Length Guidelines:**

| Context | Optimal Length | Maximum | Notes |
|---------|---------------|---------|-------|
| Blog/Web | 2-4 sentences | 5 sentences | More white space for scanning |
| Business Writing | 3-5 sentences | 7 sentences | Clear topic sentences |
| Email | 2-3 sentences | 4 sentences | Extreme brevity |
| Technical Docs | 3-5 sentences | 6 sentences | One concept per paragraph |
| Academic | 4-6 sentences | 8 sentences | More idea development |

**Examples:**

❌ **Before (Wall of Text—12 sentences in one paragraph):**
"The Prospecting Agent is a specialized AI application on HubSpot's Breeze AI platform that automates prospect research, personalizes outreach messages, and manages send workflows—freeing reps from manual work so they focus on selling. It can monitor 200+ target accounts simultaneously, research prospects in seconds, and draft personalized emails within minutes—constantly without manual intervention. The agent queries Breeze Intelligence for firmographic data, analyzes recent company news, reviews prior CRM interactions, and identifies key stakeholders before generating contextually relevant outreach messages. Research time drops from 15-20 minutes to under 1 minute per prospect, saving teams 750+ hours weekly. For a 10-person sales team researching 50 prospects weekly, this translates to 125-167 hours saved—equivalent to 3-4 full-time employees' work capacity."

**Problems:**
- 12 sentences, 210 words—cognitive overload
- 5+ distinct ideas mixed together
- No visual breaks or hierarchy
- Main value buried in the middle
- Impossible to scan

✅ **After (Chunked with BLUF structure):**

**Time Savings (BLUF):**
The Prospecting Agent reduces research time from 15-20 minutes to under 1 minute per prospect—saving teams 750+ hours weekly.

**What It Does:**
The agent automates prospect research, personalizes outreach messages, and manages send workflows—freeing reps from manual work to focus on selling.

**How It Works:**
It queries Breeze Intelligence for firmographic data, analyzes company news, reviews CRM interactions, and identifies key stakeholders. Based on this research, it generates contextually relevant outreach messages.

**Scale Impact:**
For a 10-person sales team researching 50 prospects weekly, this saves 125-167 hours—equivalent to 3-4 full-time employees' work capacity.

**Why better:**
- 4 focused paragraphs instead of 1 dense block
- Each develops one complete idea
- BLUF structure—time savings first
- Clear headings enable scanning
- 60% easier to understand

**BLUF (Bottom Line Up Front) Pattern:**

❌ **Main point at end:**
"The agent queries multiple data sources, analyzes firmographic data, reviews company news, and identifies key stakeholders to build comprehensive prospect profiles. This entire process, which would take a rep 15-20 minutes manually, is completed by the agent in under 1 minute."

✅ **BLUF—main point first:**
"The agent completes research in under 1 minute—compared to 15-20 minutes manually. It queries Breeze Intelligence for firmographic data, analyzes company news, reviews CRM interactions, and drafts personalized outreach based on findings."

**Why BLUF works:**
- Readers immediately understand value
- Supporting details follow logically
- Key information isn't buried
- Reduces cognitive load

#### Paragraph Structure Checklist

When editing paragraphs, ask:
- [ ] Does this paragraph exceed 7-8 sentences? → Break into multiple paragraphs
- [ ] Does it develop more than one idea? → Separate ideas into different paragraphs
- [ ] Is the main point at the end? → Apply BLUF—move to beginning
- [ ] Does it look like a "wall of text"? → Add white space and headings
- [ ] Can readers quickly scan and find information? → If no, add subheadings
- [ ] Does the topic sentence state the main point clearly? → If no, rewrite with BLUF
- [ ] Are ideas presented in logical sequence? → Reorder if needed

#### Automated Fat Paragraph Detection

After editing, run the paragraph analyzer script to automatically detect fat paragraphs and walls of text:

```bash
python scripts/paragraph-analyzer.py your-edited-file.md
```

**The script checks:**
- Fat paragraphs (4+ sentences) — warns about cognitive overload
- Critical paragraphs (8+ sentences) — flags for immediate action
- Walls of text (150+ words) — identifies dense blocks
- Paragraph variety — ensures mix of lengths to avoid monotony
- Visual breakdown — shows paragraph distribution at a glance

**Exit codes:**
- `0` = All paragraphs optimal (3-5 sentences)
- `1` = Critical issues found (8+ sentence paragraphs)
- `2` = Warning issues found (4-7 sentence paragraphs)

**Use this to verify Step 4 compliance before finalizing edits.**

#### Readability Checklist (Apply to Every Sentence)

When editing for readability, ask:
- [ ] Is the sentence over 25 words? → Break it into multiple sentences
- [ ] Are subject and verb separated by more than 5 words? → Move interrupting elements
- [ ] Does the sentence contain "and" or "while" connecting independent clauses? → Separate them
- [ ] Is there context/condition at the end? → Move to the beginning
- [ ] Is it passive voice? → Convert to active
- [ ] Does it use em dashes mid-sentence? → Use periods instead
- [ ] Does it contain multiple complex ideas? → Give each its own sentence
- [ ] Would I say this out loud? → If no, simplify
- [ ] Can a 12-year-old understand this? → If no, simplify vocabulary

**Target:** Most sentences 15-20 words, none over 25 words. Most paragraphs 3-5 sentences, none over 7-8 sentences.

**For detailed guidance:**
- **Sentence-level:** See `references/readability-masterclass.md` for granular examples
- **Paragraph-level:** See `references/paragraph-structure-guide.md` for comprehensive framework on chunking, BLUF, and lean writing principles
- **Automated detection:** Run `scripts/paragraph-analyzer.py` to check for fat paragraphs and walls of text

---

### Step 5: Passive Voice → Active Voice

**How to identify passive voice:**
- Look for: "was done by", "is handled by", "are managed by", "has been created by", "can be seen"
- Look for: "was", "were", "been", "being" + past participle
- Test: Can you add "by zombies" after the verb? If yes, it's passive

**Examples:**
- ❌ Before: "Social posts are created by the agent"
- ✅ After: "The agent creates social posts"

- ❌ Before: "The report was analyzed by the team"
- ✅ After: "The team analyzed the report"

- ❌ Before: "Results were achieved through implementation"
- ✅ After: "Implementation achieved results"

- ❌ Before: "The strategy was developed by our consultants and is being implemented by the operations team"
- ✅ After: "Our consultants developed the strategy. The operations team is implementing it."

- ❌ Before: "Mistakes can be avoided by following this process"
- ✅ After: "Follow this process to avoid mistakes"

**When passive voice is acceptable:**
- When the actor is unknown: "The office was broken into overnight"
- When the actor is obvious: "The president was elected in 2024"
- When the focus should be on the action, not the actor: "These findings were peer-reviewed"
- For variety or emphasis (use sparingly)

---

### Step 6: Confidence (Remove Hedging Words)

**Core Principle: Back claims with evidence. State facts directly. Trust readers to evaluate your arguments.**

Hedging signals uncertainty and weakens writing. In professional (non-academic) contexts, direct statements backed by evidence are more persuasive than hedged claims.

**What to remove:**
- **Excessive qualifiers:** probably, possibly, potentially, might, could, may, perhaps, maybe, seemingly
- **Uncertainty phrases:** "I think", "I believe", "it seems", "appears to be", "tends to", "in my opinion"
- **Weak verbs:** "try to", "attempt to", "hope to", "aim to"
- **Double hedging:** "could potentially", "might possibly", "seems like it may"

#### 6.1: The 10 Categories of Hedging to Eliminate

**1. Modal Verb Hedging**
- ❌ "This mode is best for higher-touch sales"
- ✅ "Use this mode for higher-touch sales"
- **Why:** Direct instruction is stronger than hedged recommendation

**2. Unnecessary Formality (False Formality)**
- ❌ "What You Will Spend"
- ✅ "What You'll Spend"
- **Why:** Contractions are MORE direct in professional writing (12% more readable)

**3. Explanatory Parentheticals**
- ❌ "Create segments (HubSpot's term for dynamic lists) based on..."
- ✅ "Create segments based on..."
- **Why:** Defensive parentheticals interrupt main point

**4. Slash Hedging**
- ❌ "The rep reviews every draft, approves/edits/rejects"
- ✅ "The rep reviews every draft, approves, edits, or rejects"
- **Why:** Slashes create visual clutter and suggest indecision

**5. Numeric Hedging**
- ❌ "3+ times" (web content) vs. "3 or more times" (formal docs)
- ✅ Context-dependent: "3+" is MORE direct for web/email; "3 or more" for formal documentation
- **Why:** Different formats optimize for different reading contexts

**6. "Then" Hedging**
- ❌ "The agent then takes over from there"
- ✅ "The agent takes over"
- **Why:** "Then" and "from there" are both redundant

**7. Source Citation Hedging**
- ❌ "HubSpot reports that customers achieve 2x response rates (Source: HubSpot)"
- ✅ "HubSpot reports that customers achieve 2x response rates"
- **Why:** Already said "HubSpot reports"—citation is redundant

**8. Punctuation Hedging**
- ❌ "Company news (funding, acquisitions, leadership changes)"
- ✅ "Company news: funding, acquisitions, leadership changes"
- **Why:** Colons signal "here's what I mean" more directly than parentheses

**9. "Such As" Hedging**
- ❌ "Industries where automation feels impersonal, such as wealth management"
- ✅ "Industries where automation feels impersonal include wealth management"
- **Why:** "Include" is more assertive than "such as"

**10. "Which" Clauses**
- ❌ "Enroll via segment-based or manual enrollment, which is the simplest to manage"
- ✅ "Enroll via segment-based or manual enrollment—the simplest to manage"
- **Why:** Removing "which is" makes statement more direct

#### 6.2: Quick Examples

- ❌ Before: "This could potentially maybe help teams improve their processes"
- ✅ After: "This helps teams improve their processes" (if supported by evidence)

- ❌ Before: "It seems that many teams might potentially see some benefits from this approach"
- ✅ After: "Teams report significant benefits from this approach" (with citation)

- ❌ Before: "I think that we should probably try to implement this solution"
- ✅ After: "Implement this solution"

- ❌ Before: "This approach may potentially offer some advantages"
- ✅ After: "This approach cuts processing time by 40%" (specific benefit)

#### 6.3: When to Keep Qualifiers

- When making genuine predictions: "This approach may work better for smaller teams"
- When citing uncertain data: "Some studies suggest..."
- When discussing future possibilities: "This could expand to include..."
- But minimize even these

#### 6.4: Replace Weak Phrases with Strong Ones

- "try to improve" → "improve"
- "attempt to solve" → "solve"
- "hope to achieve" → "achieve"
- "aim to deliver" → "deliver"
- "so they" → "to" (eliminate unnecessary words)
- "which is" → delete or use em dash

#### Confidence Editing Checklist

When editing for confidence, ask:
- [ ] Does this sentence hedge unnecessarily? → Back with evidence or delete qualifier
- [ ] Am I using modal verbs that weaken claims? → Replace with direct statements
- [ ] Are there defensive parentheticals? → Delete or integrate naturally
- [ ] Am I using slashes that suggest indecision? → Use commas and "or"
- [ ] Do I have redundant source citations? → Remove if already stated
- [ ] Can I replace "such as" with "include"? → More assertive
- [ ] Can I remove "which is/are" clauses? → Direct statement or em dash
- [ ] Am I double-hedging? ("could potentially") → Use one or neither
- [ ] Do I state facts directly with evidence? → If yes, no hedging needed
- [ ] Does hedging make my writing sound uncertain? → Replace with specific data

**For comprehensive hedging elimination guidance:** See `references/confidence-masterclass.md` for detailed frameworks on identifying and eliminating 10 categories of hedging, the confidence spectrum from weak to strong, context considerations (academic vs. professional), and real-world transformation examples

---

### Step 7: Defensive Writing & Content Deletion

**Core Principle: State facts with confidence. Delete content that creates doubt or confusion.**

Defensive writing signals insecurity and undermines authority. It plants doubt before readers evaluate your claims. Strong writing states facts directly, backs them with evidence, and trusts readers to think critically.

**Research Foundation:** Processing fluency—how easily readers understand content—directly affects judgments of truth and credibility. Complex, defensive language decreases perceived credibility by 17% and lowers conversion rates by 23%.

#### 7.1: Delete Defensive Parentheticals and Clarifications

**What they are:** Phrases that preemptively defend against criticism no one has made.

**Common patterns:**
- "Critical clarification:"
- "Important distinction:"
- "Important note:"
- "(NOT part of)"
- "It should be noted that..."

**Examples:**

❌ "Critical clarification: Signal detection is an optional enrollment method among four pathways."
✅ "Signal detection is one of four enrollment methods."
**Why:** "Critical clarification" plants doubt. State the fact directly.

❌ "Important distinction: The Prospecting Agent is ONE application powered by Breeze AI."
✅ "The Prospecting Agent is one application within Breeze AI."
**Why:** "Important distinction" is defensive. "ONE" in caps feels like you're correcting readers.

❌ "It's a powerful but optional combination."
✅ Delete or: "This increases conversion by 40% for accounts showing buying signals."
**Why:** "Powerful but optional" hedges in both directions. Show the value with data.

#### 7.2: Remove Reassurance Statements (Handholding)

**What they are:** Statements that reassure readers about things they weren't worried about.

**Why they're problematic:** Creating problems to solve them makes readers question whether your original claim was true.

**Examples:**

❌ "The agent functions without these, but they enhance capabilities."
✅ Delete entirely or state specific enhancement: "Breeze Intelligence adds firmographic data from 200+ sources."
**Why:** If something functions fine, why mention what it doesn't need?

❌ "Don't worry—this won't affect your existing setup."
✅ "Your existing setup remains unchanged."
**Why:** "Don't worry" plants worry. State facts without emotional framing.

❌ "This is powerful but optional."
✅ State the benefit: "This feature saves 15 hours weekly for teams managing 100+ accounts."
**Why:** Replace vague reassurance with specific value.

#### 7.3: Eliminate Uncertainty Phrases That Undermine Claims

**What they are:** Qualifiers that weaken statements without adding accuracy.

**Common patterns:**
- "could potentially"
- "might possibly"
- "seems like"
- "appears to be"
- "in some cases"
- "sort of" / "kind of"

**Examples:**

❌ "With 56% of B2B sales professionals using AI daily, automation has shifted from competitive advantage to baseline requirement."
✅ Delete entirely—generic market stat doesn't prove your specific product matters.
**Why:** Vague market trend without connection to your core claim weakens your argument.

❌ "You might want to consider implementing this approach."
✅ "Implement this approach to reduce processing time by 40%."
**Why:** "Might want to consider" is triple hedging. State the recommendation with evidence.

❌ "This could potentially help improve results in some cases."
✅ "This reduces processing time by 30%." (with citation)
**Why:** Stack of hedges signals zero confidence. Back claims with data.

#### 7.4: Remove False Authority Markers

**What they are:** Phrases that try to sound authoritative but signal uncertainty.

**Common patterns:**
- "Clearly..."
- "Obviously..."
- "As you can see..."
- "It goes without saying..."
- "As everyone knows..."

**Examples:**

❌ "As you can see, this approach is effective."
✅ "This approach reduces errors by 45%."
**Why:** If readers can see it, you don't need to tell them. Show the evidence.

❌ "It's clear that automation is important."
✅ "Automation saves 750+ hours weekly for sales teams."
**Why:** Announcing clarity suggests it might not be clear. Let evidence speak.

#### 7.5: When to Delete Content Entirely

**Delete when content:**

**1. Creates weak connections to core claims**
- Doesn't directly support your main argument
- Uses generic market stats without proving your specific solution matters
- Could apply equally to competitors

**2. Repeats without adding value**
- Says the same thing twice with different words
- Lists functions, then lists same functions again
- Restates obvious points

**3. Introduces confusion**
- Raises questions it doesn't answer
- Adds spec details without context
- Requires readers to hold multiple concepts simultaneously

**4. Uses defensive disclaimers**
- Creates doubt to preemptively address objections
- Corrects problems you created through poor structure
- Uses all-caps emphasis ("NOT") to stress points

**5. States vague claims without proof**
- Generic statements that could apply to any product
- Marketing buzzwords without metrics
- Throat-clearing AI-generated phrases

**6. Interrupts flow with sales pitches in educational content**
- Breaks the logical progression of explanation
- Inserts promotional language mid-teaching
- Repeats benefits already covered elsewhere
- Shifts from teaching to selling inappropriately

**Example deletions:**

❌ Delete: "With 56% of B2B sales professionals using AI daily..."
**Why:** Generic stat that doesn't prove your product's specific value.

❌ Delete: "It can monitor 200+ target accounts simultaneously..." (from opening)
**Better:** Move to dedicated section with context explaining why 200 matters.

❌ Delete: "All agents share the same intelligence layer, so they work together in your CRM without silos."
**Better:** "All agents access the same data—CRM records, enriched prospect data, and knowledge vaults—so there's no duplication."
**Why:** "Work together" is vague. "Share the same intelligence layer" is jargon. Be specific and direct.

❌ Delete: "As you scale, data fragmentation between tools slows prospecting. The agent eliminates manual research steps by centralizing prospect intelligence in your CRM."
**Why:** This interrupts the flow of your "Personalization at Scale" section. The point is already made in the next section. It shifts from teaching to selling mid-explanation.

#### 7.6: Write with Confidence

**Direct statements over hedging:**

❌ Weak: "This could potentially help you save time."
✅ Strong: "This saves 15 hours per week."

**Specific benefits over vague claims:**

❌ Vague: "This provides significant improvements."
✅ Specific: "This cuts prospect research from 20 minutes to under 1 minute."

**Active recommendations over passive suggestions:**

❌ Passive: "It might be worth considering this approach."
✅ Active: "Use this approach for accounts over $50K."

**Evidence over reassurance:**

❌ Reassurance: "Don't worry—this won't disrupt your workflow."
✅ Evidence: "Implementation takes 2 hours and runs alongside existing systems."

#### 7.7: Defensive Writing Checklist

When reviewing content, ask:
- [ ] Does this phrase announce itself as important? (Delete the announcement)
- [ ] Am I reassuring readers about something they weren't worried about? (Delete or reframe)
- [ ] Do I have phrases like "could potentially" or "might possibly"? (Replace with evidence)
- [ ] Am I using "Obviously" or "Clearly" to assert authority? (Delete—show evidence)
- [ ] Does this statement create confusion instead of resolving it? (Simplify or delete)
- [ ] Am I stating market trends without connecting to my specific claim? (Delete or connect)
- [ ] Am I saying the same thing twice? (Keep the stronger version)
- [ ] Would removing this sentence improve clarity? (Delete)
- [ ] Does this interrupt the flow of my explanation? (Delete or move)
- [ ] Am I inserting a sales pitch in the middle of teaching? (Delete—let demonstration teach)
- [ ] Can I replace hedging with evidence? (Add data, remove hedge)
- [ ] Can I replace vague claims with specific metrics? (Use numbers)

**For detailed examples and decision frameworks:** See `references/defensive-writing-guide.md` for comprehensive guidance on identifying and eliminating defensive writing patterns, with before/after examples for every category.

---

### Step 8: Repetition Removal

**What to check:**
- **Repeated words:** Same word used within 2-3 sentences (unless intentional)
- **Duplicate phrases:** Same phrase appearing multiple times
- **Overused transitions:** "Additionally", "Furthermore", "Moreover" used repeatedly
- **Concept repetition:** Same idea stated multiple ways without adding new information
- **Semantic repetition (anchor numbers):** Same statistic/metric repeated 3+ times without adding value

**Examples:**
- ❌ Before: "Teams use agents. The agents help teams. Teams save time when agents automate tasks."
- ✅ After: "Teams use agents that automate tasks and save time."

- ❌ Before: "HubSpot offers features. These features include automation. Additional features are reporting and analytics."
- ✅ After: "HubSpot offers automation, reporting, and analytics."

- ❌ Before: "The strategy helps teams. It helps them work faster. This help is significant."
- ✅ After: "The strategy helps teams work significantly faster."

**Vary word choice:**
- Instead of repeating "improve" three times: improve, enhance, strengthen
- Instead of repeating "teams" five times: teams, groups, organizations, departments
- Instead of repeating "important" repeatedly: critical, essential, vital, key

**Avoid echo words:**
- ❌ "The analysis of the data shows that data quality matters"
- ✅ "The analysis shows data quality matters"

**Semantic repetition (anchor numbers):**
- ❌ Before: "The agent monitors 200+ accounts... With 200+ accounts monitored... Tracking 200+ accounts... For teams managing 200+ accounts..."
- ✅ After: Deploy the anchor ONCE: "The agent monitors over 200 target accounts simultaneously." Then use conceptual language: "Enterprise-scale monitoring", "continuous tracking at pace manual teams can't sustain"
- **Why:** Repeating the same statistic 3+ times creates evidence fatigue. Deploy quantitative anchors once with full context, then vary language elsewhere.

**For comprehensive redundancy guidance:** See `references/redundancy-repetition-guide.md` for detailed frameworks on identifying and eliminating 6 types of repetition, including semantic repetition, circular reasoning, and echoing.

---

## Editing Output Format

Provide edits in this format:

**Original Text:**
[Include the original text the user provided]

**Edited Text:**
[Provide the fully edited version]

**Key Changes Made:**
1. **Grammar & Punctuation:** [Briefly note major corrections]
2. **Brevity:** [Note how many words removed and key simplifications]
3. **Clichés:** [List corporate jargon removed]
4. **Readability:** [Note complex sentences simplified]
5. **Active Voice:** [Count passive → active conversions]
6. **Confidence:** [List hedging words removed]
7. **Defensive Writing:** [Note defensive phrases and weak connections deleted]
8. **Repetition:** [Note repeated words/phrases eliminated]

**Summary:**
[Brief 2-3 sentence summary of the overall improvements and tone preservation]

---

## Important Editing Principles

### 1. Preserve the Writer's Voice
- Match the original tone (formal, casual, humorous, etc.)
- Keep stylistic choices that define the writer's voice
- Don't make writing sound generic or AI-generated
- Maintain sentence fragments if they're intentional and stylistic

### 2. Context Matters
- **Blog posts:** Can be more conversational, personality-driven
- **Business emails:** Keep professional but warm
- **Social media:** Short, punchy, engaging
- **Reports:** More formal, data-driven
- **Marketing copy:** Benefit-focused, action-oriented

### 3. Don't Over-Edit
- Some personality quirks are good
- Not every sentence needs to be perfect
- Conversational writing can break grammar rules intentionally
- Natural > Robotically perfect

### 4. Read Aloud Test
- Does this sound natural when read aloud?
- Would a human actually say this?
- If it sounds stiff or unnatural, simplify further

---

## Special Considerations

### For Different Content Types:

**Blog Posts:**
- Keep personality and unique voice
- Use shorter paragraphs (2-3 sentences)
- Vary sentence length for rhythm
- Allow some stylistic rule-breaking

**Emails:**
- Front-load the main point
- Use bullet points for action items
- Keep paragraphs extra short (1-2 sentences)
- End with clear next steps

**Social Media:**
- Extreme brevity (cut 50% of words)
- Strong opening hook
- One main idea per post
- Active voice exclusively

**Reports/Documents:**
- Clear headers and structure
- Data-driven language
- Professional tone throughout
- Specific numbers and metrics

---

## Quality Checklist

Before declaring editing complete, verify:

### Content Quality
- [ ] All grammar and spelling errors corrected
- [ ] All unnecessary words removed (target: 20-40% reduction)
- [ ] All clichés and jargon replaced with specific language
- [ ] All complex sentences simplified
- [ ] Passive voice minimized (90%+ active)
- [ ] Hedging words removed (unless justified)
- [ ] Defensive phrases and weak connections deleted
- [ ] Content that creates doubt or confusion eliminated
- [ ] Reassurance statements replaced with evidence
- [ ] Repeated words and phrases eliminated
- [ ] Paragraph structure verified: Most 3-5 sentences, none over 7-8 sentences
- [ ] Writer's original voice preserved
- [ ] Content sounds natural when read aloud
- [ ] Text is appropriate for its intended format
- [ ] Specific metrics/numbers used instead of vague claims
- [ ] Direct statements over hedging throughout

### ENFORCEMENT VALIDATION (MANDATORY)
- [ ] **Changes documented:** Created `changes.json` with specific edits for all 8 steps
- [ ] **Enforcement passed:** Ran `python scripts/editing-enforcer.py` and validation passed
- [ ] **Paragraph analysis passed:** Ran `python scripts/paragraph-analyzer.py` and no critical issues
- [ ] **Audit trail created:** Documented line numbers, before/after, and reasons for every change
- [ ] **Validation reports saved:** Captured enforcement and paragraph analysis output

**⚠️ CRITICAL: Do not proceed to presenting results without completing the enforcement validation checklist above.**

---

## Common Mistakes to Avoid

1. **Over-editing:** Making the text too formal or robotic
2. **Removing personality:** Stripping out the writer's unique voice
3. **Being too aggressive:** Changing meaning by over-simplifying
4. **Inconsistent style:** Mixing formal and informal without reason
5. **Breaking intentional style:** "Fixing" fragments that are deliberate
6. **Adding new content:** Editing should clarify, not add ideas
7. **Changing tone:** Formal → casual or vice versa inappropriately

---

## Example Editing Session

**Original Text:**
"It is really important to note that in order to optimize your workflow processes, you should probably try to leverage automation tools that can potentially help streamline operations. These tools are really quite effective and they basically enable teams to work more efficiently. At the end of the day, the utilization of these solutions could maybe result in significant improvements."

**Edited Text:**
"Automate workflows to work efficiently. Automation tools reduce task time by 40% and eliminate manual errors. Teams complete projects faster and with higher quality."

**Key Changes:**
- **Brevity:** Cut from 57 words to 25 words (56% reduction)
- **Clichés removed:** "at the end of the day", "leverage", "streamline"
- **Hedging removed:** "probably", "try to", "potentially", "could maybe"
- **Passive to active:** "utilization of" → direct action
- **Vague to specific:** Added "40%" metric instead of "significant improvements"
- **Simplified:** Removed throat-clearing and unnecessary complexity
