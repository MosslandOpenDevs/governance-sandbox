# Scenario file -> report owner/audience start

Keep the current priority lane tight: import one JSON/YAML scenario file, generate one JSON/Markdown/HTML report bundle, and make the owner/audience metadata visible in the rendered report.

Suggested replay:

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run \
  --scenario-file examples/scenario-review-pack.yaml \
  --report-dir artifacts/review-pack
```

Review cues:
- scenario file import succeeds
- markdown and HTML reports are generated beside JSON
- owner metadata is visible
- audience metadata is visible
