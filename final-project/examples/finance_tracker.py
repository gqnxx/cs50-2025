# Example 1: Personal Finance Tracker (Flask Web App)

"""
Personal Finance Tracker - A web application to manage income, expenses, and budgets.

Features:
- User registration and authentication
- Income and expense tracking
- Budget categories and limits
- Monthly/yearly financial reports
- Data visualization with charts

Tech Stack:
- Backend: Python Flask
- Database: SQLite
- Frontend: HTML, CSS, JavaScript, Chart.js
- Authentication: Flask-Login
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL, -- 'income' or 'expense'
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Budgets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Home page with dashboard."""
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Validate input
        if not username or not email or not password:
            flash('All fields are required.')
            return render_template('register.html')
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Save to database
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[3], password):
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    """Add a new income or expense transaction."""
    if request.method == 'POST':
        transaction_type = request.form['type']
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form.get('description', '')
        date = request.form['date']
        
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (user_id, type, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (current_user.id, transaction_type, amount, category, description, date))
        conn.commit()
        conn.close()
        
        flash(f'{transaction_type.title()} added successfully!')
        return redirect(url_for('transactions'))
    
    return render_template('add_transaction.html')

@app.route('/transactions')
@login_required
def transactions():
    """View all transactions."""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions 
        WHERE user_id = ? 
        ORDER BY date DESC
    ''', (current_user.id,))
    transactions = cursor.fetchall()
    conn.close()
    
    return render_template('transactions.html', transactions=transactions)

@app.route('/api/chart_data')
@login_required
def chart_data():
    """API endpoint for chart data."""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Get monthly expense data for the last 6 months
    six_months_ago = datetime.now() - timedelta(days=180)
    cursor.execute('''
        SELECT strftime('%Y-%m', date) as month, 
               SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
               SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expense
        FROM transactions 
        WHERE user_id = ? AND date >= ?
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month
    ''', (current_user.id, six_months_ago.strftime('%Y-%m-%d')))
    
    data = cursor.fetchall()
    conn.close()
    
    months = [row[0] for row in data]
    income = [row[1] for row in data]
    expenses = [row[2] for row in data]
    
    return jsonify({
        'months': months,
        'income': income,
        'expenses': expenses
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

# Usage:
# 1. pip install flask flask-login
# 2. python finance_tracker.py
# 3. Visit http://localhost:5000
