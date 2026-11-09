import psycopg
from fastapi.testclient import TestClient

import db
from main import app


class BrokenPool:
    def connection(self):
        raise psycopg.OperationalError("database is down")


def test_database_down_returns_503(monkeypatch):
    app.dependency_overrides.clear()
    monkeypatch.setattr(db, "get_pool", lambda: BrokenPool())

    client = TestClient(app)
    response = client.post(
        "/auth/login",
        json={"email": "nobody@example.com", "password": "password123"},
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
