from typing import List, Optional, Set

from pydantic import BaseModel, Field, HttpUrl, UUID4

# Refactor all models for better representaion!
# https://fastapi.tiangolo.com/tutorial/extra-models/


class LinkBase(BaseModel):
    href: HttpUrl = Field(..., example="https://www.example.com/")
    private: Optional[bool] = True
    tags: Optional[List[str]] = []


class LinkOut(BaseModel):
    id: UUID4


class LinkUpdate(BaseModel):
    href: Optional[HttpUrl] = Field(example="https://www.example.com/")
    private: Optional[bool]
    tags: Optional[Set[str]] = set()
    id: Optional[UUID4]


class Link(LinkBase):
    pass

    class Config:
        orm_mode = True
