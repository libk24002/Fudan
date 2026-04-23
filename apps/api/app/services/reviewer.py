from __future__ import annotations

import json
import os
from urllib import error, request


RUBRIC_KEYS = [
    "correctness",
    "complexity",
    "edge_cases",
    "code_quality",
    "thinking_clarity",
]


def generate_ai_solution(statement: str, language: str) -> str:
    if language == "java":
        return "public class Main { public static void main(String[] args) {} }"
    if language == "cpp":
        return "#include <bits/stdc++.h>\nint main(){return 0;}\n"
    return "#include <stdio.h>\nint main(void){return 0;}\n"


def review_submission(user_code: str, user_thinking: str) -> dict[str, object]:
    issues: list[str] = []
    suggestions: list[str] = []
    rubric = {
        "correctness": 1,
        "complexity": 2,
        "edge_cases": 2,
        "code_quality": 2,
        "thinking_clarity": 1,
    }

    if len(user_thinking.strip()) < 10:
        issues.append("解题思路过短，无法判断完整性")
        suggestions.append("补充核心算法流程、边界条件与复杂度分析")
        rubric["thinking_clarity"] = 1
    else:
        rubric["thinking_clarity"] = 4
        rubric["edge_cases"] = 4
        rubric["complexity"] = 4

    if not user_code.strip():
        issues.append("未提交代码")
        suggestions.append("提交至少可编译的基础版本")
        rubric["correctness"] = 0
        rubric["code_quality"] = 0
    else:
        rubric["correctness"] = 4
        rubric["code_quality"] = 4

    code_lower = user_code.lower()
    if any(token in code_lower for token in ["malloc", "free", "null"]):
        rubric["edge_cases"] = min(5, rubric["edge_cases"] + 1)

    total_score = sum(rubric.values())

    status = "PASS" if not issues and total_score >= 18 else "FAIL"
    if status == "FAIL" and not issues:
        suggestions.append("建议补充复杂度与边界条件分析，提高解题完整性")

    return {
        "review_status": status,
        "issues": issues,
        "suggestions": suggestions,
        "rubric": rubric,
        "total_score": total_score,
    }


def _normalize_review_result(payload: dict[str, object]) -> dict[str, object]:
    status = payload.get("review_status", "FAIL")
    if status not in {"PASS", "FAIL"}:
        status = "FAIL"

    issues = payload.get("issues", [])
    if not isinstance(issues, list):
        issues = [str(issues)]

    suggestions = payload.get("suggestions", [])
    if not isinstance(suggestions, list):
        suggestions = [str(suggestions)]

    solution = payload.get("solution", "")
    if not isinstance(solution, str):
        solution = str(solution)

    raw_rubric = payload.get("rubric", {})
    rubric: dict[str, int] = {}
    if isinstance(raw_rubric, dict):
        for key in RUBRIC_KEYS:
            value = raw_rubric.get(key, 0)
            try:
                rubric[key] = max(0, min(5, int(value)))
            except (ValueError, TypeError):
                rubric[key] = 0
    else:
        rubric = {key: 0 for key in RUBRIC_KEYS}

    total_score_raw = payload.get("total_score")
    if total_score_raw is None:
        total_score = sum(rubric.values())
    else:
        try:
            total_score = int(total_score_raw)
        except (ValueError, TypeError):
            total_score = sum(rubric.values())
    total_score = max(0, min(25, total_score))

    return {
        "solution": solution,
        "review_status": status,
        "issues": [str(item) for item in issues],
        "suggestions": [str(item) for item in suggestions],
        "rubric": rubric,
        "total_score": total_score,
    }


def _generate_with_llm(*, statement: str, language: str, user_code: str, user_thinking: str) -> dict[str, object]:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing")

    api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
    model = os.environ.get("AI_REVIEW_MODEL", "gpt-4o-mini")

    prompt = (
        "你是算法评审助手。请输出 JSON，字段必须为:"
        " solution(string), review_status(PASS或FAIL), issues(array), suggestions(array),"
        " rubric(object: correctness/complexity/edge_cases/code_quality/thinking_clarity 每项0-5),"
        " total_score(0-25)。"
        f" 题目: {statement}\n语言: {language}\n用户代码:\n{user_code}\n用户思路:\n{user_thinking}"
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一位严格的编程评审与出题助手。"},
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
    }
    raw = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{api_base.rstrip('/')}/chat/completions",
        data=raw,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=40) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except error.URLError as exc:  # pragma: no cover - network path
        raise RuntimeError(f"LLM request failed: {exc}") from exc

    choices = body.get("choices", [])
    if not choices:
        raise RuntimeError("LLM response missing choices")

    content = choices[0].get("message", {}).get("content", "{}")
    parsed = json.loads(content)
    return _normalize_review_result(parsed)


def generate_solution_and_review(*, statement: str, language: str, user_code: str, user_thinking: str) -> dict[str, object]:
    if os.environ.get("OPENAI_API_KEY"):
        try:
            return _generate_with_llm(
                statement=statement,
                language=language,
                user_code=user_code,
                user_thinking=user_thinking,
            )
        except Exception:  # noqa: BLE001
            pass

    solution = generate_ai_solution(statement, language)
    review = review_submission(user_code, user_thinking)
    return {
        "solution": solution,
        "review_status": review["review_status"],
        "issues": review["issues"],
        "suggestions": review["suggestions"],
        "rubric": review["rubric"],
        "total_score": review["total_score"],
    }
