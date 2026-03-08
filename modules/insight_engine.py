import streamlit as st
import pandas as pd
import numpy as np


def generate_insights(df):

    st.subheader("📊 AI Auto Insights")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()

    insights = []

    # -----------------------------
    # Dataset Overview
    # -----------------------------

    rows, cols = df.shape

    insights.append(f"Dataset contains **{rows} rows** and **{cols} columns**.")

    # -----------------------------
    # Missing Values
    # -----------------------------

    missing = df.isnull().sum()

    missing_cols = missing[missing > 0]

    if len(missing_cols) > 0:

        for col, val in missing_cols.items():

            insights.append(
                f"⚠ Column **{col}** has **{val} missing values**."
            )

    # -----------------------------
    # Choose Important Metric
    # -----------------------------

    if numeric_cols:

        metric = df[numeric_cols].std().idxmax()

    else:

        metric = None

    # -----------------------------
    # Choose Best Category
    # -----------------------------

    if text_cols:

        category = max(text_cols, key=lambda x: df[x].nunique())

    else:

        category = None

    # -----------------------------
    # Category Insight
    # -----------------------------

    if metric and category:

        pivot = df.groupby(category)[metric].mean()

        highest = pivot.idxmax()
        lowest = pivot.idxmin()

        insights.append(
            f"📈 **{highest}** has the highest average **{metric}**."
        )

        insights.append(
            f"📉 **{lowest}** has the lowest average **{metric}**."
        )

    # -----------------------------
    # Outlier Detection
    # -----------------------------

    if metric:

        q1 = df[metric].quantile(0.25)
        q3 = df[metric].quantile(0.75)

        iqr = q3 - q1

        upper = q3 + 1.5 * iqr

        outliers = df[df[metric] > upper]

        if len(outliers) > 0:

            insights.append(
                f"⚠ Detected **{len(outliers)} unusually high values** in **{metric}**."
            )

    # -----------------------------
    # Correlation Insight
    # -----------------------------

    if len(numeric_cols) >= 2:

        corr = df[numeric_cols].corr()

        corr_pairs = corr.unstack().sort_values(ascending=False)

        for pair, value in corr_pairs.items():

            if pair[0] != pair[1] and value > 0.6:

                insights.append(
                    f"🔗 Strong relationship between **{pair[0]}** and **{pair[1]}**."
                )

                break

    # -----------------------------
    # Display Insights
    # -----------------------------

    for insight in insights:

        st.write("•", insight)