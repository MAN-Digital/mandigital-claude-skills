# DataForSEO Tools Reference

Complete reference for all 5 DataForSEO MCP tools used in SEO pre-research.

---

## Tool 1: labs_search_intent

**Purpose:** Validate that a keyword has informational intent (suitable for blog posts)

**MCP Tool Name:** `mcp__dataforseo__labs_search_intent`

**Parameters:**
```json
{
  "keyword": "your target keyword",
  "location_name": "United States",
  "language_code": "en"
}
```

**Alternative Parameters:**
- `location_code`: 2840 (numeric code for United States)
- `language_name`: "English" (text alternative)

**What It Returns:**
- Informational intent: 0-100% (percentage of informational queries)
- Transactional intent: 0-100% (purchase intent)
- Navigational intent: 0-100% (brand/site seeking)
- Commercial intent: 0-100% (research before purchase)

**How to Use Results:**
- ✅ Informational > 60% → Perfect for blog post
- ⚠️ Informational 40-60% → Consider mixed content (info + CTA)
- ❌ Informational < 40% → Wrong content type, reconsider keyword

**Example Response:**
```json
{
  "keyword": "hubspot prospecting agent",
  "search_intent_info": {
    "se_type": "google",
    "keyword": "hubspot prospecting agent",
    "last_updated_time": "2025-01-20 12:00:00",
    "keyword_intent": {
      "label": "informational",
      "probability": 0.85,
      "intent_types": {
        "informational": 85,
        "commercial": 10,
        "transactional": 3,
        "navigational": 2
      }
    }
  }
}
```

---

## Tool 2: labs_google_keyword_overview

**Purpose:** Get keyword metrics (volume, difficulty, competition, trends)

**MCP Tool Name:** `mcp__dataforseo__labs_google_keyword_overview`

**Parameters:**
```json
{
  "keywords": ["your target keyword"],
  "location_name": "United States",
  "language_code": "en"
}
```

**What It Returns:**
- Search volume: Monthly searches
- Competition: high/medium/low
- Keyword difficulty: 0-100 score
- CPC: Cost per click (indicates commercial value)
- 12-month trend: rising/stable/declining
- SERP features: Featured snippets, PAA, videos present

**How to Use Results:**
- Volume > 500/month → Good blog post target
- Difficulty < 50 → Realistic to rank
- Rising trend → Timely content opportunity
- Featured snippet present → Opportunity to capture position 0

**Example Response:**
```json
{
  "keyword": "hubspot prospecting agent",
  "keyword_info": {
    "search_volume": 1200,
    "competition": "low",
    "competition_index": 25,
    "keyword_difficulty": 35,
    "cpc": 4.50,
    "monthly_searches": [
      {"year": 2024, "month": 12, "search_volume": 1300},
      {"year": 2024, "month": 11, "search_volume": 1200},
      {"year": 2024, "month": 10, "search_volume": 1100}
    ]
  }
}
```

---

## Tool 3: serp_organic_live_advanced

**Purpose:** Get fresh SERP rankings (WHO actually ranks for this keyword)

**MCP Tool Name:** `mcp__dataforseo__serp_organic_live_advanced`

**Parameters:**
```json
{
  "keyword": "your target keyword",
  "location_name": "United States",
  "language_code": "en",
  "depth": 10
}
```

**What It Returns:**
- Top 10 ranking URLs (positions 1-10)
- Page titles and meta descriptions
- Domain names
- URL structure
- SERP features (featured snippets, PAA, videos)

**How to Use Results:**
- **Use THESE URLs for competitor analysis** (not brief URLs)
- Rankings change daily - this is fresh data
- Identify content patterns (listicles, guides, comparisons)
- Note SERP features to target

**Example Response:**
```json
{
  "keyword": "hubspot prospecting agent",
  "items": [
    {
      "type": "organic",
      "rank_group": 1,
      "rank_absolute": 1,
      "position": "left",
      "url": "https://www.hubspot.com/products/crm/prospecting-agent",
      "domain": "hubspot.com",
      "title": "HubSpot Prospecting Agent | AI-Powered Sales Tool",
      "description": "Automate lead research and outreach with HubSpot's AI prospecting agent...",
      "is_featured_snippet": false
    },
    {
      "type": "organic",
      "rank_group": 2,
      "rank_absolute": 2,
      "url": "https://www.salesforce.com/blog/hubspot-prospecting-tools/",
      "domain": "salesforce.com",
      "title": "How to Use HubSpot's Prospecting Agent Effectively",
      "description": "Learn best practices for using HubSpot's AI-powered prospecting agent..."
    }
  ]
}
```

---

## Tool 4: labs_google_domain_rank_overview

**Purpose:** Assess competitor authority (can we compete?)

**MCP Tool Name:** `mcp__dataforseo__labs_google_domain_rank_overview`

**Parameters:**
```json
{
  "target": "competitor-domain.com",
  "location_name": "United States",
  "language_code": "en"
}
```

**What It Returns:**
- Domain rank: 1-10M (lower = more authoritative)
- Organic keywords count: Total ranking keywords
- Organic traffic: Estimated monthly traffic
- ETV (estimated traffic value): Traffic worth in $

**How to Use Results:**
- Domain rank < 10,000 → High authority (focus on content gaps)
- Domain rank 10,000-100,000 → Medium authority (beatable with quality)
- Domain rank > 100,000 → Lower authority (good opportunity)
- Organic keywords > 50,000 → Established player

**Example Response:**
```json
{
  "target": "hubspot.com",
  "metrics": {
    "organic": {
      "domain_rank": 125,
      "keywords_count": 1250000,
      "etv": 85000000,
      "traffic": 45000000,
      "is_new": false
    }
  }
}
```

---

## Tool 5: labs_google_related_keywords

**Purpose:** Discover related keywords for H2/H3 structure planning

**MCP Tool Name:** `mcp__dataforseo__labs_google_related_keywords`

**Parameters:**
```json
{
  "keyword": "your target keyword",
  "location_name": "United States",
  "language_code": "en",
  "depth": 50
}
```

**What It Returns:**
- 50+ related keywords
- Search volume for each
- Keyword difficulty for each
- Relevance score

**How to Use Results:**
- **High-volume (300+)** → Use as H2 headings
- **Medium-volume (100-299)** → Use as H3 headings
- **Low-volume (<100)** → Use as LSI keywords naturally in content
- **Questions** → Use in FAQ section

**Example Response:**
```json
{
  "keyword": "hubspot prospecting agent",
  "items": [
    {
      "keyword": "prospecting agent hubspot",
      "search_volume": 850,
      "keyword_difficulty": 32,
      "competition": "low"
    },
    {
      "keyword": "hubspot ai prospecting",
      "search_volume": 650,
      "keyword_difficulty": 28,
      "competition": "low"
    },
    {
      "keyword": "how to use prospecting agent",
      "search_volume": 320,
      "keyword_difficulty": 25,
      "competition": "low"
    },
    {
      "keyword": "prospecting agent features",
      "search_volume": 180,
      "keyword_difficulty": 22,
      "competition": "low"
    }
  ]
}
```

---

## Common Location Codes

**United States:**
- Name: "United States"
- Code: 2840

**United Kingdom:**
- Name: "United Kingdom"
- Code: 2826

**Canada:**
- Name: "Canada"
- Code: 2124

**Australia:**
- Name: "Australia"
- Code: 2036

**Other Locations:**
- Search: [DataForSEO Locations API](https://docs.dataforseo.com/v3/dataforseo_labs_locations_and_languages/)

---

## Common Language Codes

**English:**
- Code: "en"
- Name: "English"

**Spanish:**
- Code: "es"
- Name: "Spanish"

**French:**
- Code: "fr"
- Name: "French"

**German:**
- Code: "de"
- Name: "German"

---

## Best Practices

### 1. Always Use Fresh Data
- Don't cache SERP results > 7 days
- Rankings change constantly
- Re-run pre-research for same keyword after 30 days

### 2. Location Matters
- Use target audience location
- US content → location_name: "United States"
- UK content → location_name: "United Kingdom"

### 3. Depth Parameter
- SERP: depth=10 (top 10 results sufficient)
- Related keywords: depth=50 (get comprehensive list)

### 4. Parameter Consistency
- Use same location/language across all 5 tools
- Ensures data consistency

### 5. Error Handling
- If tool fails, check API key
- If no results, verify keyword has search volume
- If location invalid, use location code instead of name
