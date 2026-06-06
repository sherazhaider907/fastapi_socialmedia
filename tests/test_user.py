import uuid
from app import schemas
from .database import client , session


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
    