"""Pydantic schemas used by the Scientific Claim Verifier API."""

from typing import Literal

from pydantic import BaseModel, Field


PredictionLabel = Literal[
    "ENTAILMENT",
    "NEUTRAL",
    "CONTRADICTION",
]


class RootResponse(BaseModel):
    """Response returned by the root endpoint."""

    message: str
    status: str


class HealthResponse(BaseModel):
    """Response returned by the health endpoint."""

    status: str


class PredictionRequest(BaseModel):
    """Input data required for a claim verification request."""

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


class PredictionScores(BaseModel):
    """Confidence scores for the three NLI classes."""

    ENTAILMENT: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    NEUTRAL: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    CONTRADICTION: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )


class PredictionResponse(BaseModel):
    """Structured result returned after claim verification."""

    premise: str
    hypothesis: str
    prediction: PredictionLabel

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    scores: PredictionScores
    device: str