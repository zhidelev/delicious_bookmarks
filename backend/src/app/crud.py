from sqlalchemy.orm import Session

from . import models, schemas


def create_bookmark(db: Session, bookmark: schemas.BookmarkIn):
    db_bookmark = models.Bookmark(uri=bookmark.uri, title=bookmark.title, description=bookmark.description)
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark


def all_bookmarks(db: Session):
    return db.query(models.Bookmark).all()
