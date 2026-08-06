"""Automated tests for the Scientific Claim Verifier API."""

from typing import Any

import pytest
from fastapi.testclient import TestClient

import backend.app.main as main_module


client = TestClient(main_module.app)


class FakeModelService:
    """Provide predictable results without loading the real model."""

    def __init__(self) -> None:
        """Initialize the fake service."""

        self.device = "test"

    def is_ready(self) -> bool:
        """Return the fake model readiness state."""

        return True

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


@pytest.fixture
def valid_prediction_payload() -> dict[str, str]:

    """Return reusable valid prediction input."""

    return {
        "premise": "A man is playing a guitar.",
        "hypothesis": "A person is performing music.",
    }

@pytest.fixture
def mock_model_service(monkeypatch) -> FakeModelService:
    """Replace the real model service with a reusable fake service."""

    fake_service = FakeModelService()

    monkeypatch.setattr(
        main_module,
        "get_model_service",
        lambda: fake_service,
    )

    return fake_service


@pytest.fixture
def openapi_schema() -> dict[str, Any]:
    """Return the generated OpenAPI schema."""

    response = client.get("/openapi.json")

    assert response.status_code == 200

    return response.json()


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

def test_health_endpoint_when_model_is_not_ready(
    mock_model_service: FakeModelService,
    monkeypatch,
) -> None:
    """Test the health response when the model is not ready."""

    monkeypatch.setattr(
        mock_model_service,
        "is_ready",
        lambda: False,
    )

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "degraded",
        "model_ready": False,
        "model_status": "not_ready",
        "device": "test",
        "detail": "Model service is not ready.",
    }

def test_health_endpoint_when_model_service_fails(
    monkeypatch,
) -> None:
    """Test the health response when model loading fails."""

    def raise_model_loading_error() -> None:
        raise RuntimeError("Model loading failed.")

    monkeypatch.setattr(
        main_module,
        "get_model_service",
        raise_model_loading_error,
    )

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "degraded",
        "model_ready": False,
        "model_status": "unavailable",
        "device": None,
        "detail": "Model loading failed.",
    }

def test_health_endpoint(
    mock_model_service: FakeModelService,
) -> None:
    """Test the backend and model health endpoint."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "model_ready": True,
        "model_status": "ready",
        "device": "test",
        "detail": None,
    }

def test_predict_endpoint(
    mock_model_service: FakeModelService,
    valid_prediction_payload: dict[str, str],
) -> None:
    """Test a successful prediction request."""

    response = client.post(
        "/predict",
        json=valid_prediction_payload,
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

def test_prediction_response_structure(
    mock_model_service: FakeModelService,
    valid_prediction_payload: dict[str, str],
) -> None:
    """Test the complete prediction response structure."""

    response = client.post(
        "/predict",
       json=valid_prediction_payload,

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

def test_openapi_contains_error_response_schema(
    openapi_schema: dict[str, Any],
) -> None:
    """Test ErrorResponse schema in OpenAPI documentation."""

    error_schema = openapi_schema["components"]["schemas"]["ErrorResponse"]

    assert error_schema["type"] == "object"
    assert error_schema["required"] == ["detail"]
    assert error_schema["properties"]["detail"]["type"] == "string"
    assert (
        error_schema["properties"]["detail"]["description"]
        == "Explanation of the API error."
    )

def test_openapi_contains_custom_422_examples(
    openapi_schema: dict[str, Any],
) -> None:
    """Test custom 422 error examples in OpenAPI documentation."""

    error_response = openapi_schema["paths"]["/predict"]["post"][
        "responses"
    ]["422"]

    assert error_response["description"] == "Invalid input data."

    examples = error_response["content"]["application/json"]["examples"]

    assert examples["empty_premise"]["value"] == {
        "detail": "Premise cannot be empty.",
    }

    assert examples["empty_hypothesis"]["value"] == {
        "detail": "Hypothesis cannot be empty.",
    }