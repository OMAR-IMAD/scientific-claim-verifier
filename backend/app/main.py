"""Main FastAPI application for the Scientific Claim Verifier."""

from fastapi import FastAPI, HTTPException

from backend.app.model_service import get_model_service
from backend.app.schemas import (
    ErrorResponse,
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
    RootResponse,
)


app = FastAPI(
    title="Scientific Claim Verifier API",
    description=(
        "Backend API for the NLI-based scientific "
        "claim verification platform."
    ),
    version="1.0.0",
)


@app.get(
    "/",
    response_model=RootResponse,
    summary="Read API status",
    description="Return basic information about the API.",
)
def read_root() -> RootResponse:
    """Return basic information about the API."""

    return RootResponse(
        message="Scientific Claim Verifier API is running",
        status="success",
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Check backend health",
    description="Check whether the backend application is working.",
)
def health_check() -> HealthResponse:
    """Check whether the backend is working."""

    return HealthResponse(
        status="healthy",
    )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Verify a claim",
    description=(
        "Classify the relationship between a premise and hypothesis "
        "as Entailment, Neutral, or Contradiction."
    ),
responses={
    200: {
        "description": "Successful claim verification response.",
        "content": {
            "application/json": {
                "example": {
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
            }
        },
    },
    422: {
        "model": ErrorResponse,
        "description": "Invalid input data.",
        "content": {
            "application/json": {
                "examples": {
                    "empty_premise": {
                        "summary": "Empty premise",
                        "value": {
                            "detail": "Premise cannot be empty.",
                        },
                    },
                    "empty_hypothesis": {
                        "summary": "Empty hypothesis",
                        "value": {
                            "detail": "Hypothesis cannot be empty.",
                        },
                    },
                }
            }
        },
    },
    },
)
def predict_claim(
    request: PredictionRequest,
) -> PredictionResponse:
    """Predict the relationship between premise and hypothesis."""

    premise = request.premise.strip()
    hypothesis = request.hypothesis.strip()

    if not premise:
        raise HTTPException(
            status_code=422,
            detail="Premise cannot be empty.",
        )

    if not hypothesis:
        raise HTTPException(
            status_code=422,
            detail="Hypothesis cannot be empty.",
        )

    model_service = get_model_service()

    prediction_result = model_service.predict(
        premise=premise,
        hypothesis=hypothesis,
    )

    return PredictionResponse(
        premise=premise,
        hypothesis=hypothesis,
        **prediction_result,
    )