from fastapi import APIRouter, HTTPException

from apps.api.app.schemas import ProblemCreateRequest, ProblemDetail, ProblemSummary, SubmitRequest
from apps.api.app.services.sandbox import validate_language
from apps.api.app.state_machine import can_transition
from apps.api.app.store import SESSIONS, ProblemSession, next_id


router = APIRouter(prefix="/api/problems", tags=["problems"])


@router.post("", response_model=ProblemSummary, status_code=201)
def create_problem(payload: ProblemCreateRequest):
    if payload.difficulty not in {"easy", "medium", "hard"}:
        raise HTTPException(status_code=422, detail="invalid difficulty")
    validate_language(payload.language)

    pid = next_id()
    session = ProblemSession(
        id=pid,
        title=payload.title,
        module=payload.module,
        difficulty=payload.difficulty,
        language=payload.language,
        statement=payload.statement,
        user_thinking=payload.user_thinking,
        c_topics=payload.c_topics,
        tags=payload.tags,
        state="created",
    )
    if can_transition(session.state, "practicing"):
        session.state = "practicing"
    SESSIONS[pid] = session
    return ProblemSummary(**session.__dict__)


@router.get("", response_model=list[ProblemSummary])
def list_problems(
    module: str | None = None,
    difficulty: str | None = None,
    state: str | None = None,
):
    result = []
    for session in SESSIONS.values():
        if module and session.module != module:
            continue
        if difficulty and session.difficulty != difficulty:
            continue
        if state and session.state != state:
            continue
        result.append(ProblemSummary(**session.__dict__))
    return result


@router.get("/{problem_id}", response_model=ProblemDetail)
def get_problem(problem_id: int):
    session = SESSIONS.get(problem_id)
    if not session:
        raise HTTPException(status_code=404, detail="problem not found")
    return ProblemDetail(**session.__dict__)


@router.post("/{problem_id}/finish", response_model=ProblemSummary)
def finish_problem(problem_id: int):
    session = SESSIONS.get(problem_id)
    if not session:
        raise HTTPException(status_code=404, detail="problem not found")
    if not can_transition(session.state, "finished"):
        raise HTTPException(status_code=409, detail="current state cannot finish")
    session.state = "finished"
    return ProblemSummary(**session.__dict__)


@router.post("/{problem_id}/submit", response_model=ProblemSummary)
def submit_solution(problem_id: int, payload: SubmitRequest):
    session = SESSIONS.get(problem_id)
    if not session:
        raise HTTPException(status_code=404, detail="problem not found")
    session.latest_code = payload.code
    session.user_thinking = payload.user_thinking
    return ProblemSummary(**session.__dict__)
