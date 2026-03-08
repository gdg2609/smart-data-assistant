import streamlit as st


def apply_filters(df):

    st.sidebar.header("📊 Global Filters")

    filtered_df = df.copy()

    text_cols = df.select_dtypes(include="object").columns

    for col in text_cols:

        unique_vals = df[col].dropna().unique()

        if len(unique_vals) < 30:  # avoid huge filters

            selected = st.sidebar.multiselect(
                f"Select {col}",
                unique_vals,
                default=unique_vals
            )

            filtered_df = filtered_df[
                filtered_df[col].isin(selected)
            ]

    return filtered_df