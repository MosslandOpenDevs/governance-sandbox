# SCENARIO_REPORT_START

Use one scenario file plus `--report-dir` when you want the smallest reproducible governance rehearsal bundle.

Quick replay:

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run \
  --scenario-file examples/scenario-report-bundle.yaml \
  --report-dir artifacts/demo
```

Expected bundle:
- one JSON result artifact
- one Markdown memo
- one HTML report
- matching default `report.*` aliases inside the report directory when the bundle uses a custom basename

Use this flow before widening into web-demo work so the proposal input, preset choice, and report output stay reproducible.
