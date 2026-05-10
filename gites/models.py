from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class CommandResult:
    command: tuple[str, ...]
    cwd: Path
    returncode: int
    stdout: str = ""
    stderr: str = ""

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    @property
    def output(self) -> str:
        return "\n".join(part for part in (self.stdout, self.stderr) if part)


@dataclass(frozen=True)
class ChangedFile:
    path: str
    status: str


@dataclass(frozen=True)
class RepoState:
    name: str
    path: Path
    is_git_repo: bool
    branch: str | None = None
    upstream: str | None = None
    remote_url: str | None = None
    head: str | None = None
    ahead: int = 0
    behind: int = 0
    detached: bool = False
    dirty: bool = False
    untracked: bool = False
    conflicts: bool = False
    operation_in_progress: str | None = None
    changed_files: tuple[ChangedFile, ...] = ()
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class PlanEntry:
    repo: RepoState
    action: str
    reasons: tuple[str, ...] = ()

    @property
    def can_sync(self) -> bool:
        return self.action == "sync"


@dataclass(frozen=True)
class SyncOptions:
    root: Path
    branch: str | None
    message: str | None
    apply: bool = False
    repo_names: tuple[str, ...] = ()
    max_file_size_mb: int = 25
    jobs: int = 15
    git_timeout_seconds: float = 60.0
    progress: bool = False
    include_untracked: bool = True
    protected_paths: tuple[str, ...] = (
        ".env",
        "secrets/",
        "private/",
        "internal/",
        "_private/",
        "_internal/",
    )


@dataclass
class RepoSyncResult:
    name: str
    path: str
    action: str
    status: str
    old_head: str | None = None
    new_head: str | None = None
    commit: str | None = None
    reasons: list[str] = field(default_factory=list)
    error: str | None = None


@dataclass
class SyncRunResult:
    run_id: str
    root: Path
    message: str | None
    applied: bool
    repos: list[RepoSyncResult]
