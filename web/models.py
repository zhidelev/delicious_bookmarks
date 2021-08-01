from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    hash_id = Column(String)
    href = Column(String)
    private = Column(Boolean, default=True)
    tags = Column(String, default="")
    deleted = Column(Boolean, default=False)
