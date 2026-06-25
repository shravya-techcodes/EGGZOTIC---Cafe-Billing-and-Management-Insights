from flask import Blueprint, render_template, redirect, url_for,jsonify,request
from database import *

sales_bp = Blueprint('sales', __name__)

@sales_bp.route("/sales")
def sales():

    daily_sales = get_daily_sales()
    monthly_sales = get_monthly_sales()
    yearly_sales = get_yearly_sales()

    sales_data = get_last_7_days_sales()

    labels = []
    totals = []

    #for row in sales_data:
    #    labels.append(row["sale_date"])
    #    totals.append(row["total_sales"])

    for row in sales_data:
        labels.append(row[0])
        totals.append(row[1])

    return render_template( "sales.html", daily_sales=daily_sales, monthly_sales=monthly_sales, yearly_sales=yearly_sales,
                            chart_labels=labels,chart_totals=totals)