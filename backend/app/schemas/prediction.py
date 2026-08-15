from datetime import datetime
from typing import Any
from typing import Literal

from pydantic import AliasChoices, BaseModel, Field, field_validator

Gender = Literal["Female", "Male", "Other"]
SmokingHistory = Literal["No Info", "current", "ever", "former", "never", "not current",]


class PredictionRequest(BaseModel):
    age: int = Field(ge=1, le=120)
    gender: Gender
    hypertension: bool
    heart_disease: bool
    smoking_history: SmokingHistory
    bmi: float = Field(gt=0, le=100)
    # Accept both the newer field name and older client payload key.
    HbA1c_level: float = Field(
        ge=0,
        le=20,
        validation_alias=AliasChoices("HbA1c_level", "hbA1c_level"),
    )
    blood_glucose_level: float = Field(ge=0, le=500)

    # Normalize case so legacy lowercase values like "female" still validate.
    @field_validator("gender", mode="before")
    @classmethod
    def normalize_gender(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError("gender must be a string")
        mapping = {
            "female": "Female",
            "male": "Male",
            "other": "Other",
        }
        normalized = mapping.get(value.strip().lower())
        if normalized is None:
            raise ValueError("gender must be one of: Female, Male, Other")
        return normalized

    # Normalize separators/case so variants like "not_current" are accepted.
    @field_validator("smoking_history", mode="before")
    @classmethod
    def normalize_smoking_history(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError("smoking_history must be a string")
        key = value.strip().lower().replace("_", " ")
        mapping = {
            "no info": "No Info",
            "current": "current",
            "ever": "ever",
            "former": "former",
            "never": "never",
            "not current": "not current",
        }
        normalized = mapping.get(key)
        if normalized is None:
            raise ValueError(
                "smoking_history must be one of: No Info, current, ever, former, never, not current"
            )
        return normalized


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
