import streamlit as st
import streamlit_authenticator as stauth
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
from yaml.loader import SafeLoader
import os

# --- Set Up FastAPI URL ---
API_URL = "http://127.0.0.1:8000/process_patient/"

# --- Load Authentication Config ---
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# Render sidebar before authentication check
st.sidebar.title("🔍 Navigation")


# Handle login properly
login_info = authenticator.login(location="sidebar")
#name, authentication_status, username = authenticator.login(location="sidebar")

# Ensure `login_info` is not None before unpacking
if login_info is not None:
    name, authentication_status, username = login_info
else:
    name, authentication_status, username = None, None, None

# Ensure authentication_status is checked before using it
if authentication_status is False:
    st.sidebar.error("Incorrect username or password. Please try again.")
elif authentication_status is None:
    st.sidebar.warning("Please log in to access the application.")
    st.stop()  # ✅ This stops execution but allows login to render

# Debugging: Print authentication status
st.write(f"DEBUG - authentication_status: {authentication_status}")
st.sidebar.write(f"DEBUG - authentication_status: {authentication_status}")  # Now appears in sidebar

# ✅ Ensure authentication_status is checked before using it
if authentication_status is False:
    st.error("Incorrect username or password. Please try again.")
elif authentication_status is None:
    st.warning("Please log in to access the application.")
    st.stop()

# --- Sidebar for User Authentication ---
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Patient Dashboard", "Take Cognitive Test", "Generate Report", "About"])

# --- If User is Logged In ---
if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Welcome, **{name}** 👋")

    # --- Sidebar Navigation ---
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Patient Dashboard", "Take Cognitive Test", "About"])

    # --- Define Data Storage File ---
    DATA_FILE = "data/patient_results.csv"

    # --- Load Patient History ---
    def load_patient_history():
        if os.path.exists(DATA_FILE):
            return pd.read_csv(DATA_FILE)
        return pd.DataFrame(columns=["Username", "Patient ID", "Age", "MMSE Score", "CDR Score", "Prediction"])

    # --- Save Patient Results ---
    def save_patient_result(username, patient_data, prediction):
        df = load_patient_history()
        new_entry = pd.DataFrame([{
            "Username": username,
            "Patient ID": patient_data["patient_id"],
            "Age": patient_data["age"],
            "MMSE Score": patient_data["mmse_score"],
            "CDR Score": patient_data["cdr_score"],
            "Prediction": prediction
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

    # --- Home Page (Main Input Form) ---
    if page == "Home":
        st.title("🧠 Alzheimer’s Disease Prediction System")
        st.markdown("### Predict Alzheimer's progression using AI-powered cognitive analysis.")

        # --- Collect User Input ---
        patient_id = st.text_input("Patient ID", "1001")
        age = st.number_input("Age", min_value=50, max_value=100, value=72)
        family_history = st.radio("Family History of Alzheimer's?", ["Yes", "No"])
        mmse_score = st.slider("MMSE Score (0-30)", min_value=0, max_value=30, value=26)
        cdr_score = st.select_slider("CDR Score (0-3)", options=[0, 0.5, 1, 2, 3], value=0.5)
        education_years = st.number_input("Years of Education", min_value=0, max_value=20, value=12)
        verbal_fluency_text = st.text_area("Verbal Fluency Test Input", "apple banana orange apple grapes lemon banana orange apple")

        # --- Submit Button ---
        if st.button("🔎 Analyze Patient Data"):
            patient_data = {
                "patient_id": int(patient_id),
                "age": int(age),
                "family_history": family_history,
                "mmse_score": float(mmse_score),
                "cdr_score": float(cdr_score),
                "education_years": int(education_years),
                "verbal_fluency_text": verbal_fluency_text
            }

            # --- Send Request to FastAPI ---
            with st.spinner("Processing..."):
                response = requests.post(API_URL, json=patient_data)

            # --- Process Response ---
            if response.status_code == 200:
                result = response.json()

                # --- Display Results ---
                st.subheader("📋 Processed Patient Data")
                st.json(result["structured_patient_data"])
                st.subheader("🗣 Verbal Fluency Analysis")
                st.json(result["verbal_fluency_analysis"])
                prediction = result["progression_prediction"]
                st.subheader("🔮 Disease Progression Prediction")
                st.markdown(f"### **{prediction}**")

                # --- Save to History ---
                save_patient_result(username, patient_data, prediction)
            else:
                st.error("❌ Error processing patient data. Please check API connection.")

    # --- Patient Dashboard ---
    elif page == "Patient Dashboard":
        st.title("📊 Your Patient History & Progress")
        df = load_patient_history()
        user_df = df[df["Username"] == username]

        if not user_df.empty:
            st.dataframe(user_df)

            # --- Chart: MMSE Score Over Time ---
            st.subheader("📈 MMSE Score Over Time")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.lineplot(data=user_df, x="Age", y="MMSE Score", marker="o", ax=ax)
            st.pyplot(fig)

            # --- Chart: Prediction Breakdown ---
            st.subheader("🧠 Prediction Breakdown")
            fig, ax = plt.subplots()
            sns.countplot(data=user_df, x="Prediction", palette="coolwarm", ax=ax)
            st.pyplot(fig)
        else:
            st.info("No patient data found for this user.")

    # --- Cognitive Self-Test ---
    elif page == "Take Cognitive Test":
        from ui.cognitive_test import run_cognitive_test
        test_results = run_cognitive_test()

    # --- Generate Patient Report ---
    elif page == "Generate Report":
        from ui.patient_report import display_report_generation
        display_report_generation()

    # --- About Page ---
    elif page == "About":
        st.title("ℹ️ About This Project")
        st.markdown("""
        - **Purpose:** AI-powered tool for Alzheimer's progression analysis.
        - **Developed By:** Carmen Montero
        - **Data Sources:** ADNI, NACC
        - **Technology Stack:** Python, FastAPI, Streamlit, ML
        """)

else:
    st.warning("Please log in to access this application.")