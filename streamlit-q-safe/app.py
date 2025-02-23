import streamlit as st
import pandas as pd
from utils import (
    plot_correlation_heatmap,
    plot_time_series,
    display_filtered_table,  # Updated dropdown table function
    plot_line_graph
)

# Streamlit Page Config
st.set_page_config(
    page_title="🔒 Cybersecurity Threat Detection Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Header
st.title("🔍 Cybersecurity Threat Analysis Dashboard")
st.markdown("Analyze potential threats based on login behaviors, network activity, and access patterns.")
# Add a clickable button to redirect to an external link
st.markdown("""
    <div style='text-align: center; padding: 10px;'>
        <a href='https://q-safe.vercel.app/' target='_blank' 
           style='background-color: #4CAF50;
                  color: white;
                  padding: 12px 24px;
                  text-decoration: none;
                  font-size: 18px;
                  border-radius: 5px;
                  display: inline-block;
                  transition: background-color 0.3s ease;'>
            🚀 Q-Safe Demo Test Login App
        </a>
    </div>
""", unsafe_allow_html=True)

# Sidebar File Upload
data_source = st.sidebar.radio(
    "Choose Data Source:",
    options=["Use Preloaded Data", "Upload Your Own CSV"]
)

if data_source == "Upload Your Own CSV":
    uploaded_file = st.sidebar.file_uploader("📥 Upload your CSV file", type=["csv"])
else:
    uploaded_file = "data.csv"  # Assuming preloaded data.csv is stored in a 'data' folder


# Main App Logic
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert timestamps if the column exists
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Visualizations for All Data
    st.header("📊 Global Visual Insights (Entire Dataset)")

    # Correlation Heatmap
    plot_correlation_heatmap(df)

    st.markdown("---")

    # Time-Series Plot
    plot_time_series(df)

    st.markdown("---")

    # line graph Plot
    plot_line_graph(df)

    st.markdown("---")

    # Dropdown-Based Data Display
    display_filtered_table(df)

else:
    st.info("📌 Please upload a CSV file to begin.")
