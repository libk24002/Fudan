from fastapi import APIRouter, HTTPException

from apps.api.app.schemas import ExecuteRequest
from apps.api.app.services.sandbox import SandboxResult, execute_code, validate_language


router = APIRouter(prefix="/api/sandbox", tags=["sandbox"])


@router.post("/execute", response_model=SandboxResult)
def execute(payload: ExecuteRequest):
    try:
        validate_language(payload.language)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    try:
        return execute_code(payload.language, payload.code, payload.stdin)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=f"sandbox dependency missing: {exc}") from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"sandbox execution failed: {exc}") from exc
