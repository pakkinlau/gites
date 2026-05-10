from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


APP_NAME = "gites"


def default_root() -> Path:
    return Path.cwd()


def user_config_dir() -> Path:
    override = os.environ.get("GITES_CONFIG_HOME")
    if override:
        return Path(override).expanduser()
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home:
        return Path(xdg_config_home).expanduser() / APP_NAME
    return Path.home() / ".config" / APP_NAME


def user_config_path() -> Path:
    return user_config_dir() / "config.json"


def default_user_config() -> dict[str, Any]:
    return {
        "version": 1,
        "active": None,
        "dirs": {},
        "defaults": {
            "branch": "main",
            "message_template": "chore: checkpoint {date}",
        },
    }


def load_user_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or user_config_path()
    if not config_path.exists():
        return default_user_config()
    with config_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"user config must be a JSON object: {config_path}")
    config = default_user_config()
    config.update(data)
    if not isinstance(config.get("dirs"), dict):
        raise ValueError("user config field 'dirs' must be an object")
    if not isinstance(config.get("defaults"), dict):
        raise ValueError("user config field 'defaults' must be an object")
    return config


def save_user_config(config: dict[str, Any], path: Path | None = None) -> Path:
    config_path = path or user_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return config_path


def add_dir(name: str, path: Path, branch: str = "main", make_active: bool = True) -> Path:
    config = load_user_config()
    resolved = path.expanduser().resolve()
    config["dirs"][name] = {
        "path": str(resolved),
        "branch": branch,
    }
    if make_active:
        config["active"] = name
    return save_user_config(config)


def remove_dir(name: str) -> Path:
    config = load_user_config()
    config["dirs"].pop(name, None)
    if config.get("active") == name:
        config["active"] = None
    return save_user_config(config)


def set_active_dir(name: str) -> Path:
    config = load_user_config()
    if name not in config["dirs"]:
        raise ValueError(f"unknown dir: {name}")
    config["active"] = name
    return save_user_config(config)


def active_dir_config() -> tuple[str, dict[str, Any]]:
    config = load_user_config()
    active = config.get("active")
    if not active:
        raise ValueError("no active dir. Run 'gites init' or 'gites use <name>' first")
    dirs = config.get("dirs", {})
    if active not in dirs:
        raise ValueError(f"active dir is missing from config: {active}")
    selected = dirs[active]
    if not isinstance(selected, dict) or not selected.get("path"):
        raise ValueError(f"active dir is invalid: {active}")
    return active, selected


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
