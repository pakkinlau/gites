from __future__ import annotations

from collections import Counter

from .models import ChangedFile


def summarize_changed_files(changed_files: list[ChangedFile] | tuple[ChangedFile, ...]) -> str:
    if not changed_files:
        return "no file changes"
    counts = Counter(change_kind(changed.status) for changed in changed_files)
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


def checkpoint_subject(changed_files: list[ChangedFile] | tuple[ChangedFile, ...]) -> str:
    count = len(changed_files)
    noun = "file" if count == 1 else "files"
    return f"chore(gites): checkpoint {count} {noun}"


def change_kind(status: str) -> str:
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
