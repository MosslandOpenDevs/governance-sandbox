from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StakeholderResponse:
    name: str
    stance: str
    concern: str
    mitigation: str


def simulate_governance(proposal: str, stakeholders: list[str]) -> dict:
    responses: list[StakeholderResponse] = []

    for stakeholder in stakeholders:
        key = stakeholder.strip().lower()
        if "core" in key:
            stance = "mixed"
            concern = "Execution focus may drift from long-term mission."
            mitigation = "Define measurable campaign boundaries and publish review checkpoints."
        elif "token" in key:
            stance = "supportive"
            concern = "Wants visible short-term traction but fears treasury waste."
            mitigation = "Publish budget limits and monthly reporting."
        elif "delegate" in key or "governance" in key:
            stance = "cautious"
            concern = "Needs stronger rationale, guardrails, and rollback conditions."
            mitigation = "Add explicit success metrics and reversal criteria to the proposal."
        else:
            stance = "skeptical"
            concern = "May believe resources are being redirected away from long-term ecosystem value."
            mitigation = "Show how short-term spend supports medium-term ecosystem growth."

        responses.append(
            StakeholderResponse(
                name=stakeholder.strip(),
                stance=stance,
                concern=concern,
                mitigation=mitigation,
            )
        )

    major_risks = [
        "Stakeholder trust erosion if rationale is unclear.",
        "Narrative backlash if growth spending appears opportunistic.",
        "Execution drift if campaign success metrics are vague.",
    ]

    recommendation = (
        "Proceed with revision" if any(r.stance in {"mixed", "cautious", "skeptical"} for r in responses)
        else "Proceed"
    )

    return {
        "proposal": proposal,
        "responses": [r.__dict__ for r in responses],
        "major_risks": major_risks,
        "recommendation": recommendation,
        "decision_memo": (
            "The proposal is viable, but should be revised with clearer guardrails, "
            "success metrics, and stakeholder-facing mitigation language before launch."
        ),
    }
