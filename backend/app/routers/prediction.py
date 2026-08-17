from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.schemas.prediction import PredictionHistoryResponse, PredictionRequest, PredictionResponse
from app.services.auth_service import UserRecord
from app.services.prediction_service import PredictionRecord, prediction_service


router = APIRouter(prefix="/api/v1/predictions", tags=["predictions"])


def _to_response(record: PredictionRecord) -> PredictionResponse:
    return PredictionResponse(
        id=record.id,
        user_id=record.user_id,
        risk_label=record.risk_label,
        risk_score=record.risk_score,
        created_at=record.created_at,
    )


@router.post("", response_model=PredictionResponse, status_code=201)
def predict(
    payload: PredictionRequest,
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PredictionResponse:
    record = prediction_service.predict(
        db=db,
        user_id=current_user.id,
        age=payload.age,
        gender=payload.gender,
        hypertension=payload.hypertension,
        heart_disease=payload.heart_disease,
        smoking_history=payload.smoking_history,
        bmi=payload.bmi,
        HbA1c_level=payload.HbA1c_level,
        blood_glucose_level=payload.blood_glucose_level,
    )
    return _to_response(record)


@router.get("", response_model=list[PredictionHistoryResponse])
def list_predictions(
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[PredictionHistoryResponse]:
    items = prediction_service.list_predictions(db, current_user.id)
    return [
        PredictionHistoryResponse(
            id=item.id,
            user_id=item.user_id,
            risk_label=item.risk_label,
            risk_score=item.risk_score,
            created_at=item.created_at,
        )
        for item in items
    ]
