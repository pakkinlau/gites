from __future__ import annotations

from pathlib import Path


def discover_repositories(root: Path) -> list[Path]:
    root = root.expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Root directory does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Root path is not a directory: {root}")

    repos: list[Path] = []
    for child in sorted(root.iterdir(), key=lambda path: path.name.lower()):
        try:
            if child.name.startswith(".") or not child.is_dir():
                continue
            if (child / ".git").exists():
                repos.append(child)
        except OSError:
            continue
    return repos
