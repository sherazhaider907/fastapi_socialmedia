import uuid
from app import schemas
from .database import client , session
import pytest
from app.config import settings
from jose import jwt

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


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": test_user["email"],  
            "password": test_user["password"] 
        }
    )

    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, settings.algorithm)
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200
