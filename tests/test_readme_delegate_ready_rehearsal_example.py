from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeDelegateReadyRehearsalExampleTests(unittest.TestCase):
    def test_readme_mentions_delegate_ready_rehearsal_example(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('examples/delegate-ready-rehearsal.json', readme)
        self.assertTrue((ROOT / 'examples' / 'delegate-ready-rehearsal.json').exists())


if __name__ == '__main__':
    unittest.main()
