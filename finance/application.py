import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":

        # Retrieve user's data
        user = db.execute("SELECT cash, username FROM users WHERE id = :id", id=session["user_id"])

        # Group stocks and count shares
        stocks = db.execute(
            "SELECT symbol, price, name, sum(shares) FROM portfolio WHERE id = :id GROUP BY symbol", id=session["user_id"])

        totals = {}
        value = 0

        stocks[:] = [stock for stock in stocks if stock['sum(shares)'] > 0]
        history = db.execute("SELECT symbol FROM portfolio WHERE id = :id", id=session["user_id"])

        for stock in stocks:
            quote = lookup(stock['symbol'])
            symbol = quote['symbol']
            shares = db.execute("SELECT sum(shares) FROM portfolio WHERE id = :id AND symbol = :symbol",
                                id=session["user_id"], symbol=symbol)
            price = usd(quote['price'])
            totals[symbol] = usd(quote['price'] * shares[0]['sum(shares)'])
            value = shares[0]['sum(shares)'] * quote['price'] + value

        # Show 10000 cash if user hasn't purchased any stocks
        if not history:
            total = 10000
        else:
            # Get total
            total = value + user[0]['cash']

        # Render index template
        return render_template("index.html", stocks=stocks, total=usd(total), cash=usd(user[0]['cash']), username=user[0]['username'], totals=totals)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Validate inputs and get stock data
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("invalid symbol", 400)

        shares = request.form.get("shares")
        try:
            shares = int(shares)
        except ValueError:
            return apology("invalid quantity", 400)
        else:
            shares = int(shares)

        if shares < 1:
            return apology("invalid quantity", 400)
            
        # Select user's current funds
        cash = db.execute("SELECT cash FROM users WHERE id = :id",
                          id=session["user_id"])  
        
        price = shares * quote['price']
        difference = cash[0]['cash'] - price

        # Purchase stock if cash is sufficient
        if difference >= 0:
            db.execute("UPDATE users SET cash = :difference WHERE id = :id", difference=difference,
                       id=session["user_id"])
        else:
            return apology("Insufficient funds", 400)

        # Log purchase in portfolio
        db.execute("INSERT INTO portfolio (id, symbol, shares, price, name) VALUES(:id, :symbol, :shares, :price, :name)",
                   id=session["user_id"],
                   symbol=quote['symbol'],
                   name=quote['name'],
                   shares=shares,
                   price=quote['price'])

        # Redirect to the home page
        return redirect("/")

    elif request.method == "GET":
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Attempt to insert into database
    username = request.args.get("username")
    users = db.execute("SELECT username FROM users")
    
    # Loop through current usernames and compare new username
    for user in users:
        if user['username'] == username:
            return jsonify(False)
            
    return jsonify(True)     


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get user's portfolio
    portfolio = db.execute("SELECT * FROM portfolio WHERE id = :id", id=session["user_id"])

    # Get user's username
    username = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])

    # Get readable times
    times = {}

    for transaction in portfolio:
        symbol = transaction['symbol']
        times[symbol] = transaction['time']

    print(times)

    # Render template
    return render_template("history.html", portfolio=portfolio, username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("invalid symbol", 400)
        else:
            return render_template("quoted.html",
                                   price=usd(quote['price']),
                                   name=quote['name'],
                                   symbol=quote['symbol'])
    elif request.method == "GET":
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        
        if len(request.form.get("password")) < 8 or len(request.form.get("password")) > 20:
            return apology("password must be 8 to 20 characters long", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure passwords match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords did not match", 400)
            
        # Hash password
        hash = generate_password_hash(request.form.get("password"))

        # Check username availability and add to database
        available = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                               username=request.form.get("username"),
                               hash=hash)
        if not available:
            return apology("username unavailable", 400)

        # Log user in
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Return to home page
        return redirect("/")

    # User reached route with a GET request
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        # Get data from form
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Validate form data
        assets = db.execute("SELECT sum(shares) FROM portfolio WHERE id = :id AND symbol = :symbol GROUP BY symbol",
                            id=session["user_id"], symbol=symbol)
        if assets[0]['sum(shares)'] < shares:
            return apology("Not enough shares to sell", 400)

        # lookup share information
        quote = lookup(symbol)

        # Log sale as a negative quantity
        sold = db.execute("INSERT INTO portfolio (id, symbol, shares, price, name) VALUES(:id, :symbol, :shares, :price, :name)",
                          id=session["user_id"], symbol=symbol, name=quote['name'], shares=-shares, price=quote['price'])
                          
        value = quote['price'] * shares

        # Add value to users cash
        updated = db.execute("UPDATE users SET cash = (cash + :value) WHERE id = :id", value=value, id=session["user_id"])

        # Return to home page
        return redirect("/")

    else:
        # Get symbols from users portfolio
        symbols = db.execute("SELECT symbol FROM portfolio WHERE id = :id GROUP BY symbol", id=session["user_id"])

        # Render sell template
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
