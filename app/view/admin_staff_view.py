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

admin_staff = Blueprint('admin_staff', __name__)

#Staff and admin functions
@admin_staff.route('/staff_profile')
def staff_profile():
    if 'loggedin' in session:
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
    else:
        return redirect(url_for('home.home'))

@admin_staff.route('/admin_profile')
def admin_profile():
    if 'loggedin' in session:
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
    else:
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
        
        try:
            target_id = id
            direct_to = profile_url
            query = "UPDATE staff SET first_name=%s, last_name=%s, email=%s, work_phone=%s, position=%s, department=%s WHERE staff_id = %s "
            if usertype == 'Admin':
                query = "UPDATE administrator SET first_name=%s, last_name=%s, email=%s, work_phone=%s, position=%s, department=%s WHERE admin_id = %s "
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
    if 'loggedin' in session and (session['userType'] == 'Staff' or session['userType'] == 'Admin'):
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

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,}$', password):
            flash("Password must be at least 8 characters long and conatin uppercase, lowercase, number and special characters.")
            return redirect(url_for('admin_staff.add_new_gardener'))

        hashed_password = generate_password_hash(password) 

        try:
            query = "INSERT INTO userAuth (username, password_hash, userType) VALUES (%s, %s, %s)"
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
        except Exception as e:
            flash(f"Error: {e}. Add failed. Please try again.", "danger")
    return redirect(url_for('admin_staff.add_new_gardener'))

@admin_staff.route('/gardener_list/delete_gardener/<int:gardener_id>', methods=['GET', 'POST'])
def delete_gardener(gardener_id):
    connection = getCursor()
    if request.method == 'POST':
        query = "UPDATE gardener SET status='Inactive' WHERE gardener_id = %s"
        connection.execute(query, (gardener_id,))
        affected_rows = connection.rowcount
        if affected_rows > 0:
            flash("Successfully delete the gardener!", "success")
            return redirect(url_for('admin_staff.gardener_list'))
        else:
            flash("Delete failed. Please try again.", "danger")
    return redirect(url_for('admin_staff.gardener_list'))

@admin_staff.route('/gardener_list/recover_gardener_account/<int:gardener_id>',methods=['GET', 'POST'])
def recover_gardener_account(gardener_id):
    connection = getCursor()
    if request.method == 'POST':
        query = "UPDATE gardener SET status='Active' WHERE gardener_id = %s"
        connection.execute(query, (gardener_id,))
        affected_rows = connection.rowcount
        if affected_rows > 0:
            flash("Successfully recover the gardener!", "success")
            return redirect(url_for('admin_staff.gardener_list'))
        else:
            flash("Recover failed. Please try again.", "danger")
    return redirect(url_for('admin_staff.gardener_list'))

@admin_staff.route('/staff_list')
def staff_list():
    if 'loggedin' in session and session['userType'] == 'Admin':
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

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,}$', password):
            flash("Password must be at least 8 characters long and conatin uppercase, lowercase, number and special characters.")
            return redirect(url_for('admin_staff.add_new_staff'))

        hashed_password = generate_password_hash(password) 

        try:
            query = "INSERT INTO userAuth (username, password_hash, userType) VALUES (%s, %s, %s)"
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
        except Exception as e:
            flash(f"Error: {e}. Add failed. Please try again.", "danger")
    return redirect(url_for('admin_staff.add_new_staff'))

@admin_staff.route('/staff_list/delete_staff/<int:staff_id>', methods=['GET', 'POST'])
def delete_staff(staff_id):
    connection = getCursor()
    if request.method == 'POST':
        query = "UPDATE staff SET status='Inactive' WHERE staff_id = %s"
        connection.execute(query, (staff_id,))
        affected_rows = connection.rowcount
        if affected_rows > 0:
            flash("Successfully delete the gardener!", "success")
            return redirect(url_for('admin_staff.staff_list'))
        else:
            flash("Delete failed. Please try again.", "danger")
    return redirect(url_for('admin_staff.staff_list'))

@admin_staff.route('/staff_list/recover_staff_account/<int:staff_id>',methods=['GET', 'POST'])
def recover_staff_account(staff_id):
    connection = getCursor()
    if request.method == 'POST':
        query = "UPDATE staff SET status='Active' WHERE staff_id = %s"
        connection.execute(query, (staff_id,))
        affected_rows = connection.rowcount
        if affected_rows > 0:
            flash("Successfully recover the staff!", "success")
            return redirect(url_for('admin_staff.staff_list'))
        else:
            flash("Recover failed. Please try again.", "danger")
    return redirect(url_for('admin_staff.staff_list'))