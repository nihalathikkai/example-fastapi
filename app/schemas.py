from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator

print("file: schemas")

# Authentication

class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
    
# Users
class UserBase(BaseModel):
    email: EmailStr
    password: str
    

class UserCreate(UserBase):
    name: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    dob: Optional[datetime] = None


class UserDetails(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    dob: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        orm_mode = True
    

class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
    
# Posts
class PostBase(BaseModel):
    title: str
    content: str
    publish: bool = True
    
    
class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    publish: Optional[bool] = None
    
    
class PostOut(PostBase):   
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    class Config:
        orm_mode = True
        

class PostResponse(BaseModel): 
    Post: PostOut
    votes: int
    
    class Config:
        orm_mode = True


# Votes
class Vote(BaseModel):
    post_id: int
    dir: int
    
    @validator('dir')
    def prevent_zero(cls, v):
        if v not in (0,1): 
            raise ValueError('ensure this value is 0 or 1')
        return v
    
# class VoteResponse(Vote):
#     user_id: int
    
#     class Config:
#         orm_mode = True
        


    
    
