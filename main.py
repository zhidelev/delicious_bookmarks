from uuid import uuid4
from pydantic import UUID4

from fastapi import FastAPI, status, Path
from requests.models import requote_uri

from models import Link, LinkUpdate

app = FastAPI()

links = []


@app.get("/links")
def get_links():
    return {"links": links}


@app.post("/links", status_code=status.HTTP_201_CREATED)
def create_link(link: Link):
    bookmark = dict(link)
    bookmark["id"] = str(uuid4())
    links.append(bookmark)
    return {"id": bookmark["id"]}


@app.get("/links/{link_id}")
def get_link_by_id(link_id: UUID4 = Path(..., title="UUID4 of the Bookmark")):
    # TODO: how to fix error in tests?
    link = [i for i in links if i["id"] == link_id]
    if len(link) > 0:
        return link[0]
    return {}


@app.put("/links/{link_id}")
def update_link(*, link_id: UUID4 = Path(..., title="UUID4 of the Bookmark"), link_update: LinkUpdate):
    link = [i for i in links if i["id"] == link_id][0]
    for k, v in dict(link_update).items():
        if v is not None:
            link[k] = v
    return link


@app.delete("/links/{link_id}")
def delete_link(*, link_id: UUID4 = Path(..., title="UUID4 of the Bookmark")):
    link = [i for i in links if i["id"] == link_id][0]
    links.remove(link)
