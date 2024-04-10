from typing import Annotated, List, Union
from urllib.parse import urlsplit

from fastapi import Depends, FastAPI, Path, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import InterfaceError

from . import crud, models, schemas
from .database import SessionLocal, engine
from .tag import Tags

try:
    models.Base.metadata.create_all(bind=engine)
except InterfaceError:
    pass


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_root():
    return {"Hello": "world!"}


@app.get("/bookmarks/{b_id}", tags=[Tags.bookmarks])
def get_bookmark(b_id: Annotated[int, Path(title="The ID of the bookmark to get.", ge=1)]):
    return {"id": b_id, "bookmark": dict()}


@app.get("/bookmarks", response_model=List[schemas.BookmarkOut])
def get_all_bookmarks(db: Session = Depends(get_db)) -> Union[List[schemas.BookmarkOut], List[dict]]:
    return crud.all_bookmarks(db)


@app.post("/bookmarks/", response_model=schemas.BookmarkOut)
def create_bookmark(bookmark: schemas.BookmarkIn, db: Session = Depends(get_db)):
    parsed_url = urlsplit(str(bookmark.uri))
    if parsed_url.netloc == "":
        raise HTTPException(status_code=400, detail="Invalid URL")
    return crud.create_bookmark(db, bookmark)
