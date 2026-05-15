---
name: linkedin-post-creation
description: B2B LinkedIn post creation for high engagement. HOOKS ARE SACRED - spend 40% time on hooks (TAS/PAS/SCQA frameworks). MOBILE-FIRST formatting (one sentence per line, no paragraphs, short punchy sentences, NO EMOJIS). STRONG POV required - vanilla content fails. Research-driven with Exa.ai/Firecrawl. Seed content from topic/brain dump/article/similar post. 9-phase workflow: research → reverse outline → Y+U+I → parts → hooks → posts → formatting → 11-point editing → polish. Outputs 2 complete posts ready to publish.
---

# LinkedIn Post Creation Skill

## 🎯 What This Skill Does

Creates high-performing B2B LinkedIn posts using a systematic 9-phase workflow that prioritizes hooks and mobile-first formatting.

**Core Principles:**
- **Hooks are your religion** - 4-5 hooks per nugget, select 2 best
- **Mobile-first always** - One sentence per line, no paragraphs
- **Strong POV required** - Contrarian when appropriate
- **NO EMOJIS** - Professional B2B tone
- **Research-driven** - Validate with existing LinkedIn content

---

## 📦 Reference Files

**Read these before starting:**

- `references/workbook-workflow.md` - Complete workflow with AI prompts
- `references/hook-frameworks.md` - TAS, PAS, SCQA detailed frameworks
- `references/hook-principles.md` - Erica Schneider's core teaching
- `references/linkedin-frameworks.md` - 10 proven post structures
- `references/editing-framework.md` - 11-point editing checklist
- `references/content-formats.md` - When to use which format
- `examples/high-performing-posts.md` - Real post analyses

---

## 🔄 9-Phase Workflow

### Phase 0: Strategic Planning & Research

**BEFORE ANY EXECUTION:**

**STEP 0.1: Input Analysis**

**Type 1: Topic Only**
```
User provides: "Create a LinkedIn post about HubSpot attribution challenges"

Actions:
1. Research existing LinkedIn posts on attribution
2. Use web_search_exa: "LinkedIn posts about attribution challenges site:linkedin.com"
3. Analyze top-performing posts (hooks, structure, engagement)
4. Compile findings as seed content
5. Proceed to Phase 1
```

**Type 2: Brain Dump**
```
User provides: Unstructured thoughts/ideas about a topic

Actions:
1. Extract and organize key ideas
2. Research to validate and expand
3. Structure into coherent seed content
4. Identify main themes and angles
5. Proceed to Phase 1
```

**Type 3: Similar Post (Reverse Engineering)**
```
User provides: "Analyze this high-performing post and create something similar"

Actions:
1. Analyze structure (hook type, body format, CTA)
2. Identify engagement patterns (what resonated)
3. Extract framework and core elements
4. Adapt with original angle (don't copy)
5. Create 2 new posts maintaining spirit
```

**Type 4: Blog/Article Conversion**
```
User provides: Long-form blog post or article

Actions:
1. Blog becomes seed content
2. Proceed through full workflow
3. Extract key nuggets (not just summarize)
4. Focus on ONE angle, not entire article
5. Create 2 distinct posts from different angles
```

**STEP 0.2: Research Strategy**

**PRIMARY TOOL:** `web_search_exa`
- Search: "LinkedIn posts about [topic] site:linkedin.com"
- Analyze existing content patterns
- Identify what's working in the space
- Find gaps and unique angles
- Note engagement patterns

**FALLBACK TOOL:** `firecrawl_search` or `firecrawl_scrape`
- Use if Exa unavailable
- Can hybrid: search with Exa, scrape with Firecrawl

**Research Checklist:**
- [ ] Existing LinkedIn posts on similar topics
- [ ] Current frameworks being discussed
- [ ] Statistics and data points (with correct entity context)
- [ ] Unique angle identified
- [ ] Audience pain points validated

**STEP 0.3: Content Planning**

1. **Identify the angle** - What's the unique POV?
2. **Target audience** - Who specifically needs this?
3. **Expected outcome** - What should readers DO after reading?
4. **Hook strategy** - Which framework fits best? (TAS/PAS/SCQA)
5. **Content format** - Listicle? Story? Thought leadership? Advice?

**Reference:** See `references/content-formats.md` for format selection guide

---

### Phase 1: Seed Content Development

**What is Seed Content?**

Seed content is the raw material containing ALL the information needed for your LinkedIn posts. It's comprehensive, researched, and validated - but not yet structured for LinkedIn.

**Seed Content Sources:**

**From Research (Topic Only):**
```
Compile all research findings into one document:
- Key statistics with sources
- Expert opinions and quotes
- Framework details
- Case study information
- Current market trends
- Pain points and challenges
- Solutions and approaches
```

**From Brain Dump:**
```
Structure the thoughts into:
- Main arguments and points
- Supporting evidence
- Personal experiences
- Observations
- Questions to address
- Solutions proposed
```

**From Blog/Article:**
```
The article IS your seed content, but note:
- Focus on ONE key angle, not everything
- Extract 2-3 main nuggets
- Pull supporting stats/examples
- Identify 2-3 different post angles
```

**From Similar Post:**
```
Analyze and document:
- Core message and angle
- Hook structure and technique
- Content flow pattern
- Engagement triggers
- How to adapt without copying
```

**Seed Content Checklist:**
- [ ] All research compiled
- [ ] Statistics with correct entity context
- [ ] Frameworks and methodologies documented
- [ ] Examples and case studies included
- [ ] Pain points clearly identified
- [ ] Solutions articulated
- [ ] Sources/citations noted
- [ ] 2-3 potential angles identified

---

### Phase 2: Reverse Outline

**Purpose:** Extract the structure and key points from your seed content to identify "golden nuggets" - the ideas worth turning into posts.

**Reference:** See `references/workbook-workflow.md` for detailed reverse outline process

**Process:**

1. **Read through seed content completely**
2. **Identify main sections/themes**
3. **Extract key points from each section**
4. **Note supporting evidence for each point**
5. **Identify 3-5 "golden nuggets" - ideas with post potential**

**Reverse Outline Template:**

```
SECTION: [Main theme]
Key Point 1: [Specific insight]
  - Supporting evidence: [Stat/example]
  - Why it matters: [Impact]

Key Point 2: [Specific insight]
  - Supporting evidence: [Stat/example]
  - Why it matters: [Impact]

NUGGETS IDENTIFIED:
1. [Nugget with strong hook potential]
2. [Nugget with counterintuitive angle]
3. [Nugget with practical value]
```

**Evaluation Criteria for Nuggets:**
- [ ] Specific (not generic)
- [ ] Contrarian or unexpected
- [ ] Actionable insight
- [ ] Relevant to target audience
- [ ] Can stand alone as full post
- [ ] Has hook potential

**Output:** List of 3-5 golden nuggets to develop further

---

### Phase 3: The Whole (Y+U+I Analysis)

**Purpose:** Deep dive into WHY, FOR YOU, and FOR ME to extract the most compelling angles.

**Reference:** See `references/workbook-workflow.md` for Y+U+I prompts

**For Each Golden Nugget, Ask:**

**WHY (The Whole - Big Picture)**
- Why does this matter?
- Why is this happening now?
- Why should anyone care?
- Why is the current approach failing?
- Why does this challenge the status quo?

**FOR YOU (The Audience)**
- Why is this relevant to YOUR audience?
- What pain does this solve for THEM?
- What opportunity does this create for THEM?
- What risk does this help THEM avoid?
- What outcome can THEY achieve?

**FOR ME (Your Unique Angle)**
- Why am I the right person to share this?
- What's my unique insight or experience?
- What credibility do I bring?
- What contrarian view do I have?
- What story can only I tell?

**Y+U+I Template for Each Nugget:**

```
NUGGET: [Golden nugget statement]

WHY:
- [Big picture reason 1]
- [Big picture reason 2]
- [Trend or shift driving this]

FOR YOU (Audience):
- [Specific pain point]
- [Outcome they want]
- [Risk they face]

FOR ME (Your angle):
- [Your credibility]
- [Your unique insight]
- [Your POV]

ANGLE EMERGED: [The specific angle to take in the post]
```

**Output:** Refined nuggets with clear angles and positioning

---

### Phase 4: The Parts (Deep Nugget Mining)

**Purpose:** Zoom in and zoom out on each nugget to extract maximum depth and context.

**Reference:** See `references/workbook-workflow.md` for Parts analysis framework

**For Each Nugget with Strong Angle:**

**Face Value**
- What's the surface-level understanding?
- What do most people think this means?
- What's the obvious interpretation?

**Truth**
- What's actually true about this?
- What's the reality beyond face value?
- What's the contrarian truth?

**Assumption**
- What assumptions are people making?
- What do they take for granted?
- What conventional wisdom is wrong?

**Consequences**
- What happens if you ignore this?
- What's the cost of the status quo?
- What opportunity is missed?

**Story**
- Is there a personal story here?
- Is there a case study or example?
- Is there a moment of realization?

**Zoom In (Specific Details)**
- What's a micro-example?
- What's a specific instance?
- What's a tactical detail?

**Zoom Out (Big Picture)**
- How does this connect to larger trends?
- What's the broader implication?
- What's the industry-level impact?

**Parts Analysis Template:**

```
NUGGET: [Statement]

FACE VALUE: [What it seems to be]
TRUTH: [What it actually is]
ASSUMPTION: [What people wrongly believe]
CONSEQUENCES: [What happens if ignored]
STORY: [Example or narrative]

ZOOM IN: [Specific tactical detail]
ZOOM OUT: [Broader industry trend]

POST ANGLE: [Refined angle for post]
```

**Output:** Deep insights ready for hook creation

---

### Phase 5: Hook Creation (MOST CRITICAL PHASE)

**⚠️ SPEND 40% OF YOUR TIME HERE ⚠️**

**Hook frameworks are your religion. Master them.**

**Reference Files (READ THESE):**
- `references/hook-frameworks.md` - Detailed TAS, PAS, SCQA frameworks
- `references/hook-principles.md` - Erica Schneider's teaching
- `references/linkedin-frameworks.md` - 10 proven structures

**The 3 Core Frameworks:**

**1. TAS (Thesis, Antithesis, Synthesis)**
- **Thesis:** Present an opinion or bold claim
- **Antithesis:** Recognize a barrier or counter-argument
- **Synthesis:** Share a way through

**Best for:** Contrarian takes, thought leadership, challenging conventional wisdom

**Example:**
```
Most people think [common belief]. [Opinion on why it's wrong]

But here's the problem: [Barrier]

After [credibility marker], I've learned: [Better approach]
```

**2. PAS (Problem, Agitate, Solution)**
- **Problem:** Identify the challenge upfront
- **Agitate:** Poke the pain to increase relatability
- **Solution:** Present your solution

**Best for:** Pain-focused content, solution selling, addressing struggles

**Example:**
```
Everybody [pain point].

I used to [pain point], too. [Example of struggle]

Here's what changed: [Solution approach]
```

**3. SCQA (Situation, Complication, Question, Answer)**
- **Situation:** Set the stage (current state)
- **Complication:** The challenge this presents
- **Question:** Bridge between problem and solution
- **Answer:** The resolution (dangle the solution)

**Best for:** Educational content, industry insights, methodology posts

**Example:**
```
[Current state with data]

The challenge? [Specific complication]

So what can you do?

[Solution approach]: Here's how
```

**The 4 Foundational Hook Principles:**

**1. Poke at the Pain**
- Light up emotions
- Give something to relate to
- Show you understand their struggle

Examples:
- "Most people struggle with [thing]"
- "I'd tried every prescriptive tip, and nothing worked—until…"
- "Your boss is tired of being your manager"

**2. Add Credibility**
- Social proof
- Specific numbers
- Real experience

Examples:
- "I've edited 3M+ words"
- "We spent 5 years building systems that net us $1M ARR"
- "I've spent 1,500 hours learning about pricing psychology"

**3. Get Specific with Outcomes**
- Let readers picture exactly what they'll accomplish
- Quantify where possible
- Focus on transformation

Examples:
- "Never waste time hiring B-players again"
- "2x conversions in 30 days"
- "Use these 9 questions to save thousands"

**4. Leave a Cliffhanger**
- Pique curiosity
- Open a loop
- Make them want to click "see more"

Examples:
- "I knew what I needed to do"
- "The truth about trolls, bullies, and haters...Is less interesting than you think"

**Hook Creation Process:**

**STEP 1: Select Your Best 2-3 Nuggets**

Choose nuggets with:
- Strong contrarian angle OR
- Clear pain point OR
- Surprising insight OR
- Actionable framework

**STEP 2: Create 4-5 Hooks Per Nugget**

For EACH selected nugget, create:
- 2 TAS hooks (different angles)
- 1 PAS hook
- 1 SCQA hook
- 1 creative/hybrid hook

**Use the hook prompts from:** `references/workbook-workflow.md`

**STEP 3: Evaluate Each Hook**

Hook Quality Checklist:
- [ ] Specific (not generic)
- [ ] Contrarian or unexpected angle
- [ ] Emotional (creates feeling)
- [ ] Relatable (audience sees themselves)
- [ ] Data-driven when relevant
- [ ] Credibility marker included
- [ ] Cliffhanger or open loop
- [ ] Mobile-friendly (scans well)

**STEP 4: Select 2 BEST Hooks**

From all hooks created, select the 2 absolute best that:
- Stop the scroll immediately
- Make you want to keep reading
- Feel natural (not formulaic)
- Match your authentic voice
- Target your specific ICP

**Example Hook Workshop:**

```
NUGGET: "Most SaaS companies use HubSpot wrong - they implement features before cleaning data"

HOOKS CREATED:

Hook 1 (TAS):
Most SaaS scaleups think more HubSpot features = better results.

But I've audited 200+ instances. The pattern is clear:
Complex workflows built on dirty data break more than they help.

The companies getting ROI do one thing first: [cliffhanger]

Hook 2 (TAS - different angle):
Unpopular opinion: Your HubSpot implementation is backwards.

Everyone builds workflows first, cleans data later.
After 200+ audits, I can tell you: it should be the opposite.

Here's why:

Hook 3 (PAS):
73% of SaaS scaleups are underutilizing their HubSpot investment.

That's $50K+ annual spend with minimal ROI.
Revenue teams making decisions without proper data.
Competitors gaining advantage with better attribution.

The fix starts with cleaning your data first:

Hook 4 (SCQA):
HubSpot should give your SaaS company revenue clarity.

But most implementations become data swamps instead.
Dirty data → broken workflows → wrong decisions.

The solution isn't more features. It's this:

Hook 5 (Creative):
I've seen the same HubSpot mistake 200 times.

Smart teams spending $50K+ yearly.
Building complex workflows.
Getting zero attribution clarity.

The problem? They're building on quicksand:

SELECTED HOOKS: Hook 1 and Hook 3
(Hook 1 has strong contrarian angle, Hook 3 has data-driven pain focus)
```

**Output:** 2 selected hooks ready for full post development

---

### Phase 6: Hook Selection & Post Creation

**Now you build complete posts around your 2 selected hooks.**

**For Each Selected Hook:**

**STEP 1: Choose Post Structure**

**Reference:** `references/linkedin-frameworks.md` for 10 proven structures

Match structure to your content type:
- **Listicle** → Use for tactical how-to, mistakes, lessons
- **Story** → Use for personal journey, case studies
- **Thought Leadership** → Use for contrarian takes, predictions
- **Data-Driven** → Use for research, experiments, results
- **Framework** → Use for methodologies, systems, processes

**STEP 2: Build the Body**

**Using your Parts analysis (from Phase 4):**

1. **Hook** (already created)
2. **Context/Setup** (2-3 sentences)
   - Expand on the hook
   - Provide necessary background
   - Set up the main content

3. **Main Content** (body)
   - Use insights from Parts analysis
   - Include Face Value → Truth reveal
   - Add Consequences
   - Incorporate Story if relevant
   - Use Zoom In (specific examples)
   - Use Zoom Out (bigger picture)

4. **Structure with Bullets**
   - LinkedIn loves scannable content
   - Use bullets for lists, steps, examples
   - Keep bullets concise (1 line each)

5. **Call to Action / Engagement Element**
   - Question to spark comments
   - Invitation to share experiences
   - Prompt for engagement

**Content Flow Patterns:**

**Pattern 1: Problem → Insight → Solution**
```
Hook (establish problem)

Context (why this matters)

The insight:
• [Key point 1]
• [Key point 2]
• [Key point 3]

How to apply this:
[Actionable next steps]

What's been your experience with [topic]?
```

**Pattern 2: Story → Lesson → Application**
```
Hook (story opening)

What happened:
[Story development]

The lesson:
[Key insight extracted]

How this applies to you:
• [Application 1]
• [Application 2]
• [Application 3]

What would you do differently?
```

**Pattern 3: Contrarian → Evidence → Recommendation**
```
Hook (contrarian take)

Why most people get this wrong:
[Explanation]

Here's what the data shows:
• [Evidence point 1]
• [Evidence point 2]
• [Evidence point 3]

What to do instead:
[Recommended approach]

Agree or disagree?
```

**STEP 3: Write Both Posts**

Create complete draft for:
- **Post 1** (using Hook 1 + chosen structure)
- **Post 2** (using Hook 2 + chosen structure)

**Content Length Guidelines:**
- Total post: 150-250 words ideal
- Hook: 2-4 sentences (20-40 words)
- Body: 80-150 words
- Bullets: 5-10 points maximum
- CTA: 1-2 sentences

**Output:** 2 complete post drafts ready for formatting

---

### Phase 7: Formatting for Mobile-First

**⚠️ THIS IS CRITICAL - MOST LINKEDIN READING HAPPENS ON MOBILE ⚠️**

**Mobile-First Formatting Rules:**

**RULE 1: One Sentence Per Line**
```
❌ BAD:
HubSpot should give your SaaS company revenue clarity. But most implementations become data swamps instead.

✅ GOOD:
HubSpot should give your SaaS company revenue clarity.

But most implementations become data swamps instead.
```

**RULE 2: Spaces Between Sentences**
```
❌ BAD:
HubSpot should give your SaaS company revenue clarity.
But most implementations become data swamps instead.
Dirty data leads to broken workflows.

✅ GOOD:
HubSpot should give your SaaS company revenue clarity.

But most implementations become data swamps instead.

Dirty data leads to broken workflows.
```

**RULE 3: No Paragraphs (Multiple Sentences Together)**
```
❌ BAD (this is a paragraph):
Most SaaS companies build complex workflows before cleaning their data. This approach is backwards. The workflows break because they're built on unreliable foundations.

✅ GOOD (sentence by sentence):
Most SaaS companies build complex workflows before cleaning their data.

This approach is backwards.

The workflows break because they're built on unreliable foundations.
```

**RULE 4: Short Sentences (10-15 words ideal)**
```
❌ BAD (too long):
After auditing over 200 HubSpot implementations across various SaaS companies at different growth stages, I've identified a consistent pattern.

✅ GOOD (concise):
I've audited 200+ HubSpot implementations.

The pattern is consistent across all growth stages.
```

**RULE 5: Use Bullet Points**
```
✅ GOOD:

The companies getting ROI do three things first:
• Clean their contact database
• Set up basic attribution tracking
• Train their team on essentials

They add complexity only after the foundation is solid.
```

**RULE 6: NO EMOJIS (B2B Professional Tone)**
```
❌ BAD:
Here's what you need to know 🔥
• Clean your data 🧹
• Build workflows ⚙️
• Track results 📊

✅ GOOD:
Here's what you need to know:
• Clean your data
• Build workflows
• Track results
```

**RULE 7: Bold for Emphasis (Sparingly)**
```
✅ GOOD:

The fix isn't more features.

It's **data hygiene first**, then automation.
```

**Formatting Checklist:**
- [ ] One sentence per line
- [ ] Blank line between each sentence
- [ ] No paragraphs (2+ sentences together)
- [ ] Sentences under 15 words when possible
- [ ] Bullets for lists
- [ ] NO emojis anywhere
- [ ] Bold used sparingly (1-2 times max)
- [ ] Scans well on mobile preview

**Mobile Preview Test:**

Visualize your post on a mobile screen:
- Can you scan it in 3 seconds?
- Do the line breaks feel natural?
- Is any sentence too long?
- Does it invite scrolling or scanning?

**Output:** Both posts properly formatted for mobile

---

### Phase 8: 11-Point Editing Framework

**Apply these 11 editing checks to BOTH posts:**

**Reference:** See `editing-checklists/` folder for detailed frameworks

**1. Redundancy Check**
- Remove repeated words/phrases
- Cut "very", "really", "just", "that"
- Eliminate filler words

**2. Active Voice**
- Convert passive constructions
- Make subjects do the action
- Strengthen verb choices

**3. Parallelism**
- Match bullet point structures
- Align sentence patterns
- Create rhythm

**4. Tenses**
- Maintain consistent tense
- Fix tense shifts
- Clarify time references

**5. Sentence Structure**
- Vary sentence length (but keep short)
- Mix simple and compound
- Avoid run-ons

**6. Specificity**
- Replace generic with specific
- Add numbers and examples
- Clarify vague references

**7. Amplify Arguments**
- Strengthen weak claims
- Add evidence where needed
- Increase impact

**8. Structural Strategy**
- Check flow between sections
- Verify logical progression
- Ensure hooks deliver

**9. Takeaway**
- Clarify key message
- Strengthen conclusion
- Ensure CTA is clear

**10. Grammar & Spelling**
- Fix all errors
- Check punctuation
- Verify capitalization

**11. Final Polish**
- Read aloud
- Check mobile formatting again
- Verify no emojis
- Confirm brevity

**Editing Sequence:**

For each post:
1. Read through completely (don't edit yet)
2. Apply frameworks 1-9 in order
3. Framework 10 (grammar) after content is solid
4. Framework 11 (polish) last

**LinkedIn-Specific Edits:**

- Remove corporate jargon
- Eliminate buzzwords ("synergy", "leverage", "disrupt")
- Cut salesy language ("game-changer", "revolutionary")
- Strengthen personal voice
- Add contrarian edge where appropriate

**Output:** Both posts fully edited and polished

---

### Phase 9: Final Review & Delivery

**CRITICAL FINAL CHECKS:**

**Content Quality:**
- [ ] Hook stops the scroll immediately
- [ ] Strong POV throughout (not vanilla)
- [ ] Specific examples and data
- [ ] Logical flow and structure
- [ ] Clear value proposition
- [ ] Engagement element present

**Formatting Quality:**
- [ ] One sentence per line ✓
- [ ] Spaces between sentences ✓
- [ ] No paragraphs ✓
- [ ] Short sentences (10-15 words) ✓
- [ ] Bullets used properly ✓
- [ ] NO EMOJIS ✓
- [ ] Bold used sparingly ✓

**Mobile Test:**
- [ ] Scan in 3 seconds on mobile
- [ ] Natural line breaks
- [ ] Easy to read while scrolling
- [ ] Invites engagement

**Voice & Tone:**
- [ ] Authentic (not robotic)
- [ ] Confident (not hedging)
- [ ] Professional (not casual)
- [ ] Direct (not verbose)

**Strategic Alignment:**
- [ ] Matches original seed content angle
- [ ] Serves target audience need
- [ ] Differentiates from existing content
- [ ] Builds authority/credibility

**Final Deliverables:**

Present both posts in this format:

```
## POST 1

[Hook Framework Used: TAS/PAS/SCQA]
[Content Format: Listicle/Story/Thought Leadership/etc.]

[Complete post text with proper formatting]

---

Word Count: [X words]
Estimated Read Time: [X seconds]
Target Audience: [Who this is for]
Key Message: [Main takeaway]

---

## POST 2

[Hook Framework Used: TAS/PAS/SCQA]
[Content Format: Listicle/Story/Thought Leadership/etc.]

[Complete post text with proper formatting]

---

Word Count: [X words]
Estimated Read Time: [X seconds]
Target Audience: [Who this is for]
Key Message: [Main takeaway]
```

**Usage Notes for Each Post:**

For each post, provide:
- Best time to post (based on content type)
- Suggested hashtags (3-5 maximum)
- Engagement strategy (how to respond to comments)
- Potential follow-up content ideas

---

## 🎯 Success Metrics

**Engagement Hierarchy (Most to Least Valuable):**

1. **Comments** - Most valuable (indicates real engagement)
2. **Shares/Reposts** - High value (expands reach)
3. **Profile views** from target audience
4. **Connection requests** from ICP
5. **DMs** - High intent
6. **Likes** - Least important (vanity metric)

**Remember:** 100 engaged followers > 1,000 passive followers

---

## 🚫 Common Mistakes to Avoid

**Content Mistakes:**
- Generic hooks that could apply to anything
- No clear POV or perspective
- Overly promotional or salesy
- Too long (over 300 words)
- Boring/vanilla content without edge

**Formatting Mistakes:**
- Using paragraphs (multiple sentences together)
- Using emojis in B2B content
- Sentences that are too long
- No spaces between sentences
- Inconsistent formatting

**Hook Mistakes:**
- Starting with a question
- Being too clever/cryptic
- No credibility marker
- Vague outcomes
- Clickbait without substance

**Strategic Mistakes:**
- Writing for everyone (not niche enough)
- Copying trending formats without authenticity
- Ignoring mobile preview
- No clear CTA or engagement element
- Not researching existing content first

---

## 💡 Pro Tips

**Hook Development:**
- Create 4-5 options, select 2 best
- Test hooks by reading first 2 lines only
- If you wouldn't stop scrolling, rewrite
- Contrarian > agreeable
- Specific > generic

**Writing Process:**
- Write hook first, always
- Let hook guide the entire post
- Rewrite to make post flow from hook
- Natural bridges between sections
- End strong (not weak)

**Formatting:**
- Preview on mobile before finalizing
- Read aloud to check flow
- Less is more (cut ruthlessly)
- White space is your friend
- Bullets increase scannability

**Engagement:**
- Respond to every comment in first hour
- Ask questions to spark discussion
- Share authentic experiences
- Be willing to disagree respectfully
- Follow up with commenters

---

## 📚 Additional Resources

**For Deep Dives:**
- Hook creation → `references/hook-frameworks.md`
- Workflow details → `references/workbook-workflow.md`
- Post structures → `references/linkedin-frameworks.md`
- Editing checklist → `references/editing-framework.md`

**For Examples:**
- Successful posts → `examples/high-performing-posts.md`
- Hook analysis → `references/hook-principles.md`
- Format variety → `references/content-formats.md`

---

## ✅ Workflow Checklist

Use this to track progress through all phases:

**Phase 0: Strategic Planning**
- [ ] Input type identified (topic/brain dump/article/post)
- [ ] Research completed (existing LinkedIn content)
- [ ] Unique angle determined
- [ ] Target audience confirmed
- [ ] Content format selected

**Phase 1: Seed Content**
- [ ] All research compiled
- [ ] Statistics validated (correct entity)
- [ ] Examples documented
- [ ] 2-3 angles identified

**Phase 2: Reverse Outline**
- [ ] Seed content reviewed
- [ ] Main sections identified
- [ ] 3-5 golden nuggets extracted

**Phase 3: Y+U+I Analysis**
- [ ] WHY explored for each nugget
- [ ] FOR YOU (audience) clarified
- [ ] FOR ME (your angle) defined
- [ ] Angles refined

**Phase 4: Parts Analysis**
- [ ] Face Value identified
- [ ] Truth revealed
- [ ] Assumptions challenged
- [ ] Consequences outlined
- [ ] Stories collected
- [ ] Zoom In/Out completed

**Phase 5: Hook Creation**
- [ ] 4-5 hooks per nugget created
- [ ] All 3 frameworks used (TAS/PAS/SCQA)
- [ ] Hook quality checklist applied
- [ ] 2 best hooks selected

**Phase 6: Post Creation**
- [ ] Structure chosen for each post
- [ ] Body built using Parts analysis
- [ ] Bullets added for scannability
- [ ] CTAs included
- [ ] Both posts drafted

**Phase 7: Mobile Formatting**
- [ ] One sentence per line
- [ ] Spaces between sentences
- [ ] No paragraphs
- [ ] Short sentences (10-15 words)
- [ ] Bullets formatted properly
- [ ] NO emojis
- [ ] Mobile preview checked

**Phase 8: Editing**
- [ ] Redundancy removed
- [ ] Active voice applied
- [ ] Parallelism checked
- [ ] Tenses consistent
- [ ] Sentence structure varied
- [ ] Specificity increased
- [ ] Arguments amplified
- [ ] Structure optimized
- [ ] Takeaways clear
- [ ] Grammar perfect
- [ ] Final polish complete

**Phase 9: Final Review**
- [ ] Content quality verified
- [ ] Formatting quality confirmed
- [ ] Mobile test passed
- [ ] Voice & tone authentic
- [ ] Strategic alignment confirmed
- [ ] Both posts ready to publish

---

## 🎓 Skill Philosophy

**This skill is built on three core beliefs:**

1. **Hooks are sacred** - A mediocre hook dooms even great content. Spend the time to get it right.

2. **Mobile-first wins** - Most LinkedIn reading happens on phones. Format accordingly or lose readers.

3. **Strong POV required** - Vanilla, agreeable content gets ignored. Have an opinion. Defend it.

**Use this skill to:**
- Create high-performing LinkedIn content systematically
- Develop hooks that stop the scroll
- Format posts that mobile readers love
- Build authority and engage your target audience
- Turn ideas into posts that drive real business results

**The skill works when you:**
- Follow the 9-phase workflow completely
- Spend serious time on hooks (Phase 5)
- Respect mobile formatting rules
- Apply all 11 editing frameworks
- Maintain strong POV throughout

---

## 🚀 Ready to Create?

Start with Phase 0 (Strategic Planning).

Read the reference files.

Follow the workflow.

Create posts that stop the scroll.

**Remember:** Hooks are your religion. Mobile-first is your mantra. Strong POV is your differentiator.

Now go create LinkedIn posts that actually work.

---

*This skill represents the distilled wisdom of Erica Schneider, Matt Swain, Anthony Pierri, and analysis of thousands of high-performing B2B LinkedIn posts. Use it well.*
