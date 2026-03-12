# Scenario source alias note

When a governance scenario is piped over stdin, preserve source provenance with one of these fields if the CLI path is not available:

- `scenario_source`
- `source`
- `source_file`
- `scenario_path`
- `source_path`

The generated JSON payload, markdown report, and HTML report should all keep that same source label visible so reviewers can trace the rehearsal back to the original scenario asset.
