from psycopg.errors import UniqueViolation

from security.password import hash_password, verify_password

# A real bcrypt hash, used when the email is unknown so both paths take the same time.
DUMMY_HASH = hash_password("dummy-password-for-timing")


class EmailAlreadyRegistered(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class UserService:

    def __init__(self, repository):
        self.repository = repository

    def register(self, email, password):
        password_hash = hash_password(password)
        try:
            return self.repository.insert(email, password_hash)

        except UniqueViolation as exc:
            raise EmailAlreadyRegistered(email) from exc

    def login(self, email, password):
        user = self.repository.find_by_email(email)
        password_hash = user["password_hash"] if user else DUMMY_HASH
        password_ok = verify_password(password, password_hash)
        if user is None or not password_ok:
            raise InvalidCredentials()
        return user