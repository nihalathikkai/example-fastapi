from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..oauth2 import get_current_user
from ..database import get_db


print("file: vote")

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(data: schemas.Vote , db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    print("vote")
    
    if not db.query(models.Post).filter(models.Post.id == data.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {data.post_id} was not found")
    
    query = db.query(models.Vote).filter(models.Vote.post_id == data.post_id, models.Vote.user_id == current_user.id)
    found_vote = query.first()
    
    if data.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {data.post_id}")
        new_vote = models.Vote(post_id = data.post_id, user_id = current_user.id)
        db.add(new_vote)
        message = "Succesfully added vote"
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {current_user.id} has not voted on post {data.post_id}")
        query.delete(synchronize_session=False)
        message = "Succesfully deleted vote"
    
    db.commit()
    return {"message": message}