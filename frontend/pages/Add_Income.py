import streamlit as st
import requests
from datetime import date

st.title("Add Income")

source = st.text_input("Income Source")

amount = st.number_input(
    "Amount",
    min_value=1.0,
    step=1.0
)

income_date = st.date_input(
    "Date",
    value=date.today()
)

if st.button("Add Income"):

    if source == "":

        st.warning("Enter Source")

    else:

        response = requests.post(
            "https://expense-tracker-1-3jd3.onrender.com/income",
            json={
                "amount": amount,
                "source": source,
                "date": str(income_date)
            }
        )

        if response.status_code == 200:

            st.success("Income Added")

        else:

            st.error(response.text)