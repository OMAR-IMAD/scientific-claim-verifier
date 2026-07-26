"""Pydantic schemas used by the Scientific Claim Verifier API."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


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
                }
            ]
        }
    )

    status: str


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