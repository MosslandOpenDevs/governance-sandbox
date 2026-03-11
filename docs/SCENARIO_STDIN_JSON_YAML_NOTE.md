# Scenario stdin JSON/YAML note

`gov-sandbox run --scenario-file -` accepts stdin so other tools can pipe a JSON or YAML scenario directly into the simulator.

Minimal replay flow:

1. Pipe one JSON or YAML scenario into stdin.
2. Run `gov-sandbox run --scenario-file - --report-dir <dir>`.
3. Confirm the output JSON plus the generated markdown and HTML reports.
4. Keep the same scenario payload for browser-form or demo work so replay stays deterministic.

This supports scenario-file-first workflows without forcing a temporary fixture file.
