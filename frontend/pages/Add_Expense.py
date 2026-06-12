import streamlit as st
import requests
import time
from datetime import date

BACKEND_URL = "https://expense-tracker-1-3jd3.onrender.com"

# -----------------------------
# Login Check
# -----------------------------
if "user_id" not in st.session_state:
    st.error("Please Login First")
    st.switch_page("Login.py")
    st.stop()

st.title("💸 Add Expense")

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

categories = [
    "Food",
    "Transport",
    "Bills",
    "Health",
    "Entertainment",
    "Shopping",
    "Other"
]

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
        categories,
        index=categories.index(
            st.session_state.get("category", "Food")
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

        try:

            response = requests.post(
                f"{BACKEND_URL}/expenses",
                json=data,
                timeout=30
            )

            if response.ok:

                success_card = st.empty()

                success_card.markdown(
                    """
                    <div style="
                        padding:15px;
                        border-radius:10px;
                        background-color:#d4edda;
                        border:1px solid #28a745;
                        color:#155724;
                        text-align:center;
                        font-weight:bold;
                        font-size:18px;">
                        ✅ Expense Added Successfully
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                time.sleep(2)

                success_card.empty()

            else:

                st.error(f"Server Error ({response.status_code})")
                st.code(response.text)
                

                st.write(response.text)

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to backend server."
            )

        except requests.exceptions.Timeout:

            st.error(
                "Request timeout. Try again."
            )

        except Exception as e:

            st.error(
                f"Unexpected Error: {e}"
            )

st.divider()

st.info(
    "💡 Tip: Record expenses daily to track spending accurately."
)

if st.button("🔄 Reset Form"):

    st.session_state["category"] = "Food"

    st.rerun()