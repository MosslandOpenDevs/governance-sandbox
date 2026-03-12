# Scenario top-level wrapper note

Use the `scenario` wrapper when you want one JSON/YAML file to keep imported proposal + stakeholder inputs grouped under a single top-level key.

Minimal pattern:

```yaml
scenario:
  proposal: Ship a treasury review workflow with reversible guardrails.
  stakeholders:
    - name: Delegate council
      preset: delegates
    - name: Core contributors
      preset: contributors
  report:
    title: Wrapped scenario memo
```

This keeps scenario-file input compatible with the same markdown/html/json report flow.
