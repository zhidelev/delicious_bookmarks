from pydantic import AnyUrl, BaseModel, ConfigDict, Field


class BookmarkId(BaseModel):
    id: int


class BookmarkIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uri: AnyUrl = Field(
        title="The URI of the bookmark to get.",
        strict=True,
    )
    title: str = Field(default="", title="The title of the bookmark.", min_length=0)
    description: str = Field(default="", title="The description of the bookmark.", min_length=0)


class BookmarkOut(BookmarkIn):
    id: int
