import json
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from . import crud, models, schemas
from .crud import get_articles
from .database import SessionLocal, engine
from .models import Article, Tag

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/articles")
async def read_articles(db: Session = Depends(get_db)):
    """
    Get a list of articles.
    """
    articles = get_articles(db)
    return JSONResponse(content=[article.serialize() for article in articles])


# Article endpoints
@app.post("/articles/", response_model=Article)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@app.get("/articles/", response_model=List[Article])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = db.query(Article).offset(skip).limit(limit).all()
    return articles


@app.get("/articles/{article_id}", response_model=Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article


@app.put("/articles/{article_id}", response_model=Article)
def update_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    for field, value in article:
        setattr(db_article, field, value)
    db.commit()
    db.refresh(db_article)
    return db_article


@app.delete("/articles/{article_id}", response_model=Article)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return db_article


# Tag endpoints
@app.post("/tags/", response_model=Tag)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@app.get("/tags/", response_model=List[Tag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return tags


@app.get("/tags/{tag_id}", response_model=Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@app.put("/tags/{tag_id}", response_model=Tag)
def update_tag(tag_id: int, tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

@router.post("/images/upload/", response_model=str)
def upload_image(file: UploadFile = File(...)):
    """
    Uploads an image file to the static directory and returns the filename.
    """
    file_location = os.path.join(settings.STATIC_DIR, file.filename)
    with open(file_location, "wb") as image:
        content = file.file.read()
        image.write(content)
    return file.filename


@router.put("/images/{filename}", response_model=str)
def update_image(filename: str, file: UploadFile = File(...)):
    """
    Updates an existing image file in the static directory and returns the filename.
    """
    file_location = os.path.join(settings.STATIC_DIR, filename)
    if not os.path.isfile(file_location):
        raise HTTPException(status_code=404, detail="Image not found")
    with open(file_location, "wb") as image:
        content = file.file.read()
        image.write(content)
    return filename


@router.delete("/images/{filename}", response_model=str)
def delete_image(filename: str):
    """
    Deletes an existing image file in the static directory and returns the filename.
    """
    file_location = os.path.join(settings.STATIC_DIR, filename)
    if not os.path.isfile(file_location):
        raise HTTPException(status_code=404, detail="Image not found")
    os.remove(file_location)
    return filename