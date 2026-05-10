from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def default_root() -> Path:
    return Path.cwd()


def load_manifest(path: Path) -> dict[str, Any]:
    with path.expanduser().open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object")
    return data


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = load_manifest(path)
    except Exception as exc:
        return [str(exc)]

    roots = data.get("root_directories")
    if roots is not None and not isinstance(roots, dict):
        errors.append("root_directories must be an object")

    repositories = data.get("repositories")
    if repositories is not None:
        if not isinstance(repositories, list):
            errors.append("repositories must be a list")
        else:
            for index, repo in enumerate(repositories):
                if not isinstance(repo, dict):
                    errors.append(f"repositories[{index}] must be an object")
                    continue
                if "name" not in repo:
                    errors.append(f"repositories[{index}] missing name")
                if "remote_url" not in repo:
                    errors.append(f"repositories[{index}] missing remote_url")

    families = data.get("families")
    if families is not None:
        if not isinstance(families, dict):
            errors.append("families must be an object")
        else:
            for name, family in families.items():
                if not isinstance(family, dict):
                    errors.append(f"families.{name} must be an object")
                    continue
                repos = family.get("repos", [])
                if not isinstance(repos, list) or not all(isinstance(repo, str) for repo in repos):
                    errors.append(f"families.{name}.repos must be a list of strings")
                branch = family.get("branch")
                if branch is not None and not isinstance(branch, str):
                    errors.append(f"families.{name}.branch must be a string")
                template = family.get("commit_message_template")
                if template is not None and not isinstance(template, str):
                    errors.append(f"families.{name}.commit_message_template must be a string")

    return errors


def root_from_manifest(path: Path) -> Path:
    data = load_manifest(path)
    roots = data.get("root_directories", {})
    if isinstance(roots, dict):
        if os.name == "nt" and roots.get("windows"):
            return Path(roots["windows"]).expanduser()
        if roots.get("linux"):
            return Path(roots["linux"]).expanduser()
    raise ValueError(f"manifest does not define a root directory for this OS: {path}")


def family_from_manifest(path: Path, family: str) -> dict[str, Any]:
    data = load_manifest(path)
    families = data.get("families", {})
    if not isinstance(families, dict) or family not in families:
        raise ValueError(f"manifest does not define family: {family}")
    selected = families[family]
    if not isinstance(selected, dict):
        raise ValueError(f"family must be an object: {family}")
    return selected
