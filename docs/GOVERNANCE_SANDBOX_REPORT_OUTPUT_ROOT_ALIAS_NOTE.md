# Governance sandbox report output root alias note

Scenario files may use `output_root`, `report_output_root`, or `report_bundle_root` anywhere the report output directory is configured.

That keeps JSON, Markdown, and HTML report bundles grouped under one deterministic root even when scenario generators prefer root-style wording over `dir`.
