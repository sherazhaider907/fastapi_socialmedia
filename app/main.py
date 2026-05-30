from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user , auth

# Create tables
models.Base.metadata.create_all(bind=engine)

# App instance
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# Root route
@app.get("/")
async def root():
    return {"message": "welcome to fastapi"}





