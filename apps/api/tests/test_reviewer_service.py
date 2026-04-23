from apps.api.app.services import reviewer


def test_review_submission_passes_with_complete_input():
    result = reviewer.review_submission(
        user_code="#include <stdio.h>\nint main(void){return 0;}",
        user_thinking="先遍历顺序表找到最小值位置，再用尾元素覆盖并长度减一。",
    )
    assert result["review_status"] == "PASS"
    assert result["issues"] == []
    assert result["rubric"]["correctness"] >= 4
    assert result["total_score"] >= 20


def test_review_submission_uses_llm_when_enabled(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    def fake_llm(*, statement: str, language: str, user_code: str, user_thinking: str):
        _ = (statement, language, user_code, user_thinking)
        return {
            "solution": "#include <stdio.h>\nint main(void){return 0;}\n",
            "review_status": "PASS",
            "issues": [],
            "suggestions": ["边界条件说明清晰"],
            "rubric": {
                "correctness": 5,
                "complexity": 4,
                "edge_cases": 4,
                "code_quality": 4,
                "thinking_clarity": 5,
            },
            "total_score": 22,
        }

    monkeypatch.setattr(reviewer, "_generate_with_llm", fake_llm)
    generated = reviewer.generate_solution_and_review(
        statement="删除最小值",
        language="c",
        user_code="#include <stdio.h>\nint main(void){return 0;}",
        user_thinking="先找最小值位置，再覆盖删除并更新长度。",
    )
    assert generated["solution"].startswith("#include <stdio.h>")
    assert generated["review_status"] == "PASS"
    assert generated["rubric"]["thinking_clarity"] == 5
    assert generated["total_score"] == 22
