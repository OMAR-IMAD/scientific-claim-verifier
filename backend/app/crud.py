"""Database CRUD operations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models import Analysis, User


def get_user_by_email(db: Session, email: str) -> User | None:
    """Return a user by email if it exists."""

    statement = select(User).where(User.email == email)

    return db.scalar(statement)


def create_user(
    db: Session,
    email: str,
    hashed_password: str,
) -> User:
    """Create and return a new user."""

    user = User(
        email=email,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_analysis(
    db: Session,
    user_id: int,
    premise: str,
    hypothesis: str,
    prediction: str,
    confidence: float,
    entailment_score: float,
    neutral_score: float,
    contradiction_score: float,
) -> Analysis:
    """Create and return a new analysis."""

    analysis = Analysis(
        user_id=user_id,
        premise=premise,
        hypothesis=hypothesis,
        prediction=prediction,
        confidence=confidence,
        entailment_score=entailment_score,
        neutral_score=neutral_score,
        contradiction_score=contradiction_score,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


def get_analyses_by_user(
    db: Session,
    user_id: int,
) -> list[Analysis]:
    """Return analyses for a specific user."""

    statement = (
    select(Analysis)
    .where(Analysis.user_id == user_id)
    .order_by(
        Analysis.created_at.desc(),
        Analysis.id.desc(),
    )
)

    return list(db.scalars(statement).all())


def get_analysis_by_id_for_user(
    db: Session,
    user_id: int,
    analysis_id: int,
) -> Analysis | None:
    """Return a specific analysis owned by a specific user."""

    statement = select(Analysis).where(
        Analysis.id == analysis_id,
        Analysis.user_id == user_id,
    )

    return db.scalar(statement)