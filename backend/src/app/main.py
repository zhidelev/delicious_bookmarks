from typing import Annotated, List, Union
from urllib.parse import urlsplit

from fastapi import Depends, FastAPI, Path
from fastapi.responses import JSONResponse
from sqlalchemy.exc import InterfaceError
from sqlalchemy.orm import Session

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


@app.get("/bookmarks/{b_id}", tags=[Tags.bookmarks], responses={404: {"description": "Bookmark not found"}})
def get_bookmark(
    b_id: Annotated[int, Path(title="The ID of the bookmark to get.", ge=1)], db: Session = Depends(get_db)
):
    result = crud.get_bookmark(db, b_id)
    if result is None:
        return JSONResponse(status_code=404, content={"message": "Bookmark not found"})
    return result


@app.get("/bookmarks", tags=[Tags.bookmarks], response_model=List[schemas.BookmarkOut])
def get_all_bookmarks(db: Session = Depends(get_db)) -> Union[List[schemas.BookmarkOut], List[dict]]:
    return crud.all_bookmarks(db)


@app.post(
    "/bookmarks/",
    tags=[Tags.bookmarks],
    response_model=schemas.BookmarkOut,
    responses={400: {"description": "Invalid URL"}},
)
def create_bookmark(bookmark: schemas.BookmarkIn, db: Session = Depends(get_db)):
    parsed_url = urlsplit(str(bookmark.uri))
    if parsed_url.netloc == "":
        return JSONResponse(status_code=400, content={"message": "Invalid URL"})
    result = crud.create_bookmark(db, bookmark)
    if result is None:
        return JSONResponse(status_code=400, content={"message": "Invalid URL"})
    return result
