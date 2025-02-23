import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Filter Data by Domain and IP Address
def filter_data(df, domain, selected_ips):
    filtered = df[df["domainName"] == domain]
    if selected_ips:
        filtered = filtered[filtered["ip"].isin(selected_ips)]
    return filtered


# Interactive Correlation Heatmap
def plot_correlation_heatmap(df):
    selected_columns = ["attack_detected", "domainName", "failedAttempts", "totalAttempts"]
    filtered_df = df[selected_columns].copy()
    
    # Convert categorical data to numerical if needed
    if "domainName" in filtered_df.columns:
        filtered_df["domainName"] = pd.factorize(filtered_df["domainName"])[0]
    if "attack_detected" in filtered_df.columns:
        filtered_df["attack_detected"] = filtered_df["attack_detected"].astype(int)

    corr = filtered_df.corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="📊 Correlation Heatmap"
    )
    fig.update_layout(autosize=True, dragmode="zoom")
    st.plotly_chart(fig, use_container_width=True)


# Line Graph Plot by IP Address
def plot_time_series(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    time_series_data = df.groupby(
        ["ip", pd.Grouper(key="timestamp", freq="D")]
    ).size().reset_index(name="access_attempts")

    fig = px.line(
        time_series_data,
        x="timestamp",
        y="access_attempts",
        color="ip",
        markers=True,
        title="📅 Access Attempts Over Time by IP Address"
    )
    fig.update_layout(
        xaxis=dict(rangeselector=dict(
            buttons=list([
                dict(count=7, label="1W", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(step="all")
            ])
        ), rangeslider=dict(visible=True), type="date")
    )
    st.plotly_chart(fig, use_container_width=True)




 # Display Data Using Dropdowns Instead of a Table (Grouped by Domain)
def display_filtered_table(df):
    st.subheader("📝 Records Grouped by Domain (Dropdown View)")

    # Check if 'domainName' column exists
    if "domainName" not in df.columns:
        st.error("❌ 'domainName' column is missing in the dataset.")
        return

    # Group the data by 'domainName'
    domain_groups = df.groupby("domainName")

    # Create a dropdown (expander) for each domain
    for domain, group_data in domain_groups:
        with st.expander(f"🌍 Domain: {domain} ({len(group_data)} records)"):
            for idx, row in group_data.iterrows():
                st.markdown(
                    f"""
                    **🔐 Record ID:** `{idx}`  
                    - 📡 **IP Address:** `{row['ip']}`  
                    - 🔢 **Total Attempts:** `{row['totalAttempts']}`  
                    - ❌ **Failed Attempts:** `{row['failedAttempts']}`  
                    - 👤 **Username:** `{row['username']}`  
                    - 🕵️‍♂️ **User Agent:** `{row['userAgent']}`  
                    - 🕒 **Timestamp:** `{row['timestamp']}`  
                    - 🚩 **Attack Detected:** `{row['attack_detected']}`  
                    ---
                    """
                )

    # Download the entire dataset
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Full Dataset",
        data=csv,
        file_name="full_cybersecurity_data.csv",
        mime="text/csv"
    )



# Line Graph Aggregating Total Attempts by Browser Type Over Time
def plot_line_graph(df):
    # Check if required columns exist
    required_columns = ["timestamp", "totalAttempts", "userAgent"]
    if not all(col in df.columns for col in required_columns):
        st.error("❌ Required columns ('timestamp', 'totalAttempts', 'userAgent') are missing in the dataset.")
        return

    # Ensure timestamps are in datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Aggregate total attempts by userAgent and timestamp (daily frequency)
    time_series_data = df.groupby(
        ["userAgent", pd.Grouper(key="timestamp", freq="D")]
    )["totalAttempts"].sum().reset_index()

    # Aggregate total attempts per browser
    browser_totals = df.groupby("userAgent")["totalAttempts"].sum().reset_index().sort_values(by="totalAttempts", ascending=False)

    # Plot the line graph with separate lines for each browser type
    fig = px.line(
        time_series_data,
        x="timestamp",  # X-axis: Time
        y="totalAttempts",  # Y-axis: Total attempts
        color="userAgent",  # Different line for each browser type
        markers=True,
        title="📈 Total Login Attempts Over Time by Browser Type"
    )

    # Add total login attempts as annotations for each browser
    for i, row in browser_totals.iterrows():
        fig.add_annotation(
            text=f"Total: {row['totalAttempts']}",
            xref="paper", yref="paper",
            x=1.1, y=1 - (i * 0.05),
            showarrow=False,
            font=dict(size=12),
            bgcolor="white",
            bordercolor="black"
        )

    # Improve layout and interactivity
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis_title="Total Attempts",
        legend_title="Browser Type",
        margin=dict(l=40, r=200, t=60, b=40)  # Adjust layout for annotations
    )

    st.subheader("📈 Total Login Attempts Over Time by Browser Type")
    st.plotly_chart(fig, use_container_width=True)
