import streamlit as st

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Header
st.title("💰 Expense Tracker")
st.subheader("Track Expenses • Manage Income • Save Money")

# Welcome Message
st.success(
    "Welcome to your Personal Expense Tracker Dashboard 🚀"
)

# Feature Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### 💸 Expense Management

    ✔ Add Expenses

    ✔ Edit Expenses

    ✔ Delete Expenses
    """)

with col2:
    st.success("""
    ### 💰 Income Tracking

    ✔ Add Income

    ✔ View Income

    ✔ Savings Calculation
    """)

with col3:
    st.warning("""
    ### 📊 Reports

    ✔ Dashboard

    ✔ Charts

    ✔ PDF Reports
    """)

st.divider()

# Quick Navigation
st.subheader("⚡ Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔐 Login", use_container_width=True):
        st.switch_page("pages/Login.py")

with col2:
    if st.button("📝 Register", use_container_width=True):
        st.switch_page("pages/Register.py")

with col3:
    if st.button("💸 Add Expense", use_container_width=True):
        st.switch_page("pages/Add_Expense.py")

with col4:
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")

st.divider()

# Project Overview
st.subheader("📋 Project Overview")

st.write("""
This Expense Tracker helps users:

- Track daily expenses
- Record income sources
- Analyze spending habits
- Generate reports
- Download PDF summaries
- Monitor savings
""")

# Sidebar
st.sidebar.title("📂 Navigation")

st.sidebar.success("Expense Tracker System")

st.sidebar.markdown("""
### Features

✅ User Authentication

✅ Expense Management

✅ Income Tracking

✅ Dashboard Analytics

✅ Monthly Reports

✅ PDF Download
""")

# Footer
st.divider()

st.caption(
    "Developed using FastAPI + PostgreSQL + Streamlit 🚀"
)