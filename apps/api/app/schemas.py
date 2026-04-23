from __future__ import annotations

from pydantic import BaseModel, Field


ALLOWED_DIFFICULTY = {"easy", "medium", "hard"}
ALLOWED_STATE = {"created", "practicing", "finished", "archiving", "archived"}


class ProblemCreateRequest(BaseModel):
    title: str = Field(min_length=1)
    module: str = Field(min_length=1)
    difficulty: str
    language: str
    statement: str = Field(min_length=1)
    user_thinking: str = ""
    c_topics: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class ProblemSummary(BaseModel):
    id: int
    title: str
    module: str
    difficulty: str
    language: str
    state: str


class ProblemDetail(ProblemSummary):
    statement: str
    user_thinking: str
    latest_code: str = ""
    review_status: str | None = None
    review_history: list[dict[str, object]] = Field(default_factory=list)


class ExecuteRequest(BaseModel):
    language: str
    code: str
    stdin: str = ""


class SubmitRequest(BaseModel):
    code: str
    user_thinking: str


class ReviewResponse(BaseModel):
    review_status: str
    issues: list[str]
    suggestions: list[str]
    rubric: dict[str, int]
    total_score: int


class MessageResponse(BaseModel):
    message: str
