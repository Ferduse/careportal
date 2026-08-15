from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Gender = Literal["Female", "Male", "Other"]
SmokingHistory = Literal["No Info", "current", "ever", "former", "never", "not current",]


class PredictionRequest(BaseModel):
    age: int = Field(ge=1, le=120)
    gender: Gender
    hypertension: bool
    heart_disease: bool
    smoking_history: SmokingHistory
    bmi: float = Field(gt=0, le=100)
    HbA1c_level: float = Field(ge=0, le=20)
    blood_glucose_level: float = Field(ge=0, le=500)


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
