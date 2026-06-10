import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import time

BACKEND_URL = "https://expense-tracker-1-3jd3.onrender.com"

# -----------------------------
# Login Check
# -----------------------------
if not st.session_state.get("logged_in", False):
    st.error("Please Login First")
    st.stop()

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.metric-card{
    padding:20px;
    border-radius:15px;
    background:linear-gradient(135deg,#4facfe,#00f2fe);
    color:white;
    text-align:center;
    margin-bottom:10px;
    transition:0.3s;
}

.metric-card:hover{
    transform:scale(1.05);
}

.big-font{
    font-size:30px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("💰 Expense Tracker")

st.sidebar.success(
    f"Welcome {st.session_state.get('username', 'User')}"
)

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state.pop("username", None)
    st.rerun()

# -----------------------------
# Title
# -----------------------------
st.title("📊 Financial Dashboard")

# -----------------------------
# Loading Animation
# -----------------------------
with st.spinner("Loading Dashboard..."):
    time.sleep(1)

try:

    expenses_response = requests.get(
        f"{BACKEND_URL}/expenses/{st.session_state['user_id']}",
        timeout=30
    )

    income_response = requests.get(
        f"{BACKEND_URL}/income/{st.session_state['user_id']}",
        timeout=30
    )

    expenses = expenses_response.json()
    income = income_response.json()

    # -----------------------------
    # Total Calculations
    # -----------------------------
    total_income = sum(
        float(item.get("amount", 0))
        for item in income
    )

    total_expense = sum(
        float(item.get("amount", 0))
        for item in expenses
    )

    savings = total_income - total_expense

    # -----------------------------
    # Summary Cards
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Income</h3>
            <div class="big-font">
                ₹{total_income:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💸 Expense</h3>
            <div class="big-font">
                ₹{total_expense:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏦 Savings</h3>
            <div class="big-font">
                ₹{savings:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # Savings Rate
    # -----------------------------
    if total_income > 0:

        savings_rate = (
            savings / total_income
        ) * 100

        st.subheader("📈 Savings Rate")

        st.progress(
            min(int(max(savings_rate, 0)), 100)
        )

        st.success(
            f"{savings_rate:.1f}% of your income is saved"
        )

    # -----------------------------
    # Expense Charts
    # -----------------------------
    if expenses:

        categories = {}

        for item in expenses:

            category = item.get(
                "category",
                "Other"
            )

            amount = float(
                item.get("amount", 0)
            )

            categories[category] = (
                categories.get(category, 0)
                + amount
            )

        st.subheader("📊 Expense Distribution")

        pie_fig = px.pie(
            names=list(categories.keys()),
            values=list(categories.values()),
            hole=0.4,
            title="Expenses by Category"
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

        bar_fig = px.bar(
            x=list(categories.keys()),
            y=list(categories.values()),
            title="Category Wise Spending",
            labels={
                "x": "Category",
                "y": "Amount"
            }
        )

        st.plotly_chart(
            bar_fig,
            use_container_width=True
        )

        top_category = max(
            categories,
            key=categories.get
        )

        st.info(
            f"🔥 Highest Spending Category: "
            f"{top_category} "
            f"(₹{categories[top_category]:,.2f})"
        )

    # -----------------------------
    # Recent Expenses
    # -----------------------------
    st.subheader("📜 Recent Expenses")

    if expenses:

        df = pd.DataFrame(expenses)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning(
            "No Expenses Found"
        )

except requests.exceptions.ConnectionError:

    st.error(
        "Unable to connect to backend server."
    )

except requests.exceptions.Timeout:

    st.error(
        "Request timed out."
    )

except Exception as e:

    st.error(
        f"Error: {e}"
    )