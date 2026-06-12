import streamlit as st
import requests
from datetime import datetime

BACKEND_URL = "https://expense-tracker-1-3jd3.onrender.com"

# -----------------------------
# Login Check
# -----------------------------
if "user_id" not in st.session_state:
    st.error("Please Login First")
    st.stop()

st.title("✏️ Edit Expense")

try:

    response = requests.get(
        f"{BACKEND_URL}/expenses/{st.session_state['user_id']}",
        timeout=30
    )

    if not response.ok:
        st.error("Failed to load expenses")
        st.write("Status Code:", response.status_code)
        st.write("Response:", response.text)
        st.stop()

    expenses = response.json()

    if len(expenses) == 0:
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
        "Amount (₹)",
        min_value=1.0,
        value=float(expense["amount"])
    )

    categories = [
        "Food",
        "Transport",
        "Bills",
        "Health",
        "Entertainment",
        "Shopping",
        "Other"
    ]

    current_category = expense.get("category", "Other")

    if current_category not in categories:
        current_category = "Other"

    category = st.selectbox(
        "Category",
        categories,
        index=categories.index(current_category)
    )

    expense_date = st.date_input(
        "Date",
        value=datetime.strptime(
            expense["date"],
            "%Y-%m-%d"
        ).date()
    )

    if st.button("✅ Update Expense"):

        if title.strip() == "":
            st.warning("Please enter expense title")

        else:

            data = {
                "title": title.strip(),
                "amount": float(amount),
                "category": category,
                "date": str(expense_date),
                "user_id": st.session_state["user_id"]
            }

            update_response = requests.put(
                f"{BACKEND_URL}/expenses/{expense['id']}",
                json=data,
                timeout=30
            )

            if update_response.ok:

                st.success(
                    "Expense Updated Successfully ✅"
                )

                st.balloons()

            else:

                st.error(
                    f"Update Failed ({update_response.status_code})"
                )

                st.write(update_response.text)

except requests.exceptions.ConnectionError:

    st.error(
        "Cannot connect to backend server."
    )

except requests.exceptions.Timeout:

    st.error(
        "Request timeout."
    )

except Exception as e:

    st.error(
        f"Error: {e}"
    )

st.divider()

st.info(
    "💡 Tip: Keep expense records updated for accurate reports."
)