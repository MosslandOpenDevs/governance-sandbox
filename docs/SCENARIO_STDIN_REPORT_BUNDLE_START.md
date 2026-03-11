# Scenario stdin report bundle start

Use this when a shell pipeline or browser handoff already has one JSON/YAML scenario payload in memory and you want the quickest path to a reusable report bundle.

Keep the first replay small:

1. pipe one scenario into `--scenario-file -`,
2. write one report bundle with `--report-dir`,
3. reopen the generated `report.json`, `report.md`, and `report.html` artifacts from the same directory.

This keeps stdin-driven scenario import aligned with the current priority lane: scenario-file input first, then markdown/html/json report output.
