# Research Documentation: HubSpot Research Intent

**Keyword:** HubSpot research intent
**Date:** 2025-01-02
**Version:** v4

---

## STATISTICS EXCLUSION REGISTRY

### Already Used in Cluster:
| Statistic | Source | Used In |
|-----------|--------|---------|
| "75% of RevOps see 10-20% growth" | Gartner | /blog/revops-maturity-model |
| "36% better customer retention" | Forrester | /blog/crm-implementation-guide |
| "Companies using CRM see 29% revenue increase" | Salesforce | /blog/hubspot-roi |
| "87% report skills gaps in RevOps" | McKinsey | /blog/revops-team-structure |

### FORBIDDEN STATISTICS (Site-Wide):
- Gartner 75% RevOps stat (overused across 5+ articles)
- BCG 70% transformation fail (cliché)
- McKinsey 87% skills gap (overused)
- Forrester 36% retention (used in multiple pieces)

---

## INTERNAL ARTICLE DIFFERENTIATION

### Existing Article 1: Buyer Intent Basics Guide
- **URL:** /blog/buyer-intent-basics
- **Covers:** Intent definition, three intent types overview, basic HubSpot setup
- **DO NOT REPEAT:** Basic intent definitions, component overview, getting started steps
- **THIS ARTICLE ADDS:** Advanced configuration, threshold optimization, ROI calculation, credit cost strategies

### Existing Article 2: B2B Buyer Journey Guide
- **URL:** /blog/b2b-buyer-journey
- **Covers:** Journey stages, touchpoint mapping, content alignment
- **DO NOT REPEAT:** Journey stage definitions, basic touchpoint concepts
- **THIS ARTICLE ADDS:** Why research stage specifically matters, competitive timing advantage

### Existing Article 3: HubSpot Workflows Guide
- **URL:** /blog/hubspot-workflows
- **Covers:** Workflow creation, triggers, actions, basic automation
- **DO NOT REPEAT:** Basic workflow setup, trigger types, action configuration
- **THIS ARTICLE ADDS:** Intent-specific workflow logic, score-based branching, nurture optimization

---

## Entity Architecture

### Research Intent
Early-stage buyer behavior indicating information gathering phase. Typically 3-6 months before purchase decision.

**Relationships:**
- Part of broader "buyer intent" category
- Precedes consideration and decision stages
- Detected through content consumption patterns
- Different from commercial or transactional intent
- NOT the same as Breeze Intelligence (which is a data service)

### HubSpot Intent Tracking
Native behavioral tracking within HubSpot platform that monitors user actions on your properties.

**Relationships:**
- Captures first-party data from your website/content
- Feeds into lead scoring models
- Triggers marketing automation workflows
- Part of Marketing Hub Professional+
- Separate from third-party intent data

### Breeze Intelligence
HubSpot's data enrichment service providing third-party intent signals.

**Relationships:**
- Separate from native HubSpot tracking (NOT the same thing)
- Provides external intent data about company research activity
- Integrates with CRM records
- Uses credits (10 per company)
- NOT the same as behavioral scoring

---

## Common Misconceptions Identified

1. **Research Intent = Breeze Intelligence**
   - FALSE: Research intent is a stage/behavior type
   - Breeze Intelligence is a data service
   - They work together but are separate entities

2. **Research Intent = Ready to Buy**
   - FALSE: Research indicates early stage (3-6 months)
   - Purchase intent indicates readiness (<30 days)
   - Significant gap exists between stages

3. **All Intent Data is the Same**
   - FALSE: First-party (your site) vs third-party (across web)
   - Behavioral (actions) vs firmographic (company data)
   - Real-time vs aggregated historical

---

## Competitor Analysis

### Competitor 1
**URL:** https://blog.hubspot.com/marketing/buyer-intent-data-guide
**Angle:** Feature-focused, explaining HubSpot's intent capabilities
**Content Gaps:**
- Doesn't distinguish research vs purchase intent clearly
- No practical scoring threshold examples
- Missing ROI calculations
- No credit cost optimization strategies

### Competitor 2
**URL:** https://www.6sense.com/blog/intent-data-b2b-marketing
**Angle:** Third-party intent data focus, vendor-specific
**Content Gaps:**
- No HubSpot integration details
- Lacks first-party tracking comparison
- Too focused on their solution
- Missing time decay discussion

### Competitor 3
**URL:** https://www.demandgenreport.com/features/industry-insights/research-intent-signals
**Angle:** Industry overview, vendor-agnostic
**Content Gaps:**
- No implementation details
- Missing specific platform guidance
- Too theoretical, no scoring examples
- No ROI framework

---

## Statistics Inventory

### STAT_01
- **Statistic:** "70% of the B2B buyer journey happens before contacting sales"
- **Source:** Forrester Research
- **Year:** 2024
- **Use In:** H1 - intro paragraph
- **Context:** Emphasizes importance of catching research phase early

### STAT_02
- **Statistic:** "Companies showing research intent are 2.3x more likely to become opportunities within 6 months"
- **Source:** Aberdeen Group
- **Year:** 2024
- **Use In:** H2-1 (Why Research Intent Matters)
- **Context:** Supports strategic value of early detection

### STAT_03
- **Statistic:** "67% of B2B buyers consume 3+ pieces of content before engaging sales"
- **Source:** DemandGen Report
- **Year:** 2024
- **Use In:** H2-3 (How HubSpot Detects)
- **Context:** Supports content-based tracking approach

### STAT_04
- **Statistic:** "Intent-driven campaigns generate 4x more pipeline than traditional approaches"
- **Source:** 6sense State of B2B Buying Report
- **Year:** 2024
- **Use In:** H2-5 (Building Automated Workflows)
- **Context:** Justifies automation investment

---

## Content Gaps to Address

1. **Clear distinction between research/consideration/decision intent**
   - Opportunity: No competitor clearly maps stages with timing and examples

2. **Practical scoring thresholds and point values**
   - Opportunity: Most content is theoretical - we provide specific numbers

3. **Time decay implementation**
   - Opportunity: Not addressed by competitors - critical for accuracy

4. **Credit cost optimization for Breeze Intelligence**
   - Opportunity: Unique angle competitors don't cover

5. **ROI measurement methodology with formula**
   - Opportunity: Everyone claims ROI, few show calculation method

---

## Interlinking Strategy

### Link 1: ABM Strategy Guide
- **URL:** /blog/abm-strategy-hubspot
- **Anchor Text:** "account-based marketing strategy"
- **Place In:** H2 about combining first and third-party data
- **DO NOT REPEAT FROM LINKED ARTICLE:**
  - Basic ABM definition
  - ICP framework explanation
  - Target account list creation

### Link 2: Lead Scoring Setup
- **URL:** /blog/lead-scoring-hubspot
- **Anchor Text:** "behavioral scoring model"
- **Place In:** H3 about configuring thresholds
- **DO NOT REPEAT FROM LINKED ARTICLE:**
  - Score property creation basics
  - General point value recommendations
  - Basic threshold concepts

### Link 3: HubSpot Workflows Guide
- **URL:** /blog/hubspot-workflows
- **Anchor Text:** "automated workflows"
- **Place In:** H2 about building automation
- **DO NOT REPEAT FROM LINKED ARTICLE:**
  - Workflow creation steps
  - Basic trigger configuration
  - Action setup fundamentals

---

## MAN Digital Angle

- **Process Focus:** Design the intent identification process first, then configure HubSpot
- **Implementation Reality:** Acknowledge 2-3 month optimization period needed
- **Practical Examples:** Use real scoring scenarios with specific numbers
- **Eastern European Skepticism:** Don't oversell - intent data helps but isn't magic
- **RevOps Efficiency:** Show hours saved through automation, not vague benefits
- **Cost Transparency:** Include credit costs and ROI calculations

---

## Writing Notes

- Start sections with one-sentence definitions
- Use research-stage content examples (whitepapers, guides, webinars)
- Include specific scoring values (+5, +10, +20 points)
- Reference HubSpot navigation paths (Settings > Properties > Score)
- Acknowledge that not all industries have good intent data available
- Provide monthly optimization timeline expectations
- Always reference statistics by STAT_ID in the writing
- Check WORD_TARGET for each section - stay within ±10%
