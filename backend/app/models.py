"""Database models for the backend."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base


class User(Base):
    """Application user stored in the database."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

class Analysis(Base):
    """Claim verification analysis stored in the database."""

    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )

    premise: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    hypothesis: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    prediction: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    entailment_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    neutral_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    contradiction_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )