import json

import streamlit as st
from datetime import datetime
import requests as req
import pandas as pd

API_URL = "http://localhost:4040"

def analytics_month_tab():

    res = req.get(f"{API_URL}/analytics3/")
    res = res.json()

    '''
    # Convert to DataFrame
    df = pd.DataFrame(res)

    # st.write(df)

    # Convert 'expense_date' to datetime format
    df["expense_date"] = pd.to_datetime(df["expense_date"])

    # Group by year-month and sum the amounts
    monthly_totals = df.groupby(df["expense_date"].dt.to_period("M"))["amount"].sum().reset_index()
    # Convert period to string
    monthly_totals["expense_date"] = monthly_totals["expense_date"].astype(str)
    # monthly_totals = monthly_totals.rename({"expense_date" : "month", "amount" : "total"})
    monthly_totals.rename(columns={"expense_date": "month", "amount": "total"}, inplace=True)

    st.write(monthly_totals)

    st.title("Expenses Breakdown by Month")
    df_reformed = monthly_totals.set_index("month")["total"]
    st.bar_chart(df_reformed)
    st.write(df_reformed)
    '''

#     fetching dierctly from db
    df = pd.DataFrame(res)
    df_reformed = df.set_index("month")["total_amount"]
    st.bar_chart(df_reformed)
    st.table(df_reformed)

