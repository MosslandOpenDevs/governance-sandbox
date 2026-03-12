from __future__ import annotations

from dataclasses import asdict, dataclass


PRESET_SUMMARIES: dict[str, str] = {
    "dao": "Protocol and governance-process guardians focused on mandate clarity and accountability.",
    "delegates": "Decision-makers who want clear metrics, downside limits, and rollback conditions.",
    "contributors": "Operators and builders who balance delivery capacity against new governance demands.",
    "investors": "Capital-focused stakeholders who favor disciplined growth and visible efficiency signals.",
    "community": "Members who care about trust, inclusion, and whether the proposal still feels fair.",
}


PRESET_ALIASES: dict[str, str] = {
    'delegate': 'delegates',
    'contributor': 'contributors',
    'investor': 'investors',
    'member': 'community',
    'members': 'community',
    'communities': 'community',
}


TRAIT_PRESETS: dict[str, dict[str, str]] = {
    "dao": {
        "stance": "cautious",
        "concern": "Needs clarity on mandate, governance process, and accountability.",
        "mitigation": "State scope, decision rights, and reporting cadence in plain language.",
    },
    "delegates": {
        "stance": "cautious",
        "concern": "Wants explicit success metrics, downside limits, and rollback triggers.",
        "mitigation": "Add measurable milestones and a reversal path before the vote.",
    },
    "contributors": {
        "stance": "mixed",
        "concern": "Execution capacity may shift away from product and community commitments.",
        "mitigation": "Protect delivery bandwidth and publish ownership boundaries for the new work.",
    },
    "investors": {
        "stance": "supportive",
        "concern": "Supports growth, but worries about treasury discipline and signaling risk.",
        "mitigation": "Set budget ceilings, reporting checkpoints, and clear capital-efficiency goals.",
    },
    "community": {
        "stance": "skeptical",
        "concern": "May see the change as short-term optimization that weakens trust or inclusion.",
        "mitigation": "Explain member benefit, keep feedback loops open, and publish follow-up updates.",
    },
}


@dataclass
class StakeholderResponse:
    name: str
    stance: str
    concern: str
    mitigation: str
    preset: str | None = None


def _normalize_preset(raw: str | None) -> str | None:
    if raw is None:
        return None
    key = raw.strip().lower()
    if not key:
        return None
    return PRESET_ALIASES.get(key, key)


def _infer_response(stakeholder: str) -> StakeholderResponse:
    key = stakeholder.strip().lower()
    if "core" in key:
        return StakeholderResponse(
            name=stakeholder.strip(),
            stance="mixed",
            concern="Execution focus may drift from long-term mission.",
            mitigation="Define measurable campaign boundaries and publish review checkpoints.",
        )
    if "token" in key:
        return StakeholderResponse(
            name=stakeholder.strip(),
            stance="supportive",
            concern="Wants visible short-term traction but fears treasury waste.",
            mitigation="Publish budget limits and monthly reporting.",
        )
    if "delegate" in key or "governance" in key:
        return StakeholderResponse(
            name=stakeholder.strip(),
            stance="cautious",
            concern="Needs stronger rationale, guardrails, and rollback conditions.",
            mitigation="Add explicit success metrics and reversal criteria to the proposal.",
        )
    return StakeholderResponse(
        name=stakeholder.strip(),
        stance="skeptical",
        concern="May believe resources are being redirected away from long-term ecosystem value.",
        mitigation="Show how short-term spend supports medium-term ecosystem growth.",
    )


def simulate_governance(proposal: str, stakeholders: list[str] | list[dict[str, str]]) -> dict:
    responses: list[StakeholderResponse] = []

    for stakeholder in stakeholders:
        if isinstance(stakeholder, str):
            preset = _normalize_preset(stakeholder)
            if preset and preset in TRAIT_PRESETS:
                response = StakeholderResponse(name=stakeholder.strip(), preset=preset, **TRAIT_PRESETS[preset])
            else:
                response = _infer_response(stakeholder)
        else:
            name = (
                stakeholder.get("name")
                or stakeholder.get("stakeholder")
                or stakeholder.get("participant")
                or stakeholder.get("actor")
                or stakeholder.get("label")
                or stakeholder.get("title")
                or stakeholder.get("faction")
                or ""
            ).strip()
            preset = _normalize_preset(
                stakeholder.get("preset")
                or stakeholder.get("preset_name")
                or stakeholder.get("preset_key")
                or stakeholder.get("profile")
                or stakeholder.get("profile_name")
                or stakeholder.get("persona_preset")
                or stakeholder.get("group")
                or stakeholder.get("trait")
                or stakeholder.get("persona")
                or stakeholder.get("role")
                or stakeholder.get("archetype")
                or stakeholder.get("segment")
                or stakeholder.get("cohort")
                or stakeholder.get("bloc")
            )
            if preset and preset in TRAIT_PRESETS:
                trait = TRAIT_PRESETS[preset]
                response = StakeholderResponse(name=name, preset=preset, **trait)
            else:
                response = _infer_response(name)
                response.preset = preset
        responses.append(response)

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
        "scenario": {},
        "responses": [asdict(r) for r in responses],
        "major_risks": major_risks,
        "recommendation": recommendation,
        "decision_memo": (
            "The proposal is viable, but should be revised with clearer guardrails, "
            "success metrics, and stakeholder-facing mitigation language before launch."
        ),
    }
