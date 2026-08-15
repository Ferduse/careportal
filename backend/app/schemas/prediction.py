from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

# Required canonical values for gender: "Female", "Male", "Other" (case-sensitive)
Gender = Literal["Female", "Male", "Other"]
# Required canonical values for smoking_history: "No Info", "current", "ever", "former", "never", "not current"
SmokingHistory = Literal["No Info", "current", "ever", "former", "never", "not current",]


class PredictionRequest(BaseModel):
    age: int = Field(ge=1, le=120)
    # Required key: gender — must be exactly one of the Gender literal values above
    gender: Gender
    hypertension: bool
    heart_disease: bool
    # Required key: smoking_history — must be exactly one of the SmokingHistory literal values above
    smoking_history: SmokingHistory
    bmi: float = Field(gt=0, le=100)
    # Required key: HbA1c_level (capital H, lowercase b, uppercase A1c) — hbA1c_level is not accepted
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
