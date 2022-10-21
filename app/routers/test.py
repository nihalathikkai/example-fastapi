from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..oauth2 import get_current_user


router = APIRouter(prefix='/tests', tags=['test'])

@router.get("/sqlalchemy", response_model=schemas.PostResponse)
def test_sqlalchemy(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    print("test_sqlalchemy")
    post = db.query(models.Post).first()
    return post