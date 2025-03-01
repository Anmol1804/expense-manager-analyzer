from fastapi import FastAPI, HTTPException
from datetime import date

import db_helper
from typing import List
from pydantic import BaseModel

class Expense(BaseModel):
    amount : float
    category : str
    notes : str

class DateRange(BaseModel):
    start_date : date
    end_date : date

app = FastAPI()
# uvicorn server:app --port 4000 --reload


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date : date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code = 500, detail = "Failed to retrieve data")

    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expenses(expense_date : date, expenses :List[Expense]):
    # in UI we delete all expense from scratch and inserting again for a particular date
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

    return {"message" : "Expenses updated successfully"}

@app.post("/analytics/")
def get_analytics(date_range : DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code = 500, detail = "Failed to retrieve data")

    total = sum([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage = (row['total']*100)/total if total != 0 else 0

        breakdown[row["category"]] = {
            "total" : row['total'],
            "percentage" : percentage
        }

    return breakdown

@app.get("/analytics2/")
def analytics_by_month():
    expenses = db_helper.fetch_all_records()
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve data")
    return expenses

@app.get("/analytics2/")
def analytics_by_month():
    expenses = db_helper.fetch_all_records()
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve data")
    return expenses

@app.get("/analytics3/")
def analytics_by_month():
    expenses = db_helper.fetch_total_expense_by_month()
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve data")
    return expenses