from __future__ import annotations

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
    headers = ["repo", "status", "action", "old_head", "new_head", "reason"]
    rows = []
    for repo in result.repos:
        rows.append(
            [
                repo.name,
                repo.status,
                repo.action,
                _short(repo.old_head),
                _short(repo.new_head),
                "; ".join(repo.reasons) or (repo.error or ""),
            ]
        )
    summary = f"run_id: {result.run_id}\napplied: {'yes' if result.applied else 'no'}"
    return f"{summary}\n{_table(headers, rows)}"


def _short(value: str | None) -> str:
    return value[:12] if value else "-"


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
