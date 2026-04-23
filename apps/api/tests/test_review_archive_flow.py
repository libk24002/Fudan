def _create_problem(client):
    response = client.post(
        "/api/problems",
        json={
            "title": "delete range",
            "module": "linear-list",
            "difficulty": "easy",
            "language": "c",
            "statement": "delete [s,t]",
            "user_thinking": "two pointers and overwrite",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_archive_requires_finished_and_pass_review(client):
    pid = _create_problem(client)

    response = client.post(f"/api/problems/{pid}/archive")
    assert response.status_code == 409

    submit = client.post(
        f"/api/problems/{pid}/submit",
        json={
            "code": "#include <stdio.h>\nint main(){return 0;}",
            "user_thinking": "iterate and copy non-range elements",
        },
    )
    assert submit.status_code == 200

    finish = client.post(f"/api/problems/{pid}/finish")
    assert finish.status_code == 200

    review = client.post(f"/api/problems/{pid}/review")
    assert review.status_code == 200
    assert review.json()["review_status"] == "PASS"

    archive = client.post(f"/api/problems/{pid}/archive")
    assert archive.status_code == 200
    assert archive.json()["message"] == "archived"
