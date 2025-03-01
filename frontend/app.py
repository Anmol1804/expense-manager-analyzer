import streamlit as st
from analytics_category_ui import  analytics_tab
from add_update_ui import add_update_tab
from analytics_month_ui import analytics_month_tab

API_URL = "http://localhost:4040"

st.title("Expense Tracking System")

tab1, tab2, tab3  = st.tabs(["Add/Update", "Analytics By Category", "Analytics By Month"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()

with tab3:
    analytics_month_tab()