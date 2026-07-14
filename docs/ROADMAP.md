# Roadmap and validation gate

This roadmap reflects an owner review (2026-07-14). The guiding decision: **do not add
features yet.** Park the project as Labs / Experimental, tell the truth about what it is
(a deterministic pre-mortem, not a simulation), and earn the right to keep going by proving
utility on a real proposal within 90 days.

## The 90-day gate

| By | Gate |
| --- | --- |
| 2026-08-13 | Alias freeze, truthful README, real CI, canonical schema drafted, named backup owner |
| 2026-09-12 | Applied to at least one low-risk real Agora proposal; two human reviewers; before/after diff recorded |
| **2026-10-12** | Retrospective vs. the actual discussion/vote → **graduate, keep in Labs, or archive** |

If there is no real usage by the review date, or output stays fixed regardless of input,
archiving is the honest outcome.

## Done (this pass)

- Truth Reset of positioning (README + package description).
- CI turned into a real gate: ruff + mypy + pytest + build + link check on Python 3.10–3.13.
- Python 3.10 compatibility restored; leaked absolute path removed; broken doc link fixed;
  dead tests removed; lint/type errors cleared.
- OSS ops files added (`SECURITY.md`, `CONTRIBUTING.md`, `CODEOWNERS`, `CHANGELOG.md`).

## P0 — repository normalization (near-term)

- Set the GitHub repository description/topics to match the README ("Labs / Experimental",
  "deterministic governance proposal pre-mortem"). *(Repo setting — not in this codebase.)*
- Enable branch protection on `main` with one required review. *(Repo setting.)*
- Name a primary and backup maintainer in `.github/CODEOWNERS` (currently a placeholder).
- Tag the pre-cleanup state as `legacy-v0.1.0` for reference. *(No history rewrite needed.)*

## P1 — auditable preflight (not a predictor)

Deferred; large. Turn the deterministic renderer into an **auditable proposal preflight**:

- **Canonical schema + legacy adapter.** Define one schema (`schemaVersion`, `proposal.{id,
  version, decisionClass, effectiveAt, snapshotBlock, title, body}`, `assumptions`,
  `provenance.{sourceUri, inputSha256}`) validated with Pydantic/JSON Schema; reject unknown
  fields by default; convert the ~200 existing field aliases only inside a `LegacyV0Adapter`
  that emits deprecation warnings. This replaces the alias sprawl and the README-string tests.
- **Structured checks** over a proposal: responsible party & execution authority, budget cap
  & funding source, success metric & measurement time, termination/rollback conditions,
  `decisionClass`/`effectiveAt`, missing stakeholders, disclosure plan, and body-vs-execution
  mismatch.
- **Honest output** — replace the canned `Proceed with revision` verdict with
  `finding` / `severity` / `evidence` / `assumption` / `unknown` / `suggested_change` records.
- **Input security** before any web mode (see [SECURITY.md](../SECURITY.md)): reject
  out-of-workspace, absolute, `..`, and symlinked paths; record relative paths + input hash
  (never machine-absolute paths); bound input size and run time.
- **Doc/test consolidation**: merge the ~100 five-line micro-notes; delete presence-only
  README tests in favor of behavior tests.

## P2 — real simulation (only after validation)

Only after P1 is validated should the "simulation" language return. Minimum bar to call it a
simulation: explicit agent state and behavior rules, a proposal lifecycle/state machine,
delegation and voting-power snapshots, multiple time steps, seeded RNG, Monte Carlo runs with
distributions (not a single answer), parameter sweeps/sensitivity analysis, historical replay
+ holdout backtests, and a run manifest (model/schema/git SHA/input hash). Attack regressions
should cover human/governance attacks (apathy, whale activation, bribery, coalitions, spam,
misinformation, malicious calldata), not just code bugs.

### Reference systems to learn from

- ABM structure: **Mesa**; experiment running & Monte Carlo: **cadCAD**.
- Governance semantics: **OpenZeppelin Governor** (quorum/threshold/timelock) via a generic
  adapter — modeled separately from an off-chain, EIP-712 / snapshot-weighted Agora adapter.
- Execution safety: **Uniswap Governance Seatbelt** (fork execution / state diff).
- LLM social simulation: **DeepMind Concordia** (kept in an experimental mode).
- Interop/provenance: **ERC-4824** (DAO import) and **EIP-712** (signed artifacts).

## Boundaries (role within the wider system)

`governance-sandbox` is a non-authoritative Labs pre-mortem aid. It must not change any vote,
tally, decision class, or effect; must not gate participation or build personas from identity
data; and its output must be labeled a *heuristic authoring aid — not voter sentiment*. It
stays a separate repo (no top-level pin, no rewards/token gating) until the gate is cleared.
