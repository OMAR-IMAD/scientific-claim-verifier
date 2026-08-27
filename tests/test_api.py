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

    current_user = type(
        "UserRecord",
        (),
        {
            "id": 1,
            "email": "user@example.com",
        },
    )()

    monkeypatch.setitem(
        main_module.app.dependency_overrides,
        main_module.get_current_user,
        lambda: current_user,
    )

    monkeypatch.setattr(
        main_module,
        "create_analysis",
        lambda *args, **kwargs: None,
    )

    return fake_service

def test_get_ready_model_service_returns_ready_service(
    mock_model_service: FakeModelService,
) -> None:
    """Test returning a ready model service."""

    service = main_module.get_ready_model_service()

    assert service is mock_model_service

def test_get_ready_model_service_raises_when_service_unavailable(
    monkeypatch,
) -> None:
    """Test error when the model service cannot be loaded."""

    def raise_loading_error():
        raise RuntimeError("Model loading failed.")

    monkeypatch.setattr(
        main_module,
        "get_model_service",
        raise_loading_error,
    )

    with pytest.raises(main_module.HTTPException) as error:
        main_module.get_ready_model_service()

    assert error.value.status_code == 503
    assert error.value.detail == main_module.MODEL_SERVICE_UNAVAILABLE

def test_get_ready_model_service_raises_when_model_not_ready(
    mock_model_service: FakeModelService,
    monkeypatch,
) -> None:
    """Test error when the model service is not ready."""

    monkeypatch.setattr(
        mock_model_service,
        "is_ready",
        lambda: False,
    )

    with pytest.raises(main_module.HTTPException) as error:
        main_module.get_ready_model_service()

    assert error.value.status_code == 503
    assert error.value.detail == main_module.MODEL_SERVICE_NOT_READY

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

def test_predict_endpoint_saves_analysis_for_current_user(
    mock_model_service: FakeModelService,
    monkeypatch,
    valid_prediction_payload: dict[str, str],
) -> None:
    """Save a successful prediction for the authenticated user."""

    saved_analysis: dict[str, Any] = {}

    def capture_analysis(db, **kwargs) -> None:
        saved_analysis.update(kwargs)

    monkeypatch.setattr(
        main_module,
        "create_analysis",
        capture_analysis,
    )

    response = client.post(
        "/predict",
        json=valid_prediction_payload,
    )

    assert response.status_code == 200
    assert saved_analysis == {
        "user_id": 1,
        "premise": "A man is playing a guitar.",
        "hypothesis": "A person is performing music.",
        "prediction": "ENTAILMENT",
        "confidence": 0.90,
        "entailment_score": 0.90,
        "neutral_score": 0.08,
        "contradiction_score": 0.02,
    }

def test_predict_endpoint_strips_input_whitespace(
    mock_model_service: FakeModelService,
) -> None:
    """Test removing extra whitespace from prediction input."""

    response = client.post(
        "/predict",
        json={
            "premise": "  A man is playing a guitar.  ",
            "hypothesis": "  A person is performing music.  ",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["premise"] == "A man is playing a guitar."
    assert data["hypothesis"] == "A person is performing music."


def test_predict_endpoint_when_model_service_fails(
    mock_model_service: FakeModelService,
    monkeypatch,
    valid_prediction_payload: dict[str, str],
) -> None:
    """Test prediction when the model service is unavailable."""

    def raise_model_loading_error() -> None:
        raise RuntimeError("Model loading failed.")

    monkeypatch.setattr(
        main_module,
        "get_model_service",
        raise_model_loading_error,
    )

    response = client.post(
        "/predict",
        json=valid_prediction_payload,
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Model service is unavailable.",
    }

def test_empty_premise_is_rejected(
    mock_model_service: FakeModelService,
) -> None:
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

def test_predict_endpoint_when_model_is_not_ready(
    mock_model_service: FakeModelService,
    monkeypatch,
    valid_prediction_payload: dict[str, str],
) -> None:
    """Test prediction when the model is not ready."""

    monkeypatch.setattr(
        mock_model_service,
        "is_ready",
        lambda: False,
    )

    response = client.post(
        "/predict",
        json=valid_prediction_payload,
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Model service is not ready.",
    }

def test_predict_endpoint_when_prediction_fails(
    mock_model_service: FakeModelService,
    monkeypatch,
    valid_prediction_payload: dict[str, str],
) -> None:
    """Test prediction when model inference fails."""

    def raise_prediction_error(
        premise: str,
        hypothesis: str,
    ) -> None:
        raise RuntimeError("Prediction execution failed.")

    monkeypatch.setattr(
        mock_model_service,
        "predict",
        raise_prediction_error,
    )

    response = client.post(
        "/predict",
        json=valid_prediction_payload,
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Prediction failed.",
    }

def test_empty_hypothesis_is_rejected(
    mock_model_service: FakeModelService,
) -> None:
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


def test_missing_hypothesis_is_rejected(
    mock_model_service: FakeModelService,
) -> None:
    """Test rejection when hypothesis is missing."""

    response = client.post(
        "/predict",
        json={
            "premise": "A valid premise.",
        },
    )

    assert response.status_code == 422
    assert "detail" in response.json()

def test_missing_premise_is_rejected(
    mock_model_service: FakeModelService,
) -> None:
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

def test_openapi_contains_predict_error_responses(
    openapi_schema: dict[str, Any],
) -> None:
    """Test that predict endpoint documents 500 and 503 errors."""

    responses = openapi_schema["paths"]["/predict"]["post"]["responses"]

    assert "500" in responses
    assert "503" in responses

    assert responses["500"]["description"] == (
        "Prediction execution failed."
    )

    assert responses["503"]["description"] == (
        "Model service is unavailable or not ready."
    )



def test_register_user_returns_public_user_data(monkeypatch) -> None:
    """Test registering a new user successfully."""

    monkeypatch.setattr(
        main_module,
        "get_user_by_email",
        lambda db, email: None,
    )
    monkeypatch.setattr(
        main_module,
        "hash_password",
        lambda password: "hashed-password",
    )

    def fake_create_user(db, email, hashed_password):
        return type(
            "UserRecord",
            (),
            {
                "id": 1,
                "email": email,
                "hashed_password": hashed_password,
            },
        )()

    monkeypatch.setattr(
        main_module,
        "create_user",
        fake_create_user,
    )

    response = client.post(
        "/register",
        json={
            "email": "USER@Example.COM",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "email": "user@example.com",
    }
    assert "hashed_password" not in response.json()


def test_register_user_rejects_duplicate_email(monkeypatch) -> None:
    """Test rejecting an already registered email."""

    existing_user = object()

    monkeypatch.setattr(
        main_module,
        "get_user_by_email",
        lambda db, email: existing_user,
    )

    response = client.post(
        "/register",
        json={
            "email": "user@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Email is already registered.",
    }


def test_login_user_returns_access_token(monkeypatch) -> None:
    """Test successful login returning a JWT access token."""

    user = type(
        "UserRecord",
        (),
        {
            "email": "user@example.com",
            "hashed_password": "stored-hash",
        },
    )()

    monkeypatch.setattr(
        main_module,
        "get_user_by_email",
        lambda db, email: user,
    )
    monkeypatch.setattr(
        main_module,
        "verify_password",
        lambda plain_password, hashed_password: True,
    )
    monkeypatch.setattr(
        main_module,
        "create_access_token",
        lambda subject: "test.jwt.token",
    )

    response = client.post(
        "/login",
        json={
            "email": "user@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "test.jwt.token",
        "token_type": "bearer",
    }


def test_login_user_rejects_wrong_password(monkeypatch) -> None:
    """Test rejecting login with an incorrect password."""

    user = type(
        "UserRecord",
        (),
        {
            "email": "user@example.com",
            "hashed_password": "stored-hash",
        },
    )()

    monkeypatch.setattr(
        main_module,
        "get_user_by_email",
        lambda db, email: user,
    )
    monkeypatch.setattr(
        main_module,
        "verify_password",
        lambda plain_password, hashed_password: False,
    )

    response = client.post(
        "/login",
        json={
            "email": "user@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid email or password.",
    }


def test_login_user_rejects_unknown_email(monkeypatch) -> None:
    """Test rejecting login for an unknown email."""

    monkeypatch.setattr(
        main_module,
        "get_user_by_email",
        lambda db, email: None,
    )

    response = client.post(
        "/login",
        json={
            "email": "missing@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid email or password.",
    }


def test_me_endpoint_returns_current_user() -> None:
    """Return public data for the authenticated user."""

    user = type(
        "UserRecord",
        (),
        {
            "id": 1,
            "email": "user@example.com",
        },
    )()

    main_module.app.dependency_overrides[
        main_module.get_current_user
    ] = lambda: user

    try:
        response = client.get("/me")
    finally:
        main_module.app.dependency_overrides.pop(
            main_module.get_current_user,
            None,
        )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "user@example.com",
    }


def test_me_endpoint_rejects_missing_token() -> None:
    """Reject access to /me without a Bearer token."""

    response = client.get("/me")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated.",
    }
    assert response.headers["www-authenticate"] == "Bearer"


def test_history_endpoint_returns_current_user_analyses(
    mock_model_service: FakeModelService,
    monkeypatch,
) -> None:
    """Return previous analyses for the authenticated user."""

    analyses = [
        {
            "id": 2,
            "premise": "Water freezes at zero degrees Celsius.",
            "hypothesis": "Water can become ice.",
            "prediction": "ENTAILMENT",
            "confidence": 0.95,
            "entailment_score": 0.95,
            "neutral_score": 0.03,
            "contradiction_score": 0.02,
            "created_at": "2026-08-22T10:00:00",
        },
        {
            "id": 1,
            "premise": "The Earth revolves around the Sun.",
            "hypothesis": "The Sun revolves around the Earth.",
            "prediction": "CONTRADICTION",
            "confidence": 0.97,
            "entailment_score": 0.01,
            "neutral_score": 0.02,
            "contradiction_score": 0.97,
            "created_at": "2026-08-21T10:00:00",
        },
    ]

    requested_user_id: dict[str, int] = {}

    def fake_get_analyses_by_user(
    db,
    user_id: int,
    prediction=None,
    search=None,
    skip=0,
    limit=20,
):
        requested_user_id["value"] = user_id
        return analyses

    monkeypatch.setattr(
        main_module,
        "get_analyses_by_user",
        fake_get_analyses_by_user,
    )


    response = client.get("/history")

    assert response.status_code == 200
    assert requested_user_id["value"] == 1
    assert response.json() == analyses


def test_history_endpoint_filters_by_prediction(
    mock_model_service: FakeModelService,
    monkeypatch,
) -> None:
    """Filter analysis history by prediction."""

    analyses = [
        {
            "id": 2,
            "premise": "Water freezes at zero degrees Celsius.",
            "hypothesis": "Water can become ice.",
            "prediction": "ENTAILMENT",
            "confidence": 0.95,
            "entailment_score": 0.95,
            "neutral_score": 0.03,
            "contradiction_score": 0.02,
            "created_at": "2026-08-25T10:00:00",
        }
    ]

    requested_values = {}

    def fake_get_analyses_by_user(
    db,
    user_id: int,
    prediction=None,
    search=None,
    skip=0,
    limit=20,
):
        requested_values["user_id"] = user_id
        requested_values["prediction"] = prediction
        return analyses

    monkeypatch.setattr(
        main_module,
        "get_analyses_by_user",
        fake_get_analyses_by_user,
    )

    response = client.get("/history?prediction=ENTAILMENT")

    assert response.status_code == 200
    assert requested_values["user_id"] == 1
    assert requested_values["prediction"] == "ENTAILMENT"
    assert response.json() == analyses


def test_history_endpoint_filters_by_search(
    mock_model_service: FakeModelService,
    monkeypatch,
) -> None:
    """Filter analysis history by text search."""

    analyses = [
        {
            "id": 2,
            "premise": "Water freezes at zero degrees Celsius.",
            "hypothesis": "Water can become ice.",
            "prediction": "ENTAILMENT",
            "confidence": 0.95,
            "entailment_score": 0.95,
            "neutral_score": 0.03,
            "contradiction_score": 0.02,
            "created_at": "2026-08-25T10:00:00",
        }
    ]

    requested_values = {}

    def fake_get_analyses_by_user(
    db,
    user_id: int,
    prediction=None,
    search=None,
    skip=0,
    limit=20,
):

        requested_values["user_id"] = user_id
        requested_values["prediction"] = prediction
        requested_values["search"] = search
        return analyses

    monkeypatch.setattr(
        main_module,
        "get_analyses_by_user",
        fake_get_analyses_by_user,
    )

    response = client.get("/history?search=water")

    assert response.status_code == 200
    assert requested_values["user_id"] == 1
    assert requested_values["prediction"] is None
    assert requested_values["search"] == "water"
    assert response.json() == analyses


def test_history_endpoint_applies_pagination(
    mock_model_service: FakeModelService,
    monkeypatch,
) -> None:
    """Pass pagination parameters to analysis history."""

    requested_values = {}

    def fake_get_analyses_by_user(
        db,
        user_id: int,
        prediction=None,
        search=None,
        skip=0,
        limit=20,
    ):
        requested_values["user_id"] = user_id
        requested_values["skip"] = skip
        requested_values["limit"] = limit
        return []

    monkeypatch.setattr(
        main_module,
        "get_analyses_by_user",
        fake_get_analyses_by_user,
    )

    response = client.get("/history?skip=5&limit=10")

    assert response.status_code == 200
    assert requested_values["user_id"] == 1
    assert requested_values["skip"] == 5
    assert requested_values["limit"] == 10
    assert response.json() == []

def test_history_endpoint_rejects_invalid_prediction(
    mock_model_service: FakeModelService,
) -> None:
    """Reject unsupported prediction filters."""

    response = client.get("/history?prediction=UNKNOWN")

    assert response.status_code == 422

def test_history_endpoint_rejects_missing_token() -> None:
    """Reject access to history without a Bearer token."""

    response = client.get("/history")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated.",
    }
    assert response.headers["www-authenticate"] == "Bearer"


def test_history_detail_returns_current_user_analysis(
    mock_model_service: FakeModelService,
    monkeypatch,
) -> None:
    """Return one analysis owned by the authenticated user."""

    analysis = {
        "id": 7,
        "premise": "Water freezes at zero degrees Celsius.",
        "hypothesis": "Water can become ice.",
        "prediction": "ENTAILMENT",
        "confidence": 0.95,
        "entailment_score": 0.95,
        "neutral_score": 0.03,
        "contradiction_score": 0.02,
        "created_at": "2026-08-23T10:00:00",
    }

    requested_values: dict[str, int] = {}

    def fake_get_analysis_by_id_for_user(
        db,
        user_id: int,
        analysis_id: int,
    ):
        requested_values["user_id"] = user_id
        requested_values["analysis_id"] = analysis_id
        return analysis

    monkeypatch.setattr(
        main_module,
        "get_analysis_by_id_for_user",
        fake_get_analysis_by_id_for_user,
    )

    response = client.get("/history/7")

    assert response.status_code == 200
    assert requested_values["user_id"] == 1
    assert requested_values["analysis_id"] == 7
    assert response.json() == analysis


def test_history_detail_returns_404_when_analysis_not_found(
    mock_model_service: FakeModelService,
    monkeypatch,
) -> None:
    """Return 404 when the requested analysis is unavailable."""

    monkeypatch.setattr(
        main_module,
        "get_analysis_by_id_for_user",
        lambda db, user_id, analysis_id: None,
    )

    response = client.get("/history/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Analysis not found.",
    }


def test_history_delete_removes_current_user_analysis(
    mock_model_service: FakeModelService,
    monkeypatch,
) -> None:
    """Delete an analysis owned by the authenticated user."""

    requested_values: dict[str, int] = {}

    def fake_delete_analysis_by_id_for_user(
        db,
        user_id: int,
        analysis_id: int,
    ) -> bool:
        requested_values["user_id"] = user_id
        requested_values["analysis_id"] = analysis_id
        return True

    monkeypatch.setattr(
        main_module,
        "delete_analysis_by_id_for_user",
        fake_delete_analysis_by_id_for_user,
    )

    response = client.delete("/history/7")

    assert response.status_code == 204
    assert response.content == b""
    assert requested_values["user_id"] == 1
    assert requested_values["analysis_id"] == 7


def test_history_delete_returns_404_when_analysis_not_found(
    mock_model_service: FakeModelService,
    monkeypatch,
) -> None:
    """Return 404 when the requested analysis cannot be deleted."""

    monkeypatch.setattr(
        main_module,
        "delete_analysis_by_id_for_user",
        lambda db, user_id, analysis_id: False,
    )

    response = client.delete("/history/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Analysis not found.",
    }