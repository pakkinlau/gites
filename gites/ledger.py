from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .models import SyncRunResult


def ledger_dir(root: Path) -> Path:
    return root / ".gites" / "ledgers"


def append_run(result: SyncRunResult) -> Path:
    directory = ledger_dir(result.root)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{datetime.now(timezone.utc).strftime('%Y%m%d')}.jsonl"
    payload = asdict(result)
    payload["root"] = str(result.root)
    payload["timestamp"] = datetime.now(timezone.utc).isoformat()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
    return path


def list_runs(root: Path) -> list[dict]:
    runs: list[dict] = []
    directory = ledger_dir(root)
    if not directory.exists():
        return runs
    for path in sorted(directory.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    runs.append(json.loads(line))
    return runs


def find_run(root: Path, run_id: str) -> dict | None:
    for run in list_runs(root):
        if run.get("run_id") == run_id:
            return run
    return None
