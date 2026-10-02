import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class PerformanceTestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/test-performance":
            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                b'{"status": "ok"}'
            )

    def log_message(self, format, *args):
        return


def start_test_server():
    server = HTTPServer(
        ("127.0.0.1", 0),
        PerformanceTestHandler
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True
    )

    thread.start()

    port = server.server_address[1]

    return server, f"http://127.0.0.1:{port}/test-performance"


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "API Performance Monitoring System is running"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_get_users():
    response = client.get("/users")

    assert response.status_code == 200

    users = response.json()

    assert len(users) >= 2
    assert users[0]["name"] == "Alice"
    assert users[1]["name"] == "Bob"


def test_get_user():
    response = client.get("/users/1")

    assert response.status_code == 200

    user = response.json()

    assert user["id"] == 1
    assert user["name"] == "Alice"
    assert user["email"] == "alice@example.com"


def test_get_nonexistent_user():
    response = client.get("/users/999")

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


def test_invalid_email():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "invalid-email"
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
    assert user["email"] == "alice.updated@example.com"


def test_update_nonexistent_user():
    response = client.put(
        "/users/999",
        json={
            "name": "Nobody",
            "email": "nobody@example.com"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user():
    response = client.delete("/users/2")

    assert response.status_code == 200
    assert response.json() == {
        "message": "User deleted successfully"
    }


def test_delete_nonexistent_user():
    response = client.delete("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_performance_test():
    server, url = start_test_server()

    try:
        response = client.post(
            "/performance-test",
            json={
                "url": url,
                "number_of_requests": 3
            }
        )

        assert response.status_code == 200

        result = response.json()

        assert result["url"] == url
        assert result["total_requests"] == 3
        assert result["successful_requests"] == 3
        assert result["failed_requests"] == 0

        assert result["success_rate_percent"] == 100.0

        assert result["average_response_time_ms"] > 0
        assert result["minimum_response_time_ms"] > 0
        assert result["maximum_response_time_ms"] > 0

        assert result["maximum_response_time_ms"] >= (
            result["minimum_response_time_ms"]
        )

        assert result["p95_response_time_ms"] > 0
        assert result["p99_response_time_ms"] > 0

        assert result["p95_response_time_ms"] >= (
            result["minimum_response_time_ms"]
        )

        assert result["p99_response_time_ms"] >= (
            result["p95_response_time_ms"]
        )

        assert result["requests_per_second"] > 0
        assert result["total_test_time_seconds"] > 0

        assert len(result["results"]) == 3

    finally:
        server.shutdown()


def test_concurrent_performance_test():
    server, url = start_test_server()

    try:
        response = client.post(
            "/performance-test",
            json={
                "url": url,
                "number_of_requests": 3,
                "mode": "concurrent"
            }
        )

        assert response.status_code == 200

        result = response.json()

        assert result["total_requests"] == 3
        assert result["successful_requests"] == 3
        assert result["failed_requests"] == 0
        assert result["success_rate_percent"] == 100.0

        assert result["p95_response_time_ms"] > 0
        assert result["p99_response_time_ms"] > 0

        assert result["p95_response_time_ms"] >= (
            result["minimum_response_time_ms"]
        )

        assert result["p99_response_time_ms"] >= (
            result["p95_response_time_ms"]
        )

        assert len(result["results"]) == 3

    finally:
        server.shutdown()


def test_sequential_performance_test():
    server, url = start_test_server()

    try:
        response = client.post(
            "/performance-test",
            json={
                "url": url,
                "number_of_requests": 3,
                "mode": "sequential"
            }
        )

        assert response.status_code == 200

        result = response.json()

        assert result["total_requests"] == 3
        assert result["successful_requests"] == 3
        assert result["failed_requests"] == 0
        assert result["success_rate_percent"] == 100.0

        assert result["p95_response_time_ms"] > 0
        assert result["p99_response_time_ms"] > 0

        assert result["p95_response_time_ms"] >= (
            result["minimum_response_time_ms"]
        )

        assert result["p99_response_time_ms"] >= (
            result["p95_response_time_ms"]
        )

        assert len(result["results"]) == 3

    finally:
        server.shutdown()


def test_invalid_performance_test_mode():
    response = client.post(
        "/performance-test",
        json={
            "url": "http://127.0.0.1/test",
            "number_of_requests": 3,
            "mode": "invalid"
        }
    )

    assert response.status_code == 422


def test_invalid_performance_test_url():
    response = client.post(
        "/performance-test",
        json={
            "url": "not-a-valid-url",
            "number_of_requests": 3
        }
    )

    assert response.status_code == 422


def test_unsupported_performance_test_url_scheme():
    response = client.post(
        "/performance-test",
        json={
            "url": "ftp://example.com/file",
            "number_of_requests": 3
        }
    )

    assert response.status_code == 422
