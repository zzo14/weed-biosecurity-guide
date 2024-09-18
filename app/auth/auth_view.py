from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask import Blueprint
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime
import re
from app.utils import getCursor
from app.utils import url_select

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@auth_bp.before_request
def before_request():
    if "loggedin" in session and request.endpoint in ["auth.login", "auth.register"]:
        if session.get("userType") == "Gardener":
            return redirect(url_for("user.user_dashboard"))
        elif session.get("userType") == "Staff":
            return redirect(url_for("admin_staff.staff_dashboard"))
        elif session.get("userType") == "Admin":
            return redirect(url_for("admin_staff.admin_dashboard"))


# Login, Register and Logout
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    connection = getCursor()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        query = (
            "SELECT * FROM userauth WHERE username = %s and status = 'Active' LIMIT 1"
        )
        connection.execute(query, (username,))
        user = connection.fetchone()
        if user and check_password_hash(user[2], password):
            session.permanent = True
            session["loggedin"] = True
            session["id"] = user[0]
            session["username"] = user[1]
            session["password"] = user[2]
            session["userType"] = user[3]
            flash("Welcome back! ", "success")
            return before_request()
        else:
            flash("Invilid username or password, please try again.", "danger")
            return redirect(url_for("auth.login"))
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    connection = getCursor()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        address = request.form.get("address")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")

        if not (
            username
            and password
            and first_name
            and last_name
            and address
            and email
            and phone_number
        ):
            flash("Please fill out the form!", "danger")
            return redirect(url_for("auth.register"))
        # hash the password by using werkzeug.security
        hashed_password = generate_password_hash(password)

        try:
            query = "INSERT INTO userauth (username, password_hash, userType) VALUES (%s, %s, %s)"
            connection.execute(query, (username, hashed_password, "Gardener"))
            new_id = connection.lastrowid
            affected_rows = connection.rowcount
            if new_id and affected_rows > 0:
                query = "INSERT INTO gardener (gardener_id, username, first_name, last_name, address, email, phone_number, date_joined, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                connection.execute(
                    query,
                    (
                        new_id,
                        username,
                        first_name,
                        last_name,
                        address,
                        email,
                        phone_number,
                        datetime.now(),
                        "Active",
                    ),
                )
                affected_rows = connection.rowcount
                if affected_rows > 0:
                    flash("Successfully register! ", "success")
                    return redirect(url_for("auth.login"))
        except Exception as e:
            if "Duplicate entry" in str(e):
                flash("Username already exists, please try another one.", "danger")
            else:
                flash(f"Error: {e}. Register failed. Please try again.", "danger")
            return redirect(url_for("auth.register"))
    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    # Remove session data, this will log the user out
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    session.pop("password", None)
    session.pop("userType", None)
    # Redirect to login page
    return redirect(url_for("home.home"))


# Change password for all roles
@auth_bp.route("/change_password", methods=["GET", "POST"])
def change_password():
    connection = getCursor()
    id = session["id"]
    profile_url = url_select()
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not (current_password and new_password and confirm_password):
            flash("Please fill out the form!", "danger")
            return redirect(url_for("auth.change_password"))
        # check if the entered current password is correct
        if not check_password_hash(session["password"], current_password):
            flash("Current Password is wrong! Please try again.", "danger")
            return redirect(url_for("auth.change_password"))
        if new_password != confirm_password:
            flash("New password do not match, please try again!", "danger")
            return redirect(url_for("auth.change_password"))
        hashed_new_password = generate_password_hash(new_password)

        try:
            query = "UPDATE userauth SET password_hash=%s WHERE id=%s"
            connection.execute(
                query,
                (
                    hashed_new_password,
                    id,
                ),
            )
            affected_rows = connection.rowcount
            if affected_rows > 0:
                session["password"] = hashed_new_password
                flash("Successfully change password! ", "success")
                return redirect(url_for("auth.change_password"))
            else:
                flash("Change password failed. Please try again.", "danger")
        except Exception as e:
            flash(f"Error: {e}. Change password failed. Please try again.", "danger")
    return render_template( "change_password.html", username=session["username"], userType=session["userType"],profile_url=profile_url,)
