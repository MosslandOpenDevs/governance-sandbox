# PRESET_JSON_FORM_CARD_START

Use this note when governance-sandbox starts the first web demo and needs a stable bridge from CLI preset data to UI.

## Start from one CLI source

Generate the preset catalog first:

```bash
PYTHONPATH=src python3 -m governance_sandbox.cli run --list-presets-json
```

Then keep the first browser slice limited to:

1. one scenario form,
2. one result card,
3. one report download path.

## Why this matters

- The form can explain preset choices without duplicating hard-coded stakeholder text.
- The result card stays tied to the same scenario + report output contract already proven by the CLI.
- Browser proof remains reproducible because the first UI state starts from one machine-readable source.

## Minimum acceptance

Before widening the demo, confirm:

- the form uses preset JSON as its trait source,
- the result card summarizes one completed run,
- the card keeps one visible report download or artifact cue.
