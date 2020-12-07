import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, check_speed

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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/history")
@login_required
def history():
    data = db.execute("SELECT * FROM history WHERE user_id = :user_id", user_id=session["user_id"])
    return render_template("history.html", data=data)

@app.route("/withspeed", methods=['POST'])
@login_required
def check():
    data = check_speed()
    best_server = data.get_best_server()
    myUpload = data.upload() / 1024 / 1024
    myDownload = data.download() / 1024 / 1024
    server=[]
    data.get_servers(server)
    ping = data.results.ping

    test_date = datetime.datetime.now()
    
    db.execute("INSERT INTO history(user_id, ping, download, upload, country, name, host, date) VALUES (:user_id, :ping, :download, :upload, :country, :name, :host, :date)",
                    user_id=session["user_id"], ping=ping, download=myDownload, upload=myUpload, country=best_server["country"],
                    name=best_server["name"], host=best_server["host"], date=test_date)
    test_date = None

    return jsonify(download=myDownload, upload=myUpload, ping=ping, server=best_server)


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
            return render_template('change.html', error="Old password is not correct")
        elif not newPassword or not confirmation:
            return render_template('change.html', error="Must provide a new password and a confirmation")
        elif newPassword != confirmation:
            return render_template('change.html', error="The new password and the confirmation must be the same")
        else:
            db.execute("UPDATE users SET hash = :hash WHERE id=:id", hash=generate_password_hash(newPassword), id=session["user_id"])
            flash('You were successfully changed your password!')
            return redirect("/")

    return render_template("change.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template('login.html', error="Must provide Username!")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template('login.html', error="Must provide Password!")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template('login.html', error="Invalid username and/or password")

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

@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        rows = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template('register.html', error="Must provide Username")

        # Ensure if username already exist in database
        elif len(rows) != 0:
            return render_template('register.html', error="Username with that name already exist")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template('register.html', error="Must provide password")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return render_template('register.html', error="Must provide password confirmation")

        # Ensure confirmation = password
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template('register.html', error="The password did not match!")

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

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template('index.html', error=e.name)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

