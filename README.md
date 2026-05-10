# Gites

Gites is a local-first command line tool for deterministic multi-repo checkpointing.

It is designed for a root directory that contains many Git repositories. Gites previews repo state, refuses unsafe repositories, commits with an explicit deterministic message, pushes safely, and records each run in a local ignored ledger.

## Install

For regular CLI use, `pipx` is recommended:

```bash
pipx install gites
pipx upgrade gites --pip-args="--no-cache-dir"
```

`pip` also works:

```bash
pip install gites
```

For local development:

```bash
pip install -e .
```

## Simple Workflow

The normal workflow is to register a repo root once, give it a short name, and
then operate on that named object.

Register the current directory as a repo root:

```bash
cd ~/repos/All_hl_repo
gites init --name hl --branch main
```

Or register an explicit path:

```bash
gites init ~/repos/All_hl_repo --name hl --branch main
```

List saved roots:

```bash
gites dirs
```

Switch active root:

```bash
gites use hl
```

Show the current repo-state table for a saved root:

```bash
gites view
gites view hl
gites status hl
gites hl
```

`view`, `status`, and object shortcuts inspect repositories in parallel, show
progress by default, use 15 workers, apply a 60 second per-Git-command timeout,
and skip expensive untracked-file enumeration unless requested:

```bash
gites view hl
gites view hl --untracked
gites view hl --no-progress
gites view hl --jobs 30 --timeout 120
```

Preview what would be pushed:

```bash
gites push
gites push hl
```

Apply with a deterministic commit message:

```bash
gites push hl -m "chore: checkpoint repo family 2026-05-11"
```

The saved directory config lives outside the repo at `~/.config/gites/config.json`.

## Table Output

The status table is meant to be the main decision surface:

```text
repo                  branch  ahead  behind  dirty  untracked  action  reason
--------------------  ------  -----  ------  -----  ---------  ------  ------------------
archive-example       main    0      0       no     no         noop    working tree clean
surface-example       main    1      0       yes    no         sync
local-only-example    main    0      0       no     no         refuse  missing origin remote
```

Actions:

- `noop`: clean and already aligned with upstream
- `sync`: eligible for commit and push
- `refuse`: not safe to modify automatically; read the reason column

`gites` refuses local-only repositories because it cannot safely push them until
they have an `origin` remote and an upstream branch.

## WSL Guidance

For large repo roots on WSL, prefer native Linux paths such as:

```bash
~/repos/All_hl_repo
```

Avoid using `/mnt/c/...` as the active root for very large repositories.
Windows-mounted paths can make `git status` and `git commit` slow because Git
must perform many metadata checks through the WSL-to-Windows filesystem bridge.
The same repo can be much faster when cloned or moved under the native WSL
filesystem.

## Explicit Workflow

The lower-level `plan` and `sync` commands remain available for scripts and
one-off roots. Most interactive use should prefer `view` and `push`.

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
