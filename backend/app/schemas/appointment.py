from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


AppointmentStatus = Literal["scheduled", "completed", "canceled"]


class AppointmentCreateRequest(BaseModel):
    provider_name: str = Field(min_length=2, max_length=100)
    start_time: datetime
    end_time: datetime
    reason: str = Field(min_length=2, max_length=300)


class AppointmentUpdateRequest(BaseModel):
    provider_name: str | None = Field(default=None, min_length=2, max_length=100)
    start_time: datetime | None = None
    end_time: datetime | None = None
    reason: str | None = Field(default=None, min_length=2, max_length=300)
    status: AppointmentStatus | None = None


class AppointmentResponse(BaseModel):
    id: int
    user_id: int
    provider_name: str
    start_time: datetime
    end_time: datetime
    reason: str
    status: AppointmentStatus
