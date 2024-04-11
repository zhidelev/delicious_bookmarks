from sqlalchemy.exc import MultipleResultsFound, NoResultFound, ProgrammingError
from sqlalchemy.orm import Session

from . import models, schemas


def create_bookmark(db: Session, bookmark: schemas.BookmarkIn):
    """
    Create a new bookmark in the database.

    Args:
        db (Session): The database session.
        bookmark (BookmarkIn): The bookmark data to be created.

    Returns:
        Optional[Bookmark]: The created bookmark if successful, None otherwise.
    """
    db_bookmark = models.Bookmark(uri=bookmark.uri, title=bookmark.title, description=bookmark.description)
    try:
        db.add(db_bookmark)
        db.commit()
        db.refresh(db_bookmark)
    except ProgrammingError:
        db.rollback()
        return None
    return db_bookmark


def all_bookmarks(db: Session):
    """
    Retrieve all bookmarks from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[Bookmark]: A list of all bookmarks in the database.
    """
    return db.query(models.Bookmark).all()


def get_bookmark(db: Session, b_id: int):
    """
    Get a bookmark from the database.

    Args:
        db (Session): The database session.
        b_id (int): The ID of the bookmark to retrieve.

    Returns:
        Bookmark: The retrieved bookmark object, or None if not found.
    """
    try:
        return db.query(models.Bookmark).filter(models.Bookmark.id == b_id).one()
    except MultipleResultsFound:
        return None
    except NoResultFound:
        return None
    except ProgrammingError:
        db.rollback()
        return None
