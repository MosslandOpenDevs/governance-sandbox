from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from governance_sandbox.engine import simulate_governance


def test_simulate_governance_accepts_faction_and_bloc_aliases() -> None:
    result = simulate_governance(
        "Pilot a delegate-ready governance review.",
        [{"faction": "Treasury stewards", "bloc": "delegates"}],
    )

    response = result["responses"][0]
    assert response["name"] == "Treasury stewards"
    assert response["preset"] == "delegates"
    assert response["stance"] == "cautious"
