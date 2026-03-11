from __future__ import annotations

from governance_sandbox.engine import _normalize_preset


def test_normalize_preset_maps_singular_aliases_to_canonical_groups() -> None:
    assert _normalize_preset('delegate') == 'delegates'
    assert _normalize_preset('contributor') == 'contributors'
    assert _normalize_preset('investor') == 'investors'
    assert _normalize_preset('member') == 'community'
