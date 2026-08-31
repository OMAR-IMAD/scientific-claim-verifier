"""Main FastAPI application for the Scientific Claim Verifier."""

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.crud import (
    create_analysis,
    create_user,
    delete_analysis_by_id_for_user,
    get_analyses_by_user,
    get_analysis_by_id_for_user,
    get_analysis_stats_by_user,
    get_user_by_email,
)
from backend.app.models import Analysis, User
from backend.app.model_service import get_model_service
from backend.app.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from backend.app.schemas import (
    AnalysisResponse,
    DashboardStatsResponse,
    ErrorResponse,
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
    RootResponse,
    UserCreate,
    UserResponse,
    TokenResponse,
    UserLogin,
    PredictionLabel,
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
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Register a new user",
)
def register_user(
    request: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Register a new application user."""

    existing_user = get_user_by_email(db, request.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered.",
        )

    user = create_user(
        db,
        request.email,
        hash_password(request.password),
    )

    return UserResponse.model_validate(user)


@app.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in a user",
)
def login_user(
    request: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate a user and return a JWT access token."""

    user = get_user_by_email(db, request.email)

    if user is None or not verify_password(
        request.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    return TokenResponse(
        access_token=create_access_token(user.email),
    )


@app.get(
    "/me",
    response_model=UserResponse,
    summary="Read current user",
)
def read_current_user(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Return the currently authenticated user."""

    return UserResponse.model_validate(current_user)


@app.get(
    "/history",
    response_model=list[AnalysisResponse],
    summary="Read analysis history",
    description="Return previous analyses for the authenticated user.",
)
def read_analysis_history(
    prediction: PredictionLabel | None = None,
    search: str | None = None,
       sort_order: str = Query("newest", pattern="^(newest|oldest)$"),
    skip: int = Query(0, ge=0),
       limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AnalysisResponse]:
    """Return the authenticated user's previous analyses."""

    return get_analyses_by_user(
    db,
    current_user.id,
    prediction,
    search,
    sort_order,
    skip,
    limit,
)


@app.get(
    "/dashboard/stats",
    response_model=DashboardStatsResponse,
    summary="Read dashboard statistics",
    description="Return analysis statistics for the authenticated user.",
)
def read_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardStatsResponse:
    """Return dashboard statistics for the authenticated user."""

    return get_analysis_stats_by_user(db, current_user.id)

@app.get(
    "/history/{analysis_id}",
    response_model=AnalysisResponse,
    summary="Read analysis details",
    description="Return a specific analysis owned by the authenticated user.",
)
def read_analysis_detail(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AnalysisResponse:
    """Return one analysis belonging to the authenticated user."""

    analysis = get_analysis_by_id_for_user(
        db,
        current_user.id,
        analysis_id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found.",
        )

    return AnalysisResponse.model_validate(analysis)


@app.delete(
    "/history/{analysis_id}",
    status_code=204,
    summary="Delete analysis",
    description="Delete a specific analysis owned by the authenticated user.",
)
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete one analysis belonging to the authenticated user."""

    deleted = delete_analysis_by_id_for_user(
        db,
        current_user.id,
        analysis_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found.",
        )

    return None

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PredictionResponse:
    """Predict the relationship between premise and hypothesis."""

    premise = request.premise
    hypothesis = request.hypothesis

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


    create_analysis(
        db,
        user_id=current_user.id,
        premise=premise,
        hypothesis=hypothesis,
        prediction=prediction_result["prediction"],
        confidence=prediction_result["confidence"],
        entailment_score=prediction_result["scores"]["ENTAILMENT"],
        neutral_score=prediction_result["scores"]["NEUTRAL"],
        contradiction_score=prediction_result["scores"]["CONTRADICTION"],
    )

    return PredictionResponse(
        premise=premise,
        hypothesis=hypothesis,
        **prediction_result,
    )