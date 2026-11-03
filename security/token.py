import os
from datetime import datetime, timedelta, timezone

import jwt

ALGORITHM = "HS256"
TOKEN_MINUTES = 30


def create_access_token(user_id: int) -> str:
    secret = os.environ["JWT_SECRET"]
    expires = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES)
    payload = {"sub": str(user_id), "exp": expires}
    return jwt.encode(payload, secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int:
    secret = os.environ["JWT_SECRET"]
    payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
    return int(payload["sub"])