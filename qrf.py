import pennylane as qml
from pennylane import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import pennylane as qml
from pennylane import numpy as np
import jax
from jax import numpy as jnp
import optax
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import resample
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
file_path = "cybersecurity_intrusion_data.csv"
df = pd.read_csv(file_path)

# Load the dataset (assuming df already has the required features)
features = ["login_attempts", "failed_logins"]
target = "attack_detected"

X = df[features].values
y = df[target].values

# Normalize Features
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define a Quantum Kernel
n_qubits = X_train.shape[1]
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def quantum_kernel(x1, x2):
    qml.templates.AngleEmbedding(x1, wires=range(n_qubits))
    qml.templates.AngleEmbedding(x2, wires=range(n_qubits))
    return qml.probs(wires=range(n_qubits))

# Transform Features with Quantum Kernel
X_train_q = np.array([quantum_kernel(x, x) for x in X_train])
X_test_q = np.array([quantum_kernel(x, x) for x in X_test])

# Train Quantum Random Forest
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train_q, y_train)

# Predict and Evaluate
y_pred = clf.predict(X_test_q)
print("Quantum Random Forest Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

import pickle

# Save the trained model
with open("quantum_rf_model.pkl", "wb") as model_file:
    pickle.dump(clf, model_file)

# Save the scaler (important for transforming new inputs later)
with open("scaler.pkl", "wb") as scaler_file:
    pickle.dump(scaler, scaler_file)

print("Model and scaler saved successfully!")
