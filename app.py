"""Freelancer Expense Tracker — backend.

A single-owner Flask app that lets freelancers record business expenses,
categorize them, and see where money is going. Built to solve a real
customer problem (tax-time expense scrambling) with clear business value:
never miss a deductible, always know your true net income.

Stack: Flask + SQLite + vanilla JavaScript. One person can own this end to end.
"""

import os
import sqlite3
from datetime import date, datetime
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(os.path.dirname(__file__), "expenses.db")
app.config["JSON_SORT_KEYS"] = False


def get_db():
    """Open a per-request SQLite connection."""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    """Create the expenses table if it doesn't exist."""
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                expense_date TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        db.commit()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/expenses", methods=["GET"])
def list_expenses():
    """Return all expenses, newest first, plus category totals."""
    db = get_db()
    rows = db.execute(
        """
        SELECT id, amount, category, description, expense_date, created_at
        FROM expenses
        ORDER BY expense_date DESC, id DESC
        """
    ).fetchall()

    expenses = [
        {
            "id": r["id"],
            "amount": r["amount"],
            "category": r["category"],
            "description": r["description"],
            "expense_date": r["expense_date"],
            "created_at": r["created_at"],
        }
        for r in rows
    ]

    # Category breakdown for the summary panel.
    category_rows = db.execute(
        """
        SELECT category, COUNT(*) AS count, SUM(amount) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
        """
    ).fetchall()
    categories = [
        {"category": r["category"], "count": r["count"], "total": r["total"]}
        for r in category_rows
    ]

    grand_total = sum(e["amount"] for e in expenses)

    return jsonify(
        {
            "expenses": expenses,
            "categories": categories,
            "grand_total": grand_total,
            "count": len(expenses),
        }
    )


@app.route("/api/expenses", methods=["POST"])
def add_expense():
    """Create a new expense. Required fields: amount, category, expense_date."""
    data = request.get_json(silent=True) or {}

    amount = data.get("amount")
    category = data.get("category", "").strip()
    description = data.get("description", "").strip()
    expense_date = data.get("expense_date", "").strip()

    # --- validation -------------------------------------------------------
    errors = []
    if amount is None or amount == "":
        errors.append("amount is required")
    else:
        try:
            amount = float(amount)
            if amount <= 0:
                errors.append("amount must be greater than 0")
        except (TypeError, ValueError):
            errors.append("amount must be a number")

    if not category:
        errors.append("category is required")

    if not expense_date:
        expense_date = date.today().isoformat()
    else:
        try:
            datetime.strptime(expense_date, "%Y-%m-%d")
        except ValueError:
            errors.append("expense_date must be YYYY-MM-DD")

    if errors:
        return jsonify({"error": "validation failed", "details": errors}), 400

    # --- persist ----------------------------------------------------------
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO expenses (amount, category, description, expense_date, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            amount,
            category,
            description,
            expense_date,
            datetime.utcnow().isoformat(),
        ),
    )
    db.commit()

    new_id = cur.lastrowid
    row = db.execute(
        "SELECT id, amount, category, description, expense_date, created_at "
        "FROM expenses WHERE id = ?",
        (new_id,),
    ).fetchone()

    return (
        jsonify(
            {
                "id": row["id"],
                "amount": row["amount"],
                "category": row["category"],
                "description": row["description"],
                "expense_date": row["expense_date"],
                "created_at": row["created_at"],
            }
        ),
        201,
    )


@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    """Delete an expense by id."""
    db = get_db()
    cur = db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "not found"}), 404
    return jsonify({"deleted": expense_id})


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
