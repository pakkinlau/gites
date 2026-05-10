from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from .config import default_root, family_from_manifest, load_manifest, root_from_manifest, validate_manifest
from .ledger import find_run, list_runs
from .models import SyncOptions
from .output import render_plan, render_run
from .planner import build_plan
from .sync import run_sync


def _resolve_root(args: argparse.Namespace) -> Path:
    if getattr(args, "root", None):
        return Path(args.root).expanduser().resolve()
    if getattr(args, "manifest", None):
        return root_from_manifest(Path(args.manifest)).resolve()
    return default_root().resolve()


def _options_from_args(args: argparse.Namespace, apply: bool = False) -> SyncOptions:
    branch = getattr(args, "branch", None)
    message = getattr(args, "message", None)
    repo_names = tuple(getattr(args, "repo", None) or ())
    cli_max_file_size_mb = getattr(args, "max_file_size_mb", None)
    max_file_size_mb = cli_max_file_size_mb
    protected_paths = (
        ".env",
        "secrets/",
        "private/",
        "internal/",
        "_private/",
        "_internal/",
    )

    if getattr(args, "manifest", None):
        manifest_data = load_manifest(Path(args.manifest))
        safety = manifest_data.get("safety", {})
        if isinstance(safety, dict):
            max_file_size_mb = int(safety.get("max_file_size_mb", max_file_size_mb or 25))
            configured_protected = safety.get("protected_paths")
            if isinstance(configured_protected, list) and all(isinstance(path, str) for path in configured_protected):
                protected_paths = tuple(configured_protected)
    if cli_max_file_size_mb is not None:
        max_file_size_mb = cli_max_file_size_mb

    if getattr(args, "manifest", None) and getattr(args, "family", None):
        family_data = family_from_manifest(Path(args.manifest), args.family)
        if not branch:
            branch = family_data.get("branch")
        if not repo_names:
            repo_names = tuple(family_data.get("repos", ()))
        if not message:
            template = family_data.get("commit_message_template")
            if template:
                message = template.format(family=args.family, date=date.today().isoformat())

    return SyncOptions(
        root=_resolve_root(args),
        branch=branch,
        message=message,
        apply=apply,
        repo_names=repo_names,
        max_file_size_mb=max_file_size_mb or 25,
        protected_paths=protected_paths,
    )


def cli_plan(args: argparse.Namespace) -> int:
    entries = build_plan(_options_from_args(args))
    print(render_plan(entries))
    return 0


def cli_sync(args: argparse.Namespace) -> int:
    apply = bool(args.apply)
    result = run_sync(_options_from_args(args, apply=apply))
    print(render_run(result))
    if any(repo.status in {"failed", "refused"} for repo in result.repos):
        return 1
    return 0


def cli_ledger_list(args: argparse.Namespace) -> int:
    root = _resolve_root(args)
    runs = list_runs(root)
    if not runs:
        print("No ledger runs found.")
        return 0
    for run in runs:
        print(
            f"{run.get('run_id')}  "
            f"applied={run.get('applied')}  "
            f"repos={len(run.get('repos', []))}  "
            f"timestamp={run.get('timestamp', '-')}"
        )
    return 0


def cli_ledger_show(args: argparse.Namespace) -> int:
    root = _resolve_root(args)
    run = find_run(root, args.run_id)
    if not run:
        print(f"Run not found: {args.run_id}")
        return 1
    print(json.dumps(run, indent=2, sort_keys=True))
    return 0


def cli_config_validate(args: argparse.Namespace) -> int:
    errors = validate_manifest(Path(args.manifest))
    if errors:
        print("Manifest is invalid:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Manifest is valid.")
    return 0


def cli_config_init(args: argparse.Namespace) -> int:
    path = Path(args.manifest)
    if path.exists() and not args.force:
        print(f"Refusing to overwrite existing manifest: {path}")
        return 1
    payload = {
        "version": 1,
        "root_directories": {
            "linux": str(Path.cwd()),
            "windows": "C:\\Users\\you\\Documents\\All_github_repo",
        },
        "families": {
            "default": {
                "branch": "main",
                "repos": [],
                "commit_message_template": "chore({family}): checkpoint {date}",
            }
        },
        "safety": {
            "max_file_size_mb": 25,
            "protected_paths": [".env", "secrets/", "private/", "internal/"],
        },
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote manifest template: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic local multi-repo checkpointing")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="Inspect repositories without changing them")
    _add_repo_selection_args(plan)
    _add_safety_args(plan)
    plan.set_defaults(func=cli_plan)

    sync = subparsers.add_parser("sync", help="Dry-run or apply a safe multi-repo checkpoint")
    _add_repo_selection_args(sync)
    _add_safety_args(sync)
    mode = sync.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview only. This is the default.")
    mode.add_argument("--apply", action="store_true", help="Commit and push allowed repositories.")
    sync.add_argument("-m", "--message", help="Deterministic commit message. Required with --apply.")
    sync.set_defaults(func=cli_sync)

    ledger = subparsers.add_parser("ledger", help="Read local ignored run ledgers")
    ledger_subparsers = ledger.add_subparsers(dest="ledger_command", required=True)
    ledger_list = ledger_subparsers.add_parser("list", help="List recorded runs")
    _add_repo_selection_args(ledger_list)
    ledger_list.set_defaults(func=cli_ledger_list)
    ledger_show = ledger_subparsers.add_parser("show", help="Show one recorded run")
    _add_repo_selection_args(ledger_show)
    ledger_show.add_argument("run_id")
    ledger_show.set_defaults(func=cli_ledger_show)

    config = subparsers.add_parser("config", help="Manifest utilities")
    config_subparsers = config.add_subparsers(dest="config_command", required=True)
    validate = config_subparsers.add_parser("validate", help="Validate a gites JSON manifest")
    validate.add_argument("manifest")
    validate.set_defaults(func=cli_config_validate)
    init = config_subparsers.add_parser("init", help="Write a local manifest template")
    init.add_argument("manifest")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cli_config_init)

    return parser


def _add_repo_selection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", help="Directory containing child Git repositories")
    parser.add_argument("--manifest", help="JSON manifest with root_directories")
    parser.add_argument("--family", help="Family name from the manifest")
    parser.add_argument("--repo", action="append", help="Only include this child repo name. Can be repeated.")
    parser.add_argument("--branch", help="Required branch name for sync eligibility")


def _add_safety_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--max-file-size-mb", type=int, help="Refuse changed files larger than this")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
