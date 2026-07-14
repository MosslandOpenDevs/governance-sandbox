#!/usr/bin/env python3
"""Fail if any relative link in the README (or docs) points at a missing file.

This is a deterministic, offline link checker — it only validates repo-local
targets (``docs/...``, ``examples/...``, ``LICENSE``, ``./path``), not external
URLs. It exists because broken ``docs/*.md`` references had accumulated in the
README; see docs/ROADMAP.md.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Files whose local links we validate.
SOURCES = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]

# Markdown links [text](target) and inline-code repo paths like `docs/FOO.md`.
MD_LINK = re.compile(r"\]\(([^)]+)\)")
INLINE_PATH = re.compile(r"`((?:docs|examples|src|tests|scripts)/[^`\s]+)`")


def _is_local(target: str) -> bool:
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return False
    return True


def check_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    targets: set[str] = set()
    for m in MD_LINK.finditer(text):
        targets.add(m.group(1).split("#", 1)[0].strip())
    for m in INLINE_PATH.finditer(text):
        targets.add(m.group(1).split("#", 1)[0].strip())

    missing: list[str] = []
    for target in sorted(t for t in targets if t and _is_local(t)):
        # This repo mixes file-relative and repo-root-relative link styles, so a
        # link is valid if it resolves under either base.
        file_relative = (path.parent / target).resolve()
        root_relative = (ROOT / target).resolve()
        if not file_relative.exists() and not root_relative.exists():
            missing.append(f"{path.relative_to(ROOT)} -> {target}")
    return missing


def main() -> int:
    missing: list[str] = []
    for src in SOURCES:
        if src.exists():
            missing.extend(check_file(src))
    if missing:
        print("Broken relative links found:")
        for m in missing:
            print(f"  {m}")
        return 1
    print(f"OK: all relative links resolve across {len(SOURCES)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
