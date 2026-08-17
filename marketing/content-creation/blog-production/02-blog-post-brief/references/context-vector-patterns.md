# Context and Vector Writing Patterns (v4)

## CONTEXT Column - Directive Language Guide

### What is CONTEXT?
The CONTEXT column provides **conversational, directive instructions** to the copywriter on exactly what to write in each section. It uses action verbs to guide the writer through the content creation process.

### Action Verb Patterns

**Opening/Starting:**
- **Start with =>** "Start with a clear definition of [topic], emphasizing their purpose..."
- **Open by** "Open by establishing the transformation from X to Y..."
- **Begin with** "Begin with a comprehensive overview of..."

**Explaining/Defining:**
- **Explain** "Explain how [X] transforms [Y] into actionable intelligence..."
- **Define** "Define [term] as a system that..."
- **Describe** "Describe the process of..."
- **Detail** "Detail the configuration process in Settings > ..."

**Discussing/Exploring:**
- **Discuss** "Discuss how technology enables RevOps by..."
- **Explore** "Explore the role of [X] in [Y]..."
- **Dive into** "Dive into specific use cases for..."

**Emphasizing/Highlighting:**
- **Emphasize** "Emphasize the importance of tools for..."
- **Highlight** "Highlight that includes examples of..."
- **Stress** "Stress the distinction between..."

**Including Specifics (v4 Enhanced):**
- **Include** "Include STAT_01 (47% better conversion, Forrester) in opening..."
- **Provide** "Provide baseline recommendations..."
- **Address** "Address the common misconception that..."
- **Note** "Note the 10 credits per company cost structure..."
- **Use** "Use STAT_02 to support the ROI claim..."

**Structuring Content:**
- **Introduce** "Introduce the three main pillars..."
- **Break down** "Break down the primary responsibilities..."
- **Use subheadings** "Use subheadings to explore each in detail..."

**Concluding:**
- **Conclude** "Conclude with actionable next steps..."
- **Summarize** "Summarize the key benefits..."
- **End with** "End with a clear CTA..."

---

## v4 Enhancement: Statistics Assignment in CONTEXT

**Always reference statistics by their STAT_ID:**

```
CONTEXT (v4 style):
"Open by establishing the transformation from blind outreach to data-driven targeting. 
Include STAT_01 (47% better conversion, Forrester) to justify the importance. Define 
HubSpot Buyer Intent as a three-component system. Use STAT_02 (70% B2B journey, Forrester) 
if relevant but note this may be excluded if used elsewhere in cluster..."
```

---

## H1 Context Pattern (v4)

For H1 headings, the CONTEXT should:
1. Establish the transformation or problem-solution
2. Define the main concept comprehensively
3. Set expectations for what the guide covers
4. **Include assigned statistic with STAT_ID**
5. Specify the target audience

**Example (v4):**
```
"Open by establishing the transformation: from blind outreach to data-driven ABM targeting. 
Include STAT_01 (companies using intent data see 47% better conversion, Forrester) in the 
opening paragraph. Define HubSpot Buyer Intent as a three-component system (Visitor Intent, 
Research Intent, Intent Signals) that identifies high-intent accounts at the company level, 
not individual leads. Emphasize this is about account-based intelligence, not lead scoring. 
Set expectations that this guide covers complete configuration from market setup to workflow 
automation, specifically for B2B RevOps teams implementing ABM strategies. NOTE: Do not 
repeat basic intent definitions covered in /blog/buyer-intent-basics."
```

**Word count guidance:** H1 context should be 100-150 words

---

## H2 Context Pattern (v4)

For H2 headings, the CONTEXT should:
1. Start with the main action for the section
2. List specific components or steps to cover
3. Include examples or specifics
4. **Reference any assigned statistics**
5. Address misconceptions if relevant
6. Note important details or costs
7. **Note content to avoid (from linked articles)**

**Example (v4):**
```
"Explain the three distinct components in detail. Start with Visitor Intent and how it uses 
reverse-IP tracking to identify companies (not individuals) visiting your website. Then 
discuss Research Intent - include STAT_03 (2.3x more opportunities, Aberdeen) here. Finally, 
detail Intent Signals that track company-level events like funding rounds. Clarify that these 
work independently but can be layered. Address the misconception that this tracks individuals. 
Include the cost structure: 10 credits per company. NOTE: Basic IP tracking explanation is in 
/blog/visitor-tracking - focus on intent application here, not general tracking."
```

**Word count guidance:** H2 context should be 75-100 words

---

## H3 Context Pattern (v4)

For H3 headings, the CONTEXT should:
1. Provide specific navigation or configuration steps
2. Detail parameters and settings
3. Explain the logic or rationale
4. Provide baseline recommendations
5. Note technical details
6. **No statistics typically needed at H3 level**

**Example (v4):**
```
"Navigate to Marketing > Buyer Intent > Configuration > Intent section. Define visitor 
intent criteria based on website behavior patterns. Set parameters for: number of page 
visits (recommend 3+ visits), specific page paths (pricing, demo, case studies), visit 
recency (last 7, 14, or 30 days). Explain the logic: higher thresholds reduce noise but 
may miss early-stage interest. Provide baseline recommendation: 3 visits to high-intent 
pages within 14 days from 2+ visitors. Note retroactive analysis capability."
```

**Word count guidance:** H3 context should be 50-75 words

---

## VECTOR Column - Topical Relationship Patterns

### What is VECTOR?
The VECTOR column describes how each section connects to the overall topical map and maintains the context vector throughout the article. It ensures semantic coherence and topical flow.

### H1 Vector Patterns

**Foundation Setting:**
- "Core of the context vector: establishing the foundation for all subsections..."
- "Establishes comprehensive scope while immediately differentiating from basic feature overviews..."
- "Sets up the three-pillar structure that the rest of the article follows..."

### H2 Vector Patterns

**Key Sections:**
- "KEY PARAGRAPH: Central anchor for the context vector, linking directly to subtopics..."
- "Central component connecting to subtopics in the topical map..."
- "Creates the framework for understanding all subsequent sections..."

**Building/Progression:**
- "Establishes foundational understanding before diving into implementation..."
- "Builds from component understanding to practical implementation..."
- "Transitions from theory to hands-on configuration..."

**Connecting:**
- "Ties [concept] to [broader strategy], reinforcing its centrality to operational success..."
- "Connects the concept to broader data management and ABM strategies..."
- "Links operational efficiency to measurable business outcomes..."

### H3 Vector Patterns

**Supporting Details:**
- "Provides granular configuration details for the first intent component..."
- "Descendant topic that directly supports the parent section..."
- "Ties in contextually to [parent topic] within the topical map..."
- "Drills down into specific implementation within the broader framework..."

---

## WORD_TARGET Column (NEW in v4)

### Standard Targets by Section Type

| Section Type | Word Target | Notes |
|--------------|-------------|-------|
| H1 Introduction | 200-250 | Hook, stat, overview |
| H2 Definition | 150-200 | Concept explanation |
| H2 How-To | 250-350 | Detailed steps |
| H2 Framework | 200-250 | Structure explanation |
| H3 Configuration | 150-200 | Specific steps |
| H3 Example | 100-150 | Illustrative content |
| Conclusion | 100-150 | Summary, CTA |

### Adjusting Word Targets

**Increase target when:**
- Section has many substeps
- Complex concepts need more explanation
- Multiple examples needed

**Decrease target when:**
- Simple concept
- Reference to other content
- Mostly visual/table content

---

## Quality Checklist for CONTEXT (v4)

- [ ] Uses action verbs (Start with, Explain, Discuss, etc.)
- [ ] Provides specific instructions, not vague descriptions
- [ ] **References assigned statistics by STAT_ID**
- [ ] Mentions misconceptions to address (if relevant)
- [ ] Specifies navigation paths or settings (for technical topics)
- [ ] Conversational and directive, not passive
- [ ] **Notes content to avoid from linked articles**
- [ ] 75-150 words of detailed guidance

## Quality Checklist for VECTOR

- [ ] Describes topical relationship clearly
- [ ] Uses appropriate pattern (foundation, key paragraph, builds from, ties to)
- [ ] Shows how section connects to overall article
- [ ] Maintains context vector coherence
- [ ] Indicates if section is central anchor or supporting detail

## Quality Checklist for WORD_TARGET (v4)

- [ ] Every heading has a word target
- [ ] Targets appropriate for section type
- [ ] Total targets sum to article word count (±100)
- [ ] Complex sections have higher targets
- [ ] Simple sections have lower targets
