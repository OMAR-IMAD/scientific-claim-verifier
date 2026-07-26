"""Automated tests for the Scientific Claim Verifier API."""

from typing import Any

from fastapi.testclient import TestClient

import backend.app.main as main_module


client = TestClient(main_module.app)


class FakeModelService:
    """Provide predictable results without loading the real model."""

    def predict(
        self,
        premise: str,
        hypothesis: str,
    ) -> dict[str, Any]:
        """Return a fixed test prediction."""

        return {
            "prediction": "ENTAILMENT",
            "confidence": 0.90,
            "scores": {
                "ENTAILMENT": 0.90,
                "NEUTRAL": 0.08,
                "CONTRADICTION": 0.02,
            },
            "device": "test",
        }


def test_root_endpoint() -> None:
    """Test the main API endpoint."""

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": (
            "Scientific Claim Verifier API is running"
        ),
        "status": "success",
    }


def test_health_endpoint() -> None:
    """Test the backend health endpoint."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }


def test_predict_endpoint(monkeypatch) -> None:
    """Test a successful prediction request."""

    monkeypatch.setattr(
        main_module,
        "get_model_service",
        lambda: FakeModelService(),
    )

    response = client.post(
        "/predict",
        json={
            "premise": (
                "A man is playing a guitar."
            ),
            "hypothesis": (
                "A person is performing music."
            ),
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["prediction"] == "ENTAILMENT"
    assert result["confidence"] == 0.90
    assert result["device"] == "test"
    assert result["scores"]["ENTAILMENT"] == 0.90


def test_empty_premise_is_rejected() -> None:
    """Test rejection of an empty premise."""

    response = client.post(
        "/predict",
        json={
            "premise": "   ",
            "hypothesis": "A valid hypothesis.",
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Premise cannot be empty.",
    }


def test_empty_hypothesis_is_rejected() -> None:
    """Test rejection of an empty hypothesis."""

    response = client.post(
        "/predict",
        json={
            "premise": "A valid premise.",
            "hypothesis": "   ",
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Hypothesis cannot be empty.",
    }


def test_missing_hypothesis_is_rejected() -> None:
    """Test rejection when hypothesis is missing."""

    response = client.post(
        "/predict",
        json={
            "premise": "A valid premise.",
        },
    )

    assert response.status_code == 422
    assert "detail" in response.json()

def test_missing_premise_is_rejected() -> None:
    """Test rejection when premise is missing."""

    response = client.post(
        "/predict",
        json={
            "hypothesis": "A valid hypothesis.",
        },
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_invalid_json_is_rejected() -> None:
    """Test rejection of an invalid JSON request."""

    response = client.post(
        "/predict",
        content="{invalid json}",
        headers={
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 422
    assert "detail" in response.json()

def test_prediction_response_structure(monkeypatch) -> None:
    """Test the complete prediction response structure."""

    monkeypatch.setattr(
        main_module,
        "get_model_service",
        lambda: FakeModelService(),
    )

    response = client.post(
        "/predict",
        json={
            "premise": "A man is playing a guitar.",
            "hypothesis": "A person is performing music.",
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert set(result.keys()) == {
        "premise",
        "hypothesis",
        "prediction",
        "confidence",
        "scores",
        "device",
    }

    assert set(result["scores"].keys()) == {
        "ENTAILMENT",
        "NEUTRAL",
        "CONTRADICTION",
    }

    assert 0.0 <= result["confidence"] <= 1.0
    assert result["prediction"] in {
        "ENTAILMENT",
        "NEUTRAL",
        "CONTRADICTION",
    }