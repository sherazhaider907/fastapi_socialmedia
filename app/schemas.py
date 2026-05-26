# Define data model for request body (Post structure)
from pydantic import BaseModel
from datetime import datetime



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at: datetime

    class Config:
        from_attributes = True