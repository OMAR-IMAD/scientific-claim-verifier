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

MODEL_SERVICE_UNAVAILABLE = "Model service is unavailable."
MODEL_SERVICE_NOT_READY = "Model service is not ready."
PREDICTION_FAILED = "Prediction failed."

def get_ready_model_service():
    """Return the model service when it is available and ready."""

    try:
        model_service = get_model_service()
    except Exception:
        raise HTTPException(
            status_code=503,
            detail=MODEL_SERVICE_UNAVAILABLE,
        )

    if not model_service.is_ready():
        raise HTTPException(
            status_code=503,
            detail=MODEL_SERVICE_NOT_READY,
        )

    return model_service

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
    """Check whether the backend and model are ready."""

    try:
        model_service = get_model_service()
        model_ready = model_service.is_ready()

        if not model_ready:
            return HealthResponse(
                status="degraded",
                model_ready=False,
                model_status="not_ready",
                device=str(
                    getattr(
                        model_service,
                        "device",
                        "unknown",
                    )
                ),
                detail=MODEL_SERVICE_NOT_READY,
            )

        return HealthResponse(
            status="healthy",
            model_ready=True,
            model_status="ready",
            device=str(model_service.device),
            detail=None,
        )

    except Exception as error:
        return HealthResponse(
            status="degraded",
            model_ready=False,
            model_status="unavailable",
            device=None,
            detail=str(error),
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
        500: {
            "model": ErrorResponse,
            "description": "Prediction execution failed.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": PREDICTION_FAILED,
                    }
                }
            },
        },
        503: {
            "model": ErrorResponse,
            "description": "Model service is unavailable or not ready.",
            "content": {
                "application/json": {
                    "examples": {
                        "service_unavailable": {
                            "summary": "Model service unavailable",
                            "value": {
                                "detail": MODEL_SERVICE_UNAVAILABLE,
                            },
                        },
                        "model_not_ready": {
                            "summary": "Model not ready",
                            "value": {
                                "detail": MODEL_SERVICE_NOT_READY,
                            },
                        },
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

    model_service = get_ready_model_service()

    try:
        prediction_result = model_service.predict(
            premise=premise,
            hypothesis=hypothesis,
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=PREDICTION_FAILED,
        )

    return PredictionResponse(
        premise=premise,
        hypothesis=hypothesis,
        **prediction_result,
    )