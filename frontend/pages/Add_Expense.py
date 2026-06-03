import streamlit as st
import requests
from datetime import date

st.title("💸 Add Expense")

# Quick Category Buttons
st.subheader("Quick Select")

col1, col2, col3, col4 = st.columns(4)

if col1.button("🍔 Food"):
    st.session_state["category"] = "Food"

if col2.button("🚌 Transport"):
    st.session_state["category"] = "Transport"

if col3.button("🏥 Health"):
    st.session_state["category"] = "Health"

if col4.button("🛍 Shopping"):
    st.session_state["category"] = "Shopping"

# Form
with st.form("expense_form"):

    title = st.text_input(
        "Expense Title",
        placeholder="Enter expense title"
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=1.0,
        step=1.0
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
        ].index(
            st.session_state.get(
                "category",
                "Food"
            )
        )
    )

    expense_date = st.date_input(
        "Date",
        value=date.today()
    )

    submitted = st.form_submit_button(
        "➕ Add Expense"
    )

if submitted:

    data = {
        "title": title,
        "amount": amount,
        "category": category,
        "date": str(expense_date)
    }

    try:

        response = requests.post(
            "http://127.0.0.1:8000/expenses",
            json=data
        )

        if response.status_code == 200:

            st.success(
                "Expense Added Successfully ✅"
            )

            st.balloons()

        else:

            st.error(
                f"Error: {response.text}"
            )

    except Exception as e:

        st.error(
            f"Backend Error: {e}"
        )

# Expense Tips
st.divider()

st.info(
    "💡 Tip: Record expenses daily to track spending accurately."
)

# Clear Selection Button
if st.button("🔄 Reset Form"):
    st.session_state["category"] = "Food"
    st.rerun()