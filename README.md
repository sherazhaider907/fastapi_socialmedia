# FastAPI Social Media API

A REST API for a social media platform built with FastAPI and PostgreSQL.

## Features
- User registration and login with JWT authentication
- Create, read, update, and delete posts
- Vote/unvote on posts
- Search and pagination for posts

## Tech Stack
- Python, FastAPI, PostgreSQL
- SQLAlchemy ORM, Alembic (migrations)
- JWT Authentication, Pydantic, Uvicorn

## Setup

### 1. Clone the repo
git clone https://github.com/SherazHaider907/fastapi_socialmedia.git
cd fastapi_socialmedia

### 2. Install dependencies
pip install -r requirements.txt

### 3. Create a .env file
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_db
DATABASE_USERNAME=your_user
DATABASE_PASSWORD=your_password
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

### 4. Run migrations
alembic upgrade head

### 5. Start the server
uvicorn app.main:app --reload

## API Docs
Visit http://localhost:8000/docs for interactive Swagger documentation.