import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

# Correlation Heatmap
def plot_correlation_heatmap(df):
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=["number"])

    # Check if there are enough numeric columns for correlation
    if numeric_df.shape[1] < 2:
        st.warning("⚠️ Not enough numeric columns for correlation heatmap.")
        return

    # Handle NaNs by filling them with 0
    corr = numeric_df.fillna(0).corr()

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    st.subheader("📊 Correlation Heatmap")
    st.pyplot(fig)

# Combined Scatter Matrix
def plot_scatter_matrix(df, columns):
    numeric_df = df[columns].select_dtypes(include=["number"])
    
    if numeric_df.empty:
        st.warning("⚠️ Scatter matrix can't be plotted since numeric data is missing.")
        return

    fig = px.scatter_matrix(
        numeric_df,
        dimensions=columns,
        color="ip_reputation_score" if "ip_reputation_score" in df.columns else None,
        title="🌐 Scatter Matrix",
        height=700
    )
    fig.update_traces(diagonal_visible=False)
    st.subheader("🧩 Scatter Matrix")
    st.plotly_chart(fig, use_container_width=True)

# Line Chart for Time-based Anomalies
def plot_time_series(df, time_column, metric_column):
    fig = px.line(
        df,
        x=time_column,
        y=metric_column,
        color="encryption_used" if "encryption_used" in df.columns else None,
        title=f"📈 {metric_column} Over Time",
        markers=True
    )
    st.subheader(f"📅 Time Series: {metric_column}")
    st.plotly_chart(fig, use_container_width=True)

# Radar Chart for Comparative Analysis
def plot_radar_chart(df, category_col, metric_cols):
    numeric_df = df[metric_cols].select_dtypes(include=["number"])

    if numeric_df.empty:
        st.warning("⚠️ Radar chart requires numeric values for comparison.")
        return

    data = []
    categories = df[category_col].unique()
    for category in categories:
        subset = df[df[category_col] == category]
        avg_values = subset[metric_cols].mean()
        data.append(go.Scatterpolar(
            r=avg_values,
            theta=metric_cols,
            fill='toself',
            name=f"{category}"
        ))

    fig = go.Figure(data=data)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, df[metric_cols].max().max()])
        ),
        showlegend=True,
        title="📡 Comparative Radar Chart"
    )
    st.subheader("🛡️ Radar Chart - Feature Comparison")
    st.plotly_chart(fig, use_container_width=True)

# Box Plot for Distribution Insights
def plot_box_plot(df, x_col, y_col):
    if y_col not in df.select_dtypes(include=["number"]).columns:
        st.warning("⚠️ Box plot requires numeric values for y-axis.")
        return

    fig = px.box(df, x=x_col, y=y_col, color=x_col, title=f"📦 Distribution of {y_col} by {x_col}")
    st.subheader(f"📦 Box Plot: {y_col} by {x_col}")
    st.plotly_chart(fig, use_container_width=True)
