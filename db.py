import os

import psycopg
from psycopg.rows import dict_row


class DatabaseUnavailable(Exception):
    pass


def connect():
    return psycopg.connect(os.environ["DATABASE_URL"])


def get_connection():
    try:
        connection = connect()
    except psycopg.Error as exc:
        raise DatabaseUnavailable from exc
    connection.row_factory = dict_row
    try:
        yield connection
        connection.commit()
    except psycopg.OperationalError as exc:
        # The connection itself is broken (network, server down).
        connection.rollback()
        raise DatabaseUnavailable from exc
    except Exception:
        # SQL errors and bugs: undo the work and let them surface as 500.
        connection.rollback()
        raise
    finally:
        connection.close()