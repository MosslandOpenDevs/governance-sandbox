from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from governance_sandbox.cli import _normalize_stakeholders


class ScenarioMapObjectAliasesTests(unittest.TestCase):
    def test_normalize_stakeholders_accepts_object_aliases(self) -> None:
        stakeholders = _normalize_stakeholders({
            "delegate-slot": {"label": "Lead Delegate", "trait_preset": "delegates"}
        })

        self.assertEqual(stakeholders, [{"name": "Lead Delegate", "preset": "delegates"}])


if __name__ == "__main__":
    unittest.main()
