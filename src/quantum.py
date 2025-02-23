import pickle
import numpy as np
import pandas as pd
import pennylane as qml

# Load the trained Quantum RF model
with open("src/quantum_rf_model_rf_withbrowser.pkl", "rb") as model_file:
    clf = pickle.load(model_file)

# Load the scaler
with open("src/scaler.pkl_rf_browser", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

# Define Expected Browser Types for One-Hot Encoding
expected_browser_dummies = [
    "browser_type_Edge", "browser_type_Firefox", "browser_type_Safari", 
    "browser_type_Chrome", "browser_type_Unknown"
]

# Quantum Device Setup
n_qubits = 2  # Update based on the actual number of numerical features
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def quantum_kernel(x1, x2):
    qml.templates.AngleEmbedding(x1, wires=range(n_qubits))
    qml.templates.AngleEmbedding(x2, wires=range(n_qubits))
    return qml.probs(wires=range(n_qubits))

def quantum_random_forest(data: dict):
    try:
        # Convert object to dictionary if needed
        if hasattr(data, "__dict__"):
            data = vars(data)

        if not isinstance(data, dict):
            return {"error": "Invalid data format. Expected dictionary."}

        # Extract nested "data" field if present
        if "data" in data and isinstance(data["data"], dict):
            data = data["data"]

        # Debug: Print incoming data
        print("Processed data before cleaning:", data)

        # Rename fields only if they exist
        data["login_attempts"] = data.pop("totalAttempts", None)
        data["failed_logins"] = data.pop("failedAttempts", None)
        data["browser_type"] = data.pop("userAgent", "Unknown")  # Default to 'Unknown'

        # Drop unexpected fields
        allowed_fields = {"login_attempts", "failed_logins", "browser_type"}
        data = {key: value for key, value in data.items() if key in allowed_fields}

        # Ensure required fields exist
        if data.get("login_attempts") is None or data.get("failed_logins") is None:
            return {"error": "Missing required fields"}

        # Convert to DataFrame
        new_df = pd.DataFrame([data])

        # One-Hot Encoding for browser_type
        for col in expected_browser_dummies:
            new_df[col] = 0  # Default to 0
        browser_col = f"browser_type_{new_df.loc[0, 'browser_type']}"
        if browser_col in expected_browser_dummies:
            new_df[browser_col] = 1
        else:
            new_df["browser_type_Unknown"] = 1  # If browser type is missing, set "Unknown" to 1
        new_df.drop(columns=["browser_type"], inplace=True)

        # Scale numeric features
        new_df.iloc[:, :2] = scaler.transform(new_df.iloc[:, :2]).astype(np.float64)

        # Apply Quantum Kernel Transformation
        X_q = np.array([quantum_kernel(x, x) for x in new_df.iloc[:, :2].values])

        # Combine Quantum Features with One-Hot Encoded Features
        X_transformed = np.hstack((X_q, new_df.iloc[:, 2:].values))

        # Ensure Correct Number of Features
        if X_transformed.shape[1] > clf.n_features_in_:
            X_transformed = X_transformed[:, :clf.n_features_in_]

        # Make Prediction
        prediction = clf.predict(X_transformed)
        result = "Attack Detected" if prediction[0] == 1 else "No Attack"

        return {"prediction": result}

    except Exception as e:
        return {"error": str(e)}
