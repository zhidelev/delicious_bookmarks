from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


URL = "http://127.0.0.1:8000"
PAYLOAD = {"href": "https://www.smartvideos.ru/", "tags": [], "private": True}


LINK_ONLY_PAYLOAD = {"href": "https://www.smartvideosrvjkb.ru/"}
PRIVATE_TRUE_PAYLOAD = {"href": "https://www.smartvideos.ru/", "tags": [], "private": True}
TAGS_PAYLOAD = {"href": "https://www.smartvideosrbvjkerbv.ru/", "tags": ["travel", "video"], "private": False}
PRIVATE_FALSE_PAYLOAD = {"href": "https://www.smartvideosjrekbvjkr.ru/", "private": False}


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


@pytest.mark.parametrize(
    "payload",
    [LINK_ONLY_PAYLOAD, PRIVATE_TRUE_PAYLOAD, TAGS_PAYLOAD, PRIVATE_FALSE_PAYLOAD],
    ids=["link only", "private", "tags", "not private"],
)
def test_create_link(payload):
    r = client.post(f"{URL}/links", json=payload)
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


@pytest.mark.parametrize("link_id", [1, "string"], ids=["int", "str"])
def test_get_link_invalid_type(link_id):
    r = client.get(f"{URL}/links/{link_id}")
    assert r.status_code == 422


def test_get_link_not_found():
    r = client.get(f"{URL}/links/29fa097f-ab2f-4ada-9a4a-c9177574db19")
    assert r.status_code == 404


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
