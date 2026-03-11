# Scenario report metadata start

Use this note when you need the smallest proof that a scenario file drives a reusable report bundle with stable metadata.

## Fast path

1. Start from `examples/scenario-report-bundle.yaml` when you want one fixture to carry proposal, stakeholders, report title, and bundle naming.
2. Run `PYTHONPATH=src python3 -m governance_sandbox.cli run --scenario-file examples/scenario-report-bundle.yaml --report-dir artifacts/demo`.
3. Reopen `artifacts/demo/report.json`, `artifacts/demo/report.md`, and `artifacts/demo/report.html` together before widening the scenario or UI scope.

## What to verify

- The JSON artifact includes `report.generated_at`, `report.scenario_file`, and `report.artifacts`.
- Markdown and HTML outputs expose the same report metadata so reviewers can trace the scenario source without reopening the CLI command history.
- The default `report.*` alias files stay in sync with the configured basename output.
