import json
import os
import sys
import webbrowser
import threading
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, jsonify


def get_base_dir():
    """Restituisce la cartella base, funziona sia normalmente che come .exe"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)


BASE_DIR = get_base_dir()

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)

DATA_FILE = os.path.join(BASE_DIR, "data", "expenses.json")


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.route("/")
def index():
    data = load_data()
    expenses = data["expenses"]
    categories = data["categories"]

    totals = {}
    for exp in expenses:
        cat = exp["category"]
        totals[cat] = totals.get(cat, 0) + exp["amount"]

    chart_labels = list(totals.keys())
    chart_values = list(totals.values())
    total = sum(chart_values)

    return render_template(
        "index.html",
        expenses=expenses,
        categories=categories,
        chart_labels=chart_labels,
        chart_values=chart_values,
        totals=totals,
        total=total,
    )


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    data = load_data()

    if request.method == "POST":
        new_category = request.form.get("new_category", "").strip()
        category = new_category if new_category else request.form["category"]

        if new_category and new_category not in data["categories"]:
            data["categories"].append(new_category)

        max_id = max((e["id"] for e in data["expenses"]), default=0)
        expense = {
            "id": max_id + 1,
            "description": request.form["description"],
            "amount": round(float(request.form["amount"]), 2),
            "category": category,
            "date": request.form["date"],
        }
        data["expenses"].append(expense)
        save_data(data)
        return redirect(url_for("index"))

    return render_template(
        "add_expense.html",
        categories=data["categories"],
        today=date.today().isoformat(),
    )


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    data = load_data()
    data["expenses"] = [e for e in data["expenses"] if e["id"] != expense_id]
    save_data(data)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Apri il browser automaticamente dopo 1.5 secondi
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    print("\n  Tracker Spese avviato!")
    print("  Apri il browser su: http://127.0.0.1:5000")
    print("  Per chiudere: chiudi questa finestra\n")
    app.run(debug=False)
