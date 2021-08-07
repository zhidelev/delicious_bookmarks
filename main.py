from typing import List, Optional
from uuid import uuid4
from pydantic import UUID4

from fastapi import FastAPI, status, Path, Body, Header, Response
from requests.models import requote_uri

from models import Link, LinkOut, LinkUpdate
from threading import Lock

app = FastAPI()

links = {}

lock = Lock()


@app.get("/links")
def get_links():
    return {"links": [{**{"id": key}, **value} for key, value in links.items()]}


@app.post("/links", status_code=status.HTTP_201_CREATED, response_model=LinkOut)
def create_link(
    link: Link = Body(..., example={"href": "https://example.com", "tags": [], "private": True}),
    content_type: Optional[str] = Header("application/json"),
):
    if content_type == "application/json":
        bookmark = link.dict()
        bookmark_id = str(uuid4())
        with lock:
            links[bookmark_id] = bookmark
        return LinkOut(**{"id": bookmark_id})


@app.get("/links/{link_id}", response_model=LinkUpdate)
def get_link_by_id(response: Response, link_id: UUID4 = Path(..., title="UUID4 of the Bookmark")):
    # TODO: how to fix error in tests?
    # print(links)
    if str(link_id) not in links.keys():
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    return {**{"id": str(link_id)}, **links[str(link_id)]}


@app.put("/links/{link_id}")
def update_link(
    *,
    link_id: UUID4 = Path(..., title="UUID4 of the Bookmark"),
    link_update: LinkUpdate = Body(
        ..., example={"href": "https://example.com", "tags": ["cool", "future"], "private": False}
    )
):
    with lock:
        link = links[str(link_id)]
        for k, v in dict(link_update).items():
            if v is not None:
                link[k] = v
    return link


@app.delete("/links/{link_id}")
def delete_link(*, link_id: UUID4 = Path(..., title="UUID4 of the Bookmark")):
    with lock:
        del links[str(link_id)]
