import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load sample patient dataset
def load_dataset(csv_file):
    """
    Loads the patient dataset and selects relevant features for prediction.

    Parameters:
        csv_file (str): Path to the CSV file.

    Returns:
        X (DataFrame): Features.
        y (Series): Target labels.
    """
    df = pd.read_csv(csv_file)

    # Selecting features and target variable
    selected_features = ["Age", "FamilyHistory", "MMSE_Score", "CDR_Score", "EducationYears"]
    target_variable = "Progression"  # 0 = No progression, 1 = Progression to Alzheimer's

    # Convert categorical "FamilyHistory" column to numerical (Yes → 1, No → 0)
    df["FamilyHistory"] = df["FamilyHistory"].map({"Yes": 1, "No": 0})

    # Drop rows with missing values
    df.dropna(subset=selected_features + [target_variable], inplace=True)

    # Define features (X) and target (y)
    X = df[selected_features]
    y = df[target_variable]

    return X, y

# Train ML Model
def train_model(csv_file):
    """
    Trains a Random Forest model to predict Alzheimer's progression.

    Parameters:
        csv_file (str): Path to the CSV file.

    Returns:
        model (RandomForestClassifier): Trained model.
    """
    X, y = load_dataset(csv_file)

    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Save trained model
    with open("models/progression_model.pkl", "wb") as model_file:
        pickle.dump(model, model_file)

    return model

# Load trained model for prediction
def predict_progression(patient_data):
    """
    Predicts Alzheimer's progression risk for a given patient.

    Parameters:
        patient_data (dict): Patient history data.

    Returns:
        int: 0 (No progression) or 1 (Progression to Alzheimer's)
    """
    # Load the trained model
    with open("models/progression_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)

    # Convert input data into a DataFrame
    X_new = pd.DataFrame([patient_data])

    # Make prediction
    prediction = model.predict(X_new)[0]

    return int(prediction)

# Example training execution
if __name__ == "__main__":
    train_model("data/sample_patient_history.csv")