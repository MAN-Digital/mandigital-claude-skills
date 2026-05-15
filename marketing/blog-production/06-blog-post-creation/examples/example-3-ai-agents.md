# HubSpot's 22 AI Agents: Automating RevOps for Marketers (_Guide and AI Credit Calculator Included)_

HubSpot launches 22 built-in agents that automate marketing, sales, and service workflows. This joins the 66% of marketers ([_HubSpot AI Trends for Marketers_](https://offers.hubspot.com/ai-marketing)_)_ using AI to scale operations while concentrating on strategic revenue growth.

Most features are in beta and tie directly to native tools. They are free during beta with _no credits required. This means_ you should test high-impact agents now before pricing begins. The real opportunity lies in integrations and custom builds beyond native capabilities.

How to prioritize:

- Start with the <u>Customer Agent</u> for ticket queues, the agent that eliminates your biggest time sink.
- <u>Prospecting Agent</u> for SDR research,
- <u>Data Agent</u> for property hygiene.

## What is HubSpot Breeze AI?

Breeze AI automates routine tasks, learns from your data, and connects your stack to shift your focus from admin to revenue work.

Imagine 30% more selling time for reps, 50% faster lead response, and clean data without manual entry.

**Why this shift matters:** faster handoffs, fewer dropped balls, reliable dashboards.

It operates in two modes:

- **Agents** function as AI employees. For example, the Prospecting Agent monitors 100 contacts monthly and drafts personalized outreach when buying signals appear.

  - How: set signals (job change, intent), define sequences, and require approval before sending for the first 30 days.
- **Assistants** analyze data and create content, like asking '_What deals closed last quarter?_' but can't send reminders.

  - Use when you need insight or drafts without risk of execution.

Why two modes? Not every task should run on autopilot. Assistants remain read-only, while agents execute with guardrails.

![](https://lex-img-p.s3.us-west-2.amazonaws.com/img/f4a876c0-1c82-49f0-a0f3-e68887094728-RackMultipart20251016-192-8k5z5d.jpeg)

You manage every aspect of your AI team:

- Define outcomes and KPIs, ensuring _AI aligns with revenue objectives._
- Gate data access by role to protect _sensitive deal information._
- Customize tone and voice to match your brand while maintaining _trust with enterprise buyers._
- Build rules and guardrails to protect your process, preventing _expensive automation errors._

These AI tools use your HubSpot data and connected apps while your team maintains control through reviews, approvals, and audit trails for significant actions.

## Agents vs Assistants

![](https://lex-img-p.s3.us-west-2.amazonaws.com/img/e5e80194-55bb-4626-98de-c084f4e42604-RackMultipart20251017-160-zwuo5y.jpeg)

Breeze Studio offers two distinct configuration paths:

- **Assistants** analyze CRM data and browse the web for insights.
- **Agents** read data and execute actions through tools and MCP servers.

When to use which:

- **Assistant:** Ask questions, such as “_How many contacts came from Google Ads last week?_” or draft responses.
- **Agent:** Enforce processes such as enriching leads, scoring opportunities, updating properties, notifying owners, or creating content.

## Anatomy of an AI Agent

![](https://lex-img-p.s3.us-west-2.amazonaws.com/img/12efaf6c-227e-4009-b107-454056cbc836-RackMultipart20251017-149-ion3ni.jpeg)

Every agent builds on three fundamental elements:

1. **Instructions**

- **The system prompt** defines the role, rules, goals, tone, and guidelines.
- Optional **welcome message** and prompt patterns for common tasks

2. **Capabilities (what it can do)**

- **Tools:** Fetch data, generate content, and take action.
- **MCP servers:** External services and APIs

3. **Knowledge**

- Private knowledge base: brand guidelines, ideal customer profiles, FAQs, product documentation, service agreements, and company policies.
- Limit knowledge to 3–5 core files for targeted, on-brand outputs.

The configuration formula:

- **Assistants** = Instructions + Knowledge + Read-only access
- **Agents** = Instructions + Knowledge + Action tools or MCP

## How AI Agents Use Tools and MCP Servers

![](https://lex-img-p.s3.us-west-2.amazonaws.com/img/0987e479-937c-497f-99ef-fffdc8616bd9-RackMultipart20251017-140-jmwgqj.jpeg)

- **Tools** let agents fetch records, update properties, send messages, and generate content. Custom tools development is in beta, allowing you to create your own.

- **MCP servers** provide secure "world connections" for your agents. They support HubSpot by connecting to Asana, Jira/Atlassian, and Notion, with additional options as developers build new MCPs. You _can develop yours_.

## 22 Native HubSpot Breeze Agents & Assistants (Beta)

HubSpot's library includes 22 AI agents and assistants you can use right away.

This overview reflects the current Breeze catalog. Plans and credits remain in beta and will change.

_Why we like them:_ native security, faster setup, and lower maintenance than using multiple point tools.

Agent/Assistant Name

Description

Required Plan

Credit Usage

**Customer Agent**

Resolves customer conversations via chat, email, WhatsApp, and more; updates CRM in real time; escalates as necessary.

Service Hub Professional+ (often available in Marketing Hub as well)

100 credits per text conversation

**Prospecting Agent**

Monitors contacts for buying signals, researches companies, and drafts personalized outreach.

Sales Hub Professional+

\- 100 credits per monitored contact monthly. \- 10 credits per company research.

**Data Agent**

Answers record-specific questions, fills data gaps, and provides insights from Smart CRM.

Hub Professional+

10 credits per prompt response

**Closing Agent**

Assists late-stage deals with immediate pricing/quote answers from your content.

Sales Hub Professional+

No credits (beta)

**Company Research Agent**

Produces background briefs on target accounts from public signals and CRM.

Sales Hub Professional+

No credits (beta)

**Deal Loss Agent**

Analyzes lost deals, identifies patterns, and recommends actions to regain business.

Sales Hub Professional+

No credits (beta)

**Blog Research Agent**

Research topics and draft high-quality posts that reflect the brand voice.

Marketing Hub Professional+

No credits (beta)

**Social Post Agent**

Turns calendar events and briefs into social posts ready for channels.

Marketing Hub Professional+

No credits (beta)

**RFP Agent**

Auto-fills RFPs using approved past responses and knowledge.

Any Hub Professional+

No credits (beta)

**Customer Health Agent**

Scores customer health, identifies risk/opportunity, and suggests next actions.

Service Hub Professional+

No credits (beta)

**Customer Handoff Agent**

Creates structured handoff briefs using CRM and interaction data (Sales to CS, etc.).

Service Hub Professional+

No credits (beta)

**Sales to Marketing Feedback Agent**

Converts sales insights into practical content and campaign feedback.

Marketing Hub Professional+

No credits (beta)

**Cross-sell/Upsell Agent**

Explore expansion opportunities and create offers for current customers.

Sales or Service Hub Professional+

No credits (beta)

**Personalization Agent**

Audits content and segments, then suggests tailored variants by audience.

Marketing Hub Professional+

No credits (beta)

**Landing Pages for Events Agent**

Generates branded event landing pages from Marketing Event IDs.

Content/Marketing Hub Professional+

No credits (beta)

**Shopify Store Performance Agent**

Reports ecommerce metrics and trends; suggests actions.

CMS/Commerce Hub Professional+

No credits (beta)

**Call Recap Agent**

Transforms call/meeting transcripts into notes, action items, and follow-ups.

Sales/Service Hub Professional+

No credits (beta)

**Developer Tool Testing Agent**

Helps developers test custom tools and integrations for agents.

Any Hub with developer access

No credits (beta)

**Internal FAQ Assistant**

Answers employees' internal FAQs using authorized information.

Any Hub Professional+

No credits (beta)

**Brand Assistant**

Enforces brand voice and style in marketing content.

Marketing Hub Professional+

No credits (beta)

**Sales Coach Assistant**

Provides call-specific coaching and guidance for representatives.

Sales Hub Professional+

No credits (beta)

**ICP Assistant**

Tests and refines ideas and messaging against your ideal customer profiles.

Any Hub Professional+

No credits (beta)

_Note: Credit requirements may change after the beta phase._

## What are the 4 main AI agents in HubSpot?

![](https://lex-img-p.s3.us-west-2.amazonaws.com/img/2ab7c02f-20f5-4d79-abd8-7a0ee80179c4-RackMultipart20251018-219-9saurj.jpeg)

Four flagship AI agents integrate into the platform's UI and workflows, each solving specific revenue challenges. Start _with the one matching your biggest time sink_:

- **Social Agent** automates post creation, scheduling, and engagement. It uses AI-generated visuals and tailored optimization for each platform.
- **Prospecting Agent** monitors contacts, researches companies, and drafts personalized outreach sequences based on buying signals.
- **The Customer Agent handles** support conversations via chat, email, and WhatsApp, updates CRM data in real-time, and escalates issues to human agents.
- **Data Agent** generates insights and responses for specific records, analyzes trends, and surfaces intelligence from your CRM data.

_These flagship agents provide native AI capabilities with deeper integration than marketplace apps. Additional specialized agents extend these core functions for specific use cases._

## How HubSpot Credits Work

HubSpot Credits power AI features across the platform. Your monthly allocation depends on your subscription tier:

Subscription

Monthly Credits

Starter

500

Professional

3,000

Enterprise

5,000

**What uses credits:**

- **Customer Agent**: 100 credits per conversation (~$1)
- **Smart Properties**: 10 credits per field per record
- **Data Enrichment**: 10 credits per enriched record
- **Prospecting Agent**: 10 credits per new company added
- **AI Workflow Actions**: 10 credits per Breeze action

**Key points:**

- Credits reset monthly with no carryover.
- Additional credits cost $10 per 1,000.
- Set monthly spending limits.
- Beta features are free now, but they will consume credits later. Plan to avoid unexpected charges.

**Prioritize credits by impact:**

- Customer Agent for support teams (_immediate CSAT improvement_),
- Focus on target accounts and open opportunities for data enrichment for high-value leads.
- First, test other sandbox features — validate credit burn versus outcome.
- Assign credit ownership to RevOps for control, and publish a monthly usage report.

## Conclusion

Start with a small, effective AI team.

It depends on your GTM motion, but the pattern remains: start narrow, tie each agent to one KPI, and expand when the revenue impact shows. Focus prevents “_AI overload_” and preserves credits.

These tools don't replace your team. They eliminate the administrative burden, allowing Marketing, Sales, and Service to work more efficiently on pipeline and retention.

**How we measure:**

- Speed-to-lead,
- SLA adherence,
- Data completeness,
- Win rate
- CSAT (_Customer Satisfaction Score_)
- NRR (_Net revenue retention_)

Key insights:

- Keep humans central: ensure approvals for sensitive changes, provide clear guidelines, and maintain audit logs.

- Use tools for repeatability. Use MCP to transform insights into cross-app actions.

- Business metrics: speed-to-lead, resolution time, data completeness, win rate, CSAT, NRR.

**Next steps (90 days):**

1. **Baseline (Weeks 1-2)**: Audit data health (target: _80% contact completeness_), measure SLAs (baseline: current response time), identify manual tasks (find 5+ automation opportunities), and select team KPIs (pick 1 per department).

  - How: export properties, flag fields with <50% fill, enable Smart Properties for the top 5 fields, and publish a KPI tracker.
2. **Pilot (Weeks 3–6)**: Launch targeted pilots and add success metrics to each to define success.

  1. Marketing: Deploy Social Assistant for campaign enhancement — measure time saved and engagement increase.
  2. Sales: Launch Prospecting Agent for contact monitoring. The agent will monitor 100 contacts, approve before sending, and track reply rate and meetings.
  3. Service: Implement Customer Agent for triage support — enforce escalation rules, target FRT < 20 minutes
3. Operationalize (Weeks 7–12):

Add human checkpoints, publish role-based dashboards, and extend MCP to Asana, Notion, and Jira for smooth handoffs.

  - **How**: add required approvals, log actions, and automatically create tickets/docs on triggers.
4. Hold a 30-day review to assess KPIs. If they improve, add one more use case per team; if not, refine instructions, tools, or knowledge.

  - Use a simple post-mortem: what worked, what broke, what to change next sprint.

Execute well for faster handoffs, cleaner data, and shorter cycles. You’ll see an AI “_bench_” that compounds revenue results without adding headcount.

At MAN Digital, we're building custom agents and apps for HubSpot. If you want to discuss, we're happy to share what's working for our clients.