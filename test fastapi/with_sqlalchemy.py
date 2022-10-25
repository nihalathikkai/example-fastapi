from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)


# creating a pydantic data structure for posts
class Post(BaseModel):  
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


# initialising FastAPI object
app = FastAPI()


@app.get("/")
def root():
    print("root")
    return {"message": "Welcome to FastAPI"}


@app.get("/sqlalchemy")
def test_sqlalchemy(db: Session = Depends(get_db)):
    res = db.query(models.Post).all()
    return {"status": res}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(data: Post, db: Session = Depends(get_db)):
    print("create_post")
    res = models.Post(**data.dict())
    db.add(res)
    db.commit()
    db.refresh(res)       
    return {"data": res}


@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    print("get_all_posts")
    res = db.query(models.Post).all()
    return {"data": res}


@app.get("/posts/latest")
def get_latest_post(db: Session = Depends(get_db)):
    print("get_latest_post")
    res = db.query(models.Post).filter(models.Post.id == db.query(func.max(models.Post.id)).scalar_subquery()).first()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No posts found")
    return {"data": res}


@app.get("/posts/{id}")
def get_one_post(id: int, db: Session = Depends(get_db)):
    print("get_one_post")
    res = db.query(models.Post).filter(models.Post.id == id).first()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"data": res}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    print("delete_post")
    query = db.query(models.Post).filter(models.Post.id == id)
    res = query.first()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_posts(id: int, data: Post, db: Session = Depends(get_db)):
    print("update_post")
    query = db.query(models.Post).filter(models.Post.id == id)
    res = query.first()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    query.update(data.dict(), synchronize_session=False)
    db.commit()
    res = query.first()
    return {"data": res}