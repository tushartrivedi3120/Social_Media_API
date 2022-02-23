from datetime import datetime
import email
from lib2to3.pytree import Base
from click import Option
from pydantic import BaseModel , EmailStr, conint
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email:EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None

    
class Post(PostBase):
    id:int
    created_at: datetime
    user_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)
    
class PostOut(BaseModel):
    Post: Post
    votes:int
    class Config:
        orm_mode = True

