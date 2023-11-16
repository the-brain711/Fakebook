from datetime import datetime
from flask import current_app as app
from flask import Blueprint, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    # Displays error message on website
    msg = ""

    # When user clicks on the login button,
    # check to make sure it's a POST request.
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Retrieve hashed password
        hashed_password = password + app.secret_key
        hashed_password = hashlib.sha1(hashed_password.encode())
        password = hashed_password.hexdigest()

        # Check if user exists in database
        db = app.config['DATABASE']
        cursor: MySQLdb.cursors.Cursor = db.connection.cursor(
            MySQLdb.cursors.DictCursor
        )
        cursor.execute(
            "SELECT * FROM users_tb WHERE username = %s AND password = %s",
            (
                username,
                password,
            ),
        )
        user = cursor.fetchone()

        # Create session data for user if user exists
        if user:
            session["loggedin"] = True
            session["id"] = user["id"]

            return redirect(url_for("views.home"))
        else:
            msg = "Invalid username or password. Please try again."

    return render_template("login.html", msg=msg)


@auth.route("/logout")
def logout():
    # Remove session data counts as logging a user out
    session.pop("loggedin", None)
    session.pop("id", None)

    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # Displays error message on website
    msg = ""

    # When user clicks on the signup button,
    # check to make sure it's a POST request.
    if (
        request.method == "POST"
        and "firstname" in request.form
        and "lastname" in request.form
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
    ):
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        # Check if user exists in database
        db = app.config['DATABASE']
        cursor: MySQLdb.cursors.Cursor = db.connection.cursor(
            MySQLdb.cursors.DictCursor
        )
        cursor.execute("SELECT * FROM users_tb WHERE username = %s", (username,))
        user = cursor.fetchone()

        # Show error and validation checks if user exists
        if user:
            msg = "Username is already taken. Please choose a different one."
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid email address."
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Username must contain only characters and numbers."
        elif not username or not password or not email:
            msg = "Please fill out the form completely."
        else:
            # Hash the password
            hashed_password = password + app.secret_key
            hashed_password = hashlib.sha1(hashed_password.encode())
            password = hashed_password.hexdigest()

            # Create new account and store in database
            cursor.execute(
                "INSERT INTO users_tb (first_name, last_name, username, password, email) VALUES(%s, %s, %s, %s, %s)",
                (
                    firstname,
                    lastname,
                    username,
                    password,
                    email,
                ),
            )
            db.connection.commit()
            db.connection.close()

            # msg = "You have successfully signed up for Fakebook!"
            return redirect(url_for("auth.login"))

    # If the signup page has an empty box
    elif request.method == "POST":
        msg = "Please fill out the form completely"

    return render_template("signup.html", msg=msg)
