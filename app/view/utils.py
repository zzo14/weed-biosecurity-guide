from flask import Flask
from flask import session
from flask import url_for
from flask import current_app
import mysql.connector
import app.connect as connect
from werkzeug.utils import secure_filename
import os

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

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
    img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(img_path)
    return filename

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
