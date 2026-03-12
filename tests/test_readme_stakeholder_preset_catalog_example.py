from pathlib import Path


def test_readme_mentions_stakeholder_preset_catalog_example() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "examples/scenario-stakeholder-preset-catalog.yaml" in readme
    assert Path("examples/scenario-stakeholder-preset-catalog.yaml").exists()
