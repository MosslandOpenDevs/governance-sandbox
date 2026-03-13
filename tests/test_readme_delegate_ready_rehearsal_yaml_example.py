from pathlib import Path
import unittest


class ReadmeDelegateReadyRehearsalYamlExampleTests(unittest.TestCase):
    def test_readme_mentions_delegate_ready_rehearsal_yaml_example(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')

        self.assertIn('examples/delegate-ready-rehearsal.yaml', readme)
        example = (root / 'examples' / 'delegate-ready-rehearsal.yaml').read_text(encoding='utf-8')
        self.assertIn('preset: delegates', example)
        self.assertIn('basename: delegate-ready-rehearsal', example)


if __name__ == '__main__':
    unittest.main()
