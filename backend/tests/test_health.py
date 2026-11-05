from fastapi.testclient import TestClient

from trust_trash.bootstrap.app import app


def test_health_endpoint_returns_ok() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
