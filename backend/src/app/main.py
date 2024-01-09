from typing import Annotated, List, Union

from fastapi import FastAPI, Path
from pydantic import BaseModel, HttpUrl

from .tag import Tags


class BookmarkId(BaseModel):
    id: int


class BookmarkIn(BaseModel):
    uri: HttpUrl
    description: Union[str, None] = None
    tags: Union[List[str], None] = None


class BookmarkOut(BookmarkIn):
    id: int


app = FastAPI()

bookmarks: List[BookmarkIn] = []


@app.get("/")
def get_root():
    return {"Hello": "world!"}


@app.get("/bookmarks/{b_id}", tags=[Tags.bookmarks])
def get_bookmark(b_id: Annotated[int, Path(title="The ID of the bookmark to get.", ge=1)]):
    return {"id": b_id, "bookmark": dict()}


@app.get("/bookmarks", tags=[Tags.bookmarks], response_model=List[BookmarkOut])
def get_all_bookmarks() -> Union[List[BookmarkOut], List[None]]:
    return [BookmarkOut(id=i + 1, uri=bookmarks[i].uri) for i in range(len(bookmarks))]


@app.post("/bookmarks/", tags=[Tags.bookmarks], response_model=BookmarkId)
def create_bookmark(bookmark: BookmarkIn) -> BookmarkId:
    bookmarks.append(bookmark)
    return BookmarkId(id=len(bookmarks))
