#!/usr/bin/env python3
"""
Batch rewrite evaluation documents with codex exec.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


EN_RULES = [
    "Preserve meaning, evidence, numbers, chronology, and section structure.",
    "Keep an academic register: serious, restrained, specific, and readable.",
    "Remove common AI-writing signals: inflated significance, promotional adjectives, vague attribution, empty uplift, formulaic contrasts, rule-of-three scaffolding, em-dash overuse, filler phrases, and generic conclusions.",
    "Prefer direct claims, concrete verbs, and precise transitions.",
    "Do not invent facts, citations, or quotations.",
    "Output only the rewritten paper in Markdown.",
]

ZH_RULES = [
    "保留原文含义、证据、数字、时间顺序和章节结构。",
    "保持学术语域：严肃、克制、具体、可读，不要口语化。",
    "重点消除中文 AI 痕迹：不是……而是……、不仅……还……、首先/其次/最后、在……背景下、具有重要意义、起到重要作用、抽象名词化、空泛升华、模板化总结。",
    "优先使用直接陈述、具体动词和真实逻辑衔接，不要靠套话推进。",
    "不要编造事实、引文、数据或来源。",
    "只输出改写后的 Markdown 正文，不要加说明。",
]


def make_prompt(language: str, source_text: str) -> str:
    rules = ZH_RULES if language == "zh" else EN_RULES
    preface = (
        "请改写下面这篇中文学术文本。\n\n要求：\n"
        if language == "zh"
        else "Rewrite the following academic paper.\n\nRequirements:\n"
    )
    body = "\n".join(f"- {rule}" for rule in rules)
    source_label = "\n\n原文：\n\n" if language == "zh" else "\n\nSource paper:\n\n"
    return f"{preface}{body}{source_label}{source_text}\n"


def run_one(item: dict[str, str], root: Path, output_dir: Path, timeout: int, force: bool) -> dict[str, object]:
    source_path = root / item["path"]
    output_path = output_dir / f"{item['id']}.md"
    log_path = output_dir / f"{item['id']}.log"
    output_dir.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and output_path.stat().st_size > 0 and not force:
        return {
            "id": item["id"],
            "status": "skipped",
            "output_path": str(output_path.relative_to(root)),
            "log_path": str(log_path.relative_to(root)),
        }

    prompt = make_prompt(item["language"], source_path.read_text())
    cmd = [
        "codex",
        "exec",
        "--ephemeral",
        "-s",
        "read-only",
        "--color",
        "never",
        "-C",
        str(root),
        "-o",
        str(output_path),
        "-",
    ]
    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        log_path.write_text((exc.stdout or "") + "\n[TIMEOUT]\n" + (exc.stderr or ""))
        return {
            "id": item["id"],
            "status": "timeout",
            "output_path": str(output_path.relative_to(root)),
            "log_path": str(log_path.relative_to(root)),
        }

    log_path.write_text((result.stdout or "") + ("\n" if result.stdout else "") + (result.stderr or ""))
    status = "ok" if result.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0 else "failed"
    return {
        "id": item["id"],
        "status": status,
        "returncode": result.returncode,
        "output_path": str(output_path.relative_to(root)),
        "log_path": str(log_path.relative_to(root)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="eval/dataset_manifest.json")
    parser.add_argument("--output-dir", default="eval/outputs/codex-gpt-5.4")
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--ids", nargs="*")
    args = parser.parse_args()

    root = Path.cwd()
    manifest = json.loads((root / args.manifest).read_text())
    if args.ids:
        wanted = set(args.ids)
        manifest = [item for item in manifest if item["id"] in wanted]
    if args.limit is not None:
        manifest = manifest[: args.limit]

    output_dir = root / args.output_dir
    results = []
    rewritten_manifest = []
    for idx, item in enumerate(manifest, start=1):
        print(f"[{idx}/{len(manifest)}] {item['id']}", flush=True)
        result = run_one(item, root, output_dir, args.timeout, args.force)
        results.append(result)
        if result["status"] in {"ok", "skipped"}:
            rewritten_manifest.append(
                {
                    "id": item["id"],
                    "model_family": item["model_family"],
                    "language": item["language"],
                    "topic": item["topic"],
                    "path": result["output_path"],
                }
            )

    (output_dir / "manifest.json").write_text(json.dumps(rewritten_manifest, ensure_ascii=False, indent=2) + "\n")
    (output_dir / "run-summary.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")

    failures = [r for r in results if r["status"] not in {"ok", "skipped"}]
    print(json.dumps({"total": len(results), "failures": len(failures), "output_dir": str(output_dir.relative_to(root))}, ensure_ascii=False))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
