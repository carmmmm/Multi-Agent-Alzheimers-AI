import streamlit as st
from fpdf import FPDF
import os

def generate_patient_report(patient_name, age, test_results):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Alzheimer's Cognitive Test Report", ln=True, align="C")
    pdf.ln(10)

    # Patient Info
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Patient Name: {patient_name}", ln=True)
    pdf.cell(200, 10, f"Age: {age}", ln=True)
    pdf.ln(10)

    # Test Results
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Cognitive Test Results", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    for key, value in test_results.items():
        pdf.cell(200, 10, f"{key}: {value}", ln=True)

    # Save PDF
    report_path = f"data/{patient_name}_report.pdf"
    pdf.output(report_path)
    return report_path

def display_report_generation():
    st.title("📄 Generate Patient Report")

    patient_name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=50, max_value=100, value=72)

    test_results = {
        "Memory Recall Score": 3,
        "Math Score": "Correct",
        "Clock Drawing Score": "Passed"
    }

    if st.button("Generate Report"):
        report_path = generate_patient_report(patient_name, age, test_results)
        st.success(f"Report Generated: {report_path}")
        with open(report_path, "rb") as file:
            st.download_button("Download Report", file, file_name=f"{patient_name}_Report.pdf")
