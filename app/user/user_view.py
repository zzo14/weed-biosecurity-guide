from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask import Blueprint
from app.utils import getCursor

user_bp = Blueprint("user", __name__, template_folder="templates")


@user_bp.before_request
def before_request():
    if "loggedin" not in session and request.endpoint in ["user.gardener_profile"]:
        flash("Illegal Access!", "danger")
        return redirect(url_for("home.home"))


@user_bp.route("/user_dashboard")
def user_dashboard():
    if session["userType"] == "Gardener":
        return render_template("user_dashboard.html", username=session["username"], userType=session["userType"], profile_url=url_for("user.gardener_profile"),)
    else:
        flash("Illegal Access!", "danger")
        return redirect(url_for("home.home"))

# User functions
@user_bp.route("/gardener_profile")
def gardener_profile():
    if session["userType"] == "Gardener":
        connection = getCursor()
        id = session["id"]
        query = "SELECT * FROM gardener WHERE gardener_id = %s"
        connection.execute(query, (id,))
        user = connection.fetchone()
        return render_template(
            "gardener_profile.html", username=session["username"], userType=session["userType"], profile_url=url_for("user.gardener_profile"), user=user,)
    else:
        flash("Illegal Access!", "danger")
        return redirect(url_for("home.home"))

@user_bp.route("/gardener_profile/update_gardener_profile", defaults={"gardener_id": None}, methods=["GET", "POST"],)
@user_bp.route("/gardener_profile/update_gardener_profile/<int:gardener_id>", methods=["GET", "POST"],)
def update_gardener_profile(gardener_id):
    connection = getCursor()
    id = session["id"]
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        address = request.form.get("address")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")

        if not (first_name and last_name and address and email and phone_number):
            flash("Please fill out the form!", "danger")
            return redirect(url_for("user.gardener_profile"))
        if gardener_id and session["userType"] != "Admin":
            flash("You are not authorized to update other gardener's profile.", "danger")
            return redirect(url_for("home.home"))

        try:
            # update gardener profile by admin/staff
            if gardener_id:
                target_id = gardener_id
                direct_to = url_for("admin_staff.gardener_list")
            # update gardener profile by gardener
            else:
                target_id = id
                direct_to = url_for("user.gardener_profile")
            query = "UPDATE gardener SET first_name=%s, last_name=%s, address=%s, email=%s, phone_number=%s WHERE gardener_id = %s "
            connection.execute(query, (first_name, last_name, address, email, phone_number, target_id))
            affected_rows = connection.rowcount
            if affected_rows > 0:
                flash("Successfully update! ", "success")
            else:
                flash("No change in profile. Please try again.", "danger")
        except Exception as e:
            flash(f"Error: {e}. Update failed. Please try again.", "danger")
    return redirect(direct_to)
