from sqlalchemy import select, text
from sqlalchemy.orm import Session

# Adding ML model
from pathlib import Path
import joblib
import pandas as pd

from app.db.models import Prediction
from app.db.sql_queries import get_sql_query

PredictionRecord = Prediction


class PredictionService:
    def __init__(self) -> None:
        # Load model artifacts once at startup to avoid reloading on each request.
        # Find the CarePortal project folder
        project_root = Path(__file__).resolve().parents[3]

        # Go into the ml-model folder
        ml_model_directory = project_root / "ml-model"

        # Paths to the saved files
        model_path = ml_model_directory / "random_forest_model.pkl"
        scaler_path = ml_model_directory / "standard_scaler.pkl"
        feature_names_path = ml_model_directory / "feature_names.pkl"

        # Load them once when FastAPI starts
        self._model = joblib.load(model_path)
        self._scaler = joblib.load(scaler_path)
        self._feature_names = joblib.load(feature_names_path)

    def predict(
        self,
        db: Session,
        user_id: int,
        age: int,
        gender: str,
        bmi: float,
        hypertension: bool,
        heart_disease: bool,
        smoking_history: str,
        HbA1c_level: float,
        blood_glucose_level: float,
    ) -> PredictionRecord:
        # Build a patient record using the values submitted from the frontend
        patient_data = {
            "age": age,
            "hypertension": int(hypertension),
            "heart_disease": int(heart_disease),
            "bmi": bmi,
            "HbA1c_level": HbA1c_level,
            "blood_glucose_level": blood_glucose_level,
            "gender": gender,
            "smoking_history": smoking_history,
        }
        # Convert the patient record into a row dataframe
        # to match the format used during model training
        patient_df = pd.DataFrame([patient_data])

        # One-hot encode the categorical features
        # to match the preprocessing performed during training
        patient_df = pd.get_dummies(patient_df, columns=["gender", "smoking_history"],)

        # Reorder the columns to match the exact feature order
        # used when the Random Forest model was trained.
        # Any missing dummy columns are added with a value of 0.
        patient_df = patient_df.reindex(columns=self._feature_names, fill_value=0,)

        # Numerical features that were standardized during training
        numerical_columns = [
            "age",
            "bmi",
            "HbA1c_level",
            "blood_glucose_level",
        ]

        # Apply the saved StandardScaler so the input data
        # is transformed the same way as the training data
        patient_df[numerical_columns] = self._scaler.transform(patient_df[numerical_columns])

        # Use the trained Random Forest model to predict
        # whether the patient is at risk for diabetes
        prediction = int(self._model.predict(patient_df)[0])

        # Get the probability that the patient belongs
        # to the diabetes (positive) class, 0 = low risk, 1 = high risk
        # then convert the numerical prediction into a risk label
        score = float(self._model.predict_proba(patient_df)[0][1])
        label = "high_risk" if prediction == 1 else "low_risk"

        record = Prediction(
            user_id=user_id,
            risk_label=label,
            risk_score=round(score, 3),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def list_predictions(self, db: Session, user_id: int) -> list[PredictionRecord]:
        statement = select(Prediction).from_statement(text(get_sql_query("list_predictions_for_user")))
        return list(db.scalars(statement, params={"user_id": user_id}).all())


prediction_service = PredictionService()
