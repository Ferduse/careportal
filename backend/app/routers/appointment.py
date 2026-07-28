from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.schemas.appointment import (
    AppointmentCreateRequest,
    AppointmentResponse,
    AppointmentUpdateRequest,
)
from app.services.appointment_service import AppointmentRecord, appointment_service
from app.services.auth_service import UserRecord


router = APIRouter(prefix="/api/v1/appointments", tags=["appointments"])


def _to_response(appointment: AppointmentRecord) -> AppointmentResponse:
    return AppointmentResponse(
        id=appointment.id,
        user_id=appointment.user_id,
        provider_name=appointment.provider_name,
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        reason=appointment.reason,
        status=appointment.status,
    )


@router.post("", response_model=AppointmentResponse, status_code=201)
def create_appointment(
    payload: AppointmentCreateRequest,
    current_user: UserRecord = Depends(get_current_user),
) -> AppointmentResponse:
    appointment = appointment_service.create_appointment(
        user_id=current_user.id,
        provider_name=payload.provider_name,
        start_time=payload.start_time,
        end_time=payload.end_time,
        reason=payload.reason,
    )
    return _to_response(appointment)


@router.get("", response_model=list[AppointmentResponse])
def list_appointments(current_user: UserRecord = Depends(get_current_user)) -> list[AppointmentResponse]:
    appointments = appointment_service.list_appointments(current_user.id)
    return [_to_response(item) for item in appointments]


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    payload: AppointmentUpdateRequest,
    current_user: UserRecord = Depends(get_current_user),
) -> AppointmentResponse:
    appointment = appointment_service.update_appointment(
        user_id=current_user.id,
        appointment_id=appointment_id,
        provider_name=payload.provider_name,
        start_time=payload.start_time,
        end_time=payload.end_time,
        reason=payload.reason,
        status=payload.status,
    )
    return _to_response(appointment)


@router.post("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(
    appointment_id: int,
    current_user: UserRecord = Depends(get_current_user),
) -> AppointmentResponse:
    appointment = appointment_service.cancel_appointment(
        user_id=current_user.id,
        appointment_id=appointment_id,
    )
    return _to_response(appointment)
