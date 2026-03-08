import streamlit as st


def ai_storyteller(df):

    st.subheader("🧠 AI Data Storyteller")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns available")
        return

    # choose main metric
    metric = df[numeric_cols].std().idxmax()

    avg_val = df[metric].mean()
    max_val = df[metric].max()

    insights = []

    insights.append(f"Average {metric} is {avg_val:.2f}")
    insights.append(f"Maximum {metric} recorded is {max_val:.2f}")

    # category insights
    if text_cols:

        category = text_cols[0]

        group = df.groupby(category)[metric].mean()

        top_cat = group.idxmax()

        insights.append(
            f"{top_cat} has the highest average {metric}"
        )

    st.markdown("### Key Insights")

    for i in insights:
        st.write("•", i)