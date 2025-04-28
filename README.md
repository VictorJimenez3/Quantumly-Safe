# Quantumly Safe: Quantum-Enhanced Cybersecurity Platform

## Short Description
Quantumly Safe is a cybersecurity platform that integrates quantum-enhanced machine learning to detect cyber threats faster and more accurately. Using Quantum Random Forest models and quantum feature encoding, the system improves attack detection rates, reduces bias toward false negatives, and helps security teams respond more effectively. Built for modern network security needs where speed and precision are critical.

## Features
- **Quantum-Enhanced Threat Detection**: Uses quantum feature spaces to identify login anomalies and suspicious network behaviors.
- **Real-Time Security Intelligence**: Classifies events as safe or potentially malicious with detailed reporting.
- **Hybrid Quantum-Classical Architecture**: Combines quantum encoding with classical machine learning for scalable deployment.
- **Anomaly Detection and Response**: Reduces false negatives and improves detection precision for login attacks and credential-based intrusions.

## Tech Stack
- **Quantum Computing**: Quantum feature encoding with Angle Embedding and Strongly Entangling Layers.
- **Python**: Backend and machine learning pipelines.
- **Flask**: Web server for API handling and deployment.
- **React**: Frontend dashboard for visualization.
- **Streamlit**: Rapid dashboard prototyping.
- **InfluxDB**: Future integration planned for time-series threat data.
- **Ploomber**: ML pipeline orchestration.

## Challenges and Solutions
- **Quantum Feature Optimization**: Tuned number of qubits and entanglement layers to balance model complexity and performance.
- **Class Imbalance**: Addressed cybersecurity dataset imbalance using SMOTE and class weighting to improve detection of rare attack cases.
- **Model Tuning on Quantum Features**: Carefully optimized Random Forest hyperparameters after quantum encoding to avoid overfitting.
- **Data Preprocessing Bugs**: Resolved Pandas dtype warnings by ensuring consistent numerical scaling across feature pipelines.

## Key Outcomes / Metrics
- **Improved Detection Accuracy**: Increased cyberattack detection rate from 78% to 84.6%, significantly reducing false negatives.
- **Successful Quantum-Enhanced Pipeline**: Fully integrated quantum feature transformations into production-ready Random Forest classifiers.
- **Security-First Architecture**: Built a foundation for scalable real-time security monitoring using hybrid quantum-classical models.

## How to Run It
To deploy Quantumly Safe locally for testing:

1. Clone the repository:

       git clone https://github.com/VictorJimenez3/Quantumly-Safe.git
       cd Quantumly-Safe

2. Install dependencies:

       pip install -r requirements.txt

3. Start the Flask server:

       python app.py

4. (Optional) Launch the frontend dashboard using React or Streamlit as configured.

*Note: Production-grade deployment would require additional integration with live network data feeds and API security hardening.*

## Links
- [GitHub Repository](https://github.com/VictorJimenez3/Quantumly-Safe)
- [Devpost Project Page](https://devpost.com/software/q-safe)
- [Live Site](https://quantum-ly-safe.tech/) (Currently down due to cost)

