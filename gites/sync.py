from __future__ import annotations

import uuid

from .git_backend import GitBackend
from .ledger import append_run
from .models import RepoSyncResult, SyncOptions, SyncRunResult
from .planner import build_plan


def run_sync(options: SyncOptions, git: GitBackend | None = None) -> SyncRunResult:
    if options.apply and not options.message:
        raise ValueError("--message is required when using --apply")

    git = git or GitBackend()
    run_id = str(uuid.uuid4())
    entries = build_plan(options, git=git)
    results: list[RepoSyncResult] = []

    for entry in entries:
        repo = entry.repo
        result = RepoSyncResult(
            name=repo.name,
            path=str(repo.path),
            action=entry.action,
            status="planned",
            old_head=repo.head,
            reasons=list(entry.reasons),
        )

        if not options.apply:
            result.status = "dry-run"
            result.new_head = repo.head
            results.append(result)
            continue

        if entry.action == "noop":
            result.status = "skipped"
            result.new_head = repo.head
            results.append(result)
            continue

        if not entry.can_sync:
            result.status = "refused"
            result.new_head = repo.head
            results.append(result)
            continue

        try:
            add = git.run(repo.path, ["add", "--all"])
            if not add.ok:
                result.status = "failed"
                result.error = add.output or "git add failed"
                results.append(result)
                continue

            diff = git.run(repo.path, ["diff", "--cached", "--quiet"])
            if diff.ok:
                result.status = "skipped"
                result.action = "noop"
                result.reasons.append("nothing staged after git add")
                result.new_head = repo.head
                results.append(result)
                continue

            commit = git.run(repo.path, ["commit", "-m", options.message or ""])
            if not commit.ok:
                result.status = "failed"
                result.error = commit.output or "git commit failed"
                results.append(result)
                continue

            new_head = git.value(repo.path, ["rev-parse", "HEAD"])
            result.commit = new_head
            result.new_head = new_head

            push = git.run(repo.path, ["push"])
            if not push.ok:
                result.status = "failed"
                result.error = push.output or "git push failed"
                results.append(result)
                continue

            result.status = "pushed"
            results.append(result)
        except Exception as exc:
            result.status = "failed"
            result.error = str(exc)
            results.append(result)

    run_result = SyncRunResult(
        run_id=run_id,
        root=options.root,
        message=options.message,
        applied=options.apply,
        repos=results,
    )
    append_run(run_result)
    return run_result
