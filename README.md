# Gites

Gites is a local-first command line tool for deterministic multi-repo checkpointing.

It is designed for a root directory that contains many Git repositories. Gites previews repo state, refuses unsafe repositories, commits with an explicit deterministic message, pushes safely, and records each run in a local ignored ledger.

## Install

```bash
pip install gites
```

For local development:

```bash
pip install -e .
```

## Core Workflow

Preview repositories under a root directory:

```bash
gites plan --root ~/All_github_repo --branch main
```

Dry-run a checkpoint:

```bash
gites sync --root ~/All_github_repo --branch main --dry-run
```

Apply a checkpoint with an explicit commit message:

```bash
gites sync --root ~/All_github_repo \
  --branch main \
  --apply \
  --message "chore: checkpoint repo family 2026-05-10"
```

Read local run ledgers:

```bash
gites ledger list --root ~/All_github_repo
gites ledger show RUN_ID --root ~/All_github_repo
```

Ledgers are written under `.gites/ledgers/` inside the selected root. That directory is intentionally ignored by Git.

## Safety Rules

`gites sync --apply` refuses a repository when it detects:

- detached `HEAD`
- merge, rebase, cherry-pick, or revert in progress
- unresolved conflicts
- wrong branch
- missing `origin`
- missing upstream branch
- branch behind upstream
- branch diverged from upstream
- protected path changes such as `.env`, `secrets/`, `private/`, or `internal/`
- changed files larger than the configured size limit
- missing commit message in apply mode

Gites never force-pushes by default.

## Manifest Files

Real manifests should stay local and ignored, for example `my_gites.json` or `gites.local.json`.

Create a local template:

```bash
gites config init my_gites.json
```

Validate a manifest:

```bash
gites config validate my_gites.json
```

Use a family from a manifest:

```bash
gites sync --manifest my_gites.json \
  --family default \
  --dry-run
```

A sanitized public example is available at `examples/example.gites.json`.

## Development

Run tests:

```bash
python -m unittest discover -v
```

## Privacy

Do not commit real manifests, ledgers, credentials, ChatGPT exports, private notes, or local editor state. The repository `.gitignore` blocks the intended local-only paths.
