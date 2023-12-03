from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture(scope="module")
def test_client():
    yield TestClient(app)


def test_get_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "world!"}
