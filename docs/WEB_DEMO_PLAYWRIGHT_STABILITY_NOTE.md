# Web demo Playwright stability note

Keep the first governance-sandbox browser proof limited to one replayable form submission, one stable result card, and one visible report-download outcome.

Use this note when the web demo starts borrowing Playwright-style practices:

- check one deterministic fixture before widening inputs,
- verify the result card before validating download/report links,
- prefer explicit step-by-step assertions over broad end-to-end guesses,
- capture failures with enough context to rerun the same scenario-file path.

This keeps the web demo aligned with the CLI-first scenario-file -> markdown/html/json report workflow while staying reproducible.
