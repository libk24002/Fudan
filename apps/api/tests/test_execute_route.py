from apps.api.app.services.sandbox import SandboxResult


def test_execute_requires_supported_language(client):
    response = client.post(
        "/api/sandbox/execute",
        json={"language": "python", "code": "print(1)", "stdin": ""},
    )
    assert response.status_code == 422


def test_execute_uses_executor(client, monkeypatch):
    def fake_execute(language: str, code: str, stdin: str = ""):
        _ = (language, code, stdin)
        return SandboxResult(
            compile_ok=True,
            stdout="ok",
            stderr="",
            exit_code=0,
            time_ms=1,
            memory_kb=0,
            timeout=False,
        )

    monkeypatch.setattr("apps.api.app.routes.sandbox.execute_code", fake_execute)
    response = client.post(
        "/api/sandbox/execute",
        json={"language": "c", "code": "int main(){return 0;}", "stdin": ""},
    )
    assert response.status_code == 200
    assert response.json()["compile_ok"] is True
