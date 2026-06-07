import pytest
from app import schemas
from app import oauth2


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def token(test_user):
    return oauth2.create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session):
    from app import models
    posts = [
        models.Post(title="First post",  content="First content",  owner_id=test_user["id"]),
        models.Post(title="Second post", content="Second content", owner_id=test_user["id"]),
        models.Post(title="Third post",  content="Third content",  owner_id=test_user["id"]),
    ]
    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()


# ── GET /posts ─────────────────────────────────────────────────────────────────

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)


def test_get_all_posts_unauthorized(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


# ── GET /posts/{id} ────────────────────────────────────────────────────────────

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title


def test_get_one_post_not_found(authorized_client):
    response = authorized_client.get("/posts/99999")
    assert response.status_code == 404


def test_get_one_post_unauthorized(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


# ── POST /posts ────────────────────────────────────────────────────────────────

def test_create_post(authorized_client):
    response = authorized_client.post(
        "/posts/",
        json={"title": "New post", "content": "New content", "published": True}
    )
    post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert post.title == "New post"
    assert post.content == "New content"
    assert post.published == True


def test_create_post_unauthorized(client):
    response = client.post(
        "/posts/",
        json={"title": "New post", "content": "New content", "published": True}
    )
    assert response.status_code == 401


def test_create_post_default_published(authorized_client):
    response = authorized_client.post(
        "/posts/",
        json={"title": "Default published", "content": "Some content"}
    )
    post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert post.published == True  # assuming default is True in your schema


# ── DELETE /posts/{id} ─────────────────────────────────────────────────────────

def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_delete_post_not_found(authorized_client):
    response = authorized_client.delete("/posts/99999")
    assert response.status_code == 404


def test_delete_post_unauthorized(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_delete_other_users_post(authorized_client, session, test_user2):
    from app import models
    other_post = models.Post(title="Other post", content="Other content", owner_id=test_user2["id"])
    session.add(other_post)
    session.commit()

    response = authorized_client.delete(f"/posts/{other_post.id}")
    assert response.status_code == 403


# ── PUT /posts/{id} ────────────────────────────────────────────────────────────

def test_update_post(authorized_client, test_posts):
    response = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json={"title": "Updated title", "content": "Updated content", "published": True}
    )
    post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert post.title == "Updated title"
    assert post.content == "Updated content"


def test_update_post_not_found(authorized_client):
    response = authorized_client.put(
        "/posts/99999",
        json={"title": "Updated title", "content": "Updated content", "published": True}
    )
    assert response.status_code == 404


def test_update_post_unauthorized(client, test_posts):
    response = client.put(
        f"/posts/{test_posts[0].id}",
        json={"title": "Updated title", "content": "Updated content", "published": True}
    )
    assert response.status_code == 401


def test_update_other_users_post(authorized_client, session, test_user2):
    from app import models
    other_post = models.Post(title="Other post", content="Other content", owner_id=test_user2["id"])
    session.add(other_post)
    session.commit()

    response = authorized_client.put(
        f"/posts/{other_post.id}",
        json={"title": "Hacked title", "content": "Hacked content", "published": True}
    )
    assert response.status_code == 403