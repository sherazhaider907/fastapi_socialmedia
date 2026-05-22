from typing import Optional

from fastapi import FastAPI 
from fastapi import Body
from pydantic import BaseModel

from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "post 1", "content": "content of post 1", "published": True, "rating": 5, "id": 1},
            {"title": "post 2", "content": "content of post 2", "published": False, "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        


@app.get("/")
async def root():
    return {"message": "welcome to fastapi"}

@app.get("/posts")
async def get_posts():
    return {"data":my_posts}


@app.post("/posts")
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    return {"post_detail": post}