from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask import Blueprint
from flask import current_app
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime
import re
from app.view.utils import getCursor
from app.view.utils import url_select
from app.view.utils import handle_weed_data
from app.view.utils import save_image
import os

weed = Blueprint('weed', __name__)

# Weed guide functions
@weed.route('/weed_guide')
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

@weed.route('/weed_guide/add_new_weed', methods=['GET', 'POST'])
def add_new_weed():
    connection = getCursor()
    if request.method == 'POST':
        common_name = request.form.get('common_name')
        scientific_name = request.form.get('scientific_name')
        weed_type = request.form.get('weed_type')
        description = request.form.get('description')
        impacts = request.form.get('impacts')
        control_methods = request.form.get('control_methods')
        primary_image = request.files.get('primary_image')
        more_images = request.files.getlist('more_image')

        
        if not (common_name and scientific_name and weed_type and description and impacts and control_methods and primary_image):
            flash("Please fill out the form!", "danger")
            return redirect(url_for('weed.weed_guide'))
        try:
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
                    return redirect(url_for('weed.weed_guide'))
            else:
                flash("Add failed. Please try again.", "danger")
        except Exception as e:
            flash(f"Error: {e}.Add failed. Please try again.", "danger")
    return redirect(url_for('weed.weed_guide'))

@weed.route('/weed_guide/update_weed/<int:weed_id>', methods=['GET', 'POST'])
def update_weed(weed_id):
    connection = getCursor()
    if request.method == 'POST':
        print(request.form)
        common_name = request.form.get('common_name')
        scientific_name = request.form.get('scientific_name')
        weed_type = request.form.get('weed_type')
        description = request.form.get('description')
        impacts = request.form.get('impacts')
        control_methods = request.form.get('control_methods')
        primary_image = request.form.get('set_primary_image')
        more_images = request.files.getlist('update_more_image')
        images_to_delete = request.form.get("images_to_delete")
        print(images_to_delete)
            
        if not (common_name and scientific_name and weed_type and description and impacts and control_methods and primary_image):
            flash("Please fill out the form!", "danger")
            return redirect(url_for('weed.weed_guide'))
        
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

            if images_to_delete:
                images_to_delete_list = images_to_delete.split(',')
                query = "DELETE FROM weedimage WHERE weed_id = %s AND image_name = %s AND is_primary=0"
                for image_name in images_to_delete_list:
                    connection.execute(query, (weed_id, image_name,))
                    affected_rows = connection.rowcount
                    if affected_rows > 0:
                        img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_name)
                        if os.path.exists(img_path):
                            os.remove(img_path)
            flash("Successfully update! ", "success")
        except Exception as e:
            flash(f"Error: {e}. Update failed. Please try again ", "danger")
    return redirect(url_for('weed.weed_guide'))

@weed.route('/weed_guide/delete_weed/<int:weed_id>', methods=['GET', 'POST'])
def delete_weed(weed_id):
    connection = getCursor()
    if request.method == 'POST':
        query = "SELECT image_name FROM weedimage WHERE weed_id = %s"
        connection.execute(query, (weed_id,))
        images = connection.fetchall()

        query = "DELETE FROM weedguide WHERE weed_id = %s"
        connection.execute(query, (weed_id,))
        affected_rows = connection.rowcount
        if affected_rows > 0:
            for image in images:
                img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image[0])
                if os.path.exists(img_path):
                    os.remove(img_path)
            flash("Successfully delete the weed!", "success")
            return redirect(url_for('weed.weed_guide'))
        else:
            flash("Delete failed. Please try again.", "danger")
    return redirect(url_for('weed.weed_guide'))