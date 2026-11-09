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


def test_checking_unknown_keys_does_not_store_them():
    limiter = RateLimiter(max_attempts=1, window_seconds=60)
    for number in range(100):
        limiter.is_blocked(f"user{number}@example.com")

    assert len(limiter._attempts) == 0


def test_expired_attempts_are_removed(monkeypatch):
    limiter = RateLimiter(max_attempts=1, window_seconds=60)
    now = 1000.0
    monkeypatch.setattr("security.rate_limit.time.monotonic", lambda: now)
    limiter.record_failure("a@example.com")

    now = 1100.0  # 100 seconds later, outside the 60 second window
    assert limiter.is_blocked("a@example.com") is False
    assert "a@example.com" not in limiter._attempts


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
