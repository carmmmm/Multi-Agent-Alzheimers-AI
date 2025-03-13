import streamlit as st
import requests

# FastAPI URL (Make sure FastAPI is running!)
API_URL = "http://127.0.0.1:8000/process_patient/"

# Streamlit UI
st.title("🧠 Alzheimer’s Disease Prediction System")

# Collect user input
patient_id = st.text_input("Patient ID", "1001")
age = st.number_input("Age", min_value=50, max_value=100, value=72)
family_history = st.radio("Family History of Alzheimer's?", ["Yes", "No"])
mmse_score = st.slider("MMSE Score (0-30)", min_value=0, max_value=30, value=26)
cdr_score = st.select_slider("CDR Score (0-3)", options=[0, 0.5, 1, 2, 3], value=0.5)
education_years = st.number_input("Years of Education", min_value=0, max_value=20, value=12)

verbal_fluency_text = st.text_area("Verbal Fluency Test Input", "apple banana orange apple grapes lemon banana orange apple")

# Submit button
if st.button("Analyze Patient Data"):
    # Prepare data for API request
    patient_data = {
        "patient_id": int(patient_id),
        "age": int(age),
        "family_history": family_history,
        "mmse_score": float(mmse_score),
        "cdr_score": float(cdr_score),
        "education_years": int(education_years),
        "verbal_fluency_text": verbal_fluency_text
    }

    # Send request to FastAPI
    with st.spinner("Analyzing..."):
        response = requests.post(API_URL, json=patient_data)

    # Process response
    if response.status_code == 200:
        result = response.json()

        # Display structured patient data
        st.subheader("📋 Processed Patient Data")
        st.json(result["structured_patient_data"])

        # Display verbal fluency analysis
        st.subheader("🗣 Verbal Fluency Analysis")
        st.json(result["verbal_fluency_analysis"])

        # Display disease progression prediction
        st.subheader("🔮 Disease Progression Prediction")
        st.write(f"**Prediction:** {result['progression_prediction']}")

    else:
        st.error("❌ Error processing patient data. Please check the API connection.")