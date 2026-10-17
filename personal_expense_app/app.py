from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "personal_expense_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "expense.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            payment_mode TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS savings_goals (
            goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal_name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_amount REAL NOT NULL DEFAULT 0,
            deadline TEXT,
            monthly_target REAL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    columns = conn.execute(
        "PRAGMA table_info(savings_goals)"
    ).fetchall()

    column_names = [column["name"] for column in columns]

    if "deadline" not in column_names:
        conn.execute(
            "ALTER TABLE savings_goals ADD COLUMN deadline TEXT"
        )

    if "monthly_target" not in column_names:
        conn.execute(
            "ALTER TABLE savings_goals ADD COLUMN monthly_target REAL DEFAULT 0"
        )

    conn.commit()
    conn.close()


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template(
                "register.html",
                error="All fields are required"
            )

        hashed_password = generate_password_hash(password)

        conn = get_db()

        try:

            conn.execute(
                """
                INSERT INTO users
                (name, email, password)
                VALUES (?, ?, ?)
                """,
                (name, email, hashed_password)
            )

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            return render_template(
                "register.html",
                error="Email already registered"
            )

        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        conn = get_db()

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["user_id"]
            session["name"] = user["name"]

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid email or password"
        )

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db()

    income = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND type = 'Income'
        """,
        (user_id,)
    ).fetchone()[0]

    expense = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND type = 'Expense'
        """,
        (user_id,)
    ).fetchone()[0]

    recent_transactions = conn.execute(
        """
        SELECT *
        FROM transactions
        WHERE user_id = ?
        ORDER BY transaction_id DESC
        LIMIT 5
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    balance = income - expense

    return render_template(
        "dashboard.html",
        income=income,
        expense=expense,
        balance=balance,
        transactions=recent_transactions
    )


@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        date = request.form.get("date", "")
        amount = request.form.get("amount", "")
        category = request.form.get("category", "")
        payment_mode = request.form.get("payment_mode", "")
        description = request.form.get("description", "")

        try:

            amount = float(amount)

            if amount <= 0:
                return render_template(
                    "add_expense.html",
                    error="Amount must be greater than zero"
                )

        except ValueError:

            return render_template(
                "add_expense.html",
                error="Enter a valid amount"
            )

        conn = get_db()

        conn.execute(
            """
            INSERT INTO transactions
            (
                user_id,
                date,
                type,
                amount,
                category,
                payment_mode,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                date,
                "Expense",
                amount,
                category,
                payment_mode,
                description
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("add_expense.html")


@app.route("/add-income", methods=["GET", "POST"])
def add_income():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        date = request.form.get("date", "")
        amount = request.form.get("amount", "")
        category = request.form.get("category", "")
        payment_mode = request.form.get("payment_mode", "")
        description = request.form.get("description", "")

        try:

            amount = float(amount)

            if amount <= 0:
                return render_template(
                    "add_income.html",
                    error="Amount must be greater than zero"
                )

        except ValueError:

            return render_template(
                "add_income.html",
                error="Enter a valid amount"
            )

        conn = get_db()

        conn.execute(
            """
            INSERT INTO transactions
            (
                user_id,
                date,
                type,
                amount,
                category,
                payment_mode,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                date,
                "Income",
                amount,
                category,
                payment_mode,
                description
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("add_income.html")


@app.route("/transactions")
def transactions():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    data = conn.execute(
        """
        SELECT *
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC, transaction_id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template(
        "transactions.html",
        transactions=data
    )


@app.route("/delete_transaction/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    conn = get_db()
    conn.execute(
        "DELETE FROM transactions WHERE transaction_id = ? AND user_id = ?",
        (transaction_id, user_id)
    )
    conn.commit()
    conn.close()
    return redirect(request.referrer or url_for("transactions"))


@app.route("/budget", methods=["GET", "POST"])
def budget():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    conn = get_db()
    error = None

    if request.method == "POST":

        category = request.form.get("category", "").strip()
        amount = request.form.get("amount", "").strip()
        month = request.form.get("month", "").strip()

        if not month:
            month = datetime.now().strftime("%Y-%m")

        try:
            amount = float(amount)
            if amount <= 0:
                error = "Budget amount must be greater than zero"
            else:
                existing = conn.execute(
                    """
                    SELECT budget_id FROM budgets
                    WHERE user_id = ? AND category = ? AND month = ?
                    """,
                    (user_id, category, month)
                ).fetchone()

                if existing:
                    conn.execute(
                        "UPDATE budgets SET amount = ? WHERE budget_id = ?",
                        (amount, existing["budget_id"])
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO budgets (user_id, category, amount, month)
                        VALUES (?, ?, ?, ?)
                        """,
                        (user_id, category, amount, month)
                    )
                conn.commit()
                conn.close()
                return redirect(url_for("budget"))

        except ValueError:
            error = "Enter a valid budget amount"

    budgets = conn.execute(
        """
        SELECT *
        FROM budgets
        WHERE user_id = ?
        ORDER BY month DESC, budget_id DESC
        """,
        (user_id,)
    ).fetchall()

    budget_data = []
    total_budget = 0.0
    total_spent = 0.0

    for budget_item in budgets:

        spent = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE user_id = ?
            AND type = 'Expense'
            AND category = ?
            AND strftime('%Y-%m', date) = ?
            """,
            (
                user_id,
                budget_item["category"],
                budget_item["month"]
            )
        ).fetchone()[0]

        amt = float(budget_item["amount"])
        sp = float(spent)
        rem = amt - sp
        total_budget += amt
        total_spent += sp

        percentage = 0
        if amt > 0:
            percentage = (sp / amt) * 100

        progress_width = min(max(percentage, 0), 100)

        if percentage < 75:
            status = "safe"
            status_message = "On track"
        elif percentage <= 100:
            status = "warning"
            status_message = "Approaching budget limit"
        else:
            status = "exceeded"
            status_message = "Budget limit exceeded"

        budget_data.append({
            "budget_id": budget_item["budget_id"],
            "category": budget_item["category"],
            "amount": amt,
            "month": budget_item["month"],
            "spent": sp,
            "remaining": rem,
            "percentage": percentage,
            "progress_width": progress_width,
            "status": status,
            "status_message": status_message
        })

    total_remaining = total_budget - total_spent
    conn.close()

    return render_template(
        "budget.html",
        budgets=budget_data,
        total_budget=total_budget,
        total_spent=total_spent,
        total_remaining=total_remaining,
        error=error
    )


@app.route("/delete_budget/<int:budget_id>", methods=["POST"])
def delete_budget(budget_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    conn = get_db()
    conn.execute(
        "DELETE FROM budgets WHERE budget_id = ? AND user_id = ?",
        (budget_id, user_id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("budget"))


@app.route("/savings", methods=["GET", "POST"])
def savings():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db()

    if request.method == "POST":

        goal_name = request.form.get(
            "goal_name",
            ""
        ).strip()

        target_amount = request.form.get(
            "target_amount",
            ""
        ).strip()

        deadline = request.form.get(
            "deadline",
            ""
        ).strip()

        monthly_target = request.form.get(
            "monthly_target",
            ""
        ).strip()

        if not goal_name:
            conn.close()
            return redirect(url_for("savings"))

        try:

            target_amount = float(target_amount)

            monthly_target = (
                float(monthly_target)
                if monthly_target
                else 0
            )

            if target_amount <= 0:
                conn.close()
                return redirect(url_for("savings"))

            if monthly_target < 0:
                monthly_target = 0

        except ValueError:

            conn.close()
            return redirect(url_for("savings"))

        conn.execute(
            """
            INSERT INTO savings_goals
            (
                user_id,
                goal_name,
                target_amount,
                current_amount,
                deadline,
                monthly_target
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                goal_name,
                target_amount,
                0,
                deadline,
                monthly_target
            )
        )

        conn.commit()

    goals = conn.execute(
        """
        SELECT *
        FROM savings_goals
        WHERE user_id = ?
        ORDER BY goal_id DESC
        """,
        (user_id,)
    ).fetchall()

    goal_data = []

    for goal in goals:

        target = float(
            goal["target_amount"] or 0
        )

        current = float(
            goal["current_amount"] or 0
        )

        percentage = 0

        if target > 0:
            percentage = (
                current /
                target
            ) * 100

        percentage = min(
            max(percentage, 0),
            100
        )

        remaining = max(
            target - current,
            0
        )

        if current >= target:

            status = "completed"

            status_text = "Completed"

            status_message = (
                "Congratulations! "
                "You reached your savings goal."
            )

        elif percentage >= 75:

            status = "near"

            status_text = "Almost There"

            status_message = (
                f"You have completed "
                f"{percentage:.1f}% of your goal."
            )

        else:

            status = "active"

            status_text = "In Progress"

            status_message = (
                f"You need ₹{remaining:.2f} "
                f"more to reach your goal."
            )

        monthly_target = float(
            goal["monthly_target"] or 0
        )

        deadline = goal["deadline"]

        days_remaining = None
        deadline_status = ""

        if deadline:

            try:

                deadline_date = datetime.strptime(
                    deadline,
                    "%Y-%m-%d"
                ).date()

                today = datetime.now().date()

                days_remaining = (
                    deadline_date -
                    today
                ).days

                if (
                    days_remaining < 0
                    and current < target
                ):

                    deadline_status = "Overdue"

                elif (
                    days_remaining == 0
                    and current < target
                ):

                    deadline_status = "Due Today"

                elif (
                    days_remaining <= 7
                    and current < target
                ):

                    deadline_status = "Due Soon"

                else:

                    deadline_status = "On Track"

            except ValueError:

                days_remaining = None
                deadline_status = ""

        if (
            monthly_target > 0
            and current < target
        ):

            monthly_status = (
                "Monthly target: "
                f"₹{monthly_target:.2f}"
            )

        else:

            monthly_status = ""

        goal_data.append({
            "goal_id": goal["goal_id"],
            "goal_name": goal["goal_name"],
            "target_amount": target,
            "current_amount": current,
            "remaining": remaining,
            "percentage": percentage,
            "status": status,
            "status_text": status_text,
            "status_message": status_message,
            "deadline": deadline,
            "monthly_target": monthly_target,
            "days_remaining": days_remaining,
            "deadline_status": deadline_status,
            "monthly_status": monthly_status
        })

    total_savings = sum(
        goal["current_amount"]
        for goal in goal_data
    )

    total_target = sum(
        goal["target_amount"]
        for goal in goal_data
    )

    total_remaining = sum(
        goal["remaining"]
        for goal in goal_data
    )

    total_income = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND type = 'Income'
        """,
        (user_id,)
    ).fetchone()[0]

    total_expense = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND type = 'Expense'
        """,
        (user_id,)
    ).fetchone()[0]

    balance = (
        total_income -
        total_expense
    )

    savings_percentage = 0

    if total_target > 0:

        savings_percentage = (
            total_savings /
            total_target
        ) * 100

    savings_percentage = min(
        max(savings_percentage, 0),
        100
    )

    conn.close()

    return render_template(
        "savings.html",
        goals=goal_data,
        total_saved=total_savings,
        total_savings=total_savings,
        total_target=total_target,
        total_remaining=total_remaining,
        savings_percentage=savings_percentage,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance
    )


@app.route(
    "/add_savings_money/<int:goal_id>",
    methods=["POST"]
)
def add_savings_money(goal_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    amount = request.form.get(
        "amount",
        ""
    ).strip()

    try:

        amount = float(amount)

        if amount <= 0:
            return redirect(url_for("savings"))

    except ValueError:

        return redirect(url_for("savings"))

    conn = get_db()

    goal = conn.execute(
        """
        SELECT *
        FROM savings_goals
        WHERE goal_id = ?
        AND user_id = ?
        """,
        (
            goal_id,
            session["user_id"]
        )
    ).fetchone()

    if goal:

        current_amount = float(
            goal["current_amount"] or 0
        )

        target_amount = float(
            goal["target_amount"] or 0
        )

        new_amount = (
            current_amount +
            amount
        )

        new_amount = min(
            new_amount,
            target_amount
        )

        conn.execute(
            """
            UPDATE savings_goals
            SET current_amount = ?
            WHERE goal_id = ?
            AND user_id = ?
            """,
            (
                new_amount,
                goal_id,
                session["user_id"]
            )
        )

        conn.commit()

    conn.close()

    return redirect(url_for("savings"))


@app.route(
    "/withdraw_savings/<int:goal_id>",
    methods=["POST"]
)
def withdraw_savings(goal_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    amount = request.form.get(
        "amount",
        ""
    ).strip()

    try:

        amount = float(amount)

        if amount <= 0:
            return redirect(url_for("savings"))

    except ValueError:

        return redirect(url_for("savings"))

    conn = get_db()

    goal = conn.execute(
        """
        SELECT current_amount
        FROM savings_goals
        WHERE goal_id = ?
        AND user_id = ?
        """,
        (
            goal_id,
            session["user_id"]
        )
    ).fetchone()

    if goal:

        current_amount = float(
            goal["current_amount"] or 0
        )

        if amount <= current_amount:

            new_amount = (
                current_amount -
                amount
            )

            conn.execute(
                """
                UPDATE savings_goals
                SET current_amount = ?
                WHERE goal_id = ?
                AND user_id = ?
                """,
                (
                    new_amount,
                    goal_id,
                    session["user_id"]
                )
            )

            conn.commit()

    conn.close()

    return redirect(url_for("savings"))


@app.route(
    "/edit_savings/<int:goal_id>",
    methods=["POST"]
)
def edit_savings(goal_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    goal_name = request.form.get(
        "goal_name",
        ""
    ).strip()

    target_amount = request.form.get(
        "target_amount",
        ""
    ).strip()

    deadline = request.form.get(
        "deadline",
        ""
    ).strip()

    monthly_target = request.form.get(
        "monthly_target",
        ""
    ).strip()

    if not goal_name:
        return redirect(url_for("savings"))

    try:

        target_amount = float(
            target_amount
        )

        monthly_target = (
            float(monthly_target)
            if monthly_target
            else 0
        )

        if target_amount <= 0:
            return redirect(url_for("savings"))

        if monthly_target < 0:
            monthly_target = 0

    except ValueError:

        return redirect(url_for("savings"))

    conn = get_db()

    goal = conn.execute(
        """
        SELECT current_amount
        FROM savings_goals
        WHERE goal_id = ?
        AND user_id = ?
        """,
        (
            goal_id,
            session["user_id"]
        )
    ).fetchone()

    if goal:

        current_amount = float(
            goal["current_amount"] or 0
        )

        current_amount = min(
            current_amount,
            target_amount
        )

        conn.execute(
            """
            UPDATE savings_goals
            SET
                goal_name = ?,
                target_amount = ?,
                deadline = ?,
                monthly_target = ?,
                current_amount = ?
            WHERE goal_id = ?
            AND user_id = ?
            """,
            (
                goal_name,
                target_amount,
                deadline,
                monthly_target,
                current_amount,
                goal_id,
                session["user_id"]
            )
        )

        conn.commit()

    conn.close()

    return redirect(url_for("savings"))


@app.route(
    "/delete_savings/<int:goal_id>",
    methods=["POST"]
)
def delete_savings(goal_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    conn.execute(
        """
        DELETE FROM savings_goals
        WHERE goal_id = ?
        AND user_id = ?
        """,
        (
            goal_id,
            session["user_id"]
        )
    )

    conn.commit()
    conn.close()

    return redirect(url_for("savings"))


@app.route("/analytics")
def analytics():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db()

    data = conn.execute(
        """
        SELECT
            transaction_id,
            date,
            type,
            amount,
            category,
            payment_mode,
            description
        FROM transactions
        WHERE user_id = ?
        ORDER BY date
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    columns = [
        "transaction_id",
        "date",
        "type",
        "amount",
        "category",
        "payment_mode",
        "description"
    ]

    df = pd.DataFrame(
        data,
        columns=columns
    )

    if df.empty:

        return render_template(
            "analytics.html",
            total_income=0,
            total_expense=0,
            balance=0,
            average_expense=0,
            highest_expense=0,
            total_transactions=0,
            highest_category="No Data",
            category_data=[],
            payment_data=[],
            monthly_data=[],
            chart_category=None,
            chart_monthly=None,
            chart_income_expense=None,
            chart_payment=None
        )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    ).fillna(0)

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["date"]
    )

    income_df = df[
        df["type"] == "Income"
    ]

    expense_df = df[
        df["type"] == "Expense"
    ]

    total_income = float(
        income_df["amount"].sum()
    )

    total_expense = float(
        expense_df["amount"].sum()
    )

    balance = (
        total_income -
        total_expense
    )

    average_expense = (
        float(
            expense_df["amount"].mean()
        )
        if not expense_df.empty
        else 0
    )

    highest_expense = (
        float(
            expense_df["amount"].max()
        )
        if not expense_df.empty
        else 0
    )

    total_transactions = len(df)

    if not expense_df.empty:

        category_expense = (
            expense_df
            .groupby("category")["amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        highest_category = str(
            category_expense.index[0]
        )

        category_data = [
            {
                "category": str(category),
                "amount": float(amount)
            }
            for category, amount
            in category_expense.items()
        ]

    else:

        category_expense = pd.Series(
            dtype=float
        )

        highest_category = "No Expense"

        category_data = []

    if not expense_df.empty:

        payment_expense = (
            expense_df
            .groupby("payment_mode")["amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

    else:

        payment_expense = pd.Series(
            dtype=float
        )

    payment_data = [
        {
            "payment_mode": str(mode),
            "amount": float(amount)
        }
        for mode, amount
        in payment_expense.items()
    ]

    if not expense_df.empty:

        monthly_expense = (
            expense_df
            .assign(
                month=expense_df[
                    "date"
                ].dt.strftime("%Y-%m")
            )
            .groupby("month")["amount"]
            .sum()
        )

    else:

        monthly_expense = pd.Series(
            dtype=float
        )

    monthly_data = [
        {
            "month": str(month),
            "amount": float(amount)
        }
        for month, amount
        in monthly_expense.items()
    ]

    chart_folder = os.path.join(
        BASE_DIR,
        "static",
        "charts"
    )

    os.makedirs(
        chart_folder,
        exist_ok=True
    )

    category_chart = os.path.join(
        chart_folder,
        f"category_{user_id}.png"
    )

    monthly_chart = os.path.join(
        chart_folder,
        f"monthly_{user_id}.png"
    )

    income_expense_chart = os.path.join(
        chart_folder,
        f"income_expense_{user_id}.png"
    )

    payment_chart = os.path.join(
        chart_folder,
        f"payment_{user_id}.png"
    )

    signature_file = os.path.join(
        chart_folder,
        f"analytics_{user_id}.txt"
    )

    latest_id = int(
        df["transaction_id"].max()
    )

    latest_date = str(
        df["date"].max()
    )

    current_signature = (
        f"{total_transactions}_"
        f"{latest_id}_"
        f"{latest_date}_"
        f"{total_income}_"
        f"{total_expense}"
    )

    old_signature = ""

    if os.path.exists(signature_file):

        try:

            with open(
                signature_file,
                "r"
            ) as file:

                old_signature = (
                    file.read().strip()
                )

        except Exception:

            old_signature = ""

    charts_need_update = (
        current_signature !=
        old_signature
    )

    if charts_need_update:

        chart_colors = ["#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6", "#06b6d4", "#f43f5e", "#14b8a6"]

        if not category_expense.empty:

            fig, ax = plt.subplots(figsize=(7, 5), facecolor='white')
            category_expense.plot(
                kind="pie",
                autopct="%1.1f%%",
                colors=chart_colors[:len(category_expense)],
                startangle=140,
                ax=ax,
                wedgeprops=dict(width=0.7, edgecolor='white', linewidth=2)
            )
            ax.set_title("Expense Distribution by Category", fontsize=13, fontweight='bold', pad=15)
            ax.set_ylabel("")
            plt.tight_layout()

            temp_file = category_chart + ".tmp.png"
            plt.savefig(temp_file, format="png", dpi=130, bbox_inches='tight')
            plt.close()
            os.replace(temp_file, category_chart)

        elif os.path.exists(category_chart):
            try:
                os.remove(category_chart)
            except:
                pass

        if not monthly_expense.empty:

            fig, ax = plt.subplots(figsize=(8, 4.8), facecolor='white')
            monthly_expense.plot(
                kind="line",
                marker="o",
                color="#2563eb",
                linewidth=2.5,
                markersize=6,
                ax=ax
            )
            ax.set_title("Monthly Expense Trend", fontsize=13, fontweight='bold', pad=15)
            ax.set_xlabel("Month", fontweight='bold', labelpad=8)
            ax.set_ylabel("Expense (₹)", fontweight='bold', labelpad=8)
            ax.grid(True, linestyle="--", alpha=0.3, color="#94a3b8")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.xticks(rotation=30)
            plt.tight_layout()

            temp_file = monthly_chart + ".tmp.png"
            plt.savefig(temp_file, format="png", dpi=130, bbox_inches='tight')
            plt.close()
            os.replace(temp_file, monthly_chart)

        elif os.path.exists(monthly_chart):
            try:
                os.remove(monthly_chart)
            except:
                pass

        income_expense = pd.Series({
            "Income": total_income,
            "Expense": total_expense
        })

        fig, ax = plt.subplots(figsize=(6.5, 4.8), facecolor='white')
        income_expense.plot(
            kind="bar",
            color=["#10b981", "#ef4444"],
            width=0.45,
            ax=ax
        )
        ax.set_title("Income vs Expense Comparison", fontsize=13, fontweight='bold', pad=15)
        ax.set_ylabel("Amount (₹)", fontweight='bold', labelpad=8)
        ax.grid(axis='y', linestyle="--", alpha=0.3, color="#94a3b8")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xticks(rotation=0, fontweight='bold')
        plt.tight_layout()

        temp_file = income_expense_chart + ".tmp.png"
        plt.savefig(temp_file, format="png", dpi=130, bbox_inches='tight')
        plt.close()
        os.replace(temp_file, income_expense_chart)

        if not payment_expense.empty:

            fig, ax = plt.subplots(figsize=(7, 4.8), facecolor='white')
            payment_expense.plot(
                kind="bar",
                color="#3b82f6",
                width=0.45,
                ax=ax
            )
            ax.set_title("Expense by Payment Mode", fontsize=13, fontweight='bold', pad=15)
            ax.set_xlabel("Payment Mode", fontweight='bold', labelpad=8)
            ax.set_ylabel("Amount (₹)", fontweight='bold', labelpad=8)
            ax.grid(axis='y', linestyle="--", alpha=0.3, color="#94a3b8")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.xticks(rotation=15, fontweight='bold')
            plt.tight_layout()

            temp_file = payment_chart + ".tmp.png"
            plt.savefig(temp_file, format="png", dpi=130, bbox_inches='tight')
            plt.close()
            os.replace(temp_file, payment_chart)

        elif os.path.exists(payment_chart):

            try:
                os.remove(payment_chart)
            except:
                pass

        try:

            with open(
                signature_file,
                "w"
            ) as file:

                file.write(
                    current_signature
                )

        except Exception:
            pass

    return render_template(
        "analytics.html",
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        average_expense=average_expense,
        highest_expense=highest_expense,
        total_transactions=total_transactions,
        highest_category=highest_category,
        category_data=category_data,
        payment_data=payment_data,
        monthly_data=monthly_data,
        chart_category=(
            f"charts/category_{user_id}.png"
            if not category_expense.empty
            and os.path.exists(category_chart)
            else None
        ),
        chart_monthly=(
            f"charts/monthly_{user_id}.png"
            if not monthly_expense.empty
            and os.path.exists(monthly_chart)
            else None
        ),
        chart_income_expense=(
            f"charts/income_expense_{user_id}.png"
            if os.path.exists(
                income_expense_chart
            )
            else None
        ),
        chart_payment=(
            f"charts/payment_{user_id}.png"
            if not payment_expense.empty
            and os.path.exists(payment_chart)
            else None
        )
    )


@app.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db()

    report_transactions = conn.execute(
        """
        SELECT
            date,
            type,
            amount,
            category,
            payment_mode,
            description
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    total_income = sum(
        float(row["amount"])
        for row in report_transactions
        if row["type"] == "Income"
    )

    total_expense = sum(
        float(row["amount"])
        for row in report_transactions
        if row["type"] == "Expense"
    )

    balance = (
        total_income -
        total_expense
    )

    return render_template(
        "reports.html",
        transactions=report_transactions,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance
    )


if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )