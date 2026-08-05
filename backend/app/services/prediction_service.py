from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class PredictionRecord:
    id: int
    user_id: int
    risk_label: str
    risk_score: float
    created_at: datetime


class PredictionService:
    def __init__(self) -> None:
        self._predictions_by_id: dict[int, PredictionRecord] = {}
        self._next_id = 1

    def predict(
        self,
        user_id: int,
        age: int,
        bmi: float,
        hbA1c_level: float,
        blood_glucose_level: float,
        hypertension: bool,
        heart_disease: bool,
        smoking_history: str,
    ) -> PredictionRecord:
        # Very simple risk scoring for now until ML model integration.
        score = 0.0
        score += min(age / 120.0, 1.0) * 0.20
        score += min(bmi / 45.0, 1.0) * 0.20
        score += min(hbA1c_level / 10.0, 1.0) * 0.25
        score += min(blood_glucose_level / 250.0, 1.0) * 0.20
        if hypertension:
            score += 0.07
        if heart_disease:
            score += 0.05
        if smoking_history == "current":
            score += 0.03

        score = max(0.0, min(score, 1.0))
        label = "high_risk" if score >= 0.5 else "low_risk"

        record = PredictionRecord(
            id=self._next_id,
            user_id=user_id,
            risk_label=label,
            risk_score=round(score, 3),
            created_at=datetime.now(timezone.utc),
        )
        self._predictions_by_id[record.id] = record
        self._next_id += 1
        return record

    def list_predictions(self, user_id: int) -> list[PredictionRecord]:
        items = [p for p in self._predictions_by_id.values() if p.user_id == user_id]
        return sorted(items, key=lambda x: x.created_at, reverse=True)


prediction_service = PredictionService()
