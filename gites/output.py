from __future__ import annotations

from collections import Counter

from .models import PlanEntry, SyncRunResult


def render_plan(entries: list[PlanEntry]) -> str:
    headers = ["repo", "branch", "ahead", "behind", "dirty", "untracked", "action", "reason"]
    rows = []
    for entry in entries:
        repo = entry.repo
        rows.append(
            [
                repo.name,
                repo.branch or "-",
                str(repo.ahead),
                str(repo.behind),
                "yes" if repo.dirty else "no",
                "yes" if repo.untracked else "no",
                entry.action,
                "; ".join(entry.reasons),
            ]
        )
    return _table(headers, rows)


def render_run(result: SyncRunResult) -> str:
    summary = f"run_id: {result.run_id}\napplied: {'yes' if result.applied else 'no'}"
    clean = [repo for repo in result.repos if repo.action == "noop" and repo.status in {"dry-run", "skipped"}]
    active = [repo for repo in result.repos if repo.action == "sync" or repo.status in {"pushed", "failed"}]
    refused = [repo for repo in result.repos if repo.status == "refused" or repo.action == "refuse"]

    failed = [repo for repo in result.repos if repo.status == "failed"]
    active_without_failed = [repo for repo in active if repo.status != "failed"]
    summary_parts = [
        f"clean={len(clean)}",
        f"{'pushed' if result.applied else 'would_sync'}={len(active_without_failed)}",
        f"refused={len(refused)}",
        f"failed={len(failed)}",
    ]
    lines = [summary, f"summary: {', '.join(summary_parts)}"]

    if clean:
        lines.append(f"clean: {len(clean)} repo(s) had no changes.")

    if active_without_failed:
        title = "pushed" if result.applied else "would sync"
        lines.append("")
        lines.append(f"{title}:")
        for repo in active_without_failed:
            lines.append(f"- {repo.name}: {_change_stats(repo.changed_files)}; {_head_range(repo.old_head, repo.new_head)}")

    if refused:
        lines.append("")
        lines.append("refused:")
        for repo in refused:
            reason = "; ".join(repo.reasons) or repo.error or "refused"
            detail = _change_stats(repo.changed_files)
            lines.append(f"- {repo.name}: {detail}; {reason}")

    if failed:
        lines.append("")
        lines.append("failed:")
        for repo in failed:
            lines.append(f"- {repo.name}: {_change_stats(repo.changed_files)}; {_head_range(repo.old_head, repo.new_head)}")
            if repo.error:
                lines.append(f"  error: {_one_line(repo.error)}")

    return "\n".join(lines)


def _short(value: str | None) -> str:
    return value[:12] if value else "-"


def _head_range(old_head: str | None, new_head: str | None) -> str:
    old = _short(old_head)
    new = _short(new_head)
    if old == new:
        return f"head {old}"
    return f"{old} -> {new}"


def _change_stats(changed_files) -> str:
    if not changed_files:
        return "no file changes"
    counts = Counter(_change_kind(changed.status) for changed in changed_files)
    ordered = [
        ("modified", counts["modified"]),
        ("added", counts["added"]),
        ("deleted", counts["deleted"]),
        ("renamed", counts["renamed"]),
        ("untracked", counts["untracked"]),
        ("conflicted", counts["conflicted"]),
        ("other", counts["other"]),
    ]
    parts = [f"{count} {name}" for name, count in ordered if count]
    total = len(changed_files)
    return f"{total} file(s): {', '.join(parts)}"


def _change_kind(status: str) -> str:
    if "U" in status:
        return "conflicted"
    if status == "??":
        return "untracked"
    if "R" in status or "C" in status:
        return "renamed"
    if "D" in status:
        return "deleted"
    if "A" in status:
        return "added"
    if "M" in status:
        return "modified"
    return "other"


def _one_line(value: str) -> str:
    return " ".join(value.split())


def _table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "No repositories found."
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))
    lines = []
    lines.append("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    lines.append("  ".join("-" * width for width in widths))
    for row in rows:
        lines.append("  ".join(cell.ljust(widths[index]) for index, cell in enumerate(row)))
    return "\n".join(lines)
