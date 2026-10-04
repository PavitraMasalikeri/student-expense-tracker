import sqlite3


def create_database():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    columns = cursor.execute(
        "PRAGMA table_info(expenses)"
    ).fetchall()

    column_names = [
        column[1]
        for column in columns
    ]

    if "username" not in column_names:
        cursor.execute(
            "ALTER TABLE expenses ADD COLUMN username TEXT"
        )

    connection.commit()
    connection.close()


def register_user(username, password):
    try:
        connection = sqlite3.connect("expenses.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, password))

        connection.commit()
        connection.close()

        return True

    except sqlite3.IntegrityError:
        return False

    except Exception:
        return False


def login_user(username, password):
    try:
        connection = sqlite3.connect("expenses.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username = ?
            AND password = ?
        """, (username, password))

        user = cursor.fetchone()

        connection.close()

        return user is not None

    except Exception:
        return False


def add_expense(username, date, category, description, amount):
    try:
        connection = sqlite3.connect("expenses.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO expenses
            (username, date, category, description, amount)
            VALUES (?, ?, ?, ?, ?)
        """, (
            username,
            date,
            category,
            description,
            amount
        ))

        connection.commit()
        connection.close()

        return True

    except Exception:
        return False


def get_expenses(username):
    try:
        connection = sqlite3.connect("expenses.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, date, category, description, amount
            FROM expenses
            WHERE username = ?
            ORDER BY id DESC
        """, (username,))

        expenses = cursor.fetchall()

        connection.close()

        return expenses

    except Exception:
        return []


def update_expense(
    username,
    expense_id,
    category,
    description,
    amount
):
    try:
        connection = sqlite3.connect("expenses.db")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE expenses
            SET category = ?,
                description = ?,
                amount = ?
            WHERE id = ?
            AND username = ?
        """, (
            category,
            description,
            amount,
            expense_id,
            username
        ))

        connection.commit()
        connection.close()

        return True

    except Exception:
        return False


def delete_expense(username, expense_id):
    try:
        connection = sqlite3.connect("expenses.db")
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM expenses
            WHERE id = ?
            AND username = ?
        """, (
            expense_id,
            username
        ))

        connection.commit()
        connection.close()

        return True

    except Exception:
        return False


create_database()