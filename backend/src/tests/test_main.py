import os
from http import HTTPStatus
from urllib.parse import urlsplit

import pytest
from fastapi.testclient import TestClient
from httpx import InvalidURL
from hypothesis import given
from hypothesis import provisional as pt
from hypothesis import settings
from hypothesis import strategies as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import httpx

from app import models
from app.main import app, get_db

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


# For local development
SQLALCHEMY_SCHEMA = os.getenv("SQLALCHEMY_SCHEMA", "postgresql+pg8000")
DB_USER = os.getenv("DB_USER", "user")
DB_HOST = os.getenv("DB_HOST", "host")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME", "name")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

POOL_SIZE = os.getenv("POOL_SIZE", 10)
MAX_OVERFLOW = os.getenv("MAX_OVERFLOW", 20)

SQLALCHEMY_DATABASE_URL = f"{SQLALCHEMY_SCHEMA}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


models.Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

print(f"Deps: {app.dependency_overrides}")


@pytest.fixture(scope="module")
def test_client():
    yield TestClient(app)


def test_get_root(test_client):
    response = test_client.get("/")
    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == {"Hello": "world!"}


@settings(max_examples=500)
@given(b_id=st.one_of(st.integers().filter(lambda x: x <= 0), st.text(min_size=1), st.none(), st.booleans()))
def test_get_by_id(test_client, b_id):
    try:
        if isinstance(b_id, (bool, type(None))):
            raise ValueError
        if int(b_id) <= 0:
            raise ValueError
    except ValueError:
        try:
            response = test_client.get(f"/bookmarks/{b_id}", follow_redirects=False)
            if b_id == ".":
                assert response.status_code == HTTPStatus.OK.value
            else:
                assert response.status_code in [
                    HTTPStatus.UNPROCESSABLE_ENTITY.value,
                    HTTPStatus.TEMPORARY_REDIRECT.value,
                    HTTPStatus.NOT_FOUND.value,
                ]
        except InvalidURL:
            pass
    else:
        response = test_client.get(f"/bookmarks/{b_id}")
        assert response.status_code in [HTTPStatus.OK.value, HTTPStatus.NOT_FOUND.value]


def test_get_all_bookmarks(test_client):
    response = test_client.get("/bookmarks")
    assert response.status_code == HTTPStatus.OK.value
    assert isinstance(response.json(), list)


def test_get_all_bookmarks_not_empty(test_client):
    test_client.post("/bookmarks/", json={"uri": "https://test.com"})
    response = test_client.get("/bookmarks")
    assert response.status_code == HTTPStatus.OK.value
    assert len(response.json()) > 0


@settings(max_examples=150)
@given(uri=st.one_of(st.text(), pt.urls()))
def test_create_bookmark(test_client, uri):
    parsed = ""
    try:
        parsed = urlsplit(str(uri))
    except ValueError:
        response = test_client.post("/bookmarks/", json={"uri": uri})
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value
    else:
        response = test_client.post("/bookmarks/", json={"uri": uri})
        if parsed.netloc:
            assert response.status_code == HTTPStatus.OK.value
            assert "id" in response.json()
            assert isinstance(response.json()["id"], int)
        else:
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value


@given(b_id=st.one_of(st.text(), pt.urls(), st.integers()))
def test_delete_bookmark(test_client, b_id):
    try:
        response = test_client.delete(f"/bookmarks/{b_id}")
        assert response.status_code in [
            HTTPStatus.OK.value,
            HTTPStatus.NOT_FOUND.value,
            HTTPStatus.METHOD_NOT_ALLOWED.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        ]
    except httpx.InvalidURL:
        pass
