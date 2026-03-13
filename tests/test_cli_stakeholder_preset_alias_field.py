import unittest

from governance_sandbox.engine import simulate_governance


class StakeholderPresetAliasFieldTests(unittest.TestCase):
    def test_simulate_governance_accepts_preset_alias_field(self) -> None:
        result = simulate_governance(
            "Adopt a staged governance rollout.",
            [{"name": "Treasury delegates", "preset_alias": "delegate"}],
        )
        response = result["responses"][0]
        self.assertEqual(response["preset"], "delegates")
        self.assertEqual(response["stance"], "cautious")


if __name__ == "__main__":
    unittest.main()
