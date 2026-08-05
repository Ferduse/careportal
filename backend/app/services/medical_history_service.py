from dataclasses import dataclass
from datetime import datetime, timezone

from app.core.errors import NotFoundError


@dataclass
class MedicalHistoryRecord:
    id: int
    user_id: int
    condition_name: str
    notes: str
    created_at: datetime


class MedicalHistoryService:
    def __init__(self) -> None:
        self._records_by_id: dict[int, MedicalHistoryRecord] = {}
        self._next_id = 1

    def create_record(self, user_id: int, condition_name: str, notes: str) -> MedicalHistoryRecord:
        record = MedicalHistoryRecord(
            id=self._next_id,
            user_id=user_id,
            condition_name=condition_name.strip(),
            notes=notes.strip(),
            created_at=datetime.now(timezone.utc),
        )
        self._records_by_id[record.id] = record
        self._next_id += 1
        return record

    def list_records(self, user_id: int) -> list[MedicalHistoryRecord]:
        items = [r for r in self._records_by_id.values() if r.user_id == user_id]
        return sorted(items, key=lambda x: x.created_at, reverse=True)

    def update_record(
        self,
        user_id: int,
        record_id: int,
        condition_name: str | None,
        notes: str | None,
    ) -> MedicalHistoryRecord:
        record = self._records_by_id.get(record_id)
        if not record or record.user_id != user_id:
            raise NotFoundError("Medical history record not found")

        if condition_name is not None:
            record.condition_name = condition_name.strip()
        if notes is not None:
            record.notes = notes.strip()
        return record


medical_history_service = MedicalHistoryService()
