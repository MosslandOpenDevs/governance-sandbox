# governance-sandbox

Agent-based governance scenario rehearsal engine for testing proposals, stakeholder reactions, and decision risks before real-world execution.

> Rehearse governance decisions in a simulated stakeholder environment before you ship them to reality.

---

## The problem

Governance decisions often fail not because the proposal is invalid, but because stakeholders react in unexpected ways, communication breaks down, or second-order effects are ignored.

`governance-sandbox` is designed to help teams rehearse proposals before launch by simulating stakeholder perspectives, surfacing likely tensions, and generating a structured decision memo.

---

## Demo Preview

- Demo concept: scenario input → stakeholder simulation → decision memo
- Planned live demo: `docs/assets/examples/demo-link.md`
- Current MVP output: local CLI-generated governance rehearsal report

<table>
<tr>
<td><img src="./docs/assets/screenshot-1.svg" alt="Scenario input" width="100%"/></td>
<td><img src="./docs/assets/screenshot-2.svg" alt="Stakeholder simulation" width="100%"/></td>
<td><img src="./docs/assets/screenshot-3.svg" alt="Decision memo" width="100%"/></td>
</tr>
</table>

---

## 3-step how it works

### 1) Input a governance proposal
Provide a short proposal description, target decision context, and optional constraints.

### 2) Simulate stakeholder responses
The engine generates multiple stakeholder perspectives and predicts likely support, concern, or resistance patterns.

### 3) Produce a decision memo
The system outputs a structured memo with risks, tensions, recommended mitigations, and a go/no-go style summary.

---

## Sample scenario

Scenario files can also include an optional scenario name and decision context that appear in markdown/html reports.


**Scenario:**
A DAO plans to change treasury allocation from long-term ecosystem grants to short-term growth campaigns. Stakeholders include core contributors, token holders, external builders, and governance delegates.

**Expected questions:**
- Will short-term growth weaken long-term trust?
- Which stakeholders resist first?
- What messaging or safeguards reduce backlash?

---

## Quickstart

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run \
  --proposal "Shift 25% of treasury budget from grants to growth campaigns" \
  --stakeholders "core contributors,token holders,external builders,governance delegates"
```

Or generate the default report bundle in one step:

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run \
  --scenario-file examples/scenario.yaml \
  --report-dir artifacts/demo
```

Use the richer scenario/report fixture when you want one YAML file to drive proposal input, stakeholder presets, report naming, and a reusable JSON/Markdown/HTML artifact bundle:

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run \
  --scenario-file examples/scenario-report-bundle.yaml \
  --report-dir artifacts/delegate-ready
```

---

## Why this project exists

Most governance tooling focuses on voting, execution, or on-chain recordkeeping.
Much less attention is given to **pre-decision rehearsal**:

- What happens if this proposal is misunderstood?
- Which stakeholders align or oppose it first?
- Which mitigation language should appear before launch?
- What second-order narrative risks are visible early?

This project exists to fill that gap.

---

## Product direction

This repository is intended to become a long-lived public simulation layer for governance teams, DAOs, policy groups, and agent-native decision systems.

### Direction 1 — Decision support over prediction theater
We do not aim to "predict everything." We aim to improve the quality of governance decisions by making reactions and tradeoffs easier to inspect.

### Direction 2 — Scenario clarity over model complexity
A smaller, auditable system with explicit assumptions is more useful than a flashy black box.

### Direction 3 — Governance-native workflows
Outputs should resemble real decision artifacts:

- stakeholder map
- alignment/conflict matrix
- risk summary
- mitigation recommendations
- final decision memo

### Direction 4 — Demo-ready public repos
Every release should improve the public-repo surface:

- cleaner README
- stronger visual walkthroughs
- scenario examples
- reproducible commands
- evidence of practical use

### Direction 5 — Extensible domain packs
Long term, this engine can support multiple domain packs:

- DAO governance
- public sentiment rehearsal
- internal org decision rehearsal
- policy and communications scenarios

---

## MVP scope

Current MVP includes:

- proposal input
- stakeholder list input
- simple heuristic response simulation
- structured decision memo output

Near-term additions:

- scenario files
- richer stakeholder traits
- conflict graph export
- markdown/html report generation

Current CLI additions now include:

- optional scenario metadata (`name`, `context` / `decision_context`) loaded from scenario files and surfaced in reports
- `--scenario-file` for JSON/YAML proposal + stakeholder input
- nested scenario blocks (`scenario.name`, `scenario.context`, `inputs.proposal`, `inputs.stakeholders`) for reusable demo fixtures and UI handoff payloads
- scenario-file aliases for lightweight imports (`title` → scenario name, `decision`/`summary` → report context, `proposal_text`/`prompt` → proposal, `participants`/`actors` → stakeholders, stakeholder `group`/`trait` → preset)
- `--report-markdown` for a local decision memo report file
- `--report-html` for a lightweight visual report artifact
- `--report-json` for writing the structured output artifact to disk
- `--report-dir` for emitting a default report artifact bundle in one command
- scenario `tags` / `labels` for reusable demo fixtures and richer markdown/html report context
- optional scenario `report_title` / `report_heading` metadata for cleaner markdown/html memo headings, page titles, and demo handoff bundles
- nested `report.title` / `report.heading` and `report.tags` blocks for report-first scenario fixtures and UI handoff payloads
- scenario `description` as a lightweight context alias for report-oriented fixtures
- outcome snapshot summaries in JSON + markdown/html reports so stakeholder stance balance is visible at a glance
- `run --list-presets` for built-in stakeholder trait groups (`dao`, `delegates`, `contributors`, `investors`, `community`)

---

## Repository structure

```text
governance-sandbox/
├─ README.md
├─ pyproject.toml
├─ src/governance_sandbox/
│  ├─ __init__.py
│  ├─ engine.py
│  └─ cli.py
├─ docs/assets/
│  ├─ screenshot-1.svg
│  ├─ screenshot-2.svg
│  └─ screenshot-3.svg
└─ .github/workflows/ci.yml
```

---

## Roadmap

### Phase 1
- MVP simulation engine
- CLI workflow
- launch-page style README

### Phase 2
- scenario file support
- markdown/html report generation
- richer stakeholder trait presets

### Phase 3
- domain packs
- visual stakeholder graph
- benchmark scenarios and replay comparison

### Phase 4
- browser UI
- saved simulation runs
- team workflow integration

---

## License

MIT


## Scenario-driven report bundles

Scenario files can now steer report bundle naming through `report.basename`, which is useful when you want stable markdown/html/json artifact names per rehearsal.
Configured `report.basename` values are sanitized into a safe slug so punctuation or path-like separators do not leak into the generated bundle paths.

```yaml
scenario:
  name: Treasury signal rehearsal
report:
  title: Delegate-ready rehearsal memo
  basename: delegate-ready-rehearsal
inputs:
  proposal: Add milestone checkpoints before treasury growth experiments.
  stakeholders:
    - name: Delegate circle
      preset: delegates
```

Then run `gov-sandbox run --scenario-file scenario.yaml --report-dir artifacts/` to produce `delegate-ready-rehearsal.json`, `.md`, and `.html`.
If `report.basename` is omitted, `report.title` becomes the default bundle basename before the CLI falls back to generic `report.*` filenames.
