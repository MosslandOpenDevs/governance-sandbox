# Scenario report output `files` mapping

When one JSON/YAML scenario fixture already owns the report bundle wiring, keep the JSON, Markdown, and HTML targets together under `report.outputs.files`.

Use this when you want one reviewable `files.json` / `files.markdown` / `files.html` block instead of repeating sibling output-path keys.

That keeps scenario-file input support and markdown/html report generation moving together in one visible bundle contract.
