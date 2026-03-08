import streamlit as st
import plotly.express as px


def ai_query_engine(df):

    st.subheader("🧠 AI Data Q&A")

    question = st.text_input(
        "Ask a question about your data",
        placeholder="Example: Which city has highest sales?"
    )

    if not question:
        return

    question = question.lower()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()

    if not numeric_cols:
        st.warning("Dataset has no numeric columns.")
        return

    if not text_cols:
        st.warning("Dataset has no categorical columns.")
        return

    # ------------------------------------------------
    # Synonym dictionaries
    # ------------------------------------------------

    metric_synonyms = {
        "revenue": "charges",
        "amount": "charges",
        "cost": "charges",
        "claim": "charges",
        "income": "charges"
    }

    category_synonyms = {
        "location": "region",
        "place": "region",
        "city": "region",
        "area": "region",
        "gender": "sex"
    }

    # ------------------------------------------------
    # Detect metric (numeric column)
    # ------------------------------------------------

    metric = None

    for col in numeric_cols:
        if col.lower() in question:
            metric = col
            break

    if metric is None:
        for word, col in metric_synonyms.items():
            if word in question and col in numeric_cols:
                metric = col
                break

    if metric is None:
        metric = numeric_cols[0]

    # ------------------------------------------------
    # Detect category column
    # ------------------------------------------------

    category = None

    for col in text_cols:
        if col.lower() in question:
            category = col
            break

    if category is None:
        for word, col in category_synonyms.items():
            if word in question and col in text_cols:
                category = col
                break

    if category is None:
        category = text_cols[0]

    # ------------------------------------------------
    # Detect intent
    # ------------------------------------------------

    intent = None

    if "highest" in question or "max" in question:
        intent = "highest"

    elif "lowest" in question or "min" in question:
        intent = "lowest"

    elif "distribution" in question:
        intent = "distribution"

    elif "top" in question:
        intent = "top"

    # ------------------------------------------------
    # Highest
    # ------------------------------------------------

    if intent == "highest":

        pivot = df.groupby(category)[metric].mean().reset_index()

        row = pivot.loc[pivot[metric].idxmax()]

        st.markdown("### Answer")

        st.write(
            f"**{row[category]}** has the highest average **{metric}**."
        )

        fig = px.bar(
            pivot,
            x=category,
            y=metric,
            title=f"{metric} by {category}"
        )

        st.plotly_chart(fig, use_container_width=True)

        return

    # ------------------------------------------------
    # Lowest
    # ------------------------------------------------

    if intent == "lowest":

        pivot = df.groupby(category)[metric].mean().reset_index()

        row = pivot.loc[pivot[metric].idxmin()]

        st.markdown("### Answer")

        st.write(
            f"**{row[category]}** has the lowest average **{metric}**."
        )

        fig = px.bar(
            pivot,
            x=category,
            y=metric,
            title=f"{metric} by {category}"
        )

        st.plotly_chart(fig, use_container_width=True)

        return

    # ------------------------------------------------
    # Top 5
    # ------------------------------------------------

    if intent == "top":

        pivot = df.groupby(category)[metric].mean().reset_index()

        pivot = pivot.sort_values(metric, ascending=False).head(5)

        st.markdown("### Top 5")

        fig = px.bar(
            pivot,
            x=category,
            y=metric,
            title=f"Top {category} by {metric}"
        )

        st.plotly_chart(fig, use_container_width=True)

        return

    # ------------------------------------------------
    # Distribution
    # ------------------------------------------------

    if intent == "distribution":

        fig = px.histogram(
            df,
            x=metric,
            title=f"{metric} Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        return

    # ------------------------------------------------
    # Help message
    # ------------------------------------------------

    st.info(
        "Try questions like:\n\n"
        "- Which location has highest revenue?\n"
        "- Which region has lowest charges?\n"
        "- Top 5 regions by charges\n"
        "- Show charges distribution"
    )