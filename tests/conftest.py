from dotenv import load_dotenv

load_dotenv()
import os
import uuid

import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg.rows import dict_row

from db import get_connection
from main import app
from security.rate_limit import login_limiter


@pytest.fixture(autouse=True)
def reset_login_limiter():
    login_limiter.reset()
    yield


@pytest.fixture
def connection():
    url = os.environ.get("DATABASE_URL")
    if not url:
        pytest.skip("DATABASE_URL is not set")
    conn = psycopg.connect(url)
    conn.row_factory = dict_row
    try:
        yield conn
    finally:
        conn.rollback()
        conn.close()


@pytest.fixture
def client(connection):
    def override():
        yield connection

    app.dependency_overrides[get_connection] = override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    email = f"owner-{uuid.uuid4().hex[:8]}@example.com"
    client.post(
        "/auth/register",
        json={"email": email, "password": "12345678"},
    )
    response = client.post(
        "/auth/login",
        json={"email": email, "password": "12345678"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
