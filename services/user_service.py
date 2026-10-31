from psycopg.errors import UniqueViolation

from security.password import hash_password, verify_password


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
        if user is None:
            raise InvalidCredentials()
        if not verify_password(password, user["password_hash"]):
            raise InvalidCredentials()
        return user
    