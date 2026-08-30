"""Tests for database CRUD operations."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.crud import (
    create_analysis,
    create_user,
    get_analyses_by_user,
    get_analysis_stats_by_user,
    get_user_by_email,
)
from backend.app.database import Base


@pytest.fixture
def db() -> Session:
    """Provide a temporary in-memory database session."""

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    test_session = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    session = test_session()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_get_user_by_email_returns_none(db: Session):
    """Return None when the user does not exist."""

    user = get_user_by_email(db, "missing@example.com")

    assert user is None


def test_create_and_get_user(db: Session):
    """Create a user and retrieve it by email."""

    created_user = create_user(
        db,
        "user@example.com",
        "hashed_password",
    )

    found_user = get_user_by_email(
        db,
        "user@example.com",
    )

    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == "user@example.com"


def test_create_and_get_analyses_by_user(db: Session):
    """Create analyses and return the newest one first."""

    user = create_user(
        db,
        "analysis@example.com",
        "hashed_password",
    )

    create_analysis(
        db,
        user.id,
        "Premise 1",
        "Hypothesis 1",
        "ENTAILMENT",
        0.90,
        0.90,
        0.08,
        0.02,
    )

    create_analysis(
        db,
        user.id,
        "Premise 2",
        "Hypothesis 2",
        "NEUTRAL",
        0.70,
        0.20,
        0.70,
        0.10,
    )

    analyses = get_analyses_by_user(db, user.id)

    assert len(analyses) == 2
    assert analyses[0].prediction == "NEUTRAL"
    assert analyses[1].prediction == "ENTAILMENT"


def test_get_analyses_by_user_oldest_order(db: Session):
    """Return the oldest analysis first when oldest sorting is requested."""

    user = create_user(
        db,
        "sorting@example.com",
        "hashed_password",
    )

    create_analysis(
        db,
        user.id,
        "Old premise",
        "Old hypothesis",
        "ENTAILMENT",
        0.90,
        0.90,
        0.08,
        0.02,
    )

    create_analysis(
        db,
        user.id,
        "New premise",
        "New hypothesis",
        "NEUTRAL",
        0.70,
        0.20,
        0.70,
        0.10,
    )

    analyses = get_analyses_by_user(
        db,
        user.id,
        sort_order="oldest",
    )

    assert len(analyses) == 2
    assert analyses[0].prediction == "ENTAILMENT"
    assert analyses[1].prediction == "NEUTRAL"


def test_get_analysis_stats_by_user(db: Session):
    """Return total and prediction counts for a specific user."""

    user = create_user(
        db,
        "stats@example.com",
        "hashed_password",
    )

    create_analysis(
        db,
        user.id,
        "Premise 1",
        "Hypothesis 1",
        "ENTAILMENT",
        0.90,
        0.90,
        0.08,
        0.02,
    )

    create_analysis(
        db,
        user.id,
        "Premise 2",
        "Hypothesis 2",
        "ENTAILMENT",
        0.85,
        0.85,
        0.10,
        0.05,
    )

    create_analysis(
        db,
        user.id,
        "Premise 3",
        "Hypothesis 3",
        "NEUTRAL",
        0.70,
        0.20,
        0.70,
        0.10,
    )

    create_analysis(
        db,
        user.id,
        "Premise 4",
        "Hypothesis 4",
        "CONTRADICTION",
        0.95,
        0.02,
        0.03,
        0.95,
    )

    stats = get_analysis_stats_by_user(db, user.id)

    assert stats["total"] == 4
    assert stats["ENTAILMENT"] == 2
    assert stats["NEUTRAL"] == 1
    assert stats["CONTRADICTION"] == 1