from datetime import datetime
from zoneinfo import ZoneInfo
import sqlite3
def get_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def creating_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS login (
    admin_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL)""")

# Insert default admin
    cursor.execute("INSERT OR IGNORE INTO login (username, password) VALUES('EGGZOTIC', 'sourav@29')")

#--------- table data --------

    # -------------MY ACTUAL ORDERS TABLE----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu_order (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subtotal REAL,
        tax REAL,
        grand_total REAL,
        created_at TEXT
    )
    """)

    # order_items table for recent ordered items......
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        item_name TEXT,
        category TEXT,
        quantity INTEGER,
        price REAL,
        total REAL,
        FOREIGN KEY(order_id) REFERENCES menu_order(id)
    )
    """)

    # Expenses Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            amount REAL NOT NULL,
            expense_date TEXT NOT NULL
        )
    """)



    # Menu Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        UNIQUE(name, category)
    )
    """)

    conn.commit()
    conn.close()


#------ Fetching the data  recent orders-------

def get_recent_orders():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT

        order_items.id,
        order_items.item_name,
        order_items.category,
        order_items.quantity,
        order_items.price,
        menu_order.created_at

    FROM order_items JOIN menu_order ON order_items.order_id = menu_order.id ORDER BY menu_order.id DESC """)

    recent_orders = cursor.fetchall()

    conn.close()
    return recent_orders


def get_total_sales():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(""" SELECT SUM(grand_total) FROM menu_order """)
    result = cursor.fetchone()
    conn.close()

    if result[0] is None:
        return 0
    return round(result[0],2)


def get_all_expenses():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM expenses ORDER BY id ASC""")
    
    expenses = cursor.fetchall()
    conn.close()

    return expenses

def get_total_expense():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" SELECT SUM(amount) FROM expenses """)
    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0
    return round(total, 2)



def get_total_orders():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(""" SELECT COUNT(*) FROM menu_order """)

    result = cursor.fetchone()
    conn.close()

    return result[0]


def get_profit():
    return round(get_total_sales() - get_total_expense(), 2)

# ---------Top selling items
def get_top_selling_items():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(""" SELECT item_name, SUM(quantity) as total_sold FROM order_items GROUP BY item_name ORDER BY total_sold DESC LIMIT 5 """)

    top_items = cursor.fetchall()
    conn.close()
    return top_items

#---------------------------------------Add menu items--------------------
def add_menu_item(name, category, price):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""INSERT INTO menu (name, category, price) VALUES (?, ?, ?)""", (name, category, price))
        conn.commit()
    except:
        return "Item already exists!"
    finally:
        conn.close()

#------------Getting all items---------------------
def get_all_menu_items():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM menu ORDER BY id DESC")
    items = cursor.fetchall()

    conn.close()
    return items

#---------------------- Deleting item-----------------------------
def delete_menu_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM menu WHERE id = ?", (item_id,))

    conn.commit()
    conn.close()

def get_menu_items(search="", category=""):

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM menu WHERE 1=1"
    values = []

    # ----Search
    if search:
        query += " AND name LIKE ?"
        values.append(f"%{search}%")
    
        
    # ---Category Filter
    if category and category != "All":
        query += " AND category = ?"
        values.append(category)

    query += " ORDER BY id DESC"
    cursor.execute(query, values)
    items = cursor.fetchall()
    conn.close()

    return items

#------------ Billing modul's order tables -----------

def save_order_db(cart, subtotal, tax, grand_total):

    conn = get_connection()
    cursor = conn.cursor()

    # -------- CURRENT INDIAN TIME --------

    current_time = datetime.now(ZoneInfo("Asia/Kolkata"))

    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # -------- INSERT INTO menu_order --------

    cursor.execute("""
        INSERT INTO menu_order (
            subtotal,
            tax,
            grand_total,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (subtotal, tax, grand_total, formatted_time))

    # -------- GET ORDER ID --------

    order_id = cursor.lastrowid

    # -------- INSERT ORDER ITEMS --------

    for item in cart:

        item_name = item["name"]
        category = item["category"]
        quantity = item["quantity"]
        price = item["price"]
        total = price * quantity

        cursor.execute("""
            INSERT INTO order_items (
                order_id,
                item_name,
                category,
                quantity,
                price,
                total
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            order_id,
            item_name,
            category,
            quantity,
            price,
            total
        ))

    conn.commit()
    conn.close()

#------- adding the expenses------------------
def add_expense(item_name, amount, expense_date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO expenses(item_name, amount, expense_date) VALUES (?, ?, ?) """, (item_name, amount, expense_date))

    conn.commit()
    conn.close()

#----------deleting the expense module-------
def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM expenses WHERE id = ?""", (expense_id,))

    conn.commit()
    conn.close()

#------ Expense Cards------------------
def get_today_expense():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" SELECT SUM(amount) FROM expenses WHERE expense_date = ? """, (today,))

    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0
    return round(total, 2)

def get_month_expense():
    current_month = datetime.now().strftime("%Y-%m")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" SELECT SUM(amount) FROM expenses WHERE expense_date LIKE ? """, (f"{current_month}%",))

    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0
    return round(total, 2)

def get_year_expense():
    current_year = datetime.now().strftime("%Y")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" SELECT SUM(amount) FROM expenses WHERE expense_date LIKE ? """, (f"{current_year}%",))

    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0
    return round(total, 2)

#---- date filter of expense module-----
def filter_expenses(filter_value):
    conn = get_connection()
    cursor = conn.cursor()

    # ----------TODAY
    if filter_value == "today":
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(""" SELECT * FROM expenses WHERE expense_date = ? ORDER BY id DESC """, (today,))

    # ------------------MONTH
    elif filter_value == "month":
        month = datetime.now().strftime("%Y-%m")
        cursor.execute(""" SELECT * FROM expenses WHERE expense_date LIKE ? ORDER BY id DESC """, (f"{month}%",))

    # -----------YEAR
    elif filter_value == "year":
        year = datetime.now().strftime("%Y")
        cursor.execute(""" SELECT * FROM expenses WHERE expense_date LIKE ? ORDER BY id DESC """, (f"{year}%",))

    # ----------------ALL
    else:
        cursor.execute(""" SELECT * FROM expenses ORDER BY id DESC """)
    expenses = cursor.fetchall()
    conn.close()
    return expenses

#--------------------------------------------------------------- SALES MODULE----------
def get_daily_sales():
    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(""" SELECT SUM(grand_total) FROM menu_order WHERE DATE(created_at) = ? """, (today,))
    result = cursor.fetchone()[0]
    conn.close()

    return round(result, 2) if result else 0

def get_monthly_sales():
    conn = get_connection()
    cursor = conn.cursor()

    current_month = datetime.now().strftime("%Y-%m")
    cursor.execute(""" SELECT SUM(grand_total) FROM menu_order WHERE strftime('%Y-%m', created_at) = ? """, (current_month,))

    result = cursor.fetchone()[0]
    conn.close()
    return round(result, 2) if result else 0

def get_yearly_sales():
    conn = get_connection()
    cursor = conn.cursor()

    current_year = datetime.now().strftime("%Y")
    cursor.execute(""" SELECT SUM(grand_total) FROM menu_order WHERE strftime('%Y', created_at) = ?
    """, (current_year,))

    result = cursor.fetchone()[0]
    conn.close()
    return round(result, 2) if result else 0

#-----Sales Chart----------------
def get_last_7_days_sales():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(""" SELECT DATE(created_at) as sale_date, SUM(grand_total) as total_sales FROM menu_order
        GROUP BY DATE(created_at) ORDER BY DATE(created_at) DESC LIMIT 7 """)

    results = cursor.fetchall()
    conn.close()
    results.reverse()
    return results

print("Data Loaded sucessfully!")