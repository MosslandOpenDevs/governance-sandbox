# Scenario report artifact bundle start

Use one scenario file plus one `--report-dir` destination as the default proof loop.

1. Start from `examples/scenario-report-bundle.yaml` when you want JSON, Markdown, and HTML artifacts together.
2. Run `PYTHONPATH=src python3 -m governance_sandbox.cli run --scenario-file examples/scenario-report-bundle.yaml --report-dir artifacts/demo`.
3. Confirm `report.json`, `report.md`, and `report.html` exist (plus the named bundle when the scenario sets a custom basename).
4. Share the Markdown or HTML report path in handoff notes so reviewers can inspect the same scenario replay.
