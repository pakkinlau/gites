from __future__ import annotations

import subprocess
from pathlib import Path

from .models import CommandResult


class GitError(RuntimeError):
    pass


class GitBackend:
    def __init__(self, quiet: bool = True):
        self.quiet = quiet

    def run(self, repo: Path, args: list[str], check: bool = False) -> CommandResult:
        command = ("git", *args)
        completed = subprocess.run(
            command,
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        result = CommandResult(
            command=command,
            cwd=repo,
            returncode=completed.returncode,
            stdout=completed.stdout.strip(),
            stderr=completed.stderr.strip(),
        )
        if check and not result.ok:
            raise GitError(result.output or f"git command failed: {' '.join(command)}")
        return result

    def value(self, repo: Path, args: list[str]) -> str | None:
        result = self.run(repo, args)
        if not result.ok:
            return None
        return result.stdout.strip() or None
