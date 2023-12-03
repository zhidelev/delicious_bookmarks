from fastapi import FastAPI, Path
from pydantic import BaseModel, HttpUrl
from typing import List, Union
from .tag import Tags
import json


class BookmarkId(BaseModel):
    id: int


class BookmarkIn(BaseModel):
    uri: HttpUrl
    description: Union[str, None] = None
    tags: Union[List[str], None] = None


class BookmarkOut(BookmarkIn):
    id: int


app = FastAPI()

bookmarks = []


@app.get("/")
def get_root():
    return {"Hello": "world!"}


@app.get("/bookmarks/{b_id}", tags=[Tags.bookmarks])
def get_bookmark(b_id: int = Path(title="The ID of the bookmark to get.", ge=1)):
    return {"id": b_id, "bookmark": dict()}


@app.get("/bookmarks/", tags=[Tags.bookmarks])
def get_all_bookmarks() -> Union[List[BookmarkOut], List[None]]:
    if bookmarks:
        return [bookmark for bookmark in bookmarks]
    return []


@app.post("/bookmarks/", tags=[Tags.bookmarks])
def create_bookmark(bookmark: BookmarkIn) -> BookmarkId:
    return {"id": 1}
