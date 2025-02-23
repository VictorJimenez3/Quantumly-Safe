import matplotlib.pyplot as plt
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

# Keep only the selected features and target
#df = df[["login_attempts", "failed_logins", "unusual_time_access", "attack_detected"]]

plt.figure(figsize=(8, 6))
plt.scatter(df["login_attempts"], df["attack_detected"], alpha=0.5, c=df["attack_detected"], cmap="coolwarm", edgecolors="k")
plt.xlabel("login_attempts")
plt.ylabel("Attack Detected (0 = No, 1 = Yes)")
plt.title("Failed Logins vs Attack Detection")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
plt.scatter(df["failed_logins"], df["attack_detected"], alpha=0.5, c=df["attack_detected"], cmap="coolwarm", edgecolors="k")
plt.xlabel("Failed Logins")
plt.ylabel("Attack Detected (0 = No, 1 = Yes)")
plt.title("Failed Logins vs Attack Detection")
plt.grid(True)
plt.show()

df_grouped = df.groupby("login_attempts")["attack_detected"].mean()

plt.figure(figsize=(10, 5))
df_grouped.plot(kind="bar", color="red")
plt.xlabel("login_attempts")
plt.ylabel("Attack Probability")
plt.title("Average Attack Detection Rate by login_attempts")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.show()

df_grouped = df.groupby("failed_logins")["attack_detected"].mean()

plt.figure(figsize=(10, 5))
df_grouped.plot(kind="bar", color="red")
plt.xlabel("Failed Logins")
plt.ylabel("Attack Probability")
plt.title("Average Attack Detection Rate by Failed Logins")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.show()

df_grouped = df.groupby("browser_type")["attack_detected"].mean()

plt.figure(figsize=(10, 5))
df_grouped.plot(kind="bar", color="red")
plt.xlabel("browser_type")
plt.ylabel("Attack Probability")
plt.title("Average Attack Detection Rate by browser_type")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.show()

import matplotlib.pyplot as plt

# Group by network_packet_size and calculate the mean attack detection rate
df_grouped = df.groupby("network_packet_size")["attack_detected"].mean()

# Plot the bar chart
plt.figure(figsize=(12, 6))
df_grouped.plot(kind="bar", color="blue")

# Labels and title
plt.xlabel("Network Packet Size")
plt.ylabel("Attack Probability")
plt.title("Attack Detection Rate by Network Packet Size")
plt.xticks(rotation=45)
plt.grid(axis="y")

# Show the plot
plt.show()

import matplotlib.pyplot as plt

# Group by session_duration and calculate the mean attack detection rate
df_grouped = df.groupby("session_duration")["attack_detected"].mean()

# Plot the bar chart
plt.figure(figsize=(12, 6))
df_grouped.plot(kind="bar", color="green")

# Labels and title
plt.xlabel("Session Duration")
plt.ylabel("Attack Probability")
plt.title("Attack Detection Rate by Session Duration")
plt.xticks(rotation=45)
plt.grid(axis="y")

# Show the plot
plt.show()


import matplotlib.pyplot as plt
import numpy as np

# Group by ip_reputation_score and calculate mean attack detection rate
df_grouped = df.groupby("ip_reputation_score")["attack_detected"].mean()

# Scatter plot with transparency
plt.figure(figsize=(12, 6))
plt.scatter(df_grouped.index, df_grouped.values, s=2, alpha=0.3, color="green", edgecolors="black")
# Labels and title
plt.xlabel("IP Reputation Score")
plt.ylabel("Attack Probability")
plt.title("Attack Detection Rate by IP Reputation Score")
plt.xticks(rotation=45)
plt.grid(axis="y")

# Show the plot
plt.show()


import matplotlib.pyplot as plt
import numpy as np

# Group by ip_reputation_score and calculate mean attack detection rate
df_grouped = df.groupby("ip_reputation_score")["attack_detected"].mean()

# Generate some jitter
jitter = np.random.normal(0, 0.05, size=len(df_grouped))  # Add small noise

# Scatter plot with jitter and transparency
plt.figure(figsize=(12, 6))
plt.scatter(df_grouped.index + jitter, df_grouped.values, alpha=0.5, color="green", edgecolors="black")

# Labels and title
plt.xlabel("IP Reputation Score")
plt.ylabel("Attack Probability")
plt.title("Attack Detection Rate by IP Reputation Score (With Jitter)")
plt.xticks(rotation=45)
plt.grid(axis="y")

# Show the plot
plt.show()
