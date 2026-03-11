from __future__ import annotations

from governance_sandbox.engine import _normalize_preset


def test_normalize_preset_maps_plural_community_aliases_to_canonical_group() -> None:
    assert _normalize_preset('members') == 'community'
    assert _normalize_preset('communities') == 'community'
