from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.db.models import PatientProfile
from app.db.sql_queries import get_sql_query


PatientProfileRecord = PatientProfile


class PatientService:
    def upsert_profile(
        self,
        db: Session,
        user_id: int,
        full_name: str,
        age: int,
        gender: str,
        bmi: float,
    ) -> PatientProfileRecord:
        # Upsert keeps one profile per user and updates values on repeated saves.
        profile_stmt = select(PatientProfile).from_statement(text(get_sql_query("get_patient_profile_by_user_id")))
        profile = db.scalar(profile_stmt, params={"user_id": user_id})
        if profile is None:
            profile = PatientProfile(
                user_id=user_id,
                full_name=full_name.strip(),
                age=age,
                gender=gender.strip(),
                bmi=bmi,
            )
            db.add(profile)
        else:
            profile.full_name = full_name.strip()
            profile.age = age
            profile.gender = gender.strip()
            profile.bmi = bmi

        db.commit()
        db.refresh(profile)
        return profile

    def get_profile(self, db: Session, user_id: int) -> PatientProfileRecord:
        profile_stmt = select(PatientProfile).from_statement(text(get_sql_query("get_patient_profile_by_user_id")))
        profile = db.scalar(profile_stmt, params={"user_id": user_id})
        if not profile:
            raise NotFoundError("Patient profile not found")
        return profile


patient_service = PatientService()
