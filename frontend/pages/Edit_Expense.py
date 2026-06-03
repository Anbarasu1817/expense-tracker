import streamlit as st
import requests
from datetime import datetime

st.title("Edit Expense")

try:

    response = requests.get(
        "http://127.0.0.1:8000/expenses"
    )

    expenses = response.json()

    if not expenses:
        st.warning("No Expenses Found")
        st.stop()

    expense = st.selectbox(
        "Select Expense",
        expenses,
        format_func=lambda x:
        f"{x['title']} - ₹{x['amount']}"
    )

    title = st.text_input(
        "Title",
        value=expense.get("title", "")
    )

    amount = st.number_input(
        "Amount",
        min_value=1.0,
        value=float(expense["amount"])
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Bills",
            "Health",
            "Entertainment",
            "Shopping",
            "Other"
        ],
        index=[
            "Food",
            "Transport",
            "Bills",
            "Health",
            "Entertainment",
            "Shopping",
            "Other"
        ].index(expense["category"])
    )

    expense_date = st.date_input(
        "Date",
        value=datetime.strptime(
            expense["date"],
            "%Y-%m-%d"
        ).date()
    )

    if st.button("Update Expense"):

        data = {
            "title": title,
            "amount": amount,
            "category": category,
            "date": str(expense_date)
        }

        response = requests.put(
            f"http://127.0.0.1:8000/expenses/{expense['id']}",
            json=data
        )

        if response.status_code == 200:
            st.success("Expense Updated")
        else:
            st.error(response.text)

except Exception as e:
    st.error(str(e))