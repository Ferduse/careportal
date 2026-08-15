from dataclasses import dataclass
from datetime import datetime, timezone

from app.core.errors import AppError, NotFoundError


@dataclass
class AppointmentRecord:
    id: int
    user_id: int
    provider_name: str
    start_time: datetime
    end_time: datetime
    reason: str
    status: str


class AppointmentService:
    def __init__(self) -> None:
        self._appointments_by_id: dict[int, AppointmentRecord] = {}
        self._next_id = 1

    def create_appointment(
        self,
        user_id: int,
        provider_name: str,
        start_time: datetime,
        end_time: datetime,
        reason: str,
    ) -> AppointmentRecord:
        self._validate_time_range(start_time, end_time)
        self._validate_not_in_past(start_time)
        self._ensure_no_conflict(user_id, provider_name, start_time, end_time)

        appointment = AppointmentRecord(
            id=self._next_id,
            user_id=user_id,
            provider_name=provider_name.strip(),
            start_time=start_time,
            end_time=end_time,
            reason=reason.strip(),
            status="scheduled",
        )
        self._appointments_by_id[appointment.id] = appointment
        self._next_id += 1
        return appointment

    def list_appointments(self, user_id: int) -> list[AppointmentRecord]:
        items = [a for a in self._appointments_by_id.values() if a.user_id == user_id]
        return sorted(items, key=lambda x: x.start_time)

    def get_appointment(self, user_id: int, appointment_id: int) -> AppointmentRecord:
        appointment = self._appointments_by_id.get(appointment_id)
        if not appointment or appointment.user_id != user_id:
            raise NotFoundError("Appointment not found")
        return appointment

    def update_appointment(
        self,
        user_id: int,
        appointment_id: int,
        provider_name: str | None,
        start_time: datetime | None,
        end_time: datetime | None,
        reason: str | None,
        status: str | None,
    ) -> AppointmentRecord:
        appointment = self.get_appointment(user_id, appointment_id)
        if appointment.status == "canceled":
            raise AppError("Canceled appointments cannot be updated", 400, "bad_request")

        new_provider = provider_name.strip() if provider_name is not None else appointment.provider_name
        new_start = start_time if start_time is not None else appointment.start_time
        new_end = end_time if end_time is not None else appointment.end_time

        self._validate_time_range(new_start, new_end)
        self._validate_not_in_past(new_start)
        self._ensure_no_conflict(user_id, new_provider, new_start, new_end, skip_id=appointment.id)

        appointment.provider_name = new_provider
        appointment.start_time = new_start
        appointment.end_time = new_end
        if reason is not None:
            appointment.reason = reason.strip()
        if status is not None:
            appointment.status = status
        return appointment

    def cancel_appointment(self, user_id: int, appointment_id: int) -> AppointmentRecord:
        appointment = self.get_appointment(user_id, appointment_id)
        appointment.status = "canceled"
        return appointment

    def _validate_time_range(self, start_time: datetime, end_time: datetime) -> None:
        if end_time <= start_time:
            raise AppError("End time must be after start time", 400, "bad_request")

    def _validate_not_in_past(self, start_time: datetime) -> None:
        now = datetime.now(timezone.utc)
        check_time = start_time if start_time.tzinfo else start_time.replace(tzinfo=timezone.utc)
        if check_time < now:
            raise AppError("Cannot book appointments in the past", 400, "bad_request")

    def _ensure_no_conflict(
        self,
        user_id: int,
        provider_name: str,
        start_time: datetime,
        end_time: datetime,
        skip_id: int | None = None,
    ) -> None:
        for appointment in self._appointments_by_id.values():
            if appointment.user_id != user_id:
                continue
            if appointment.status == "canceled":
                continue
            if appointment.provider_name != provider_name:
                continue
            if skip_id is not None and appointment.id == skip_id:
                continue
            overlaps = start_time < appointment.end_time and end_time > appointment.start_time
            if overlaps:
                raise AppError("Appointment overlaps an existing time slot", 409, "conflict")


appointment_service = AppointmentService()
