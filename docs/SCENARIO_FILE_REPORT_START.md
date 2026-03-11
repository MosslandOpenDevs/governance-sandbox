# Scenario file -> report start

Use one scenario file plus one report directory when you want the narrowest believable governance-sandbox replay for imported proposal/stakeholder input and generated JSON/Markdown/HTML report artifacts.

## Fast path

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run \
  --scenario-file examples/scenario-report-bundle.yaml \
  --report-dir artifacts/review
```

## Why this lane exists

- keeps proposal + stakeholder input in one replayable JSON/YAML fixture
- generates markdown/html report files beside the JSON artifact bundle
- gives maintainers one reviewable command before widening to web-demo work
