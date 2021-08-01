from typing import Optional, List
from uuid import uuid4

from fastapi import FastAPI, status

# from pydantic import BaseModel

from .schema import Link, LinkUpdate


app = FastAPI()

links = []


@app.get("/links")
def get_links():
    return {"links": links}


@app.post("/links", status_code=status.HTTP_201_CREATED)
def create_link(link: Link):
    l = dict(link)
    l["id"] = str(uuid4())
    links.append(l)
    return {"id": l["id"]}


@app.get("/links/{link_id}")
def get_link_by_id(link_id):
    link = [i for i in links if i["id"] == link_id]

    return link[0]


@app.put("/links/{link_id}")
def update_link(link_id, link_update: LinkUpdate):
    link = [i for i in links if i["id"] == link_id][0]
    for k, v in dict(link_update).items():
        if v is not None:
            link[k] = v
    return link


@app.delete("/links/{link_id}")
def delete_link(link_id):
    link = [i for i in links if i["id"] == link_id][0]
    links.remove(link)
