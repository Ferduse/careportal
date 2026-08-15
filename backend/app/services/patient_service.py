from dataclasses import dataclass

from app.core.errors import NotFoundError


@dataclass
class PatientProfileRecord:
    user_id: int
    full_name: str
    age: int
    gender: str
    bmi: float


class PatientService:
    def __init__(self) -> None:
        self._profiles_by_user_id: dict[int, PatientProfileRecord] = {}

    def upsert_profile(self, user_id: int, full_name: str, age: int, gender: str, bmi: float) -> PatientProfileRecord:
        profile = PatientProfileRecord(
            user_id=user_id,
            full_name=full_name.strip(),
            age=age,
            gender=gender.strip(),
            bmi=bmi,
        )
        self._profiles_by_user_id[user_id] = profile
        return profile

    def get_profile(self, user_id: int) -> PatientProfileRecord:
        profile = self._profiles_by_user_id.get(user_id)
        if not profile:
            raise NotFoundError("Patient profile not found")
        return profile


patient_service = PatientService()
