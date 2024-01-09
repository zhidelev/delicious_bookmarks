import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def test_client():
    yield TestClient(app)


def test_get_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "world!"}


@pytest.mark.parametrize("b_id", [-1, "test_string", None, True])
def test_get_by_id(test_client, b_id):
    response = test_client.get(f"/bookmarks/{b_id}")
    assert response.status_code == 422


@pytest.mark.xfail
def test_get_all_bookmarks(test_client):
    response = test_client.get("/bookmarks/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_bookmarks_not_empty(test_client):
    test_client.post("/bookmarks/", json={"uri": "https://test.com"})
    response = test_client.get("/bookmarks")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_create_bookmark(test_client):
    response = test_client.post("/bookmarks/", json={"uri": "https://test.com"})
    assert response.status_code == 200
    assert "id" in response.json()
    assert isinstance(response.json()["id"], int)
