# Multi-Machine Skill Maintenance Design

## Purpose

Keep the MAN Digital CMS, Figma website design, and PSI/Web Vitals skills consistent across three macOS machines while still allowing contributors to improve them safely from any machine.

The system must make routine updates automatic without silently overwriting local work or merging unreviewed instructions that can change agent behavior.

## Source of Truth

The `main` branch of `MAN-Digital/mandigital-claude-skills` is the only canonical source.

Each machine has one managed checkout and installs skills by symlinking the configured skill folders from that checkout into its local Codex or Claude skills directory. Installed folders are therefore views of the checkout, not independent copies that can drift unnoticed.

The default managed set is:

- `marketing/web-development/man-digital-cms-pages`
- `marketing/web-development/man-digital-figma-website-design`
- `marketing/web-development/auditing-web-vitals`

The manifest remains editable so other standalone skills can be added without changing the synchronization code.

## Approaches Considered

### 1. Scheduled copy from GitHub

Download and overwrite installed folders on a timer.

This is simple, but it can erase machine-local edits and makes it difficult to identify which files changed locally. It is not suitable for machines that also contribute improvements.

### 2. Managed checkout with symlinked installs

Maintain one Git checkout per machine, validate remote updates before fast-forwarding, and symlink installed skills to that checkout.

This is the selected approach. Git provides reliable drift detection and contribution history, while symlinks eliminate duplicate installed copies. A dirty checkout blocks synchronization instead of being reset or stashed.

### 3. GitHub Actions only

Validate the central repository without installing any local scheduler.

This protects `main` but cannot observe or update private files on the three machines. It is useful as a central validation layer, not as the complete solution.

## Components

### Repository validator

`scripts/skills-doctor` performs dependency-light validation against a repository path:

- validate every repository `SKILL.md` frontmatter and folder name, while reporting the managed subset separately;
- compile tracked Python scripts without creating bytecode files;
- run shell syntax checks;
- verify configured local Markdown links;
- start the PSI CLI with `--help`;
- validate the CMS source when it is already available, with an explicit option to bootstrap it;
- report the current commit, branch, dirty state, and validation summary.

The same command runs locally, from Git hooks, and in GitHub Actions.

### Safe synchronizer

`scripts/skills-sync` runs the following sequence:

1. Acquire a per-machine lock so two scheduled runs cannot overlap.
2. Confirm the managed checkout is on `main` and has no tracked or untracked changes.
3. Fetch `origin/main` without changing the checkout.
4. Create a temporary detached worktree at the fetched commit.
5. Validate the fetched commit with the currently trusted validator.
6. Remove the temporary worktree.
7. Fast-forward the managed checkout only when validation passes.
8. Re-run the validator from the updated checkout and verify all managed symlinks.
9. Record the result, timestamp, and commit in the machine state directory.

It never runs `reset --hard`, automatically stashes files, force-pushes, or overwrites a dirty checkout. An invalid remote commit leaves the currently installed version unchanged.

### Machine bootstrap

`scripts/install-machine-maintenance` configures a macOS machine:

- verify the checkout and required commands;
- install the versioned Git hooks with `core.hooksPath`;
- read the managed skill manifest;
- back up existing non-symlink skill folders before replacing them;
- create managed symlinks for Codex, Claude, or both, as selected by the operator;
- install and load a user LaunchAgent;
- run an initial doctor check and synchronization dry run.

Backups live in a timestamped state-directory folder and are never automatically deleted.

### Contribution publisher

`scripts/publish-skill-changes` is an explicit command, not a scheduled job. It:

1. Shows the local diff and requires confirmation unless `--yes` is provided.
2. Runs the full validator.
3. Creates a branch named `machine/{machine-name}/{timestamp}` when necessary.
4. Commits the confirmed repository changes.
5. Pushes the branch and opens a draft pull request with the machine name and validation results.

The command never merges the pull request. Skill-instruction changes require GitHub validation and human approval before reaching `main`.

### Git hooks

Versioned hooks perform validation, not synchronization:

- `pre-commit` validates changed skill metadata and scripts quickly;
- `pre-push` runs the complete repository doctor.

Keeping downloads out of hooks makes Git operations deterministic and prevents a commit from unexpectedly changing the working tree.

### GitHub Actions

The repository workflow runs the complete validator:

- on every pull request that changes skills, maintenance scripts, manifests, or documentation;
- on pushes to `main`;
- every Monday as a central health check.

No workflow automatically merges instruction changes. Branch protection should require the validation workflow before merging.

### Status and notifications

Each machine writes logs and a machine-readable status file under its user state directory. The status includes:

- machine name;
- installed commit;
- latest `origin/main` commit;
- ahead/behind state;
- dirty or clean state;
- last validation and synchronization result;
- last successful run time.

Scheduled failures produce a macOS notification and a non-zero exit status. Secrets, access tokens, and machine-specific absolute paths are never committed.

## Schedule

The macOS LaunchAgent runs safe synchronization at 09:00 and 17:00 local time each day.

GitHub Actions performs the central weekly health check each Monday at 07:00 UTC. Pull-request and `main` validation remains event-driven.

Automatic draft publishing is deliberately not scheduled. A dirty checkout prompts the operator to review and run `scripts/publish-skill-changes`.

## Error Handling

| Condition | Result |
| --- | --- |
| Checkout is dirty | Stop, preserve files, write status, and notify |
| Checkout is not on `main` | Stop and report the active branch |
| Fetch fails | Keep the installed commit and report the network/authentication failure |
| Remote validation fails | Keep the installed commit and report the failing check |
| Fast-forward is impossible | Stop without merging or rebasing |
| Existing install is not a managed symlink | Bootstrap backs it up before replacement |
| Draft PR creation fails | Keep the local branch and commit; report the retry command |
| Scheduler overlaps a previous run | Exit cleanly after reporting the existing lock |

## Testing Strategy

Shell integration tests create temporary local Git repositories and isolated fake home/state directories. Tests cover:

- a clean checkout fast-forwards to a valid remote commit;
- dirty and non-`main` checkouts are preserved and rejected;
- an invalid remote commit never replaces the installed commit;
- bootstrap creates correct symlinks and retains recoverable backups;
- repeated bootstrap and synchronization runs are idempotent;
- overlapping runs respect the lock;
- the publisher creates a draft branch/PR request but never invokes merge;
- status output accurately reports commit and dirty/behind state.

Every new behavior is introduced with a failing test before implementation. GitHub Actions runs repository validation on Ubuntu and the machine-maintenance integration tests on macOS.

## Rollout

1. Add the validator, synchronizer, bootstrap, publisher, hooks, tests, manifest, workflow, and operator documentation to the current draft pull request.
2. Validate the pull request from a fresh clone and merge it after review.
3. Create or update a stable managed checkout on the current machine and run bootstrap for Codex.
4. Run the one-command bootstrap on the other two machines, selecting Codex, Claude, or both.
5. Confirm all three machines report the same `main` commit after the next scheduled synchronization.

The current environment can configure only the current machine. The two remaining machines require someone with access to run the committed bootstrap command once.

## Acceptance Criteria

- All three web-development skills are sourced from one validated `main` commit on each configured machine.
- Scheduled synchronization cannot destroy or hide local changes.
- Invalid upstream changes cannot replace the currently installed version.
- Local improvements can be published as reviewable draft pull requests from any machine.
- No automation merges skill-instruction changes.
- Repository validation is mandatory and reproducible locally and in GitHub Actions.
- The current machine runs the approved twice-daily schedule after the implementation is merged.
