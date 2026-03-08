import streamlit as st
import plotly.express as px


def generate_executive_report(df):

    st.subheader("📄 AI Executive Report")

    if st.button("Generate Executive Summary"):

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        text_cols = df.select_dtypes(include="object").columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns available")
            return

        # Select main metric automatically
        metric = df[numeric_cols].std().idxmax()

        avg_val = df[metric].mean()
        max_val = df[metric].max()

        # ----------------------------
        # KPI SECTION
        # ----------------------------

        st.markdown("### Key Metrics")

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Records", len(df))
        c2.metric(f"Average {metric}", f"{avg_val:.2f}")
        c3.metric(f"Max {metric}", f"{max_val:.2f}")

        # ----------------------------
        # CHART SECTION
        # ----------------------------

        if text_cols:

            category = text_cols[0]

            chart_data = (
                df.groupby(category)[metric]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                chart_data,
                x=category,
                y=metric,
                title=f"{metric} by {category}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="executive_chart"
            )

        # ----------------------------
        # EXECUTIVE INSIGHTS
        # ----------------------------

        st.markdown("### Executive Insights")

        insights = []

        insights.append(f"Total records analyzed: {len(df)}")
        insights.append(f"Average {metric}: {avg_val:.2f}")
        insights.append(f"Maximum {metric}: {max_val:.2f}")

        if text_cols:

            top_category = (
                df.groupby(category)[metric]
                .mean()
                .idxmax()
            )

            insights.append(
                f"{top_category} shows the highest average {metric}"
            )

        for i in insights:
            st.write("•", i)

        # ----------------------------
        # FULL DATASET
        # ----------------------------

        st.markdown("### Full Dataset")

        st.dataframe(
            df,
            use_container_width=True
        )

        # ----------------------------
        # DOWNLOAD DATA
        # ----------------------------

        csv = df.to_csv(index=False)

        st.download_button(
            label="📥 Download Dataset (CSV)",
            data=csv,
            file_name="executive_report_data.csv",
            mime="text/csv"
        )