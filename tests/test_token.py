import jwt
import pytest

from security.token import ALGORITHM, create_access_token, decode_access_token


@pytest.fixture(autouse=True)
def secret(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret-with-at-least-32-bytes-long!!")


def test_token_returns_the_same_user_id():
    token = create_access_token(7)
    assert decode_access_token(token) == 7


def test_token_signed_with_other_secret_is_rejected(monkeypatch):
    token = create_access_token(7)
    monkeypatch.setenv("JWT_SECRET", "another-secret-also-with-at-least-32-bytes")
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(token)


def test_expired_token_is_rejected():
    expired = jwt.encode(
        {"sub": "7", "exp": 1},
        "test-secret-with-at-least-32-bytes-long!!",
        algorithm=ALGORITHM,
    )
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(expired)