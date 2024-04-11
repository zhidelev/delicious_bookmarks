from sqlalchemy import Column, Integer, String

from .database import Base


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    uri = Column(String)
    title = Column(String)
    description = Column(String)
