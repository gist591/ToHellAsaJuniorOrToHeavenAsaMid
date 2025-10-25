from datetime import UTC, datetime, timedelta
from pathlib import Path
from random import randint
from typing import Any

import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

keys_dir = Path(__file__).parent.parent.parent.parent.parent / "keys"
PRIVATE_KEY = (keys_dir / "private.pem").read_bytes()
PUBLIC_KEY = (keys_dir / "public.pem").read_bytes()

REVOKED_TOKENS = set()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check password"""
    return bool(pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    """Hash password"""
    return str(pwd_context.hash(password))


def create_token_pair(user_id: int, username: str) -> tuple[str, str]:
    """
    Create access and refresh token when login
    """
    session_id = str(randint(0, 10000))

    access_payload = {
        "sub": str(user_id),
        "username": username,
        "session_id": session_id,
        "type": "access",
        "exp": datetime.now(UTC) + timedelta(minutes=15),
        "iat": datetime.now(UTC),
    }

    refresh_payload = {
        "sub": str(user_id),
        "session_id": session_id,
        "type": "refresh",
        "exp": datetime.now(UTC) + timedelta(days=7),
        "iat": datetime.now(UTC),
    }

    access_token = jwt.encode(access_payload, PRIVATE_KEY, algorithm="RS256")
    refresh_token = jwt.encode(refresh_payload, PRIVATE_KEY, algorithm="RS256")

    return (access_token, refresh_token)


def verify_token(token: str) -> dict[str, Any] | None:
    """
    Check token. It may all services
    """
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])

        if payload.get("type") != "access":
            return None

        if token in REVOKED_TOKENS:
            return None

        return dict(payload)

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None


def refresh_access_token(refresh_token: str) -> str | None:
    """
    Refresh access
    """
    try:
        payload = jwt.decode(refresh_token, PUBLIC_KEY, algorithms=["RS256"])

        if payload.get("type") != "refresh":
            return None

        if refresh_token in REVOKED_TOKENS:
            return None

        new_access_payload = {
            "sub": payload["sub"],
            "username": "from_db",
            "session_id": payload["session_id"],
            "type": "access",
            "exp": datetime.now(UTC) + timedelta(minutes=15),
            "iat": datetime.now(UTC),
        }

        return str(jwt.encode(new_access_payload, PRIVATE_KEY, algorithm="RS256"))

    except jwt.InvalidTokenError:
        return None


def logout(refresh_token: str) -> None:
    """
    Logout - revoke refresh
    """
    REVOKED_TOKENS.add(refresh_token)
