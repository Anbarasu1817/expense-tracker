import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import time

# -----------------------------
# Login Check
# -----------------------------
if not st.session_state.get("logged_in", False):
    st.error("Please Login First")
    st.stop()

# -----------------------------
# Custom CSS Animation
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
st.sidebar.title("Expense Tracker")

st.sidebar.success(
    f"Welcome {st.session_state.get('username','User')}"
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

    expenses = requests.get(
        "https://expense-tracker-1-3jd3.onrender.com"
    ).json()

    income = requests.get(
        "https://expense-tracker-1-3jd3.onrender.com"
    ).json()

    total_income = sum(
        item["amount"]
        for item in income
    )

    total_expense = sum(
        item["amount"]
        for item in expenses
    )

    savings = total_income - total_expense

    # -----------------------------
    # Animated Cards
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Income</h3>
            <div class="big-font">
                ₹{total_income:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💸 Expense</h3>
            <div class="big-font">
                ₹{total_expense:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏦 Savings</h3>
            <div class="big-font">
                ₹{savings:,.0f}
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

        st.subheader("Savings Rate")

        st.progress(
            min(int(savings_rate), 100)
        )

        st.success(
            f"{savings_rate:.1f}% of your income is saved"
        )

    # -----------------------------
    # Charts
    # -----------------------------
    if expenses:

        categories = {}

        for item in expenses:

            cat = item["category"]

            if cat not in categories:
                categories[cat] = 0

            categories[cat] += item["amount"]

        st.subheader("Expense Distribution")

        pie_fig = px.pie(
            names=list(categories.keys()),
            values=list(categories.values()),
            hole=0.4,
            title="Expense Breakdown"
        )

        st.plotly_chart(
            pie_fig,
            width="stretch"
        )

        bar_fig = px.bar(
            x=list(categories.keys()),
            y=list(categories.values()),
            title="Category Wise Spending"
        )

        st.plotly_chart(
            bar_fig,
            width="stretch"
        )

        top_category = max(
            categories,
            key=categories.get
        )

        st.info(
            f"🔥 Highest Spending Category: "
            f"{top_category}"
        )

    # -----------------------------
    # Recent Expenses
    # -----------------------------
    st.subheader("Recent Expenses")

    if expenses:

        df = pd.DataFrame(expenses)

        st.dataframe(
            df,
            width="stretch"
        )

    else:
        st.warning("No Expenses Found")

except Exception as e:
    st.error(f"Error: {e}")