# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project aims to follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Truth Reset of positioning.** README and package description now describe the tool
  honestly as a *deterministic governance-proposal pre-mortem (Labs / Experimental)*
  rather than an agent-based simulation or a predictor of stakeholder reactions. Added a
  "What this is — and what it is not" section and a `reviewAt: 2026-10-12` graduation gate.
- Rewrote the README into a concise product document; the large scenario/report field
  alias catalog is preserved but collapsed into a single reference section.
- Replaced the CI workflow (previously a single CLI smoke command) with a real quality
  gate: lint (ruff), type check (mypy), tests (pytest), packaging build, and a link check,
  across Python 3.10–3.13, with least-privilege `permissions`.

### Added
- `governance_sandbox.__main__` so `python -m governance_sandbox` works.
- `scripts/check_links.py` offline relative-link checker.
- `SECURITY.md`, `CONTRIBUTING.md`, `CODEOWNERS`, this changelog, and `docs/ROADMAP.md`.
- Structured output now also exposes top-level `scenario_file` and `report_paths`, plus
  `scenario.proposal`.
- Tooling config in `pyproject.toml` (`[project.optional-dependencies].dev`, ruff, mypy).

### Fixed
- Restored Python 3.10 compatibility (declared floor): use `datetime.timezone.utc` instead
  of `datetime.UTC` (3.11+).
- Removed a leaked absolute filesystem path (`/home/.../.openclaw/...`) from committed
  example report artifacts.
- Fixed a broken README doc link and a self-contradictory `report_basename` test; removed
  ~120 lines of dead, never-executed tests in `tests/test_cli.py`.
- Resolved all `ruff` lint findings and `mypy` type errors in the package.

## [0.1.0]
- Initial MVP: proposal + stakeholder input, deterministic stakeholder heuristics, and
  JSON/Markdown/HTML report bundle generation from CLI flags or a scenario file.
