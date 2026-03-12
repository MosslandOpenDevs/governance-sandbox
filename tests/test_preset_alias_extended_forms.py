from __future__ import annotations

import unittest

from governance_sandbox.engine import simulate_governance


class PresetAliasExtendedFormsTests(unittest.TestCase):
    def test_extended_preset_aliases_map_to_trait_presets(self) -> None:
        result = simulate_governance(
            "Publish a delegate-ready treasury review with clear rollback checkpoints.",
            [
                {"name": "DAO core", "preset": "daos"},
                {"name": "Working delegation", "preset": "delegation"},
                {"name": "Ops guild", "preset": "contributors-core"},
                {"name": "Treasury update list", "preset": "investor-relations"},
                {"name": "Forum members", "preset": "community-members"},
            ],
        )

        presets = [response["preset"] for response in result["responses"]]
        self.assertEqual(presets, ["dao", "delegates", "contributors", "investors", "community"])


if __name__ == "__main__":
    unittest.main()
