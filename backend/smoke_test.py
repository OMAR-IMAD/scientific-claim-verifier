from __future__ import annotations

import warnings

warnings.filterwarnings(
    "ignore",
    message=r"Using `httpx` with `starlette\.testclient` is deprecated.*",
)

from fastapi.testclient import TestClient

from backend.app.main import app


EXPECTED_LABELS = {
    "ENTAILMENT",
    "NEUTRAL",
    "CONTRADICTION",
}


def main() -> None:
    """Run basic integration checks for the backend API."""

    client = TestClient(app)

    root_response = client.get("/")

    assert root_response.status_code == 200
    assert root_response.json()["status"] == "success"

    print("[PASS] Root endpoint")


    health_response = client.get("/health")

    assert health_response.status_code == 200
    assert health_response.json() == {
        "status": "healthy",
    }

    print("[PASS] Health endpoint")


    prediction_response = client.post(
        "/predict",
        json={
            "premise": "A man is playing a guitar.",
            "hypothesis": "A person is making music.",
        },
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
    )

    assert empty_hypothesis_response.status_code == 422

    assert empty_hypothesis_response.json() == {
        "detail": "Hypothesis cannot be empty.",
    }

    print("[PASS] Empty hypothesis validation")

    print("\nAll backend smoke tests passed.")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print("\nBackend smoke test failed.")
        raise SystemExit(1) from error