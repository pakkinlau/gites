from __future__ import annotations

import subprocess
from pathlib import Path

from .models import CommandResult


class GitError(RuntimeError):
    pass


class GitBackend:
    def __init__(self, quiet: bool = True, timeout: float | None = None):
        self.quiet = quiet
        self.timeout = timeout

    def run(self, repo: Path, args: list[str], check: bool = False, timeout: float | None = None) -> CommandResult:
        command = ("git", *args)
        try:
            completed = subprocess.run(
                command,
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=self.timeout if timeout is None else timeout,
            )
        except subprocess.TimeoutExpired as exc:
            return CommandResult(
                command=command,
                cwd=repo,
                returncode=124,
                stdout=(exc.stdout or "").strip() if isinstance(exc.stdout, str) else "",
                stderr=f"command timed out after {exc.timeout} seconds",
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

    def value(self, repo: Path, args: list[str], timeout: float | None = None) -> str | None:
        result = self.run(repo, args, timeout=timeout)
        if not result.ok:
            return None
        return result.stdout.strip() or None
