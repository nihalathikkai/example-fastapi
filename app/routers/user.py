from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from ..oauth2 import get_current_user

print("file: user")

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    print("create_user")
    post = db.query(models.User).filter(models.User.email == data.email).first()
    if  post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"email already excists")
    data.password = utils.get_password_hash(data.password)
    user = models.User(**data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_model=schemas.UserDetails)
def get_curr_user_details(current_user: models.User = Depends(get_current_user)):
    print("get_curr_user_details")
    return current_user
    


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    print("get_user")
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    return user