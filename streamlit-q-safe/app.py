import streamlit as st
import pandas as pd
from utils import (
    plot_correlation_heatmap,
    plot_scatter_matrix,
    plot_time_series,
    plot_radar_chart,
    plot_box_plot
)

# App Configuration
st.set_page_config(
    page_title="🔍 Cybersecurity Threat Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Title
st.title("🔒 Cybersecurity Threat Detection Dashboard")
st.markdown("Analyze potential threats based on login behaviors, network activity, and access patterns.")

# File Upload
uploaded_file = st.sidebar.file_uploader("📥 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Sidebar Filters
    st.sidebar.header("⚙️ Filters")

    # Ensure 'ip_reputation_score' exists and has valid numeric values
    if "ip_reputation_score" in df.columns:
        # Drop NaNs
        df["ip_reputation_score"] = pd.to_numeric(df["ip_reputation_score"], errors="coerce").fillna(0)

        # Check for unique values
        if df["ip_reputation_score"].nunique() > 1:
            min_score = int(df["ip_reputation_score"].min())
            max_score = int(df["ip_reputation_score"].max())

            # Ensure min_score is less than max_score
            if min_score < max_score:
                score_threshold = st.sidebar.slider(
                    "IP Reputation Score Threshold",
                    min_value=min_score,
                    max_value=max_score,
                    value=int(df["ip_reputation_score"].mean())
                )
                filtered_df = df[df["ip_reputation_score"] >= score_threshold]
            else:
                st.sidebar.warning("⚠️ All values in IP Reputation Score are the same.")
                filtered_df = df
        else:
            st.sidebar.warning("⚠️ IP Reputation Score has only one unique value.")
            filtered_df = df  # No filtering applied
    else:
        st.sidebar.error("❌ IP Reputation Score column is missing in the dataset.")
        filtered_df = df

    # Check for empty filtered data
    if filtered_df.empty:
        st.error("❌ No data available after applying filters. Please adjust the filter settings.")
    else:
        # Main Visualizations
        st.header("📊 Visual Analysis")

        

        
        plot_correlation_heatmap(filtered_df)

        
        plot_radar_chart(
                filtered_df,
                category_col="browser_type",
                metric_cols=[
                    "attack_detected",
                    "failed_logins",
                    "session_duration",
                    "login_attempts",
                    "network_packet_size"
                ]
            )

        st.markdown("---")

        plot_scatter_matrix(
            filtered_df,
            columns=[
                "attack_detected",
                "ip_reputation_score",          
                "login_attempts"
            ]
        )

        st.markdown("---")

        # Time-series Visualization
        if "unusual_time_access" in df.columns:
            plot_time_series(filtered_df, "unusual_time_access", "attack_detected")

        # Box Plot
        plot_box_plot(
            filtered_df,
            x_col="protocol_type",
            y_col="network_packet_size"
        )

        # Data Preview
        st.subheader("📝 Filtered Data Preview")
        st.dataframe(filtered_df)

        # Download Filtered Data
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Filtered Data",
            data=csv,
            file_name="filtered_cybersecurity_data.csv",
            mime="text/csv"
        )

else:
    st.info("📌 Upload a CSV file from the sidebar to begin.")
