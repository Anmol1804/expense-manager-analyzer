from backend import db_helper

def test_fetch_expenses_for_date():
    expenses = db_helper.fetch_expenses_for_date("2024-08-15")
    assert len(expenses) == 1
    assert expenses[0]["amount"] == 10
    assert expenses[0]["category"] == "Shopping"
    assert expenses[0]["notes"] == "Bought potatoes"

def test_fetch_expenses_for_invalid_date():
    pass

def test_fetch_expenses_summary_range():
    pass

def test_fetch_expenses_summary_invalid_range():
    pass