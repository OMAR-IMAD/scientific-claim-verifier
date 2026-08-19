"""Tests for password security helpers."""
import jwt

from backend.app.security import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    create_access_token,
    decode_access_token,
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