from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .discovery import discover_repositories
from .git_backend import GitBackend
from .models import ChangedFile, PlanEntry, RepoState, SyncOptions

UNMERGED_CODES = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}


def inspect_repo(path: Path, git: GitBackend | None = None, include_untracked: bool = True) -> RepoState:
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

    status_args = ["status", "--porcelain=v1"]
    if not include_untracked:
        status_args.append("--untracked-files=no")
    status = git.run(path, status_args)
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
    selected = set(options.repo_names)
    repo_paths = [path for path in discover_repositories(options.root) if not selected or path.name in selected]
    if options.progress:
        print(f"Inspecting {len(repo_paths)} repos with {max(1, options.jobs)} worker(s)...", file=sys.stderr)

    if len(repo_paths) <= 1 or options.jobs <= 1:
        entries = []
        local_git = git or GitBackend(timeout=options.git_timeout_seconds)
        for index, repo_path in enumerate(repo_paths, start=1):
            entries.append(_plan_one(repo_path, options, local_git))
            if options.progress:
                print(f"[{index}/{len(repo_paths)}] {repo_path.name}", file=sys.stderr)
        return entries

    by_name: dict[str, PlanEntry] = {}
    max_workers = max(1, min(options.jobs, len(repo_paths)))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_plan_one, repo_path, options, GitBackend(timeout=options.git_timeout_seconds)): repo_path
            for repo_path in repo_paths
        }
        completed = 0
        for future in as_completed(futures):
            repo_path = futures[future]
            completed += 1
            try:
                entry = future.result()
            except Exception as exc:
                repo = RepoState(
                    name=repo_path.name,
                    path=repo_path,
                    is_git_repo=True,
                    errors=(str(exc),),
                )
                entry = PlanEntry(repo=repo, action="refuse", reasons=(str(exc),))
            by_name[repo_path.name] = entry
            if options.progress:
                print(f"[{completed}/{len(repo_paths)}] {repo_path.name} -> {entry.action}", file=sys.stderr)

    entries = [by_name[path.name] for path in repo_paths if path.name in by_name]
    return entries


def _plan_one(repo_path: Path, options: SyncOptions, git: GitBackend) -> PlanEntry:
    repo = inspect_repo(repo_path, git=git, include_untracked=options.include_untracked)
    reasons = preflight_reasons(repo, options)
    if reasons:
        action = "refuse"
    elif not repo.dirty:
        action = "noop"
        reasons = ["working tree clean"]
    else:
        action = "sync"
    return PlanEntry(repo=repo, action=action, reasons=tuple(reasons))


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
