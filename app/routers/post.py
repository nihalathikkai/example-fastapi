from typing import List, Optional
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas
from ..oauth2 import get_current_user
from ..database import get_db

print("file: post")

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(data: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    print("create_post")
    post = models.Post(owner_id=current_user.id, **data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)       
    return post


@router.get("/", response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print("get_all_posts")
    post = db.query(models.Post, func.count(models.Vote.user_id).label('votes')) \
            .join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True) \
            .filter(models.Post.title.contains(search)) \
            .group_by(models.Post.id) \
            .offset(skip).limit(limit) \
            .all()
    return post


@router.get("/latest", response_model= schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    print("get_latest_post")
    post = db.query(models.Post, func.count(models.Vote.user_id).label('votes')) \
            .join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True) \
            .filter(models.Post.id == db.query(func.max(models.Post.id)).scalar_subquery()) \
            .group_by(models.Post.id) \
            .first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No posts found")
    return post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_one_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    print("get_one_post")
    post = db.query(models.Post, func.count(models.Vote.user_id).label('votes')) \
            .join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True) \
            .filter(models.Post.id == id) \
            .group_by(models.Post.id) \
            .first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    print("delete_post")
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostOut)
def update_posts(id: int, data: schemas.PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    print("update_post")
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
        
    data = {k:v for k,v in data.dict().items() if v}
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"error in data sent")
    query.update(data, synchronize_session=False)
    db.commit()
    post = query.first()
    return post