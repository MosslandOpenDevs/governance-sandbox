# Scenario report downloads alias note

When a scenario fixture is written for a first web demo or result-card handoff, `report.outputs.downloads` can carry the same JSON/Markdown/HTML file paths as `report.outputs.files` without reshaping the payload first.

Keep the generated report bundle replayable from the CLI:

- `report.outputs.downloads.json`
- `report.outputs.downloads.markdown`
- `report.outputs.downloads.html`

This keeps browser-demo copy closer to a download-oriented UI while preserving the same scenario-file -> report bundle contract.
