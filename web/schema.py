from typing import Optional, List

from pydantic import BaseModel


class LinkBase(BaseModel):
    href: str
    private: Optional[bool] = True
    tags: Optional[List[str]] = []


class LinkUpdate(LinkBase):
    href: Optional[str]
    private: Optional[bool]
    tags: Optional[List[str]]


class Link(LinkBase):
    pass

    class Config:
        orm_mode = True
