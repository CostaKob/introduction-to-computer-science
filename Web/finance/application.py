import os
import datetime

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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
    users_cash = user[0]["cash"]
    data = db.execute("SELECT * FROM stocks WHERE user_id = :user_id", user_id=session["user_id"])
    total_users_stocks = 0

    for row in data:
        total_users_stocks += row["price"] * row["shares"]

    return render_template("index.html", data=data, users_cash=users_cash, total=float(total_users_stocks))


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():

    rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])

    if request.method == "POST":

        currentPassword = request.form.get("currentPassword")
        newPassword = request.form.get("newPassword")
        confirmation = request.form.get("confirmation")
        isCorrect = check_password_hash(rows[0]["hash"], request.form.get("currentPassword"))

        # check if old password is correct
        if not isCorrect or not currentPassword:
            return apology("Old password is not correct", 403)
        elif not newPassword or not confirmation:
            return apology("Must provide a new password and a confirmation", 403)
        elif newPassword != confirmation:
            return apology("The new passwor and the confirmation must be the same", 403)
        else:
            db.execute("UPDATE users SET hash = :hash WHERE id=:id", hash=generate_password_hash(newPassword), id=session["user_id"])
            flash('You were successfully changed your password!')
            return redirect("/")

    return render_template("change.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")


        if not symbol:
            return apology("Must provide a symbol as a string", 403)
        elif not shares or int(shares) <= 0:
            return apology("Share have to be a positive number", 403)

        if not lookup(symbol):
            return apology("The symbol is not correct", 403)

        data = lookup(symbol)
        name = data["name"]
        price = data["price"]
        user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
        users_cash = user[0]["cash"]

        if float(users_cash) < (price * float(shares)):
            return apology("You don't have enough money", 403)
        else:
            # check if stock is exist
            stock_row = db.execute("SELECT * FROM stocks WHERE symbol = :symbol AND user_id=:user_id", symbol = symbol, user_id=session["user_id"])
            # if exist update shares
            if len(stock_row) != 0:
                db.execute("UPDATE stocks SET shares = shares+:shares WHERE symbol=:symbol AND user_id=:user_id", shares=shares, symbol = symbol, user_id=session["user_id"])
                # update users cash
                db.execute("UPDATE users SET cash = cash-:total_price WHERE id=:id", total_price=price*float(shares), id=session["user_id"])
                transaction_date = datetime.datetime.now()
            # if doesn't create new row
            else:
                db.execute("INSERT INTO stocks(symbol, company, shares, price, user_id) VALUES (:symbol, :company, :shares, :price, :user_id)",
                    symbol=symbol, company=name, shares=shares, price=price, user_id=session["user_id"])
                # update users cash
                db.execute("UPDATE users SET cash = cash-:total_price WHERE id=:id", total_price=price*float(shares), id=session["user_id"])

                transaction_date = datetime.datetime.now()

            db.execute("INSERT INTO transactions(symbol, shares, price, transacted, user_id) VALUES (:symbol, :shares, :price, :transacted, :user_id)",
                    symbol=symbol, shares=shares, price=price, transacted=transaction_date, user_id=session["user_id"])
            transaction_date = None
        flash('Bought!')
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    data = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])

    return render_template("history.html", data=data)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    if request.method == "POST":
        if not lookup(request.form.get("symbol")):
            return apology("The symbol is not correct", 403)

        data = lookup(request.form.get("symbol"))
        name = data["name"]
        price = data["price"]
        symbol = data["symbol"]

        print(name, price, symbol)
        return render_template("quoted.html", name=name, price=price, symbol=symbol)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        rows = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure if username already exist in database
        elif len(rows) != 0:
            return apology("Username with that name already exist", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

        # Ensure confirmation = password
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Type the same password twice!", 403)

        # if everything is OK
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
                username = request.form.get("username"), password = generate_password_hash(request.form.get("password")))

            registeredUser_row = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))

            # Remember which user has logged in
            session["user_id"] = registeredUser_row[0]["id"]

            # Redirect user to home page
            flash('Registered!')
            return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    users_stocks = db.execute("SELECT * FROM stocks WHERE user_id = :user_id", user_id=session["user_id"])

    """Sell shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Must provide a symbol as a string", 403)
        elif not shares or int(shares) <= 0:
            return apology("Share have to be a positive number", 403)

        if not lookup(symbol):
            return apology("The symbol is not correct", 403)

        data = lookup(symbol)
        price = data["price"]

        # check that you have enough shares to sell
        checker_before = db.execute("SELECT * FROM stocks WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=symbol)
        current_shares = checker_before[0]["shares"]

        if current_shares < int(shares):
            return apology(f"You have only {current_shares} shares to sell", 403)

        #if everything's ok update shares
        db.execute("UPDATE stocks SET shares = shares-:shares WHERE symbol=:symbol AND user_id=:user_id", shares=shares, symbol = symbol, user_id=session["user_id"])
        # update users cash
        db.execute("UPDATE users SET cash = cash+:total_price WHERE id=:id", total_price=price*float(shares), id=session["user_id"])
        transaction_date = datetime.datetime.now()

        # record transaction
        db.execute("INSERT INTO transactions(symbol, shares, price, transacted, user_id) VALUES (:symbol, :shares, :price, :transacted, :user_id)",
        symbol=symbol, shares=int(shares)*(-1), price=price, transacted=transaction_date, user_id=session["user_id"])

        # clear date
        transaction_date = None

        # check and if shares = 0 delete row
        checker_after = db.execute("SELECT * FROM stocks WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=symbol)
        current_shares = checker_after[0]["shares"]

        if current_shares == 0:
            db.execute("DELETE FROM stocks WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=symbol)
        flash('Sold!')
        return redirect("/")

    return render_template("sell.html", data=users_stocks)





def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

