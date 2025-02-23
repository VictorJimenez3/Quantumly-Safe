import pickle
import numpy as np
import pennylane as qml
import pandas as pd

# Load the trained Quantum RF model
with open("quantum_rf_model_rf_withbrowser.pkl", "rb") as model_file:
    clf = pickle.load(model_file)

# Load the scaler
with open("scaler.pkl_rf_browser", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

print("Model and Scaler loaded successfully!")

# Example new data
new_data = {
    "login_attempts": 150,
    "failed_logins": 50,
    "browser_type": "Unknown"  # Supports "Unknown" browsers
}

# Convert to DataFrame
new_df = pd.DataFrame([new_data])

# One-Hot Encode browser_type (must match training set encoding)
expected_browser_dummies = [
    "browser_type_Edge", "browser_type_Firefox", "browser_type_Safari", 
    "browser_type_Chrome", "browser_type_Unknown"
]

# Add missing one-hot columns with default 0
for col in expected_browser_dummies:
    if col not in new_df.columns:
        new_df[col] = 0  # Default to 0

# Set correct browser column to 1
browser_col = f"browser_type_{new_df.loc[0, 'browser_type']}"
if browser_col in expected_browser_dummies:
    new_df[browser_col] = 1
else:
    new_df["browser_type_Unknown"] = 1  # If browser type is missing, set "Unknown" to 1

# Drop original browser_type column
new_df.drop(columns=["browser_type"], inplace=True)

# Scale numeric features (Fix: Cast to float)
new_df.iloc[:, :2] = scaler.transform(new_df.iloc[:, :2]).astype(np.float64)

# Quantum Kernel Transformation
n_qubits = new_df.iloc[:, :2].shape[1]
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def quantum_kernel(x1, x2):
    qml.templates.AngleEmbedding(x1, wires=range(n_qubits))
    qml.templates.AngleEmbedding(x2, wires=range(n_qubits))
    return qml.probs(wires=range(n_qubits))

# Apply Quantum Transformation to Numeric Features
X_q = np.array([quantum_kernel(x, x) for x in new_df.iloc[:, :2].values])

# Combine Quantum Features with One-Hot Encoded Features
X_transformed = np.hstack((X_q, new_df.iloc[:, 2:].values))

# **Ensure Correct Number of Features**
print("Expected number of features by model:", clf.n_features_in_)
print("Final input feature names:", new_df.columns)
print("X_transformed shape:", X_transformed.shape)

# **Fix: Drop the extra feature if needed**
if X_transformed.shape[1] > clf.n_features_in_:
    X_transformed = X_transformed[:, :clf.n_features_in_]

# Predict using the trained model
prediction = clf.predict(X_transformed)
print("Prediction:", "Attack Detected" if prediction[0] == 1 else "No Attack")
