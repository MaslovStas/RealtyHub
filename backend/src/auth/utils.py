import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from src.auth.constants import TokenType
from src.auth.schemas import Token
from src.config import settings
from src.user.models import User


def encode_jwt(
    payload: dict[str, Any],
    token_type: TokenType,
    secret_key: str = settings.auth_jwt.SECRET_KEY,
    algorithm: str = settings.auth_jwt.ALGORITHM,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    expire = now + (expire_timedelta or timedelta(minutes=15))
    to_encode.update(
        {
            "type": token_type,
            "exp": expire,
            "iat": now,
            "jti": uuid.uuid4().hex,
        }
    )
    return jwt.encode(to_encode, secret_key, algorithm)


def decode_jwt(
    token: str | bytes,
    secret_key: str = settings.auth_jwt.SECRET_KEY,
    algorithm: str = settings.auth_jwt.ALGORITHM,
) -> dict[str, Any]:
    decoded: dict[str, Any] = jwt.decode(token, secret_key, algorithms=[algorithm])
    return decoded


def create_access_token(data: dict[str, Any]) -> str:
    return encode_jwt(
        payload=data,
        token_type=TokenType.ACCESS,
        expire_timedelta=timedelta(
            minutes=settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )


def create_refresh_token(data: dict[str, Any]) -> str:
    return encode_jwt(
        payload=data,
        token_type=TokenType.REFRESH,
        expire_timedelta=timedelta(days=settings.auth_jwt.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def create_tokens(user: User) -> Token:
    access_token = create_access_token({"sub": user.id, "username": user.username})
    refresh_token = create_refresh_token({"sub": user.id})
    return Token(access_token=access_token, refresh_token=refresh_token)
