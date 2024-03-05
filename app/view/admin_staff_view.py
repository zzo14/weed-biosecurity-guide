from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask import Blueprint
from werkzeug.security import generate_password_hash
from datetime import datetime
import re
from app.view.utils import getCursor
from app.view.utils import handle_user_data
from app.view.utils import url_select
from app.view.utils import handle_user_status

admin_staff = Blueprint('admin_staff', __name__)

@admin_staff.before_request
def before_request():
    if 'loggedin' not in session and request.endpoint in ['admin_staff.staff_profile', 'admin_staff.admin_profile', 'admin_staff.gardener_list', 'admin_staff.staff_list']:
        return redirect(url_for('home.home'))

#Staff and admin functions
@admin_staff.route('/staff_profile')
def staff_profile():
    # staff profile page
    if session['userType'] == 'Staff':
        connection = getCursor()
        id = session['id']
        query = "SELECT * FROM staff WHERE staff_id = %s"
        connection.execute(query, (id,))
        staff = connection.fetchone()
        return render_template("staff_profile.html", username=session['username'], userType=session['userType'], profile_url=url_for('admin_staff.staff_profile'), staff=staff)
    else:
        flash("Illegal Access!", "danger")
        return redirect(url_for('home.home'))

@admin_staff.route('/admin_profile')
def admin_profile():
    # staff profile page
    if session['userType'] == 'Admin':
        connection = getCursor()
        id = session['id']
        query = "SELECT * FROM administrator WHERE admin_id = %s"
        connection.execute(query, (id,))
        admin = connection.fetchone()
        return render_template("admin_profile.html", username=session['username'], userType=session['userType'], profile_url=url_for('admin_staff.admin_profile'), admin=admin)
    else:
        flash("Illegal Access!", "danger")
        return redirect(url_for('home.home'))

@admin_staff.route('/update_SA_profile', defaults={'staff_id': None}, methods=['GET', 'POST'])
@admin_staff.route('/update_SA_profile/<int:staff_id>', methods=['GET', 'POST'])
def update_SA_profile(staff_id):
    connection = getCursor()
    id = session['id']
    usertype = session['userType']
    profile_url = url_select()
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        work_phone = request.form.get('work_phone')
        email = request.form.get('email')
        position = request.form.get('position')
        department = request.form.get('department')

        if not (first_name and last_name and work_phone and email and position and department):
            flash("Please fill out the form!", "danger")
            return redirect(profile_url)
        if staff_id and session['userType'] != 'Admin':
            flash("You are not authorized to update other staff's profile.", "danger")
            return redirect(url_for('home.home'))
        
        try:
            # update the user profile by user types
            target_id = id
            direct_to = profile_url
            query = "UPDATE staff SET first_name=%s, last_name=%s, email=%s, work_phone=%s, position=%s, department=%s WHERE staff_id = %s "
            # if the user is admin, update the admin profile
            if usertype == 'Admin':
                query = "UPDATE administrator SET first_name=%s, last_name=%s, email=%s, work_phone=%s, position=%s, department=%s WHERE admin_id = %s "
                # if the user is admin and the staff_id is not None, meaning the admin is updating the staff profile
                if staff_id:
                    target_id = staff_id
                    direct_to = url_for('admin_staff.staff_list')
                    query = "UPDATE staff SET first_name=%s, last_name=%s, email=%s, work_phone=%s, position=%s, department=%s WHERE staff_id = %s "

            connection.execute(query, (first_name, last_name, email, work_phone, position, department, target_id))
            affected_rows = connection.rowcount
            if affected_rows > 0:
                flash("Successfully update! ", "success")
                return redirect(direct_to)
            else:
                flash("Update failed. Please try again.", "danger")
        except Exception as e:
            flash(f"Error: {e}. Update failed. Please try again.", "danger")
    return redirect(profile_url)

@admin_staff.route('/gardener_list')
def gardener_list():
    # admin/staff view gardener list
    if (session['userType'] == 'Staff' or session['userType'] == 'Admin'):
        profile_url = url_select()
        connection = getCursor()
        query = "SELECT * FROM gardener"
        connection.execute(query)
        gardeners_list = connection.fetchall()
        active_gardeners, inActive_gardeners = handle_user_data(gardeners_list)
        return render_template("gardener_list.html", username=session['username'], userType=session['userType'], profile_url=profile_url, active_gardeners=active_gardeners, inActive_gardeners=inActive_gardeners)
    else:
        flash("Illegal Access!", "danger")
        return redirect(url_for('home.home'))

@admin_staff.route('/gardener_list/add_new_gardener',  methods=['GET', 'POST'])
def add_new_gardener():
    connection = getCursor()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')

        if not (username and password and first_name and last_name and address and email and phone_number):
            flash("Please fill out the form!", "danger")
            return redirect(url_for('admin_staff.add_new_gardener'))
        hashed_password = generate_password_hash(password) 

        try:
            query = "INSERT INTO userauth (username, password_hash, userType) VALUES (%s, %s, %s)"
            connection.execute(query, (username, hashed_password, 'Gardener'))
            new_id = connection.lastrowid
            affected_rows = connection.rowcount
            if new_id and affected_rows > 0:
                query = "INSERT INTO gardener (gardener_id, username, first_name, last_name, address, email, phone_number, date_joined, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                connection.execute(query, (new_id, username, first_name, last_name, address, email, phone_number, datetime.now(), 'Active'))
                affected_rows = connection.rowcount
                if affected_rows > 0:
                    flash("Successfully add a new gardener! ", "success")
                    return redirect(url_for('admin_staff.gardener_list'))
            else:
                flash("Username already exists, please try another one.", "danger")
                return redirect(url_for('admin_staff.gardener_list'))
        except Exception as e:
            flash(f"Error: {e}. Add failed. Please try again.", "danger")
            return redirect(url_for('admin_staff.gardener_list'))
    return redirect(url_for('admin_staff.add_new_gardener'))

@admin_staff.route('/gardener_list/delete_gardener/<int:gardener_id>', methods=['GET', 'POST'])
def delete_gardener(gardener_id):
    connection = getCursor()
    if request.method == 'POST':
        # delete the gardener by setting the status to 'Inactive'
        if handle_user_status(connection, 'gardener', gardener_id, 'Inactive'):
            flash("Successfully delete the gardener!", "success")
            return redirect(url_for('admin_staff.gardener_list'))
        else:
            flash("Delete failed. Please try again.", "danger")
            return redirect(url_for('admin_staff.gardener_list'))
    return redirect(url_for('admin_staff.gardener_list'))

@admin_staff.route('/gardener_list/recover_gardener_account/<int:gardener_id>',methods=['GET', 'POST'])
def recover_gardener_account(gardener_id):
    # recover the gardener by setting the status to 'Active'
    connection = getCursor()
    if request.method == 'POST':
        if handle_user_status(connection, 'gardener', gardener_id, 'Active'):
            flash("Successfully recover the gardener!", "success")
            return redirect(url_for('admin_staff.gardener_list'))
        else:
            flash("Recover failed. Please try again.", "danger")
            return redirect(url_for('admin_staff.gardener_list'))
    return redirect(url_for('admin_staff.gardener_list'))

@admin_staff.route('/staff_list')
def staff_list():
    # admin view staff list
    if session['userType'] == 'Admin':
        connection = getCursor()
        query = "SELECT * FROM staff"
        connection.execute(query)
        staff_list = connection.fetchall()
        active_staffs, inActive_staffs = handle_user_data(staff_list)
        return render_template("staff_list.html", username=session['username'], userType=session['userType'], profile_url=url_for('admin_staff.admin_profile'), active_staffs=active_staffs, inActive_staffs=inActive_staffs)
    else:
        flash("Illegal Access!", "danger")
        return redirect(url_for('home.home'))

@admin_staff.route('/staff_list/add_new_staff',  methods=['GET', 'POST'])
def add_new_staff():
    connection = getCursor()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        work_phone = request.form.get('work_phone')
        email = request.form.get('email')
        position = request.form.get('position')
        department = request.form.get('department')

        if not (username and password and first_name and last_name and work_phone and email and position and department):
            flash("Please fill out the form!", "danger")
            return redirect(url_for('admin_staff.add_new_staff'))
        hashed_password = generate_password_hash(password) 

        try:
            query = "INSERT INTO userauth (username, password_hash, userType) VALUES (%s, %s, %s)"
            connection.execute(query, (username, hashed_password, 'Staff'))
            new_id = connection.lastrowid
            affected_rows = connection.rowcount
            if new_id and affected_rows > 0:
                query = "INSERT INTO staff (staff_id, username, first_name, last_name, email, work_phone, hire_date, position, department, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                connection.execute(query, (new_id, username, first_name, last_name, email, work_phone, datetime.now(), position, department, 'Active'))
                affected_rows = connection.rowcount
                if affected_rows > 0:
                    flash("Successfully add a new staff! ", "success")
                    return redirect(url_for('admin_staff.staff_list'))
            else:
                flash("Username already exists, please try another one.", "danger")
                return redirect(url_for('admin_staff.staff_list'))
        except Exception as e:
            flash(f"Error: {e}. Add failed. Please try again.", "danger")
            return redirect(url_for('admin_staff.staff_list'))
    return redirect(url_for('admin_staff.add_new_staff'))

@admin_staff.route('/staff_list/delete_staff/<int:staff_id>', methods=['GET', 'POST'])
def delete_staff(staff_id):
    # delete the staff, same as gargener
    connection = getCursor()
    if request.method == 'POST':
        if handle_user_status(connection, 'staff', staff_id, 'Inactive'):
            flash("Successfully delete the staff!", "success")
            return redirect(url_for('admin_staff.staff_list'))
        else:
            flash("Delete failed. Please try again.", "danger")
            return redirect(url_for('admin_staff.staff_list'))
    return redirect(url_for('admin_staff.staff_list'))

@admin_staff.route('/staff_list/recover_staff_account/<int:staff_id>',methods=['GET', 'POST'])
def recover_staff_account(staff_id):
    # recover the staff, same as gargener
    connection = getCursor()
    if request.method == 'POST':
        if handle_user_status(connection, 'staff', staff_id, 'Active'):
            flash("Successfully recover the staff!", "success")
            return redirect(url_for('admin_staff.staff_list'))
        else:
            flash("Recover failed. Please try again.", "danger")
            return redirect(url_for('admin_staff.staff_list'))
    return redirect(url_for('admin_staff.staff_list'))