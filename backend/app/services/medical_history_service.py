from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.db.models import MedicalHistory
from app.db.sql_queries import get_sql_query


MedicalHistoryRecord = MedicalHistory


class MedicalHistoryService:
    def create_record(self, db: Session, user_id: int, condition_name: str, notes: str) -> MedicalHistoryRecord:
        record = MedicalHistory(
            user_id=user_id,
            condition_name=condition_name.strip(),
            notes=notes.strip(),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def list_records(self, db: Session, user_id: int) -> list[MedicalHistoryRecord]:
        statement = select(MedicalHistory).from_statement(text(get_sql_query("list_medical_history_for_user")))
        return list(db.scalars(statement, params={"user_id": user_id}).all())

    def update_record(
        self,
        db: Session,
        user_id: int,
        record_id: int,
        condition_name: str | None,
        notes: str | None,
    ) -> MedicalHistoryRecord:
        statement = select(MedicalHistory).from_statement(text(get_sql_query("get_medical_history_for_user")))
        record = db.scalar(statement, params={"record_id": record_id, "user_id": user_id})
        if not record:
            raise NotFoundError("Medical history record not found")

        if condition_name is not None:
            record.condition_name = condition_name.strip()
        if notes is not None:
            record.notes = notes.strip()

        db.commit()
        db.refresh(record)
        return record


medical_history_service = MedicalHistoryService()
