# Governance Sandbox v2 — Logic Engine Upgrade

## Goal
Turn `governance-sandbox` from a one-shot governance rehearsal tool into a reusable governance logic engine.

## Problem
One-shot LLM outputs are useful, but they do not accumulate reasoning structure well enough.
The same governance tensions and tradeoffs get rediscovered repeatedly.

## v2 idea
Use the LLM less as a runtime answer generator and more as a reasoning-structure builder.

That means extracting and storing:
- variables,
- causal links,
- stakeholder influence patterns,
- mitigation rules,
- recurring governance failure modes.

## Example
Question:
"Should we shift treasury allocation from grants to short-term growth campaigns?"

Instead of only producing a narrative answer, v2 should also store reusable structure such as:
- growth spending affects short-term traction,
- short-term traction may conflict with long-term trust,
- trust is especially sensitive for contributors and delegates,
- explicit rollback criteria reduce resistance.

## Benefits
- more reusable reasoning
- lower future inference cost
- better consistency
- stronger governance memory
- easier scenario comparison across proposals

## Proposed output layers
1. stakeholder simulation output
2. decision memo
3. extracted logic graph
4. reusable governance rules

## Suggested next implementation steps
1. Add a structured intermediate schema for variables, edges, and stakeholder effects.
2. Store that schema alongside simulation results.
3. Add a report mode that shows both narrative output and extracted logic structure.
4. Add scenario diffing between two proposals.
