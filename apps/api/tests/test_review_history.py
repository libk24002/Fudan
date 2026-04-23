def _create_and_finish_problem(client):
    created = client.post(
        "/api/problems",
        json={
            "title": "history demo",
            "module": "linear-list",
            "difficulty": "easy",
            "language": "c",
            "statement": "删除最小值",
            "user_thinking": "遍历找到最小值",
        },
    )
    assert created.status_code == 201
    pid = created.json()["id"]

    submitted = client.post(
        f"/api/problems/{pid}/submit",
        json={
            "code": "#include <stdio.h>\nint main(void){return 0;}",
            "user_thinking": "遍历顺序表，找到最小值后覆盖删除",
        },
    )
    assert submitted.status_code == 200

    finished = client.post(f"/api/problems/{pid}/finish")
    assert finished.status_code == 200
    return pid


def test_review_history_is_persisted_in_problem_detail(client):
    pid = _create_and_finish_problem(client)

    review_1 = client.post(f"/api/problems/{pid}/review")
    assert review_1.status_code == 200

    submitted_again = client.post(
        f"/api/problems/{pid}/submit",
        json={
            "code": "#include <stdio.h>\nint main(void){return 0;}",
            "user_thinking": "补充边界条件，空表直接返回，再执行覆盖删除",
        },
    )
    assert submitted_again.status_code == 200

    review_2 = client.post(f"/api/problems/{pid}/review")
    assert review_2.status_code == 200

    detail = client.get(f"/api/problems/{pid}")
    assert detail.status_code == 200
    payload = detail.json()

    assert "review_history" in payload
    assert len(payload["review_history"]) == 2
    assert payload["review_history"][0]["attempt"] == 1
    assert payload["review_history"][1]["attempt"] == 2
