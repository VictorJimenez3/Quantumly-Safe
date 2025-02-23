import pandas as pd
import numpy as np
import pickle
import pennylane as qml
from pennylane import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
file_path = "cybersecurity_intrusion_data_cleaned.csv"
df = pd.read_csv(file_path)

# Define features (Adding browser_type)
features = ["login_attempts", "failed_logins", "browser_type"]
target = "attack_detected"

X = df[features]
y = df[target]

# One-Hot Encode browser_type
X = pd.get_dummies(X, columns=["browser_type"], drop_first=True)

# Normalize Numeric Features
scaler = MinMaxScaler()
X.iloc[:, :2] = scaler.fit_transform(X.iloc[:, :2]).astype(float)  # Explicitly cast to float

# Quantum Kernel Transformation
n_qubits = X.iloc[:, :2].shape[1]  # Use only numeric columns for quantum embedding
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def quantum_kernel(x1, x2):
    qml.templates.AngleEmbedding(x1, wires=range(n_qubits))
    qml.templates.AngleEmbedding(x2, wires=range(n_qubits))
    return qml.probs(wires=range(n_qubits))

# Apply Quantum Transformation to Numeric Features
X_q = np.array([quantum_kernel(x, x) for x in X.iloc[:, :2].values])

# Combine Quantum Features with One-Hot Encoded Features
X_transformed = np.hstack((X_q, X.iloc[:, 2:].values))

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.15, random_state=42)

# Train Quantum Random Forest Model
clf = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
clf.fit(X_train, y_train)

# Predict and Evaluate
y_pred = clf.predict(X_test)
print("Quantum Random Forest Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save the trained Quantum RF model
with open("quantum_rf_model_rf_withbrowser.pkl", "wb") as model_file:
    pickle.dump(clf, model_file)

# Save the scaler (important for transforming new inputs later)
with open("scaler.pkl_rf_browser", "wb") as scaler_file:
    pickle.dump(scaler, scaler_file)

print("Quantum Random Forest Model and scaler saved successfully!")
