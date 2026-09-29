# Portal configuration maintenance

## Locate and scope

The default config is `portals.yaml` in the real skill directory. Both skill symlinks share this same file. An explicit user-supplied config path overrides that location. Never copy the example over an existing config. If the config is missing, obtain the required values before creating it; example portal IDs, accounts, and themes are not defaults.

Read the current file before editing. Match the requested entry by its unique `id`. Preserve the task's current portal selection unless the user requests a switch. Selecting another existing entry changes task context only: scripts accept `--portal <id> --config <path>` and have no persisted default-portal field. A CLI account name is not proof of a portal ID; local validation cannot verify their remote association.

For additions, obtain `id`, `portalId`, `hsAccount`, and `theme`. A new entry in a valid existing config is non-staging unless the user requests a staging change; use `blogId: null`, `domain: null`, and `forms: {}` when those values are not supplied. Explain that null blog configuration may require manual setup before deployment. Keep credentials in the environment, with `tokenEnv` holding only the environment variable's name. Do not read or print secret values to validate config. Do not change another entry's staging flag unless the requested staging switch requires it; a switch sets the old entry false and the selected entry true together.

## Local validation before saving

Validate a proposed candidate in memory before replacing the original. Use a safe YAML parser (PyYAML is already a deployment dependency), rejecting duplicate YAML mapping keys rather than silently accepting the last value. If the parser is unavailable, report the dependency instead of claiming validation passed.

- The root is a mapping with a nonempty `portals` list of mappings.
- Every `id` is a nonempty unique string. Reject duplicate selectors before any dict conversion; the deployment loader otherwise silently collapses them.
- Every entry has a positive numeric `portalId` (integer or digit string, never boolean), nonempty string `hsAccount`, and nonempty relative `theme` path without parent traversal. Theme folders may contain spaces or nested paths.
- Every `staging` is a boolean and exactly one entry is true. Never quietly choose a staging portal when creating the first config.
- `blogId` is null or a positive numeric ID; `domain` is null or a nonempty string; `forms` is a mapping of module names to nonempty form GUID strings. Local shape validation does not establish that IDs exist in HubSpot.
- If present, `tokenEnv` is a valid shell environment variable name matching `[A-Za-z_][A-Za-z0-9_]*`. An unset variable is a deployment prerequisite to report, not a reason to reset config or substitute another portal's credential.
- If present, `formsProvision` is a mapping with only `enabled`, `spec`, and `prefix`. `enabled` is boolean; when true, `spec` must be a nonempty string resolving to an existing form-spec file (relative paths resolve against the config directory). A supplied `prefix` must be a nonempty string. Preserve existing provisioning settings unless requested otherwise.
- Preserve unrecognized existing fields rather than dropping them. Compare the candidate against the original to ensure only requested changes and necessary staging-switch changes occurred.

Keep unrelated comments and formatting; prefer a narrow edit to a whole-file YAML dump. Write atomically with the original permissions, then parse the saved file again and confirm the intended values. Keep config and temporary copies out of version control; verify the config is ignored in its owning repository, and never stage it. If validation finds an unrelated pre-existing issue, report it without silently rewriting unrelated entries.

## Completion

Summarize the entry and field names changed without printing customer mappings or credentials. Distinguish local config validation from remote account verification. Do not run deploy, upload, blog provisioning, form creation, or theme migration merely to validate a config edit. A changed `theme` field only changes the destination of future commands; it does not move an existing HubSpot theme or reassign pages.
