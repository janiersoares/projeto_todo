class UserRepository:
    def find_by_email(self, email):
        cursor = self.connection.execute(
            """
            SELECT id, email, password_hash, created_at
            FROM users
            WHERE email = %s
            """,
            (email,),
        )
        row = cursor.fetchone()
        cursor.close()
        return row


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