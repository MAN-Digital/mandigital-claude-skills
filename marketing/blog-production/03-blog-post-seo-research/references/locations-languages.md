# Locations and Languages Reference

Complete reference for location codes and language codes used in DataForSEO tools.

---

## How to Specify Location

You can use either **location name** (text) or **location code** (numeric):

**Option 1 - Location Name (Recommended):**
```json
{
  "location_name": "United States"
}
```

**Option 2 - Location Code:**
```json
{
  "location_code": 2840
}
```

---

## Common Locations

### North America

| Country | Location Name | Location Code |
|---------|---------------|---------------|
| United States | "United States" | 2840 |
| Canada | "Canada" | 2124 |
| Mexico | "Mexico" | 2484 |

### Europe

| Country | Location Name | Location Code |
|---------|---------------|---------------|
| United Kingdom | "United Kingdom" | 2826 |
| Germany | "Germany" | 2276 |
| France | "France" | 2250 |
| Spain | "Spain" | 2724 |
| Italy | "Italy" | 2380 |
| Netherlands | "Netherlands" | 2528 |
| Belgium | "Belgium" | 2056 |
| Switzerland | "Switzerland" | 2756 |
| Austria | "Austria" | 2040 |
| Sweden | "Sweden" | 2752 |
| Norway | "Norway" | 2578 |
| Denmark | "Denmark" | 2208 |
| Poland | "Poland" | 2616 |
| Ireland | "Ireland" | 2372 |

### Asia-Pacific

| Country | Location Name | Location Code |
|---------|---------------|---------------|
| Australia | "Australia" | 2036 |
| New Zealand | "New Zealand" | 2554 |
| Japan | "Japan" | 2392 |
| Singapore | "Singapore" | 2702 |
| India | "India" | 2356 |
| China | "China" | 2156 |
| Hong Kong | "Hong Kong" | 2344 |
| South Korea | "South Korea" | 2410 |
| Thailand | "Thailand" | 2764 |
| Malaysia | "Malaysia" | 2458 |
| Philippines | "Philippines" | 2608 |
| Indonesia | "Indonesia" | 2360 |

### Middle East

| Country | Location Name | Location Code |
|---------|---------------|---------------|
| United Arab Emirates | "United Arab Emirates" | 2784 |
| Saudi Arabia | "Saudi Arabia" | 2682 |
| Israel | "Israel" | 2376 |

### Latin America

| Country | Location Name | Location Code |
|---------|---------------|---------------|
| Brazil | "Brazil" | 2076 |
| Argentina | "Argentina" | 2032 |
| Chile | "Chile" | 2152 |
| Colombia | "Colombia" | 2170 |

### Africa

| Country | Location Name | Location Code |
|---------|---------------|---------------|
| South Africa | "South Africa" | 2710 |
| Nigeria | "Nigeria" | 2566 |
| Kenya | "Kenya" | 2404 |
| Egypt | "Egypt" | 2818 |

---

## Common Languages

You can use either **language code** (recommended) or **language name**:

**Option 1 - Language Code (Recommended):**
```json
{
  "language_code": "en"
}
```

**Option 2 - Language Name:**
```json
{
  "language_name": "English"
}
```

---

## Language Codes

| Language | Language Code | Language Name |
|----------|---------------|---------------|
| English | "en" | "English" |
| Spanish | "es" | "Spanish" |
| French | "fr" | "French" |
| German | "de" | "German" |
| Italian | "it" | "Italian" |
| Portuguese | "pt" | "Portuguese" |
| Dutch | "nl" | "Dutch" |
| Russian | "ru" | "Russian" |
| Chinese (Simplified) | "zh-CN" | "Chinese (Simplified)" |
| Chinese (Traditional) | "zh-TW" | "Chinese (Traditional)" |
| Japanese | "ja" | "Japanese" |
| Korean | "ko" | "Korean" |
| Arabic | "ar" | "Arabic" |
| Hindi | "hi" | "Hindi" |
| Polish | "pl" | "Polish" |
| Swedish | "sv" | "Swedish" |
| Norwegian | "no" | "Norwegian" |
| Danish | "da" | "Danish" |
| Finnish | "fi" | "Finnish" |
| Greek | "el" | "Greek" |
| Turkish | "tr" | "Turkish" |
| Hebrew | "iw" | "Hebrew" |
| Thai | "th" | "Thai" |
| Vietnamese | "vi" | "Vietnamese" |
| Indonesian | "id" | "Indonesian" |
| Malay | "ms" | "Malay" |

---

## Usage Examples

### Example 1: US English Content
```json
{
  "keyword": "hubspot crm",
  "location_name": "United States",
  "language_code": "en"
}
```

### Example 2: UK English Content
```json
{
  "keyword": "crm software",
  "location_name": "United Kingdom",
  "language_code": "en"
}
```

### Example 3: Spanish Content (Spain)
```json
{
  "keyword": "software crm",
  "location_name": "Spain",
  "language_code": "es"
}
```

### Example 4: French Content (Canada)
```json
{
  "keyword": "logiciel crm",
  "location_name": "Canada",
  "language_code": "fr"
}
```

### Example 5: German Content
```json
{
  "keyword": "crm software",
  "location_name": "Germany",
  "language_code": "de"
}
```

---

## Best Practices

### 1. Match Target Audience Location
Use the location where your target audience lives:
- Writing for US audience → `location_name: "United States"`
- Writing for UK audience → `location_name: "United Kingdom"`
- Writing for Australian audience → `location_name: "Australia"`

### 2. Consistency Across Tools
Use the **same location and language** for all 5 tools:
```json
// Use this for ALL 5 tools
{
  "location_name": "United States",
  "language_code": "en"
}
```

### 3. Language Variants Matter
- US English: `"en"` + `"United States"`
- UK English: `"en"` + `"United Kingdom"`
- Canadian English: `"en"` + `"Canada"`
- Australian English: `"en"` + `"Australia"`

**Why it matters:** Search behavior and vocabulary differ:
- US: "color", "optimize"
- UK: "colour", "optimise"

### 4. Location Name vs Code
- **Use location name** for readability: `"United States"`
- **Use location code** if name fails: `2840`

### 5. Special Cases

**Multi-Region Content:**
If targeting multiple regions, run pre-research separately for each:
```
Run 1: location_name: "United States"
Run 2: location_name: "United Kingdom"
Run 3: location_name: "Canada"
```

**International English:**
Use most specific location:
- ✅ "United States" for US-focused content
- ❌ Don't use generic "English" without location

---

## Finding Other Locations

If you need a location not listed here:

1. **Check DataForSEO API:**
   - Endpoint: `/v3/dataforseo_labs/locations`
   - Documentation: https://docs.dataforseo.com/v3/dataforseo_labs_locations_and_languages/

2. **Use Name Search:**
   ```
   Search for: "New York" → Get location code
   Search for: "London" → Get location code
   Search for: "Tokyo" → Get location code
   ```

3. **City-Specific Locations:**
   Available for major cities:
   - "New York, United States" → 1023191
   - "London, United Kingdom" → 2826
   - "Toronto, Canada" → 9062395

---

## Troubleshooting

### Error: "Invalid location"
**Solution:** Use location code instead of name
```json
// Instead of this:
{"location_name": "US"}

// Use this:
{"location_code": 2840}
```

### Error: "Language not supported for this location"
**Solution:** Check language is available in that country
- Not all languages available in all locations
- Example: `language_code: "ja"` works with `location_name: "Japan"`

### Different Results for Same Keyword
**Cause:** Different location/language settings
**Solution:** Always use consistent settings across all 5 tools

---

## Quick Reference Table

| Use Case | Location | Language |
|----------|----------|----------|
| US B2B SaaS Blog | United States | en |
| UK Enterprise Content | United Kingdom | en |
| Canadian Content | Canada | en |
| Australian Content | Australia | en |
| Spanish (Spain) Content | Spain | es |
| Spanish (Mexico) Content | Mexico | es |
| French (France) Content | France | fr |
| French (Canada) Content | Canada | fr |
| German Content | Germany | de |
| Japanese Content | Japan | ja |
