import pytest

from apps.api.app.services.sandbox import SandboxResult, validate_language


def test_result_contract_fields():
    result = SandboxResult(
        compile_ok=False,
        stdout="",
        stderr="compile error",
        exit_code=1,
        time_ms=10,
        memory_kb=1024,
        timeout=False,
    )
    assert result.compile_ok is False
    assert result.exit_code == 1


@pytest.mark.parametrize("language", ["c", "cpp", "java"])
def test_validate_language_accepts_supported(language):
    assert validate_language(language) == language


def test_validate_language_rejects_unsupported():
    with pytest.raises(ValueError):
        validate_language("python")
