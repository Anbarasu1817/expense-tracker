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

                try:

                    result = response.json()

                    if result.get("message") == "Registered Successfully":

                        st.success(
                            "✅ Registration Successful"
                        )

                        time.sleep(1)

                        st.switch_page(
                            "Login.py"
                        )

                    else:

                        st.warning(
                            result.get(
                                "message",
                                "Registration Failed"
                            )
                        )

                except Exception:

                    st.error(
                        f"Invalid Server Response\n\n{response.text}"
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
    "Already have an account?"
)

if st.button(
    "🔐 Go To Login",
    use_container_width=True
):
    st.switch_page(
        "Login.py"
    )