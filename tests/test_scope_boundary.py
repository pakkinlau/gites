from __future__ import annotations

import unittest
from pathlib import Path

from gites.cli import build_parser


class ScopeBoundaryTests(unittest.TestCase):
    def test_public_cli_stays_generic(self) -> None:
        parser = build_parser()
        subparser_action = next(
            action for action in parser._actions if getattr(action, "choices", None)
        )

        self.assertEqual(
            set(subparser_action.choices),
            {
                "init",
                "dirs",
                "use",
                "where",
                "push",
                "view",
                "status",
                "plan",
                "sync",
                "ledger",
                "config",
            },
        )

    def test_no_project_specific_runtime_modules(self) -> None:
        package_files = {path.name for path in (Path(__file__).parents[1] / "gites").glob("*.py")}

        self.assertEqual(
            package_files,
            {
                "__init__.py",
                "cli.py",
                "config.py",
                "discovery.py",
                "git_backend.py",
                "ledger.py",
                "models.py",
                "output.py",
                "planner.py",
                "sync.py",
            },
        )


if __name__ == "__main__":
    unittest.main()
