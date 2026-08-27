# Multi-Machine Skill Maintenance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and activate a safe, testable system that keeps the CMS, Figma website design, and PSI skills synchronized across macOS machines without overwriting local work or automatically merging instruction changes.

**Architecture:** A dependency-free Python maintenance package provides repository validation, safe Git synchronization, symlink bootstrap, status reporting, and draft-PR publishing. Small executable wrappers expose those functions to versioned Git hooks, GitHub Actions, and a macOS LaunchAgent. Every scheduled update validates a detached candidate worktree before fast-forwarding the managed checkout.

**Tech Stack:** Python 3 standard library, POSIX shell, Git, GitHub CLI, macOS `launchd`, GitHub Actions, `unittest`.

## Global Constraints

- `main` in `MAN-Digital/mandigital-claude-skills` is the only canonical source.
- The default managed skills are `man-digital-cms-pages`, `man-digital-figma-website-design`, and `auditing-web-vitals` under `marketing/web-development/`.
- Synchronization must never reset, stash, force-push, overwrite a dirty checkout, or auto-merge a pull request.
- A fetched commit must pass validation in a detached worktree before the installed checkout advances.
- Existing non-managed install folders must be moved to timestamped recoverable backups before symlinks replace them.
- Scheduled synchronization runs at 09:00 and 17:00 local time.
- GitHub performs pull-request and `main` validation plus a Monday 07:00 UTC health check.
- Production code must be introduced only after its test has failed for the expected missing behavior.
- Runtime code may use only Python's standard library and commands already required by the workflow: `git`, `bash`, `python3`, `gh`, and macOS `launchctl` for installation.

## File Map

- `automation/managed-skills.txt`: canonical list of repository paths and installed names.
- `scripts/maintenance/common.py`: command execution, manifest parsing, Git helpers, locks, and atomic status writes.
- `scripts/maintenance/doctor.py`: repository, skill metadata, script, link, PSI, and CMS validation.
- `scripts/maintenance/sync.py`: detached-candidate validation and fast-forward synchronization.
- `scripts/maintenance/bootstrap.py`: symlink migration, backup creation, hook setup, and LaunchAgent installation.
- `scripts/maintenance/publish.py`: confirmed branch, commit, push, and draft-PR flow; the publisher never merges.
- `scripts/maintenance/status.py`: machine health snapshot generation.
- `scripts/skills-doctor`, `scripts/skills-sync`, `scripts/skills-status`, `scripts/install-machine-maintenance`, `scripts/publish-skill-changes`: executable CLI entry points.
- `.githooks/pre-commit`, `.githooks/pre-push`: versioned validation hooks.
- `.github/workflows/validate-skills.yml`: CI and scheduled central validation.
- `tests/maintenance/`: isolated `unittest` coverage for all behavior.
- `MAINTENANCE.md`: operator setup, recovery, publishing, and second/third-machine instructions.
- `README.md`: link to the maintenance guide.

---

### Task 1: Core manifest and repository doctor

**Files:**
- Create: `automation/managed-skills.txt`
- Create: `scripts/maintenance/__init__.py`
- Create: `scripts/maintenance/common.py`
- Create: `scripts/maintenance/doctor.py`
- Create: `scripts/skills-doctor`
- Create: `tests/maintenance/__init__.py`
- Create: `tests/maintenance/test_doctor.py`

**Interfaces:**
- Produces: `ManagedSkill(repo_path: str, install_name: str)`.
- Produces: `load_manifest(repo: Path, manifest: Path | None = None) -> list[ManagedSkill]`.
- Produces: `run_command(args: Sequence[str], cwd: Path | None = None, check: bool = True) -> CompletedProcess[str]`.
- Produces: `Issue(path: str, message: str)` and `DoctorReport(issues: tuple[Issue, ...], skill_count: int, python_count: int, shell_count: int, link_count: int)` with an `ok` property.
- Produces: `validate_repository(repo: Path, *, quick: bool = False, bootstrap_cms: bool = False) -> DoctorReport`.

- [ ] **Step 1: Add the manifest and write failing doctor tests**

Create `automation/managed-skills.txt` with exactly:

```text
marketing/web-development/man-digital-cms-pages|man-digital-cms-pages
marketing/web-development/man-digital-figma-website-design|man-digital-figma-website-design
marketing/web-development/auditing-web-vitals|auditing-web-vitals
```

Create tests that import the not-yet-existing package and assert:

```python
class DoctorTests(unittest.TestCase):
    def test_manifest_resolves_default_three(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        skills = load_manifest(repo_root)
        self.assertEqual(
            [skill.install_name for skill in skills],
            ["man-digital-cms-pages", "man-digital-figma-website-design", "auditing-web-vitals"],
        )
        self.assertTrue(all((repo_root / skill.repo_path / "SKILL.md").is_file() for skill in skills))

    def test_invalid_skill_frontmatter_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            skill = repo / "marketing" / "broken-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: broken-skill\nversion: 1\n---\n")
            report = validate_repository(repo, quick=True)
            self.assertFalse(report.ok)
            self.assertTrue(any("description" in issue.message or "version" in issue.message for issue in report.issues))
```

- [ ] **Step 2: Run the doctor tests and verify RED**

Run:

```bash
python3 -m unittest tests.maintenance.test_doctor -v
```

Expected: import failure for `scripts.maintenance` because the maintenance package does not exist.

- [ ] **Step 3: Implement common helpers and dependency-free validation**

Implement manifest parsing, frontmatter extraction, allowed-key validation, skill-name matching, description-length checks, Python `compile()`, `bash -n`, configured Markdown link checking, PSI `--help`, and optional CMS bootstrap/validation. The quick mode must skip network-capable CMS bootstrap and run metadata/script checks only.

The CLI must support:

```text
scripts/skills-doctor --repo PATH [--quick] [--bootstrap-cms] [--json]
```

Exit `0` when `DoctorReport.ok` is true and `1` otherwise.

- [ ] **Step 4: Run tests and the doctor against the real repository**

Run:

```bash
python3 -m unittest tests.maintenance.test_doctor -v
scripts/skills-doctor --repo . --bootstrap-cms
```

Expected: tests pass; the repository report contains 27 valid skills, 20 Python files, 6 shell scripts, working PSI help, and a successful 393-JSON CMS validation.

- [ ] **Step 5: Commit the doctor**

```bash
git add automation/managed-skills.txt scripts/maintenance scripts/skills-doctor tests/maintenance
git commit -m "feat: add shared skill health checks"
```

---

### Task 2: Safe synchronizer and status reporting

**Files:**
- Create: `scripts/maintenance/sync.py`
- Create: `scripts/maintenance/status.py`
- Create: `scripts/skills-sync`
- Create: `scripts/skills-status`
- Create: `tests/maintenance/helpers.py`
- Create: `tests/maintenance/test_sync.py`
- Create: `tests/maintenance/test_status.py`

**Interfaces:**
- Consumes: `run_command`, `load_manifest`, and `validate_repository` from Task 1.
- Produces: `SyncResult(changed: bool, commit: str, message: str)`.
- Produces: `sync_checkout(repo: Path, state_dir: Path, install_roots: Sequence[Path], *, remote: str = "origin", branch: str = "main") -> SyncResult`.
- Produces: `collect_status(repo: Path, state_dir: Path, install_roots: Sequence[Path]) -> dict[str, object]`.
- Produces: `write_status(state_dir: Path, payload: Mapping[str, object]) -> Path` using a temporary file followed by `os.replace()`.

- [ ] **Step 1: Write failing synchronization tests using temporary Git repositories**

Use `tests/maintenance/helpers.py` to create a bare remote, seed repository, managed clone, and valid minimal skill. Add real integration tests:

```python
class SyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = GitFixture(Path(self.temporary.name))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_clean_checkout_fast_forwards_after_candidate_validation(self) -> None:
        old = self.fixture.managed_head
        new = self.fixture.push_valid_change()
        result = sync_checkout(self.fixture.managed, self.fixture.state, [])
        self.assertTrue(result.changed)
        self.assertEqual(result.commit, new)
        self.assertNotEqual(self.fixture.head(self.fixture.managed), old)

    def test_dirty_checkout_is_preserved(self) -> None:
        marker = self.fixture.managed / "local-note.txt"
        marker.write_text("unfinished")
        before = self.fixture.head(self.fixture.managed)
        with self.assertRaisesRegex(SyncError, "dirty"):
            sync_checkout(self.fixture.managed, self.fixture.state, [])
        self.assertEqual(marker.read_text(), "unfinished")
        self.assertEqual(self.fixture.head(self.fixture.managed), before)

    def test_invalid_remote_commit_does_not_advance(self) -> None:
        self.fixture.push_invalid_skill()
        before = self.fixture.head(self.fixture.managed)
        with self.assertRaisesRegex(SyncError, "validation"):
            sync_checkout(self.fixture.managed, self.fixture.state, [])
        self.assertEqual(self.fixture.head(self.fixture.managed), before)
```

- [ ] **Step 2: Run synchronization tests and verify RED**

Run:

```bash
python3 -m unittest tests.maintenance.test_sync tests.maintenance.test_status -v
```

Expected: import failure for missing `scripts.maintenance.sync` and `scripts.maintenance.status`.

- [ ] **Step 3: Implement locking, detached validation, fast-forward, and status**

Use an atomic lock directory under `state_dir`. Reject dirty or non-`main` checkouts. Fetch without checkout mutation, validate `origin/main` in a temporary detached worktree using the current trusted validator, require `git merge-base --is-ancestor HEAD origin/main`, then run `git merge --ff-only origin/main`. Always remove the temporary worktree and lock in `finally` blocks.

The sync CLI must support repeatable `--install-root PATH` arguments and write a JSON status file whether it succeeds or fails. `skills-status --json` must print the status snapshot without modifying Git state.

- [ ] **Step 4: Verify GREEN and run the complete maintenance tests**

```bash
python3 -m unittest discover -s tests/maintenance -v
scripts/skills-status --repo . --state-dir "$PWD/.test-state" --json
```

Expected: clean-update, dirty-refusal, invalid-candidate, lock, idempotency, and status tests pass.

- [ ] **Step 5: Commit synchronization**

```bash
git add scripts/maintenance/sync.py scripts/maintenance/status.py scripts/skills-sync scripts/skills-status tests/maintenance
git commit -m "feat: add safe machine skill synchronization"
```

---

### Task 3: Machine bootstrap, symlink migration, and LaunchAgent

**Files:**
- Create: `scripts/maintenance/bootstrap.py`
- Create: `scripts/install-machine-maintenance`
- Create: `tests/maintenance/test_bootstrap.py`

**Interfaces:**
- Consumes: `ManagedSkill`, `load_manifest`, `run_command`, and `validate_repository`.
- Produces: `BootstrapResult(symlinks: tuple[Path, ...], backups: tuple[Path, ...], plist_path: Path)`.
- Produces: `configure_machine(repo: Path, state_dir: Path, install_roots: Sequence[Path], launch_agents_dir: Path, *, load_agent: bool = True) -> BootstrapResult`.
- Produces: `build_launch_agent(repo: Path, state_dir: Path, install_roots: Sequence[Path]) -> dict[str, object]`.

- [ ] **Step 1: Write failing backup, symlink, idempotency, and schedule tests**

```python
class BootstrapTests(unittest.TestCase):
    def test_existing_install_is_backed_up_before_symlink(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install_root = root / "skills"
            existing = install_root / "auditing-web-vitals"
            existing.mkdir(parents=True)
            (existing / "local-change.txt").write_text("keep me")
            result = configure_machine(repo_root, root / "state", [install_root], root / "LaunchAgents", load_agent=False)
            self.assertTrue(existing.is_symlink())
            self.assertTrue(any((backup / "local-change.txt").read_text() == "keep me" for backup in result.backups))

    def test_launch_agent_runs_twice_daily(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = build_launch_agent(repo_root, root / "state", [root / "skills"])
            self.assertEqual(payload["StartCalendarInterval"], [{"Hour": 9, "Minute": 0}, {"Hour": 17, "Minute": 0}])
```

- [ ] **Step 2: Run bootstrap tests and verify RED**

```bash
python3 -m unittest tests.maintenance.test_bootstrap -v
```

Expected: import failure for missing `scripts.maintenance.bootstrap`.

- [ ] **Step 3: Implement safe bootstrap**

Use `plistlib` for the LaunchAgent, `shutil.move` for recoverable backups, and absolute symlink targets. Refuse to replace a path outside the selected install roots. Configure `core.hooksPath=.githooks`. Support `--codex`, `--claude`, repeatable `--install-root`, `--no-load`, and explicit `--repo`/`--state-dir` arguments.

When loading the agent on macOS, use `launchctl bootout gui/{uid} PLIST` if already loaded, ignore only the documented not-loaded result, then use `launchctl bootstrap gui/{uid} PLIST`.

- [ ] **Step 4: Run tests and a fully isolated bootstrap**

```bash
python3 -m unittest discover -s tests/maintenance -v
scripts/install-machine-maintenance --repo . --state-dir "$PWD/.test-state" --install-root "$PWD/.test-skills" --launch-agents-dir "$PWD/.test-agents" --no-load
scripts/skills-doctor --repo . --quick
```

Expected: three managed symlinks, one valid plist with 09:00/17:00 entries, idempotent second run, and no modifications outside the isolated paths.

- [ ] **Step 5: Commit bootstrap**

```bash
git add scripts/maintenance/bootstrap.py scripts/install-machine-maintenance tests/maintenance/test_bootstrap.py
git commit -m "feat: add macOS skill maintenance bootstrap"
```

---

### Task 4: Explicit draft-PR publisher

**Files:**
- Create: `scripts/maintenance/publish.py`
- Create: `scripts/publish-skill-changes`
- Create: `tests/maintenance/test_publish.py`

**Interfaces:**
- Consumes: `run_command` and `validate_repository`.
- Produces: `Publisher` with injected `runner: Callable[..., CompletedProcess[str]]` so tests observe real command arguments without invoking GitHub.
- Produces: `build_branch_name(machine: str, timestamp: datetime) -> str`.
- Produces: `publish_changes(repo: Path, machine: str, *, assume_yes: bool, runner=run_command) -> str` returning the draft PR URL.

- [ ] **Step 1: Write failing publisher tests**

```python
class PublishTests(unittest.TestCase):
    def test_publisher_opens_draft_pr_and_never_merges(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = create_dirty_git_repo(Path(directory))
            runner = RecordingRunner(pr_url="https://github.com/MAN-Digital/mandigital-claude-skills/pull/99")
            url = publish_changes(repo, "studio-mac", assume_yes=True, runner=runner)
            flattened = [argument for call in runner.calls for argument in call]
            self.assertIn("--draft", flattened)
            self.assertNotIn("merge", flattened)
            self.assertEqual(url, "https://github.com/MAN-Digital/mandigital-claude-skills/pull/99")

    def test_branch_name_is_machine_scoped(self) -> None:
        value = build_branch_name("Studio Mac", datetime(2026, 8, 17, 12, 30, tzinfo=timezone.utc))
        self.assertEqual(value, "machine/studio-mac/20260817-123000")
```

- [ ] **Step 2: Run publisher tests and verify RED**

```bash
python3 -m unittest tests.maintenance.test_publish -v
```

Expected: import failure for missing `scripts.maintenance.publish`.

- [ ] **Step 3: Implement the confirmed publish flow**

Show `git status --short` and `git diff` before confirmation. Validate before staging. Create the machine branch when currently on `main`, stage repository changes, commit with `chore: publish skill updates from {machine}`, push with tracking, and run `gh pr create --draft --base main --head BRANCH --title TITLE --body-file FILE`. If GitHub creation fails, retain the local branch and pushed commit and print the exact retry command.

Do not define or invoke any merge operation.

- [ ] **Step 4: Verify GREEN and inspect executable help**

```bash
python3 -m unittest discover -s tests/maintenance -v
scripts/publish-skill-changes --help
```

Expected: publisher tests pass, `--draft` is present in the recorded GitHub command, and no command contains `merge`.

- [ ] **Step 5: Commit publisher**

```bash
git add scripts/maintenance/publish.py scripts/publish-skill-changes tests/maintenance/test_publish.py
git commit -m "feat: publish machine skill changes as draft PRs"
```

---

### Task 5: Repository hooks, CI, and operator documentation

**Files:**
- Create: `.githooks/pre-commit`
- Create: `.githooks/pre-push`
- Create: `.github/workflows/validate-skills.yml`
- Create: `tests/maintenance/test_repository_wiring.py`
- Create: `MAINTENANCE.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: executable CLIs from Tasks 1–4.
- Produces: pre-commit quick validation, pre-push full offline validation, Ubuntu repository validation, macOS integration tests, and Monday 07:00 UTC scheduled validation.

- [ ] **Step 1: Write failing repository-wiring tests**

```python
class RepositoryWiringTests(unittest.TestCase):
    repo_root = Path(__file__).resolve().parents[2]

    def test_hooks_delegate_to_versioned_doctor(self) -> None:
        self.assertIn("scripts/skills-doctor --repo . --quick", (self.repo_root / ".githooks/pre-commit").read_text())
        self.assertIn("scripts/skills-doctor --repo .", (self.repo_root / ".githooks/pre-push").read_text())

    def test_workflow_has_pr_push_and_monday_schedule(self) -> None:
        workflow = (self.repo_root / ".github/workflows/validate-skills.yml").read_text()
        self.assertIn("pull_request:", workflow)
        self.assertIn("push:", workflow)
        self.assertIn("cron: '0 7 * * 1'", workflow)
        self.assertIn("macos-latest", workflow)
```

- [ ] **Step 2: Run wiring tests and verify RED**

```bash
python3 -m unittest tests.maintenance.test_repository_wiring -v
```

Expected: failure because hooks and workflow do not exist.

- [ ] **Step 3: Add hooks, workflow, and maintenance guide**

Make hooks fail closed when validation fails. The workflow must run `python3 -m unittest discover -s tests/maintenance -v` and `scripts/skills-doctor --repo . --bootstrap-cms`. Document initial setup, scheduled behavior, interpreting status, recovering backups, publishing changes, disabling the LaunchAgent, and running bootstrap on machines two and three.

Add a visible `Multi-machine maintenance` link to the root README.

- [ ] **Step 4: Run complete local validation**

```bash
python3 -m unittest discover -s tests/maintenance -v
scripts/skills-doctor --repo . --bootstrap-cms
bash -n .githooks/pre-commit .githooks/pre-push
git diff --check
```

Expected: all tests and validation pass without modifying tracked files.

- [ ] **Step 5: Commit repository wiring**

```bash
git add .githooks .github/workflows/validate-skills.yml tests/maintenance/test_repository_wiring.py MAINTENANCE.md README.md
git commit -m "ci: validate and schedule shared skill maintenance"
```

---

### Task 6: Remote verification, merge, and current-machine activation

**Files:**
- Modify: PR #5 title and body through GitHub.
- Install outside repository: stable checkout under `/Users/romeoman/Documents/Codex/mandigital-claude-skills`.
- Install outside repository: `/Users/romeoman/Library/LaunchAgents/com.man-digital.skills-sync.plist`.
- Install outside repository: managed symlinks under `/Users/romeoman/.codex/skills`.

**Interfaces:**
- Consumes: all scripts, workflow, documentation, and tests from Tasks 1–5.
- Produces: merged `main`, an active current-machine LaunchAgent, and verified managed Codex skill symlinks.

- [ ] **Step 1: Push the completed branch and update draft PR #5**

```bash
git push
gh pr edit 5 --title "chore: organize and automate shared skill maintenance" --body-file /tmp/mandigital-pr5-body.md
```

The PR body must include the folder migration, maintenance components, safety rules, test counts, and exact rollout limitation for the two inaccessible machines.

- [ ] **Step 2: Verify the pushed commit from a fresh clone**

Clone PR #5's head into a new temporary directory and run:

```bash
python3 -m unittest discover -s tests/maintenance -v
scripts/skills-doctor --repo . --bootstrap-cms
git status --porcelain
```

Expected: tests and doctor pass; status is empty.

- [ ] **Step 3: Mark ready and squash-merge with a head-SHA guard**

```bash
verified_head="$(git rev-parse HEAD)"
gh pr ready 5
gh pr merge 5 --squash --match-head-commit "$verified_head"
```

Expected: PR #5 is merged and its merge commit equals the new remote `main` head.

- [ ] **Step 4: Create/update the stable checkout and bootstrap this machine**

Clone or fast-forward `/Users/romeoman/Documents/Codex/mandigital-claude-skills` to remote `main`, then run:

```bash
scripts/install-machine-maintenance \
  --repo /Users/romeoman/Documents/Codex/mandigital-claude-skills \
  --state-dir /Users/romeoman/.local/state/man-digital-skills \
  --codex
```

Expected: the three existing Codex skill folders are safely backed up, replaced by symlinks into the stable checkout, Git hooks are configured, and the LaunchAgent is loaded.

- [ ] **Step 5: Verify the active current-machine installation**

```bash
launchctl print "gui/$(id -u)/com.man-digital.skills-sync"
/Users/romeoman/Documents/Codex/mandigital-claude-skills/scripts/skills-status \
  --repo /Users/romeoman/Documents/Codex/mandigital-claude-skills \
  --state-dir /Users/romeoman/.local/state/man-digital-skills \
  --install-root /Users/romeoman/.codex/skills \
  --json
```

Expected: LaunchAgent is loaded, checkout and `origin/main` match, worktree is clean, all three symlinks resolve into the stable checkout, and the last doctor result is successful.

- [ ] **Step 6: Record the other-machine bootstrap command**

Confirm `MAINTENANCE.md` gives machines two and three a single clone/bootstrap sequence and explicitly states that each machine must run it once with local access.
