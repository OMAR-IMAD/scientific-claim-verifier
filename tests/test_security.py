"""Tests for password security helpers."""

from backend.app.security import hash_password, verify_password


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