"""Pydantic schemas used by the Scientific Claim Verifier API."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


PredictionLabel = Literal[
    "ENTAILMENT",
    "NEUTRAL",
    "CONTRADICTION",
]


class RootResponse(BaseModel):
    """Response returned by the root endpoint."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "message": (
                        "Scientific Claim Verifier API is running"
                    ),
                    "status": "success",
                }
            ]
        }
    )

    message: str
    status: str


class HealthResponse(BaseModel):
    """Response returned by the health endpoint."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "healthy",
                    "model_ready": True,
                    "model_status": "ready",
                    "device": "cuda",
                    "detail": None,
                }
            ]
        }
    )

    status: str
    model_ready: bool
    model_status: str
    device: str | None = None
    detail: str | None = None


class PredictionRequest(BaseModel):
    """Input data required for a claim verification request."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "premise": (
                        "A man is playing a guitar on stage."
                    ),
                    "hypothesis": (
                        "A person is performing music."
                    ),
                }
            ]
        }
    )

    premise: str = Field(
        ...,
        description="Evidence or supporting text.",
        examples=[
            "A man is playing a guitar on stage.",
        ],
    )

    hypothesis: str = Field(
        ...,
        description="Scientific or general claim to verify.",
        examples=[
            "A person is performing music.",
        ],
    )

    @field_validator("premise", "hypothesis")
    @classmethod
    def strip_input_text(cls, value: str) -> str:
        """Remove leading and trailing whitespace from input text."""
        return value.strip()

class PredictionScores(BaseModel):
    """Confidence scores for the three NLI classes."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "ENTAILMENT": 0.90,
                    "NEUTRAL": 0.08,
                    "CONTRADICTION": 0.02,
                }
            ]
        }
    )

    ENTAILMENT: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Entailment probability score.",
    )

    NEUTRAL: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Neutral probability score.",
    )

    CONTRADICTION: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Contradiction probability score.",
    )


class PredictionResponse(BaseModel):
    """Structured result returned after claim verification."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "premise": (
                        "A man is playing a guitar on stage."
                    ),
                    "hypothesis": (
                        "A person is performing music."
                    ),
                    "prediction": "ENTAILMENT",
                    "confidence": 0.90,
                    "scores": {
                        "ENTAILMENT": 0.90,
                        "NEUTRAL": 0.08,
                        "CONTRADICTION": 0.02,
                    },
                    "device": "cuda",
                }
            ]
        }
    )

    premise: str
    hypothesis: str
    prediction: PredictionLabel

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score of the selected prediction.",
    )

    scores: PredictionScores
    device: str = Field(
        ...,
        description="Device used to run the model.",
    )

class ErrorResponse(BaseModel):
    """Simple error response returned by the API."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "detail": "Premise cannot be empty.",
                }
            ]
        }
    )

    detail: str = Field(
        ...,
        description="Explanation of the API error.",
    )


class UserCreate(BaseModel):
    """Request body used to register a new user."""

    email: str = Field(
        ...,
        min_length=3,
        max_length=255,
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        """Normalize and validate the email address."""

        email = value.strip().lower()

        if "@" not in email:
            raise ValueError("Email must contain @.")

        return email


class UserLogin(UserCreate):
    """Request body used to log in a user."""


class UserResponse(BaseModel):
    """Public user data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str


class TokenResponse(BaseModel):
    """JWT access token returned after successful login."""

    access_token: str
    token_type: Literal["bearer"] = "bearer"