import streamlit as st
import requests

st.title("Register")

username = st.text_input("Username")
password = st.text_input(
    "Password",
    type="password"
)

if st.button("Register"):

    if username == "" or password == "":
        st.warning("Please fill all fields")

    else:

        try:

            response = requests.post(
                "http://127.0.0.1:8000/register",
                json={
                    "username": username,
                    "password": password
                }
            )

            if response.status_code == 200:

                try:
                    result = response.json()

                    if "message" in result:

                        if result["message"] == "Registered Successfully":
                            st.success(result["message"])

                        else:
                            st.warning(result["message"])

                    else:
                        st.error("Invalid response from server")

                except Exception:
                    st.error(
                        f"Server returned non-JSON response:\n{response.text}"
                    )

            else:
                st.error(
                    f"Server Error ({response.status_code})"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to backend. Start FastAPI server first."
            )

        except Exception as e:
            st.error(str(e))