# Scenario stakeholder_types wrapper note

Keep `stakeholder_types` valid even when a JSON/YAML rehearsal arrives through a wrapper such as `scenario_demo` or another scenario bundle envelope.

Phase-one rule stays the same:

1. import one scenario file,
2. resolve proposal + stakeholder aliases without reshaping the bundle by hand,
3. regenerate one JSON/Markdown/HTML report bundle.

This keeps stakeholder preset imports compatible with wrapper-style exports while the repo still stays scenario-file and report-first.
