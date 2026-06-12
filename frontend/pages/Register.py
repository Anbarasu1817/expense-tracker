import streamlit as st
import requests
import time

BACKEND_URL = "https://expense-tracker-1-3jd3.onrender.com"

st.set_page_config(
    page_title="Register",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Register")

username = st.text_input(
    "👤 Username",
    placeholder="Enter Username"
)

password = st.text_input(
    "🔑 Password",
    type="password",
    placeholder="Enter Password"
)

register_btn = st.button(
    "🚀 Register",
    use_container_width=True
)

if register_btn:

    if username.strip() == "" or password.strip() == "":

        st.warning(
            "⚠ Please fill all fields"
        )

    elif len(password) < 4:

        st.warning(
            "⚠ Password must be at least 4 characters"
        )

    else:

        try:

            response = requests.post(
                f"{BACKEND_URL}/register",
                json={
                    "username": username.strip(),
                    "password": password
                },
                timeout=30
            )

            if response.status_code == 200:

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
                        ✅ Registration Successful
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                time.sleep(3)

                st.switch_page("pages/Login.py")

            else:

                try:
                    result = response.json()
                    st.error(
                        result.get(
                            "message",
                            f"Server Error ({response.status_code})"
                        )
                    )
                except Exception:
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