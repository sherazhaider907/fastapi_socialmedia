from typing import Annotated, Optional

from fastapi import FastAPI, Response, status, HTTPException , Depends # Depends is for dependency injection (like getting DB session)
from fastapi import Body
from pydantic import BaseModel

from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine , get_db
from sqlalchemy.orm import Session # This is for SQLAlchemy session management


models.Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI()

db_dependency = Annotated[Session, Depends(get_db)]




# Define data model for request body (Post structure)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Keep trying to connect to PostgreSQL database until successful
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres', 
            password='admin', 
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break

    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(2)


# Sample in-memory posts (not used in DB operations here)
my_posts = [
    {"title": "post 1", "content": "content of post 1", "published": True, "rating": 5, "id": 1},
    {"title": "post 2", "content": "content of post 2", "published": False, "id": 2}
]


# Find a post by ID from in-memory list
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


# Find index of a post in in-memory list
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


# Root route (home page)
@app.get("/")
async def root():
    return {"message": "welcome to fastapi"}


@app.get("/sqlalchemy")
def test_posts(db: db_dependency):
    posts =  db.query(models.Post).all()
    return {"data": posts}


# Get all posts from PostgreSQL database
@app.get("/posts")
async def get_posts(db: db_dependency):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


# Create a new post in database
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post , db: db_dependency):
    # cursor.execute(
    #     """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict()) # This is a more concise way to create a new Post instance using the data from the Pydantic model
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


# Get a single post by ID
@app.get("/posts/{id}")
async def get_post(id: int, db: db_dependency):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    return {"post_detail": post}


# Delete a post by ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: db_dependency):

    post = db.query(models.Post).filter(models.Post.id == id)


    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post by ID
@app.put("/posts/{id}")
async def update_post(id: int, updated_post: Post, db: db_dependency):
    # cursor.execute(
    #     """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #     (post.title, post.content, post.published, str(id))
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query= db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}