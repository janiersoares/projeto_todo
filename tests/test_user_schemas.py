import pytest
from pydantic import ValidationError

from schemas.user import UserCreate, UserOut


def test_valid_user_is_accepted():
    user = UserCreate(email="test@example.com", password="12345678")
    assert user.email == "test@example.com"


def test_invalid_email_is_rejected():
    with pytest.raises(ValidationError):
        UserCreate(email="not-an-email", password="12345678")


def test_short_password_is_rejected():
    with pytest.raises(ValidationError):
        UserCreate(email="test@example.com", password="1234567")


def test_user_out_does_not_expose_password():
    assert "password" not in UserOut.model_fields
    assert "password_hash" not in UserOut.model_fields


def test_password_with_exactly_8_characters_is_accepted():
    user = UserCreate(email="test@example.com", password="12345678")
    assert user.password == "12345678"


def test_email_is_normalized_to_lowercase():
    user = UserCreate(email="  User@Example.COM  ", password="12345678")
    assert user.email == "user@example.com"
    