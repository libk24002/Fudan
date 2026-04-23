def test_create_problem_session(client):
    response = client.post(
        "/api/problems",
        json={
            "title": "delete min element",
            "module": "linear-list",
            "difficulty": "easy",
            "language": "c",
            "statement": "delete min",
            "user_thinking": "scan and replace",
        },
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["state"] == "practicing"
    assert payload["module"] == "linear-list"


def test_finish_requires_existing_problem(client):
    response = client.post("/api/problems/999/finish")
    assert response.status_code == 404
