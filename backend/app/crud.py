"""Database CRUD operations."""

from datetime import date, timedelta

from sqlalchemy import func, or_, select
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
    prediction: str | None = None,
    search: str | None = None,
    sort_order: str = "newest",
    skip: int = 0,
    limit: int = 20,
) -> list[Analysis]:
    """Return analyses for a specific user with optional prediction filtering."""

    statement = select(Analysis).where(
        Analysis.user_id == user_id
    )

    if prediction is not None:
        statement = statement.where(
            Analysis.prediction == prediction
        )

    if search is not None and search.strip():
        search_pattern = f"%{search.strip()}%"

        statement = statement.where(
            or_(
                Analysis.premise.ilike(search_pattern),
                Analysis.hypothesis.ilike(search_pattern),
            )
        )

    if sort_order == "oldest":
        statement = statement.order_by(
            Analysis.created_at.asc(),
            Analysis.id.asc(),
        )
    else:
        statement = statement.order_by(
            Analysis.created_at.desc(),
            Analysis.id.desc(),
        )

    statement = statement.offset(skip).limit(limit)

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


def delete_analysis_by_id_for_user(
    db: Session,
    user_id: int,
    analysis_id: int,
) -> bool:
    """Delete a specific analysis owned by a specific user."""

    analysis = get_analysis_by_id_for_user(
        db,
        user_id,
        analysis_id,
    )

    if analysis is None:
        return False

    db.delete(analysis)
    db.commit()

    return True


def get_analysis_stats_by_user(
    db: Session,
    user_id: int,
) -> dict[str, object]:
    """Return analysis statistics for a specific user."""

    statement = (
        select(
            Analysis.prediction,
            func.count(Analysis.id),
        )
        .where(Analysis.user_id == user_id)
        .group_by(Analysis.prediction)
    )

    rows = db.execute(statement).all()

    stats = {
        "total": 0,
        "ENTAILMENT": 0,
        "CONTRADICTION": 0,
        "NEUTRAL": 0,
    }

    for prediction, count in rows:
        stats[prediction] = count
        stats["total"] += count

    if stats["total"] > 0:
        stats["entailment_percentage"] = round(
            stats["ENTAILMENT"] / stats["total"] * 100,
            2,
        )

        stats["contradiction_percentage"] = round(
            stats["CONTRADICTION"] / stats["total"] * 100,
            2,
        )

        stats["neutral_percentage"] = round(
            stats["NEUTRAL"] / stats["total"] * 100,
            2,
        )
    else:
        stats["entailment_percentage"] = 0.0
        stats["contradiction_percentage"] = 0.0
        stats["neutral_percentage"] = 0.0

    today = date.today()
    start_date = today - timedelta(days=6)

    daily_counts = {
        (start_date + timedelta(days=offset)).isoformat(): 0
        for offset in range(7)
    }

    daily_statement = (
        select(
            func.date(Analysis.created_at),
            func.count(Analysis.id),
        )
        .where(
            Analysis.user_id == user_id,
            func.date(Analysis.created_at) >= start_date.isoformat(),
            func.date(Analysis.created_at) <= today.isoformat(),
        )
        .group_by(func.date(Analysis.created_at))
        .order_by(func.date(Analysis.created_at))
    )

    daily_rows = db.execute(daily_statement).all()

    for analysis_date, count in daily_rows:
        day_key = str(analysis_date)

        if day_key in daily_counts:
            daily_counts[day_key] = count

    stats["today_total"] = daily_counts[today.isoformat()]
    stats["last_7_days_total"] = sum(daily_counts.values())
    stats["daily_counts"] = daily_counts

    return stats