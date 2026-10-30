from psycopg.errors import UniqueViolation

from security.password import hash_password


class EmailAlreadyRegistered(Exception):
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
        