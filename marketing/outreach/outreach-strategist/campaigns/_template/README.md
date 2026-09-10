# New campaign template

Copy this whole directory to `campaigns/<slug>/`; do not create another skill.
The `outreach-strategist` remains the single campaign coordinator.

Read `provider-capabilities.md` for the provider contract and current official
API constraints.

1. Complete `intake.yaml`. Ask only unanswered required questions and show all
   assumptions before proceeding.
2. Fill `campaign.yaml`, replacing every `<...>` marker. Choose providers by
   capability, not by vendor name. Missing optional capabilities must produce
   explicit evidence; missing required capabilities hold before external I/O.
3. Add `brief.md`, `research-protocol.md`, `routing.md`, and stream files only
   when the campaign needs them.
4. Create one Mission Control campaign definition from its
   `config/outreach/campaign-template.json`. Running its generic preparer with
   no mode flag is read-free; `--compile` permits provider reads and a private
   artifact. DRAFT/prospect writes only happen after the authenticated Mission
   Control build-approval gate. The compiler cannot activate or send.

Provider adapters share four lifecycle operations: `probe`, `plan`, `execute`,
and `verify`. Their registry metadata also declares mutation risk, metering,
approval requirements, environment-variable names, and runtime commands.
Never store credential values in campaign config, evidence, or git.

Relationship states are `first_degree`, `pending_outbound`, `pending_inbound`,
`second_degree`, `third_degree`, and `unknown`. Only `first_degree` may route
straight to a direct message. Unknown always holds. A failed DM must not
silently broaden into InMail or a connection request.

Relationship snapshots must carry a timezone-aware `captured_at` and are
rejected after the configured freshness window (24 hours by default). Linkup
invitation-status reads cost one credit each: authorize a numeric ceiling before
the run. A zero ceiling performs no Linkup calls and leaves unresolved people
on hold.
