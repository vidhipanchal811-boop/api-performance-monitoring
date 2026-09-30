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

    assert len(users) == 2
    assert users[0]["name"] == "Alice"


def test_get_user():
    response = client.get("/users/5")

    assert response.status_code == 200

    user = response.json()

    assert user["id"] == 5