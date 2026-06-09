import streamlit as st
import requests
import time
from datetime import date

BACKEND_URL = "https://expense-tracker-1-3jd3.onrender.com"

st.title("💰 Add Income")

source = st.text_input(
    "Income Source",
    placeholder="Salary, Freelancing, Business..."
)

amount = st.number_input(
    "Amount (₹)",
    min_value=1.0,
    step=1.0
)

income_date = st.date_input(
    "Date",
    value=date.today()
)

if st.button("➕ Add Income"):

    if source.strip() == "":

        st.warning("Please enter income source")

    else:

        data = {
            "source": source.strip(),
            "amount": float(amount),
            "date": str(income_date)
        }

        try:

            response = requests.post(
                f"{BACKEND_URL}/income",
                json=data,
                timeout=30
            )

            if response.ok:

                card = st.empty()

                card.markdown(
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
                        ✅ Income Added Successfully
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                time.sleep(3)

                card.empty()

            else:

                st.error(
                    f"Server Error ({response.status_code})"
                )

                st.write(response.text)

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to backend server."
            )

        except requests.exceptions.Timeout:

            st.error(
                "Request Timeout. Please try again."
            )

        except Exception as e:

            st.error(
                f"Unexpected Error: {e}"
            )

st.divider()

st.info(
    "💡 Tip: Add all income sources to track your savings accurately."
)