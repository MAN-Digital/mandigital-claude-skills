# LinkedIn guest identity verification

Treat every LinkedIn URL from a prompt, transcript description, spreadsheet, or prior draft as an unverified candidate. Same-name profiles are common, and a plausible URL slug is not identity evidence.

## Resolve the person

Use one of these public, read-only routes before drafting:

1. **Apollo.io:** use `apollo_mixed_people_api_search` with the guest's full name plus company, role, or location. This no-credit search is sufficient when the returned profile and career signals are clear. Do not call credit-based people enrichment or reveal contact data without the user's explicit confirmation.
2. **Exa:** use `web_search_exa` with `category:people`, the full name, company, and role. Run a second, differently angled search for career history or the interview/episode page, then use `web_fetch_exa` on the strongest profile and corroborating source.

If one provider is empty or ambiguous, use the other. Search results are candidates, not validation: review them and discard same-name people whose role, employer, location, or history conflicts with the interview source.

## Verification threshold

Accept a profile only when all of these are true:

- the public profile displays the exact guest name;
- at least two person-specific signals match the interview source, such as company and role at recording, a previous employer, location, or a distinctive career detail;
- at least two independent HTTPS evidence URLs support the match, one of which is the canonical LinkedIn `/in/` profile;
- no reviewed source contradicts the match.

Current employment may have changed after the recording. Compare the role at recording and career history instead of rejecting a person merely because their current title is newer.

Stop and ask the user when two plausible profiles remain, the evidence conflicts, or fewer than two signals can be corroborated. Never choose the closest slug or silently retain a URL from an older draft.

## Normalize and record

Normalize the accepted URL to `https://www.linkedin.com/in/<slug>` with no query string, fragment, or trailing slash. Store this internal object in `metadata.example.json`:

```json
{
  "linkedinVerification": {
    "status": "verified",
    "provider": "exa",
    "verifiedAt": "YYYY-MM-DD",
    "profileUrl": "https://www.linkedin.com/in/example",
    "matchedSignals": [
      "Exact full name",
      "Role and company at recording"
    ],
    "evidenceUrls": [
      "https://www.linkedin.com/in/example",
      "https://example.com/corroborating-interview-page"
    ]
  }
}
```

`provider` may be `apollo`, `exa`, or `apollo+exa`. Keep this record and its evidence out of the reader-facing article. Copy `profileUrl` exactly into `source.json.provided.linkedinProfile` and every `.rli-linkedin` link. Run the validator before any CMS write; a mismatch or incomplete verification is a hard failure.

## CMS verification

After the API save, reopen the HubSpot draft and confirm:

- every rendered LinkedIn action uses the verified normalized URL;
- the old/candidate URL is absent;
- the accessible SVG icon is still present;
- the post remains a draft.
