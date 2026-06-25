from flask import Flask, Blueprint, render_template, request, redirect, url_for, session 
import sqlite3 
from database import get_connection 
 
 
login_bp = Blueprint('login', __name__ ) 
logout_bp = Blueprint('logout', __name__ ) 
 
@login_bp.route('/', methods=['GET', 'POST']) 
def login():
    if 'login' in session: 
        return redirect(url_for('dashboard.dashboard')) 
    if request.method == 'POST': 
        username = request.form['username'] 
        password = request.form['password'] 
        
        conn = get_connection() 
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor() 
 
 
        user = cursor.execute("SELECT * FROM login WHERE username=? AND password = ?", (username, password)).fetchone()

        conn.close() 
# login validation 
        if user: 
            session['login'] = username 
            return redirect(url_for('dashboard.dashboard'))
        else: 
            return render_template("login.html", error="Invalid Username/Password")
    return render_template("login.html") 
    
# Logout Route 
@login_bp.route('/logout') 
def logout(): 
    session.clear() 
    return redirect(url_for('login.login')) 
