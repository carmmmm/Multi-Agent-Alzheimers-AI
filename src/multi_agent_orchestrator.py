from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from src.cognitive_test_agent import analyze_verbal_fluency
from src.patient_history_agent import extract_relevant_features
from src.progression_prediction_agent import predict_progression

app = FastAPI()

# Define request model
class PatientDataInput(BaseModel):
    patient_id: int
    age: int
    family_history: str
    mmse_score: float
    cdr_score: float
    education_years: int
    verbal_fluency_text: str

@app.post("/process_patient/")
def process_patient(data: PatientDataInput):
    """
    Endpoint that processes a patient's structured history, cognitive test, and progression prediction.
    """
    # Convert patient history data into a dictionary
    patient_dict = {
        "Age": data.age,
        "FamilyHistory": 1 if data.family_history == "Yes" else 0,
        "MMSE_Score": data.mmse_score,
        "CDR_Score": data.cdr_score,
        "EducationYears": data.education_years
    }

    # Extract structured patient data
    structured_data = extract_relevant_features(pd.DataFrame([patient_dict]))

    # Run cognitive test analysis
    verbal_analysis = analyze_verbal_fluency(data.verbal_fluency_text)

    # Run progression prediction
    prediction = predict_progression(patient_dict)

    # Combine results
    result = {
        "structured_patient_data": structured_data.to_dict(orient="records"),
        "verbal_fluency_analysis": verbal_analysis,
        "progression_prediction": "Likely to progress" if prediction == 1 else "Unlikely to progress"
    }

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)