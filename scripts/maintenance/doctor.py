from __future__ import annotations

import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote

from .common import load_manifest, run_command


ALLOWED_FRONTMATTER_KEYS = {"allowed-tools", "description", "license", "metadata", "name"}
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
LOCAL_LINK_DOCS = (
    "README.md",
    "CONTRIBUTING.md",
    "marketing/README.md",
    "marketing/content-creation/README.md",
    "marketing/web-development/README.md",
    "marketing/content-creation/man-digital-blog-graphics/README.md",
    "marketing/content-creation/man-digital-youtube-scripts/README.md",
)


@dataclass(frozen=True)
class Issue:
    path: str
    message: str


@dataclass(frozen=True)
class DoctorReport:
    issues: tuple[Issue, ...]
    skill_count: int
    python_count: int
    shell_count: int
    link_count: int
    managed_count: int
    psi_checked: bool = False
    cms_checked: bool = False

    @property
    def ok(self) -> bool:
        return not self.issues

    def render(self) -> str:
        status = "PASS" if self.ok else "FAIL"
        lines = [
            f"{status}: {self.skill_count} skills, {self.python_count} Python files, "
            f"{self.shell_count} shell files, {self.link_count} links, "
            f"{self.managed_count} managed skills"
        ]
        lines.extend(f"- {issue.path}: {issue.message}" for issue in self.issues)
        return "\n".join(lines)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["ok"] = self.ok
        return payload


def _frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["SKILL.md must start with YAML frontmatter"]
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, ["frontmatter closing delimiter is missing"]

    values: dict[str, str] = {}
    errors: list[str] = []
    current_key: str | None = None
    block_lines: list[str] = []

    def finish_block() -> None:
        nonlocal current_key, block_lines
        if current_key is not None:
            values[current_key] = " ".join(line.strip() for line in block_lines if line.strip())
        current_key = None
        block_lines = []

    for line in lines[1:end]:
        if line.startswith((" ", "\t")):
            if current_key is not None:
                block_lines.append(line)
            continue
        finish_block()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, raw_value = match.group(1), (match.group(2) or "").strip()
        if raw_value in {">", ">-", "|", "|-"}:
            current_key = key
            continue
        values[key] = raw_value.strip('"\'')
    finish_block()
    return values, errors


def _skill_issues(skill_file: Path, repo: Path) -> list[Issue]:
    relative = skill_file.relative_to(repo).as_posix()
    values, errors = _frontmatter(skill_file.read_text(encoding="utf-8"))
    issues = [Issue(relative, error) for error in errors]
    unexpected = sorted(set(values) - ALLOWED_FRONTMATTER_KEYS)
    if unexpected:
        issues.append(Issue(relative, f"unsupported frontmatter keys: {', '.join(unexpected)}"))
    name = values.get("name", "").strip()
    description = values.get("description", "").strip()
    if not name:
        issues.append(Issue(relative, "name is required"))
    elif not SKILL_NAME_PATTERN.fullmatch(name):
        issues.append(Issue(relative, "name must use lowercase kebab-case"))
    if not description:
        issues.append(Issue(relative, "description is required"))
    elif len(description) > 1024:
        issues.append(Issue(relative, f"description is {len(description)} characters; maximum is 1024"))
    return issues


def _tracked_marketing_files(repo: Path, suffix: str) -> list[Path]:
    marketing = repo / "marketing"
    if not marketing.is_dir():
        return []
    return sorted(
        path
        for path in marketing.rglob(f"*{suffix}")
        if "references/source" not in path.as_posix() and ".git" not in path.parts
    )


def _link_issues(repo: Path) -> tuple[list[Issue], int]:
    issues: list[Issue] = []
    checked = 0
    for relative_name in LOCAL_LINK_DOCS:
        source = repo / relative_name
        if not source.is_file():
            continue
        for raw_target in MARKDOWN_LINK_PATTERN.findall(source.read_text(encoding="utf-8")):
            target = raw_target.strip().split("#", maxsplit=1)[0]
            if not target or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            checked += 1
            resolved = (source.parent / unquote(target)).resolve()
            if not resolved.exists():
                issues.append(Issue(relative_name, f"missing local link target: {raw_target}"))
    return issues, checked


def validate_repository(
    repo: Path,
    *,
    quick: bool = False,
    bootstrap_cms: bool = False,
) -> DoctorReport:
    repo = repo.resolve()
    issues: list[Issue] = []
    skill_files = sorted(
        path
        for path in (repo / "marketing").rglob("SKILL.md")
        if "references/source" not in path.as_posix()
    ) if (repo / "marketing").is_dir() else []
    for skill_file in skill_files:
        issues.extend(_skill_issues(skill_file, repo))

    python_files = _tracked_marketing_files(repo, ".py")
    for path in python_files:
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except (SyntaxError, UnicodeError) as error:
            issues.append(Issue(path.relative_to(repo).as_posix(), f"Python syntax error: {error}"))

    shell_files = _tracked_marketing_files(repo, ".sh")
    for path in shell_files:
        result = run_command(["bash", "-n", str(path)], cwd=repo, check=False)
        if result.returncode:
            issues.append(
                Issue(path.relative_to(repo).as_posix(), result.stderr.strip() or "shell syntax check failed")
            )

    link_issues, link_count = _link_issues(repo)
    issues.extend(link_issues)
    managed = load_manifest(repo)
    for skill in managed:
        skill_path = repo / skill.repo_path
        skill_file = skill_path / "SKILL.md"
        if not skill_file.is_file():
            issues.append(Issue("automation/managed-skills.txt", f"missing managed skill: {skill.repo_path}"))
            continue
        values, _ = _frontmatter(skill_file.read_text(encoding="utf-8"))
        if values.get("name") != skill.install_name:
            issues.append(
                Issue(
                    "automation/managed-skills.txt",
                    f"install name {skill.install_name!r} does not match {skill.repo_path}/SKILL.md",
                )
            )

    psi_checked = False
    cms_checked = False
    if not quick:
        psi = repo / "marketing/web-development/auditing-web-vitals/scripts/psi"
        if psi.is_file():
            result = run_command([str(psi), "--help"], cwd=repo, check=False)
            psi_checked = True
            if result.returncode:
                issues.append(Issue(psi.relative_to(repo).as_posix(), "PSI CLI --help failed"))

        cms = repo / "marketing/web-development/man-digital-cms-pages"
        ensure = cms / "scripts/ensure-source.sh"
        validate = cms / "scripts/validate-source.sh"
        source = cms / "references/source"
        if bootstrap_cms and ensure.is_file():
            result = run_command([str(ensure)], cwd=repo, check=False)
            if result.returncode:
                issues.append(Issue(ensure.relative_to(repo).as_posix(), result.stderr.strip() or "CMS bootstrap failed"))
            elif result.stdout.strip():
                source = Path(result.stdout.strip().splitlines()[-1])
        if source.is_dir() and validate.is_file():
            result = run_command([str(validate), str(source)], cwd=repo, check=False)
            cms_checked = True
            if result.returncode:
                issues.append(Issue(validate.relative_to(repo).as_posix(), result.stderr.strip() or "CMS validation failed"))

    return DoctorReport(
        issues=tuple(issues),
        skill_count=len(skill_files),
        python_count=len(python_files),
        shell_count=len(shell_files),
        link_count=link_count,
        managed_count=len(managed),
        psi_checked=psi_checked,
        cms_checked=cms_checked,
    )
