"""Tests for Pydantic schemas."""

import pytest
from pydantic import ValidationError

from backend.app.schemas import PredictionRequest, PredictionScores

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