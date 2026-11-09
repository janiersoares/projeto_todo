import uuid

from schemas.user import LoginBody


def test_login_body_normalizes_email_case():
    body = LoginBody(email="Ana@Example.com", password="whatever")
    assert body.email == "ana@example.com"


def test_login_works_with_different_email_case(client):
    email = f"Mixed-{uuid.uuid4().hex[:8]}@Example.com"
    client.post(
        "/auth/register",
        json={"email": email, "password": "12345678"},
    )

    response = client.post(
        "/auth/login",
        json={"email": email, "password": "12345678"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()