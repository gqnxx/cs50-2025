# CS50 pset9: Finance - Stock Trading Web Application

import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import requests

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    # For CS50 environment, set a default or warning
    os.environ["API_KEY"] = "pk_test_key"
    print("Warning: Using default API_KEY. Set API_KEY environment variable for live trading.")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    
    # Get user's stocks
    stocks = db.execute("""
        SELECT symbol, SUM(shares) as total_shares 
        FROM transactions 
        WHERE user_id = ? 
        GROUP BY symbol 
        HAVING total_shares > 0
    """, user_id)
    
    # Get current prices and calculate values
    total_value = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        if quote:
            stock["name"] = quote["name"]
            stock["price"] = quote["price"]
            stock["value"] = stock["total_shares"] * quote["price"]
            total_value += stock["value"]
        else:
            stock["name"] = "Unknown"
            stock["price"] = 0
            stock["value"] = 0
    
    # Get user's cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    total_value += cash
    
    return render_template("index.html", stocks=stocks, cash=cash, total=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        
        # Validate input
        if not symbol:
            return apology("must provide symbol", 400)
        
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive number of shares", 400)
        
        shares = int(shares)
        
        # Look up stock
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)
        
        # Calculate cost
        cost = shares * quote["price"]
        
        # Check if user has enough cash
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        
        if cash < cost:
            return apology("can't afford", 400)
        
        # Execute purchase
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price, timestamp) 
            VALUES (?, ?, ?, ?, ?)
        """, user_id, symbol, shares, quote["price"], datetime.datetime.now())
        
        # Update user's cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, user_id)
        
        flash(f"Bought {shares} shares of {symbol} for {usd(cost)}!")
        return redirect("/")
    
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    
    transactions = db.execute("""
        SELECT symbol, shares, price, timestamp 
        FROM transactions 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
    """, user_id)
    
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    
    # Forget any user_id
    session.clear()
    
    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        
        if not symbol:
            return apology("must provide symbol", 400)
        
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)
        
        return render_template("quoted.html", quote=quote)
    
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # Validate input
        if not username:
            return apology("must provide username", 400)
        
        if not password:
            return apology("must provide password", 400)
        
        if not confirmation:
            return apology("must confirm password", 400)
        
        if password != confirmation:
            return apology("passwords don't match", 400)
        
        # Check if username already exists
        existing = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing:
            return apology("username already exists", 400)
        
        # Hash password and insert user
        hash_pw = generate_password_hash(password)
        user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)
        
        # Log user in
        session["user_id"] = user_id
        
        flash("Registered successfully!")
        return redirect("/")
    
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        
        # Validate input
        if not symbol:
            return apology("must select stock", 400)
        
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive number of shares", 400)
        
        shares = int(shares)
        
        # Check if user owns enough shares
        owned = db.execute("""
            SELECT SUM(shares) as total_shares 
            FROM transactions 
            WHERE user_id = ? AND symbol = ?
        """, user_id, symbol)[0]["total_shares"]
        
        if not owned or owned < shares:
            return apology("not enough shares", 400)
        
        # Look up current price
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)
        
        # Calculate sale value
        sale_value = shares * quote["price"]
        
        # Execute sale
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price, timestamp) 
            VALUES (?, ?, ?, ?, ?)
        """, user_id, symbol, -shares, quote["price"], datetime.datetime.now())
        
        # Update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale_value, user_id)
        
        flash(f"Sold {shares} shares of {symbol} for {usd(sale_value)}!")
        return redirect("/")
    
    else:
        # Get user's stocks for dropdown
        stocks = db.execute("""
            SELECT symbol 
            FROM transactions 
            WHERE user_id = ? 
            GROUP BY symbol 
            HAVING SUM(shares) > 0
        """, user_id)
        
        return render_template("sell.html", stocks=stocks)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to account"""
    if request.method == "POST":
        amount = request.form.get("amount")
        
        # Validate input
        try:
            amount = float(amount)
            if amount <= 0:
                return apology("must provide positive amount", 400)
        except ValueError:
            return apology("must provide valid amount", 400)
        
        # Add cash to user's account
        user_id = session["user_id"]
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, user_id)
        
        flash(f"Added {usd(amount)} to your account!")
        return redirect("/")
    
    else:
        return render_template("add_cash.html")


if __name__ == "__main__":
    app.run(debug=True)
