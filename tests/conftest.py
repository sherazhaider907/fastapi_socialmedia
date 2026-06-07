from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
import uuid
from app.config import settings
from app.database import get_db
from app.database import Base
from app import models, oauth2
import pytest

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
        "email": f"{uuid.uuid4()}@example.com",
        "password": "password123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": f"{uuid.uuid4()}@example.com",
        "password": "password123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return oauth2.create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    original_headers = dict(client.headers)
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    yield client
    client.headers = original_headers


@pytest.fixture
def test_posts(test_user, session):
    posts = [
        models.Post(title="First post",  content="First content",  owner_id=test_user["id"]),
        models.Post(title="Second post", content="Second content", owner_id=test_user["id"]),
        models.Post(title="Third post",  content="Third content",  owner_id=test_user["id"]),
    ]
    session.add_all(posts)
    session.commit()
    return [{"id": p.id, "title": p.title, "content": p.content} for p in posts]


@pytest.fixture
def test_vote(authorized_client, test_posts):
    response = authorized_client.post(
        "/vote/",
        json={"post_id": test_posts[0]["id"], "dir": 1}
    )
    assert response.status_code == 201

