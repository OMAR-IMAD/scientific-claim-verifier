from __future__ import annotations

import warnings

import uuid

from sqlalchemy import delete

warnings.filterwarnings(
    "ignore",
    message=r"Using `httpx` with `starlette\.testclient` is deprecated.*",
)

from fastapi.testclient import TestClient

from backend.app.main import app

from backend.app.database import SessionLocal
from backend.app.models import Analysis, User

EXPECTED_LABELS = {
    "ENTAILMENT",
    "NEUTRAL",
    "CONTRADICTION",
}


def main() -> None:
    """Run basic integration checks for the backend API."""

    client = TestClient(app)

    email = f"smoke_{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPassword123!"

    register_response = client.post(
        "/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201
    user_id = register_response.json()["id"]
    print("[PASS] Register endpoint")

    login_response = client.post(
        "/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]
    auth_headers = {
        "Authorization": f"Bearer {access_token}",
    }

    print("[PASS] Login endpoint")

    root_response = client.get("/")

    assert root_response.status_code == 200
    assert root_response.json()["status"] == "success"

    print("[PASS] Root endpoint")


    health_response = client.get("/health")

    assert health_response.status_code == 200

    health_data = health_response.json()

    assert health_data["status"] == "healthy"
    assert health_data["model_ready"] is True
    assert health_data["model_status"] == "ready"
    assert health_data["device"] in {"cpu", "cuda"}
    assert health_data["detail"] is None

    print("[PASS] Health endpoint")

    prediction_response = client.post(
    "/predict",
    json={
        "premise": "A man is playing a guitar.",
        "hypothesis": "A person is making music.",
    },
    headers=auth_headers,
)

    assert prediction_response.status_code == 200

    prediction_data = prediction_response.json()

    required_fields = {
        "premise",
        "hypothesis",
        "prediction",
        "confidence",
        "scores",
        "device",
    }

    assert required_fields.issubset(
        prediction_data.keys()
    )

    assert (
        prediction_data["prediction"]
        in EXPECTED_LABELS
    )

    assert (
        0.0
        <= prediction_data["confidence"]
        <= 1.0
    )

    assert set(
        prediction_data["scores"].keys()
    ) == EXPECTED_LABELS

    scores_total = sum(
        prediction_data["scores"].values()
    )

    assert abs(scores_total - 1.0) < 0.001

    print(
        "[PASS] Predict endpoint:",
        prediction_data["prediction"],
        prediction_data["confidence"],
        prediction_data["device"],
    )


    empty_premise_response = client.post(
    "/predict",
    json={
        "premise": "   ",
        "hypothesis": "Valid hypothesis",
    },
    headers=auth_headers,
)

    assert empty_premise_response.status_code == 422

    assert empty_premise_response.json() == {
        "detail": "Premise cannot be empty.",
    }

    print("[PASS] Empty premise validation")


    empty_hypothesis_response = client.post(
    "/predict",
    json={
        "premise": "Valid premise",
        "hypothesis": "   ",
    },
    headers=auth_headers,
)

    assert empty_hypothesis_response.status_code == 422

    assert empty_hypothesis_response.json() == {
        "detail": "Hypothesis cannot be empty.",
    }

    print("[PASS] Empty hypothesis validation")

    db = SessionLocal()
    try:
        db.execute(
            delete(Analysis).where(Analysis.user_id == user_id)
        )
        db.execute(
            delete(User).where(User.id == user_id)
        )
        db.commit()
    finally:
        db.close()

    print("[PASS] Smoke test data cleanup")

    print("\nAll backend smoke tests passed.")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print("\nBackend smoke test failed.")
        raise SystemExit(1) from error