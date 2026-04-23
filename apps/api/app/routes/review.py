from pathlib import Path

from fastapi import APIRouter, HTTPException

from apps.api.app.schemas import MessageResponse, ReviewResponse
from apps.api.app.services.indexer import rebuild_indexes
from apps.api.app.services.repo_writer import write_archive
from apps.api.app.services.reviewer import generate_solution_and_review
from apps.api.app.state_machine import can_transition
from apps.api.app.store import SESSIONS


router = APIRouter(prefix="/api/problems", tags=["review"])


@router.post("/{problem_id}/review", response_model=ReviewResponse)
def review_problem(problem_id: int):
    session = SESSIONS.get(problem_id)
    if not session:
        raise HTTPException(status_code=404, detail="problem not found")
    if session.state not in {"finished", "archiving"}:
        raise HTTPException(status_code=409, detail="problem must be finished before review")

    result = generate_solution_and_review(
        statement=session.statement,
        language=session.language,
        user_code=session.latest_code,
        user_thinking=session.user_thinking,
    )
    session.ai_solution = str(result["solution"])

    session.review_status = str(result["review_status"])
    session.review_issues = list(result["issues"])
    session.review_suggestions = list(result["suggestions"])
    session.review_rubric = dict(result.get("rubric", {}))
    session.review_total_score = int(result.get("total_score", 0))
    session.review_history.append(
        {
            "attempt": len(session.review_history) + 1,
            "status": session.review_status,
            "total_score": session.review_total_score,
            "rubric": session.review_rubric,
        }
    )

    return ReviewResponse(**result)


@router.post("/{problem_id}/archive", response_model=MessageResponse)
def archive_problem(problem_id: int):
    session = SESSIONS.get(problem_id)
    if not session:
        raise HTTPException(status_code=404, detail="problem not found")
    if session.state != "finished":
        raise HTTPException(status_code=409, detail="problem must be finished before archive")
    if session.review_status != "PASS":
        raise HTTPException(status_code=409, detail="review status must be PASS")
    if not can_transition(session.state, "archiving"):
        raise HTTPException(status_code=409, detail="invalid state transition")

    session.state = "archiving"
    repo_root = Path(__file__).resolve().parents[5]
    write_archive(repo_root, session)
    rebuild_indexes(repo_root)
    session.state = "archived"
    return MessageResponse(message="archived")
