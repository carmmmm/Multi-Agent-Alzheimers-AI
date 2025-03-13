import pandas as pd

def load_patient_data(csv_file):
    """
    Loads patient history data from a CSV file.

    Parameters:
        csv_file (str): Path to the CSV file containing patient data.

    Returns:
        DataFrame: Processed patient history data.
    """
    try:
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        print(f"Error loading patient data: {e}")
        return None

def extract_relevant_features(df):
    """
    Extracts important features from patient history data.

    Parameters:
        df (DataFrame): Raw patient history DataFrame.

    Returns:
        DataFrame: Processed DataFrame with selected columns.
    """
    # Define the columns to keep (adjust based on actual dataset)
    selected_columns = ["PatientID", "Age", "FamilyHistory", "MMSE_Score", "CDR_Score", "EducationYears"]

    # Ensure columns exist in the dataset
    available_columns = [col for col in selected_columns if col in df.columns]

    if not available_columns:
        print("No matching columns found in dataset.")
        return None

    processed_df = df[available_columns].copy()

    return processed_df

# Example Usage
if __name__ == "__main__":
    # Load a sample dataset (Replace with actual file)
    sample_csv = "data/sample_patient_history.csv"
    patient_data = load_patient_data(sample_csv)

    if patient_data is not None:
        processed_data = extract_relevant_features(patient_data)
        print("Processed Patient Data:")
        print(processed_data.head())