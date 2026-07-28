from pydantic import BaseModel, Field


class PatientProfileUpsertRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=1, le=120)
    gender: str = Field(min_length=1, max_length=30)
    bmi: float = Field(gt=0, le=100)


class PatientProfileResponse(BaseModel):
    user_id: int
    full_name: str
    age: int
    gender: str
    bmi: float
