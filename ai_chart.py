import streamlit as st
import plotly.express as px
import pandas as pd


def ai_chart_builder(df):

    st.subheader("🤖 AI Chart Builder")

    query = st.text_input(
        "Describe the chart you want",
        placeholder="Example: claim by city, top 10 cities by claim"
    )

    if not query:
        return

    query = query.lower()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()

    # -----------------------------------
    # DISTRIBUTION
    # -----------------------------------

    if "distribution" in query:

        for col in numeric_cols:
            if col in query:

                fig = px.histogram(df, x=col)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key=query
                )

                return

    # -----------------------------------
    # TOP N
    # -----------------------------------

    if "top" in query:

        words = query.split()

        n = 10

        for w in words:
            if w.isdigit():
                n = int(w)

        for col in numeric_cols:

            if col in query:

                result = df.nlargest(n, col)

                fig = px.bar(
                    result,
                    x=result.index,
                    y=col,
                    title=f"Top {n} {col}"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key=query
                )

                return

    # -----------------------------------
    # BY CATEGORY
    # -----------------------------------

    if "by" in query:

        parts = query.split("by")

        metric = parts[0].strip()
        category = parts[1].strip()

        metric_col = None
        category_col = None

        for col in numeric_cols:
            if metric in col:
                metric_col = col

        for col in text_cols:
            if category in col:
                category_col = col

        if metric_col and category_col:

            result = (
                df.groupby(category_col)[metric_col]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                result,
                x=category_col,
                y=metric_col
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key=query
            )

            return

    # -----------------------------------
    # TREND OVER TIME
    # -----------------------------------

    if "trend" in query or "over time" in query:

        date_cols = df.select_dtypes(
            include=["datetime64"]
        ).columns.tolist()

        if date_cols:

            date_col = date_cols[0]
            metric = numeric_cols[0]

            trend = (
                df.groupby(date_col)[metric]
                .mean()
                .reset_index()
            )

            fig = px.line(
                trend,
                x=date_col,
                y=metric
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key=query
            )

            return

    st.info(
        "Try queries like: claim by city, claim distribution, top 10 claims"
    )