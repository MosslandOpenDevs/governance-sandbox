# scenario-file JSON/YAML report start

Keep the current build order narrow: import one JSON or YAML scenario file first, then generate the matching JSON, Markdown, and HTML report bundle.

Quick replay:

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run \
  --scenario-file examples/scenario-report-bundle.yaml \
  --report-dir artifacts/replay
```

Use this path before widening preset expansion or the web demo.
