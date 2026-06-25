from flask import Flask, redirect, render_template, Blueprint,request,url_for
from database import *

expense_bp = Blueprint('expense', __name__)

@expense_bp.route("/expense", methods=["GET", "POST"])
def expense():

    if request.method == "POST":

        item_name = request.form["item_name"]

        amount_input = request.form["amount"].strip()
        try:
            amount = float(amount_input)
        except ValueError:
            return "Invalid amount entered"

        expense_date = request.form["expense_date"]

        add_expense( item_name, amount, expense_date)

        return redirect(url_for("expense.expense"))

    filter_value = request.args.get("filter","all")
    expenses = filter_expenses(filter_value)
    today_expense = get_today_expense()
    month_expense = get_month_expense()
    year_expense = get_year_expense()
    total_expense = 0
    for expense in expenses:
        total_expense += float(expense["amount"])

    return render_template("expense.html", expenses=expenses, total_expense=total_expense,
                           today_expense=today_expense,month_expense=month_expense,year_expense=year_expense)

@expense_bp.route("/delete_expense/<int:expense_id>")
def delete_expense_route(expense_id):
    delete_expense(expense_id)
    return redirect(url_for("expense.expense"))
