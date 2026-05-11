from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gites.cli import main
from gites.config import load_user_config
from gites.models import ChangedFile, RepoSyncResult, SyncOptions, SyncRunResult
from gites.output import render_run
from gites.planner import build_plan
from gites.sync import run_sync


def git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args),
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    return result.stdout.strip()


class PlannerSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def create_repo(self, name: str = "repo") -> Path:
        remote = self.root / f"{name}.git"
        repo = self.root / name
        git(self.root, "init", "--bare", remote.name)
        git(self.root, "clone", str(remote), repo.name)
        git(repo, "config", "user.email", "test@example.com")
        git(repo, "config", "user.name", "Test User")
        (repo / "README.md").write_text("# Test\n", encoding="utf-8")
        git(repo, "add", "README.md")
        git(repo, "commit", "-m", "initial commit")
        git(repo, "branch", "-M", "main")
        git(repo, "push", "-u", "origin", "main")
        return repo

    def test_plan_marks_clean_repo_noop(self) -> None:
        self.create_repo()
        plan = build_plan(SyncOptions(root=self.root, branch="main", message=None))
        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0].action, "noop")

    def test_sync_commits_pushes_and_writes_ledger(self) -> None:
        repo = self.create_repo()
        (repo / "file.txt").write_text("changed\n", encoding="utf-8")

        result = run_sync(
            SyncOptions(
                root=self.root,
                branch="main",
                message="chore: deterministic checkpoint",
                apply=True,
            )
        )

        self.assertEqual(result.repos[0].status, "pushed")
        self.assertIn("chore: deterministic checkpoint", git(repo, "log", "-1", "--pretty=%B"))
        self.assertTrue((self.root / ".gites" / "ledgers").exists())

    def test_sync_can_generate_checkpoint_commit_message(self) -> None:
        repo = self.create_repo()
        (repo / "file.txt").write_text("changed\n", encoding="utf-8")

        result = run_sync(
            SyncOptions(
                root=self.root,
                branch="main",
                message=None,
                apply=True,
                auto_message=True,
                instance_name="local",
            )
        )

        self.assertEqual(result.repos[0].status, "pushed")
        message = git(repo, "log", "-1", "--pretty=%B")
        self.assertIn("chore(gites): checkpoint 1 file", message)
        self.assertIn("Gites checkpoint", message)
        self.assertIn("Instance: local", message)
        self.assertIn("Repo: repo", message)
        self.assertIn("Changes: 1 file(s): 1 untracked", message)

    def test_sync_refuses_protected_path(self) -> None:
        repo = self.create_repo()
        (repo / ".env").write_text("TOKEN=secret\n", encoding="utf-8")

        result = run_sync(
            SyncOptions(
                root=self.root,
                branch="main",
                message="chore: deterministic checkpoint",
                apply=True,
            )
        )

        self.assertEqual(result.repos[0].status, "refused")
        self.assertIn("protected path changed: .env", result.repos[0].reasons)

    def test_plan_refuses_wrong_branch(self) -> None:
        repo = self.create_repo()
        git(repo, "checkout", "-b", "feature/test")
        (repo / "file.txt").write_text("changed\n", encoding="utf-8")

        plan = build_plan(SyncOptions(root=self.root, branch="main", message=None))

        self.assertEqual(plan[0].action, "refuse")
        self.assertIn("wrong branch: expected main, found feature/test", plan[0].reasons)

    def test_plan_refuses_missing_upstream(self) -> None:
        repo = self.create_repo()
        git(repo, "checkout", "--orphan", "local-only")
        git(repo, "rm", "-rf", ".")
        (repo / "local.txt").write_text("local only\n", encoding="utf-8")
        git(repo, "add", "local.txt")
        git(repo, "commit", "-m", "local only")

        plan = build_plan(SyncOptions(root=self.root, branch="local-only", message=None))

        self.assertEqual(plan[0].action, "refuse")
        self.assertIn("missing upstream branch", plan[0].reasons)

    def test_apply_requires_message(self) -> None:
        self.create_repo()

        with self.assertRaises(ValueError):
            run_sync(SyncOptions(root=self.root, branch="main", message=None, apply=True))

    def test_simple_init_use_and_push_preview(self) -> None:
        self.create_repo()
        config_home = self.root / "config-home"

        with patch.dict("os.environ", {"GITES_CONFIG_HOME": str(config_home)}):
            self.assertEqual(main(["init", str(self.root), "--name", "local"]), 0)
            config = load_user_config()
            self.assertEqual(config["active"], "local")
            self.assertEqual(config["dirs"]["local"]["path"], str(self.root))

            self.assertEqual(main(["dirs"]), 0)
            self.assertEqual(main(["where"]), 0)
            self.assertEqual(main(["where", "local"]), 0)
            self.assertEqual(main(["view", "--no-progress"]), 0)
            self.assertEqual(main(["view", "local", "--jobs", "2", "--timeout", "5"]), 0)
            self.assertEqual(main(["view", "local", "--untracked", "--no-progress"]), 0)
            self.assertEqual(main(["status", "local", "--no-progress"]), 0)
            self.assertEqual(main(["local", "--no-progress"]), 0)
            self.assertEqual(main(["push", "--no-progress"]), 0)
            self.assertEqual(main(["push", "local", "--jobs", "2", "--timeout", "5"]), 0)

    def test_render_run_summarizes_clean_sync_and_refused_repos(self) -> None:
        result = SyncRunResult(
            run_id="run-1",
            root=self.root,
            message=None,
            applied=False,
            repos=[
                RepoSyncResult(
                    name="clean-repo",
                    path=str(self.root / "clean-repo"),
                    action="noop",
                    status="dry-run",
                    old_head="a" * 40,
                    new_head="a" * 40,
                    reasons=["working tree clean"],
                ),
                RepoSyncResult(
                    name="changed-repo",
                    path=str(self.root / "changed-repo"),
                    action="sync",
                    status="dry-run",
                    old_head="b" * 40,
                    new_head="b" * 40,
                    commit_message="chore(gites): checkpoint 3 files\n\nBody",
                    changed_files=[
                        ChangedFile(path="file.txt", status=" M"),
                        ChangedFile(path="old.txt", status=" D"),
                        ChangedFile(path="new.txt", status="??"),
                    ],
                ),
                RepoSyncResult(
                    name="local-only",
                    path=str(self.root / "local-only"),
                    action="refuse",
                    status="dry-run",
                    old_head="c" * 40,
                    new_head="c" * 40,
                    reasons=["missing origin remote"],
                ),
            ],
        )

        output = render_run(result)

        self.assertIn("summary: clean=1, would_sync=1, refused=1, failed=0", output)
        self.assertIn("clean: 1 repo(s) had no changes.", output)
        self.assertIn("would sync:", output)
        self.assertIn(
            "- changed-repo: 3 file(s): 1 modified, 1 deleted, 1 untracked; "
            "head bbbbbbbbbbbb; commit: chore(gites): checkpoint 3 files",
            output,
        )
        self.assertIn("refused:", output)
        self.assertIn("- local-only: no file changes; missing origin remote", output)


if __name__ == "__main__":
    unittest.main()
