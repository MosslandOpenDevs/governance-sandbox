# Scenario report relative-path replay

When a scenario file already owns the report outputs, keep relative JSON/Markdown/HTML paths replayable from the scenario directory without extra shell glue.

Minimum proof:
- one scenario file with relative report output paths
- one generated JSON artifact
- one generated markdown report
- one generated HTML report
- one README example that can be rerun from a clean checkout
