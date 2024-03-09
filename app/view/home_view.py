from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import Blueprint

home_bp = Blueprint("home", __name__)


# Home
@home_bp.route("/")
def home():
    if "loggedin" in session:
        if session["userType"] == "Gardener":
            return redirect(url_for("user.gardener_profile"))
        elif session["userType"] == "Staff":
            return redirect(url_for("admin_staff.staff_profile"))
        elif session["userType"] == "Admin":
            return redirect(url_for("admin_staff.admin_profile"))
    return render_template("home.html")
