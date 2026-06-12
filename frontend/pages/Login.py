import streamlit as st
import requests
import time

BACKEND_URL = "https://expense-tracker-1-3jd3.onrender.com"

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

# Already Logged In
if st.session_state.get("logged_in", False):
    st.success(
        f"Already logged in as {st.session_state.get('username')}"
    )

    if st.button("Go To Dashboard"):
        st.switch_page("pages/Dashboard.py")

    st.stop()

st.title("🔐 Login")

username = st.text_input(
    "👤 Username",
    placeholder="Enter Username"
)

password = st.text_input(
    "🔑 Password",
    type="password",
    placeholder="Enter Password"
)

col1, col2 = st.columns(2)

with col1:
    login_btn = st.button(
        "🚀 Login",
        use_container_width=True
    )

with col2:
    clear_btn = st.button(
        "🧹 Clear",
        use_container_width=True
    )

if clear_btn:

    st.session_state.clear()
    st.rerun()

if login_btn:

    if username.strip() == "" or password.strip() == "":

        st.warning(
            "⚠ Please enter username and password"
        )

    else:

        try:

            response = requests.post(
                f"{BACKEND_URL}/login",
                json={
                    "username": username.strip(),
                    "password": password
                },
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                if result.get("message") == "Login Successful":

                    st.session_state["logged_in"] = True
                    st.session_state["username"] = result.get("username", username)
                    st.session_state["user_id"] = result.get("user_id")

                    st.success(
                        f"✅ Welcome {st.session_state['username']}"
                    )

                    time.sleep(1)

                    st.switch_page("pages/Dashboard.py")

                else:

                    st.error(
                        "❌ Invalid Username or Password"
                    )

            else:

                st.error(
                    f"Server Error ({response.status_code})"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to backend server."
            )

        except requests.exceptions.Timeout:

            st.error(
                "⌛ Request Timeout."
            )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

st.divider()

st.info(
    "💡 New user? Register first."
)

if st.button(
    "📝 Go To Register Page",
    use_container_width=True
):
    st.switch_page(
        "pages/Register.py"
    )

# Sidebar
st.sidebar.title("💰 Expense Tracker")

st.sidebar.success(
    "Manage your money smarter"
)

st.sidebar.markdown("""
### Features

✅ User Login

✅ Add Expenses

✅ Add Income

✅ Dashboard

✅ Expense History

✅ Reports

✅ PDF Export
""")