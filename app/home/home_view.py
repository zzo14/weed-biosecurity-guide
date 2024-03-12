from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import Blueprint

home_bp = Blueprint("home", __name__, template_folder="templates")


# Home
@home_bp.route("/")
def home():
    if "loggedin" in session:
        if session["userType"] == "Gardener":
            return redirect(url_for("user.user_dashboard"))
        elif session["userType"] == "Staff":
            return redirect(url_for("admin_staff.staff_dashboard"))
        elif session["userType"] == "Admin":
            return redirect(url_for("admin_staff.admin_dashboard"))
    return render_template("home.html")
