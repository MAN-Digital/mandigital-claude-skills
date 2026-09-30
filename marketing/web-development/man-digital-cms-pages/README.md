# MAN Digital CMS Pages

Maintains and validates the HubSpot CMS source for `www.man.digital`, including the
Man-Digital Theme 2023 and the RevOps Service page.

## When to use it

Use `$man-digital-cms-pages` for HubL, Design Manager, theme, module, page, deployment,
render verification, or HubSpot-specific performance work on MAN Digital's website.

## Inputs and outputs

- Inputs: the requested CMS change or audit, portal `1969772`, and the canonical source
  repository.
- Outputs: validated source changes, scoped upload commands, verification evidence, and
  rollback-ready Git history.

## Setup

The skill definition lives here; website source remains canonical in
[`MAN-Digital/man-digital-cms-pages`](https://github.com/MAN-Digital/man-digital-cms-pages)
to avoid maintaining two copies.

From this skill directory, run:

```bash
scripts/ensure-source.sh
scripts/validate-source.sh
```

`ensure-source.sh` clones into `references/source/` when missing. Set
`MAN_DIGITAL_CMS_SOURCE=/absolute/path/to/checkout` to reuse another checkout.

Prerequisites: Git, Python 3, and ripgrep. HubSpot CLI access is needed only for an
explicitly authorized upload; local validation does not contact HubSpot.
## Safe API credentials

For draft page edits, use a HubSpot private-app token with the `content` scope.
The CLI personal access key can read pages without being able to write them.
Theme file uploads continue to use the existing CLI account workflow.

1. In the intended HubSpot portal, open **Development → Legacy apps**. Select an
   existing private app or create one, for example `MAN Digital CMS Draft Editor`.
2. Add the **`content`** scope. This scope also permits publication; our draft
   workflow uses only draft endpoints. Add `files` separately only if uploads are
   required. Existing video/image URLs need no upload permission.
3. Open **Auth → Show token → Copy**. See the
   [official private-app instructions](https://developers.hubspot.com/docs/apps/legacy-apps/private-apps/overview).
4. Run this command in an interactive terminal on the computer where Codex runs:

   ```bash
   python3 "$HOME/.local/share/mandigital-claude-skills/marketing/web-development/man-digital-cms-pages/scripts/cms-token.py" setup --portal-id 1969772
   ```

   For another checkout, run `python3 scripts/cms-token.py setup --portal-id <portalId>`
   from this skill directory. Use the ID of the selected portal, never a CLI default.
5. Paste the token **at the hidden prompt** and press Enter. Do not paste it into
   chat, a command argument, a README, `portals.yaml`, or a GitHub secret field for
   this local workflow. The command verifies the HubSpot portal and `content`
   scope before saving; it does not edit any page.

Credentials are stored at `~/.config/man-digital/hubspot/<portalId>.json`, outside
this repository. The directory uses mode `700`; the file uses mode `600`. This is
an owner-readable local file, not an encrypted vault. Tokens are never printed,
and hidden input keeps them out of shell history and process arguments. The helper
refuses an unverified token, a different portal, and insufficient scopes.

For this production portal, the file is
`~/.config/man-digital/hubspot/1969772.json`. Add only its path to the selected local
`portals.yaml` entry as `tokenFile`; never add the file contents. This optional
field is used by the page-content API workflow, not by existing deploy/form scripts.

To verify access later without displaying the token:

```bash
python3 "$HOME/.local/share/mandigital-claude-skills/marketing/web-development/man-digital-cms-pages/scripts/cms-token.py" check --portal-id 1969772
```

To replace a rotated token, rerun `setup`; the existing file is replaced only after
verification succeeds. To revoke access, revoke/rotate the token in HubSpot;
deleting the local file alone does not revoke it. On another computer, run setup
there rather than syncing this credential through Git.

See [the page-content API workflow](references/page-content-api.md) for draft
snapshots, writes, readback, and visual verification.

## Full-site generation

Converts a React (Vite + Tailwind + shadcn) repo or a Figma handoff into a validated HubSpot theme ZIP: global header/footer, blog listing + post, DnD templates, `deploy.json` page manifest, `assets.json` image manifest.

- Inputs: repo URL + branch (private repos via `gh` auth) or "here is figma" + handoff.
- Outputs: QA-passed ZIP + per-gate evidence; deploy via `scripts/deploy.sh` with a gitignored `portals.yaml`.
- Small edits ("small edit …") stay lightweight: touched files only, no forced rebuild.

Prerequisites beyond Setup above: `hs` CLI v8+, `gh` CLI, Python 3 with PyYAML (`pip3 install --user pyyaml`), `zip`, `unzip`, `curl`. Gate 3 (`hs cms lint`) needs hs auth (PAK) + network + an hs account with source-code-read or content-editor-access — local validation is NOT fully offline. Set `HS_ACCOUNT=<hsAccount>` (staging, never prod for routine runs) to select the lint account.

## Portal configuration maintenance

Ask to add or update an entry in `portals.yaml`, or say “use portal `<id>`” to select an existing entry for the task. The skill follows the Portal-config flow and [maintenance checklist](references/portal-config-maintenance.md), preserves unrelated settings, and validates edits locally. Config changes do not deploy anything. The existing gitignored config remains shared by both skill symlinks.
