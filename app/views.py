from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import re
from datetime import datetime
from datetime import timedelta
import mysql.connector
from mysql.connector import FieldType
import app.connect as connect
from . import app
import os


app.secret_key = 'key'
app.permanent_session_lifetime = timedelta(hours=24)
dbconn = None
connection = None
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/images/db')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

#Interface
@app.route("/")
def home():
    if 'loggedin' in session:
        if session['userType'] == 'Gardener':
            return redirect(url_for('gardener_profile'))
        elif session['userType'] == 'Staff':
            return redirect(url_for('staff_profile'))
        elif session['userType'] == 'Admin':
            return redirect(url_for('admin_profile'))
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    connection = getCursor()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        query = "SELECT * FROM userauth WHERE username = %s"
        connection.execute(query, (username,))
        user = connection.fetchone()
        if user and check_password_hash(user[2], password):
            session.permanent = True
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            session['password'] = user[2]
            session['userType'] = user[3]
            flash("Welcome back! ", "success")
            if session['userType'] == 'Gardener':
                return redirect(url_for('gardener_profile'))
            elif session['userType'] == 'Staff':
                return redirect(url_for('staff_profile'))
            elif session['userType'] == 'Admin':
                return redirect(url_for('admin_profile'))
            return redirect(url_for('login'))
        else:
            flash("Invilid username or password, please try again.", "danger")
    return render_template("accounts/login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
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
            return redirect(url_for('register'))

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,}$', password):
            flash("Password must be at least 8 characters long and conatin uppercase, lowercase, number and special characters.")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password) 
        query = "INSERT INTO userAuth (username, password_hash, userType) VALUES (%s, %s, %s)"
        connection.execute(query, (username, hashed_password, 'Gardener'))
        new_id = connection.lastrowid
        affected_rows = connection.rowcount
        if new_id and affected_rows > 0:
            query = "INSERT INTO gardener (gardener_id, username, first_name, last_name, address, email, phone_number, date_joined, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            connection.execute(query, (new_id, username, first_name, last_name, address, email, phone_number, datetime.now(), 'Active'))
            affected_rows = connection.rowcount
            if affected_rows > 0:
                flash("Successfully register! ", "success")
                return redirect(url_for('login'))
        else:
            flash("Username already exists, please try another one.", "danger")
    return render_template("accounts/register.html")

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('password', None)
   session.pop('userType', None)
   # Redirect to login page
   return redirect(url_for('home'))

@app.route('/gardener_profile', methods=['GET', 'POST'])
def gardener_profile():
    if 'loggedin' in session:
        connection = getCursor()
        id = session['id']
        query = "SELECT * FROM gardener WHERE gardener_id = %s"
        connection.execute(query, (id,))
        user = connection.fetchone()
        return render_template("gardener_profile.html", username=session['username'], userType=session['userType'], profile_url=url_for('gardener_profile'), user=user)
    else:
        return redirect(url_for('home'))

@app.route('/gardener_profile/update_gardener_profile', methods=['GET', 'POST'])
def update_gardener_profile():
    connection = getCursor()
    id = session['id']
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')

        if not (first_name and last_name and address and email and phone_number):
            flash("Please fill out the form!", "danger")
            return redirect(url_for('gardener_profile'))

        query = "UPDATE gardener SET first_name=%s, last_name=%s, address=%s, email=%s, phone_number=%s WHERE gardener_id = %s "
        connection.execute(query, (first_name, last_name, address, email, phone_number, id))
        affected_rows = connection.rowcount
        if affected_rows > 0:
            flash("Successfully update! ", "success")
            return redirect(url_for('gardener_profile'))
        else:
            flash("Update failed. Please try again.", "danger")
    return redirect(url_for('gardener_profile'))

@app.route('/staff_profile', methods=['GET', 'POST'])
def staff_profile():
    if 'loggedin' in session:
        if session['userType'] == 'Staff':
            connection = getCursor()
            id = session['id']
            query = "SELECT * FROM staff WHERE staff_id = %s"
            connection.execute(query, (id,))
            staff = connection.fetchone()
            return render_template("staff_profile.html", username=session['username'], userType=session['userType'], profile_url=url_for('staff_profile'), staff=staff)
        else:
            flash("Illegal Access!", "danger")
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/update_SA_profile', methods=['GET', 'POST'])
def update_SA_profile():
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
        
        if usertype == 'Admin':
            query = "UPDATE administration SET first_name=%s, last_name=%s, email=%s, work_phone=%s, position=%s, department=%s WHERE admin_id = %s "
        else:
            query = "UPDATE staff SET first_name=%s, last_name=%s, email=%s, work_phone=%s, position=%s, department=%s WHERE staff_id = %s "
        connection.execute(query, (first_name, last_name, email, work_phone, position, department, id))
        affected_rows = connection.rowcount
        if affected_rows > 0:
            flash("Successfully update! ", "success")
            return redirect(profile_url)
        else:
            flash("Update failed. Please try again.", "danger")
    return redirect(profile_url)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    connection = getCursor()
    id = session['id']
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,}$'
    profile_url = url_select()
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not (current_password and new_password and confirm_password):
            flash("Please fill out the form!", "danger")
            return redirect(url_for('change_password'))

        if not check_password_hash(session['password'], current_password):
            flash("Current Password is wrong! Please try again.", "danger")
            return redirect(url_for('change_password'))
        if not re.match(password_regex, new_password):
            flash("New password must be at least 8 characters long and conatin uppercase, lowercase, number and special characters.", "danger")
            return redirect(url_for('change_password'))
        if new_password != confirm_password:
            flash("New password do not mathc, please try again!", "danger")
            return redirect(url_for('change_password'))
        hashed_new_password = generate_password_hash(new_password)

        query = "UPDATE userAuth SET password_hash=%s WHERE id=%s"
        connection.execute(query, (hashed_new_password, id,))
        affected_rows = connection.rowcount
        if affected_rows > 0:
            flash("Successfully change password! ", "success")
            return redirect(url_for('change_password'))
        else:
            flash("Change password failed. Please try again.", "danger")
    return render_template("change_password.html", username=session['username'], userType=session['userType'], profile_url=profile_url)


@app.route('/weed_guide')
def weed_guide():
    profile_url = url_select()
    connection = getCursor()
    weed_query = "SELECT * FROM weedguide"
    weed_img_query = "SELECT * FROM weedimage"
    connection.execute(weed_query)
    weed_data = connection.fetchall()
    connection.execute(weed_img_query)
    weed_imgs = connection.fetchall()
    weed_guide = handle_weed_data(weed_data, weed_imgs)
    return render_template("weed_guide.html", username=session['username'], userType=session['userType'], profile_url=profile_url, weed_guide=weed_guide)

@app.route('/weed_guide/add_new_weed', methods=['GET', 'POST'])
def add_new_weed():
    connection = getCursor()
    if request.method == 'POST':
        common_name = request.form.get('common_name')
        scientific_name = request.form.get('scientific_name')
        weed_type = request.form.get('weed_type')
        description = request.form.get('description')
        impacts = request.form.get('impacts')
        control_methods = request.form.get('control_methods')
        primary_image = request.files.getlist('primary_image')
        more_images = request.files.getlist('more_image')

        
        if not (common_name and scientific_name and weed_type and description and impacts and control_methods and primary_image):
            flash("Please fill out the form!", "danger")
            return redirect(url_for('weed_guide'))
        
        query = "INSERT INTO weedGuide (common_name, scientific_name, weed_type, description, impacts, control_methods) VALUES (%s, %s, %s, %s, %s, %s)"
        connection.execute(query, (common_name, scientific_name, weed_type, description, impacts, control_methods))
        new_id = connection.lastrowid
        affected_rows = connection.rowcount

        if new_id and affected_rows > 0:
            query = "INSERT INTO weedImage (weed_id, image_name, is_primary) VALUES (%s, %s, %s)"
            primary_filename = save_image(primary_image)
            connection.execute(query, (new_id, primary_filename, 1))
            try:
                for image in more_images:
                    filename = save_image(image)
                    connection.execute(query, (new_id, filename, 0))
            except:
                pass
            affected_rows = connection.rowcount
            if affected_rows > 0:
                flash("Successfully add a new weed! ", "success")
                return redirect(url_for('weed_guide'))
        else:
            flash("Add failed. Please try again.", "danger")
    return redirect(url_for('weed_guide'))

@app.route('/weed_guide/update_weed/<int:weed_id>', methods=['GET', 'POST'])
def update_weed(weed_id):
    connection = getCursor()
    if request.method == 'POST':
        common_name = request.form.get('common_name')
        scientific_name = request.form.get('scientific_name')
        weed_type = request.form.get('weed_type')
        description = request.form.get('description')
        impacts = request.form.get('impacts')
        control_methods = request.form.get('control_methods')
        primary_image = request.form.get('set_primary_image')
        more_images = request.files.getlist('update_more_image')
            
        if not (common_name and scientific_name and weed_type and description and impacts and control_methods and primary_image):
            flash("Please fill out the form!", "danger")
            return redirect(url_for('weed_guide'))
        
        try:
            query = "UPDATE weedimage SET is_primary=0 WHERE weed_id=%s AND is_primary=1 AND image_name!=%s"
            connection.execute(query, (weed_id, primary_image,))
            affected_rows = connection.rowcount
            if affected_rows > 0:
                query = "UPDATE weedimage SET is_primary=1 WHERE weed_id=%s AND image_name=%s"
                connection.execute(query, (weed_id, primary_image,))
                
            query = "INSERT INTO weedImage (weed_id, image_name, is_primary) VALUES (%s, %s, %s)"
            try:
                for image in more_images:
                    filename = save_image(image)
                    connection.execute(query, (weed_id, filename, 0))
            except:
                pass
                
            query = "UPDATE weedguide SET common_name=%s, scientific_name=%s, weed_type=%s, description=%s, impacts=%s, control_methods=%s WHERE weed_id=%s"
            connection.execute(query, (common_name, scientific_name, weed_type, description, impacts, control_methods, weed_id))
            flash("Successfully update! ", "success")
        except:
            flash("Update failed. Please try again ", "danger")
    return redirect(url_for('weed_guide'))

@app.route('/weed_guide/delete_weed/<int:weed_id>', methods=['GET', 'POST'])
def delete_weed(weed_id):
    connection = getCursor()
    if request.method == 'POST':
        query = "DELETE FROM weedimage WHERE weed_id = %s"
        connection.execute(query, (weed_id,))
        affected_rows = connection.rowcount
        if affected_rows > 0:
            query = "DELETE FROM weedguide WHERE weed_id = %s"
            connection.execute(query, (weed_id,))
            affected_rows = connection.rowcount
            if affected_rows > 0:
                flash("Successfully delete the weed!", "success")
                return redirect(url_for('weed_guide'))
        else:
            flash("Delete failed. Please try again.", "danger")
    return redirect(url_for('weed_guide'))




def handle_weed_data(data, imgs):
    combined_data = []
    for weed in data:
        weed_data = [item.decode('utf-8') if isinstance(item, bytes) else item for item in weed]
        primary = []
        not_primary = []
        for img in imgs:
            if weed[0] == img[1]:
                img_data = [item.decode('utf-8') if isinstance(item, bytes) else item for item in img]
                if img[3] == 1:
                    primary.append(img_data[2]), 
                else:
                    not_primary.append(img_data[2])
        img_data = primary + not_primary
        weed_data.append(img_data)
        combined_data.append(weed_data)
    return combined_data

def save_image(file):
    filename = secure_filename(file.filename)
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(img_path)
    return filename


def url_select():
    user_type = session['userType']
    if user_type == 'Gardener':
        profile_url=url_for('gardener_profile')
    elif user_type == 'Staff':
        profile_url=url_for('staff_profile')
    elif user_type == 'Admin':
        profile_url=url_for('admin_profile')
    else:
        profile_url=url_for('home')
    return profile_url