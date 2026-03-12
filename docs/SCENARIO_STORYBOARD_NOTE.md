# SCENARIO_STORYBOARD_NOTE

Use `scenario_storyboard` when a workshop or web-form export wraps proposal, stakeholder, and report fields under one storyboard-style scenario object.

Keep the proof narrow:

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run   --scenario-file examples/scenario-report-bundle.yaml   --report-dir artifacts/storyboard-demo
```

Treat the wrapper as validated only when the imported scenario still regenerates the same JSON, Markdown, and HTML report bundle.
