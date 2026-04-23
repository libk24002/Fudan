from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ProblemSession:
    id: int
    title: str
    module: str
    difficulty: str
    language: str
    statement: str
    user_thinking: str
    c_topics: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    state: str = "created"
    latest_code: str = ""
    review_status: str | None = None
    review_issues: list[str] = field(default_factory=list)
    review_suggestions: list[str] = field(default_factory=list)
    review_rubric: dict[str, int] = field(default_factory=dict)
    review_total_score: int = 0
    review_history: list[dict[str, object]] = field(default_factory=list)
    ai_solution: str = ""


SESSIONS: dict[int, ProblemSession] = {}
NEXT_ID = 1


def next_id() -> int:
    global NEXT_ID
    value = NEXT_ID
    NEXT_ID += 1
    return value


def reset_store() -> None:
    global NEXT_ID
    SESSIONS.clear()
    NEXT_ID = 1
