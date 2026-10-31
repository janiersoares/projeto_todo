import pytest

from security.password import hash_password
from services.user_service import InvalidCredentials, UserService


class FakeRepository:
    def __init__(self, user):
        self.user = user

    def find_by_email(self, email):
        if self.user and self.user["email"] == email:
            return self.user
        return None


def make_service():
    user = {
        "id": 1,
        "email": "ana@example.com",
        "password_hash": hash_password("12345678"),
    }
    return UserService(FakeRepository(user))


def test_login_with_correct_password_returns_user():
    service = make_service()
    user = service.login("ana@example.com", "12345678")
    assert user["email"] == "ana@example.com"


def test_login_with_wrong_password_rejected():
    service = make_service()
    with pytest.raises(InvalidCredentials):
        service.login("ana@example.com", "87654321")


def test_login_with_unknown_email_is_rejected():
    service = make_service()
    with pytest.raises(InvalidCredentials):
        service.login("nobody@example.com", "12345678")