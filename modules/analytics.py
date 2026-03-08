import streamlit as st
import plotly.express as px

def run_dashboard(df):

    st.subheader("📊 KPI Dashboard")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns available")
        return

    measure_col = df[numeric_cols].std().idxmax()

    avg_val = df[measure_col].mean()
    max_val = df[measure_col].max()

    c1, c2, c3 = st.columns(3)

    c1.metric("Rows", len(df))
    c2.metric("Average", f"{avg_val:.2f}")
    c3.metric("Max", f"{max_val:.2f}")

    fig = px.histogram(df, x=measure_col)
    st.plotly_chart(fig, use_container_width=True)