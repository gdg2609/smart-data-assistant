import streamlit as st

from modules.analytics import run_dashboard
from modules.data_loader import load_file
from modules.data_cleaner import clean_data
from modules.anomaly_detection import detect_anomalies
from modules.ai_chart import ai_chart_builder
from modules.ai_insights import ai_storyteller
from modules.ai_sql import ai_sql_engine
from modules.filters import apply_filters
from modules.ai_report import generate_executive_report
from modules.stakeholder_report import generate_stakeholder_report
from modules.ai_query_engine import ai_query_engine
from modules.insight_engine import generate_insights

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Smart Data Assistant",
    layout="wide"
)


# ======================================================
# NAVIGATION STATE
# ======================================================
if "page" not in st.session_state:
    st.session_state.page = "overview"


# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:

    st.title("🚀 Smart Data Assistant")

    st.markdown("### Navigation")

    if st.button("📊 Overview", use_container_width=True):
        st.session_state.page = "overview"

    if st.button("📈 Analysis", use_container_width=True):
        st.session_state.page = "analysis"

    if st.button("🤖 AI Tools", use_container_width=True):
        st.session_state.page = "ai"

    if st.button("⚠ Risk Detection", use_container_width=True):
        st.session_state.page = "risk"

    if st.button("📑 Reports", use_container_width=True):
        st.session_state.page = "reports"

    st.divider()

    st.subheader("Global Filters")


# ======================================================
# MAIN TITLE
# ======================================================
st.title("🚀 Smart Data Assistant")


# ======================================================
# DATASET UPLOAD
# ======================================================
st.header("📊 Dataset Overview")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)


# ======================================================
# IF FILE UPLOADED
# ======================================================
if uploaded_file is not None:

    try:

        df = load_file(uploaded_file)

        df = clean_data(df)

        df = apply_filters(df)

        st.subheader("Preview of Data")
        st.dataframe(df.head())

        st.success("Data loaded successfully")

        st.divider()

        # ============================
        # OVERVIEW
        # ============================
        if st.session_state.page == "overview":

            st.header("📈 KPI Dashboard")

            run_dashboard(df)

        # ============================
        # ANALYSIS
        # ============================
        elif st.session_state.page == "analysis":

            st.header("📊 Visual Analysis")

            ai_chart_builder(df)

        # ============================
        # AI TOOLS
        # ============================
        elif st.session_state.page == "ai":

            st.header("🤖 AI Tools")

            col1, col2 = st.columns(2)

            with col1:
                ai_storyteller(df)
                ai_query_engine(df)

            with col2:
                ai_sql_engine(df)
                generate_insights(df)

        # ============================
        # RISK DETECTION
        # ============================
        elif st.session_state.page == "risk":

            st.header("⚠ Risk Detection")

            detect_anomalies(df)

        # ============================
        # REPORTS
        # ============================
        elif st.session_state.page == "reports":

            st.header("📑 Reports")

            col1, col2 = st.columns(2)

            with col1:
                generate_executive_report(df)

            with col2:
                generate_stakeholder_report(df)

    except Exception as e:

        st.error(f"Error loading dataset: {e}")

else:

    st.info("Please upload a dataset to start.")