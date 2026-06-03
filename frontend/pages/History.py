import streamlit as st
import requests
import pandas as pd

st.title("📜 Expense History")

# Refresh Button
if st.button("🔄 Refresh"):
    st.rerun()

try:

    response = requests.get(
        "http://127.0.0.1:8000/expenses"
    )

    expenses = response.json()

    if expenses:

        # Summary Cards
        total_expense = sum(
            e["amount"]
            for e in expenses
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "📊 Total Expenses",
            len(expenses)
        )

        col2.metric(
            "💰 Total Amount",
            f"₹{total_expense:,.0f}"
        )

        st.divider()

        # Search Box
        search = st.text_input(
            "🔍 Search Expense"
        )

        # Category Filter
        categories = [
            "All"
        ] + sorted(
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

        # Filtering
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

        # Expense List
        for expense in filtered:

            with st.expander(
                f"💸 ₹{expense['amount']} - "
                f"{expense['category']}"
            ):

                st.write(
                    f"**Title:** "
                    f"{expense.get('title','N/A')}"
                )

                st.write(
                    f"**Category:** "
                    f"{expense['category']}"
                )

                st.write(
                    f"**Amount:** "
                    f"₹{expense['amount']}"
                )

                st.write(
                    f"**Date:** "
                    f"{expense.get('date','N/A')}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{expense['id']}"
                    ):

                        requests.delete(
                            f"http://127.0.0.1:8000/expenses/{expense['id']}"
                        )

                        st.success(
                            "Expense Deleted"
                        )

                        st.rerun()

                with col2:

                    st.button(
                        "✏ Edit",
                        key=f"edit_{expense['id']}"
                    )

        # CSV Download
        st.divider()

        df = pd.DataFrame(filtered)

        st.download_button(
            "📥 Download CSV",
            df.to_csv(index=False),
            "expenses.csv",
            "text/csv"
        )

    else:

        st.info(
            "📭 No expenses found"
        )

except Exception as e:

    st.error(
        f"Error: {e}"
    )