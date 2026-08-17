# How To Build Customer Health Score in HubSpot

Customer health is a single score that rolls many signals into one clear view: who’s thriving, who needs attention, and who’s at risk.

It’s built from four pillars you likely already track—product usage and behavior, customer feedback (NPS/CSAT), account health (billing/renewals), and engagement (emails, webinars, meetings)

Acts as an early‑warning system to flag adoption drops, support friction, and renewal risk before they snowball.

**Why you should care**

- Protect revenue: catch churn early; improve retention and NRR.
- Focus the team: CSMs and AMs know exactly where to act first.
- Grow smart: flag expansion candidates when usage and sentiment are strong.
- Move faster: automate alerts, tasks, and playbooks the moment status changes.
- Make it obvious: one signal leaders can read in 2 minutes—no deep digging required.

**What it looks like in HubSpot**

- A 0–100 score plus a traffic‑light status:

  - Green (healthy)
  - Yellow (needs attention)
  - Red (at risk)
- Visible on Company/Account records and a shared dashboard anyone can scan.
- Driven by 3–10 signals with weights that total 100 (keep it clean; fewer is better).
- Wired to simple automations:

  - Red → create Renewal‑Risk ticket; notify owner + manager; book a check‑in within 48h.
  - Yellow → Green → add to Expansion list; send a “next‑value” touch; invite to an advanced webinar.
  - 60 days to renewal and not Green → start Save Plan sequence; add an exec‑level touch.

\[Screenshot\]

When feature adoption slips or support friction rises, teams often notice too late because signals live in different places. A shared health score brings those signals together so you act early and consistently.

**What y****ou’ll get in this guide**

- How to choose the right 3–10 signals for your model
- How to weight them to 100 and set clear Green/Yellow/Red thresholds
- The three automations to wire on day one
- Where to surface the score (records + dashboards) and how to drive adoption
- Examples by business type so you can ship a credible v1 in a week

Imagine, at the end of this, your team opens a single dashboard: the traffic light shows two Reds, three Yellows, and the rest Green. Tasks are already queued, owners know their next move, and a renewal you would’ve missed is now a 48‑hour save plan—in motion.

## What is a Customer Health Score?

A customer health score is a single roll-up that predicts whether an account is healthy or at risk by combining a few key signals.

In HubSpot, you calculate it from the signals that matter to your business and use it to trigger proactive workflows that protect retention and [NRR](https://churnzero.com/churnopedia/net-revenue-retention/).

We’ll frame the score around four pillars:

- Product usage and behavior
- Engagement
- Customer feedback
- Account health

Next, we’ll choose the right signals under each pillar and set weights and thresholds.

### Key factors that influence customer health

Your score is only as good as its inputs. Single metrics mislead; combine a few high‑signal inputs across four pillars:

- **Product usage & behavior**: logins, feature adoption, depth of use.  
Sustained usage = value; 30‑day drops flag adoption risk and trigger outreach.

- **Customer feedback**: NPS/CSAT, reviews, support CSAT/response time.  
Dips below threshold → follow up within 48h to diagnose and recover.

- **Account health**: billing status, renewal window, seats vs. contract.  
Late payments or T‑60 renewals not Green → start a save plan.

- **Engagement**: email replies, webinar attendance, community activity. High engagement → expansion list; inactivity → reactivation play.

Weight by business model. Start simple (3–10 signals), then review quarterly to tune for leading indicators of retention and expansion.

## Why customer health scores matter

A single customer health score turns scattered signals into one clear picture so you can act early and confidently. So your team knows exactly which accounts to rescue, nurture, or grow—and why—without digging through five tools.

- Unify what you already track (usage, feedback, account activity) into one 0–100 score you can read at a glance.
- Spot risk and growth opportunities sooner, prioritize the right accounts, and know your next move.

_\[Maybe an infographic showing how the “complete picture” is created?\]_

Used consistently, it does more than protect retention—it grows revenue by surfacing upsell opportunities, driving expansions, and strengthening loyalty.

Prioritize by health:

- Red: 48-hour save plan, exec touch, clear next steps.
- Yellow: targeted adoption help, resolve blockers, scheduled check-in.
- Green: expansion track, intro to advanced use, ask for referral/review.

Outcome: fewer churn surprises, stronger renewals, clearer growth.

It’s more than a metric; it helps you keep customers and spot upsell opportunities.

## HubSpot Customer Success Workspace & health scoring overview

HubSpot’s [<u>Customer Success workspace</u>](https://knowledge.hubspot.com/service/customer-success-workspace) is the place where you manage customer health scores and run retention efforts.

\[screenshot with the first page of workspace\]

The workspace pulls together usage, interactions, feedback, and account details, making risks and opportunities obvious. Pick the key behaviors and attributes to power your health score.

Here are some examples:

**Business type**

**Signals that may matter most for health scoring**

SaaS platform

Product usage depth, feature adoption, login frequency, support tickets

Professional services firm

Customer feedback ([<u>NPS</u>](https://www.hotjar.com/net-promoter-score/)/[<u>CSAT</u>](https://www.qualtrics.com/experience-management/customer/what-is-csat/)), contract renewals, billing history

E-commerce

Purchase frequency, order value trends, customer support interactions

Online education provider

Course completion rates, session attendance, engagement in community forums

Subscription box business

Renewal rates, skipped orders, feedback on delivered items

Here’s what the workspace enables:

- Blend metrics into one 0–100 score
- Weight signals to fit your business
- Track trends with built-in analytics
- Drill into account-level drivers
- Turn scattered data into clear actions

### Access and setup requirements

Service Hub offers two tiers for health scoring:

Feature

Professional

Enterprise

Active Health Scores

Single score

Multiple scores

Best For

Simple customer bases with similar needs

Complex segments, multiple product lines, different customer stages

Before you can create health scores, you need two things:

1. Set up the Customer Success workspace in HubSpot
2. Have the right permissions:

  - Access to Service tools (seat of Service Pro or Entreprise)
  - Permission to work with health scores
  - Permission to create workflows (if you want to automate actions)

### Step‑by‑step: creating a health score in HubSpot

Once you’ve set up your **Customer Success workspace**, you can proceed to creating your first health score. Here’s how you do it. 

_\[Graphics: provide a screenshot for each step of the following process\]_

• Step 1 — Open Health Scoring Tool

- Navigate to: Service → Customer Success → Customer Health Scoring
- View list of all active and draft scores

• Step 2 — Create New Score

- Click "Create score"
- Professional tier: Edit existing score or use one of five drafts
- Enterprise tier: Add new scores for different segments

• Step 3 — Define Scoring Signals

- Select key metrics for customer health
- Choose indicators relevant to your business model

• Step 4 — Assign Weights and Thresholds

- Set importance level for each signal
- Ensure weights total 100 points
- Example: Login frequency (40 points) vs. webinar attendance (20 points)

☑ **Important**: The maximum points across all groups must total **100**. This keeps your scoring balanced and easier to interpret.

Set thresholds for “Healthy”, “At Risk”, and “Unhealthy” states so your team can read the score at a glance.

• Step 5 — Review and Publish

- Review all signals and weights one final time
- Confirm score matches your team's view of customer health
- Click "Publish" button to activate the score
- Monitor initial results for any needed adjustments

• Step 6 — Put Score Into Action

- Add health score to key dashboards
- Set up automated alerts for score changes
- Create workflows for specific triggers:

  - Tasks for CSMs when scores drop
  - Email sequences based on threshold changes
  - Automated check-in scheduling for at-risk accounts

### Customising event and property groups

In the Calculations tab, pick your metrics and set their weights. Simple as that.

_\[Graphics: Add a Screenshot of the Calculations tab\]_

Event groups track what customers actually do - every login, feature click, webinar view, and download. Make them work harder by:

- Setting decay rates - old actions fade, recent ones matter more
- Defining triggers - "3 logins this week" vs "zero touches in 30 days"
- Adding impact rules - reward good behavior, flag warning signs
- Rolling up or drilling down - score actions solo or bundle them together

Property groups let you score based on HubSpot object values like:

- Subscription tier
- Account size
- Contract length

You can score properties individually or combine them. The key is getting the weights right:

Too high = masks real problems; Too low = misses critical signals

Look at your past churn data to set smart weights. Then make the scores dead simple to read:

- Green (70-100): Healthy
- Yellow (40-69): Needs attention
- Red (0-39): At risk

That's it - clear signals, clear actions.

- **Green** for healthy accounts, 
- **Yellow** for those that need attention, 
- **Red** for at-risk customers. 

_\[Graphics: Add an Screenshot of a those thresholds from any project\]_

### Setting thresholds & labels and turning on the score

Before activating your health score system, it's critical to validate that it accurately reflects your customer relationships.

A proper testing phase helps avoid confusion and ensures your team can trust the scores.

• Test your health score before going live:

- Preview scores using sample customer records
- Check score distribution across your customer base
- Verify thresholds match real customer health patterns
- Fix any issues or misconfigurations

• When testing looks good, activate the score

### Evolving your health score

Start dead simple: track what matters now, tune what works later.

Your v1 health score? Three things:

- How often they use your product
- When they need help
- If they engage with your team

That's it. Ship that. Watch what predicts churn or growth. Double down on those signals. Kill the noise.

The best health scores aren't built in boardrooms—they're battle-tested with real customers. Let the data tell you what matters.

The key is momentum, not perfection. Start small, learn fast, evolve.

Want stronger health scores? Plug in the tools you already use:

- [Amplitude](https://amplitude.com/templates/product-health-dashboard) tracks product behavior
- [Pendo](https://support.pendo.io/hc/en-us/articles/360042454072-Improve-customer-health-and-retention) shows feature adoption
- [Segment](https://segment.com/customer-data-platform/) connects customer data

No spreadsheets, no manual updates. Just richer signals flowing straight into your health score—automatically.

Set it once, trust it always. Your scores stay fresh and accurate across every platform your customers touch.

## Measuring & monitoring customer health scores

Monitor scores. Act fast. Here's how:

Example:

- Signal: Customer's daily logins drop to zero for 30 days
- Trigger: HubSpot alerts CSM automatically
- Action: CSM books check-in call within 48 hours

Set up similar workflows for other health signals. Review and adjust your model quarterly based on what actually predicts churn.

### Analysing results & segmentation

Your team needs more than just numbers - they need to know what those numbers mean and what to do about them.

Get your CSMs, support leads, and account managers in a room. Look at the scores together. Ask:

- Which accounts are slipping and why?
- Who's ready for expansion?
- What patterns keep showing up?

Then act:

- Red scores → rescue plan
- Yellow scores → fix specific issues
- Green scores → explore upsell opportunities

HubSpot lets you group similar accounts and automate your response. But the real work happens when your team meets regularly to spot trends and adjust your approach.

Remember: A health score is just a tool. Your team's insight and action make it valuable.

## Best practices for implementing customer health scores

The success of your health score depends on proper implementation and maintenance. Here are the key practices:

1. Clear Criteria

- Set specific, measurable benchmarks
- Define what "healthy" means for your business model
- Use concrete metrics, not vague goals

2. Mix Data Types

- Combine usage data with customer feedback
- Track support tickets and conversation notes
- Run regular customer surveys

3. Regular Monitoring

- Check scores weekly or monthly
- Use dashboards to spot trends
- Set alerts for significant changes

4. Quick Response

- Create workflows that trigger on score changes
- Define clear actions for each threshold
- Follow up within set timeframes

5. Regular Updates

- Review scoring criteria quarterly
- Adjust weights based on what predicts churn
- Remove metrics that don't drive decisions

6. Team Alignment

- Share dashboards across departments
- Define who owns which responses
- Document and update playbooks

## Challenges & limitations of health scoring

Health scores support but don't replace human judgment. They can't capture every nuance of customer relationships. Common challenges include:

- Integrating data from multiple sources
- Managing overlapping tools
- Manual setup requirements (no AI scoring yet)

Keep your scoring criteria aligned with your business model and review regularly to maintain accuracy.

Reliable data is key—[<u>using incomplete or low-quality data can lead to misleading scores</u>](https://www.totango.com/blog/mastering-customer-health-scoring-how-to-get-data-you-actually-trust) and poor decisions. 

## Conclusion

Your path to effective health scoring:

• Start small

- Pick 3-5 core metrics that directly signal risk or growth
- Ship a basic model in one week
- Let real customer data guide what matters

• Act fast

- Red scores → 48-hour rescue plan
- Yellow scores → targeted fixes
- Green scores → expansion plays

• Stay sharp

- Review scores monthly
- Kill metrics that don't drive decisions
- Double down on signals that predict churn

Remember: Scores guide action; relationships drive retention. Build both.