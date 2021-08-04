from typing import List, Optional, Set

from pydantic import BaseModel, Field, HttpUrl


class LinkBase(BaseModel):
    href: HttpUrl = Field(..., example="https://www.example.com/")
    private: Optional[bool] = True
    tags: Optional[List[str]] = []


class LinkUpdate(LinkBase):
    href: Optional[HttpUrl] = Field(..., example="https://www.example.com/")
    private: Optional[bool]
    tags: Optional[Set[str]] = set()


class Link(LinkBase):
    pass

    class Config:
        orm_mode = True
