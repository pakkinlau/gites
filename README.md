# Gites

Gites is a safe multi-repo Git CLI for developers who manage many related
repositories outside a monorepo. It gives a repo family one short name, shows a
single table of branch/dirty/ahead/behind state, and can commit and push the
eligible repositories with one deterministic checkpoint command.

Use it when you have a directory full of Git repos and need a practical way to
inspect, checkpoint, and push them without hand-running `git status`, `git
commit`, and `git push` in every folder.

The interface is intentionally context-like: register a directory as a named
instance, list the instances, select the active one, then run short commands
against it. If you are used to Docker contexts or named environments, `gites`
applies that same small mental model to repo families.

## Why Gites

- Define a directory of repositories as a named instance, then select it from a
  list.
- One command shows a table for every repo in a saved root.
- One command previews or applies a bulk Git checkpoint.
- Unsafe repos are refused instead of force-pushed or silently modified.
- Large repo roots are inspected in parallel with timeouts.
- Local run ledgers stay ignored and private.
- Works well for WSL users who keep large Git repo families on native Linux
  paths instead of slow `/mnt/c/...` checkouts.

Typical use cases include multi-repo project families, research/code archives,
documentation surface repos, generated repo sets, and teams that want some of
the operational convenience of a monorepo without merging repositories together.

The name carries the idea: Git plus easy, and also `gites` as in small houses
or lodgings. A `gites` root is meant to feel like a modest home for related
repositories: each repo keeps its own room, while the front door gives you one
place to check what changed and send the whole house home safely.

![A small stone house representing a gites root for related repositories.](docs/assets/gites-house.jpg)

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
cd ~/repos/work
gites init --name work --branch main
```

Or register an explicit path:

```bash
gites init ~/repos/work --name work --branch main
```

List saved roots:

```bash
gites dirs
```

Switch active root:

```bash
gites use work
```

Show the current repo-state table for a saved root:

```bash
gites view
gites view work
gites status work
gites work
```

Viewing a named instance prints the selected directory, optional progress, and
then a single table for the repositories inside that instance:

```text
$ gites view work
dir: work  root: ~/repos/work  branch: main
untracked scan: skipped (use --untracked for full scan)
Inspecting 4 repos with 15 worker(s)...
[1/4] api-service -> noop
[2/4] web-app -> sync
[3/4] docs-site -> noop
[4/4] local-tooling -> refuse

repo           branch  ahead  behind  dirty  untracked  action  reason
-------------  ------  -----  ------  -----  ---------  ------  --------------------------------
api-service    main    0      0       no     no         noop    working tree clean
web-app        main    1      0       yes    no         sync
docs-site      main    0      0       no     no         noop    working tree clean
local-tooling  main    0      0       no     no         refuse  missing origin remote
```

`view`, `status`, and object shortcuts inspect repositories in parallel, show
progress by default, use 15 workers, apply a 60 second per-Git-command timeout,
and skip expensive untracked-file enumeration unless requested:

```bash
gites view work
gites view work --untracked
gites view work --no-progress
gites view work --jobs 30 --timeout 120
```

Preview what would be pushed:

```bash
gites push
gites push work
```

Apply with a deterministic commit message:

```bash
gites push work -m "chore: checkpoint repo family 2026-05-11"
```

The saved directory config lives outside the repo at `~/.config/gites/config.json`.

## Table Output

The status table is meant to be the main decision surface:

```text
repo                  branch  ahead  behind  dirty  untracked  action  reason
--------------------  ------  -----  ------  -----  ---------  ------  ------------------
api-service           main    0      0       no     no         noop    working tree clean
web-app               main    1      0       yes    no         sync
local-tooling         main    0      0       no     no         refuse  missing origin remote
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
~/repos/work
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
gites plan --root ~/repos/work --branch main
```

Dry-run a checkpoint:

```bash
gites sync --root ~/repos/work --branch main --dry-run
```

Apply a checkpoint with an explicit commit message:

```bash
gites sync --root ~/repos/work \
  --branch main \
  --apply \
  --message "chore: checkpoint repo family 2026-05-10"
```

Read local run ledgers:

```bash
gites ledger list --root ~/repos/work
gites ledger show RUN_ID --root ~/repos/work
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
