import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "https://expense-tracker-1-3jd3.onrender.com"

# Login Check
if not st.session_state.get("logged_in", False):
    st.error("Please Login First")
    st.stop()

st.title("📊 Monthly Report")

try:

    response = requests.get(
        f"{BACKEND_URL}/expenses",
        timeout=30
    )

    if not response.ok:
        st.error("Failed to fetch expenses")
        st.stop()

    expenses = response.json()

    if expenses:

        df = pd.DataFrame(expenses)

        df["date"] = pd.to_datetime(df["date"])

        report = (
            df.groupby(
                df["date"].dt.strftime("%B")
            )["amount"]
            .sum()
            .reset_index()
        )

        report.columns = [
            "Month",
            "Total Expense"
        ]

        st.subheader(
            "📅 Monthly Expense Summary"
        )

        st.dataframe(
            report,
            use_container_width=True
        )

        st.subheader(
            "📈 Expense Chart"
        )

        st.bar_chart(
            data=report,
            x="Month",
            y="Total Expense"
       )

        total_expense = report[
            "Total Expense"
        ].sum()

        st.metric(
            "💰 Total Expenses",
            f"₹{total_expense:,.2f}"
        )

        st.divider()

        st.subheader(
            "📥 Export Report"
        )

        csv = report.to_csv(
            index=False
        )

        st.download_button(
            label="⬇ Download CSV Report",
            data=csv,
            file_name="monthly_report.csv",
            mime="text/csv"
        )

        st.link_button(
            "📄 Download PDF Report",
            f"{BACKEND_URL}/export-pdf"
        )

    else:

        st.warning(
            "No Expense Data Found"
        )

except requests.exceptions.ConnectionError:

    st.error(
        "Cannot connect to backend server."
    )

except requests.exceptions.Timeout:

    st.error(
        "Request Timeout."
    )

except Exception as e:

    st.error(
        f"Error: {e}"
    )