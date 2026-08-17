from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.schemas.medical_history import (
    MedicalHistoryCreateRequest,
    MedicalHistoryResponse,
    MedicalHistoryUpdateRequest,
)
from app.services.auth_service import UserRecord
from app.services.medical_history_service import MedicalHistoryRecord, medical_history_service


router = APIRouter(prefix="/api/v1/medical-history", tags=["medical_history"])


def _to_response(record: MedicalHistoryRecord) -> MedicalHistoryResponse:
    return MedicalHistoryResponse(
        id=record.id,
        user_id=record.user_id,
        condition_name=record.condition_name,
        notes=record.notes,
        created_at=record.created_at,
    )


@router.post("", response_model=MedicalHistoryResponse, status_code=201)
def create_medical_history(
    payload: MedicalHistoryCreateRequest,
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MedicalHistoryResponse:
    record = medical_history_service.create_record(
        db=db,
        user_id=current_user.id,
        condition_name=payload.condition_name,
        notes=payload.notes,
    )
    return _to_response(record)


@router.get("", response_model=list[MedicalHistoryResponse])
def list_medical_history(
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[MedicalHistoryResponse]:
    records = medical_history_service.list_records(db, current_user.id)
    return [_to_response(item) for item in records]


@router.put("/{record_id}", response_model=MedicalHistoryResponse)
def update_medical_history(
    record_id: int,
    payload: MedicalHistoryUpdateRequest,
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MedicalHistoryResponse:
    record = medical_history_service.update_record(
        db=db,
        user_id=current_user.id,
        record_id=record_id,
        condition_name=payload.condition_name,
        notes=payload.notes,
    )
    return _to_response(record)
