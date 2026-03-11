# Governance sandbox scenario inputs report note

If the scenario fixture already keeps its runnable inputs inside `inputs`, allow `inputs.report` to carry report title, summary, audience, basename, and output paths too.

This keeps one JSON/YAML scenario file responsible for proposal text, stakeholder import, and report-bundle naming without forcing a second top-level report block.
