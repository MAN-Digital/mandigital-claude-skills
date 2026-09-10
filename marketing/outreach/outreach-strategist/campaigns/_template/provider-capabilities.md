# Provider capability reference

Campaigns select capabilities, not brands. Candidate order is preference order;
fallback never broadens authorization or changes the route.

| Capability | Candidate examples | Unavailable behavior |
| --- | --- | --- |
| CRM audience read | HubSpot, CSV adapter | required: fail before access |
| Web research | Exa, Linkup Search, Crawl4AI | optional: skip with evidence |
| Intent signals | Trigify, approved webhook adapter | optional: skip with evidence |
| Warm paths | Graph.one, HubSpot activity | optional: cold-route without claiming there is no warm path |
| LinkedIn relationship | snapshot, Linkup social, OpenClaw Browser | required: hold `unknown` |
| DRAFT/sequence/prospects | Woodpecker API | required: fail before access |
| Native conditions | OpenClaw Browser after API limitation is proved | required: hold |
| Discord thread | OpenClaw Discord adapter | required: queue evidence and hold notification-dependent approval |

`Linkup Search` is the `linkup.so` search API. `Linkup social` is the
`linkupapi.com` LinkedIn automation API. They must have distinct provider ids,
auth variables, probes, and adapter schemas.

Relationship routing uses Linkup social's read-only invitation-status endpoint
with `LINKUP_API_KEY` plus `LINKUP_ACCOUNT_ID` (V2), or the legacy
`LINKUP_LOGIN_TOKEN` fallback. It costs one credit per profile,
so snapshot generation defaults to zero calls and requires an explicit credit
ceiling. `PENDING/SENT` and `PENDING/RECEIVED` are held; absence from LeadDelta
is also `unknown`, never proof that another connection request is safe.

Woodpecker remains API-first for readable DRAFTs, supported sequence content,
and prospect enrollment. Its official API documentation lists conditional
steps and LinkedIn/manual task features as unsupported in API-run campaigns;
the live account also returns `WCNF001 / API_UNSUPPORTED_CAMPAIGN_FEATURES` for
condition-bearing reads. The OpenClaw Browser adapter therefore owns only the
condition editor operation and must verify persistence by a fresh reload. It
may not click Run Campaign or Send test campaign.

Activation is a separate capability and is intentionally absent from the
preparation registry.

Environment variables and installed commands prove only that static
requirements are satisfied. They are not a live provider probe. Evidence must
say `selected_unprobed` until the owning pipeline executes and verifies the
adapter; never translate it to “healthy” or “ready.”

Primary documentation:

- Woodpecker campaigns and unsupported features:
  <https://woodpecker.co/help-center/en/articles/9046676-campaigns>
- Woodpecker developer authentication: <https://developers.woodpecker.co/docs/>
- Woodpecker prospects: <https://developers.woodpecker.co/docs/prospects/>
- HubSpot Lists/Segments API:
  <https://developers.hubspot.com/docs/api-reference/latest/crm/lists/guide>
- Exa Search API: <https://exa.ai/docs/reference/search>
- Linkup Search: <https://docs.linkup.so/pages/documentation/endpoints/search/reference>
- Linkup social v2: <https://docs.linkupapi.com/api-reference/v2/introduction>
- Linkup invitation status:
  <https://docs.linkupapi.com/api-reference/linkup/Network/get_invitations_status>
- Trigify API/MCP/CLI: <https://help.trigify.io/articles/1607275-api-docs-scalar-access>
- Graph.one public capability description: <https://graph.one/>
- Discord webhooks/threads: <https://docs.discord.com/developers/resources/webhook>

Public documentation for Graph.one does not currently establish a concrete
auth/request contract, so it remains optional and its production adapter must
be verified against the actual workspace before use. Trigify's detailed schema
is likewise workspace-authenticated; do not invent endpoints from the summary
page.
