# Scenario source_location alias note

Use `source_location` when a JSON or YAML scenario fixture already carries the original scenario path or URL under a neutral export field. The CLI resolves `source_location` into the same `scenario_file` metadata shown in JSON output plus generated Markdown and HTML reports, so imported rehearsal bundles do not need a separate rename step before replay.
