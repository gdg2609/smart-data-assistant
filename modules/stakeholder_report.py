import pandas as pd
import streamlit as st
import io


def generate_stakeholder_report(df):

    st.subheader("📊 Stakeholder Report")

    if st.button("Download Stakeholder Report (Excel)"):

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        text_cols = df.select_dtypes(include="object").columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns found")
            return

        metric = df[numeric_cols].std().idxmax()

        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

            workbook = writer.book

            # -------------------------
            # Executive Summary
            # -------------------------

            summary = pd.DataFrame({
                "Metric": [
                    "Total Records",
                    f"Average {metric}",
                    f"Sum {metric}",
                    f"Maximum {metric}"
                ],
                "Value": [
                    len(df),
                    df[metric].mean(),
                    df[metric].sum(),
                    df[metric].max()
                ]
            })

            summary.to_excel(
                writer,
                sheet_name="Executive_Summary",
                index=False
            )

            # -------------------------
            # Category Analysis
            # -------------------------

            for col in text_cols:

                if df[col].nunique() > 50:
                    continue

                pivot = (
                    df.groupby(col)[metric]
                    .agg(["mean", "sum", "count"])
                    .reset_index()
                )

                sheet_name = f"Analysis_{col}"

                pivot.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False
                )

                worksheet = writer.sheets[sheet_name]

                chart = workbook.add_chart({
                    "type": "column"
                })

                chart.add_series({
                    "name": f"Average {metric}",
                    "categories": [sheet_name, 1, 0, len(pivot), 0],
                    "values": [sheet_name, 1, 1, len(pivot), 1],
                })

                chart.set_title({
                    "name": f"{metric} by {col}"
                })

                worksheet.insert_chart("G2", chart)

            # -------------------------
            # Full Dataset
            # -------------------------

            df.to_excel(
                writer,
                sheet_name="Full_Dataset",
                index=False
            )

        output.seek(0)

        st.download_button(
            label="📥 Download Stakeholder Report (Excel)",
            data=output,
            file_name="Stakeholder_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )