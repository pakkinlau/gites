from __future__ import annotations

from pathlib import Path

from .discovery import discover_repositories
from .git_backend import GitBackend
from .models import ChangedFile, PlanEntry, RepoState, SyncOptions

UNMERGED_CODES = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}


def inspect_repo(path: Path, git: GitBackend | None = None) -> RepoState:
    git = git or GitBackend()
    errors: list[str] = []

    inside = git.run(path, ["rev-parse", "--is-inside-work-tree"])
    if not inside.ok or inside.stdout.strip() != "true":
        return RepoState(name=path.name, path=path, is_git_repo=False, errors=("not a git repository",))

    branch_result = git.run(path, ["symbolic-ref", "--quiet", "--short", "HEAD"])
    detached = not branch_result.ok
    branch = None if detached else branch_result.stdout.strip()

    head = git.value(path, ["rev-parse", "HEAD"])
    upstream = git.value(path, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    remote_url = git.value(path, ["remote", "get-url", "origin"])

    ahead = 0
    behind = 0
    if upstream:
        counts = git.run(path, ["rev-list", "--left-right", "--count", "HEAD...@{u}"])
        if counts.ok:
            parts = counts.stdout.split()
            if len(parts) == 2:
                ahead, behind = int(parts[0]), int(parts[1])
        else:
            errors.append(counts.output or "failed to compare branch with upstream")

    status = git.run(path, ["status", "--porcelain=v1"])
    changed_files: list[ChangedFile] = []
    conflicts = False
    untracked = False
    if status.ok and status.stdout:
        for line in status.stdout.splitlines():
            if not line:
                continue
            code = line[:2]
            raw_path = line[3:] if len(line) > 3 else ""
            if " -> " in raw_path:
                raw_path = raw_path.split(" -> ", 1)[1]
            changed_files.append(ChangedFile(path=raw_path, status=code))
            if code == "??":
                untracked = True
            if code in UNMERGED_CODES or "U" in code:
                conflicts = True
    elif not status.ok:
        errors.append(status.output or "failed to read git status")

    operation = _operation_in_progress(path)

    return RepoState(
        name=path.name,
        path=path,
        is_git_repo=True,
        branch=branch,
        upstream=upstream,
        remote_url=remote_url,
        head=head,
        ahead=ahead,
        behind=behind,
        detached=detached,
        dirty=bool(changed_files),
        untracked=untracked,
        conflicts=conflicts,
        operation_in_progress=operation,
        changed_files=tuple(changed_files),
        errors=tuple(errors),
    )


def build_plan(options: SyncOptions, git: GitBackend | None = None) -> list[PlanEntry]:
    git = git or GitBackend()
    entries: list[PlanEntry] = []
    selected = set(options.repo_names)
    for repo_path in discover_repositories(options.root):
        if selected and repo_path.name not in selected:
            continue
        repo = inspect_repo(repo_path, git=git)
        reasons = preflight_reasons(repo, options)
        if reasons:
            action = "refuse"
        elif not repo.dirty:
            action = "noop"
            reasons = ("working tree clean",)
        else:
            action = "sync"
        entries.append(PlanEntry(repo=repo, action=action, reasons=tuple(reasons)))
    return entries


def preflight_reasons(repo: RepoState, options: SyncOptions) -> list[str]:
    reasons = list(repo.errors)

    if not repo.is_git_repo:
        return reasons or ["not a git repository"]
    if repo.detached:
        reasons.append("detached HEAD")
    if repo.operation_in_progress:
        reasons.append(f"{repo.operation_in_progress} in progress")
    if repo.conflicts:
        reasons.append("unresolved conflicts")
    if options.branch and repo.branch != options.branch:
        reasons.append(f"wrong branch: expected {options.branch}, found {repo.branch or 'unknown'}")
    if not repo.remote_url:
        reasons.append("missing origin remote")
    if not repo.upstream:
        reasons.append("missing upstream branch")
    if repo.behind > 0 and repo.ahead > 0:
        reasons.append(f"branch diverged from upstream: ahead {repo.ahead}, behind {repo.behind}")
    elif repo.behind > 0:
        reasons.append(f"branch is behind upstream by {repo.behind} commit(s)")

    protected = _changed_protected_paths(repo, options.protected_paths)
    reasons.extend(f"protected path changed: {path}" for path in protected)

    large_files = _large_changed_files(repo, options.max_file_size_mb)
    reasons.extend(f"large file exceeds {options.max_file_size_mb} MB: {path}" for path in large_files)

    return reasons


def _operation_in_progress(repo: Path) -> str | None:
    git_dir = repo / ".git"
    markers = {
        "MERGE_HEAD": "merge",
        "rebase-merge": "rebase",
        "rebase-apply": "rebase",
        "CHERRY_PICK_HEAD": "cherry-pick",
        "REVERT_HEAD": "revert",
    }
    for marker, name in markers.items():
        if (git_dir / marker).exists():
            return name
    return None


def _changed_protected_paths(repo: RepoState, protected_paths: tuple[str, ...]) -> list[str]:
    matched: list[str] = []
    for changed in repo.changed_files:
        normalized = changed.path.replace("\\", "/")
        for protected in protected_paths:
            protected_normalized = protected.replace("\\", "/")
            if protected_normalized.endswith("/"):
                if normalized.startswith(protected_normalized):
                    matched.append(changed.path)
            elif normalized == protected_normalized or normalized.startswith(f"{protected_normalized}/"):
                matched.append(changed.path)
    return sorted(set(matched))


def _large_changed_files(repo: RepoState, max_file_size_mb: int) -> list[str]:
    threshold = max_file_size_mb * 1024 * 1024
    large: list[str] = []
    for changed in repo.changed_files:
        if "D" in changed.status:
            continue
        path = repo.path / changed.path
        if path.is_file() and path.stat().st_size > threshold:
            large.append(changed.path)
    return sorted(set(large))
