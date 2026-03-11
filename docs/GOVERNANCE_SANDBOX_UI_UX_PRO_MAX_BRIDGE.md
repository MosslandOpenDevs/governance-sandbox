# Governance Sandbox UI/UX pro-max bridge

Use this note when the first web demo expands beyond scenario-file replay and starts touching form layout, result-card clarity, and report-download affordances.

## Keep the first slice narrow

- One scenario input form
- One result-card summary
- One visible report-download proof path

## UI/UX review rules

- Keep the scenario import path obvious before adding extra controls.
- Prefer one primary action per screen state.
- Make report artifacts easy to spot from the first result card.
- Preserve CLI parity so the web demo still maps back to the same scenario-file workflow.

## Browser-proof rules

- Verify one stable happy path first.
- Expand coverage only after the first form-to-card replay is deterministic.
- Keep recovery notes close to the demo slice so failed browser checks have a clear next action.
