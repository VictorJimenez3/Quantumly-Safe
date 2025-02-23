from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
import pennylane as qml

# Initialize Flask App
app = Flask(__name__)

# Load the trained Quantum RF model
with open("quantum_rf_model_rf_withbrowser.pkl", "rb") as model_file:
    clf = pickle.load(model_file)

# Load the scaler
with open("scaler.pkl_rf_browser", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

# Define Expected Browser Types for One-Hot Encoding
expected_browser_dummies = [
    "browser_type_Edge", "browser_type_Firefox", "browser_type_Safari", 
    "browser_type_Chrome", "browser_type_Unknown"
]

# Quantum Device Setup
n_qubits = 2  # Update this based on the actual number of numerical features
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def quantum_kernel(x1, x2):
    qml.templates.AngleEmbedding(x1, wires=range(n_qubits))
    qml.templates.AngleEmbedding(x2, wires=range(n_qubits))
    return qml.probs(wires=range(n_qubits))

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.json

        # Ensure required fields exist
        if "login_attempts" not in data or "failed_logins" not in data or "browser_type" not in data:
            return jsonify({"error": "Missing required fields"}), 400

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

        # Return Response
        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
