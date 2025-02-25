import pymysql
from contextlib import contextmanager

@contextmanager
def get_db_cursor(commit=False):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    yield cursor

    # want only to use for insert cmds
    if commit:
        connection.commit()

    cursor.close()
    connection.close()

# def fetch_all_records():
#     with get_db_cursor() as cursor:
#         cursor.execute("SELECT * FROM expenses")
#         expenses = cursor.fetchall()
#
#         return expenses

def fetch_expenses_for_date(expense_date):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses where expense_date = %s",(expense_date))
        expenses = cursor.fetchall()

        return expenses
        # for expense in expenses:
        #     print(expense)

def insert_expense(expense_date, amount, category, notes):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s,%s)",
            (expense_date,amount, category, notes)
        )
    # print("Inseted a value in table")

def delete_expenses_for_date(expense_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM expenses where expense_date = %s",(expense_date)
        )
    # print("Deleted a value from table")

def fetch_expense_summary(start_date, end_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            '''
            SELECT category, SUM(amount) as total
            FROM expenses WHERE expense_date
            BETWEEN %s and %s
            GROUP BY category;
            ''', (start_date, end_date)
        )

        data = cursor.fetchall()

        return data


if __name__ == "__main__":
    # expenses = fetch_expenses_for_date("2024-08-01")
    # print(expenses)

    expenses = fetch_expense_summary("2024-08-01", "2024-08-05")
    print(expenses)

