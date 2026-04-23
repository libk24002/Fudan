import pytest
from fastapi.testclient import TestClient

from apps.api.app.store import reset_store
from apps.api.main import app


@pytest.fixture
def client():
    reset_store()
    return TestClient(app)
