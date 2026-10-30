class UserRepository:
    def __init__(self, connection):
        self.connection = connection

    def insert(self, email, password_hash):
        cursor = self.connection.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (%s, %s)
            RETURNING id, email, created_at
            """,
            (email, password_hash),
        )
        row = cursor.fetchone()
        cursor.close()
        return row