"""Main FastAPI application for the Scientific Claim Verifier."""

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.app.model_service import get_model_service


app = FastAPI(
    title="Scientific Claim Verifier API",
    description=(
        "Backend API for the NLI-based scientific "
        "claim verification platform."
    ),
    version="1.0.0",
)


class PredictionRequest(BaseModel):
    """Input sentences required for NLI prediction."""

    premise: str
    hypothesis: str


@app.get("/")
def read_root() -> dict[str, str]:
    """Return basic information about the API."""

    return {
        "message": "Scientific Claim Verifier API is running",
        "status": "success",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Check whether the backend is working."""

    return {
        "status": "healthy",
    }


@app.post("/predict")
def predict_claim(
    request: PredictionRequest,
) -> dict[str, Any]:
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

    return {
        "premise": premise,
        "hypothesis": hypothesis,
        **prediction_result,
    }