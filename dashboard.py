from flask import Flask, Blueprint, render_template, redirect, session,url_for
import sqlite3
from database import *

dashboard_bp = Blueprint('dashboard',__name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'login' not in session:
        return redirect(url_for('login.login'))
    
    recent_orders = get_recent_orders()
    top_items = get_top_selling_items()
    sales = get_total_sales()
    orders_count = get_total_orders()
    profit = get_profit()
    expense = get_total_expense()
    
    return render_template("dashboard.html", recent_orders=recent_orders, top_items=top_items, sales=sales,
                           orders_count=orders_count, profit=profit, expense=expense)
   
