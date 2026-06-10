import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "https://expense-tracker-1-3jd3.onrender.com"

# -----------------------------
# Login Check
# -----------------------------
if "user_id" not in st.session_state:
    st.error("Please Login First")
    st.switch_page("Login.py")
    st.stop()

st.title("📜 Expense History")

# Refresh Button
if st.button("🔄 Refresh"):
    st.rerun()

try:

    response = requests.get(
        f"{BACKEND_URL}/expenses/{st.session_state['user_id']}",
        timeout=30
    )

    if not response.ok:
        st.error("Failed to load expenses")
        st.stop()

    expenses = response.json()

    if expenses:

        total_expense = sum(
            float(e["amount"])
            for e in expenses
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "📊 Total Expenses",
            len(expenses)
        )

        col2.metric(
            "💰 Total Amount",
            f"₹{total_expense:,.2f}"
        )

        st.divider()

        search = st.text_input(
            "🔍 Search Expense"
        )

        categories = ["All"] + sorted(
            list(
                set(
                    e["category"]
                    for e in expenses
                )
            )
        )

        selected_category = st.selectbox(
            "📂 Filter Category",
            categories
        )

        filtered = expenses

        if search:

            filtered = [
                e for e in filtered
                if search.lower()
                in e.get(
                    "title",
                    ""
                ).lower()
            ]

        if selected_category != "All":

            filtered = [
                e for e in filtered
                if e["category"]
                == selected_category
            ]

        st.subheader(
            f"Showing {len(filtered)} Expenses"
        )

        for expense in filtered:

            with st.expander(
                f"💸 ₹{expense['amount']} - {expense['category']}"
            ):

                st.write(
                    f"**Title:** {expense.get('title', 'N/A')}"
                )

                st.write(
                    f"**Category:** {expense['category']}"
                )

                st.write(
                    f"**Amount:** ₹{expense['amount']}"
                )

                st.write(
                    f"**Date:** {expense.get('date', 'N/A')}"
                )

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{expense['id']}"
                ):

                    delete_response = requests.delete(
                        f"{BACKEND_URL}/expenses/{expense['id']}/{st.session_state['user_id']}",
                        timeout=30
                    )

                    if delete_response.ok:

                        st.success(
                            "Expense Deleted Successfully ✅"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Failed to delete expense"
                        )

        st.divider()

        df = pd.DataFrame(filtered)

        st.download_button(
            label="📥 Download CSV",
            data=df.to_csv(index=False),
            file_name="my_expenses.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "📭 No Expenses Found"
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