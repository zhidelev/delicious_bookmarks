from pydantic import BaseModel, Field, AnyUrl


class BookmarkId(BaseModel):
    id: int


class BookmarkIn(BaseModel):
    uri: AnyUrl = Field(
        title="The URI of the bookmark to get.",
        strict=True,
    )
    title: str = Field(default="", title="The title of the bookmark.", min_length=0)
    description: str = Field(default="", title="The description of the bookmark.", min_length=0)

    class Config:
        from_attributes = True


class BookmarkOut(BookmarkIn):
    id: int
