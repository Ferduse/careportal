from datetime import datetime

from pydantic import BaseModel, Field


class MedicalHistoryCreateRequest(BaseModel):
    condition_name: str = Field(min_length=2, max_length=100)
    notes: str = Field(min_length=2, max_length=500)


class MedicalHistoryUpdateRequest(BaseModel):
    condition_name: str | None = Field(default=None, min_length=2, max_length=100)
    notes: str | None = Field(default=None, min_length=2, max_length=500)


class MedicalHistoryResponse(BaseModel):
    id: int
    user_id: int
    condition_name: str
    notes: str
    created_at: datetime
