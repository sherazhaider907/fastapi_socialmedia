from typing import Annotated, List

from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models, schemas , utils
from .database import engine, get_db



# Create tables
models.Base.metadata.create_all(bind=engine)

# App instance
app = FastAPI()

# DB dependency shortcut
db_dependency = Annotated[Session, Depends(get_db)]




# Root route
@app.get("/")
async def root():
    return {"message": "welcome to fastapi"}


# Get all posts
@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: db_dependency):
    return db.query(models.Post).all()


# Create post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: db_dependency):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get single post
@app.get("/posts/{id}", response_model=schemas.Post)
async def get_post(id: int, db: db_dependency):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    return post


# Delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: db_dependency):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update post
@app.put("/posts/{id}", response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db: db_dependency):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()



# create user
@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: db_dependency):

    # Hash the password before saving to database
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user