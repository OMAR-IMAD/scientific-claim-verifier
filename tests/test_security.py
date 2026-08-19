"""Tests for password security helpers."""
import jwt
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

import backend.app.security as security_module

from backend.app.security import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    create_access_token,
    decode_access_token,
    get_current_user,
    hash_password,
    verify_password,
)

def test_hash_password_creates_argon2_hash():
    """Create an Argon2 hash from a plain-text password."""

    hashed_password = hash_password("TestPassword123!")

    assert hashed_password != "TestPassword123!"
    assert hashed_password.startswith("$argon2")


def test_verify_password_accepts_correct_password():
    """Accept the correct password."""

    hashed_password = hash_password("TestPassword123!")

    assert verify_password(
        "TestPassword123!",
        hashed_password,
    ) is True


def test_verify_password_rejects_wrong_password():
    """Reject an incorrect password."""

    hashed_password = hash_password("TestPassword123!")

    assert verify_password(
        "WrongPassword",
        hashed_password,
    ) is False


def test_create_access_token_contains_subject_and_expiration():
    """Create a JWT containing subject and expiration claims."""

    token = create_access_token("user@example.com")

    payload = jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
    )

    assert payload["sub"] == "user@example.com"
    assert "exp" in payload


def test_decode_access_token_returns_payload():
    """Decode a valid JWT access token."""

    token = create_access_token("user@example.com")

    payload = decode_access_token(token)

    assert payload["sub"] == "user@example.com"
    assert "exp" in payload


def test_get_current_user_returns_authenticated_user(monkeypatch) -> None:
    """Return the authenticated user for a valid token."""

    user = type(
        "UserRecord",
        (),
        {
            "id": 1,
            "email": "user@example.com",
        },
    )()

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="valid-token",
    )

    monkeypatch.setattr(
        security_module,
        "decode_access_token",
        lambda token: {"sub": "user@example.com"},
    )
    monkeypatch.setattr(
        security_module,
        "get_user_by_email",
        lambda db, email: user,
    )

    current_user = get_current_user(
        credentials=credentials,
        db=object(),
    )

    assert current_user is user
    assert current_user.email == "user@example.com"


def test_get_current_user_rejects_missing_credentials() -> None:
    """Reject requests that do not include a Bearer token."""

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=None,
            db=object(),
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Not authenticated."
    assert exc_info.value.headers == {
        "WWW-Authenticate": "Bearer",
    }


def test_get_current_user_rejects_invalid_token(monkeypatch) -> None:
    """Reject an invalid JWT access token."""

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid-token",
    )

    def raise_invalid_token(token):
        raise jwt.InvalidTokenError("Invalid token")

    monkeypatch.setattr(
        security_module,
        "decode_access_token",
        raise_invalid_token,
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=object(),
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid or expired token."
    assert exc_info.value.headers == {
        "WWW-Authenticate": "Bearer",
    }


def test_get_current_user_rejects_unknown_user(monkeypatch) -> None:
    """Reject a token whose subject does not match a database user."""

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="valid-token",
    )

    monkeypatch.setattr(
        security_module,
        "decode_access_token",
        lambda token: {"sub": "missing@example.com"},
    )
    monkeypatch.setattr(
        security_module,
        "get_user_by_email",
        lambda db, email: None,
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=object(),
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid or expired token."
    assert exc_info.value.headers == {
        "WWW-Authenticate": "Bearer",
    }