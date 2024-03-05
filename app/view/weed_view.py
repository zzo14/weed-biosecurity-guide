from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask import Blueprint
from flask import current_app
from app.view.utils import getCursor
from app.view.utils import url_select
from app.view.utils import handle_weed_data
from app.view.utils import save_image
from app.view.utils import allowed_file
import os

weed = Blueprint('weed', __name__)

@weed.before_request
def before_request():
    if 'loggedin' not in session and request.endpoint in ['weed.weed_guide']:
        return redirect(url_for('home.home'))

# Weed guide functions
@weed.route('/weed_guide')
def weed_guide():
    # fetch the weed guide data from the database
    profile_url = url_select()
    connection = getCursor()
    query = "SELECT g.*, i.image_id, i.image_name, i.is_primary FROM biosercurity.weedguide g JOIN biosercurity.weedimage i ON g.weed_id = i.weed_id Order by weed_id ASC, is_primary DESC;"
    try:
        connection.execute(query)
        weed_data = connection.fetchall()
        if not weed_data:
            flash("No weeds found in the database.", "info")
    except Exception as e:
        flash(f"Database error: {e}", "danger")
        return redirect(url_for('home.home'))
    weed_guide = handle_weed_data(weed_data)
    return render_template("weed_guide.html", username=session['username'], userType=session['userType'], profile_url=profile_url, weed_guide=weed_guide)

@weed.route('/weed_guide/add_new_weed', methods=['GET', 'POST'])
def add_new_weed():
    # add a new weed to the database
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
        # check if the file is image
        if not allowed_file(primary_image) or (more_images[0].filename != "" and not allowed_file(more_images)):
            flash("Please upload valid images.", "danger")
            return redirect(url_for('weed.add_new_weed'))
        try:
            # insert the weed data to the weedguide table
            query = "INSERT INTO weedGuide (common_name, scientific_name, weed_type, description, impacts, control_methods) VALUES (%s, %s, %s, %s, %s, %s)"
            connection.execute(query, (common_name, scientific_name, weed_type, description, impacts, control_methods))
            new_id = connection.lastrowid
            affected_rows = connection.rowcount

            # insert the image data to the weedimage table
            if new_id and affected_rows > 0:
                query = "INSERT INTO weedImage (weed_id, image_name, is_primary) VALUES (%s, %s, %s)"
                primary_filename = save_image(primary_image)
                connection.execute(query, (new_id, primary_filename, 1))
                try:
                    for image in more_images:
                        if image.filename != "":
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
    # update the weed data in the database
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
        images_to_delete = request.form.get("images_to_delete")
        
        if not (common_name and scientific_name and weed_type and description and impacts and control_methods and primary_image):
            flash("Please fill out the form!", "danger")
            return redirect(url_for('weed.weed_guide'))
        # check if the file is image
        if more_images[0].filename != "" and not allowed_file(more_images):
            flash("Please upload valid images.", "danger")
            return redirect(url_for('weed.add_new_weed'))
        
        try:
            # if the primary image is changed to another image
            query = "UPDATE weedimage SET is_primary=0 WHERE weed_id=%s AND is_primary=1 AND image_name!=%s"
            connection.execute(query, (weed_id, primary_image,))
            affected_rows = connection.rowcount
            if affected_rows > 0:
                # primary has changed, so update the new image as primary
                query = "UPDATE weedimage SET is_primary=1 WHERE weed_id=%s AND image_name=%s"
                connection.execute(query, (weed_id, primary_image,))
            #insert the new images to the weedimage table
            query = "INSERT INTO weedImage (weed_id, image_name, is_primary) VALUES (%s, %s, %s)"
            try:
                for image in more_images:
                    if image.filename != "":
                        filename = save_image(image)
                        connection.execute(query, (weed_id, filename, 0))
            except:
                pass

            # update the weed data in the weedguide table 
            query = "UPDATE weedguide SET common_name=%s, scientific_name=%s, weed_type=%s, description=%s, impacts=%s, control_methods=%s WHERE weed_id=%s"
            connection.execute(query, (common_name, scientific_name, weed_type, description, impacts, control_methods, weed_id))
            if images_to_delete:
                images_to_delete_list = images_to_delete.split(',')
                # only delete a image if it is not primary
                query = "DELETE FROM weedimage WHERE weed_id = %s AND image_name = %s AND is_primary=0"
                for image_name in images_to_delete_list:
                    connection.execute(query, (weed_id, image_name,))
                    affected_rows = connection.rowcount
                    if affected_rows > 0:
                        # delete the images from the static folder
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
        # get the images name which are going to be deleted from database
        query = "SELECT image_name FROM weedimage WHERE weed_id = %s"
        connection.execute(query, (weed_id,))
        images = connection.fetchall()

        query = "DELETE FROM weedguide WHERE weed_id = %s"
        connection.execute(query, (weed_id,))
        affected_rows = connection.rowcount
        if affected_rows > 0:
            for image in images:
                # delete the images from the static folder
                img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image[0])
                if os.path.exists(img_path):
                    os.remove(img_path)
            flash("Successfully delete the weed!", "success")
            return redirect(url_for('weed.weed_guide'))
        else:
            flash("Delete failed. Please try again.", "danger")
    return redirect(url_for('weed.weed_guide'))