import streamlit as st
import pandas as pd
from utils import (
    plot_correlation_heatmap,
    plot_scatter,
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
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <a href='https://q-safe.vercel.app/' target='_blank' 
           style='background-color: #FF4B4B; 
                  color: white; 
                  padding: 15px 30px; 
                  text-decoration: none; 
                  border-radius: 10px; 
                  font-size: 24px; 
                  font-weight: bold; 
                  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                  display: inline-block;
                  transition: all 0.3s ease;'>
            🚀 Test it out!!!
        </a>
    </div>
""", unsafe_allow_html=True)
# File Upload
uploaded_file = st.sidebar.file_uploader("📥 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Sidebar Filters
    st.sidebar.header("⚙️ Filters")

    # Ensure 'attack_detected' exists
    if "attack_detected" in df.columns:
        # Drop NaNs from 'attack_detected' if any
        df["attack_detected"] = pd.to_numeric(df["attack_detected"], errors="coerce").fillna(0).astype(int)

        # Filter by attack detection status
        attack_filter = st.sidebar.radio(
            "🔍 Filter by Attack Detection:",
            options=[0, 1],
            format_func=lambda x: "No Attack Detected" if x == 0 else "Attack Detected"
        )

        filtered_df = df

    else:
        st.sidebar.error("❌ 'attack_detected' column is missing in the dataset.")
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
                    "failed_logins",
                    "session_duration",
                    "login_attempts",
                    "network_packet_size"
                ]
            )

        st.markdown("---")

        plot_scatter(
            filtered_df,                                        
            "login_attempts", 
            "ip_reputation_score"               
            
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
