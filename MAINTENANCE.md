# Multi-Machine Skill Maintenance

This repository can safely maintain the CMS, Figma website design, and PSI/Web Vitals skills on multiple macOS machines.

## Safety Model

- GitHub `main` is the source of truth.
- Installed skills are symlinks into one managed checkout per machine.
- Scheduled updates use fetch plus fast-forward only.
- A fetched commit is validated in a detached worktree before the installed checkout advances.
- Dirty or non-`main` checkouts are preserved and block synchronization.
- Skill changes can be published as draft pull requests, but no maintenance command merges them.

## Prerequisites

Each machine needs:

- macOS with Python 3 and Git;
- GitHub access to `MAN-Digital/mandigital-claude-skills`;
- GitHub CLI authentication only when publishing local changes;
- a stable checkout path that will not be removed after setup.

## First-Time Setup

Choose a stable location and clone the repository:

```bash
git clone https://github.com/MAN-Digital/mandigital-claude-skills.git "$HOME/Documents/Codex/mandigital-claude-skills"
cd "$HOME/Documents/Codex/mandigital-claude-skills"
```

Install maintenance for Codex:

```bash
scripts/install-machine-maintenance --repo "$PWD" --codex
```

Use `--claude` instead of `--codex`, or pass both, when that machine uses Claude's skills directory too. Existing non-managed folders are moved into timestamped backups before symlinks replace them.

The installer also:

- configures `.githooks/` as the checkout's Git hook directory;
- writes `~/Library/LaunchAgents/com.man-digital.skills-sync.plist`;
- loads the LaunchAgent;
- schedules synchronization for 09:00 and 17:00 local time.

Run the same clone and bootstrap sequence once on machines two and three. The installer is idempotent, so running it again repairs links and refreshes the LaunchAgent without creating duplicate jobs.

## Check Status

```bash
scripts/skills-status \
  --repo "$PWD" \
  --state-dir "$HOME/.local/state/man-digital-skills" \
  --install-root "$HOME/.codex/skills" \
  --json
```

The result includes the local and remote commits, branch, dirty state, ahead/behind counts, managed link status, and last scheduled result.

Logs and state are stored under:

```text
~/.local/state/man-digital-skills/
├── backups/
├── logs/
└── status.json
```

## Run Synchronization Manually

```bash
scripts/skills-sync \
  --repo "$PWD" \
  --state-dir "$HOME/.local/state/man-digital-skills" \
  --install-root "$HOME/.codex/skills"
```

If the command reports a dirty checkout or a branch other than `main`, it makes no changes. Review and publish or discard the local work deliberately before synchronizing again.

## Publish Local Improvements

Review local changes first, then run:

```bash
scripts/publish-skill-changes --repo "$PWD"
```

The publisher shows the diff, validates the repository, asks for confirmation, creates a machine-scoped branch, commits, pushes, and opens a draft pull request. It does not merge the pull request.

After the pull request is reviewed and merged, return the managed checkout to `main` and synchronize:

```bash
git switch main
scripts/skills-sync \
  --repo "$PWD" \
  --state-dir "$HOME/.local/state/man-digital-skills" \
  --install-root "$HOME/.codex/skills"
```

## Validate Before Publishing

```bash
scripts/skills-doctor --repo . --bootstrap-cms
python3 -m unittest discover -s tests/maintenance -v
```

The versioned pre-commit hook runs quick checks. The pre-push hook runs the full offline repository doctor. GitHub Actions repeats the tests and offline validation on pull requests and `main`.

The CMS source repository is private. To add CMS-source bootstrap validation in GitHub Actions, create a repository Actions secret named `CMS_SOURCE_TOKEN` containing a fine-grained token with read-only access to `MAN-Digital/man-digital-cms-pages`. Without that secret, the private step is skipped while every repository-contained skill and maintenance test is still validated. Local machines continue to run CMS validation through their existing GitHub credentials.

## Recover a Previous Install

The bootstrap never deletes the folder it replaces. Locate the most recent backup under `~/.local/state/man-digital-skills/backups/`, unload the LaunchAgent, remove only the managed symlink, and move the chosen backup into the original install path.

To unload the scheduled job:

```bash
launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.man-digital.skills-sync.plist"
```

Do not remove the managed checkout until installed symlinks have been replaced or removed.

## Change the Managed Skill Set

Edit [`automation/managed-skills.txt`](./automation/managed-skills.txt) using one `repository-path|install-name` entry per standalone skill. Publish that change through a pull request, merge it, then rerun bootstrap on each machine.

## Central Validation Schedule

GitHub Actions validates pull requests and pushes to `main`. It also runs a central health check every Monday at 07:00 UTC. Private CMS-source validation runs during those checks when `CMS_SOURCE_TOKEN` is configured. Machine synchronization failures remain local and produce a non-zero LaunchAgent result plus logs in the machine state directory.
