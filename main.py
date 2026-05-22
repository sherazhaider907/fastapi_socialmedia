from typing import Optional

from fastapi import FastAPI 
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "welcome to fastapi"}

@app.get("/posts")
async def get_posts():
    return {"data": "This is your posts"}


@app.post("/create")
async def create_post(post: Post):
    print(post)
    return {"data":"new post"}