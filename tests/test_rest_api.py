import pytest
from fastapi.testclient import TestClient
from web.main import app

client = TestClient(app)

URL = "http://127.0.0.1:8000"
PAYLOAD = {"href": "https://www.smartvideos.ru/", "tags": [], "private": True}


def test_get_all_links():
    r = client.post(f"{URL}/links", json=PAYLOAD)
    assert r.status_code == 201
    resp = r.json()
    assert "id" in resp

    link_id = resp["id"]

    r = client.get(f"{URL}/links")
    assert r.status_code == 200
    resp = r.json()
    assert "links" in resp
    assert link_id in [i["id"] for i in resp["links"]]


def test_create_link():
    r = client.post(f"{URL}/links", json=PAYLOAD)
    assert r.status_code == 201
    resp = r.json()
    assert "id" in resp


def test_get_link():
    r = client.post(f"{URL}/links", json=PAYLOAD)
    assert r.status_code == 201
    resp = r.json()
    assert "id" in resp

    link_id = resp["id"]

    r = client.get(f"{URL}/links/{link_id}")
    assert r.status_code == 200
    resp = r.json()
    assert "id" in resp
    assert resp["id"] == link_id
    assert "href" in resp
    assert resp["href"] == "https://www.smartvideos.ru/"
    assert "private" in resp
    assert resp["private"] is True
    assert "tags" in resp
    assert resp["tags"] == []


@pytest.mark.parametrize("payload", [{"private": False}])
def test_update_link(payload):
    r = client.post(f"{URL}/links", json=PAYLOAD)
    assert r.status_code == 201
    resp = r.json()
    assert "id" in resp

    link_id = resp["id"]

    r = client.put(f"{URL}/links/{link_id}", json=payload)
    assert r.status_code == 200

    resp = r.json()
    assert "href" in resp
    assert resp["href"] == "https://www.smartvideos.ru/"
    assert "private" in resp
    assert resp["private"] is False
    assert "tags" in resp
    assert resp["tags"] == []


def test_delete_link():
    r = client.post(f"{URL}/links", json=PAYLOAD)
    assert r.status_code == 201
    resp = r.json()
    assert "id" in resp

    link_id = resp["id"]

    r = client.delete(f"{URL}/links/{link_id}")
    assert r.status_code == 200
