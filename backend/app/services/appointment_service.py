from datetime import datetime, timezone

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.errors import AppError, NotFoundError
from app.db.models import Appointment
from app.db.sql_queries import get_sql_query


AppointmentRecord = Appointment


class AppointmentService:
    def create_appointment(
        self,
        db: Session,
        user_id: int,
        provider_name: str,
        start_time: datetime,
        end_time: datetime,
        reason: str,
    ) -> AppointmentRecord:
        self._validate_time_range(start_time, end_time)
        self._validate_not_in_past(start_time)
        self._ensure_no_conflict(db, user_id, provider_name, start_time, end_time)

        appointment = Appointment(
            user_id=user_id,
            provider_name=provider_name.strip(),
            start_time=start_time,
            end_time=end_time,
            reason=reason.strip(),
            status="scheduled",
        )
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment

    def list_appointments(self, db: Session, user_id: int) -> list[AppointmentRecord]:
        statement = select(Appointment).from_statement(text(get_sql_query("list_appointments_for_user")))
        return list(db.scalars(statement, params={"user_id": user_id}).all())

    def get_appointment(self, db: Session, user_id: int, appointment_id: int) -> AppointmentRecord:
        statement = select(Appointment).from_statement(text(get_sql_query("get_appointment_for_user")))
        appointment = db.scalar(statement, params={"appointment_id": appointment_id, "user_id": user_id})
        if not appointment:
            raise NotFoundError("Appointment not found")
        return appointment

    def update_appointment(
        self,
        db: Session,
        user_id: int,
        appointment_id: int,
        provider_name: str | None,
        start_time: datetime | None,
        end_time: datetime | None,
        reason: str | None,
        status: str | None,
    ) -> AppointmentRecord:
        appointment = self.get_appointment(db, user_id, appointment_id)
        if appointment.status == "canceled":
            raise AppError("Canceled appointments cannot be updated", 400, "bad_request")

        new_provider = provider_name.strip() if provider_name is not None else appointment.provider_name
        new_start = start_time if start_time is not None else appointment.start_time
        new_end = end_time if end_time is not None else appointment.end_time

        self._validate_time_range(new_start, new_end)
        self._validate_not_in_past(new_start)
        self._ensure_no_conflict(db, user_id, new_provider, new_start, new_end, skip_id=appointment.id)

        appointment.provider_name = new_provider
        appointment.start_time = new_start
        appointment.end_time = new_end
        if reason is not None:
            appointment.reason = reason.strip()
        if status is not None:
            appointment.status = status

        db.commit()
        db.refresh(appointment)
        return appointment

    def cancel_appointment(self, db: Session, user_id: int, appointment_id: int) -> AppointmentRecord:
        appointment = self.get_appointment(db, user_id, appointment_id)
        appointment.status = "canceled"
        db.commit()
        db.refresh(appointment)
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
        db: Session,
        user_id: int,
        provider_name: str,
        start_time: datetime,
        end_time: datetime,
        skip_id: int | None = None,
    ) -> None:
        statement = select(Appointment).from_statement(text(get_sql_query("find_appointment_conflict")))
        conflict = db.scalar(
            statement,
            params={
                "user_id": user_id,
                "provider_name": provider_name.strip(),
                "start_time": start_time,
                "end_time": end_time,
                "skip_id": skip_id,
            },
        )
        if conflict is not None:
            raise AppError("Appointment overlaps an existing time slot", 409, "conflict")


appointment_service = AppointmentService()
