# Contributing

Thanks for your interest. `governance-sandbox` is **Labs / Experimental** — see the
[README](README.md) for what it is (a deterministic governance-proposal pre-mortem) and
what it is not (a simulation or a predictor). Please read [docs/ROADMAP.md](docs/ROADMAP.md)
before proposing substantial changes; the near-term direction is consolidation and
validation, not new surface area.

## Development setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Checks (run before opening a PR)

The CI runs the same gates on Python 3.10–3.13:

```bash
ruff check .          # lint
mypy                  # type check (src)
pytest -q             # tests
python -m build       # packaging
python scripts/check_links.py   # relative links in README/docs resolve
```

`PYTHONPATH=src` is set for local runs without an editable install.

## Contribution guidelines

- **Alias freeze.** Do not add new scenario-file field aliases or wrapper keys. The
  existing alias sprawl is being consolidated behind a single canonical schema plus a
  legacy adapter (see the roadmap). New behavior should target the canonical schema.
- **Keep positioning honest.** Don't describe the tool as a simulation, prediction, or
  authoritative analysis in code, docs, or output.
- **Prefer consolidation.** Favor merging/removing redundant micro-notes and tests over
  adding new ones. New tests should assert behavior, not merely the presence of a string
  in `README.md`.
- **Types and lint must pass.** New code in `src/` should be mypy-clean.

## Pull requests

- Keep PRs focused and describe the behavior change.
- One maintainer approval is required before merge; `main` should be protected.
- Update [CHANGELOG.md](CHANGELOG.md) under **Unreleased** for user-visible changes.
