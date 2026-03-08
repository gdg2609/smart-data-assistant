import streamlit as st
from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    st.subheader("⚠ Risk & Anomaly Detection")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns available")
        return

    measure_col = df[numeric_cols].std().idxmax()

    # IQR Outliers
    q1 = df[measure_col].quantile(0.25)
    q3 = df[measure_col].quantile(0.75)

    iqr = q3 - q1

    outliers = df[
        (df[measure_col] < q1 - 1.5 * iqr) |
        (df[measure_col] > q3 + 1.5 * iqr)
    ]

    st.write("IQR Outliers:", len(outliers))

    # Isolation Forest
    model = IsolationForest(contamination=0.05, random_state=42)

    df["anomaly"] = model.fit_predict(df[[measure_col]])

    anomalies = df[df["anomaly"] == -1]

    st.write("IsolationForest Anomalies:", len(anomalies))

    st.dataframe(anomalies.head())