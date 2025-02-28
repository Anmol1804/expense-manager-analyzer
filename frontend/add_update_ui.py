import streamlit as st
from datetime import datetime
import requests as req

API_URL = "http://localhost:4040"

def add_update_tab():
    selected_date = st.date_input("Enter date", datetime(2024, 8, 1), label_visibility="collapsed")

    res = req.get(f"{API_URL}/expenses/{selected_date}")
    if res.status_code == 200:
        existing_expeneses = res.json()
        # st.write(existing_expeneses)
    else:
        st.error("Failed to retrieve expenses")
        existing_expeneses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        col1.text("Amount")
        col2.text("Category")
        col3.text("Notes")

        expenses = []
        for i in range(5):
            if i < len(existing_expeneses):
                amount = existing_expeneses[i]['amount']
                category = existing_expeneses[i]['category']
                notes = existing_expeneses[i]['notes']

            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}",
                                               label_visibility="collapsed")

            with col2:
                category_input = st.selectbox(label="Category", options=categories, key=f"category_{i}",
                                              index=categories.index(category), label_visibility="collapsed")

            with col3:
                notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })
        submit_button = st.form_submit_button()
        # generally values retrieved will be shown
        #  but if we enter new or modify values then it updates the values
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]

            res = req.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)

            if res.status_code == 200:
                st.success("Expenses updated successfully")
            else:
                st.error("Failed to update expenses")