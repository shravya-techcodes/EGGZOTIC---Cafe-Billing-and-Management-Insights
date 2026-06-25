from flask import Blueprint, render_template, redirect, url_for,jsonify,request
from database import *

billing_bp = Blueprint('billing', __name__)

@billing_bp.route("/billing")
def billing():

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    items = cursor.fetchall()
    conn.close()

    search = request.args.get("search", "")
    category = request.args.get("category", "")
    items = get_menu_items(search, category)

    message = ""

    if search and len(items) == 0:
        message = "Item Not Found"

    if category and len(items) == 0:
        message = "Item Not Found"

    return render_template("billing.html", items=items, search=search, selected_category=category, message=message)


@billing_bp.route("/save-order", methods=["POST"])
def save_order():

    data = request.get_json()
    cart = data["cart"]

    subtotal = float(data["subtotal"])
    tax = float(data["tax"])
    grand_total = float(data["grandTotal"])


    save_order_db(cart, subtotal, tax, grand_total)

    return jsonify({
        "message": "Order saved successfully"
    })