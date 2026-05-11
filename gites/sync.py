from __future__ import annotations

import uuid
from datetime import datetime

from .change_summary import checkpoint_subject, summarize_changed_files
from .git_backend import GitBackend
from .ledger import append_run
from .models import ChangedFile, RepoSyncResult, SyncOptions, SyncRunResult
from .planner import build_plan


def run_sync(options: SyncOptions, git: GitBackend | None = None) -> SyncRunResult:
    if options.apply and not options.message and not options.auto_message:
        raise ValueError("--message is required when using --apply")

    git = git or GitBackend()
    run_id = str(uuid.uuid4())
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
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
            changed_files=list(repo.changed_files),
            reasons=list(entry.reasons),
        )
        if entry.can_sync:
            result.commit_message = _commit_message_for_repo(
                options=options,
                repo_name=repo.name,
                run_id=run_id,
                timestamp=timestamp,
                changed_files=repo.changed_files,
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

            commit = git.run(repo.path, ["commit", "-m", result.commit_message or ""])
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


def _commit_message_for_repo(
    *,
    options: SyncOptions,
    repo_name: str,
    run_id: str,
    timestamp: str,
    changed_files: tuple[ChangedFile, ...],
) -> str:
    if options.message:
        return options.message

    instance = options.instance_name or "-"
    subject = checkpoint_subject(changed_files)
    return "\n".join(
        [
            subject,
            "",
            "Gites checkpoint",
            "",
            f"Instance: {instance}",
            f"Repo: {repo_name}",
            f"Run: {run_id}",
            f"Time: {timestamp}",
            f"Changes: {summarize_changed_files(changed_files)}",
        ]
    )
