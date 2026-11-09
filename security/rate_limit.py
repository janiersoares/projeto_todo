import time
from collections import deque


class RateLimiter:
    """Counts failed attempts per key inside a sliding time window.

    The state lives in this process's memory: it resets on restart and is
    not shared between multiple workers.
    """

    def __init__(self, max_attempts, window_seconds):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._attempts = {}

    def _prune(self, key, now):
        attempts = self._attempts.get(key)
        if attempts is None:
            return
        while attempts and now - attempts[0] > self.window_seconds:
            attempts.popleft()
        if not attempts:
            del self._attempts[key]

    def is_blocked(self, key):
        now = time.monotonic()
        self._prune(key, now)
        attempts = self._attempts.get(key)
        return attempts is not None and len(attempts) >= self.max_attempts

    def record_failure(self, key):
        now = time.monotonic()
        self._prune(key, now)
        self._attempts.setdefault(key, deque()).append(now)

    def clear(self, key):
        self._attempts.pop(key, None)

    def reset(self):
        self._attempts.clear()


login_limiter = RateLimiter(max_attempts=5, window_seconds=15 * 60)
