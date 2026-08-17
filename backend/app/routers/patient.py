from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.schemas.patient import PatientProfileResponse, PatientProfileUpsertRequest
from app.services.auth_service import UserRecord
from app.services.patient_service import patient_service


router = APIRouter(prefix="/api/v1/patient", tags=["patient"])


@router.get("/profile", response_model=PatientProfileResponse)
def get_profile(
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PatientProfileResponse:
    profile = patient_service.get_profile(db, current_user.id)
    return PatientProfileResponse(
        user_id=profile.user_id,
        full_name=profile.full_name,
        age=profile.age,
        gender=profile.gender,
        bmi=profile.bmi,
    )


@router.put("/profile", response_model=PatientProfileResponse)
def upsert_profile(
    payload: PatientProfileUpsertRequest,
    current_user: UserRecord = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PatientProfileResponse:
    profile = patient_service.upsert_profile(
        db=db,
        user_id=current_user.id,
        full_name=payload.full_name,
        age=payload.age,
        gender=payload.gender,
        bmi=payload.bmi,
    )
    return PatientProfileResponse(
        user_id=profile.user_id,
        full_name=profile.full_name,
        age=profile.age,
        gender=profile.gender,
        bmi=profile.bmi,
    )
