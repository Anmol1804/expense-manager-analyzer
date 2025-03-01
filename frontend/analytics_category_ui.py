import json

import streamlit as st
from datetime import datetime
import requests as req
import pandas as pd

API_URL = "http://localhost:4040"

def analytics_tab():

    col1, col2 = st.columns(2)
    with col1:
        st_date = st.date_input("Start date", datetime(2024, 8, 1))

    with col2:
        end_date = st.date_input("End date", datetime(2024, 8, 5))


    if st.button("Get Analytics"):
        payload = {
            "start_date" : st_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        res = req.post(f"{API_URL}/analytics/", json=payload)
        res = res.json()

        # df with 3 cols for cat, total, percent format
        # df = pd.DataFrame({
        #     "Category" : ["Rent", "Shopping"],
        #     "Total" : [12123,234],
        #     "Percentage" : [10, 4]
        # })

        data = {
            "Category" : list(res.keys()),
            "Total" : [res[cat]["total"] for cat in res],
            "Percentage": [res[cat]["percentage"] for cat in res],
        }
        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Percentage", ascending=False)

        # bar chart
        # Also in barchart we have to setindex to category
        # else its index is 0,1,2 etc and it display againt it
        # st.bar_chart(data=df_sorted)

        # plotting category - index vs percentage - values
        st.title("Expenses Breakdown by category")
        df_reformed = df_sorted.set_index("Category")["Percentage"]
        # st.write(df_reformed)
        st.bar_chart(df_reformed)

        # table
        st.table(df_sorted)
