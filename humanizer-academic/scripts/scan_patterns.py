#!/usr/bin/env python3
"""
Lightweight pattern scan for humanizer-academic.

This is a deterministic helper for long drafts and batch review. It does not
rewrite text; it only reports rough counts for the pattern families the skill
cares about most.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ZH_RULES = {
    "negative_parallelism": [r"不是.{0,30}而是", r"不仅.{0,20}(还|更)", r"不只是.{0,20}更是"],
    "scaffolding": [r"首先", r"其次", r"最后", r"此外", r"同时", r"另一方面", r"综上所述", r"由此可见"],
    "officialese": [r"在.{0,15}背景下", r"具有重要意义", r"起到重要作用", r"提供有力支撑"],
    "nominalization": [r"对.{0,20}进行.{1,12}", r"实现.{0,20}提升", r"构建.{0,20}体系"],
    "uplift": [r"未来可期", r"彰显价值", r"书写新篇章", r"注入新动能"],
}

EN_RULES = {
    "inflation": [r"\bpivotal\b", r"\bcrucial\b", r"\bsignificant\b", r"\btestament\b", r"\bserves as\b"],
    "promotional": [r"\bvibrant\b", r"\bgroundbreaking\b", r"\bseamless\b", r"\bpowerful\b", r"\bshowcases?\b"],
    "vague_attribution": [r"\bexperts argue\b", r"\bobservers note\b", r"\bindustry reports suggest\b"],
    "ai_vocab": [r"\badditionally\b", r"\benhance\b", r"\bfostering\b", r"\blandscape\b", r"\bunderscore\b"],
    "filler_hedging": [r"\bin order to\b", r"\bdue to the fact that\b", r"\bat this point in time\b"],
}


def detect_language(text: str) -> str:
    zh_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    en_words = len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text))
    if zh_chars > en_words:
        return "zh"
    return "en"


def scan(text: str, language: str) -> dict[str, int]:
    rules = ZH_RULES if language == "zh" else EN_RULES
    flags = 0 if language == "zh" else re.IGNORECASE
    return {
        category: sum(len(re.findall(pattern, text, flags)) for pattern in patterns)
        for category, patterns in rules.items()
    }


def read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text()
    return sys.stdin.read()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?")
    parser.add_argument("--language", choices=["en", "zh", "auto"], default="auto")
    args = parser.parse_args()

    text = read_input(args.path)
    language = detect_language(text) if args.language == "auto" else args.language
    counts = scan(text, language)
    print(json.dumps({"language": language, "counts": counts}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
