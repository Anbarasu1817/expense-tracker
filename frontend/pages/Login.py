import streamlit as st
import requests
import time

st.set_page_config(
    page_title="Login",
    page_icon="🔐"
)

st.title("🔐 Login")

username = st.text_input(
    "👤 Username"
)

password = st.text_input(
    "🔑 Password",
    type="password"
)

col1, col2 = st.columns(2)

with col1:
    login_btn = st.button(
        "🚀 Login",
        width="stretch"
    )

with col2:
    clear_btn = st.button(
        "🧹 Clear",
        width="stretch"
    )

if clear_btn:
    st.rerun()

if login_btn:

    if not username or not password:
        st.warning(
            "⚠ Please enter username and password"
        )

    else:

        try:

            response = requests.post(
                "http://127.0.0.1:8000/login",
                json={
                    "username": username,
                    "password": password
                }
            )

            result = response.json()

            if result.get("message") == "Login Successful":

                st.session_state["logged_in"] = True
                st.session_state["username"] = username

                st.success(
                    f"✅ Login Successful! Welcome {username}"
                )

                time.sleep(1.5)

                st.switch_page(
                    "pages/Dashboard.py"
                )

            else:

                st.error(
                    "❌ Invalid Username or Password"
                )

        except Exception as e:

            st.error(
                f"Backend Error: {e}"
            )

st.divider()

st.info(
    "💡 New user? Register first."
)

if st.button(
    "📝 Go To Register Page",
    width="stretch"
):
    st.switch_page(
        "pages/Register.py"
    )

st.sidebar.title(
    "💰 Expense Tracker"
)

st.sidebar.success(
    "Manage your money smarter"
)

st.sidebar.markdown(
    """
### Features

✅ Add Expenses

✅ Add Income

✅ Dashboard

✅ Reports

✅ PDF Export
"""
)