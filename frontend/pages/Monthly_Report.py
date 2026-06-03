import streamlit as st
import requests
import pandas as pd

if not st.session_state.get("logged_in", False):
    st.error("Please Login First")
    st.stop()

st.title("Monthly Report")

try:

    expenses = requests.get(
        "http://127.0.0.1:8000/expenses"
    ).json()

    if expenses:

        df = pd.DataFrame(expenses)

        df["date"] = pd.to_datetime(df["date"])

        report = (
            df.groupby(df["date"].dt.month)["amount"]
            .sum()
            .reset_index()
        )

        report.columns = ["Month", "Total Expense"]

        st.subheader("Monthly Expense Summary")

        st.dataframe(report)

        st.bar_chart(
            report.set_index("Month")
        )

        st.subheader("Export Report")

        st.markdown(
            "[📄 Download PDF Report](http://127.0.0.1:8000/export-pdf)"
        )

    else:
        st.warning("No Expense Data Found")

except Exception as e:
    st.error(e)