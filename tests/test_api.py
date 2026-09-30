from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "API Performance Monitoring System is running"
    )


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_users():
    response = client.get("/users")

    assert response.status_code == 200

    users = response.json()

    assert len(users) >= 2
    assert users[0]["name"] == "Alice"


def test_get_user():
    response = client.get("/users/1")

    assert response.status_code == 200

    user = response.json()

    assert user["id"] == 1
    assert user["name"] == "Alice"


def test_get_nonexistent_user():
    response = client.get("/users/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user():
    response = client.post(
        "/users",
        json={
            "name": "Charlie",
            "email": "charlie@example.com"
        }
    )

    assert response.status_code == 201

    user = response.json()

    assert user["name"] == "Charlie"
    assert user["email"] == "charlie@example.com"
    assert "id" in user


def test_create_user_invalid_email():
    response = client.post(
        "/users",
        json={
            "name": "Invalid User",
            "email": "not-an-email"
        }
    )

    assert response.status_code == 422


def test_update_user():
    response = client.put(
        "/users/1",
        json={
            "name": "Alice Updated",
            "email": "alice.updated@example.com"
        }
    )

    assert response.status_code == 200

    user = response.json()

    assert user["id"] == 1
    assert user["name"] == "Alice Updated"


def test_update_nonexistent_user():
    response = client.put(
        "/users/9999",
        json={
            "name": "Nobody",
            "email": "nobody@example.com"
        }
    )

    assert response.status_code == 404


def test_delete_user():
    response = client.delete("/users/2")

    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"


def test_delete_nonexistent_user():
    response = client.delete("/users/9999")

    assert response.status_code == 404