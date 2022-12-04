from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union


class Bookmark(BaseModel):
    uri: str
    description: Union[str, None] = None


app = FastAPI()


@app.get("/")
def get_root():
    return {"Hello, world!"}


@app.get("/bookmarks/{b_id}")
def get_bookmark(b_id: int):
    return {"bookmark": b_id}


@app.post("/bookmarks/")
def create_bookmark(bookmark: Bookmark):
    return bookmark
