from apps.api.app.services.repo_writer import write_archive
from apps.api.app.store import ProblemSession


def test_write_archive_includes_structured_review(tmp_path):
    session = ProblemSession(
        id=7,
        title="Delete Min Element",
        module="linear-list",
        difficulty="easy",
        language="c",
        statement="删除最小值元素",
        user_thinking="遍历找到最小位置后覆盖删除",
        state="finished",
        review_status="PASS",
        review_issues=[],
        review_suggestions=["可以补充空表边界说明"],
        ai_solution="#include <stdio.h>\nint main(void){return 0;}\n",
        review_rubric={
            "correctness": 5,
            "complexity": 4,
            "edge_cases": 4,
            "code_quality": 4,
            "thinking_clarity": 5,
        },
        review_total_score=22,
    )

    problem_dir = write_archive(tmp_path, session)
    review_text = (problem_dir / "review.md").read_text(encoding="utf-8")

    assert "status: PASS" in review_text
    assert "total_score: 22" in review_text
    assert "rubric:" in review_text
    assert "- thinking_clarity: 5" in review_text
