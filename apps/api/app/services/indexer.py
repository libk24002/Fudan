from __future__ import annotations

from collections import defaultdict
from pathlib import Path


def _parse_meta(meta_path: Path) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for raw in meta_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def rebuild_indexes(repo_root: Path) -> None:
    problems_root = repo_root / "problems"
    index_root = repo_root / "index"
    index_root.mkdir(parents=True, exist_ok=True)

    by_module: dict[str, list[str]] = defaultdict(list)
    by_c_topic: dict[str, list[str]] = defaultdict(list)

    if problems_root.exists():
        for meta in problems_root.glob("**/meta.yaml"):
            data = _parse_meta(meta)
            module = data.get("module", "unknown")
            title = data.get("title", meta.parent.name)
            rel = meta.parent.relative_to(repo_root)
            by_module[module].append(f"- {title} (`{rel}`)")

            raw_topics = data.get("c_topics", "[]").strip("[]")
            topics = [item.strip() for item in raw_topics.split(",") if item.strip()]
            for topic in topics:
                by_c_topic[topic].append(f"- {title} (`{rel}`)")

    module_lines = ["# By Module", ""]
    for module in sorted(by_module):
        module_lines.append(f"## {module}")
        module_lines.extend(sorted(by_module[module]))
        module_lines.append("")
    (index_root / "by-module.md").write_text("\n".join(module_lines), encoding="utf-8")

    topic_lines = ["# By C Topic", ""]
    for topic in sorted(by_c_topic):
        topic_lines.append(f"## {topic}")
        topic_lines.extend(sorted(by_c_topic[topic]))
        topic_lines.append("")
    (index_root / "by-c-topic.md").write_text("\n".join(topic_lines), encoding="utf-8")
