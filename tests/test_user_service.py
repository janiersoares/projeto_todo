import pytest

from services import user_service
from services.user_service import InvalidCredentials, UserService


class FakeRepository:
    def __init__(self, user=None):
        self.user = user

    def find_by_email(self, email):
        return self.user


def test_unknown_email_still_runs_password_check(monkeypatch):
    calls = []

    def fake_verify(password, password_hash):
        calls.append(password_hash)
        return False

    monkeypatch.setattr(user_service, "verify_password", fake_verify)
    service = UserService(FakeRepository(user=None))

    with pytest.raises(InvalidCredentials):
        service.login("nobody@example.com", "password123")

    assert calls == [user_service.DUMMY_HASH]