from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from governance_sandbox.engine import simulate_governance


def test_simulate_governance_accepts_label_alias_for_stakeholder_name() -> None:
    result = simulate_governance(
        "Adopt a staged treasury reporting pilot.",
        [{"label": "Treasury delegates", "preset": "delegates"}],
    )

    response = result["responses"][0]
    assert response["name"] == "Treasury delegates"
    assert response["preset"] == "delegates"
    assert response["stance"] == "cautious"


def test_simulate_governance_accepts_string_preset_name() -> None:
    result = simulate_governance(
        "Adopt a staged treasury reporting pilot.",
        ["delegates"],
    )

    response = result["responses"][0]
    assert response["name"] == "delegates"
    assert response["preset"] == "delegates"
    assert response["stance"] == "cautious"
