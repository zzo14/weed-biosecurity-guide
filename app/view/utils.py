from flask import Flask
from flask import session
from flask import url_for
from flask import current_app
import mysql.connector
import app.connect as connect
from werkzeug.utils import secure_filename
from datetime import datetime
import os

dbconn = None
connection = None
ALLOWED_EXTENSIONS = {'png', 'jpg','jpeg','gif'}

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

def handle_weed_data(weed_data):
    combined_data = {}
    for weed in weed_data:
        weed_id = weed[0]
        if weed_id not in combined_data:
            combined_data[weed_id] = {
                'common_name': weed[1],
                'scientific_name': weed[2],
                'weed_type': weed[3],
                'description': weed[4],
                'impacts': weed[5],
                'control_methods': weed[6],
                'images': [weed[8]],
            }
        else:
            combined_data[weed_id]['images'].append(weed[8])
    return combined_data

def allowed_file(file):
    result = True
    if type(file) == list:
        for f in file:
            result = '.' in f.filename and f.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            if not result:
                break
    else:
        result = '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return result

def save_image(file):
    filename = secure_filename(file.filename)
    timeStamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_name = f"{timeStamp}_{filename}"
    img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
    file.save(img_path)
    return unique_name

def url_select():
    user_type = session['userType']
    if user_type == 'Gardener':
        profile_url=url_for('user.gardener_profile')
    elif user_type == 'Staff':
        profile_url=url_for('admin_staff.staff_profile')
    elif user_type == 'Admin':
        profile_url=url_for('admin_staff.admin_profile')
    else:
        profile_url=url_for('home')
    return profile_url

def handle_user_data(role_list):
    active_roles = []
    inactive_roles = []
    for user in role_list:
        if user[-1] == 'Active':
            active_roles.append(user)
        else:
            inactive_roles.append(user)
    return active_roles, inactive_roles
