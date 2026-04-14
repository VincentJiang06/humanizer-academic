#!/usr/bin/env python3
"""
Apply a narrow post-pass to English academic drafts to remove report-shell residue
without changing the underlying argument.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bTaken together,\s+"), ""),
    (
        re.compile(
            r"\bThe first major growth pillar over the next five years is likely to remain ([^.]+?)\.",
            re.IGNORECASE,
        ),
        r"Over the next five years, \1 is likely to remain the main growth pillar.",
    ),
    (
        re.compile(r"\bThe second pillar is ([^.]+?)\.", re.IGNORECASE),
        r"A second growth driver is \1.",
    ),
    (
        re.compile(r"\bThe third pillar is ([^.]+?)\.", re.IGNORECASE),
        r"A third growth driver is \1.",
    ),
    (
        re.compile(r"(?m)^## Executive Summary\s*$"),
        "## Abstract",
    ),
    (
        re.compile(r"(?m)^### Chapter (\d+): (.+)$"),
        r"### \2",
    ),
    (
        re.compile(r"(?m)^## Part [IVX]+: (.+)$"),
        r"## \1",
    ),
]


def polish(text: str) -> str:
    updated = text
    for pattern, replacement in REPLACEMENTS:
        updated = pattern.sub(replacement, updated)
    updated = re.sub(r"\n{3,}", "\n\n", updated)
    return updated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    for raw_path in args.paths:
        path = Path(raw_path)
        original = path.read_text()
        revised = polish(original)
        if revised != original:
            path.write_text(revised)
            print(f"Polished {path}")


if __name__ == "__main__":
    main()
