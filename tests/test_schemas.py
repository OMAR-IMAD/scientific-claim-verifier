"""Tests for Pydantic schemas."""

import pytest
from pydantic import ValidationError

from backend.app.schemas import (
    ErrorResponse,
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
    PredictionScores,
    RootResponse,
)

def test_prediction_request_strips_whitespace() -> None:
    """Test removing extra whitespace from request fields."""

    request = PredictionRequest(
        premise="  A man is playing a guitar.  ",
        hypothesis="  A person is performing music.  ",
    )

    assert request.premise == "A man is playing a guitar."
    assert request.hypothesis == "A person is performing music."

def test_prediction_scores_rejects_values_outside_range() -> None:
    """Test rejecting probability scores outside the valid range."""

    with pytest.raises(ValidationError):
        PredictionScores(
            ENTAILMENT=1.20,
            NEUTRAL=0.10,
            CONTRADICTION=-0.05,
        )

def test_prediction_scores_accepts_valid_values() -> None:
    """Test accepting probability scores inside the valid range."""

    scores = PredictionScores(
        ENTAILMENT=0.80,
        NEUTRAL=0.15,
        CONTRADICTION=0.05,
    )

    assert scores.ENTAILMENT == 0.80
    assert scores.NEUTRAL == 0.15
    assert scores.CONTRADICTION == 0.05

def test_prediction_response_rejects_invalid_label() -> None:
    """Test rejecting an unsupported prediction label."""

    with pytest.raises(ValidationError):
        PredictionResponse(
            premise="A man is playing a guitar.",
            hypothesis="A person is performing music.",
            prediction="UNKNOWN",
            confidence=0.90,
            scores={
                "ENTAILMENT": 0.90,
                "NEUTRAL": 0.08,
                "CONTRADICTION": 0.02,
            },
            device="test",
        )

def test_prediction_response_rejects_invalid_confidence() -> None:
    """Test rejecting confidence values outside the valid range."""

    with pytest.raises(ValidationError):
        PredictionResponse(
            premise="A man is playing a guitar.",
            hypothesis="A person is performing music.",
            prediction="ENTAILMENT",
            confidence=1.20,
            scores={
                "ENTAILMENT": 0.90,
                "NEUTRAL": 0.08,
                "CONTRADICTION": 0.02,
            },
            device="test",
        )

def test_error_response_stores_detail_message() -> None:
    """Test storing the API error detail message."""

    error = ErrorResponse(
        detail="Premise cannot be empty.",
    )

    assert error.detail == "Premise cannot be empty."

def test_error_response_requires_detail() -> None:
    """Test requiring the API error detail field."""

    with pytest.raises(ValidationError):
        ErrorResponse()

def test_root_response_stores_message_and_status() -> None:
    """Test storing root response fields."""

    response = RootResponse(
        message="Scientific Claim Verifier API is running",
        status="success",
    )

    assert response.message == "Scientific Claim Verifier API is running"
    assert response.status == "success"

def test_health_response_stores_fields() -> None:
    """Test storing health response fields."""

    response = HealthResponse(
        status="healthy",
        model_ready=True,
        model_status="ready",
        device="cuda",
        detail=None,
    )

    assert response.status == "healthy"
    assert response.model_ready is True
    assert response.model_status == "ready"
    assert response.device == "cuda"
    assert response.detail is None