# Gate-3 `hs` syntax verification (C1 fixup, 2026-09-26)

Live `--help` captured on `hs` (C1 premise confirmed):

## `hs cms theme marketplace-validate --help` (exit 0)

```
hs cms theme marketplace-validate <path>

Validate a theme for the marketplace.

Positionals:
  path  Path to the theme within the Design Manager.  [string] [required]

Options:
  -d, --debug    Set log level to debug  [boolean] [default: false]
  -a, --account  HubSpot account id or name from config  [string]
  -c, --config   Path to a config file  [string]
      --use-env  Use environment variable config  [boolean]
  -h, --help     Show help  [boolean]
```

Findings:

- Takes a POSITIONAL remote path (theme within Design Manager) — no `--src` flag exists.
- Takes `-a/--account <name>` for the portal account.
- Cannot validate local dirs → removed from local gate 3; lives in gate 5 (staging) instead.
- Gate-5 form: `hs cms theme marketplace-validate <staging-theme-path> --account=<staging-hsAccount>`

## `hs cms lint --help` (exit 0)

```
hs cms lint <path>

Positionals:
  path  Local folder to lint  [string] [required]

Options:
  -d, --debug    Set log level to debug  [boolean] [default: false]
  -a, --account  HubSpot account id or name from config  [string]
  -c, --config   Path to a config file  [string]
  -h, --help     Show help  [boolean]
```

Findings:

- Takes a POSITIONAL local path → `hs cms lint <theme-dir>` is the correct local invocation (kept in gate 3).
- Also accepts `-a/--account`; gate 3 stays on the default account (no flag).

## Real-`hs` gate-3 run on the fixture (2026-09-26, after the fix)

Command (from repo root):

```
HS_BIN=hs marketing/web-development/man-digital-cms-pages/scripts/validate-theme.sh tests/cms-pages/fixtures/mini-theme --inventory tests/cms-pages/fixtures/mini-inventory.json
```

Output (token fragment redacted):

```
Linting /Users/romeoman/.local/share/mandigital-claude-skills/.worktrees/cms-full-site/tests/cms-pages/fixtures/mini-theme
✖ ERROR This oauth-token ([REDACTED-PREFIX]) does not have proper permissions! (requires any of [source-code-read, content-editor-access])

✖ ERROR Debug logs can be viewed at /Users/romeoman/.hscli/logs/lint-2026-09-26T20-27-15-044.log
FAIL: g3: hs cms lint failed
```

Exit 1. Verdict: EXPECTED outcome — the invocation FORM is accepted (usage OK:
lint ran against the local dir and performed an authenticated API call, proving
local-path lint is valid syntax), but live-green awaits staging creds with
`content`/`source-code-read` scopes. This matches the pre-existing Task 8 Step 6
auth-error record. NOT a usage error → no fix needed here; full live validation
pending staging credentials. Validator suite with `fake-hs` stays green
(13 tests: 11 + 2 new M3), and the `fake-hs` marketplace-validate guard never
tripped — proving local gates no longer invoke it.
