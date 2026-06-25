from flask import Flask
from login import login_bp
from dashboard import dashboard_bp
from menu import menu_bp
from billing import billing_bp
from expense import expense_bp
from sales import sales_bp
from database import creating_db

app = Flask(__name__)
app.secret_key = "secreteEggzoticKey29"

app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(billing_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(sales_bp)

creating_db()

if __name__ == "__main__":
    app.run(debug=True)