import streamlit as st
import pandas as pd


def ai_sql_engine(df):

    st.subheader("🤖 AI → SQL Engine")

    query = st.text_input("Ask a data question")

    if not query:
        return

    query = query.lower()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()

    # -------------------------
    # TOTAL BY CATEGORY
    # -------------------------
    if "total" in query and "by" in query:

        parts = query.split("by")

        measure = parts[0].replace("total", "").strip()
        category = parts[1].strip()

        measure_col = None
        category_col = None

        for col in numeric_cols:
            if measure in col:
                measure_col = col

        for col in text_cols:
            if category in col:
                category_col = col

        if measure_col and category_col:

            result = (
                df.groupby(category_col)[measure_col]
                .sum()
                .reset_index()
            )

            st.dataframe(result)

            return

    # -------------------------
    # AVERAGE
    # -------------------------
    if "average" in query:

        for col in numeric_cols:

            if col in query:

                avg_val = df[col].mean()

                st.write(f"Average {col}: {avg_val:.2f}")

                return

    # -------------------------
    # TOP N
    # -------------------------
    if "top" in query:

        words = query.split()

        n = 5

        for w in words:
            if w.isdigit():
                n = int(w)

        for col in numeric_cols:

            if col in query:

                result = df.nlargest(n, col)

                st.dataframe(result)

                return

    st.warning("Could not understand the query")