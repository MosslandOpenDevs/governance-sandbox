# Governance Sandbox report output slug alias note

Use `report.output_slug` or `report.outputs.output_slug` when a scenario file should set the shared basename for JSON, Markdown, and HTML report artifacts without repeating the same path stem across multiple keys.

This keeps scenario-file import and report-bundle generation coupled in one replayable fixture.
