import os
import threading

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool, PoolTimeout


class DatabaseUnavailable(Exception):
    pass


_pool = None
_pool_lock = threading.Lock()


def connect():
    return psycopg.connect(os.environ["DATABASE_URL"])


def get_pool():
    global _pool
    with _pool_lock:
        if _pool is None:
            _pool = ConnectionPool(
                os.environ["DATABASE_URL"],
                min_size=1,
                max_size=10,
                timeout=5,
                kwargs={"row_factory": dict_row},
            )
    return _pool


def close_pool():
    global _pool
    with _pool_lock:
        if _pool is not None:
            _pool.close()
            _pool = None


def get_connection():
    try:
        with get_pool().connection() as connection:
            yield connection
    except (psycopg.OperationalError, PoolTimeout) as exc:
        # Only connection-level failures mean "database unavailable".
        raise DatabaseUnavailable from exc
