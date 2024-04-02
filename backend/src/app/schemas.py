from pydantic import BaseModel
from typing import List, Union


class BookmarkId(BaseModel):
    id: int


class BookmarkIn(BaseModel):
    uri: str
    title: str
    description: str = ""

    class Config:
        from_attributes = True


class BookmarkOut(BookmarkIn):
    id: int
