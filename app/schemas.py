# Define data model for request body (Post structure)
from typing import Annotated
from pydantic import BaseModel, EmailStr , Field
from datetime import datetime
from typing import Optional

# post schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

# user schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

    
# login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# token schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


# vote schema
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)] # direction of the vote, 0 for downvote and 1 for upvote