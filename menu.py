from flask import Blueprint, render_template, redirect, url_for, request, flash
from database import *

menu_bp = Blueprint('menu', __name__)

@menu_bp.route("/menu")
def menu():
    search = request.args.get("search", "")
    category = request.args.get("category", "")
    msg = request.args.get("msg")

    items = get_menu_items(search, category)

    message = ""

    if search and len(items) == 0:
        message = "Item Not Found"

    if category and len(items) == 0:
        message = "Item Not Found"

    return render_template(
        "menu.html",
        items=items,
        search=search,
        selected_category=category,
        message=msg,
        note=message
    )

@menu_bp.route("/add_item", methods=["POST"])
def add_item():
    name = request.form["name"].strip().title()
    category = request.form["category"]
    price = float(request.form["price"])

    message = add_menu_item(name, category, price)
    return redirect(url_for('menu.menu', msg=message))

@menu_bp.route("/delete_item/<int:id>")
def delete_item(id):
    delete_menu_item(id)
    return redirect("/menu")
