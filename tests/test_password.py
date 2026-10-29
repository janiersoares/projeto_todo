from security.password import hash_password, verify_password


def test_hash_is_not_the_plain_password():
    hashed = hash_password("12345678")
    assert hashed != "12345678"


def test_correct_password_verifies():
    hashed = hash_password("12345678")
    assert verify_password("12345678", hashed) is True


def test_wrong_password_does_not_verify():
    hashed = hash_password("12345678")
    assert verify_password("87654321", hashed) is False


def test_same_password_gives_different_hashes():
    first = hash_password("12345678")
    second = hash_password("12345678")
    assert first != second