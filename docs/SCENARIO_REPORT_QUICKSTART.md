# SCENARIO_REPORT_QUICKSTART

Use this quickstart when you need the shortest replayable path for governance-sandbox scenario imports and report generation.

## One-file rehearsal loop

Create a scenario file with:
- `scenario.name` or `title`
- `scenario.context` / `decision_context` / `summary`
- `inputs.proposal` / `proposal` / `proposal_text`
- stakeholder entries using `preset`, `group`, or `trait`

Example command:

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run \
  --scenario-file examples/scenario-report-bundle.yaml \
  --report-dir artifacts/delegate-ready
```

## Expected output

A single run should emit:
- one JSON artifact
- one Markdown artifact
- one HTML artifact

## Replay-ready check

The slice is healthy when the same scenario file can be rerun without editing flags and still preserves:
- scenario name/context
- stakeholder preset resolution
- report title or basename
- bundle artifact paths
