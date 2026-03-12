# Scenario report bundle quickstart

Use this when a governance rehearsal should start from one JSON/YAML scenario file and end as a report bundle.

1. Put the proposal text plus stakeholder presets in the scenario file.
2. Set `report.title` or `report.basename` so the generated bundle names stay predictable.
3. Run `gov-sandbox run --scenario-file scenario.yaml --report-dir artifacts/`.
4. Reopen the generated JSON, markdown, and HTML files together before sharing conclusions.

Prefer one stable scenario file plus one shared artifact bundle over ad-hoc flag combinations.
