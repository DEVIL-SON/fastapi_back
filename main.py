from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from databases import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)


BOOKS = []


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Users
    ).all()


@app.post("/")
def create_book(user: Book, db: Session = Depends(get_db)):

    user_model = models.Users
    ()
    user_model.title = user.title
    user_model.author = user.author
    user_model.description = user.description
    user_model.rating = user.rating

    db.add(user_model)
    db.commit()

    return user


@app.put("/{user_id}")
def update_book(user_id: int, user: Book, db: Session = Depends(get_db)):

    user_model = db.query(models.Users
    ).filter(models.Users
    .id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    user_model.title = user.title
    user_model.author = user.author
    user_model.description = user.description
    user_model.rating = user.rating

    db.add(user_model)
    db.commit()

    return user


@app.delete("/{user_id}")
def delete_book(user_id: int, db: Session = Depends(get_db)):

    user_model = db.query(models.Users
    ).filter(models.Users
    .id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    db.query(models.Users
    ).filter(models.Users
    .id == user_id).delete()

    db.commit()