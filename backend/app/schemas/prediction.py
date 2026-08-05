from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


SmokingHistory = Literal["never", "former", "current"]


class PredictionRequest(BaseModel):
    age: int = Field(ge=1, le=120)
    gender: str = Field(min_length=1, max_length=30)
    bmi: float = Field(gt=0, le=100)
    hbA1c_level: float = Field(ge=0, le=20)
    blood_glucose_level: float = Field(ge=0, le=500)
    hypertension: bool
    heart_disease: bool
    smoking_history: SmokingHistory


class PredictionResponse(BaseModel):
    id: int
    user_id: int
    risk_label: str
    risk_score: float
    created_at: datetime


class PredictionHistoryResponse(BaseModel):
    id: int
    user_id: int
    risk_label: str
    risk_score: float
    created_at: datetime
