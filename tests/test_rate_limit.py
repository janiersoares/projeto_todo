import uuid

from security.rate_limit import RateLimiter


def test_limiter_blocks_after_max_attempts():
    limiter = RateLimiter(max_attempts=2, window_seconds=60)
    assert limiter.is_blocked("a@example.com") is False

    limiter.record_failure("a@example.com")
    limiter.record_failure("a@example.com")

    assert limiter.is_blocked("a@example.com") is True
    assert limiter.is_blocked("b@example.com") is False


def test_limiter_clear_resets_one_key():
    limiter = RateLimiter(max_attempts=1, window_seconds=60)
    limiter.record_failure("a@example.com")
    limiter.clear("a@example.com")

    assert limiter.is_blocked("a@example.com") is False


def test_login_returns_429_after_too_many_failures(client):
    email = f"locked-{uuid.uuid4().hex[:8]}@example.com"
    client.post("/auth/register", json={"email": email, "password": "12345678"})

    for _ in range(5):
        response = client.post(
            "/auth/login",
            json={"email": email, "password": "wrong-password"},
        )
        assert response.status_code == 401

    blocked = client.post(
        "/auth/login",
        json={"email": email, "password": "12345678"},
    )
    assert blocked.status_code == 429
