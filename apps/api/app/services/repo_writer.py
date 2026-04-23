from __future__ import annotations

from datetime import date
from pathlib import Path

from apps.api.app.store import ProblemSession


def slugify(name: str) -> str:
    return "-".join(name.strip().lower().split())


def write_archive(repo_root: Path, session: ProblemSession) -> Path:
    problem_dir = repo_root / "problems" / session.module / slugify(session.title)
    problem_dir.mkdir(parents=True, exist_ok=True)

    (problem_dir / "solution.c").write_text(session.ai_solution, encoding="utf-8")

    readme = f"""# {session.title}

## 题意

{session.statement}

## AI 标准思路

归档时由 AI 自动生成参考实现。

## 用户思路摘要

{session.user_thinking}

## 复杂度

- 时间复杂度: TBD
- 空间复杂度: TBD

## 记录

- 首次完成日期: {date.today().isoformat()}
- 最后修改日期: {date.today().isoformat()}
"""
    (problem_dir / "README.md").write_text(readme, encoding="utf-8")

    meta = f"""id: P-{session.id:04d}
title: {session.title}
module: {session.module}
difficulty: {session.difficulty}
status: done
language: {session.language}
c_topics: [{', '.join(session.c_topics)}]
tags: [{', '.join(session.tags)}]
"""
    (problem_dir / "meta.yaml").write_text(meta, encoding="utf-8")

    rubric_lines = [f"- {key}: {value}" for key, value in sorted(session.review_rubric.items())]
    review = "\n".join([
        f"status: {session.review_status}",
        f"total_score: {session.review_total_score}",
        "rubric:",
        *rubric_lines,
        "issues:",
        *[f"- {item}" for item in session.review_issues],
        "suggestions:",
        *[f"- {item}" for item in session.review_suggestions],
    ])
    (problem_dir / "review.md").write_text(review + "\n", encoding="utf-8")
    return problem_dir
