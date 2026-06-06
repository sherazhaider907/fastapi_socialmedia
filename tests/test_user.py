import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

#################################################################################



@pytest.fixture
def client():
    # run this code before we run our tests
    Base.metadata.drop_all(bind=engine)
    # run this code after we run our tests
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

    


def test_root(client):
    response = client.get("/")
    print(response.json().get("message"))
    assert response.json().get("message") == "welcome to fastapi"
    assert response.status_code == 200

def test_create_user(client):
    random_email = f"{uuid.uuid4()}@example.com"
    response = client.post(
        "/users/",
        json={
            "email": random_email,
            "password": "password123"
        }
    )
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == random_email
    assert response.status_code == 201
    